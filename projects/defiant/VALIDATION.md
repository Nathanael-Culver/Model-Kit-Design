# USS Defiant — Electrical Validation Register

**Document status:** **STEP 9 STATIC AUDIT COMPLETE / POLICY DECISIONS CLOSED / PHYSICAL VALIDATION PENDING**  
**Release rule:** no final schematic/CAD release while any `ERROR` remains or any hardware-critical `BLOCKER` is untested.

Severity:

- `ERROR` — electrically invalid/unsafe until resolved
- `BLOCKER` — must be physically proven before release
- `WARNING` — acceptable only with stated test/mitigation
- `PASS` — static requirement/policy currently satisfied

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | **PASS** | common GND defined for all active subsystems |
| VAL-002 | MFRC522 voltage | **PASS** | U3 powered only from switched 3.3 V |
| VAL-003 | SK6812 logic level | **PASS** | U4 AHCT buffer provides proper 3.3 V -> 5 V data translation |
| VAL-004 | XIAO boot straps | **BLOCKER — bench test** | D0/GPIO2=NFC_MISO, D8/GPIO8=NFC_SCK, D9/GPIO9=SK_DATA_RAW; repeated boot/sleep-wake testing required with U3/U4 attached |
| VAL-005 | D6 boot chatter | **BLOCKER — combined U3 test** | D6/GPIO21=NFC_CS; prove U3 remains truly unpowered/not back-fed at reset |
| VAL-006 | wireless-present voltage | **BLOCKER — measure before connection** | R1/R2 divider is valid near nominal 5 V but RX1 max must be measured before attaching to U1 |
| VAL-007 | wireless-present wake | **PASS assignment / bench test required** | D1/GPIO3 is suitable wake pin; actual wake test still required |
| VAL-008 | pin budget | **PASS** | 11 unique functions on 11 exposed GPIOs; no expander |
| VAL-009 | MT3608 shutdown | **PASS architecture** | Q1/Q2 physically disconnect BAT+ from U2 |
| VAL-010 | battery P-MOS gate drive | **PASS architecture** | Q1 is controlled through source-referenced Q2 helper |
| VAL-011 | power-on defaults | **PASS design / bench test required** | R3/R4/R10–R16 establish default-OFF states |
| VAL-012 | XIAO external 5 V path | **BLOCKER — bench test** | verify D1 charging/recovery and no reverse feed |
| VAL-013 | Schottky polarity | **PASS** | D1 anode=WLC_5V_RAW, cathode=SYS_5V_IN |
| VAL-014 | phaser current limiting | **ERROR** | R6–R9 cannot be finalized until actual prewired LED resistor/Vf/current configuration is known |
| VAL-015 | logic-buffer bypass | **PASS design** | C1=0.1 µF local at U4 |
| VAL-016 | SK6812 bulk capacitance | **WARNING** | C2=470 µF target; validate after physical emitter count/load known |
| VAL-017 | SK6812 chain topology | **PASS architecture** | one serial data bus; physical emitter count/order remains layout input |
| VAL-018 | RC522 power-off I/O | **BLOCKER — highest-priority bench test** | prove no U3 back-power/clamp/boot/deep-sleep-current issue while rail is OFF |
| VAL-019 | RC522 reset strategy | **BLOCKER — physical module check** | verify switched-power reset/R17 on exact breakout |
| VAL-020 | MT3608 output capability | **BLOCKER — load/thermal test** | load-test actual U2 at realistic LiPo voltages |
| VAL-021 | XKT receiver capability | **BLOCKER — load/thermal test** | measure RX1 voltage/current/alignment/heating |
| VAL-022 | backfeed paths | **BLOCKER — integrated bench test** | verify no reverse feed into RX1, U2, U3, or switched rails |
| VAL-023 | duplicate GPIO use | **PASS** | one primary function per D0–D10 |
| VAL-024 | OTA after sealing | **BLOCKER for final assembly** | prove Wi-Fi/BLE control and OTA repeatedly before closure |
| VAL-025 | GPIO2 pull-up | **PASS design / bench test required** | R18=10 kΩ; verify exact U3 MISO does not clamp it while U3 off |
| VAL-026 | GPIO9 BOOT load | **BLOCKER — bench test** | verify repeated cold boot/reset/deep-sleep wake with U4 attached/off |
| VAL-027 | battery protection | **BLOCKER — safety** | determine whether BT1 has integral 1S protection; fit U5 if not |
| VAL-028 | battery discharge capability | **BLOCKER — load capability** | verify pack can supply worst-case MT3608 input current |
| VAL-029 | Q1 carrier current path | **BLOCKER — physical carrier test** | inspect/load-test/reinforce carrier current path if needed |
| VAL-030 | D1 current/thermal margin | **WARNING / bench test** | verify actual drop/temperature with run+charge current |
| VAL-031 | SK6812 local decoupling | **BLOCKER until LED form confirmed** | confirm strip sections retain local bypass or add local ceramic caps |
| VAL-032 | SK6812 power envelope | **BLOCKER — measurement/firmware limit** | establish physical load and firmware brightness/current cap |
| VAL-033 | charging/NFC hard inhibit policy | **PASS — USER APPROVED DNP** | Q9 is DNP; NFC is allowed while charging; W013/W053 DNP |
| VAL-034 | deep-sleep wake workflow | **PASS — USER APPROVED** | normal v1 wake is applying/enabling wireless charging; Wi-Fi/BLE/NFC do not wake deep sleep |
| VAL-035 | deep-sleep strap-cycle behavior | **BLOCKER — bench test** | verify repeated sleep->WLC wake never enters wrong boot mode |
| VAL-036 | final distribution implementation | **BLOCKER before drawing/harness release** | define actual BAT+/GND/+5V/+3V3 bus/splice/protoboard layout and new W-numbers |
| VAL-037 | carrier pad orientation | **BLOCKER before soldering** | continuity-check SOT-23/SOT-23-5 carrier pad numbering/orientation |
| VAL-038 | NFC while charging coexistence | **BLOCKER — integrated functional test** | with Q9 DNP, test MFRC522 read range/reliability while XKT charging is active; mitigate only if measured interference is unacceptable |

## Static audit conclusion

**Core topology: CONDITIONAL PASS.** The two Step-9 policy decisions are now closed and incorporated consistently: Q9 is DNP, and wireless charging presence is the normal deep-sleep wake method.

**Drawing release: still DENIED.** The remaining blockers are physical/electrical verification, not unresolved architecture policy.

## Required physical validation sequence

1. identify BT1 protection/discharge capability;
2. measure RX1 before attaching `WLC_PRESENT` to U1;
3. verify D1 charging/recovery/reverse isolation;
4. test Q1/Q2 + U2 with representative load and carrier heating/drop;
5. identify one phaser LED and close R6–R9;
6. identify U3 and test OFF-state SPI/backfeed/boot/deep-sleep current;
7. confirm SK6812 form/count/decoupling and lighting load;
8. run repeated cold-boot/reset/deep-sleep -> WLC wake cycles;
9. test NFC reads with wireless charging active;
10. define physical distribution nodes/harness additions;
11. run integrated Wi-Fi/BLE/NFC/lighting/OTA/thermal tests before closure.