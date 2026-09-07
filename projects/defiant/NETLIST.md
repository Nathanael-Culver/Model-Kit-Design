# USS Defiant — Authoritative Netlist

**Document status:** **FORMAL v1.5 — 14-pixel lighting chain incorporated / NOT YET DRAWING-APPROVED**  
**Architecture source:** `POWER-ARCHITECTURE.md` FROZEN v1.1  
**Designator source:** `DESIGNATORS.md` FROZEN v1.6  
**Pin source:** `PINOUT.md` FROZEN v1.0  
**Lighting source:** `LIGHTING-LAYOUT.md` FROZEN v1.0  
**Drawing use:** PROHIBITED until physical validation closes remaining blockers.

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

Battery-protection branch decision remains OPEN pending safe evidence.

## 3. Common ground

`GND` connects U1, RX1 negative, U2 VIN-/VOUT-, U3 GND, U4 pin 3, Q2/Q3/Q4/Q5/Q6/Q8 sources, all SK6812 grounds, divider returns, pull-down resistors, and capacitor returns.

Q9 is DNP and has no electrical connection.

## 4. Wireless-power / charging path

- RX1 = XKT-3168 receiver module.
- TX1 = XKT-412 transmitter module.
- RX1 positive output -> `WLC_5V_RAW`
- RX1 negative output -> `GND`
- D1 anode -> `WLC_5V_RAW`
- D1 cathode / marked-bar end -> `SYS_5V_IN`
- `SYS_5V_IN` -> U1 5V/VBUS external-input pad

D1 permits RX1 -> U1 current and blocks reverse feed toward RX1.

The XKT pair is treated as the selected 5 V / 2 A wireless-power hardware. Polarity/voltage/load/thermal verification remains an integrated bench acceptance item rather than a pre-design blocker.

## 5. Wireless-present detector / wake

- R1 = 130 kΩ: `WLC_5V_RAW` -> `WLC_PRESENT`
- R2 = 180 kΩ: `WLC_PRESENT` -> `GND`
- `WLC_PRESENT` -> U1 D1/GPIO3

Approved v1 wake policy:

- applying/enabling wireless charging wakes the ship;
- Wi-Fi/BLE/NFC do not wake U1 from deep sleep.

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

`PERIPH_EN` -> U1 D7/GPIO20.

## 7. U2 MT3608

Actual board pads:

- `VIN+` -> `U2_VIN_SW`
- `VIN-` -> `GND`
- `VOUT+` -> `+5V_LIGHT_SW`
- `VOUT-` -> `GND`

No external EN pad is used. Q1/Q2 provides true input disconnect. U2 is adjusted to 5.0 V before lighting connection.

## 8. +5 V lighting rail

`+5V_LIGHT_SW` feeds:

- U4 pin 5;
- LED14–LED27 VDD through the final power-distribution harness;
- R6–R9 phaser branches;
- C2 positive.

C2 target = 470 µF, >=6.3 V; 10 V preferred if size permits. Final acceptance is based on the measured 14-pixel integrated load.

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
- `SK_DIN_FIRST` -> LED14 DIN.

## 10. Frozen physical SK6812 chain

Exact stock: BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, black IP30 flexible strip.

**Physical count = 14 emitters, LED14–LED27.**

| Ref | Index | Logical zone | Physical feature | Data input |
|---|---:|---|---|---|
| LED14 | 0 | P0 | deflector top | `SK_DIN_FIRST` / W023 |
| LED15 | 1 | P0 | deflector bottom | LED14 DOUT / W054 |
| LED16 | 2 | P1 | port bussard | LED15 DOUT / W055 |
| LED17 | 3 | P3 | port chiller forward | LED16 DOUT / W056 |
| LED18 | 4 | P3 | port chiller aft | LED17 DOUT / W057 |
| LED19 | 5 | P5 | port impulse crystal A | LED18 DOUT / W058 |
| LED20 | 6 | P5 | port impulse crystal B | LED19 DOUT / W059 |
| LED21 | 7 | P7 | port impulse engine | LED20 DOUT / W060 |
| LED22 | 8 | P8 | starboard impulse engine | LED21 DOUT / W061 |
| LED23 | 9 | P6 | starboard impulse crystal B | LED22 DOUT / W062 |
| LED24 | 10 | P6 | starboard impulse crystal A | LED23 DOUT / W063 |
| LED25 | 11 | P4 | starboard chiller aft | LED24 DOUT / W064 |
| LED26 | 12 | P4 | starboard chiller forward | LED25 DOUT / W065 |
| LED27 | 13 | P2 | starboard bussard | LED26 DOUT / W066 |

