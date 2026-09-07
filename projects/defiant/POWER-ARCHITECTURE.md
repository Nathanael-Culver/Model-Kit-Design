# USS Defiant — Power / Electrical Architecture

**Document status:** **FROZEN v1.1 — approved Step-9 policy decisions incorporated**  
**Drawing gate:** remains CLOSED until physical validation closes the remaining blockers.  
**Rule:** no silent architecture changes; any future revision must identify the specific problem it solves.

## 1. Frozen system concept

- `BT1` remains permanently connected to `U1` XIAO ESP32-C3.
- U1 uses deep sleep for low standby draw.
- The 5 V lighting rail is physically OFF in deep sleep.
- The MFRC522 3.3 V rail is physically OFF in deep sleep.
- **Wireless-power-present is the normal deep-sleep wake method for v1.**
- Wi-Fi, BLE, and NFC do **not** wake the ship from deep sleep; they become available after wake.
- NFC is allowed to operate while wireless charging is present. If real bench testing later proves unacceptable interference, address that demonstrated problem then.
- One SK6812 serial data bus serves all addressable lighting.
- Four pulse phasers remain four independent conventional LED channels.
- No GPIO expander, touch sensor, audio system, or additional controller is part of the architecture.

## 2. Voltage domains

| Net/domain | Source | Main consumers | Deep-sleep state |
|---|---|---|---|
| `GND` | common system reference | all electronics | connected |
| `BAT+` | BT1, ~3.0–4.2 V | U1 battery input; switched lighting-input path | present |
| `WLC_5V_RAW` | RX1 wireless receiver | U1 charging/recovery path; presence detector | present only while coupled |
| `SYS_5V_IN` | isolated `WLC_5V_RAW` | U1 external 5 V / charger input | present while charging |
| `+3V3_ALWAYS` | U1 onboard 3.3 V regulator | low-current control/sensing | present while U1 powered |
| `+5V_LIGHT_SW` | U2 MT3608 through Q1/Q2 gate | SK6812s, U4, phasers | **OFF** |
| `+3V3_NFC_SW` | Q7/Q8 switched `+3V3_ALWAYS` | U3 MFRC522 | **OFF** |

## 3. Battery/controller path

```text
BT1 LiPo
  ├──> U1 BAT input  [permanent]
  └──> Q1/Q2 high-side gate -> U2 MT3608 -> +5V_LIGHT_SW
```

Battery protection remains mandatory. If BT1 is protected, U5 is DNP. If BT1 is an unprotected bare cell, U5 must be fitted before final assembly.

## 4. Wireless charging / recovery / wake

```text
TX1 XKT-412 ))) RX1
                 │
                 └── WLC_5V_RAW
                       ├──> D1 Schottky -> SYS_5V_IN -> U1 5V/charger input
                       └──> R1/R2 divider -> WLC_PRESENT -> U1 D1/GPIO3
```

Frozen behavior:

1. wireless power is not the lighting supply;
2. lighting remains BT1 -> Q1/Q2 -> U2 -> `+5V_LIGHT_SW`;
3. wireless power feeds U1 charging/recovery through D1;
4. `WLC_PRESENT` never connects raw 5 V directly to a GPIO;
5. `WLC_PRESENT` on D1/GPIO3 is the **only normal deep-sleep wake source in v1**;
6. applying/enabling the wireless charging field is the normal way to wake a sleeping sealed ship;
7. after wake, Wi-Fi/BLE/NFC controls may be used normally;
8. RX1 output capability remains subject to bench measurement.

## 5. Lighting power gate

```text
BAT+ -> Q1 AO3401A P-MOS -> U2 MT3608 -> +5V_LIGHT_SW
              ^
              |
          Q2 AO3400A
              ^
              |
          PERIPH_EN
```

- Q1 physically disconnects U2 from BAT+.
- Q2 pulls Q1 gate low when `PERIPH_EN` is HIGH.
- R3 pulls Q1 gate to BAT+ for hardware-default OFF.
- R4 pulls `PERIPH_EN` LOW for hardware-default OFF.
- MT3608 EN is not relied upon for sleep isolation.

## 6. Addressable lighting

```text
U1 SK_DATA_RAW -> U4 SN74AHCT1G125 -> R5 -> one SK6812 serial chain
```

- one addressable data line only;
- one U4 level-shifter;
- U4 powered from `+5V_LIGHT_SW`;
- C1 local bypass at U4;
- R5 330 Ω formal starting value;
- P0–P8 are logical zones, not physical LED counts.

