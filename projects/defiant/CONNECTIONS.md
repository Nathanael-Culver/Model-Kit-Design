# USS Defiant — Per-Component Pin / Connection Tables

**Document status:** **FORMAL v1.4 — 14-pixel lighting chain incorporated**  
**Sources:** `POWER-ARCHITECTURE.md`, `DESIGNATORS.md`, `NETLIST.md`, `PINOUT.md`, `WIRE-LIST.md`, `LIGHTING-LAYOUT.md`.  
**Rule:** every installed terminal resolves to a named net, `NC`, `DNP`, or a conditional branch.

## 1. U1 — Seeed Studio XIAO ESP32-C3

| U1 pin/pad | GPIO | Net/function | Wire/local | Status |
|---|---:|---|---|---|
| BAT+ | — | `BAT+` | W001 if BT1 protected; W005 if U5 fitted | conditional |
| BAT- | — | `GND` | W002 if BT1 protected; W006 if U5 fitted | conditional |
| 5V/VBUS | — | `SYS_5V_IN` | W010 | FROZEN |
| 3V3 | — | `+3V3_ALWAYS` | W050; local R14/R18 feeds | FROZEN |
| GND | — | `GND` | system ground | FROZEN |
| D0 | GPIO2 | `NFC_MISO` | W046; R18 pull-up | FROZEN |
| D1 | GPIO3 | `WLC_PRESENT` | W012 | FROZEN; normal deep-sleep wake |
| D2 | GPIO4 | `PH0_GATE` | W028 | FROZEN |
| D3 | GPIO5 | `PH1_GATE` | W029 | FROZEN |
| D4 | GPIO6 | `PH2_GATE` | W030 | FROZEN |
| D5 | GPIO7 | `PH3_GATE` | W031 | FROZEN |
| D6 | GPIO21 | `NFC_CS` | W047 | FROZEN |
| D7 | GPIO20 | `PERIPH_EN` | W018; R4/R15 local branches | FROZEN |
| D8 | GPIO8 | `NFC_SCK` | W044 | FROZEN |
| D9 | GPIO9 | `SK_DATA_RAW` | W021 | FROZEN / BOOT strap |
| D10 | GPIO10 | `NFC_MOSI` | W045 | FROZEN |
| RESET/EN | — | service only | none | NC final harness |
| BOOT switch | GPIO9 onboard | onboard | none | do not obstruct |

## 2. BT1 — 103450 LiPo

If protected:

| Lead | Net | Connection | Wire |
|---|---|---|---|
| + | `BAT+` | U1 BAT+ / Q1 branch | W001; W007 branch |
| - | `GND` | U1 BAT-/GND | W002 |

If unprotected:

| Lead | Net | Connection | Wire |
|---|---|---|---|
| + | `CELL+` | U5 B+ | W003 |
| - | `CELL-` | U5 B- | W004 |

## 3. U5 — optional 1S protection

| Terminal | Net | Connection | Wire | Status |
|---|---|---|---|---|
| B+ | `CELL+` | BT1 + | W003 | conditional |
| B- | `CELL-` | BT1 - | W004 | conditional |
| P+ | `BAT+` | U1 BAT+ / Q1 branch | W005 | conditional |
| P- | `GND` | U1 BAT-/GND | W006 | conditional |

## 4. RX1 — XKT-3168 receiver

| Terminal/lead | Net | Connection | Wire | Status |
|---|---|---|---|---|
| factory red DC output | `WLC_5V_RAW` | D1 anode and R1 divider | W008/W011 | selected positive lead; polarity check at integration |
| factory black DC output | `GND` | system GND | W009 | selected negative lead; polarity check at integration |
| receive coil pair | resonant input | integral receiver coil | integral | PHYSICALLY IDENTIFIED |

## 5. TX1 — XKT-412 transmitter

External to ship:

- `IN+` / `IN-` = transmitter supply input.
- `OUT` pair = flat spiral transmitter coil.

## 6. D1 — PMEG2010ER

