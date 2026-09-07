# USS Defiant — Electrical Validation Register

**Document status:** **STATIC AUDIT COMPLETE / PHYSICAL DESIGN ADVANCING / BENCH VALIDATION STILL REQUIRED BEFORE RELEASE**  
**Release rule:** no final schematic/CAD release while any hardware-critical `BLOCKER` required for drawing correctness remains unresolved.

Severity:

- `ERROR` — electrically invalid/unsafe until resolved
- `BLOCKER` — must be physically proven before release
- `WARNING` — acceptable only with stated test/mitigation
- `PASS` — static requirement/policy currently satisfied

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | **PASS** | common GND defined for all active subsystems |
| VAL-002 | NFC reader voltage | **PASS** | U3 V602 is 3.3 V SPI and remains on switched 3.3 V |
| VAL-003 | SK6812 logic level | **PASS** | U4 AHCT buffer provides 3.3 V -> 5 V data translation |
| VAL-004 | XIAO boot straps | **BLOCKER — bench test** | D0/GPIO2=NFC_MISO, D8/GPIO8=NFC_SCK, D9/GPIO9=SK_DATA_RAW; repeated boot/sleep-wake test with U3/U4 attached |
| VAL-005 | D6 boot chatter | **BLOCKER — combined U3 test** | D6/GPIO21=NFC_CS; prove V602 is unpowered/not back-fed at reset |
| VAL-006 | wireless-present voltage | **BLOCKER — integrated bench acceptance** | XKT pair is selected 5 V/2 A hardware; confirm actual RX1 polarity/voltage before first permanent connection to U1 sense/charge path |
| VAL-007 | wireless-present wake | **PASS assignment / bench test required** | D1/GPIO3 is the defined wake pin |
| VAL-008 | pin budget | **PASS** | 11 unique functions on 11 exposed GPIOs; no expander |
| VAL-009 | MT3608 shutdown | **PASS architecture + board ID** | U2 has no exposed EN; Q1/Q2 battery-side disconnect remains correct |
| VAL-010 | battery P-MOS gate drive | **PASS architecture** | Q1 controlled through source-referenced Q2 helper |
| VAL-011 | power-on defaults | **PASS design / bench test required** | R3/R4/R10–R16 establish default-OFF states |
| VAL-012 | XIAO external 5 V path | **BLOCKER — integrated bench test** | verify D1 charging/recovery and no reverse feed |
| VAL-013 | Schottky polarity | **PASS** | D1 anode=WLC_5V_RAW, cathode=SYS_5V_IN |
| VAL-014 | phaser current limiting | **PASS design / one-sample check remains** | R6–R9 = 150 Ω >=1/8 W for DiCUNO white LEDs |
| VAL-015 | logic-buffer bypass | **PASS design** | C1=0.1 µF local at U4 |
| VAL-016 | SK6812 bulk capacitance | **WARNING** | C2=470 µF target; validate rail behavior with all 14 pixels |
| VAL-017 | SK6812 chain topology | **PASS — FROZEN** | one serial bus, exact stock confirmed |
| VAL-018 | V602 power-off I/O | **BLOCKER — bench test** | measure unpowered backfeed/clamp/deep-sleep current on SPI and switched 3V3 rail |
| VAL-019 | V602 reset strategy | **BLOCKER — bench test** | verify switched-power reset and whether R17 is required |
| VAL-020 | MT3608 output capability | **BLOCKER — load/thermal test** | load-test at realistic LiPo voltages with final lighting load |
| VAL-021 | XKT receiver capability | **BLOCKER — integrated acceptance** | RX1=XKT-3168 and TX1=XKT-412 are physically identified; load/alignment/heating test remains before closure, not before continuing design |
| VAL-022 | backfeed paths | **BLOCKER — integrated bench test** | verify no reverse feed into RX1, U2, V602, or switched rails |
| VAL-023 | duplicate GPIO use | **PASS** | one primary function per D0–D10 |
| VAL-024 | OTA after sealing | **BLOCKER for final assembly** | prove Wi-Fi/BLE control and OTA repeatedly before closure |
| VAL-025 | GPIO2 pull-up | **PASS design / bench test required** | R18=10 kΩ; verify V602 MISO does not clamp it while U3 off |
| VAL-026 | GPIO9 BOOT load | **BLOCKER — bench test** | verify repeated cold boot/reset/deep-sleep wake with U4 attached/off |
| VAL-027 | battery protection | **BLOCKER — safety** | BT1 appears likely protected but proof remains required; fit U5 if unprotected |
| VAL-028 | battery discharge capability | **BLOCKER — load capability** | verify pack can supply final MT3608 input current |
| VAL-029 | Q1 carrier current path | **BLOCKER — physical carrier test** | inspect/load-test/reinforce carrier current path if needed |
| VAL-030 | D1 current/thermal margin | **WARNING / bench test** | verify actual drop/temperature during run+charge |
| VAL-031 | SK6812 local decoupling/form | **PASS form / assembly rule** | retain complete cuttable pixel sections and local SMD support parts |
| VAL-032 | SK6812 power envelope | **BLOCKER — measured load/firmware cap** | count is now fixed at 14; establish measured load and safe firmware brightness/current cap |
| VAL-033 | charging/NFC hard inhibit policy | **PASS — USER APPROVED DNP** | Q9 DNP; NFC allowed while charging |
| VAL-034 | deep-sleep wake workflow | **PASS — USER APPROVED** | normal v1 wake is applying/enabling wireless charging |
| VAL-035 | deep-sleep strap-cycle behavior | **BLOCKER — bench test** | verify repeated sleep->WLC wake never enters wrong boot mode |
| VAL-036 | final distribution implementation | **BLOCKER before drawing/harness release** | define actual BAT+/GND/+5V/+3V3 bus/splice/protoboard layout and new W-numbers |
| VAL-037 | carrier pad orientation | **BLOCKER before soldering** | continuity-check SOT-23/SOT-23-5 carrier pad numbering/orientation |
| VAL-038 | NFC while charging coexistence | **BLOCKER — integrated functional test** | V602 must read reliably while XKT charging is active |
| VAL-039 | compact-reader selection | **PASS** | black XFW-ETLIVE V602 frozen as U3 |
| VAL-040 | wireless module identity | **PASS** | TX1=XKT-412; RX1=XKT-3168 physically identified |
| VAL-041 | physical SK6812 count/order | **PASS — FROZEN** | LED14–LED27 = 14 pixels; chain and P0–P8 membership frozen in `LIGHTING-LAYOUT.md` |
| VAL-042 | inter-emitter data harness | **PASS design** | W054–W066 define all 13 data links; LED27 DOUT NC |
| VAL-043 | pixel power distribution | **BLOCKER — mechanical layout** | choose parallel +5V/GND trunk/branch geometry after exact hull placement; do not force all current through serial strip copper |

## Current validation conclusion

**No unresolved static electrical ERROR remains.** The physical SK6812 count and data order are now closed.

**Drawing release remains DENIED** because power distribution, exact physical placement, battery protection, carrier details, and integrated electrical tests still affect final assembly correctness.

## Next engineering work

Without requiring immediate bench testing, continue with:

1. final physical component-placement plan inside the hull;
2. +5V/GND/BAT+/3V3 distribution strategy and W067+ assignments;
3. wire-gauge strategy by current class;
4. exact harness lengths after ruler measurements of the hull;
5. only then integrated bench validation of XKT, U2/Q1, U3, boot/wake, lighting load, OTA, and thermal behavior.
