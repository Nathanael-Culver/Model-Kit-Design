# USS Defiant — Per-Component Pin / Connection Tables

**Document status:** **FORMAL v1.0 — STEP 8 COMPLETE ENOUGH TO PROCEED**  
**Sources:** `POWER-ARCHITECTURE.md`, `DESIGNATORS.md`, `NETLIST.md`, `PINOUT.md`, `WIRE-LIST.md`.  
**Rule:** every installed electrical terminal must resolve to a named net, `NC`, `DNP`, or a conditional branch. Exact physical header order on generic modules must still be verified from the actual hardware before soldering.

## 1. U1 — Seeed Studio XIAO ESP32-C3

| U1 pin/pad | ESP32-C3 GPIO | Net / function | Wire ID / local connection | Status |
|---|---:|---|---|---|
| BAT+ pad | — | `BAT+` | W001 if BT1 protected; W005 if U5 fitted | **FROZEN conditional branch** |
| BAT- pad | — | `GND` | W002 if BT1 protected; W006 if U5 fitted | **FROZEN conditional branch** |
| 5V / VBUS pad | — | `SYS_5V_IN` | W010 from D1 cathode | **FROZEN** |
| 3V3 pad | — | `+3V3_ALWAYS` | W050 to Q7 source; local feeds R14/R18 as applicable | **FROZEN** |
| GND pad | — | `GND` | system ground distribution | **FROZEN** |
| D0 / A0 | GPIO2 | `NFC_MISO` | W046 from U3 MISO; R18 local pull-up to `+3V3_ALWAYS` | **FROZEN** |
| D1 / A1 | GPIO3 | `WLC_PRESENT` | W012 from R1/R2 midpoint | **FROZEN; deep-sleep wake input** |
| D2 / A2 | GPIO4 | `PH0_GATE` | W028 to Q3 gate | **FROZEN** |
| D3 / A3 | GPIO5 | `PH1_GATE` | W029 to Q4 gate | **FROZEN** |
| D4 / SDA | GPIO6 | `PH2_GATE` | W030 to Q5 gate | **FROZEN** |
| D5 / SCL | GPIO7 | `PH3_GATE` | W031 to Q6 gate | **FROZEN** |
| D6 / TX | GPIO21 | `NFC_CS` | W047 to U3 SDA/SS/CS | **FROZEN** |
| D7 / RX | GPIO20 | `PERIPH_EN` | W018 to Q2 gate/control node; R4 local pull-down; R15 branch into NFC control | **FROZEN** |
| D8 / SCK | GPIO8 | `NFC_SCK` | W044 to U3 SCK | **FROZEN** |
| D9 / MISO | GPIO9 | `SK_DATA_RAW` | W021 to U4 pin 2 A | **FROZEN; critical BOOT strap** |
| D10 / MOSI | GPIO10 | `NFC_MOSI` | W045 to U3 MOSI | **FROZEN** |
| RESET / EN | — | service only | no permanent project connection | **NC in final harness unless later test fixture approved** |
| BOOT switch | GPIO9 onboard | onboard function | no external project connection | **Do not obstruct** |

## 2. BT1 — 103450 LiPo

Only one branch is assembled.

### If BT1 contains integral protection

| BT1 lead | Net | Connection | Wire |
|---|---|---|---|
| `+` | `BAT+` | U1 BAT+ and BAT+ distribution/Q1 source branch | W001 to U1; W007 from BAT+ node to Q1 |
| `-` | `GND` | U1 BAT- / system ground | W002 |

### If BT1 is unprotected

| BT1 lead | Net | Connection | Wire |
|---|---|---|---|
| `+` | `CELL+` | U5 B+ | W003 |
| `-` | `CELL-` | U5 B- | W004 |

BT1 protection status remains a required physical safety check.

## 3. U5 — optional 1S LiPo protection device/module

**Condition:** fitted only if BT1 is confirmed unprotected. Exact protection module is not yet selected because it may be unnecessary.

| U5 functional terminal | Net | Connection | Wire | Status |
|---|---|---|---|---|
| B+ | `CELL+` | BT1 + | W003 | conditional |
| B- | `CELL-` | BT1 - | W004 | conditional |
| P+ / protected + | `BAT+` | U1 BAT+ / BAT+ distribution | W005; W007 branches from protected BAT+ node to Q1 | conditional |
| P- / protected - | `GND` | U1 BAT- / system GND | W006 | conditional |

