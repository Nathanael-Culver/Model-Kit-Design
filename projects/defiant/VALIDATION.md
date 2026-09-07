# USS Defiant — Electrical Validation Register

**Document status:** ACTIVE — updated through Step 6  
**Release rule:** no final schematic/CAD release while any `ERROR` remains or any hardware-critical `BLOCKER` is untested.

Severity:

- `ERROR` — electrically invalid/unsafe until resolved
- `BLOCKER` — design choice is defined but requires physical proof before release
- `WARNING` — acceptable only with stated test/mitigation
- `PASS` — design requirement currently satisfied

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | **PASS** | formal netlist defines common GND for U1/U2/U3/U4/RX1/phasers/SK6812s |
| VAL-002 | MFRC522 voltage | **PASS** | U3 powered only from switched 3.3 V rail |
| VAL-003 | SK6812 logic level | **PASS** | one SN74AHCT1G125 at switched 5 V translates the single 3.3 V SK data line |
| VAL-004 | XIAO boot straps | **BLOCKER — bench test** | final map uses D0/GPIO2=`NFC_MISO`, D8/GPIO8=`NFC_SCK`, D9/GPIO9=`SK_DATA_RAW`; D0 gets R18 10 kΩ pull-up; repeated reset/power-cycle tests required with U3/U4 physically connected |
| VAL-005 | D6 boot chatter | **PASS by architecture / test required** | D6/GPIO21=`NFC_CS`; U3 is physically off during reset so UART boot chatter cannot operate NFC |
| VAL-006 | wireless-present voltage | **WARNING — measured RX1 voltage required** | R1=130 kΩ/R2=180 kΩ gives ~2.90 V from nominal 5.0 V; safe only if actual RX1 loaded/unloaded voltage stays within validated range |
| VAL-007 | wireless-present wake | **PASS assignment / bench test required** | `WLC_PRESENT` frozen to D1/GPIO3, a wake-capable non-strapping XIAO pin |
| VAL-008 | pin budget | **PASS** | exactly 11 unique functions assigned to D0–D10; no GPIO expander required and no spare GPIO remains |
| VAL-009 | MT3608 shutdown | **PASS architecture** | Q1/Q2 physically disconnect BAT+ from U2; design no longer relies on MT3608 EN for sleep isolation |
| VAL-010 | battery P-MOS gate drive | **PASS architecture** | AO3401A Q1 is driven through AO3400A Q2 helper; MCU does not directly attempt to drive battery-domain P-MOS gate HIGH |
| VAL-011 | power-on defaults | **PASS design / bench test required** | R3/R4/R10–R16 establish hardware default-off states for lighting/NFC/phasers |
| VAL-012 | XIAO external 5 V path | **BLOCKER — bench test** | D1 isolation path is formally defined; verify actual wireless charging/recovery and absence of reverse feed |
| VAL-013 | Schottky polarity | **PASS** | D1 anode=`WLC_5V_RAW`, cathode/marked bar=`SYS_5V_IN` toward U1 |
| VAL-014 | phaser current limiting | **ERROR** | R6–R9 cannot be finalized until exact prewired 0805 LED resistor/Vf/current configuration is identified or measured |
| VAL-015 | logic-buffer bypass | **PASS design** | C1=0.1 µF ceramic assigned at U4 VCC/GND; physical placement must be local |
| VAL-016 | SK6812 bulk capacitance | **WARNING** | C2=470 µF target; revalidate after physical emitter count/load is known |
| VAL-017 | SK6812 chain topology | **PASS architecture** | exactly one serial data bus is frozen; physical emitter count/order remains mechanical-layout input |
| VAL-018 | RC522 power-off I/O | **BLOCKER — bench test** | confirm exact U3 breakout does not clamp/backfeed D0/D8/D10/D6 while unpowered; D0 boot margin especially critical |
| VAL-019 | RC522 reset strategy | **WARNING — physical module check** | no MCU reset pin; R17/switched-power reset method must be verified on exact breakout |
| VAL-020 | MT3608 output capability | **WARNING** | load-test complete U2 from battery voltage at representative SK6812/phaser load; module '2 A' marketing is not assumed |
| VAL-021 | XKT receiver capability | **WARNING** | measure RX1 output under realistic coil alignment/load; seller 5 V/2 A claim not assumed |
| VAL-022 | backfeed paths | **BLOCKER — integrated bench test** | validate no reverse feed into RX1, U2 output, powered-down U3, or U4 through signals/power paths |
| VAL-023 | duplicate GPIO use | **PASS** | `PINOUT.md` FROZEN v1.0 assigns exactly one primary function to each D0–D10 |
| VAL-024 | OTA after sealing | **BLOCKER for final assembly** | Wi-Fi/BLE control and OTA must be proven repeatedly before hull closure |
| VAL-025 | GPIO2 pull-up | **PASS design / bench test required** | R18=10 kΩ pulls `NFC_MISO`/D0 to +3V3_ALWAYS; verify exact U3 MISO does not overpower this while U3 is off |
| VAL-026 | GPIO9 BOOT load | **BLOCKER — bench test** | D9 drives only U4 A input with no external pull-down; verify normal boot with U4 unpowered through repeated resets |

## Required final validation pass

Before schematic release, verify:

1. repeated normal boot with all external circuits attached;
2. D1/GPIO3 deep-sleep wake from wireless power;
3. no powered-down peripheral backfeed;
4. default-off lighting/NFC/phaser states;
5. RX1 voltage/current and D1 charging path;
6. U2 5 V regulation/thermal margin under representative load;
7. actual phaser LED current limiting;
8. exact U3 header/reset behavior;
9. battery protection status;
10. physical SK6812 count/load and C2 adequacy;
11. OTA before sealing;
12. every component pin/net/wire endpoint accounted for.
