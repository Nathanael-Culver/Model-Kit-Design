# USS Defiant — Master Wire List

**Document status:** **FORMAL v1.2 — 14-pixel SK6812 chain incorporated / LENGTHS-COLORS-GAUGES OPEN**  
**Sources:** `NETLIST.md`, `PINOUT.md`, `DESIGNATORS.md`, `LIGHTING-LAYOUT.md`.  
**Rule:** wire IDs are permanent. Deleted/unused wires are marked `DNP/SUPERSEDED`; IDs are never renumbered or reused.

## 1. What receives a W-number

A `Wxxx` ID represents a discrete insulated conductor or module lead between physical endpoints. Local same-board traces, component leads, solder bridges, and short carrier connections remain defined in `NETLIST.md`/`CONNECTIONS.md` and do not receive fake harness IDs.

Every fabricated wire ultimately records: ID, endpoints, net/function, color, gauge, routed length, cut length, strip lengths, termination note, and status. Numeric length/gauge/color remain OPEN until physical layout/load measurement.

## 2. Battery / primary power

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W001 | BT1 `+` | U1 BAT+ | `BAT+` | battery -> MCU | fitted only if BT1 protected |
| W002 | BT1 `-` | U1 BAT- | `GND` | battery return -> MCU | fitted only if BT1 protected |
| W003 | BT1 `+` | U5 B+ | `CELL+` | raw cell -> protection | fitted only if BT1 unprotected |
| W004 | BT1 `-` | U5 B- | `CELL-` | raw cell -> protection | fitted only if BT1 unprotected |
| W005 | U5 P+ | U1 BAT+ | `BAT+` | protected battery -> MCU | fitted only if U5 required |
| W006 | U5 P- | U1 BAT-/GND | `GND` | protected return -> MCU | fitted only if U5 required |
| W007 | `BAT+` source node | Q1 source/pin 2 | `BAT+` | battery -> lighting gate | ACTIVE |

## 3. Wireless receiver / charging / wake

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W008 | RX1 positive output | D1 anode/pin 2 | `WLC_5V_RAW` | wireless charge feed | ACTIVE; factory red lead expected positive, meter-check at integration |
| W009 | RX1 negative output | system GND | `GND` | receiver return | ACTIVE; factory black lead expected negative, meter-check at integration |
| W010 | D1 cathode/pin 1 | U1 5V/VBUS | `SYS_5V_IN` | isolated charge/recovery input | ACTIVE |
| W011 | `WLC_5V_RAW` node | R1 high side | `WLC_5V_RAW` | presence-divider feed | ACTIVE |
| W012 | R1/R2 midpoint | U1 D1/GPIO3 | `WLC_PRESENT` | charge-present sense / normal deep-sleep wake | ACTIVE |
| W013 | R1/R2 midpoint | former Q9 gate | `WLC_PRESENT` | former NFC inhibit branch | **DNP / SUPERSEDED — never reuse** |

## 4. Lighting power subsystem

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W014 | Q1 drain/pin 3 | U2 VIN+ | `U2_VIN_SW` | switched battery -> MT3608 | ACTIVE |
| W015 | U2 VIN- | system GND | `GND` | MT3608 input return | ACTIVE |
| W016 | U2 VOUT+ | +5 V lighting distribution | `+5V_LIGHT_SW` | main 5 V feed | ACTIVE |
| W017 | U2 VOUT- | system GND | `GND` | 5 V return | ACTIVE |
| W018 | U1 D7/GPIO20 | Q2 gate/pin 1 | `PERIPH_EN` | master peripheral enable | ACTIVE |
| W019 | Q2 drain/pin 3 | Q1 gate/pin 1 | `LIGHT_GATE` | lighting P-MOS gate pull-low | ACTIVE if separate carriers |
| W020 | Q2 source/pin 2 | system GND | `GND` | lighting helper return | ACTIVE if separate lead required |

## 5. SK6812 level shifter / first pixel

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W021 | U1 D9/GPIO9 | U4 pin 2 A | `SK_DATA_RAW` | 3.3 V LED data | ACTIVE |
| W022 | U4 pin 4 Y | R5 input | `SK_DATA_5V` | shifted data | ACTIVE if discrete wire needed |
| W023 | R5 output | LED14 DIN | `SK_DIN_FIRST` | first physical SK6812 data | ACTIVE |
| W024 | +5 V lighting distribution | U4 pin 5 | `+5V_LIGHT_SW` | U4 power | ACTIVE |
| W025 | U4 pin 3 | system GND | `GND` | U4 return | ACTIVE |
| W026 | +5 V lighting distribution | first SK6812 power-distribution entry | `+5V_LIGHT_SW` | addressable-light power feed | ACTIVE; branch geometry pending hull layout |
| W027 | first SK6812 ground-distribution entry | system GND | `GND` | addressable-light return | ACTIVE; branch geometry pending hull layout |

## 6. Phaser control wires

| ID | From | To | Net | Status |
|---|---|---|---|---|
| W028 | U1 D2/GPIO4 | Q3 gate | `PH0_GATE` | ACTIVE |
| W029 | U1 D3/GPIO5 | Q4 gate | `PH1_GATE` | ACTIVE |
| W030 | U1 D4/GPIO6 | Q5 gate | `PH2_GATE` | ACTIVE |
| W031 | U1 D5/GPIO7 | Q6 gate | `PH3_GATE` | ACTIVE |

