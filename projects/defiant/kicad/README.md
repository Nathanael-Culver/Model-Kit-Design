# USS Defiant KiCad Project

The KiCad schematic is **generated from semantic connectivity data**, not hand-drawn as the source of truth.

Primary source:

- `../eda/defiant-connectivity.xml`

Generator / validation:

- `../eda/validate_connectivity.py`
- `../eda/generate_kicad.py`
- `../eda/defiant-connectivity.xsd`

## Repository state

The repository keeps the machine-readable source, generator, project file, and hierarchical root schematic under version control.

Run this from `projects/defiant/` to generate or refresh the complete KiCad hierarchy:

```bash
python eda/validate_connectivity.py
python eda/generate_kicad.py
```

That generates/refreshes:

- `kicad/USS-Defiant.kicad_pro`
- `kicad/USS-Defiant.kicad_sch`
- `kicad/power.kicad_sch`
- `kicad/controller.kicad_sch`
- `kicad/lighting.kicad_sch`
- `kicad/phasers.kicad_sch`
- `kicad/nfc.kicad_sch`

A complete generated package is also being provided in the engineering chat so it can be opened immediately without running the generator first.

## First KiCad-open procedure

1. Open `kicad/USS-Defiant.kicad_pro` in a current KiCad release.
2. If KiCad offers to update/resave the generated schematic format, allow it.
3. Inspect all five child sheets.
4. Run **Electrical Rules Checker (ERC)**.
5. Save/export the ERC report or capture the remaining errors/warnings.
6. Do **not** use the project for fabrication until meaningful ERC findings are resolved or explicitly documented.

## Current validation state

The generator output has been checked for:

- XML/XSD validity;
- duplicate component/pin definitions;
- active pins lacking a net;
- required critical-net semantics;
- JSON parseability of the `.kicad_pro` file;
- balanced S-expressions/quotes in generated `.kicad_sch` files.

**Native KiCad ERC has not been run in the generation environment because KiCad is not installed there.**

## Why this workflow exists

The earlier manually rendered SVG/PDF schematic attempts mixed two separate jobs:

1. deciding electrical connectivity;
2. arranging a readable drawing.

That made it possible for the picture to accidentally imply connections that were not intended.

This workflow separates them. Component pins, nets, wire IDs, DNP/NC state, and functional grouping are stored as data first. KiCad is then a renderer/editor/ERC engine for that data.

The same XML source can later be extended into a VeSys-style harness database with connector cavities, splices, wire gauge/color/length, bundles, branches, termination information, and physical harness coordinates. Harness SVG/PDF tables can then be generated from the same electrical source instead of redrawn independently.

## Generation philosophy

The first generated symbols are deliberately simple embedded block symbols. Connectivity correctness comes before cosmetic symbol quality.

Once the first KiCad open/ERC cycle succeeds, the next refinement is to:

- replace selected blocks with polished custom symbols where useful;
- make generated UUIDs deterministic so Git diffs remain clean;
- add stronger automated cross-checks against `WIRE-LIST.md` and `DESIGNATORS.md`;
- generate the physical harness drawing from the same XML model.
