# USS Defiant KiCad Project

This directory is generated from `../eda/defiant-connectivity.xml`.

## Files

- `USS-Defiant.kicad_pro` — KiCad project.
- `USS-Defiant.kicad_sch` — root schematic.
- `power.kicad_sch` — battery, wireless charging, divider, Q1/Q2 and MT3608.
- `controller.kicad_sch` — XIAO ESP32-C3 pin/net assignment.
- `lighting.kicad_sch` — U4 level shifter, C1/C2, R5 and LED14–LED27.
- `phasers.kicad_sch` — four conventional phaser LED/MOSFET channels.
- `nfc.kicad_sch` — V602 SPI and Q7/Q8 switched 3.3 V rail.

## Important

The project was generated without a KiCad binary available in the execution environment. The files are structurally checked and the XML connectivity is semantically validated, but **KiCad ERC has not yet been run**. Open the project in KiCad, allow KiCad to update/save the file format if prompted, then run ERC before using it for fabrication.

The design deliberately uses embedded custom block symbols and named nets. This makes the connectivity deterministic and avoids the line-routing ambiguity that affected earlier hand-rendered drawings. Once opened in KiCad, the symbols can be rearranged or replaced with prettier standard/custom symbols without changing the net names.

## Source-of-truth workflow

1. Change/audit electrical intent in `../eda/defiant-connectivity.xml`.
2. Run `../eda/validate_connectivity.py`.
3. Regenerate KiCad with `../eda/generate_kicad.py`.
4. Open KiCad and run ERC.
5. Only then update PDF/harness drawings.
