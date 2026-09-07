# USS Defiant — Master Wire List

**Document status:** **FORMAL v1.0 — ELECTRICAL ENDPOINTS ASSIGNED / LENGTHS-COLORS-GAUGES OPEN**  
**Sources:** `NETLIST.md` FORMAL v1.0, `PINOUT.md` FROZEN v1.0, `DESIGNATORS.md` FROZEN v1.0.  
**Rule:** wire IDs are permanent. Deleted/unused wires are marked `DNP/SUPERSEDED`; IDs are never renumbered or reused.

## 1. What receives a W-number

A `Wxxx` ID represents a discrete insulated conductor or module lead that must be fabricated/routed between physical endpoints.

Local connections that can be made directly on the same carrier/protoboard by component lead, pad, solder bridge, or PCB/copper trace remain authoritative in `NETLIST.md`/`CONNECTIONS.md` and **do not receive a fake wire number solely for documentation**.

Factory-attached LED leads are treated as part of the LED assembly unless extended; any extension receives its own W-number later.

## 2. Required final fields

Every fabricated wire ultimately records:

- Wire ID
- From component/pin
- To component/pin
- Net
- function/class
- color
- gauge
- routed length
- cut length
- strip length at each end
- termination/solder note
- status

No numeric length or final gauge/color is allowed until the physical layout and available wire inventory are measured.

## 3. Battery / primary power

The battery-protection decision creates two mutually exclusive branches.

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W001 | BT1 `+` lead | U1 BAT+ pad | `BAT+` | battery -> MCU | **FITTED only if BT1 has integral protection; otherwise DNP** |
| W002 | BT1 `-` lead | U1 BAT- pad | `GND` | battery return -> MCU | **FITTED only if BT1 has integral protection; otherwise DNP** |
| W003 | BT1 `+` lead | U5 B+ | `CELL+` | raw cell -> protection | **FITTED only if BT1 is unprotected; otherwise DNP** |
| W004 | BT1 `-` lead | U5 B- | `CELL-` | raw cell -> protection | **FITTED only if BT1 is unprotected; otherwise DNP** |
| W005 | U5 P+ | U1 BAT+ pad | `BAT+` | protected battery -> MCU | **FITTED only if U5 required; otherwise DNP** |
| W006 | U5 P- | U1 BAT- / GND node | `GND` | protected return -> MCU | **FITTED only if U5 required; otherwise DNP** |
| W007 | `BAT+` source node | Q1 source / pin 2 | `BAT+` | battery -> lighting high-side switch | ACTIVE; source node is BT1+ if protected pack, U5 P+ if U5 fitted |

## 4. Wireless receiver / charging / wake

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W008 | RX1 positive output | D1 anode / pin 2 | `WLC_5V_RAW` | wireless charge feed | ACTIVE; exact RX1 pad label still verify physically |
| W009 | RX1 negative output | system GND distribution | `GND` | wireless receiver return | ACTIVE; exact RX1 pad label still verify physically |
| W010 | D1 cathode / pin 1, marked-bar end | U1 5V/VBUS pad | `SYS_5V_IN` | isolated wireless input -> XIAO charging/recovery | ACTIVE |
| W011 | RX1 positive / `WLC_5V_RAW` node | R1 high side | `WLC_5V_RAW` | wireless-presence divider feed | ACTIVE; may be local jumper depending final board layout |
| W012 | R1/R2 divider midpoint | U1 D1 / GPIO3 | `WLC_PRESENT` | deep-sleep wake / charge-present sense | ACTIVE |
| W013 | R1/R2 divider midpoint | Q9 gate / pin 1 | `WLC_PRESENT` | hardware NFC inhibit | ACTIVE; may be local jumper |

## 5. Lighting power subsystem

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W014 | Q1 drain / pin 3 | U2 IN+ | `U2_VIN_SW` | switched battery -> MT3608 | ACTIVE |
| W015 | U2 IN- | system GND distribution | `GND` | MT3608 input return | ACTIVE |
| W016 | U2 OUT+ | +5 V lighting distribution node | `+5V_LIGHT_SW` | main 5 V lighting feed | ACTIVE |
| W017 | U2 OUT- | system GND distribution | `GND` | 5 V rail return | ACTIVE |
| W018 | U1 D7 / GPIO20 | Q2 gate / pin 1 | `PERIPH_EN` | master peripheral-enable control | ACTIVE |
| W019 | Q2 drain / pin 3 | Q1 gate / pin 1 | `LIGHT_GATE` | lighting P-MOS gate pull-low | ACTIVE if Q1/Q2 carriers are separate; otherwise same-board local connection |
| W020 | Q2 source / pin 2 | system GND distribution | `GND` | lighting helper return | ACTIVE if separate carrier lead required |