LED27 DOUT -> NC unless a deliberate test point is later approved.

Every LED14–LED27:

- VDD -> `+5V_LIGHT_SW`;
- GND -> `GND`;
- retain the complete manufacturer-defined cut section and its local SMD support components.

**Data is serial/daisy-chained. Power and ground may be distributed in parallel trunks/branches and are not required to follow the data chain.**

## 11. Pulse-phaser channels

Exact LEDs: DiCUNO prewired white 0805, 2.8–3.3 V, 20 mA listed.

Use **R6–R9 = 150 Ω, >=1/8 W**.

### PH0

- `+5V_LIGHT_SW` -> R6 -> LED10 anode
- LED10 cathode -> Q3 drain
- Q3 source -> GND
- Q3 gate -> `PH0_GATE` -> U1 D2/GPIO4
- R10 = 100 kΩ gate -> GND

### PH1

- `+5V_LIGHT_SW` -> R7 -> LED11 anode
- LED11 cathode -> Q4 drain
- Q4 source -> GND
- Q4 gate -> `PH1_GATE` -> U1 D3/GPIO5
- R11 = 100 kΩ gate -> GND

### PH2

- `+5V_LIGHT_SW` -> R8 -> LED12 anode
- LED12 cathode -> Q5 drain
- Q5 source -> GND
- Q5 gate -> `PH2_GATE` -> U1 D4/GPIO6
- R12 = 100 kΩ gate -> GND

### PH3

- `+5V_LIGHT_SW` -> R9 -> LED13 anode
- LED13 cathode -> Q6 drain
- Q6 source -> GND
- Q6 gate -> `PH3_GATE` -> U1 D5/GPIO7
- R13 = 100 kΩ gate -> GND

## 12. NFC high-side gate

### Q7 AO3401A

- source -> `+3V3_ALWAYS`
- drain -> `+3V3_NFC_SW`
- gate -> `NFC_GATE`

### Q8 AO3400A

- drain -> `NFC_GATE`
- source -> GND
- gate -> `NFC_EN_GATE`

- R14 = 100 kΩ `NFC_GATE` -> `+3V3_ALWAYS`
- R15 = 10 kΩ `PERIPH_EN` -> `NFC_EN_GATE`
- R16 = 100 kΩ `NFC_EN_GATE` -> GND

Q9 is DNP. `NFC_POWER = PERIPH_EN`, including while wireless charging is active.

## 13. U3 — black XFW-ETLIVE V602

| U3 printed pin | Net | U1 endpoint/use |
|---|---|---|
| `SDA` | `NFC_CS` | U1 D6/GPIO21 |
| `SCK` | `NFC_SCK` | U1 D8/GPIO8 |
| `MOSI` | `NFC_MOSI` | U1 D10/GPIO10 |
| `MISO` | `NFC_MISO` | U1 D0/GPIO2 |
| `IRQ` | NC | no connection |
| `GND` | GND | system GND |
| `RST` | reset-bias network | R17 to switched 3.3 V unless bench test makes R17 DNP |
| `3V3` | `+3V3_NFC_SW` | Q7-switched supply |

- R17 target = 10 kΩ from RST -> `+3V3_NFC_SW`.
- R18 = 10 kΩ from `NFC_MISO`/GPIO2 -> `+3V3_ALWAYS`.

## 14. Required reset/deep-sleep states

| Net | Required state |
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

1. BT1 protection/discharge capability proof;
2. integrated XKT/D1 charging/recovery/load/thermal verification;
3. U2 load/thermal test and Q1 carrier-current test;
4. V602 reset/read-range/unpowered-SPI/backfeed test;
5. D0/D8 boot safety with V602 attached/off;
6. D9 boot safety with U4 attached/off;
7. D1/GPIO3 wireless deep-sleep wake test;
8. measured 14-pixel lighting power envelope and firmware brightness/current cap;
9. final +5V/GND pixel power-distribution geometry and wire sizes/lengths;
10. integrated charging/NFC coexistence and OTA/control testing.

## 16. Current conclusion

The physical SK6812 count and data chain are no longer open: **14 emitters, LED14–LED27, one serial data bus**. Remaining lighting work concerns physical placement, power distribution, wire sizing, and measured load—not emitter count or logical mapping.
