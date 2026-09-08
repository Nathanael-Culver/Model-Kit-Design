# USS Defiant — Semantic EDA / Generated Schematic Pipeline

This directory is the machine-readable electrical-design layer for the Defiant.

## Authority chain

The intended workflow is:

1. engineering intent is reviewed/frozen in the project architecture, netlist, pinout, wire-list and validation documents;
2. `defiant-connectivity.xml` records component/pin/net/wire connectivity in machine-readable form;
3. `defiant-connectivity.xsd` + `validate_connectivity.py` validate the semantic source;
4. `generate_kicad.py` generates the canonical KiCad electrical graph;
5. `generate_kicad_autolayout.py` adds presentation-only flow/layout/ERC metadata;
6. GitHub Actions runs KiCad 10 ERC, PDF export and XML netlist export;
7. `validate_kicad_netlist.py` compares the KiCad-exported netlist back against the semantic XML;
8. `../harness/harness-topology.xml` adds VeSys-style physical branch/bundle organization without redefining electrical connectivity;
9. `../harness/generate_harness.py` creates the wire schedule, endpoint matrix and functional harness overview from the same electrical model.

The drawing is therefore a generated view of the electrical model rather than a manually drawn source of connectivity.

## Current readable-drawing behavior

The subsystem drawings now use:

- character-aware symbol width based on pin names, pin numbers, net names, values and wire IDs;
- 5.08 mm pin pitch and explicit wire stubs;
- automatic A4/A3/A2/A1/A0 sheet selection;
- deterministic subsystem flow lanes;
- no ERC-only `PWR_FLAG` helper boxes in human build sheets;
- direct orthogonal wires for safe two-terminal local nets;
- one explicit net-name label and one wire-ID annotation per direct-routed net;
- collision checks before export.

Examples of direct-routed nets:

- Q1 -> U2 `U2_VIN_SW`;
- U4 -> R5 -> LED14 and LED14 -> ... -> LED27 serial data path;
- R6–R9 -> LED10–LED13 and LED10–LED13 -> Q3–Q6 phaser current paths.

Shared rails / branched nets such as `GND`, `+5V_LIGHT_SW`, `PERIPH_EN`, `NFC_GATE`, etc. remain named-net connections for now. They will be promoted to explicit rails/junctions only when the renderer can do so without creating ambiguous crossings.

## Presentation-only pin orientation

For readability only, the generated view may change which side of a rectangular symbol a pin is drawn on. It does **not** change pin number or electrical net.

Current examples:

- LED21–LED27 swap displayed DIN/DOUT sides so the second half of the physical SK6812 chain can be drawn right-to-left as a clean snake;
- Q3–Q6 display Drain toward the phaser LED cathode.

The exported canonical flat KiCad netlist is still cross-checked against XML pin-by-pin.

## KiCad ERC helpers

`generate_kicad_autolayout.py` adds KiCad-only `PWR_FLAG` objects so ERC can understand supplies that cross passive diode/MOSFET pins. These helpers:

- are not physical parts;
- are excluded from the BOM;
- are omitted from human subsystem drawings;
- exist only in the canonical flat KiCad electrical model used for ERC.

## Current CI acceptance

A release of the generated electrical drawing is accepted only when CI confirms all of the following:

- semantic XML/XSD validation PASS;
- generator/layout collision checks PASS;
- KiCad native ERC = 0 errors / 0 warnings;
- KiCad PDF exports PASS;
- KiCad XML netlist export PASS;
- all active XML pin/net assignments exactly match KiCad export.

The same workflow now also validates the harness layer. Harness generation is accepted only when:

- every reserved W001-W066 ID belongs to a defined functional branch;
- every active/conditional conductor resolves to two endpoints or an explicit approved distribution-node override;
- W013 and W053 remain permanent DNP/superseded IDs;
- no active harness net/endpoint is left unresolved;
- the functional harness SVG/PDF renders successfully.

This validates the EDA/harness representation. It does **not** replace physical bench tests such as battery protection, MT3608 load/thermal behavior, V602 backfeed/boot behavior, charging coexistence, final LED current, or OTA testing.

## Harness layer

See `../harness/README.md`.

The current baseline groups W001-W066 into:

- `H-BAT`;
- `H-WLC`;
- `H-CTRL`;
- `H-PHASER`;
- `H-NFC`;
- `H-SKDATA`;
- `H-LIGHT-PWR-FUTURE` for W067+ after hull dimensions are measured.

Wire colors, routed/cut lengths, exact splice locations and final gauge acceptance remain intentionally open until physical measurements and bench load validation exist.

## Next presentation-layer work

The schematic generator can continue to improve incrementally without changing the electrical source:

1. modest alignment/spacing cleanup;
2. more safe local two-pin routes;
3. selected shared rails / junction dots where collision-free routing can be proven;
4. off-sheet continuation conventions.

The harness side is now far enough along that future physical measurements can be added as data rather than forcing the electrical documentation to be redrawn manually.
