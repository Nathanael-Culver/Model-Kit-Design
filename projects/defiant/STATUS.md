# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 9b — bench / physical validation**  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | COMPLETE enough to proceed |
| 2. Identify part numbers/packages/carriers | **MAJOR PART IDENTIFICATION CLOSED; remaining RX1/TX1 + BT1 protection proof** |
| 3. Freeze electrical architecture | FROZEN v1.1 |
| 4. Freeze reference designators | **FROZEN v1.3** |
| 5. Formal netlist | **FORMAL v1.3** |
| 6. XIAO pin map | FROZEN v1.0 |
| 7. Master wire list | FORMAL v1.1; W001–W053 reserved, W013/W053 DNP |
| 8. Per-module pin tables | **FORMAL v1.2** |
| 9. Static electrical validation | COMPLETE — CONDITIONAL PASS |
| 9a. Architecture-policy decisions | COMPLETE / APPROVED |
| 9b. Bench / physical validation | **ACTIVE** |
| 10+. Final drawings/layout/closure validation | gated |

## Newly confirmed from current hardware/product photos

- **BT1:** exact 103450 / 3.7 V / 2500 mAh / 9.25 Wh pack confirmed. Lead-end construction looks consistent with a protection PCB, but protection is not yet proven.
- **U2:** exact small adjustable MT3608 board form confirmed. Pads are visibly `VIN+`, `VIN-`, `VOUT+`, `VOUT-`; no external EN pad is visible. Frozen Q1/Q2 input gating remains correct.
- **Phasers:** exact DiCUNO prewired white 0805 LEDs confirmed: 2.8–3.3 V, 20 mA, 240–280 mcd, 120°, 6.3 in leads. **R6–R9 are now 150 Ω >=1/8 W.**
- **Addressable LEDs:** exact BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, black IP30 strip confirmed. Physical emitter count/order remains open.
- **NFC/RFID:** large blue standard RC522 is mechanically disfavored. Two compact 3.3 V SPI readers are viable:
  - black XFW-ETLIVE V602 — primary candidate, 8-pin SDA/SCK/MOSI/MISO/IRQ/GND/RST/3V3;
  - green RC522 MINI V1.1-style — alternate, 7-pin NSS/SCK/MOSI/MISO/RST/GND/3.3V.
  Final compact-board selection will be based on hull fit, read range, reset behavior, unpowered-SPI backfeed, and charging coexistence.

## Important validation result

**There are now no unresolved static electrical ERROR items.** The previous phaser-current-limit ERROR is closed.

The drawing gate remains closed because final physical/load/fit facts are still required.

## Remaining blockers before drawing release

1. prove BT1 protection status and discharge capability;
2. identify/measure RX1 output pads, voltage/current/alignment/heating;
3. verify D1 charging/recovery/reverse-current/thermal behavior;
4. load-test U2 and Q1 carrier from realistic battery voltage;
5. compare black vs green compact RC522 and select U3;
6. verify selected U3 reset and unpowered-SPI/backfeed/boot behavior;
7. choose physical SK6812 emitter count/order and measure lighting load;
8. repeated strap-pin boot/reset/deep-sleep -> WLC wake tests;
9. test NFC while wireless charging is active;
10. define final BAT+/GND/+5V/+3V3 physical distribution and resulting W-numbers;
11. carrier pad-orientation continuity check;
12. OTA/control/integrated thermal testing before hull closure.

`VALIDATION.md` is authoritative for blocker status.
