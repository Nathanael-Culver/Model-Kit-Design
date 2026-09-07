# USS Defiant — Power Architecture

**Document status:** RECONSTRUCTED REQUIREMENTS / NOT YET FROZEN  
**Architecture freeze gate:** CLOSED pending exact module inspection and bench checks.

## 1. Locked functional architecture

The following are requirements, not proposals:

1. `BT1` remains connected to `U1` (XIAO ESP32-C3) so the MCU can remain alive in deep sleep.
2. The XIAO uses deep sleep for low standby current.
3. The 5 V lighting subsystem is not energized during deep sleep.
4. The MFRC522 subsystem is not energized during deep sleep.
5. `RX1` wireless-power-present must be sensed by `U1` and must be capable of waking the MCU.
6. Wireless power must provide a recovery/charging path when BT1 is too depleted for normal model operation.
7. The sealed model must retain Wi-Fi/BLE control and wireless firmware update capability.

## 2. Named voltage domains

| Net/domain | Nominal range | Source | Consumers | State during deep sleep | Status |
|---|---:|---|---|---|---|
| `GND` | 0 V | common reference | all subsystems | connected | LOCKED common-ground requirement |
| `BAT+` | about 3.0–4.2 V | BT1 | U1 battery input; candidate U2 input | present | LOCKED battery domain |
| `WLC_5V_RAW` | seller-rated 5 V | RX1 | candidate charge/power-input path; presence detector | only when transmitter coupled | RECONSTRUCTED name; exact loaded voltage must be measured |
| `SYS_5V_IN` | approximately 5 V less isolation-diode drop | candidate D1 output | U1 5 V/VBUS input path | when wireless power present | PROVISIONAL until XIAO/module bench validation |
| `+3V3_ALWAYS` | 3.3 V | U1 onboard regulator | always-on sensing/control only | present | PROVISIONAL name; loading must remain small |
| `+5V_LIGHT_SW` | 5.0 V target | U2 MT3608 | SK6812 RGBW and any 5 V logic buffer | OFF | LOCKED behavior; implementation OPEN |
| `+3V3_NFC_SW` | 3.3 V | switched from XIAO 3.3 V or equivalent | U3 MFRC522 module | OFF | LOCKED behavior; implementation OPEN |

## 3. Baseline topology under review

This is the current textual candidate and must not be turned into final drawings yet.

```text
BT1 3.7 V LiPo
  ├──> U1 XIAO battery pads  [always connected]
  └──> U2 MT3608 input path  [gated or EN-controlled]
         └──> +5V_LIGHT_SW
               ├──> SK6812 lighting
               └──> SN74AHCT1G125 data-buffer VCC

U1 +3V3
  └──> NFC high-side gate
         └──> +3V3_NFC_SW
               └──> U3 MFRC522

RX1 wireless receiver
  └──> WLC_5V_RAW
         ├──> protected/isolation path -> U1 5 V input / onboard charger path
         └──> resistor-divider / protection -> wake-capable U1 GPIO
```

## 4. Lighting-rail gate implementation decision

Two implementation paths exist; **one must be selected after the exact MT3608 module is inspected**.

### Path A — use MT3608 EN (preferred only if physically accessible and the module behaves correctly)

The MT3608 IC has an EN input (pin 4): high = enabled, low = disabled. If the purchased board exposes EN or can be modified cleanly, the MCU can disable the boost converter without an external high-side input switch.

Required bench checks:

- EN really controls the module without another hard pull-up defeating it.
- shutdown current of the complete module is acceptable, not merely the bare IC specification.
- output does not backfeed through connected 5 V loads.

### Path B — physically gate MT3608 input with purchased MOSFETs

If EN is inaccessible/unacceptable, use an AO3401A P-channel device as the high-side switch on `BAT+ -> U2 VIN`, with an AO3400A N-channel helper to pull the P-channel gate low. A pull-up from the AO3401A gate to `BAT+` gives a default-OFF state while U1 resets/sleeps.

This two-device method is important on a battery-domain P-channel switch because U1 GPIO HIGH is about 3.3 V while BT1 can reach 4.2 V; directly driving the P-channel gate from the GPIO may not guarantee a sufficiently small |VGS| for a hard OFF state at full charge.

**Status:** PROVISIONAL engineering solution using already-purchased parts; do not assign final Q/R designators until Path A/B is selected.

## 5. NFC power gate

U3 must be OFF in deep sleep.

Candidate implementation: AO3401A high-side switch from `+3V3_ALWAYS` to `+3V3_NFC_SW`, with a source-to-gate pull-up for default OFF. Because source and MCU logic-high are both approximately 3.3 V, direct GPIO gate control may be possible; exact control polarity and boot state will be validated before freeze.

**Open question:** separate NFC and lighting enables consume two GPIOs. A shared enable would save a GPIO but changes control granularity. This must be resolved during pin-budget review, not silently assumed.

## 6. Wireless-power input and wake/recovery path

### Requirements

- `WLC_5V_RAW` must not exceed any U1 GPIO rating.
- Presence detection therefore requires a divider/protection network; direct 5 V-to-GPIO connection is prohibited.
- The chosen presence GPIO must support deep-sleep wake on the XIAO ESP32-C3. Seeed documents wake-capable board pins D0–D3.
- The detect network must not pull a boot-strapping pin into an invalid reset state.
- Wireless input must not create an uncontrolled reverse-current path into RX1 when wireless power is absent.

### Candidate power-input isolation

A purchased PMEG2010ER Schottky is a candidate series isolation diode between `WLC_5V_RAW` and the XIAO 5 V input path. This matches Seeed's requirement to use a diode when applying an external source to the XIAO 5 V pin, but the exact connection is **PROVISIONAL until bench validation** of the exact board and receiver.

### Recovery sequence target

1. BT1 depleted / U1 unable to run normally.
2. User applies the XKT transmitter.
3. RX1 produces `WLC_5V_RAW`.
4. U1 receives external 5 V power through the validated isolation path and the onboard battery-management circuit can recharge BT1.
5. U1 detects wireless-power-present after it boots/wakes.
6. Firmware enters a charge/recovery-aware state rather than blindly enabling the lighting rail at maximum load.

## 7. Power-up/down defaults

The hardware must be fail-safe before firmware configures GPIOs:

- lighting rail: default OFF
- NFC rail: default OFF
- phasers: default OFF
- SK6812 data buffer output: disabled or benign until 5 V lighting rail is valid
- no GPIO may be forced into an invalid ESP32-C3 boot strap during reset

## 8. Architecture-freeze tests

Before changing this document to **FROZEN**:

- measure RX1 unloaded and loaded output voltage/current behavior;
- verify RX1 polarity/pads;
- verify U1 charging from the proposed wireless-input path;
- verify no reverse feed into RX1;
- inspect U2 EN accessibility and measure full-module shutdown draw;
- verify U3 module supply current and power-off SPI-pin behavior;
- confirm selected MOSFET gate topology powers up OFF;
- measure +5V_LIGHT_SW under representative SK6812 load;
- verify U1 can wake from the selected wireless-present pin;
- verify normal boot with every external circuit connected.
