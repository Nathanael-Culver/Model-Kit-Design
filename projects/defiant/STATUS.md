# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 9c — physical placement / power-distribution design**  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | COMPLETE enough to proceed |
| 2. Identify part numbers/packages/carriers | MAJOR PART IDENTIFICATION CLOSED; BT1 protection proof still open |
| 3. Freeze electrical architecture | FROZEN v1.1 |
| 4. Freeze reference designators | **FROZEN v1.6** |
| 5. Formal netlist | **FORMAL v1.5** |
| 6. XIAO pin map | FROZEN v1.0 |
| 7. Master wire list | **FORMAL v1.2; W001–W066 reserved, W013/W053 DNP** |
| 8. Per-module pin tables | **FORMAL v1.4** |
| 9. Static electrical validation | COMPLETE — CONDITIONAL PASS |
| 9a. Architecture-policy decisions | COMPLETE / APPROVED |
| 9b. Part/module physical identification | COMPLETE enough to proceed |
| 9c. Physical placement / distribution | **ACTIVE** |
| 10+. Final drawings/layout/closure validation | gated |

## Frozen hardware / architecture

- BT1: 103450 / 3.7 V / 2500 mAh / 9.25 Wh; protection likely but not proven.
- TX1: XKT-412 transmitter + coil.
- RX1: XKT-3168 receiver + coil; selected as the 5 V/2 A wireless-power hardware.
- U2: MT3608 board with VIN+/VIN-/VOUT+/VOUT-; no exposed EN.
- U3: black XFW-ETLIVE V602 compact 3.3 V SPI reader.
- Pulse phasers: four DiCUNO prewired white 0805 LEDs, R6–R9 = 150 Ω.
- Addressable lighting: BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, one serial bus.

## Frozen physical lighting plan

**14 physical SK6812 pixels, LED14–LED27, across 9 logical zones:**

| Zone | Feature | Pixels |
|---|---|---:|
| P0 | top + bottom deflector | 2 |
| P1 | port bussard | 1 |
| P2 | starboard bussard | 1 |
| P3 | port warp chiller | 2 |
| P4 | starboard warp chiller | 2 |
| P5 | port impulse crystals | 2 |
| P6 | starboard impulse crystals | 2 |
| P7 | port impulse engine | 1 |
| P8 | starboard impulse engine | 1 |

Data chain is frozen as LED14 -> ... -> LED27 using W054–W066. See `LIGHTING-LAYOUT.md`.

## Important validation result

**There are no unresolved static electrical ERROR items.**

The remaining work is primarily physical implementation and bench acceptance, not architecture redesign.

## Remaining blockers before drawing release

1. prove BT1 protection status and discharge capability;
2. define exact component locations/orientations in the hull;
3. define BAT+/GND/+5V/+3V3 distribution and W067+ jumpers;
4. select wire gauges by current class and then measure lengths from the actual hull;
5. integrated XKT/D1 charging/recovery/load/thermal test;
6. U2/Q1 load/thermal test;
7. V602 reset/read-range/unpowered-backfeed/boot test;
8. D0/D8/D9 repeated boot and sleep/wake validation;
9. measure 14-pixel lighting load and freeze firmware current/brightness cap;
10. test V602 while wireless charging is active;
11. carrier-pad orientation validation;
12. OTA/control/integrated thermal testing before hull closure.

## Immediate design task

Proceed with the **physical component-placement and power-distribution plan**. Bench characterization of the XKT pair is deferred to the integrated validation stage rather than blocking this design work.

`VALIDATION.md` is authoritative for release blockers.
