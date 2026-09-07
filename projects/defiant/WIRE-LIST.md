# USS Defiant — Master Wire List

**Document status:** **FORMAL v1.1 — Q9 DNP INCORPORATED / LENGTHS-COLORS-GAUGES OPEN**  
**Sources:** `NETLIST.md` FORMAL v1.2, `PINOUT.md` FROZEN v1.0, `DESIGNATORS.md` FROZEN v1.2.  
**Rule:** wire IDs are permanent. Deleted/unused wires are marked `DNP/SUPERSEDED`; IDs are never renumbered or reused.

## 1. What receives a W-number

A `Wxxx` ID represents a discrete insulated conductor or module lead between physical endpoints. Local same-board traces, component leads, solder bridges, and short carrier connections remain defined in `NETLIST.md`/`CONNECTIONS.md` and do not receive fake harness IDs.

## 2. Final wire fields

Every fabricated wire ultimately records: ID, endpoints, net/function, color, gauge, routed length, cut length, strip lengths, termination note, and status. Numeric length/gauge/color remain OPEN until physical layout/load measurement.

## 3. Battery / primary power

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W001 | BT1 `+` | U1 BAT+ | `BAT+` | battery -> MCU | fitted only if BT1 protected |
| W002 | BT1 `-` | U1 BAT- | `GND` | battery return -> MCU | fitted only if BT1 protected |
| W003 | BT1 `+` | U5 B+ | `CELL+` | raw cell -> protection | fitted only if BT1 unprotected |
| W004 | BT1 `-` | U5 B- | `CELL-` | raw cell -> protection | fitted only if BT1 unprotected |
| W005 | U5 P+ | U1 BAT+ | `BAT+` | protected battery -> MCU | fitted only if U5 required |
| W006 | U5 P- | U1 BAT-/GND | `GND` | protected return -> MCU | fitted only if U5 required |
| W007 | `BAT+` source node | Q1 source/pin 2 | `BAT+` | battery -> lighting gate | ACTIVE |

## 4. Wireless receiver / charging / wake

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W008 | RX1 positive output | D1 anode/pin 2 | `WLC_5V_RAW` | wireless charge feed | ACTIVE; RX1 pad verify |
| W009 | RX1 negative output | system GND | `GND` | receiver return | ACTIVE; RX1 pad verify |
| W010 | D1 cathode/pin 1 | U1 5V/VBUS | `SYS_5V_IN` | isolated charge/recovery input | ACTIVE |
| W011 | `WLC_5V_RAW` node | R1 high side | `WLC_5V_RAW` | presence-divider feed | ACTIVE |
| W012 | R1/R2 midpoint | U1 D1/GPIO3 | `WLC_PRESENT` | charge-present sense / **normal deep-sleep wake** | ACTIVE |
| W013 | R1/R2 midpoint | former Q9 gate | `WLC_PRESENT` | former NFC inhibit branch | **DNP / SUPERSEDED — Q9 removed; never reuse ID** |

## 5. Lighting power subsystem

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W014 | Q1 drain/pin 3 | U2 IN+ | `U2_VIN_SW` | switched battery -> MT3608 | ACTIVE |
| W015 | U2 IN- | system GND | `GND` | MT3608 input return | ACTIVE |
| W016 | U2 OUT+ | +5 V lighting distribution | `+5V_LIGHT_SW` | main 5 V feed | ACTIVE |
| W017 | U2 OUT- | system GND | `GND` | 5 V return | ACTIVE |
| W018 | U1 D7/GPIO20 | Q2 gate/pin 1 | `PERIPH_EN` | master peripheral enable | ACTIVE |
| W019 | Q2 drain/pin 3 | Q1 gate/pin 1 | `LIGHT_GATE` | lighting P-MOS gate pull-low | ACTIVE if separate carriers |
| W020 | Q2 source/pin 2 | system GND | `GND` | lighting helper return | ACTIVE if separate lead required |

## 6. SK6812 data / level shifter

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W021 | U1 D9/GPIO9 | U4 pin 2 A | `SK_DATA_RAW` | 3.3 V LED data | ACTIVE |
| W022 | U4 pin 4 Y | R5 input | `SK_DATA_5V` | shifted data | ACTIVE if discrete wire needed |
| W023 | R5 output | LED14 DIN | `SK_DIN_FIRST` | first physical SK6812 data | ACTIVE once location confirmed |
| W024 | +5 V lighting distribution | U4 pin 5 | `+5V_LIGHT_SW` | U4 power | ACTIVE |
| W025 | U4 pin 3 | system GND | `GND` | U4 return | ACTIVE |
| W026 | +5 V lighting distribution | first SK6812 power entry | `+5V_LIGHT_SW` | addressable-light power harness | ACTIVE; downstream topology OPEN |
| W027 | first SK6812 ground entry | system GND | `GND` | addressable-light return | ACTIVE; downstream topology OPEN |

