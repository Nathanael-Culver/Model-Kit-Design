# USS Defiant — Electrical Schematic

**Current drawing status:** **MANUAL SVG/PDF SCHEMATICS DEPRECATED FOR CONNECTIVITY AUTHORITY**  
**New EDA direction:** KiCad project generated from machine-readable connectivity data.

## Why this changed

The earlier hand-rendered schematic sheets were useful as visual drafts but were too easy to make graphically ambiguous. The electrical design is now moving to a semantic-first workflow where component pins and named nets are defined as machine-readable data, then rendered by an EDA tool.

The authoritative electrical intent remains:

- `../POWER-ARCHITECTURE.md`
- `../DESIGNATORS.md`
- `../NETLIST.md`
- `../PINOUT.md`
- `../CONNECTIONS.md`
- `../LIGHTING-LAYOUT.md`
- `../WIRE-LIST.md`

## New generated EDA structure

- `../kicad/USS-Defiant.kicad_pro` — KiCad project scaffold.
- `../kicad/USS-Defiant.kicad_sch` — hierarchical root schematic.
- `../kicad/README.md` — KiCad workflow and validation notes.
- `../eda/defiant-connectivity.xsd` — schema for machine-readable connectivity.
- `../eda/validate_connectivity.py` — semantic validator.
- `../eda/VALIDATION-REPORT.md` — current generator/structure validation result.

The complete generated EDA package also contains the XML connectivity source and five generated child schematic sheets: power, controller, lighting, phasers, and NFC.

## Validation policy

The generated files have passed XML/schema/semantic checks and structural S-expression checks, but **KiCad ERC has not yet been run in this environment because KiCad is not installed here**.

Therefore:

1. generated KiCad files are **REVIEW**, not fabrication release;
2. open/save the project in KiCad first;
3. run ERC;
4. resolve or explicitly document every meaningful ERC finding;
5. only then promote the KiCad schematic to electrical drawing authority.

## Drawing philosophy going forward

Do not manually redraw circuit connectivity into SVG/PDF and treat the picture as the source of truth. Connectivity should be defined semantically first, validated, and then rendered/exported by KiCad or a harness-style XML/SVG renderer.

Physical harness drawings remain a later deliverable and should be generated from the same pin/net/wire database so reference designators, pin numbers, net names, and wire IDs cannot silently diverge.
