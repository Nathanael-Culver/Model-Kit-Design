# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** Step 4 — freeze reference designators  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** |
| 3. Freeze electrical architecture | **COMPLETE — FROZEN v1.0** in `POWER-ARCHITECTURE.md` |
| 4. Freeze reference designators | **NEXT** |
| 5. Formal netlist | draft only; update after Step 4 |
| 6. XIAO pin map | provisional only |
| 7. Master wire list | partial only |
| 8. Per-module pin tables | partial only |
| 9. Validation | active; release blockers remain |
| 10+. Drawings/layout/firmware | gated |

## Frozen architecture summary

- U1 XIAO ESP32-C3 remains permanently connected to BT1.
- RX1 wireless power feeds U1's charging/recovery path through isolation and also creates `WLC_PRESENT` for wake.
- One `PERIPH_EN` GPIO controls the high-draw subsystem power architecture.
- U2 MT3608 is physically disconnected from BAT+ in sleep using AO3401A high-side switching with AO3400A helper control; MT3608 EN is not relied upon as the primary sleep disconnect.
- `+5V_LIGHT_SW` powers the single SK6812 serial bus, its SN74AHCT1G125 level shifter, and the four pulse-phaser LED supplies.
- Four AO3400A channels independently sink the four conventional phaser LEDs.
- U3 MFRC522 is supplied from a separately switched 3.3 V rail but does not consume a separate MCU power-enable GPIO.
- Hardware prevents MFRC522 operation while wireless charging is present: `NFC allowed = PERIPH_EN AND NOT WLC_PRESENT`.
- MFRC522 uses SPI SCK/MOSI/MISO/CS only; IRQ and dedicated MCU reset are not allocated.
- Total required U1 GPIO budget remains exactly 11: 1 SK data + 4 phasers + 4 NFC SPI + 1 wireless wake + 1 peripheral enable.
- No GPIO expander, touch module, audio, second SK6812 data bus, reed wake, or NTC monitoring is part of the frozen architecture.
- Battery protection remains a mandatory safety requirement; exact implementation depends on whether BT1 is physically confirmed to contain an integral protection circuit.

## Lighting decision

The accepted logical map remains:

| Zone | Function |
|---|---|
| P0 | Deflector, top + bottom combined |
| P1 | Port bussard |
| P2 | Starboard bussard |
| P3 | Port warp chiller/grille |
| P4 | Starboard warp chiller/grille |
| P5 | Port impulse crystals, both crystals combined |
| P6 | Starboard impulse crystals, both crystals combined |
| P7 | Port impulse engine |
| P8 | Starboard impulse engine |

PH0–PH3 remain four independent non-addressable white pulse-phaser LEDs.

The SK6812 architecture is now frozen as **one serial data bus**, but physical emitter count/order remains a mechanical-layout detail and must not be inferred from the nine logical zones.

## Open implementation checks

These no longer block the architecture concept but must be closed before schematic/assembly release:

1. BT1 protection status.
2. Exact RX1 board/pad identity and measured output.
3. Exact U2 module/pads and 5 V load behavior.
4. Exact U3 module/header/reset behavior.
5. Prewired phaser LED electrical specification.
6. Physical SK6812 emitter count/order.
7. Final passive values and inventory.
8. Final GPIO assignment/boot validation.
9. Backfeed/default-off tests.

## Drawing release criteria

The drawing gate opens only when all of the following are true:

- `POWER-ARCHITECTURE.md` remains **FROZEN**.
- `NETLIST.md` is **APPROVED**.
- `PINOUT.md` has no duplicate GPIO or boot-state conflicts.
- `CONNECTIONS.md` defines every component pin.
- `WIRE-LIST.md` covers every applicable off-board connection.
- `VALIDATION.md` has no unresolved ERROR items.