R3 and R4 are local gate-bias components and are not assigned separate W-numbers unless the physical assembly places them remotely from Q1/Q2.

## 6. SK6812 data / level shifter

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W021 | U1 D9 / GPIO9 | U4 pin 2 `A` | `SK_DATA_RAW` | 3.3 V addressable-lighting data | ACTIVE |
| W022 | U4 pin 4 `Y` | R5 input | `SK_DATA_5V` | 5 V shifted data | ACTIVE if R5 not mounted directly at U4 output |
| W023 | R5 output | LED14 DIN | `SK_DIN_FIRST` | first physical SK6812 data input | ACTIVE once LED14 physical location is confirmed |
| W024 | +5 V lighting distribution | U4 pin 5 VCC | `+5V_LIGHT_SW` | level-shifter power | ACTIVE |
| W025 | U4 pin 3 GND | system GND distribution | `GND` | level-shifter return | ACTIVE |
| W026 | +5 V lighting distribution | first SK6812 power-distribution entry | `+5V_LIGHT_SW` | addressable-lighting power harness | ACTIVE; downstream branch topology waits on physical emitter layout |
| W027 | first SK6812 ground-distribution entry | system GND distribution | `GND` | addressable-lighting return harness | ACTIVE; downstream topology waits on physical emitter layout |

U4 pin 1 `OE` is tied locally to U4 pin 3/GND and does not need a separate harness wire.

### Physical SK6812 chain wires still to append

Inter-emitter data, 5 V, and ground conductors for `LED14+` receive the next unused W-numbers **after physical emitter count/order and hull placement are confirmed**. This is the only major harness section that cannot yet be enumerated without guessing the physical lighting layout.

## 7. Four pulse-phaser control wires

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W028 | U1 D2 / GPIO4 | Q3 gate / pin 1 | `PH0_GATE` | phaser 0 control | ACTIVE |
| W029 | U1 D3 / GPIO5 | Q4 gate / pin 1 | `PH1_GATE` | phaser 1 control | ACTIVE |
| W030 | U1 D4 / GPIO6 | Q5 gate / pin 1 | `PH2_GATE` | phaser 2 control | ACTIVE |
| W031 | U1 D5 / GPIO7 | Q6 gate / pin 1 | `PH3_GATE` | phaser 3 control | ACTIVE |

R10–R13 gate pull-downs are local to Q3–Q6 and do not receive separate W-numbers unless later physical placement requires remote wiring.

## 8. Phaser LED power/sink harness

The prewired LED factory leads are part of LED10–LED13. These W-numbers cover any fabricated conductor between the power/switch assembly and those factory leads.

| ID | From | To | Net/function | Status |
|---|---|---|---|---|
| W032 | +5 V lighting distribution / R6 output as finally assembled | LED10 anode factory lead | PH0 LED supply | ACTIVE; R6 value or DNP still pending LED verification |
| W033 | LED10 cathode factory lead | Q3 drain / pin 3 | PH0 switched return | ACTIVE |
| W034 | Q3 source / pin 2 | system GND distribution | `GND` | ACTIVE |
| W035 | +5 V lighting distribution / R7 output | LED11 anode factory lead | PH1 LED supply | ACTIVE; R7 value/DNP pending |
| W036 | LED11 cathode factory lead | Q4 drain / pin 3 | PH1 switched return | ACTIVE |
| W037 | Q4 source / pin 2 | system GND distribution | `GND` | ACTIVE |
| W038 | +5 V lighting distribution / R8 output | LED12 anode factory lead | PH2 LED supply | ACTIVE; R8 value/DNP pending |
| W039 | LED12 cathode factory lead | Q5 drain / pin 3 | PH2 switched return | ACTIVE |
| W040 | Q5 source / pin 2 | system GND distribution | `GND` | ACTIVE |
| W041 | +5 V lighting distribution / R9 output | LED13 anode factory lead | PH3 LED supply | ACTIVE; R9 value/DNP pending |
| W042 | LED13 cathode factory lead | Q6 drain / pin 3 | PH3 switched return | ACTIVE |
| W043 | Q6 source / pin 2 | system GND distribution | `GND` | ACTIVE |

