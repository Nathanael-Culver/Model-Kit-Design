# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** Step 5 — formal netlist  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** |
| 3. Freeze electrical architecture | **COMPLETE — FROZEN v1.0** |
| 4. Freeze reference designators | **COMPLETE — FROZEN v1.0** in `DESIGNATORS.md` |
| 5. Formal netlist | **NEXT** |
| 6. XIAO pin map | provisional only |
| 7. Master wire list | partial only |
| 8. Per-module pin tables | partial only |
| 9. Validation | active; release blockers remain |
| 10+. Drawings/layout/firmware | gated |

## Frozen architecture summary

- U1 XIAO ESP32-C3 remains permanently connected to BT1.
- RX1 wireless power feeds U1's charging/recovery path through isolation and also creates `WLC_PRESENT` for wake.
- One `PERIPH_EN` GPIO controls the high-draw subsystem power architecture.
- U2 MT3608 is physically disconnected from BAT+ in sleep using Q1/Q2; MT3608 EN is not relied upon as the primary sleep disconnect.
- `+5V_LIGHT_SW` powers the single SK6812 serial bus, U4 level shifter, and four pulse-phaser LED supplies.
- Q3–Q6 independently switch PH0–PH3.
- U3 MFRC522 is supplied from separately switched 3.3 V through Q7/Q8 and is hardware-inhibited during wireless charging through Q9.
- U3 uses SPI SCK/MOSI/MISO/CS only; IRQ and dedicated MCU reset are not allocated.
- Total required U1 GPIO budget remains exactly 11.
- No GPIO expander, touch module, audio, second SK6812 data bus, reed wake, or NTC monitoring is part of the frozen architecture.
- Battery protection remains mandatory; U5 is reserved/DNP unless BT1 proves unprotected.

## Frozen reference-designator highlights

- `U1` XIAO, `U2` MT3608, `U3` MFRC522, `U4` SN74AHCT1G125; `U5` conditional battery protection.
- `Q1/Q2` lighting power gate.
- `Q3–Q6` PH0–PH3 switches.
- `Q7/Q8/Q9` NFC power gate and wireless-charge inhibit.
- `D1` wireless-input Schottky isolation.
- `LED10–LED13` are the four physical pulse-phaser LEDs.
- `LED1–LED9` are permanently superseded placeholders and must not be reused.
- Physical SK6812 emitters begin at `LED14` once physical count/order is confirmed.
- `R1–R17` and `C1–C2` have fixed functional slots; exact unresolved values are completed in Step 5.

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

The SK6812 architecture is one serial data bus, but physical emitter count/order remains a mechanical-layout detail and must not be inferred from the nine logical zones.

## Open implementation checks

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
- `DESIGNATORS.md` remains **FROZEN**.
- `NETLIST.md` is **APPROVED**.
- `PINOUT.md` has no duplicate GPIO or boot-state conflicts.
- `CONNECTIONS.md` defines every component pin.
- `WIRE-LIST.md` covers every applicable off-board connection.
- `VALIDATION.md` has no unresolved ERROR items.