## 7. Pulse phasers

Each channel:

```text
+5V_LIGHT_SW -> R6/R7/R8/R9 as required -> LED -> Q3/Q4/Q5/Q6 -> GND
```

Each gate has a hardware pull-down. R6–R9 remain unresolved until the exact prewired LED configuration is measured.

## 8. NFC architecture

U3 uses SPI:

- `NFC_SCK`
- `NFC_MOSI`
- `NFC_MISO`
- `NFC_CS`

No MCU IRQ or reset GPIO is allocated.

### NFC supply gate

```text
+3V3_ALWAYS -> Q7 AO3401A -> +3V3_NFC_SW -> U3
                    ^
                    |
                Q8 AO3400A
                    ^
                    |
              PERIPH_EN via R15
```

- R14 makes Q7 default OFF.
- R16 makes Q8 default OFF.
- `PERIPH_EN` enables the NFC rail through R15/Q8.
- **Q9 is DNP.** `WLC_PRESENT` does not inhibit NFC power.
- NFC may operate while wireless charging is present.

If bench testing later proves wireless-power/NFC interference, document the measured failure before adding mitigation.

## 9. GPIO budget

| Function | Count |
|---|---:|
| one SK6812 data bus | 1 |
| four phasers | 4 |
| MFRC522 SPI | 4 |
| `WLC_PRESENT` wake | 1 |
| `PERIPH_EN` | 1 |
| **Total** | **11 / 11** |

Q9 removal does not change the GPIO budget because it never consumed an MCU GPIO.

## 10. Deep-sleep behavior

Before sleep firmware must:

1. turn off logical lighting and phasers;
2. place SK data in a benign LOW state;
3. place SPI outputs in a state that does not back-power U3;
4. deassert `PERIPH_EN`;
5. verify `+5V_LIGHT_SW` and `+3V3_NFC_SW` collapse;
6. configure `WLC_PRESENT` on D1/GPIO3 as the wake source;
7. enter deep sleep.

While asleep, Wi-Fi/BLE/NFC are unavailable. The user wakes the model by applying wireless charging power.

## 11. Wake / charging behavior

When wireless power appears:

1. RX1 produces `WLC_5V_RAW`;
2. U1 receives charging/recovery power through D1;
3. `WLC_PRESENT` wakes U1;
4. firmware enters a safe boot/recovery state;
5. after supply checks, `PERIPH_EN` may enable lighting and NFC;
6. NFC is allowed while charging;
7. firmware must avoid blindly enabling maximum lighting load during recovery/low-battery conditions.

## 12. Intentionally excluded

- GPIO expander
- TTP223 touch module
- speaker/audio
- second SK6812 data bus
- dedicated MFRC522 IRQ GPIO
- dedicated MFRC522 reset GPIO
- always-powered MFRC522
- Q9 charging/NFC inhibit
- MT3608 EN-only sleep isolation
- reed-switch wake
- NTC monitoring
- Wi-Fi/BLE/NFC deep-sleep wake in v1

## 13. Remaining physical checks

1. BT1 protection/discharge capability.
2. RX1 polarity, unloaded/loaded voltage/current/temperature.
3. D1 charge/recovery/reverse-current behavior.
4. U2 5 V load/thermal capability and Q1 carrier current capability.
5. exact U3 header/reset/unpowered-I/O behavior.
6. phaser LED current-limit determination.
7. physical SK6812 count/order/decoupling/load.
8. repeated boot/reset/deep-sleep -> wireless-wake cycles.
9. final distribution-board/harness implementation.
10. Wi-Fi/BLE/NFC/OTA integrated tests before sealing.

## 14. Frozen topology summary

```text
RX1 -> D1 -> U1 5V/charger
  └----> R1/R2 -> WLC_PRESENT -> U1 wake

BT1 -> U1 permanently
BT1 -> Q1/Q2 -> U2 -> +5V_LIGHT_SW

U1 SK data -> U4 -> one SK6812 chain
U1 PH0..PH3 -> Q3..Q6 -> four phasers
U1 PERIPH_EN -> Q2 lighting gate
                └-> R15/Q8 -> Q7 -> +3V3_NFC_SW -> U3

Q9 = DNP
```

This v1.1 architecture incorporates the user's explicit approval to allow NFC while charging and to use wireless charging presence as the normal deep-sleep wake method.