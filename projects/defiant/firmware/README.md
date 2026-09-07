# Firmware Workspace

Firmware code will be added only after the approved electrical pin map exists.

Planned structure:

- `test/` — staged hardware bring-up sketches/builds
- `src/` — final firmware
- `include/hardware_config.*` — single code-side hardware mapping derived from `PINOUT.md` and `NETLIST.md`

No code should hard-code an alternate pin map or pixel order outside the centralized hardware configuration.
