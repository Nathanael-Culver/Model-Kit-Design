# USS Defiant — Authoritative Netlist

**Document status:** **FORMAL v1.1 — GPIO ASSIGNMENT COMPLETE / NOT YET DRAWING-APPROVED**  
**Architecture source:** `POWER-ARCHITECTURE.md` FROZEN v1.0  
**Designator source:** `DESIGNATORS.md` FROZEN v1.1  
**Pin source:** `PINOUT.md` FROZEN v1.0  
**Drawing use:** PROHIBITED until physical module verification and validation close the remaining blockers.

## 1. U1 XIAO ESP32-C3 — frozen signal assignment

| XIAO pin | GPIO | Net | Direction |
|---|---:|---|---|
| D0 | GPIO2 | `NFC_MISO` | input |
| D1 | GPIO3 | `WLC_PRESENT` | input / deep-sleep wake |
| D2 | GPIO4 | `PH0_GATE` | output |
| D3 | GPIO5 | `PH1_GATE` | output |
| D4 | GPIO6 | `PH2_GATE` | output |
| D5 | GPIO7 | `PH3_GATE` | output |
| D6 | GPIO21 | `NFC_CS` | output |
| D7 | GPIO20 | `PERIPH_EN` | output |
| D8 | GPIO8 | `NFC_SCK` | output |
| D9 | GPIO9 | `SK_DATA_RAW` | output |
| D10 | GPIO10 | `NFC_MOSI` | output |

No additional U1 GPIO is available. Any added GPIO function requires an approved architecture change.

## 2. Battery / protection branch

If BT1 has integral protection, U5 is DNP:

- BT1 positive -> `BAT+`
- BT1 negative -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

If BT1 is unprotected, U5 must be fitted:

- BT1 positive -> `CELL+` -> U5 B+
- BT1 negative -> `CELL-` -> U5 B-
- U5 P+ -> `BAT+`
- U5 P- -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

## 3. Common ground — `GND`

Connects U1, RX1 negative, U2 IN-/OUT-, U3 GND, U4 pin 3, Q2/Q3/Q4/Q5/Q6/Q8/Q9 sources, all SK6812 grounds, sensing-divider return, pull-down resistors, and capacitor returns.

## 4. Wireless-power / charging path

- RX1 positive -> `WLC_5V_RAW`
- RX1 negative -> `GND`
- D1 PMEG2010ER anode -> `WLC_5V_RAW`
- D1 cathode / marked-bar end -> `SYS_5V_IN`
- `SYS_5V_IN` -> U1 5 V external-input pin/pad

D1 permits RX1 -> U1 current and blocks reverse feed toward RX1.

## 5. Wireless-present detector / wake

- R1 = 130 kΩ: `WLC_5V_RAW` -> `WLC_PRESENT`
- R2 = 180 kΩ: `WLC_PRESENT` -> `GND`
- `WLC_PRESENT` -> **U1 D1 / GPIO3**
- `WLC_PRESENT` -> Q9 gate

Nominal 5.0 V receiver output produces about 2.90 V at `WLC_PRESENT`. Actual RX1 voltage must be measured before final approval.

## 6. Lighting input power gate

### Q1 AO3401A

- source -> `BAT+`
- drain -> `U2_VIN_SW`
- gate -> `LIGHT_GATE`

### R3

- 100 kΩ: `LIGHT_GATE` -> `BAT+`

### Q2 AO3400A

- drain -> `LIGHT_GATE`
- source -> `GND`
- gate -> `PERIPH_EN`

### R4

- 100 kΩ: `PERIPH_EN` -> `GND`

### U1 endpoint

- `PERIPH_EN` -> **U1 D7 / GPIO20**

`PERIPH_EN` floating/LOW = lighting gate OFF. HIGH = Q1 enables U2 input.

## 7. U2 MT3608

- IN+ -> `U2_VIN_SW`
- IN- -> `GND`
- OUT+ -> `+5V_LIGHT_SW`
- OUT- -> `GND`

Adjust/load-test U2 to 5.0 V before LEDs are connected. MT3608 EN is not the primary sleep-isolation mechanism.

## 8. +5 V lighting rail

`+5V_LIGHT_SW` feeds:

- U4 pin 5
- all physical SK6812 VDD pins
- LED10–LED13 current-limit branches
- C2 positive

C2 target = 470 µF, >=6.3 V; 10 V preferred if size permits.

## 9. U4 SN74AHCT1G125 SK6812 level shifter

| U4 pin | Connection |
|---:|---|
| 1 OE | `GND` |
| 2 A | `SK_DATA_RAW` = U1 D9/GPIO9 |
| 3 GND | `GND` |
| 4 Y | `SK_DATA_5V` |
| 5 VCC | `+5V_LIGHT_SW` |

- C1 = 0.1 µF ceramic between U4 VCC and GND, physically local to U4.
- R5 = 330 Ω from `SK_DATA_5V` to `SK_DIN_FIRST`.

`SK_DATA_RAW` is deliberately assigned to D9/GPIO9 because U4 presents the least intrusive available load to the critical BOOT strap. There is no external pull-down on this net.

## 10. Physical SK6812 chain

One serial chain only:

```text
SK_DIN_FIRST -> LED14 DIN
LED14 DOUT -> LED15 DIN
LED15 DOUT -> LED16 DIN
... -> final physical SK6812
```

Every physical SK6812:

- VDD -> `+5V_LIGHT_SW`
- GND -> `GND`

Physical emitter count/order remains OPEN; logical zones P0–P8 are mapped in firmware and are not physical component counts.