| Pin | Polarity | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | cathode / marked bar | `SYS_5V_IN` | U1 5V | W010 |
| 2 | anode | `WLC_5V_RAW` | RX1 positive | W008 |

## 7. R1/R2 — WLC_PRESENT divider

| Part | Terminal | Connection |
|---|---|---|
| R1 130 kΩ | high | `WLC_5V_RAW` / W011 |
| R1 | low | `WLC_PRESENT` midpoint |
| R2 180 kΩ | high | `WLC_PRESENT`; W012 to U1 D1 |
| R2 | low | `GND` |

W013 is DNP.

## 8. Q1/Q2 — lighting high-side gate

### Q1 AO3401A

| Pin | Name | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | Gate | `LIGHT_GATE` | Q2 drain; R3 -> BAT+ | W019 if separate |
| 2 | Source | `BAT+` | battery node | W007 |
| 3 | Drain | `U2_VIN_SW` | U2 VIN+ | W014 |

### Q2 AO3400A

| Pin | Name | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | Gate | `PERIPH_EN` | U1 D7; R4 -> GND | W018 |
| 2 | Source | `GND` | system GND | W020 if separate |
| 3 | Drain | `LIGHT_GATE` | Q1 gate | W019 if separate |

R3 = 100 kΩ LIGHT_GATE -> BAT+. R4 = 100 kΩ PERIPH_EN -> GND.

## 9. U2 — MT3608 module

| Pad | Net | Connection | Wire |
|---|---|---|---|
| `VIN+` | `U2_VIN_SW` | Q1 drain | W014 |
| `VIN-` | `GND` | system GND | W015 |
| `VOUT+` | `+5V_LIGHT_SW` | 5 V distribution | W016 |
| `VOUT-` | `GND` | system GND | W017 |

No external EN is used.

## 10. U4 — SN74AHCT1G125DBVR

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | OE | `GND` | local tie | local |
| 2 | A | `SK_DATA_RAW` | U1 D9 | W021 |
| 3 | GND | `GND` | system GND/C1 low | W025 |
| 4 | Y | `SK_DATA_5V` | R5 | W022 if needed |
| 5 | VCC | `+5V_LIGHT_SW` | switched 5 V/C1 high | W024 |

C1 = 0.1 µF local VCC-GND. R5 = 330 Ω U4 Y -> LED14 DIN.

## 11. C2 — 5 V bulk capacitor

| Terminal | Net |
|---|---|
| + | `+5V_LIGHT_SW` |
| - | `GND` |

Target 470 µF, >=6.3 V; validate under integrated 14-pixel load.

## 12. Physical SK6812 emitters LED14–LED27

All fourteen are BTF-LIGHTING 5 V SK6812 RGBW Natural White cut sections. Each has:

- VDD -> `+5V_LIGHT_SW` through final power distribution;
- GND -> system GND through final power distribution;
- DIN/DOUT as below;
- complete manufacturer-defined cut section/local SMD support components retained.

| Ref | Zone/feature | DIN from | DOUT to |
|---|---|---|---|
| LED14 | P0 deflector top | R5 / W023 | LED15 / W054 |
| LED15 | P0 deflector bottom | LED14 / W054 | LED16 / W055 |
| LED16 | P1 port bussard | LED15 / W055 | LED17 / W056 |
| LED17 | P3 port chiller forward | LED16 / W056 | LED18 / W057 |
| LED18 | P3 port chiller aft | LED17 / W057 | LED19 / W058 |
| LED19 | P5 port impulse crystal A | LED18 / W058 | LED20 / W059 |
| LED20 | P5 port impulse crystal B | LED19 / W059 | LED21 / W060 |
| LED21 | P7 port impulse engine | LED20 / W060 | LED22 / W061 |
| LED22 | P8 starboard impulse engine | LED21 / W061 | LED23 / W062 |
| LED23 | P6 starboard impulse crystal B | LED22 / W062 | LED24 / W063 |
| LED24 | P6 starboard impulse crystal A | LED23 / W063 | LED25 / W064 |
| LED25 | P4 starboard chiller aft | LED24 / W064 | LED26 / W065 |
| LED26 | P4 starboard chiller forward | LED25 / W065 | LED27 / W066 |
| LED27 | P2 starboard bussard | LED26 / W066 | NC |