If a selected protection device uses a different terminal convention, the net functions remain unchanged but physical labels must be documented before assembly.

## 4. RX1 — XKT wireless-power receiver

Exact pad names/order must be verified from the physical receiver before soldering.

| RX1 functional terminal | Net | Connection | Wire | Status |
|---|---|---|---|---|
| positive DC output | `WLC_5V_RAW` | D1 anode and R1 divider feed | W008 to D1; W011 branch to R1 | **FROZEN function / physical pad OPEN** |
| negative DC output | `GND` | system ground | W009 | **FROZEN function / physical pad OPEN** |
| coil terminal A | receiver coil | factory/purchased coil | integral assembly | verify physical module |
| coil terminal B | receiver coil | factory/purchased coil | integral assembly | verify physical module |

## 5. TX1 — XKT-412 transmitter

TX1 is external to the sealed ship and therefore not part of the internal W001+ harness.

| TX1 function | Connection | Status |
|---|---|---|
| DC input | external power supply appropriate to exact TX1 module | physical connector/polarity to verify |
| coil outputs | TX1 transmitter coil | purchased assembly; physical labels to verify |

## 6. D1 — PMEG2010ER,115 Schottky

| D1 pin | Polarity | Net | Connection | Wire |
|---:|---|---|---|---|
| 1 | K / cathode / marked-bar end | `SYS_5V_IN` | U1 5V/VBUS | W010 |
| 2 | A / anode | `WLC_5V_RAW` | RX1 positive output | W008 |

**Direction:** RX1 -> D1 anode -> D1 cathode -> U1 5V.

## 7. R1 / R2 — wireless-present divider

| Part | Terminal | Net / connection | Wire / note |
|---|---|---|---|
| R1 130 kΩ | high side | `WLC_5V_RAW` | W011 |
| R1 130 kΩ | low side | `WLC_PRESENT` | divider midpoint |
| R2 180 kΩ | high side | `WLC_PRESENT` | midpoint feeds W012 to U1 and W013 to Q9 |
| R2 180 kΩ | low side | `GND` | local ground |

## 8. Q1 / Q2 — lighting high-side power gate

### Q1 — AO3401A P-channel

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | Gate | `LIGHT_GATE` | Q2 drain; R3 pull-up to BAT+ | W019 if carriers separate |
| 2 | Source | `BAT+` | protected battery node | W007 |
| 3 | Drain | `U2_VIN_SW` | U2 IN+ | W014 |

### Q2 — AO3400A N-channel

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | Gate | `PERIPH_EN` | U1 D7/GPIO20; R4 to GND | W018 |
| 2 | Source | `GND` | system ground | W020 if separate carrier |
| 3 | Drain | `LIGHT_GATE` | Q1 gate | W019 if separate carrier |

### Local gate resistors

| Ref | Value | Connection |
|---|---:|---|
| R3 | 100 kΩ | Q1 gate / `LIGHT_GATE` -> `BAT+` |
| R4 | 100 kΩ | Q2 gate / `PERIPH_EN` -> `GND` |

## 9. U2 — MT3608 boost-converter module

Exact board pad labels/order still require physical confirmation; these are the frozen functional endpoints.

| U2 functional pad | Net | Connection | Wire |
|---|---|---|---|
| IN+ | `U2_VIN_SW` | Q1 drain | W014 |
| IN- | `GND` | system ground | W015 |
| OUT+ | `+5V_LIGHT_SW` | 5 V lighting distribution | W016 |
| OUT- | `GND` | system ground | W017 |
| EN, if accessible | board-normal enabled state | not used as primary sleep isolation | no project GPIO |

Do not wire directly to bare MT3608 IC pins unless an explicit module modification is later approved.

## 10. U4 — SN74AHCT1G125DBVR

| U4 pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | `OE` active-low | `GND` | tied locally to ground / pin 3 node | local |
| 2 | A | `SK_DATA_RAW` | U1 D9/GPIO9 | W021 |
| 3 | GND | `GND` | system ground; C1 low side; OE local tie | W025 |
| 4 | Y | `SK_DATA_5V` | R5 input | W022 if R5 not directly mounted |
| 5 | VCC | `+5V_LIGHT_SW` | switched 5 V; C1 high side | W024 |