## 11. Pulse-phaser channels

### PH0 / LED10 / Q3

- `+5V_LIGHT_SW` -> R6 -> LED10 anode
- LED10 cathode -> Q3 drain
- Q3 source -> `GND`
- Q3 gate / `PH0_GATE` -> **U1 D2/GPIO4**
- R10 = 100 kΩ from `PH0_GATE` -> `GND`

### PH1 / LED11 / Q4

- `+5V_LIGHT_SW` -> R7 -> LED11 anode
- LED11 cathode -> Q4 drain
- Q4 source -> `GND`
- Q4 gate / `PH1_GATE` -> **U1 D3/GPIO5**
- R11 = 100 kΩ from `PH1_GATE` -> `GND`

### PH2 / LED12 / Q5

- `+5V_LIGHT_SW` -> R8 -> LED12 anode
- LED12 cathode -> Q5 drain
- Q5 source -> `GND`
- Q5 gate / `PH2_GATE` -> **U1 D4/GPIO6**
- R12 = 100 kΩ from `PH2_GATE` -> `GND`

### PH3 / LED13 / Q6

- `+5V_LIGHT_SW` -> R9 -> LED13 anode
- LED13 cathode -> Q6 drain
- Q6 source -> `GND`
- Q6 gate / `PH3_GATE` -> **U1 D5/GPIO7**
- R13 = 100 kΩ from `PH3_GATE` -> `GND`

R6–R9 remain TBD or DNP pending verification of the actual prewired LEDs.

## 12. NFC high-side gate and wireless inhibit

### Q7 AO3401A

- source -> `+3V3_ALWAYS`
- drain -> `+3V3_NFC_SW`
- gate -> `NFC_GATE`

### R14

- 100 kΩ: `NFC_GATE` -> `+3V3_ALWAYS`

### Q8 AO3400A

- drain -> `NFC_GATE`
- source -> `GND`
- gate -> `NFC_EN_GATE`

### R15 / R16

- R15 = 10 kΩ: `PERIPH_EN` -> `NFC_EN_GATE`
- R16 = 100 kΩ: `NFC_EN_GATE` -> `GND`

### Q9 AO3400A

- drain -> `NFC_EN_GATE`
- source -> `GND`
- gate -> `WLC_PRESENT`

Hardware truth condition:

`NFC_POWER = PERIPH_EN AND NOT WLC_PRESENT`

## 13. U3 MFRC522

Functional net-to-U1 mapping:

| U3 function | Net | U1 endpoint |
|---|---|---|
| VCC / 3.3 V | `+3V3_NFC_SW` | switched supply |
| GND | `GND` | GND |
| SCK | `NFC_SCK` | **D8 / GPIO8** |
| MOSI | `NFC_MOSI` | **D10 / GPIO10** |
| MISO | `NFC_MISO` | **D0 / GPIO2** |
| SDA/SS/CS | `NFC_CS` | **D6 / GPIO21** |
| IRQ | NC | none |
| RST/NRSTPD | reset-bias network | none |

### R17 — reset bias

- target 10 kΩ from U3 RST/NRSTPD -> `+3V3_NFC_SW`
- may become DNP if exact breakout already provides a suitable onboard pull-up/reset behavior

### R18 — GPIO2 boot pull-up

- R18 = **10 kΩ** from `NFC_MISO` / U1 D0/GPIO2 -> `+3V3_ALWAYS`

R18 preserves the recommended HIGH bias on GPIO2 while U3 is unpowered. Bench boot testing with the exact breakout remains mandatory.

Firmware must explicitly configure MFRC522 SPI as:

- SCK GPIO8
- MOSI GPIO10
- MISO GPIO2
- CS GPIO21

Do not assume the board's default SPI pin macros.

## 14. Required hardware reset/deep-sleep states

| Net | Required hardware state |
|---|---|
| `PERIPH_EN` | LOW via R4 |
| `LIGHT_GATE` | HIGH to BAT+ via R3 -> Q1 OFF |
| `PH0_GATE` | LOW via R10 |
| `PH1_GATE` | LOW via R11 |
| `PH2_GATE` | LOW via R12 |
| `PH3_GATE` | LOW via R13 |
| `NFC_GATE` | HIGH to +3V3_ALWAYS via R14 -> Q7 OFF |
| `NFC_EN_GATE` | LOW via R16 |
| `WLC_PRESENT` | LOW via R2 when receiver absent |
| `NFC_MISO` / D0 | HIGH-biased via R18 when U3 not driving |
| `+5V_LIGHT_SW` | OFF |
| `+3V3_NFC_SW` | OFF |

## 15. Remaining blockers before drawing approval

1. physical boot test of D0/GPIO2 with U3 connected/unpowered;
2. physical boot test of D8/GPIO8 with U3 connected/unpowered;
3. physical boot test of D9/GPIO9 with U4 connected/unpowered;
4. WLC_PRESENT deep-sleep wake test on D1/GPIO3;
5. exact RX1 pad identity/loaded voltage;
6. exact U2 module verification/load test;
7. exact U3 header/reset behavior;
8. BT1 protection status;
9. prewired phaser LED current/resistor determination;
10. physical SK6812 emitter count/order;
11. integrated backfeed/default-off validation.

## 16. Step-6 conclusion

The netlist now contains a complete one-to-one XIAO GPIO mapping. No duplicate GPIO exists and no additional GPIO is available. The remaining work is physical verification, wire identification, connection tables, and validation—not additional pin allocation.
