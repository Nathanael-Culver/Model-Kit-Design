# USS Defiant — Master Wire List

**Document status:** PARTIAL / ROUTED LENGTHS NOT YET ALLOWED  
**Rule:** wire IDs are permanent. Deleted wires are marked `DNP/SUPERSEDED`; IDs are never renumbered.

## Fields

Every final wire record must include: Wire ID, from component/pin, to component/pin, net, color, gauge, routed length, cut length, strip length, termination note, and status.

## Current master list

Only connections already locked strongly enough to define physical endpoints receive wire IDs now.

| Wire ID | From | From pin | To | To pin | Net | Color | Gauge | Routed length | Cut length | Strip | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W001 | BT1 | + lead | U1 | BAT+ pad | `BAT+` | TBD | TBD | TBD after hull measurement | TBD | TBD | LOCKED electrical endpoint; physical length OPEN |
| W002 | BT1 | - lead | U1 | BAT- pad | `GND` | TBD | TBD | TBD after hull measurement | TBD | TBD | LOCKED electrical endpoint; physical length OPEN |

## Why the list stops at W002

RX1, U2, U3, power-gate MOSFETs, SK6812 chains, and phaser channels still contain architecture-critical open endpoints. Assigning W003+ now would make a guessed harness look authoritative.

When `NETLIST.md` is approved, wire IDs will be allocated in this order: primary power/ground; wireless input/recovery; switched rails; MCU control/sense; NFC SPI; addressable LED harness; phasers; test/service leads.

## Harness length policy

No numeric length belongs here until the physical hull layout is approved from measurements/photos.

- **Routed length** = measured path along the actual approved route.
- **Cut length** = routed length + service allowance + termination allowance.
- **Strip length** = specified independently for each termination type.

Drawings may reference wire IDs but may not invent wire lengths.