Physical LED14+ inter-emitter wires receive new IDs only after count/order/layout is confirmed.

## 7. Phaser control wires

| ID | From | To | Net | Status |
|---|---|---|---|---|
| W028 | U1 D2/GPIO4 | Q3 gate | `PH0_GATE` | ACTIVE |
| W029 | U1 D3/GPIO5 | Q4 gate | `PH1_GATE` | ACTIVE |
| W030 | U1 D4/GPIO6 | Q5 gate | `PH2_GATE` | ACTIVE |
| W031 | U1 D5/GPIO7 | Q6 gate | `PH3_GATE` | ACTIVE |

## 8. Phaser LED power/sink harness

| ID | From | To | Function | Status |
|---|---|---|---|---|
| W032 | +5 V/R6 output | LED10 anode | PH0 supply | ACTIVE; R6 TBD/DNP |
| W033 | LED10 cathode | Q3 drain | PH0 switched return | ACTIVE |
| W034 | Q3 source | GND | PH0 ground | ACTIVE |
| W035 | +5 V/R7 output | LED11 anode | PH1 supply | ACTIVE; R7 TBD/DNP |
| W036 | LED11 cathode | Q4 drain | PH1 switched return | ACTIVE |
| W037 | Q4 source | GND | PH1 ground | ACTIVE |
| W038 | +5 V/R8 output | LED12 anode | PH2 supply | ACTIVE; R8 TBD/DNP |
| W039 | LED12 cathode | Q5 drain | PH2 switched return | ACTIVE |
| W040 | Q5 source | GND | PH2 ground | ACTIVE |
| W041 | +5 V/R9 output | LED13 anode | PH3 supply | ACTIVE; R9 TBD/DNP |
| W042 | LED13 cathode | Q6 drain | PH3 switched return | ACTIVE |
| W043 | Q6 source | GND | PH3 ground | ACTIVE |

Factory leads may satisfy these connection IDs directly if no extension is required.

## 9. NFC SPI / power harness

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W044 | U1 D8/GPIO8 | U3 SCK | `NFC_SCK` | SPI clock | ACTIVE |
| W045 | U1 D10/GPIO10 | U3 MOSI | `NFC_MOSI` | SPI MCU -> reader | ACTIVE |
| W046 | U3 MISO | U1 D0/GPIO2 | `NFC_MISO` | SPI reader -> MCU | ACTIVE |
| W047 | U1 D6/GPIO21 | U3 SDA/SS/CS | `NFC_CS` | SPI chip select | ACTIVE |
| W048 | Q7 drain/pin 3 | U3 VCC | `+3V3_NFC_SW` | switched NFC power | ACTIVE |
| W049 | U3 GND | system GND | `GND` | NFC return | ACTIVE |

## 10. NFC power-gate control

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W050 | U1 3V3 | Q7 source/pin 2 | `+3V3_ALWAYS` | NFC high-side source | ACTIVE |
| W051 | Q8 drain/pin 3 | Q7 gate/pin 1 | `NFC_GATE` | NFC P-MOS gate pull-low | ACTIVE if carriers separate |
| W052 | Q8 source/pin 2 | system GND | `GND` | NFC helper return | ACTIVE if separate lead required |
| W053 | former Q9 source | system GND | `GND` | former NFC inhibit return | **DNP / SUPERSEDED — Q9 removed; never reuse ID** |

R14–R16 are local. `PERIPH_EN` reaches Q8 through R15. **There is no WLC_PRESENT branch into the NFC gate. NFC is allowed while charging.**

## 11. U1 GPIO2 boot pull-up

R18 is local:

- U1 D0/GPIO2 / `NFC_MISO` -> R18 -> `+3V3_ALWAYS`

## 12. Distribution implementation

GND, BAT+, +5V and +3V3 distribution nodes are electrical nodes only. Final physical bus/splice/protoboard implementation remains a layout decision. Any new discrete jumpers receive the next unused W-number.

## 13. Open wire properties

Color, gauge, insulation, routed length, cut length and strip lengths remain OPEN until actual load and hull routing are measured.

## 14. Future additions

New W-numbers begin at **W054**. W013 and W053 remain permanently DNP and are not reused. Future IDs cover:

1. LED14+ inter-emitter power/data/ground wiring;
2. any final distribution-node jumpers;
3. U5-specific additions if required;
4. deliberate test/service leads;
5. necessary LED lead extensions.

## 15. Conclusion

The stable base harness remains numbered through W053. Q9's two associated wire positions are preserved as DNP for traceability, and the approved architecture now allows NFC operation while wireless charging is present.