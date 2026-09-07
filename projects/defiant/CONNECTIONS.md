# USS Defiant — Per-Component Pin / Connection Tables

**Document status:** **FORMAL v1.3 — black V602 U3 selection incorporated**  
**Sources:** `POWER-ARCHITECTURE.md`, `DESIGNATORS.md`, `NETLIST.md`, `PINOUT.md`, `WIRE-LIST.md`.  
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
| D7 | GPIO20 | `PERIPH_EN` | W018; R4 pull-down; R15 branch to NFC gate | FROZEN |
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

Current photograph is consistent with an end-mounted protection board but does not prove protection function; branch remains conditional.

## 3. U5 — optional 1S protection

| Terminal | Net | Connection | Wire | Status |
|---|---|---|---|---|
| B+ | `CELL+` | BT1 + | W003 | conditional |
| B- | `CELL-` | BT1 - | W004 | conditional |
| P+ | `BAT+` | U1 BAT+ / Q1 branch | W005 | conditional |
| P- | `GND` | U1 BAT-/GND | W006 | conditional |

## 4. RX1 — XKT receiver

| Functional terminal | Net | Connection | Wire | Status |
|---|---|---|---|---|
| positive DC output | `WLC_5V_RAW` | D1 anode and R1 divider | W008/W011 | physical pad OPEN |
| negative DC output | `GND` | system GND | W009 | physical pad OPEN |
| coil A/B | receiver coil | integral | integral | verify physical module |

## 5. TX1 — XKT-412 transmitter

External to ship. Verify exact DC input polarity/rating and coil terminals on physical module.

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

W013 is DNP; no Q9 branch exists.

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

## 9. U2 — photographed MT3608 module

| Physical pad label | Net | Connection | Wire | Status |
|---|---|---|---|---|
| `VIN+` | `U2_VIN_SW` | Q1 drain | W014 | VERIFIED label |
| `VIN-` | `GND` | system GND | W015 | VERIFIED label |
| `VOUT+` | `+5V_LIGHT_SW` | 5 V distribution | W016 | VERIFIED label |
| `VOUT-` | `GND` | system GND | W017 | VERIFIED label |

No separate external EN pad is visible. Do not modify the bare IC for normal assembly.

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

Target 470 µF, >=6.3 V; revalidate after physical LED load is known.

## 12. Physical SK6812 emitters LED14+

Exact stock is BTF-LIGHTING 5 V SK6812 RGBW Natural White, 144 LED/m, black IP30 strip.

LED14:

| Pad | Net | Connection |
|---|---|---|
| VDD | `+5V_LIGHT_SW` | W026 distribution entry |
| GND | `GND` | W027 distribution entry |
| DIN | `SK_DIN_FIRST` | W023 from R5 |
| DOUT | next serial data net | LED15 DIN if present |

For every cut section, retain the complete manufacturer-defined pixel segment and its local SMD support components.

## 13. Q3–Q6 — phaser switches

| Ref | Gate/pin1 | Source/pin2 | Drain/pin3 | Pull-down |
|---|---|---|---|---|
| Q3 | W028 `PH0_GATE` | W034 GND | W033 LED10 cathode | R10 100 kΩ |
| Q4 | W029 `PH1_GATE` | W037 GND | W036 LED11 cathode | R11 100 kΩ |
| Q5 | W030 `PH2_GATE` | W040 GND | W039 LED12 cathode | R12 100 kΩ |
| Q6 | W031 `PH3_GATE` | W043 GND | W042 LED13 cathode | R13 100 kΩ |

## 14. LED10–LED13 — DiCUNO white 0805 phasers

Exact listed LED parameters: white, 2.8–3.3 V, 20 mA, 240–280 mcd, 120°, prewired 6.3 in leads.

| LED | Anode | Cathode | Current resistor |
|---|---|---|---|
| LED10 | R6/W032 | Q3/W033 | **R6 = 150 Ω, >=1/8 W** |
| LED11 | R7/W035 | Q4/W036 | **R7 = 150 Ω, >=1/8 W** |
| LED12 | R8/W038 | Q5/W039 | **R8 = 150 Ω, >=1/8 W** |
| LED13 | R9/W041 | Q6/W042 | **R9 = 150 Ω, >=1/8 W** |

At 5.0 V, 150 Ω produces approximately 11.3–14.7 mA across the listed Vf range. Verify one physical LED's polarity before duplicating all channels; do not infer polarity solely from wire color.

## 15. Q7/Q8 — NFC power gate; Q9 DNP

### Q7 AO3401A

| Pin | Name | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | Gate | `NFC_GATE` | Q8 drain; R14 pull-up | W051 if separate |
| 2 | Source | `+3V3_ALWAYS` | U1 3V3 | W050 |
| 3 | Drain | `+3V3_NFC_SW` | U3 3V3 | W048 |

### Q8 AO3400A

| Pin | Name | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | Gate | `NFC_EN_GATE` | R15 from PERIPH_EN; R16 -> GND | local |
| 2 | Source | `GND` | system GND | W052 if separate |
| 3 | Drain | `NFC_GATE` | Q7 gate | W051 if separate |

R14 = 100 kΩ NFC_GATE -> +3V3_ALWAYS. R15 = 10 kΩ PERIPH_EN -> NFC_EN_GATE. R16 = 100 kΩ NFC_EN_GATE -> GND.

Q9 pins 1/2/3: DNP / no connection. W013 and W053: DNP.

## 16. U3 — black XFW-ETLIVE V602

**This is the selected/frozen Defiant NFC reader.**

Photographed header order, top-to-bottom as printed:

| Printed pin | Net / project use | Wire | Status |
|---|---|---|---|
| `SDA` | `NFC_CS` -> U1 D6/GPIO21 | W047 | FROZEN |
| `SCK` | `NFC_SCK` -> U1 D8/GPIO8 | W044 | FROZEN |
| `MOSI` | `NFC_MOSI` -> U1 D10/GPIO10 | W045 | FROZEN |
| `MISO` | `NFC_MISO` -> U1 D0/GPIO2 | W046 | FROZEN |
| `IRQ` | NC | none | NC |
| `GND` | `GND` | W049 | FROZEN |
| `RST` | reset bias via R17 to `+3V3_NFC_SW` unless bench test makes R17 DNP | local | validation pending |
| `3V3` | `+3V3_NFC_SW` | W048 | FROZEN |

R17 target = 10 kΩ unless the V602 onboard reset circuitry proves it unnecessary. R18 = 10 kΩ from U1 D0/GPIO2 `NFC_MISO` to `+3V3_ALWAYS`.

The green compact RC522 and large blue RC522 are retained only as spares and have no active Defiant wire assignments.

## 17. Unused / superseded

- Q9: DNP.
- W013/W053: DNP / never reuse.
- U3 IRQ: NC.
- green compact RC522: spare / not installed.
- large blue standard RC522: spare / not installed.
- U1 external RESET/BOOT wiring: NC final harness.
- LED1–LED9: superseded placeholders.
- reed switches/NTCs: not installed.
- MT3608 EN: not MCU sleep control.

## 18. Physical verification still required

1. RX1 output/coil pad labels and measured output.
2. BT1 protection proof.
3. U3 V602 reset/backfeed/read-range/charging-coexistence behavior.
4. SK6812 physical count/order.
5. one-sample phaser polarity confirmation.
6. SOT carrier pad numbering/orientation.
7. load/thermal tests for U2/Q1/D1/battery.

## 19. Conclusion

The black XFW-ETLIVE V602 is now the sole active U3 connection table. No black-vs-green selection remains open.
