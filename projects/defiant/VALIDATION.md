# USS Defiant — Electrical Validation Register

**Document status:** **STEP 9 STATIC AUDIT COMPLETE / PHYSICAL VALIDATION PENDING**  
**Release rule:** no final schematic/CAD release while any `ERROR` remains, any hardware-critical `BLOCKER` is untested, or any explicit design-policy blocker is unresolved.

Severity:

- `ERROR` — electrically invalid/unsafe until resolved
- `BLOCKER` — must be physically proven or explicitly decided before release
- `WARNING` — acceptable only with stated test/mitigation
- `PASS` — static requirement currently satisfied

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | **PASS** | formal netlist defines common GND for U1/U2/U3/U4/RX1/phasers/SK6812s |
| VAL-002 | MFRC522 voltage | **PASS** | U3 powered only from switched 3.3 V rail |
| VAL-003 | SK6812 logic level | **PASS** | one SN74AHCT1G125 at switched 5 V translates the single 3.3 V data line; U4 input arrangement is electrically appropriate |
| VAL-004 | XIAO boot straps | **BLOCKER — bench test** | final map uses D0/GPIO2=`NFC_MISO`, D8/GPIO8=`NFC_SCK`, D9/GPIO9=`SK_DATA_RAW`; D0 has R18 10 kΩ pull-up; repeated reset/power/deep-sleep cycles required with U3/U4 attached |
| VAL-005 | D6 boot chatter | **BLOCKER — combined with U3 backfeed test** | D6/GPIO21=`NFC_CS`; U3 is nominally off at reset, but an unpowered breakout can still be back-powered through an input. Do not call chatter harmless until measured |
| VAL-006 | wireless-present voltage | **BLOCKER — measure before connection** | R1=130 kΩ/R2=180 kΩ is valid around nominal 5 V but gives only limited margin above ~6 V; measure RX1 unloaded/loaded max voltage before attaching `WLC_PRESENT` to U1 |
| VAL-007 | wireless-present wake | **PASS assignment / bench test required** | `WLC_PRESENT` is on D1/GPIO3, a valid deep-sleep wake GPIO and not a strap pin |
| VAL-008 | pin budget | **PASS** | exactly 11 unique functions assigned to D0–D10; no GPIO expander needed |
| VAL-009 | MT3608 shutdown | **PASS architecture** | Q1/Q2 physically disconnect BAT+ from U2; MT3608 EN is not relied on for sleep isolation |
| VAL-010 | battery P-MOS gate drive | **PASS architecture** | AO3401A Q1 is source-referenced and controlled through Q2; no direct 3.3 V-high-to-4.2 V-source ambiguity |
| VAL-011 | power-on defaults | **PASS design / bench test required** | R3/R4/R10–R16 establish hardware default-OFF states; verify no reset flashes/rail glitches |
| VAL-012 | XIAO external 5 V path | **BLOCKER — bench test** | D1 isolation matches the external-source concept; verify actual XIAO run/charge/recovery behavior and reverse-current isolation |
| VAL-013 | Schottky polarity | **PASS** | D1 anode=`WLC_5V_RAW`, cathode/marked bar=`SYS_5V_IN` toward U1 |
| VAL-014 | phaser current limiting | **ERROR** | R6–R9 cannot be finalized until actual prewired 0805 resistor/Vf/current configuration is identified or measured |
| VAL-015 | logic-buffer bypass | **PASS design** | C1=0.1 µF ceramic assigned at U4 VCC/GND and must be physically local |
| VAL-016 | SK6812 bulk capacitance | **WARNING** | C2=470 µF target; validate after physical emitter count/load is known |
| VAL-017 | SK6812 chain topology | **PASS architecture** | exactly one serial data bus is frozen; physical emitter count/order remains a layout input |
| VAL-018 | RC522 power-off I/O | **BLOCKER — highest-priority bench test** | measure U3 OFF-state rail voltage/current and each SPI line. Verify no back-power, clamp, boot interference, or deep-sleep current penalty |
| VAL-019 | RC522 reset strategy | **BLOCKER — physical module check** | no MCU reset pin; switched-power reset/R17 must be verified on exact breakout |
| VAL-020 | MT3608 output capability | **BLOCKER — load/thermal test** | load-test actual U2 from realistic LiPo voltage at expected and worst-case lighting current |
| VAL-021 | XKT receiver capability | **BLOCKER — load/thermal test** | measure RX1 unloaded/loaded voltage, current, alignment sensitivity and heating; seller 5 V/2 A claim is not authoritative |
| VAL-022 | backfeed paths | **BLOCKER — integrated bench test** | validate no reverse feed into RX1, U2 output, powered-down U3, or other switched rails |
| VAL-023 | duplicate GPIO use | **PASS** | `PINOUT.md` assigns exactly one primary function to each D0–D10 |
| VAL-024 | OTA after sealing | **BLOCKER for final assembly** | Wi-Fi/BLE control and OTA must be proven repeatedly before hull closure |
| VAL-025 | GPIO2 pull-up | **PASS design / bench test required** | R18=10 kΩ pulls `NFC_MISO`/D0 high; verify exact U3 MISO does not clamp it or create excessive standby draw while U3 is off |
| VAL-026 | GPIO9 BOOT load | **BLOCKER — bench test** | D9 drives only U4 A input with no pull-down; verify repeated cold boot, reset, and deep-sleep wake behavior with U4 attached/unpowered |
| VAL-027 | battery protection | **BLOCKER — safety** | determine whether BT1 includes integral 1S protection. If not, U5 must be selected/fitted before final wiring |
| VAL-028 | battery discharge capability | **BLOCKER — load capability** | verify exact 103450 cell/pack can comfortably supply measured worst-case MT3608 input current, especially at low battery voltage |
| VAL-029 | Q1 carrier current path | **BLOCKER — physical carrier test** | Q1 carrier/source/drain copper carries full lighting-boost input current; generic breakout traces/pads must be inspected and load/thermal tested or reinforced |
| VAL-030 | D1 current/thermal margin | **WARNING / bench test** | PMEG2010ER is 1 A class, but actual proto-board copper and XIAO run+charge current determine temperature/drop |
| VAL-031 | SK6812 local decoupling | **BLOCKER until physical LED form confirmed** | if strip sections retain per-pixel bypass capacitors, PASS; if bare pixels lack local decoupling, add local ceramic bypass at each emitter |
| VAL-032 | SK6812 power envelope | **BLOCKER — measurement/firmware limit** | physical emitter count and per-emitter current must establish safe all-white/load limit and firmware maximum brightness/current envelope |
| VAL-033 | charging/NFC hard inhibit | **DECISION BLOCKER** | current Q9 forces NFC off whenever `WLC_PRESENT` is high. No user requirement currently proves this is desirable; explicit KEEP vs DNP decision required before final architecture release |
| VAL-034 | deep-sleep wake workflow | **DECISION BLOCKER** | current only normal wake source is wireless-power-present. Wi-Fi/BLE/NFC cannot wake a deep-sleeping ship. User must explicitly accept charging-field wake or request another wake strategy |
| VAL-035 | deep-sleep strap-cycle behavior | **BLOCKER — bench test** | verify repeated sleep->WLC wake cycles never sample GPIO9 low or otherwise enter wrong boot mode; do not rely on cold-boot tests alone |
| VAL-036 | final distribution implementation | **BLOCKER before drawing/harness release** | actual BAT+/GND/+5V/+3V3 bus/splice/protoboard implementation must be defined; any discrete distribution jumper receives a W-number |
| VAL-037 | carrier pad orientation | **BLOCKER before soldering** | continuity-check purchased SOT-23 and SOT-23-5 carrier pad numbering/orientation against actual device pin numbers; do not trust generic silkscreen |

## Static audit conclusion

**Core topology: CONDITIONAL PASS.** No static review found a catastrophic short, reversed high-side topology, duplicate GPIO, wrong MFRC522 voltage domain, or incompatible SK6812 level-shift concept.

**Drawing release: DENIED.** The current design is not yet ready for final schematic/CAD release because physical/module/load facts remain unverified and VAL-033/VAL-034 require explicit user decisions.

Detailed reasoning is preserved in `STEP9-AUDIT.md`.

## Required physical validation sequence

Before schematic release, complete in this order:

1. identify BT1 protection and discharge specification;
2. identify/measure RX1 before connecting `WLC_PRESENT` to U1;
3. verify D1 external-input charging/recovery path;
4. build/test Q1/Q2 + U2 with a dummy/representative load and inspect Q1 carrier heating/drop;
5. identify one phaser LED and close R6–R9;
6. identify U3 breakout, then test OFF-state SPI/backfeed/boot/deep-sleep current;
7. confirm SK6812 form/count/local decoupling and measure lighting load;
8. run repeated boot/reset/deep-sleep wake cycles;
9. define physical distribution nodes/harness additions;
10. run integrated Wi-Fi/BLE/NFC/lighting/OTA/thermal tests before closure.
