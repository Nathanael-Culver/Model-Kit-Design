# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 9b — bench / physical validation**  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | COMPLETE enough to proceed |
| 2. Identify part numbers/packages/carriers | **MAJOR PART IDENTIFICATION CLOSED; only BT1 protection proof remains** |
| 3. Freeze electrical architecture | FROZEN v1.1 |
| 4. Freeze reference designators | **FROZEN v1.5** |
| 5. Formal netlist | FORMAL v1.4; update after RX1 electrical characterization if needed |
| 6. XIAO pin map | FROZEN v1.0 |
| 7. Master wire list | FORMAL v1.1; W001–W053 reserved, W013/W053 DNP |
| 8. Per-module pin tables | FORMAL v1.3; RX1 polarity stays meter-verified before release |
| 9. Static electrical validation | COMPLETE — CONDITIONAL PASS |
| 9a. Architecture-policy decisions | COMPLETE / APPROVED |
| 9b. Bench / physical validation | **ACTIVE** |
| 10+. Final drawings/layout/closure validation | gated |

## Confirmed hardware

- **BT1:** 103450 / 3.7 V / 2500 mAh / 9.25 Wh. Protection likely but not proven.
- **TX1:** **XKT-412 transmitter board + flat spiral coil**; `IN+`/`IN-` supply end and `OUT` coil end physically visible.
- **RX1:** **XKT-3168 receiver board + flat spiral coil**; IC marking physically confirmed. Factory red/black DC output leads visible; polarity and voltage still meter-verify before connection.
- **U2:** photographed MT3608 board with `VIN+`, `VIN-`, `VOUT+`, `VOUT-`; no exposed EN pad visible.
- **U3:** black XFW-ETLIVE V602 compact 3.3 V SPI RC522-class reader — USER SELECTED / FROZEN.
- **Phasers:** DiCUNO prewired white 0805 LEDs, 2.8–3.3 V / 20 mA. R6–R9 = **150 Ω >=1/8 W**.
- **Addressable LEDs:** BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, black IP30 strip. Physical emitter count/order remains open.

## Important validation result

**There are no unresolved static electrical ERROR items.** Major module identification is now essentially complete.

The drawing gate remains closed because final electrical/load/fit facts still need proof.

## Remaining blockers before drawing release

1. prove BT1 protection status and discharge capability;
2. **characterize RX1:** meter-confirm polarity, unloaded/max voltage, loaded voltage/current, alignment sensitivity and heating;
3. verify D1 charging/recovery/reverse-current/thermal behavior;
4. load-test U2 and Q1 carrier from realistic battery voltage;
5. bench-test V602 U3 reset, read range and unpowered-SPI/backfeed behavior;
6. verify D0/D8 boot safety with V602 attached/off and D9 boot safety with U4 attached/off;
7. choose physical SK6812 emitter count/order and measure lighting load;
8. repeated strap-pin boot/reset/deep-sleep -> WLC wake tests;
9. test V602 NFC while wireless charging is active;
10. define final BAT+/GND/+5V/+3V3 physical distribution and resulting W-numbers;
11. carrier pad-orientation continuity check;
12. OTA/control/integrated thermal testing before hull closure.

## Immediate next physical test

**Measure RX1 now, with nothing connected to its DC output.** TX1 can be powered and the coils coupled, but RX1 must remain isolated from U1/D1/R1/R2 for this measurement.

Record:

- red-to-black DC voltage at best alignment;
- highest voltage seen while moving/separating/misaligning coils;
- whether polarity is red-positive / black-negative;
- approximate coil spacing at the best/expected final position.

`VALIDATION.md` is authoritative for blocker status.
