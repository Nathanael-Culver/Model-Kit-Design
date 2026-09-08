# USS Defiant - Harness / Interconnect Documentation

This directory is the physical interconnect layer that sits on top of the semantic electrical model in `../eda/`.

## Purpose

The EDA XML answers **what is electrically connected**. The harness layer answers **how the conductors are organized for fabrication and installation**.

The intended workflow mirrors a lightweight VeSys-style process:

1. `../eda/defiant-connectivity.xml` defines component pins, electrical nets, and permanent wire IDs.
2. `harness-topology.xml` groups those wire IDs into functional harness branches/bundles and defines provisional distribution nodes.
3. `generate_harness.py` resolves the two endpoints of every W001-W066 conductor from the semantic EDA source or an explicit distribution-node override.
4. The generator emits a wire schedule, endpoint matrix, functional harness overview, and validation report.
5. After hull measurements, W067+ will define the actual front/port/starboard +5V and GND distribution branches, along with routed/cut lengths.

The harness layer must never silently change electrical connectivity. If a harness endpoint conflicts with the semantic EDA model, validation must fail.

## Current branch IDs

| Branch | Purpose | Main classes |
|---|---|---|
| `H-BAT` | battery / primary power / MT3608 path | PWR-A |
| `H-WLC` | RX1 wireless charging and wake | PWR-B, SIG-B |
| `H-CTRL` | power-gate control and SK6812 level-shifter interface | SIG-A, SIG-B, PWR-B |
| `H-PHASER` | four phaser control/current paths | SIG-B, PHASER |
| `H-NFC` | V602 SPI, switched 3.3V and NFC gate | SIG-B, PWR-B |
| `H-SKDATA` | LED14 -> LED27 serial SK6812 data path | SIG-A |
| `H-LIGHT-PWR-FUTURE` | future W067+ front/port/starboard +5V/GND branches | PWR-B |

## Wire-class targets

These are starting design targets, not yet fabrication releases:

- `PWR-A`: 24 AWG preferred for main battery/boost current path.
- `PWR-B`: 26 AWG preferred for module/lighting power branches.
- `SIG-A`: 30 AWG preferred for SK6812 data.
- `SIG-B`: 30 AWG preferred for SPI/gates/sense/control.
- `PHASER`: factory LED leads where practical; otherwise ~30 AWG.

Final gauge acceptance depends on actual wire inventory and integrated current/thermal testing.

## Generated outputs

`generate_harness.py` creates under `generated/`:

- `HARNESS-OVERVIEW.svg` - functional assembly-zone/branch view;
- `WIRE-SCHEDULE.csv` - machine-friendly fabrication schedule;
- `WIRE-SCHEDULE.md` - human-readable schedule;
- `PIN-ENDPOINT-MATRIX.csv` - endpoint cross-reference;
- `HARNESS-VALIDATION.md` - generation/endpoint validation result.

GitHub Actions additionally renders `HARNESS-OVERVIEW.pdf` and publishes all generated harness files as the `defiant-harness-documentation` artifact.

## What remains intentionally open

No guessed dimensions are stored here. The following wait for actual hull measurements:

- wire color;
- routed length;
- cut length;
- strip length;
- final splice/junction coordinates;
- exact bundle breakout locations;
- W067+ lighting power-distribution conductors;
- final gauge confirmation after load testing.

This allows harness documentation to advance now without pretending we know physical dimensions that have not yet been measured.
