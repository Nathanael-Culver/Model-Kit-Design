# USS Defiant — Power / Electrical Architecture

**Document status:** **FROZEN v1.0 — functional/topology architecture**  
**Drawing gate:** remains CLOSED until netlist/pinout/validation are approved.  
**Rule:** physical module pin labels, passive values, and exact carrier wiring may still be verified later, but the block-level architecture below is now authoritative unless a documented engineering change is approved.

## 1. Frozen system concept

The Defiant is a sealed, battery-powered model controlled by `U1` (Seeed Studio XIAO ESP32-C3).

- `BT1` remains permanently connected to U1.
- U1 enters deep sleep for standby.
- All high-draw lighting hardware is physically power-gated OFF in deep sleep.
- MFRC522 NFC hardware is physically power-gated OFF in deep sleep.
- Wireless-power presence wakes U1 and provides the charging/recovery input.
- The nine accepted addressable lighting zones use **one SK6812 serial data bus**. Physical emitter count/order may differ from logical zone count and is resolved later from hull layout.
- The four pulse phasers remain four independent conventional LED channels.
- No GPIO expander, touch sensor, audio system, or additional controller is part of the frozen architecture.

## 2. Frozen voltage domains

| Net/domain | Source | Main consumers | Deep-sleep state |
|---|---|---|---|
| `GND` | common system reference | all electronics | connected |
| `BAT+` | BT1, ~3.0–4.2 V operating range | U1 battery input; switched lighting-input path | present |
| `WLC_5V_RAW` | RX1 wireless receiver | U1 charging/recovery input through isolation; presence detector | present only while coupled to transmitter |
| `SYS_5V_IN` | isolated `WLC_5V_RAW` | U1 external 5 V / charger input path | present only while charging |
| `+3V3_ALWAYS` | U1 onboard 3.3 V regulator | low-current control/sensing circuitry | present while U1 is powered |
| `+5V_LIGHT_SW` | U2 MT3608, fed through a high-side battery gate | SK6812s, AHCT data buffer, phaser LED supply | **OFF** |
| `+3V3_NFC_SW` | high-side switched `+3V3_ALWAYS` | U3 MFRC522 | **OFF** |

## 3. Battery and controller path — frozen

```text
BT1 LiPo
  ├──> U1 XIAO BAT input  [permanent connection]
  └──> lighting high-side switch -> U2 MT3608 -> +5V_LIGHT_SW
```

U1 stays connected to BT1 at all times and is responsible for control, Wi-Fi/BLE, OTA, deep sleep, wake handling, addressable-lighting data, phasers, and NFC SPI.

### Battery protection safety gate

The architecture requires normal single-cell LiPo over-charge/over-discharge/short-circuit protection. Whether BT1 already includes that protection is still physically unverified. If BT1 is a protected pack, no added protector is required. If it is an unprotected bare pouch cell, a suitable 1S protection device/module becomes mandatory before final assembly. This is a safety requirement, not an optional feature.

## 4. Wireless charging / recovery / wake — frozen

```text
TX1 XKT-412 ))) RX1
                 │
                 └── WLC_5V_RAW
                       ├──> Schottky isolation -> SYS_5V_IN -> U1 5V/charger input
                       └──> resistor-divider/protection -> WLC_PRESENT
                                                    ├──> one wake-capable U1 GPIO
                                                    └──> NFC hardware inhibit
```

Frozen behavior:

1. Wireless power is **not** the main 5 V lighting supply. Lighting remains battery -> switched MT3608.
2. Wireless power feeds U1's validated external-power/charging path through a Schottky isolation device.
3. `WLC_PRESENT` is a protected 3.3 V-domain logic signal derived from the receiver output; 5 V is never connected directly to an ESP32-C3 GPIO.
4. `WLC_PRESENT` uses one of the XIAO's deep-sleep wake-capable GPIOs.
5. If BT1 is deeply depleted, coupling to TX1 provides the recovery/charging path for U1/BT1.
6. RX1's seller 5 V/2 A claim is not treated as guaranteed until load-tested.

