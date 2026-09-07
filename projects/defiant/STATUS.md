# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 10a — semantic EDA / KiCad first-open + ERC**  
**Fabrication/closure gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | COMPLETE enough to proceed |
| 2. Identify part numbers/packages/carriers | MAJOR PART IDENTIFICATION CLOSED; BT1 protection proof still open |
| 3. Freeze electrical architecture | **FROZEN v1.2** |
| 4. Freeze reference designators | **FROZEN v1.6** |
| 5. Formal netlist | **FORMAL v1.5** |
| 6. XIAO pin map | FROZEN v1.0 |
| 7. Master wire list | **FORMAL v1.2; W001–W066 reserved, W013/W053 DNP** |
| 8. Per-module pin tables | **FORMAL v1.4** |
| 9. Static electrical validation | COMPLETE — CONDITIONAL PASS |
| 9a. Architecture-policy decisions | COMPLETE / APPROVED |
| 9b. Part/module physical identification | COMPLETE enough to proceed |
| 9c. Physical placement / distribution concept | CONCEPT FROZEN; exact coordinates/lengths deferred |
| 10a. Machine-readable EDA source | **CREATED — XML/XSD + semantic validator** |
| 10b. KiCad generation | **GENERATED structurally; native KiCad ERC still required** |
| 10c. Harness-style renderer/database | NEXT after KiCad first-open/ERC |
| Bench development layout | DEFINED in `bench/BENCH-LAYOUT.md` |
| Assembly sequence | DEFINED in `ASSEMBLY.md` |

## EDA workflow now in use

Manual SVG/PDF schematics are no longer connectivity authority. The new flow is:

1. electrical intent in the authoritative text/netlist documents;
2. machine-readable connectivity in `eda/defiant-connectivity.xml`;
3. schema/semantic validation using `eda/defiant-connectivity.xsd` and `eda/validate_connectivity.py`;
4. deterministic schematic generation using `eda/generate_kicad.py`;
5. open/save in KiCad and run native ERC;
6. only after ERC, promote/export the readable schematic;
7. extend the same semantic model into VeSys-style harness data and generated harness drawings.

Current generated structure includes a KiCad project/root plus power, controller, lighting, phaser, and NFC child sheets. The generation environment does not contain KiCad, so **ERC has not yet been run** and no fabrication claim is being made.

## Confirmed hardware

- BT1: 103450 / 3.7 V / 2500 mAh / 9.25 Wh; protection likely but not proven.
- TX1: XKT-412 transmitter + flat spiral coil.
- RX1: XKT-3168 receiver + flat spiral coil; selected 5 V/2 A wireless-power hardware.
- U2: MT3608 with VIN+/VIN-/VOUT+/VOUT-; no exposed EN.
- U3: black XFW-ETLIVE V602 compact 3.3 V SPI reader.
- U4: SN74AHCT1G125DBVR level shifter.
- Phasers: four DiCUNO prewired white 0805 LEDs, R6–R9 = 150 Ω.
- Addressable lighting: BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m.

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

**There are no unresolved static electrical ERROR items in the textual audit.**

That does not replace KiCad ERC or bench validation.

## Remaining blockers before fabrication/closure release

1. first-open/resave of generated KiCad project and native ERC review;
2. prove BT1 protection status and discharge capability;
3. continuity-map SOT carriers;
4. integrated XKT/D1 charging/recovery/load/thermal test;
5. U2/Q1 load/thermal test;
6. V602 reset/read-range/unpowered-backfeed/boot test;
7. D0/D8/D9 repeated boot and sleep/wake validation;
8. measure 14-pixel lighting load and freeze firmware current/brightness cap;
9. test V602 while wireless charging is active;
10. later: measure exact component/LED positions and assign W067+ distribution segments/lengths;
11. OTA/control/integrated thermal testing before hull closure.

## Immediate next milestone

Open the generated KiCad project, allow KiCad to update/save the format if requested, and run ERC. Any parsing/ERC findings become the next concrete engineering work. Hull dimensions can wait until the electrical drawing pipeline is proven.

`VALIDATION.md` remains authoritative for hardware release blockers.
