# Model Kit Design

Engineering source-of-truth repository for model-kit electronics, lighting, firmware, mechanical integration, and test documentation.

## Current project

- `projects/defiant/` — 1/1000 USS Defiant electronics project

## Engineering rule

Drawings are downstream artifacts. The authoritative order is:

1. purchased BOM reconstruction
2. exact part/package identification
3. electrical architecture freeze
4. reference designators
5. formal netlist
6. MCU pin map
7. master wire list
8. per-module pin/connection tables
9. electrical validation
10. schematic sheets
11. physical harness/mechanical layout
12. bench layout
13. test firmware
14. final firmware

No schematic or CAD drawing is authoritative unless it is generated from and agrees with the approved textual netlist and pin map.

## Status convention

- **LOCKED** — previously agreed requirement; do not change silently.
- **VERIFIED** — checked against a manufacturer document, purchase record, or physical evidence.
- **RECONSTRUCTED** — recovered from project history but not yet re-verified against hardware.
- **PROVISIONAL** — engineering proposal awaiting review.
- **OPEN** — unresolved; must not be guessed in downstream drawings.
- **SUPERSEDED** — historical design retained only for traceability.
