# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 10b — validated semantic EDA / readable generated schematic**  
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
| 10b. KiCad generation / validation | **ACTIVE AND PASSING — KiCad 10 ERC + netlist cross-check + PDF render** |
| 10c. Readable schematic presentation | **FLOW-AWARE + CHARACTER-AWARE + SELECTIVE DIRECT ROUTING IMPLEMENTED** |
| 10d. VeSys-style harness database/renderer | NEXT after shared-rail/junction presentation |
| Bench development layout | DEFINED in `bench/BENCH-LAYOUT.md` |
| Assembly sequence | DEFINED in `ASSEMBLY.md` |

## EDA workflow now in use

Manual SVG/PDF schematics are no longer connectivity authority. The current flow is:

1. electrical intent in the authoritative project documents;
2. machine-readable component/pin/net/wire connectivity in `eda/defiant-connectivity.xml`;
3. schema/semantic validation with `defiant-connectivity.xsd` and `validate_connectivity.py`;
4. canonical KiCad electrical-graph generation using `generate_kicad.py`;
5. flow-aware / character-aware human-view generation using `generate_kicad_autolayout.py`;
6. GitHub Actions installs KiCad 10 and runs native ERC, PDF export and XML netlist export;
7. `validate_kicad_netlist.py` compares the KiCad-exported pin/net assignments back against source XML.

See `eda/README.md` for the pipeline rules.

## Current EDA validation result

Latest validated generator stage:

- **59 KiCad objects** in the canonical flat model, including 4 explicitly EDA-only ERC power flags;
- **178 connected KiCad pins**;
- **164/164 active semantic XML pin/net assignments exactly match the KiCad export**;
- **KiCad native ERC: 0 errors / 0 warnings**;
- subsystem PDF export: PASS;
- complete flat PDF export: PASS;
- character/layout collision checks: PASS.

The human subsystem drawings exclude ERC-only PWR_FLAG helper boxes.

## Current readable schematic improvements

The generated subsystem drawings now:

- size component bodies/envelopes according to pin-name, pin-number, net-name, value and wire-ID character lengths;
- automatically select a standard page size that fits without squeezing labels;
- group components by actual functional flow;
- arrange the SK6812 chain as a visual snake matching LED14 -> ... -> LED27;
- arrange each phaser as its own repeated current path;
- draw safe two-terminal local nets as actual orthogonal wires instead of duplicate disconnected-looking labels;
- retain exactly one explicit net name and wire ID for every direct-routed net;
- keep shared/multi-drop nets named until a deterministic junction/rail router is added.

Current directly rendered paths include:

- Q1 -> U2 `U2_VIN_SW`;
- U4 -> R5 -> LED14 and all thirteen inter-pixel SK6812 data links;
- R6–R9 -> LED10–LED13 and LED10–LED13 -> Q3–Q6.

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

**There are no unresolved static electrical ERROR items, and the current generated KiCad electrical graph passes native ERC and source-netlist comparison.**

That still does not replace the physical bench-validation items below.

## Remaining blockers before fabrication/closure release

1. prove BT1 protection status and discharge capability;
2. continuity-map SOT carriers;
3. integrated XKT/D1 charging/recovery/load/thermal test;
4. U2/Q1 load/thermal test;
5. V602 reset/read-range/unpowered-backfeed/boot test;
6. D0/D8/D9 repeated boot and sleep/wake validation;
7. measure 14-pixel lighting load and freeze firmware current/brightness cap;
8. test V602 while wireless charging is active;
9. later: measure exact component/LED positions and assign W067+ distribution segments/lengths;
10. OTA/control/integrated thermal testing before hull closure.

## Immediate next EDA milestone

Add deterministic rendering for selected **multi-drop/shared nets** using explicit rails, branch junctions and continuation labels without allowing wire/label/component collisions. Then extend the same semantic model with VeSys-style harness attributes: wire gauge, color, routed length, bundle/branch and splice data.

`VALIDATION.md` remains authoritative for hardware release blockers.
