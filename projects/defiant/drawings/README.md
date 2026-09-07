# Drawings

**FINAL RELEASE GATE: CLOSED**

A **pre-release engineering schematic** is now allowed because the electrical architecture, reference designators, netlist, GPIO assignment, 14-pixel lighting map, and per-component connection tables are sufficiently defined to draw the circuit accurately.

This does **not** mean final assembly release is approved. Remaining bench/physical blockers in `VALIDATION.md` still control final release.

## Current schematic set

The current engineering schematic is documented in `SCHEMATIC.md` and organized as four sheets:

1. power, wireless charging, wake, battery path, Q1/Q2 and MT3608;
2. U4 level shifting and the complete LED14-LED27 SK6812 RGBW chain;
3. XIAO pin map, V602 NFC SPI interface, Q7/Q8 NFC power gating, Q9 DNP;
4. four independent pulse-phaser channels Q3-Q6 / LED10-LED13.

## Release rule

The schematic remains **PRE-RELEASE** until the hardware-critical validation items that can affect drawing correctness are closed. Final schematic/CAD release must remain consistent with:

- `POWER-ARCHITECTURE.md`
- `DESIGNATORS.md`
- `NETLIST.md`
- `PINOUT.md`
- `CONNECTIONS.md`
- `LIGHTING-LAYOUT.md`
- `VALIDATION.md`

Physical dimensions are **not** required for the electrical schematic. They are required later for the harness/mechanical layout and final wire lengths.
