# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** Step 7 — master wire list  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** |
| 3. Freeze electrical architecture | **COMPLETE — FROZEN v1.0** |
| 4. Freeze reference designators | **COMPLETE — FROZEN v1.1** |
| 5. Formal netlist | **COMPLETE enough to proceed — FORMAL v1.1** |
| 6. XIAO pin map | **COMPLETE — FROZEN v1.0** |
| 7. Master wire list | **NEXT** |
| 8. Per-module pin tables | partial; update after Step 7 |
| 9. Validation | active; bench blockers remain |
| 10+. Drawings/layout/firmware | gated |

## Frozen XIAO assignment

| XIAO pin | GPIO | Signal |
|---|---:|---|
| D0 | GPIO2 | `NFC_MISO` |
| D1 | GPIO3 | `WLC_PRESENT` |
| D2 | GPIO4 | `PH0_GATE` |
| D3 | GPIO5 | `PH1_GATE` |
| D4 | GPIO6 | `PH2_GATE` |
| D5 | GPIO7 | `PH3_GATE` |
| D6 | GPIO21 | `NFC_CS` |
| D7 | GPIO20 | `PERIPH_EN` |
| D8 | GPIO8 | `NFC_SCK` |
| D9 | GPIO9 | `SK_DATA_RAW` |
| D10 | GPIO10 | `NFC_MOSI` |

Step 6 added `R18 = 10 kΩ` from D0/GPIO2 (`NFC_MISO`) to `+3V3_ALWAYS` to preserve the recommended GPIO2 boot-high bias.

## Frozen architecture summary

- U1 XIAO stays permanently connected to BT1.
- RX1 feeds U1 charging/recovery through D1 and provides `WLC_PRESENT` wake.
- Q1/Q2 physically disconnect U2/5 V lighting from battery in sleep.
- One SK6812 serial bus uses U4 SN74AHCT1G125 level translation.
- Q3–Q6 independently switch the four pulse-phaser LEDs.
- Q7/Q8/Q9 control and inhibit the switched MFRC522 3.3 V rail.
- NFC cannot operate while wireless charging is present.
- No GPIO expander, touch module, audio, second SK bus, reed wake, or NTC monitoring.

## Remaining physical blockers before drawing release

1. BT1 protection status.
2. RX1 exact pads and measured output/current.
3. U2 exact module/pads and load-tested 5 V output.
4. U3 exact module/header/reset behavior and unpowered-I/O behavior.
5. Prewired phaser LED current/resistor configuration.
6. Physical SK6812 emitter count/order.
7. Repeated boot tests for D0/GPIO2, D8/GPIO8 and especially D9/GPIO9 with peripherals attached.
8. D1/GPIO3 wireless wake test.
9. Backfeed/default-off tests.
10. OTA/control tests before closure.

`VALIDATION.md` remains authoritative for blocker severity.

## Drawing release criteria

The drawing gate opens only when:

- architecture/designators/pinout remain frozen;
- `NETLIST.md` is drawing-approved;
- `CONNECTIONS.md` defines every component pin;
- `WIRE-LIST.md` covers every applicable off-board connection;
- `VALIDATION.md` has no unresolved ERROR and no unaccepted hardware-critical blocker.