If the factory leads reach the final switch/power assembly directly, W032/W033 etc. may be implemented by the factory lead itself and marked `INTEGRAL LEAD` rather than fabricating an extension. The wire ID remains attached to that connection requirement.

## 9. NFC SPI harness

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W044 | U1 D8 / GPIO8 | U3 SCK | `NFC_SCK` | SPI clock | ACTIVE; exact U3 header label/order verify physically |
| W045 | U1 D10 / GPIO10 | U3 MOSI | `NFC_MOSI` | SPI MCU -> reader | ACTIVE |
| W046 | U3 MISO | U1 D0 / GPIO2 | `NFC_MISO` | SPI reader -> MCU | ACTIVE |
| W047 | U1 D6 / GPIO21 | U3 SDA/SS/CS | `NFC_CS` | SPI chip-select | ACTIVE |
| W048 | Q7 drain / pin 3 | U3 3.3V/VCC | `+3V3_NFC_SW` | switched NFC power | ACTIVE |
| W049 | U3 GND | system GND distribution | `GND` | NFC return | ACTIVE |

U3 IRQ is NC. U3 RST/NRSTPD is locally biased to `+3V3_NFC_SW` by R17 unless the exact board makes R17 DNP.

## 10. NFC power-gate control

| ID | From | To | Net | Function | Status |
|---|---|---|---|---|---|
| W050 | U1 3V3 pad | Q7 source / pin 2 | `+3V3_ALWAYS` | NFC high-side source supply | ACTIVE |
| W051 | Q8 drain / pin 3 | Q7 gate / pin 1 | `NFC_GATE` | NFC P-MOS gate pull-low | ACTIVE if carriers separate; otherwise local |
| W052 | Q8 source / pin 2 | system GND distribution | `GND` | NFC enable helper return | ACTIVE if separate lead required |
| W053 | Q9 source / pin 2 | system GND distribution | `GND` | NFC inhibit return | ACTIVE if separate lead required |

R14–R16 and the Q8/Q9 gate-control junctions are local board connections. `PERIPH_EN` reaches the NFC-control network through R15 as defined in `NETLIST.md`; a separate long harness branch is not required if Q2/Q7/Q8/Q9 are consolidated on the control board.

## 11. U1 GPIO2 boot pull-up

R18 is local to U1/control-board wiring:

- U1 D0/GPIO2 / `NFC_MISO` -> R18 -> `+3V3_ALWAYS`

No additional W-number is required unless R18 is physically remote. The pull-up must not be omitted simply because it is not represented as an independent harness wire.

## 12. Ground and power distribution implementation

`system GND distribution`, `+5 V lighting distribution`, and the control-board `+3V3_ALWAYS` junctions are **electrical nodes**, not permission to create arbitrary hidden wiring.

Their physical implementation is deferred to the mechanical/harness-layout step and may be:

- a solderable protoboard bus,
- a deliberate star/splice point,
- appropriately sized copper tape where RF/coil placement permits,
- or direct grouped solder joints.

Once the distribution topology is selected, any additional discrete jumpers receive new W-numbers. Existing IDs are not renumbered.

## 13. Wire properties still intentionally open

The following are not guessed in Step 7:

- color
- gauge
- insulation type
- routed length
- cut length
- strip length
- whether some short connection is wire vs board trace/solder bridge

Gauge will be chosen by measured current and physical length, not simply by convenience. Signal wires and LED data can be fine gauge; battery/boost/5 V distribution must be sized for measured lighting current.

## 14. Step-7 unresolved additions

The base harness now has permanent IDs through **W053**. Additional wire IDs are added later for:

1. physical `LED14+` SK6812 inter-emitter power/data/ground wiring after emitter count/order is confirmed;
2. any U5 battery-protection connections if the exact protection module has more/different physical terminals than the reserved B+/B-/P+/P- convention;
3. test points/service leads deliberately added after validation planning;
4. distribution-node jumpers created by the final protoboard/mechanical layout;
5. any LED lead extensions proven necessary by hull measurements.

## 15. Step-7 conclusion

The stable electrical harness endpoints now have permanent W-identifiers. The list is complete enough to build the per-component pin tables in Step 8 without pretending that unknown hull lengths, wire colors, gauges, or physical SK6812 routing have already been measured.