## 5. Lighting power gate — frozen topology

**The final design uses true high-side input disconnect for U2. MT3608 EN alone is not the primary sleep isolation method.**

```text
BAT+ -> AO3401A P-MOS high-side switch -> U2 MT3608 VIN -> +5V_LIGHT_SW
                ^
                |
        AO3400A N-MOS helper
                ^
                |
           PERIPH_EN
```

- AO3401A provides the physical battery disconnect to U2.
- AO3400A pulls the P-channel gate low when `PERIPH_EN` is asserted.
- A gate pull-up to `BAT+` makes the lighting rail hardware-default OFF during reset, boot, and deep sleep.
- Exact gate/pull resistor values are assigned during the netlist/passive-design step.
- U2 output is adjusted/tested to 5.0 V before LEDs are connected.

## 6. Addressable lighting — frozen architecture

One XIAO GPIO drives one 5 V-level-shifted SK6812 serial bus:

```text
U1 SK_DATA_RAW
      │
      v
SN74AHCT1G125DBVR
  VCC = +5V_LIGHT_SW
      │
      v
series data resistor
      │
      v
SK6812 -> SK6812 -> ... -> final physical emitter
```

Frozen rules:

- **One independent SK6812 data line only.**
- One SN74AHCT1G125DBVR is therefore required in the final architecture.
- Its `OE` does **not** consume an MCU GPIO; it is hardware-configured so the buffer is usable whenever the switched 5 V rail is valid.
- The buffer gets a local ceramic bypass capacitor.
- Historical 330 Ω data-series and 470 µF bulk-capacitor values remain provisional until the passive calculation/review step.
- The nine logical zones P0–P8 are preserved; firmware maps physical emitter indices/groups to those logical zones.

## 7. Pulse-phaser architecture — frozen

There are four independent conventional white-LED channels:

```text
+5V_LIGHT_SW -> current-limit network -> phaser LED -> AO3400A -> GND
                                                     ^
                                                     |
                                              U1 PHx_GATE
```

- Four phasers = four AO3400A low-side switch channels.
- Each channel consumes one U1 GPIO.
- Each gate receives a hardware default-OFF pull-down.
- Exact LED resistor values are **not** frozen until the actual prewired 0805 LEDs are measured/identified.
- Phaser LEDs are powered from the switched lighting rail, so they are physically dead in deep sleep.

## 8. NFC architecture — frozen

U3 remains the MFRC522 SPI module.

Required MCU signals:

- `NFC_SCK`
- `NFC_MOSI`
- `NFC_MISO`
- `NFC_CS`

No dedicated MCU GPIO is allocated to MFRC522 IRQ or reset.

### NFC supply gate

```text
+3V3_ALWAYS -> AO3401A P-MOS -> +3V3_NFC_SW -> U3 MFRC522
                       ^
                       |
                AO3400A enable helper
                       ^
                       |
            conditioned PERIPH_EN
```

The NFC rail is default OFF and physically disconnected in deep sleep.

### NFC reset

MFRC522 reset/power-down is handled by the switched-power/reset arrangement rather than consuming a dedicated U1 GPIO. Exact passive connection to the breakout's RST/NRSTPD pin is finalized after the exact module header is verified.

### Wireless-power / NFC interlock — frozen requirement

The MFRC522 must **not operate while wireless charging is present**. To enforce this without spending another MCU GPIO, `WLC_PRESENT` also acts as a hardware inhibit on the NFC gate:

```text
NFC power allowed = PERIPH_EN AND NOT WLC_PRESENT
```

Implementation uses the already-purchased AO3400A/AO3401A devices and resistors; no new logic IC is required. This permits the 5 V lighting rail to remain available while docked/charging, while NFC stays physically off.

## 9. Master peripheral enable / GPIO budget — frozen concept

