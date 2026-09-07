# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** Step 6 — XIAO pin map  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** |
| 3. Freeze electrical architecture | **COMPLETE — FROZEN v1.0** |
| 4. Freeze reference designators | **COMPLETE — FROZEN v1.0** |
| 5. Formal netlist | **COMPLETE enough to proceed — FORMAL v1.0** in `NETLIST.md`; drawing approval waits on physical/pin validation |
| 6. XIAO pin map | **NEXT** |
| 7. Master wire list | partial only |
| 8. Per-module pin tables | partial only |
| 9. Validation | active; release blockers remain |
| 10+. Drawings/layout/firmware | gated |

## Step-5 formal netlist highlights

- D1 orientation is fixed: `WLC_5V_RAW` -> D1 anode; D1 cathode -> `SYS_5V_IN` -> U1 5 V input.
- `WLC_PRESENT` divider is R1 130 kΩ / R2 180 kΩ, subject to final RX1 voltage measurement.
- Q1/Q2 lighting power gate topology and default-OFF resistor network are fully defined.
- U2 functional IN+/IN-/OUT+/OUT- nets are defined.
- U4 is fully pinned; OE is tied low, VCC is switched 5 V, C1 = 0.1 µF local bypass, R5 = 330 Ω SK data-series resistor.
- Physical SK6812 chain is `LED14+` in one serial chain; exact count/order remains open.
- Q3–Q6 phaser channels are fully defined except R6–R9 values, which depend on the exact prewired LED configuration.
- Q7/Q8/Q9 hardware implements `NFC_POWER = PERIPH_EN AND NOT WLC_PRESENT` without another MCU pin.
- MFRC522 uses only SCK/MOSI/MISO/CS; IRQ is NC; reset is supply-biased rather than MCU-controlled.
- The exact 11 functional MCU signals are now fixed for Step 6.

## Frozen architecture summary

- U1 XIAO ESP32-C3 remains permanently connected to BT1.
- RX1 wireless power feeds U1 charging/recovery through isolation and provides `WLC_PRESENT` wake/inhibit sensing.
- One `PERIPH_EN` GPIO controls the high-draw subsystem architecture.
- U2 is physically disconnected from BAT+ during sleep.
- `+5V_LIGHT_SW` powers one SK6812 serial bus, U4, and the four phaser LED branches.
- U3 MFRC522 is supplied from separately switched 3.3 V and hardware-inhibited while wireless charging is present.
- Total required U1 GPIO budget is exactly 11.
- No GPIO expander, touch module, audio, second SK6812 data bus, reed wake, or NTC monitoring is part of the frozen architecture.
- Battery protection remains mandatory; U5 is reserved/DNP unless BT1 proves unprotected.

## Open implementation checks

1. BT1 protection status.
2. Exact RX1 board/pad identity and measured output.
3. Exact U2 module/pads and 5 V load behavior.
4. Exact U3 module/header/reset behavior.
5. Prewired phaser LED electrical specification / R6–R9 value.
6. Physical SK6812 emitter count/order.
7. Final XIAO GPIO assignment and boot validation.
8. Backfeed/default-off tests.

## Drawing release criteria

The drawing gate opens only when all of the following are true:

- `POWER-ARCHITECTURE.md` remains **FROZEN**.
- `DESIGNATORS.md` remains **FROZEN**.
- `NETLIST.md` is **APPROVED**.
- `PINOUT.md` has no duplicate GPIO or boot-state conflicts.
- `CONNECTIONS.md` defines every component pin.
- `WIRE-LIST.md` covers every applicable off-board connection.
- `VALIDATION.md` has no unresolved ERROR items.