## 7. Phaser LED power/sink harness

| ID | From | To | Function | Status |
|---|---|---|---|---|
| W032 | R6 output | LED10 anode | PH0 supply; R6=150 Ω | ACTIVE |
| W033 | LED10 cathode | Q3 drain | PH0 switched return | ACTIVE |
| W034 | Q3 source | GND | PH0 ground | ACTIVE |
| W035 | R7 output | LED11 anode | PH1 supply; R7=150 Ω | ACTIVE |
| W036 | LED11 cathode | Q4 drain | PH1 switched return | ACTIVE |
| W037 | Q4 source | GND | PH1 ground | ACTIVE |
| W038 | R8 output | LED12 anode | PH2 supply; R8=150 Ω | ACTIVE |
| W039 | LED12 cathode | Q5 drain | PH2 switched return | ACTIVE |
| W040 | Q5 source | GND | PH2 ground | ACTIVE |
| W041 | R9 output | LED13 anode | PH3 supply; R9=150 Ω | ACTIVE |
| W042 | LED13 cathode | Q6 drain | PH3 switched return | ACTIVE |
| W043 | Q6 source | GND | PH3 ground | ACTIVE |

Factory leads may satisfy these IDs directly if no extension is required.

## 8. NFC SPI / power harness

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W044 | U1 D8/GPIO8 | U3 SCK | `NFC_SCK` | SPI clock | ACTIVE |
| W045 | U1 D10/GPIO10 | U3 MOSI | `NFC_MOSI` | SPI MCU -> reader | ACTIVE |
| W046 | U3 MISO | U1 D0/GPIO2 | `NFC_MISO` | SPI reader -> MCU | ACTIVE |
| W047 | U1 D6/GPIO21 | U3 SDA/SS/CS | `NFC_CS` | SPI chip select | ACTIVE |
| W048 | Q7 drain/pin 3 | U3 3V3 | `+3V3_NFC_SW` | switched NFC power | ACTIVE |
| W049 | U3 GND | system GND | `GND` | NFC return | ACTIVE |
| W050 | U1 3V3 | Q7 source/pin 2 | `+3V3_ALWAYS` | NFC high-side source | ACTIVE |
| W051 | Q8 drain/pin 3 | Q7 gate/pin 1 | `NFC_GATE` | NFC P-MOS gate pull-low | ACTIVE if carriers separate |
| W052 | Q8 source/pin 2 | system GND | `GND` | NFC helper return | ACTIVE if separate lead required |
| W053 | former Q9 source | system GND | `GND` | former NFC inhibit return | **DNP / SUPERSEDED — never reuse** |

## 9. Frozen SK6812 inter-emitter data chain

Physical chain order is frozen in `LIGHTING-LAYOUT.md`. These wires carry **data only**; 5 V/GND may use parallel trunks/branches.

| ID | From | To | Function | Status |
|---|---|---|---|---|
| W054 | LED14 DOUT | LED15 DIN | P0 top -> P0 bottom | ACTIVE |
| W055 | LED15 DOUT | LED16 DIN | deflector -> port bussard | ACTIVE |
| W056 | LED16 DOUT | LED17 DIN | port bussard -> port chiller forward | ACTIVE |
| W057 | LED17 DOUT | LED18 DIN | port chiller forward -> aft | ACTIVE |
| W058 | LED18 DOUT | LED19 DIN | port chiller -> port impulse crystal A | ACTIVE |
| W059 | LED19 DOUT | LED20 DIN | port impulse crystal A -> B | ACTIVE |
| W060 | LED20 DOUT | LED21 DIN | port crystals -> port impulse engine | ACTIVE |
| W061 | LED21 DOUT | LED22 DIN | aft cross-hull: port engine -> starboard engine | ACTIVE |
| W062 | LED22 DOUT | LED23 DIN | starboard engine -> starboard impulse crystal B | ACTIVE |
| W063 | LED23 DOUT | LED24 DIN | starboard impulse crystal B -> A | ACTIVE |
| W064 | LED24 DOUT | LED25 DIN | starboard crystals -> starboard chiller aft | ACTIVE |
| W065 | LED25 DOUT | LED26 DIN | starboard chiller aft -> forward | ACTIVE |
| W066 | LED26 DOUT | LED27 DIN | starboard chiller -> starboard bussard | ACTIVE |

LED27 DOUT is NC unless a later deliberate test point is approved.

## 10. Local-only items

- R14–R16 are local to the NFC gate network.
- R18 is local from U1 D0/GPIO2 / `NFC_MISO` to `+3V3_ALWAYS`.
- C1 is local to U4.
- C2 is across the switched 5 V distribution node.

## 11. Distribution implementation

GND, BAT+, +5V and +3V3 are electrical nodes. Final physical bus/splice/protoboard implementation remains a mechanical-layout decision. The SK6812 **data path is fixed**, but 5 V/GND should use practical parallel distribution rather than forcing all current through every tiny strip segment.

New discrete distribution jumpers begin at **W067**. W013 and W053 remain permanently DNP.

## 12. Open wire properties

Color, gauge, insulation, routed length, cut length and strip lengths remain OPEN until the components are physically placed in the hull and the current path is finalized.