### U4 passives

| Ref | Value | Connection |
|---|---:|---|
| C1 | 0.1 µF ceramic | U4 pin 5 / `+5V_LIGHT_SW` -> U4 pin 3 / `GND`, physically adjacent |
| R5 | 330 Ω | U4 pin 4 / `SK_DATA_5V` -> `SK_DIN_FIRST` / LED14 DIN |

## 11. C2 — lighting-rail bulk capacitor

| C2 terminal | Net | Connection |
|---|---|---|
| `+` | `+5V_LIGHT_SW` | 5 V lighting distribution |
| `-` | `GND` | lighting/system ground distribution |

Target value: 470 µF, at least 6.3 V rating; 10 V preferred if size permits. Final value remains subject to physical SK6812 count/load validation.

## 12. Physical SK6812 emitters — LED14+

The exact emitter count/order remains intentionally open. Each confirmed physical emitter receives the next LED reference in serial-chain order.

### LED14 — first physical emitter

| LED14 function/pad | Net | Connection | Wire/status |
|---|---|---|---|
| VDD | `+5V_LIGHT_SW` | SK6812 5 V distribution | W026 enters lighting harness; exact branch topology later |
| GND | `GND` | SK6812 ground distribution | W027 enters lighting harness; exact branch topology later |
| DIN | `SK_DIN_FIRST` | R5 output | W023 |
| DOUT | next SK data net | LED15 DIN if LED15 exists | wire ID assigned after physical chain count/order confirmed |

### LED15 and later

For each subsequent physical SK6812:

- VDD -> `+5V_LIGHT_SW`
- GND -> `GND`
- DIN <- previous emitter DOUT
- DOUT -> next emitter DIN, or NC on the last physical emitter

Logical zones P0–P8 are mapped in firmware and do not alter these electrical pin rules.

## 13. Q3–Q6 — four pulse-phaser switches

All are AO3400A N-channel MOSFETs.

| Ref | Pin 1 Gate | Pin 2 Source | Pin 3 Drain | Gate pull-down |
|---|---|---|---|---|
| Q3 / PH0 | `PH0_GATE`, W028 | `GND`, W034 | LED10 cathode, W033 | R10 100 kΩ -> GND |
| Q4 / PH1 | `PH1_GATE`, W029 | `GND`, W037 | LED11 cathode, W036 | R11 100 kΩ -> GND |
| Q5 / PH2 | `PH2_GATE`, W030 | `GND`, W040 | LED12 cathode, W039 | R12 100 kΩ -> GND |
| Q6 / PH3 | `PH3_GATE`, W031 | `GND`, W043 | LED13 cathode, W042 | R13 100 kΩ -> GND |

## 14. LED10–LED13 — prewired white pulse-phaser LEDs

Do not infer polarity from lead color until one physical LED is verified.

| LED ref | Function | Anode connection | Cathode connection | Status |
|---|---|---|---|---|
| LED10 | PH0 | R6 output / W032 | Q3 drain / W033 | R6 value or DNP pending actual LED inspection |
| LED11 | PH1 | R7 output / W035 | Q4 drain / W036 | R7 value or DNP pending |
| LED12 | PH2 | R8 output / W038 | Q5 drain / W039 | R8 value or DNP pending |
| LED13 | PH3 | R9 output / W041 | Q6 drain / W042 | R9 value or DNP pending |

### Phaser current-limit positions

| Ref | Input | Output | Status |
|---|---|---|---|
| R6 | `+5V_LIGHT_SW` | LED10 anode / W032 | value TBD or DNP if verified prewired resistor exists |
| R7 | `+5V_LIGHT_SW` | LED11 anode / W035 | value TBD or DNP |
| R8 | `+5V_LIGHT_SW` | LED12 anode / W038 | value TBD or DNP |
| R9 | `+5V_LIGHT_SW` | LED13 anode / W041 | value TBD or DNP |

## 15. Q7 / Q8 / Q9 — NFC power and wireless inhibit

### Q7 — AO3401A P-channel high-side switch

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | Gate | `NFC_GATE` | Q8 drain; R14 pull-up | W051 if carriers separate |
| 2 | Source | `+3V3_ALWAYS` | U1 3V3 | W050 |
| 3 | Drain | `+3V3_NFC_SW` | U3 VCC | W048 |

