# USS Defiant — Power / Electrical Architecture

**Document status:** **FROZEN v1.2 — 14-pixel lighting and current-limit decisions incorporated**  
**Drawing gate:** remains CLOSED until physical validation closes remaining blockers.  
**Rule:** no silent architecture changes; any future revision must identify the specific problem it solves.

## 1. Frozen system concept

- `BT1` remains permanently connected to `U1` XIAO ESP32-C3.
- U1 uses deep sleep for low standby draw.
- The 5 V lighting rail is physically OFF in deep sleep.
- The NFC 3.3 V rail is physically OFF in deep sleep.
- Wireless-power-present is the normal deep-sleep wake method for v1.
- Wi-Fi, BLE, and NFC do not wake the ship from deep sleep; they become available after wake.
- NFC is allowed to operate while wireless charging is present.
- One SK6812 serial data bus serves **14 physical RGBW pixels** mapped to 9 logical zones.
- Four pulse phasers remain four independent conventional white LED channels.
- No GPIO expander, touch sensor, audio system, or additional controller is part of the architecture.

## 2. Voltage domains

| Net/domain | Source | Main consumers | Deep-sleep state |
|---|---|---|---|
| `GND` | common system reference | all electronics | connected |
| `BAT+` | BT1, ~3.0–4.2 V | U1 battery input; switched lighting-input path | present |
| `WLC_5V_RAW` | RX1 XKT-3168 receiver | U1 charging/recovery path; presence detector | present only while coupled |
| `SYS_5V_IN` | isolated `WLC_5V_RAW` | U1 external 5 V / charger input | present while charging |
| `+3V3_ALWAYS` | U1 onboard 3.3 V regulator | low-current control/sensing | present while U1 powered |
| `+5V_LIGHT_SW` | U2 MT3608 through Q1/Q2 gate | LED14–LED27, U4, LED10–LED13 | **OFF** |
| `+3V3_NFC_SW` | Q7/Q8 switched `+3V3_ALWAYS` | U3 V602 | **OFF** |

## 3. Battery/controller path

```text
BT1 LiPo
  ├──> U1 BAT input  [permanent]
  └──> Q1/Q2 high-side gate -> U2 MT3608 -> +5V_LIGHT_SW
```

Battery protection remains mandatory. If BT1 is protected, U5 is DNP. If BT1 is an unprotected bare cell, U5 must be fitted before final assembly.

## 4. Wireless charging / recovery / wake

```text
TX1 XKT-412 ))) RX1 XKT-3168
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
5. `WLC_PRESENT` on D1/GPIO3 is the only normal deep-sleep wake source in v1;
6. applying/enabling the wireless charging field is the normal way to wake a sleeping sealed ship;
7. after wake, Wi-Fi/BLE/NFC controls may be used normally;
8. the selected XKT pair's final polarity/load/thermal behavior is verified during integrated bench acceptance rather than blocking further design.

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
U1 SK_DATA_RAW -> U4 SN74AHCT1G125 -> R5 -> LED14 -> ... -> LED27
```

- one addressable data line only;
- one U4 level shifter;
- U4 powered from `+5V_LIGHT_SW`;
- C1 = 0.1 µF local bypass at U4;
- R5 = 330 Ω data-series resistor;
- **14 physical SK6812 RGBW pixels, LED14–LED27**;
- **9 logical zones P0–P8**;
- physical count, zone membership, and data order are frozen in `LIGHTING-LAYOUT.md`;
- data is daisy-chained, while +5 V/GND use separate front/port/starboard distribution branches defined in `POWER-DISTRIBUTION.md`.

## 7. Pulse phasers

Each channel:

```text
+5V_LIGHT_SW -> 150 Ω -> LED -> AO3400A -> GND
```

- LED10–LED13 are DiCUNO prewired white 0805 emitters.
- R6 = R7 = R8 = R9 = **150 Ω, >=1/8 W**.
- Q3–Q6 independently switch PH0–PH3.
- each gate has a 100 kΩ hardware pull-down.

## 8. NFC architecture

U3 is the black XFW-ETLIVE V602 compact RC522-class reader and uses SPI:

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
- Q9 is DNP.
- NFC may operate while wireless charging is present.

## 9. GPIO budget

| Function | Count |
|---|---:|
| one SK6812 data bus | 1 |
| four phasers | 4 |
| V602 SPI | 4 |
| `WLC_PRESENT` wake | 1 |
| `PERIPH_EN` | 1 |
| **Total** | **11 / 11** |

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

## 11. Physical power-distribution architecture

The final harness uses a central power/control island and separate lighting power branches:

```text
                    +5V_LIGHT_SW
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      front branch    port branch   starboard branch
      LED14–15        LED16–21       LED22–27
```

U4/C2/phaser resistors are local to the central island. Ground follows the same functional branch pattern. See `POWER-DISTRIBUTION.md`.

## 12. Intentionally excluded

- GPIO expander
- TTP223 touch module
- speaker/audio
- second SK6812 data bus
- dedicated NFC IRQ GPIO
- dedicated NFC reset GPIO
- always-powered NFC reader
- Q9 charging/NFC inhibit
- MT3608 EN-only sleep isolation
- reed-switch wake
- NTC monitoring
- Wi-Fi/BLE/NFC deep-sleep wake in v1

## 13. Remaining physical checks

1. BT1 protection/discharge capability.
2. integrated XKT/D1 charge/recovery/load/thermal behavior.
3. U2 5 V load/thermal capability and Q1 carrier current capability.
4. U3 reset/unpowered-I/O/read-range behavior.
5. repeated boot/reset/deep-sleep -> wireless-wake cycles.
6. final 14-pixel current draw and firmware current/brightness cap.
7. exact component coordinates, wire lengths and W067+ power-branch implementation.
8. carrier pad orientation.
9. Wi-Fi/BLE/NFC/OTA integrated tests before sealing.

## 14. Frozen topology summary

```text
RX1 -> D1 -> U1 5V/charger
  └----> R1/R2 -> WLC_PRESENT -> U1 wake

BT1 -> U1 permanently
BT1 -> Q1/Q2 -> U2 -> +5V_LIGHT_SW

U1 SK data -> U4 -> LED14 ... LED27
U1 PH0..PH3 -> Q3..Q6 -> four phasers
U1 PERIPH_EN -> Q2 lighting gate
                └-> R15/Q8 -> Q7 -> +3V3_NFC_SW -> U3

Q9 = DNP
```

This v1.2 architecture incorporates the frozen 14-pixel lighting plan, final phaser current-limit values, the selected V602 reader, and the central/branched physical power-distribution strategy.