The design uses **one MCU `PERIPH_EN` output** for peripheral-power control.

Functional GPIO budget:

| Function | GPIO count |
|---|---:|
| one SK6812 serial data bus | 1 |
| four independent phasers | 4 |
| MFRC522 SPI: SCK/MOSI/MISO/CS | 4 |
| `WLC_PRESENT` wake input | 1 |
| `PERIPH_EN` | 1 |
| **Total** | **11** |

This intentionally uses the XIAO's full exposed GPIO budget but requires no GPIO expander. Final assignment to D0–D10 is Step 6 and must account for ESP32-C3 strapping/boot behavior.

## 10. Deep-sleep hardware state — frozen

Before entering deep sleep, firmware must:

1. stop addressable-lighting updates and put the SK data output in a benign state;
2. force PH0–PH3 OFF;
3. leave NFC SPI lines in a state that cannot backfeed the unpowered module;
4. deassert `PERIPH_EN`;
5. verify `+5V_LIGHT_SW` and `+3V3_NFC_SW` collapse;
6. configure `WLC_PRESENT` as the defined wake source;
7. enter deep sleep.

Hardware pull resistors ensure lighting, NFC, and phasers remain OFF even before firmware has configured GPIOs.

## 11. Wake / charging behavior — frozen

When wireless power appears:

1. RX1 produces `WLC_5V_RAW`.
2. U1 receives external/charging power through the isolation path.
3. `WLC_PRESENT` wakes U1 if it was asleep.
4. Hardware keeps NFC inhibited while wireless power remains present.
5. Firmware checks power/battery conditions before enabling high-current lighting.
6. Lighting may operate from BT1/U2 while charging if power/thermal tests permit; the architecture does not require the XKT receiver to directly supply the lighting rail.

## 12. Things intentionally NOT in the architecture

- GPIO expander
- TTP223 touch module
- speaker/audio
- separate addressable-lighting data buses
- dedicated MFRC522 IRQ GPIO
- dedicated MFRC522 reset GPIO
- always-powered MFRC522
- MT3608 EN-only sleep isolation
- reed-switch wake (purchased reed switches remain spare inventory unless a later approved feature specifically requires one)
- NTC monitoring (purchased NTCs remain spare inventory unless later justified)

## 13. Implementation checks that remain open but do not alter the frozen block architecture

1. Verify BT1 protection status.
2. Photograph/identify exact RX1 pads and loaded output behavior.
3. Verify U1 charging/recovery through the proposed Schottky input path.
4. Photograph/identify U2 module and set/load-test 5 V output.
5. Photograph/identify U3 header/RST behavior.
6. Verify unpowered U3 does not backfeed through SPI with the final pin assignment.
7. Confirm physical SK6812 emitter count/order.
8. Identify prewired 0805 resistor/current characteristics.
9. Calculate all gate pulls, LED current resistors, divider values, decoupling, and bulk capacitance.

Any failure here may trigger a documented engineering-change review, but none is currently a reason to redesign the architecture preemptively.

## 14. Architecture freeze summary

**Frozen topology:**

```text
                 RX1 wireless receiver
                      │
              ┌───────┴────────┐
              │                │
       Schottky -> U1 5V   WLC_PRESENT -> U1 wake
              │                └────────> NFC inhibit
             U1
     XIAO ESP32-C3
       │   │    │
       │   │    └── SPI ─────────────> U3 MFRC522 on gated 3.3 V
       │   └──── PH0–PH3 ────────────> 4x AO3400A phaser switches
       └──────── SK data -> AHCT ─────> one SK6812 serial bus
       │
       └──────── PERIPH_EN
                   ├──> battery high-side gate -> MT3608 -> +5V_LIGHT_SW
                   └──> NFC high-side gate, inhibited by WLC_PRESENT

BT1 -> U1 permanently
BT1 -> switched MT3608 lighting path
```

This is the electrical architecture to use for the remaining design steps unless explicitly revised in Git.