### Q8 — AO3400A NFC-enable helper

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | Gate | `NFC_EN_GATE` | R15 from `PERIPH_EN`; R16 to GND; Q9 drain clamp | local control node |
| 2 | Source | `GND` | system ground | W052 if separate carrier |
| 3 | Drain | `NFC_GATE` | Q7 gate | W051 if separate carrier |

### Q9 — AO3400A wireless-present inhibit

| Pin | Name | Net | Connection | Wire/local |
|---:|---|---|---|---|
| 1 | Gate | `WLC_PRESENT` | R1/R2 midpoint | W013 |
| 2 | Source | `GND` | system ground | W053 if separate carrier |
| 3 | Drain | `NFC_EN_GATE` | clamps Q8 gate/control node low while wireless power present | local |

### NFC gate resistors

| Ref | Value | Connection |
|---|---:|---|
| R14 | 100 kΩ | `NFC_GATE` / Q7 gate -> `+3V3_ALWAYS` |
| R15 | 10 kΩ | `PERIPH_EN` -> `NFC_EN_GATE` / Q8 gate |
| R16 | 100 kΩ | `NFC_EN_GATE` / Q8 gate -> `GND` |

Hardware truth condition remains: **NFC power = PERIPH_EN AND NOT WLC_PRESENT**.

## 16. U3 — MFRC522 breakout

Exact physical header spelling/order must be verified on the actual board. The functional connections are frozen.

| U3 function/header label | Net | Connection | Wire | Status |
|---|---|---|---|---|
| 3.3V / VCC | `+3V3_NFC_SW` | Q7 drain | W048 | **FROZEN function** |
| GND | `GND` | system ground | W049 | **FROZEN** |
| SCK | `NFC_SCK` | U1 D8/GPIO8 | W044 | **FROZEN function** |
| MOSI | `NFC_MOSI` | U1 D10/GPIO10 | W045 | **FROZEN function** |
| MISO | `NFC_MISO` | U1 D0/GPIO2 | W046 | **FROZEN function** |
| SDA / SS / CS | `NFC_CS` | U1 D6/GPIO21 | W047 | **FROZEN function; exact printed label verify** |
| RST / NRSTPD | reset bias | R17 to `+3V3_NFC_SW` unless onboard bias makes R17 DNP | local | **physical-board behavior OPEN** |
| IRQ | NC | no project connection | none | **NC** |

### R17

- target 10 kΩ from U3 RST/NRSTPD to `+3V3_NFC_SW`
- mark DNP if the exact breakout already includes a suitable pull-up and power-cycle reset is verified

## 17. R18 — GPIO2 boot pull-up

| R18 terminal | Net / connection |
|---|---|
| one side | U1 D0/GPIO2 / `NFC_MISO` |
| other side | `+3V3_ALWAYS` |

Value: **10 kΩ**. Required by the frozen Step-6 pin map unless later bench evidence forces a documented engineering change.

## 18. Unused / superseded items

- U3 IRQ: **NC**.
- U1 external RESET/BOOT wiring: **NC for final harness** unless a deliberate service fixture is later approved.
- LED1–LED9: **SUPERSEDED placeholders; never use as physical LED refs**.
- reed switches and NTC thermistors: purchased spares, **not installed**.
- MT3608 EN: not used as an MCU-controlled sleep switch.

## 19. Physical verification still required before soldering generic modules

The electrical destination of every active pin is now defined, but these exact physical labels/order remain to be checked from the hardware:

1. RX1 positive/negative output pads and coil pads.
2. U2 IN+/IN-/OUT+/OUT- board orientation.
3. U3 header order and exact `SDA/SS/CS`, `RST`, `IRQ` labeling.
4. U5 terminal labels only if U5 becomes necessary.
5. actual SK6812 package pad direction/arrows and total physical emitter order.
6. LED10–LED13 polarity and built-in resistor status.
7. SOT-23/SOT-23-5 carrier pad numbering/orientation before any Q1–Q9/U4 is soldered.

## 20. Step-8 conclusion

Every currently defined installed component now has a pin/function table tied to the frozen net names and, where appropriate, permanent W001–W053 wire IDs. The remaining OPEN items are physical-identification/bench-validation items rather than missing circuit destinations.
