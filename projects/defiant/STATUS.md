# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** Step 3 — electrical architecture freeze  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** — exact purchase evidence recorded; unresolved physical variants explicitly OPEN |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** — exact semiconductor packages established; module variants requiring photographs remain OPEN |
| 3. Freeze electrical architecture | **NEXT** |
| 4. Freeze reference designators | pending |
| 5. Formal netlist | draft only; pending architecture freeze |
| 6. XIAO pin map | provisional only |
| 7. Master wire list | partial only |
| 8. Per-module pin tables | partial only |
| 9. Validation | active; release blockers remain |
| 10+. Drawings/layout/firmware | gated |

Detailed Step-2 identification is in `PARTS-AND-PACKAGES.md`.

## Locked project requirements

- Seeed Studio XIAO ESP32-C3 remains connected to the 3.7 V LiPo.
- Deep sleep is the normal low-standby state.
- The lighting boost rail is off while asleep.
- MFRC522 NFC hardware is off while asleep.
- Wireless-power-present must be detectable by the XIAO and must support wake/recovery behavior.
- NFC is retained for future Star Trek “memory crystal” controls.
- The sealed model must remain controllable and firmware-updatable wirelessly.
- No TTP223 touch module.
- No speaker/audio in this build.
- Preserve purchased parts wherever reasonably possible; no silent substitutions.
- No final CAD/schematic artwork until the textual netlist and pin map pass validation.

## Reconstructed lighting decision

Recovered from project history on 2026-02-22:

| Pixel/zone | Function | Status |
|---|---|---|
| P0 | Deflector, top + bottom combined | RECONSTRUCTED / previously accepted |
| P1 | Port bussard | RECONSTRUCTED / previously accepted |
| P2 | Starboard bussard | RECONSTRUCTED / previously accepted |
| P3 | Port warp chiller/grille | RECONSTRUCTED / previously accepted |
| P4 | Starboard warp chiller/grille | RECONSTRUCTED / previously accepted |
| P5 | Port impulse crystals, both crystals combined | RECONSTRUCTED / previously accepted |
| P6 | Starboard impulse crystals, both crystals combined | RECONSTRUCTED / previously accepted |
| P7 | Port impulse engine | RECONSTRUCTED / previously accepted |
| P8 | Starboard impulse engine | RECONSTRUCTED / previously accepted |

Pulse phasers are separate from the addressable pixels:

- PH0–PH3: four independent non-addressable prewired 0805 white LEDs.

### Important unresolved point

History confirms **nine accepted addressable logical zones**, but the evidence recovered so far does **not** conclusively establish the final physical SK6812 emitter count or physical routing/chain topology. Earlier project history reconstructs 5050 SK6812 RGBW flexible strip. Physical count/order must be confirmed rather than inferred from the nine logical zones.

## Current blockers before architecture freeze

1. Confirm exact purchased MFRC522 breakout/module variant and its exposed pins.
2. Confirm exact MT3608 carrier/module variant, especially whether EN is accessible or hard-wired high.
3. Confirm exact XKT receiver board/module and connector/pad labels; IC marking is believed to be XKT-3168.
4. Confirm exact prewired 0805 LED electrical specification and whether series resistors are already present in the leads.
5. Resolve final SK6812 physical emitter count/chain topology while preserving the accepted P0–P8 logical map.
6. Resolve GPIO allocation with boot/strapping and deep-sleep wake constraints.
7. Resolve exact lighting and NFC power-gating implementation.
8. Confirm resistor/capacitor inventory actually on hand; the recovered DigiKey invoice does not contain ordinary resistors or capacitors.
9. Confirm whether BT1 includes integral cell-protection circuitry.

## Drawing release criteria

The drawing gate opens only when all of the following are true:

- `BOM.md` has no architecture-critical unknown component variant.
- `POWER-ARCHITECTURE.md` is marked **FROZEN**.
- `NETLIST.md` is marked **APPROVED**.
- `PINOUT.md` has no duplicate GPIO or boot-state conflicts.
- `WIRE-LIST.md` covers every off-board electrical connection.
- `VALIDATION.md` has no unresolved ERROR items.