Power/ground may use parallel branches; only data follows this serial order.

## 13. Q3–Q6 — phaser switches

| Ref | Gate/pin1 | Source/pin2 | Drain/pin3 | Pull-down |
|---|---|---|---|---|
| Q3 | W028 `PH0_GATE` | W034 GND | W033 LED10 cathode | R10 100 kΩ |
| Q4 | W029 `PH1_GATE` | W037 GND | W036 LED11 cathode | R11 100 kΩ |
| Q5 | W030 `PH2_GATE` | W040 GND | W039 LED12 cathode | R12 100 kΩ |
| Q6 | W031 `PH3_GATE` | W043 GND | W042 LED13 cathode | R13 100 kΩ |

## 14. LED10–LED13 — phasers

| LED | Anode | Cathode | Current resistor |
|---|---|---|---|
| LED10 | R6/W032 | Q3/W033 | R6 = 150 Ω, >=1/8 W |
| LED11 | R7/W035 | Q4/W036 | R7 = 150 Ω, >=1/8 W |
| LED12 | R8/W038 | Q5/W039 | R8 = 150 Ω, >=1/8 W |
| LED13 | R9/W041 | Q6/W042 | R9 = 150 Ω, >=1/8 W |

## 15. Q7/Q8 — NFC power gate; Q9 DNP

### Q7 AO3401A

| Pin | Net | Connection | Wire |
|---:|---|---|---|
| 1 Gate | `NFC_GATE` | Q8 drain; R14 pull-up | W051 if separate |
| 2 Source | `+3V3_ALWAYS` | U1 3V3 | W050 |
| 3 Drain | `+3V3_NFC_SW` | U3 3V3 | W048 |

### Q8 AO3400A

| Pin | Net | Connection | Wire |
|---:|---|---|---|
| 1 Gate | `NFC_EN_GATE` | R15 from PERIPH_EN; R16 -> GND | local |
| 2 Source | GND | system GND | W052 if separate |
| 3 Drain | `NFC_GATE` | Q7 gate | W051 if separate |

Q9 pins 1/2/3: DNP. W013/W053: DNP.

## 16. U3 — black XFW-ETLIVE V602

| Printed pin | Net / project use | Wire |
|---|---|---|
| `SDA` | `NFC_CS` -> U1 D6/GPIO21 | W047 |
| `SCK` | `NFC_SCK` -> U1 D8/GPIO8 | W044 |
| `MOSI` | `NFC_MOSI` -> U1 D10/GPIO10 | W045 |
| `MISO` | `NFC_MISO` -> U1 D0/GPIO2 | W046 |
| `IRQ` | NC | none |
| `GND` | GND | W049 |
| `RST` | reset bias via R17 to `+3V3_NFC_SW` unless test makes R17 DNP | local |
| `3V3` | `+3V3_NFC_SW` | W048 |

R18 = 10 kΩ from `NFC_MISO`/GPIO2 to `+3V3_ALWAYS`.

## 17. Unused / superseded

- Q9: DNP.
- W013/W053: DNP / never reuse.
- U3 IRQ: NC.
- green compact RC522 and large blue RC522: spares.
- U1 external RESET/BOOT wiring: NC final harness.
- LED1–LED9: superseded placeholders.
- reed switches/NTCs: not installed.
- MT3608 EN: not MCU sleep control.

## 18. Physical verification still required

1. BT1 protection/discharge proof.
2. integrated XKT/D1 acceptance testing.
3. U3 V602 reset/backfeed/read-range/charging-coexistence behavior.
4. exact hull coordinates/orientation for LED14–LED27 and final power/ground branches.
5. one-sample phaser polarity confirmation.
6. SOT carrier pad numbering/orientation.
7. load/thermal tests for U2/Q1/D1/battery and the 14-pixel lighting load.
