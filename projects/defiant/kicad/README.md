# USS Defiant KiCad / Semantic EDA Project

The KiCad schematic is **generated from semantic connectivity data**, not hand-drawn as the electrical source of truth.

Primary source:

- `../eda/defiant-connectivity.xml`

Generator / validation:

- `../eda/validate_connectivity.py`
- `../eda/validate_kicad_netlist.py`
- `../eda/generate_kicad.py`
- `../eda/defiant-connectivity.xsd`
- `../../.github/workflows/defiant-eda-validation.yml`

## Current native validation state

GitHub Actions now installs **KiCad 10** and performs a real generation / parse / ERC / export cycle.

Latest validated result (2026-09-07/08, run 10):

- semantic XML/XSD validation: **PASS**;
- generated complete KiCad schematic parses: **PASS**;
- KiCad native ERC: **0 errors / 0 warnings** after documented ERC-only switched-power modeling hints;
- KiCad PDF export: **PASS**;
- KiCad XML netlist export: **PASS**;
- source XML -> exported KiCad connectivity cross-check: **PASS**;
- exported KiCad netlist contains **55 components and 174 connected pins**;
- **164 active source pin/net assignments exactly match** the semantic XML.

This cross-check exists specifically to prevent the earlier false-positive failure mode where KiCad successfully opened a hierarchy whose child pages contained no electrical objects.

## Generated drawing model

The generator now creates:

- `USS-Defiant.kicad_sch` — one **complete flat electrical connectivity sheet** used for ERC and machine netlist comparison;
- `power.kicad_sch` — standalone phone/readability view;
- `controller.kicad_sch` — standalone controller view;
- `lighting.kicad_sch` — standalone 14-pixel lighting view;
- `phasers.kicad_sch` — standalone phaser view;
- `nfc.kicad_sch` — standalone NFC view.

The subsystem pages deliberately use simple block symbols and pin-attached net labels. They are **connectivity drawings**, not yet the polished conventional schematic presentation.

## Regeneration

Run from `projects/defiant/`:

```bash
python eda/validate_connectivity.py
python eda/generate_kicad.py
```

The GitHub Action performs the same regeneration automatically before native validation, so CI always validates the XML-generated design rather than trusting stale generated files.

## Validation artifacts

The GitHub Action publishes an artifact named `defiant-kicad-validation` containing:

- `USS-Defiant-Complete-Flat.pdf`
- `USS-Defiant-Subsystems.pdf`
- separate power/controller/lighting/phasers/NFC PDFs
- `USS-Defiant-KiCad-netlist.xml`
- `defiant-erc.rpt`
- `connectivity-crosscheck.log`
- `VALIDATION-SUMMARY.md`

## Why this workflow exists

The earlier manually rendered SVG/PDF attempts mixed two jobs:

1. deciding electrical connectivity;
2. arranging a readable drawing.

That allowed a visually plausible drawing to imply the wrong circuit.

The new workflow separates them. Component pins, nets, wire IDs, DNP/NC state, and functional grouping are stored as machine-readable data first. KiCad then acts as a CAD renderer/editor/ERC engine.

The same semantic source is intended to grow into a **VeSys-style harness model** containing connector cavities, splices, wire gauge/color/length, bundles, branches, termination data, and physical harness coordinates. Harness XML/SVG/PDF outputs can then be generated from the validated connectivity instead of redrawn independently.

## Next refinement

Connectivity validation is now functioning correctly. The next CAD work is presentation and harness modeling:

- replace important generic blocks with polished electrical symbols where that improves readability;
- keep the source XML and exported KiCad netlist automatically cross-checked;
- cross-check XML against `WIRE-LIST.md` and `DESIGNATORS.md`;
- extend the XML schema with harness branch/splice/termination fields;
- generate a VeSys-like harness/connection drawing from the same validated model.
