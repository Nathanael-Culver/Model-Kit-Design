# USS Defiant — Electrical Validation Register

**Document status:** **STEP 9 STATIC AUDIT COMPLETE / POLICY DECISIONS CLOSED / PHYSICAL VALIDATION ACTIVE**  
**Release rule:** no final schematic/CAD release while any hardware-critical `BLOCKER` required for drawing correctness is untested.

Severity:

- `ERROR` — electrically invalid/unsafe until resolved
- `BLOCKER` — must be physically proven before release
- `WARNING` — acceptable only with stated test/mitigation
- `PASS` — static requirement/policy currently satisfied

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | **PASS** | common GND defined for all active subsystems |
| VAL-002 | RC522 voltage | **PASS** | compact reader candidates are 3.3 V SPI devices; U3 remains on switched 3.3 V |
| VAL-003 | SK6812 logic level | **PASS** | U4 AHCT buffer provides proper 3.3 V -> 5 V data translation |
| VAL-004 | XIAO boot straps | **BLOCKER — bench test** | D0/GPIO2=NFC_MISO, D8/GPIO8=NFC_SCK, D9/GPIO9=SK_DATA_RAW; repeated boot/sleep-wake testing required with selected U3/U4 attached |
| VAL-005 | D6 boot chatter | **BLOCKER — combined U3 test** | D6/GPIO21=NFC_CS; prove selected compact U3 remains truly unpowered/not back-fed at reset |
| VAL-006 | wireless-present voltage | **BLOCKER — measure before connection** | R1/R2 divider is valid near nominal 5 V but RX1 max must be measured before attaching to U1 |
| VAL-007 | wireless-present wake | **PASS assignment / bench test required** | D1/GPIO3 is suitable wake pin; actual wake test still required |
| VAL-008 | pin budget | **PASS** | 11 unique functions on 11 exposed GPIOs; no expander |
| VAL-009 | MT3608 shutdown | **PASS architecture + board ID** | actual U2 has no visible exposed EN pad; Q1/Q2 battery-side disconnect remains the correct implementation |
| VAL-010 | battery P-MOS gate drive | **PASS architecture** | Q1 is controlled through source-referenced Q2 helper |
| VAL-011 | power-on defaults | **PASS design / bench test required** | R3/R4/R10–R16 establish default-OFF states |
| VAL-012 | XIAO external 5 V path | **BLOCKER — bench test** | verify D1 charging/recovery and no reverse feed |
| VAL-013 | Schottky polarity | **PASS** | D1 anode=WLC_5V_RAW, cathode=SYS_5V_IN |
| VAL-014 | phaser current limiting | **PASS design / one-sample check remains** | exact DiCUNO white 0805 stock identified: 2.8–3.3 V, 20 mA. R6–R9 fixed at **150 Ω >=1/8 W**, giving about 11–15 mA from 5.0 V. Verify polarity/operation on one sample before duplicating channels |
| VAL-015 | logic-buffer bypass | **PASS design** | C1=0.1 µF local at U4 |
| VAL-016 | SK6812 bulk capacitance | **WARNING** | C2=470 µF target; validate after physical emitter count/load known |
| VAL-017 | SK6812 chain topology | **PASS architecture** | exact BTF-LIGHTING SK6812 RGBW Natural White 5 V 144 LED/m strip confirmed; one serial data bus remains frozen |
| VAL-018 | compact RC522 power-off I/O | **BLOCKER — highest-priority bench test** | black XFW-ETLIVE V602 and green RC522 MINI V1.1 are viable; compare unpowered backfeed/clamp/deep-sleep current before selecting U3 |
| VAL-019 | RC522 reset strategy | **BLOCKER — bench selection test** | both compact boards expose RST; verify switched-power reset and determine whether R17 is required |
| VAL-020 | MT3608 output capability | **BLOCKER — load/thermal test** | actual board/pads identified; load-test at realistic LiPo voltages |
| VAL-021 | XKT receiver capability | **BLOCKER — load/thermal test** | measure RX1 voltage/current/alignment/heating |
| VAL-022 | backfeed paths | **BLOCKER — integrated bench test** | verify no reverse feed into RX1, U2, selected U3, or switched rails |
| VAL-023 | duplicate GPIO use | **PASS** | one primary function per D0–D10 |
| VAL-024 | OTA after sealing | **BLOCKER for final assembly** | prove Wi-Fi/BLE control and OTA repeatedly before closure |
| VAL-025 | GPIO2 pull-up | **PASS design / bench test required** | R18=10 kΩ; verify selected compact U3 MISO does not clamp it while U3 off |
| VAL-026 | GPIO9 BOOT load | **BLOCKER — bench test** | verify repeated cold boot/reset/deep-sleep wake with U4 attached/off |
| VAL-027 | battery protection | **BLOCKER — safety** | BT1 label/spec confirmed; photo is consistent with end-mounted protection PCB but does not prove it. Close with better edge photo or seller documentation; fit U5 if unprotected |
| VAL-028 | battery discharge capability | **BLOCKER — load capability** | verify pack can supply worst-case MT3608 input current |
| VAL-029 | Q1 carrier current path | **BLOCKER — physical carrier test** | inspect/load-test/reinforce carrier current path if needed |
| VAL-030 | D1 current/thermal margin | **WARNING / bench test** | verify actual drop/temperature with run+charge current |
| VAL-031 | SK6812 local decoupling/form | **PASS form / assembly rule** | exact BTF strip shown with per-section SMD support components; retain complete manufacturer-defined pixel sections when cutting. Final installed sections still continuity-check before closure |
| VAL-032 | SK6812 power envelope | **BLOCKER — measurement/firmware limit** | physical emitter count remains open; establish load and firmware brightness/current cap |
| VAL-033 | charging/NFC hard inhibit policy | **PASS — USER APPROVED DNP** | Q9 DNP; NFC allowed while charging |
| VAL-034 | deep-sleep wake workflow | **PASS — USER APPROVED** | normal v1 wake is applying/enabling wireless charging |
| VAL-035 | deep-sleep strap-cycle behavior | **BLOCKER — bench test** | verify repeated sleep->WLC wake never enters wrong boot mode |
| VAL-036 | final distribution implementation | **BLOCKER before drawing/harness release** | define actual BAT+/GND/+5V/+3V3 bus/splice/protoboard layout and new W-numbers |
| VAL-037 | carrier pad orientation | **BLOCKER before soldering** | continuity-check SOT-23/SOT-23-5 carrier pad numbering/orientation |
| VAL-038 | NFC while charging coexistence | **BLOCKER — integrated functional test** | selected compact reader must read reliably while XKT charging is active; mitigate only if measured interference is unacceptable |
| VAL-039 | compact-reader selection | **BLOCKER — mechanical/bench choice** | large blue standard RC522 is disfavored. Black XFW-ETLIVE V602 is primary candidate; green RC522 MINI V1.1 is alternate. Select by actual hull fit, read range, reset, backfeed and coexistence results |

## Current validation conclusion

**No unresolved static electrical ERROR remains.** The phaser current-limit error is now closed with verified product data and 150 Ω resistors.

**Drawing release remains DENIED** because the remaining items are physical/load/fit facts that affect final assembly correctness.

## Highest-value next tests

1. better evidence for BT1 protection status;
2. photograph/measure RX1 and test raw output before connection to U1;
3. test one 150 Ω phaser channel;
4. compare the black and green compact RC522 boards on the bench for read range, reset and unpowered backfeed;
5. decide actual SK6812 emitter count/order in the hull;
6. load-test U2/Q1/battery path;
7. run boot/sleep-wake and charging/NFC coexistence tests.
