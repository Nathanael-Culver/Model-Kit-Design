# USS Defiant — Authoritative Netlist

**Document status:** **FORMAL v1.2 — approved Step-9 policy decisions incorporated / NOT YET DRAWING-APPROVED**  
**Architecture source:** `POWER-ARCHITECTURE.md` FROZEN v1.1  
**Designator source:** `DESIGNATORS.md` FROZEN v1.2  
**Pin source:** `PINOUT.md` FROZEN v1.0  
**Drawing use:** PROHIBITED until physical validation closes the remaining blockers.

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

No spare exposed GPIO remains.

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

## 3. Common ground

`GND` connects U1, RX1 negative, U2 IN-/OUT-, U3 GND, U4 pin 3, Q2/Q3/Q4/Q5/Q6/Q8 sources, all SK6812 grounds, sensing-divider return, pull-down resistors, and capacitor returns.

Q9 is DNP and has no electrical connection.

## 4. Wireless-power / charging path

- RX1 positive -> `WLC_5V_RAW`
- RX1 negative -> `GND`
- D1 anode -> `WLC_5V_RAW`
- D1 cathode / marked-bar end -> `SYS_5V_IN`
- `SYS_5V_IN` -> U1 5 V external-input pin/pad

D1 permits RX1 -> U1 current and blocks reverse feed toward RX1.

## 5. Wireless-present detector / wake

- R1 = 130 kΩ: `WLC_5V_RAW` -> `WLC_PRESENT`
- R2 = 180 kΩ: `WLC_PRESENT` -> `GND`
- `WLC_PRESENT` -> **U1 D1 / GPIO3 only**

`WLC_PRESENT` no longer branches to Q9 because Q9 is DNP.

Approved v1 wake policy:

- `WLC_PRESENT` is the normal deep-sleep wake source;
- applying/enabling wireless charging wakes the ship;
- Wi-Fi/BLE/NFC do not wake U1 from deep sleep.

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

- `PERIPH_EN` -> U1 D7/GPIO20

LOW/floating = lighting off; HIGH = lighting input enabled.

## 7. U2 MT3608

- IN+ -> `U2_VIN_SW`
- IN- -> `GND`
- OUT+ -> `+5V_LIGHT_SW`
- OUT- -> `GND`

Adjust/load-test to 5.0 V before LEDs are connected. MT3608 EN is not the sleep-isolation mechanism.

## 8. +5 V lighting rail

`+5V_LIGHT_SW` feeds:

- U4 pin 5
- all physical SK6812 VDD pins
- LED10–LED13 current-limit branches
- C2 positive

C2 target = 470 µF, >=6.3 V; 10 V preferred if size permits.

## 9. U4 SN74AHCT1G125

| U4 pin | Connection |
|---:|---|
| 1 OE | `GND` |
| 2 A | `SK_DATA_RAW` = U1 D9/GPIO9 |
| 3 GND | `GND` |
| 4 Y | `SK_DATA_5V` |
| 5 VCC | `+5V_LIGHT_SW` |

- C1 = 0.1 µF ceramic between VCC and GND, local to U4.
- R5 = 330 Ω from `SK_DATA_5V` to `SK_DIN_FIRST`.

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

Physical emitter count/order remains OPEN. P0–P8 are firmware logical zones.

## 11. Pulse-phaser channels

### PH0

- `+5V_LIGHT_SW` -> R6 -> LED10 anode
- LED10 cathode -> Q3 drain
- Q3 source -> `GND`
- Q3 gate -> `PH0_GATE` -> U1 D2/GPIO4
- R10 = 100 kΩ `PH0_GATE` -> `GND`

### PH1

- `+5V_LIGHT_SW` -> R7 -> LED11 anode
- LED11 cathode -> Q4 drain
- Q4 source -> `GND`
- Q4 gate -> `PH1_GATE` -> U1 D3/GPIO5
- R11 = 100 kΩ `PH1_GATE` -> `GND`

### PH2

- `+5V_LIGHT_SW` -> R8 -> LED12 anode
- LED12 cathode -> Q5 drain
- Q5 source -> `GND`
- Q5 gate -> `PH2_GATE` -> U1 D4/GPIO6
- R12 = 100 kΩ `PH2_GATE` -> `GND`

### PH3

- `+5V_LIGHT_SW` -> R9 -> LED13 anode
- LED13 cathode -> Q6 drain
- Q6 source -> `GND`
- Q6 gate -> `PH3_GATE` -> U1 D5/GPIO7
- R13 = 100 kΩ `PH3_GATE` -> `GND`

R6–R9 remain TBD or DNP pending actual LED verification.

## 12. NFC high-side gate

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

### Q9

- **DNP**
- no gate connection to `WLC_PRESENT`
- no drain connection to `NFC_EN_GATE`
- no source connection to `GND`

Hardware truth condition is now simply:

`NFC_POWER = PERIPH_EN`

This explicitly allows NFC to operate while wireless charging is present.

## 13. U3 MFRC522

| U3 function | Net | U1 endpoint |
|---|---|---|
| VCC / 3.3 V | `+3V3_NFC_SW` | switched supply |
| GND | `GND` | GND |
| SCK | `NFC_SCK` | D8 / GPIO8 |
| MOSI | `NFC_MOSI` | D10 / GPIO10 |
| MISO | `NFC_MISO` | D0 / GPIO2 |
| SDA/SS/CS | `NFC_CS` | D6 / GPIO21 |
| IRQ | NC | none |
| RST/NRSTPD | reset-bias network | none |

### R17

- target 10 kΩ from U3 RST/NRSTPD -> `+3V3_NFC_SW`
- may become DNP if the exact breakout already provides appropriate bias/reset behavior

### R18

- 10 kΩ from `NFC_MISO` / U1 D0/GPIO2 -> `+3V3_ALWAYS`

Firmware must explicitly configure SPI pins GPIO8/GPIO10/GPIO2/GPIO21.

## 14. Required reset/deep-sleep states

| Net | Required hardware state |
|---|---|
| `PERIPH_EN` | LOW via R4 |
| `LIGHT_GATE` | HIGH to BAT+ via R3 -> Q1 OFF |
| PH0–PH3 gates | LOW via R10–R13 |
| `NFC_GATE` | HIGH via R14 -> Q7 OFF |
| `NFC_EN_GATE` | LOW via R16 |
| `WLC_PRESENT` | LOW via R2 when RX1 absent |
| `NFC_MISO` / D0 | HIGH-biased via R18 when U3 not driving |
| `+5V_LIGHT_SW` | OFF |
| `+3V3_NFC_SW` | OFF |

## 15. Remaining blockers before drawing approval

1. D0/GPIO2 boot and U3 unpowered-I/O test;
2. D8/GPIO8 boot test with U3 attached/off;
3. D9/GPIO9 boot test with U4 attached/off;
4. D1/GPIO3 wireless deep-sleep wake test;
5. RX1 pad identity/loaded voltage/current;
6. U2 load/thermal test and Q1 carrier-current test;
7. U3 header/reset behavior;
8. BT1 protection/discharge capability;
9. phaser LED current/resistor determination;
10. physical SK6812 count/order/decoupling/load;
11. integrated backfeed/default-off/charging/NFC coexistence validation.

## 16. Current conclusion

The approved Q9 removal and charging-field wake policy are now incorporated. The electrical topology remains coherent and the GPIO map is unchanged.