# USS Defiant — Physical Lighting Layout

**Document status:** **FROZEN v1.0 — physical emitter count and data-chain order**  
**Source:** accepted P0–P8 logical-zone design, reconstructed earlier 14-pixel working concept, current BTF-LIGHTING SK6812 RGBW strip, and current low-count/realistic-lighting design goal.

## 1. Frozen result

The Defiant uses **14 physical SK6812 RGBW emitters** on **one serial data bus**, mapped into the existing **9 logical zones P0–P8**.

This is intentionally not 9 physical pixels. Single compact features use one emitter; paired or elongated features use two emitters where one pixel would produce visibly uneven illumination.

## 2. Logical-zone emitter counts

| Zone | Feature | Physical emitters | Reason |
|---|---|---:|---|
| P0 | deflector, top + bottom combined | 2 | one for each visible top/bottom optical feature; firmware controls both as one zone |
| P1 | port bussard | 1 | compact feature |
| P2 | starboard bussard | 1 | compact feature |
| P3 | port warp chiller/grille | 2 | elongated illuminated feature; forward + aft coverage |
| P4 | starboard warp chiller/grille | 2 | elongated illuminated feature; forward + aft coverage |
| P5 | port impulse crystals | 2 | two physical crystals; controlled together |
| P6 | starboard impulse crystals | 2 | two physical crystals; controlled together |
| P7 | port impulse engine | 1 | compact optical feature |
| P8 | starboard impulse engine | 1 | compact optical feature |
|  | **Total** | **14** |  |

## 3. Frozen physical data-chain order

The data chain follows a single snake route intended to minimize long cross-hull data jumps:

1. central deflector area;
2. down the port side toward the aft hull;
3. one aft cross-hull transition;
4. forward along the starboard side.

| Ref | Chain index | Logical zone | Physical feature |
|---|---:|---|---|
| LED14 | 0 | P0 | deflector — top |
| LED15 | 1 | P0 | deflector — bottom |
| LED16 | 2 | P1 | port bussard |
| LED17 | 3 | P3 | port warp chiller — forward |
| LED18 | 4 | P3 | port warp chiller — aft |
| LED19 | 5 | P5 | port impulse crystal — forward / A |
| LED20 | 6 | P5 | port impulse crystal — aft / B |
| LED21 | 7 | P7 | port impulse engine |
| LED22 | 8 | P8 | starboard impulse engine |
| LED23 | 9 | P6 | starboard impulse crystal — aft / B |
| LED24 | 10 | P6 | starboard impulse crystal — forward / A |
| LED25 | 11 | P4 | starboard warp chiller — aft |
| LED26 | 12 | P4 | starboard warp chiller — forward |
| LED27 | 13 | P2 | starboard bussard |

Final DOUT of LED27 is NC unless a deliberate test point is later added.

## 4. Frozen firmware mapping

```text
P0_DEFLECTOR                 = [0, 1]
P1_BUSSARD_PORT              = [2]
P2_BUSSARD_STARBOARD         = [13]
P3_CHILLER_PORT              = [3, 4]
P4_CHILLER_STARBOARD         = [11, 12]
P5_IMPULSE_CRYSTALS_PORT     = [5, 6]
P6_IMPULSE_CRYSTALS_STARBOARD= [9, 10]
P7_IMPULSE_ENGINE_PORT       = [7]
P8_IMPULSE_ENGINE_STARBOARD  = [8]
```

Firmware must use this mapping layer rather than assuming a logical zone number equals a physical pixel index.

## 5. Data wiring

- U1 D9/GPIO9 -> U4 -> R5 -> LED14 DIN.
- Each emitter DOUT goes only to the next emitter DIN in the table above.
- Data does not branch.
- Inter-emitter data wires are W054–W066 in `WIRE-LIST.md`.

## 6. Power distribution rule

The **data bus is daisy chained; power is not required to be**.

Do not route the full lighting current through a long sequence of tiny cut-strip copper pads if a lower-resistance parallel distribution is practical. `+5V_LIGHT_SW` and GND may be distributed as trunks/branches to the physical pixel groups while the data line remains serial.

Final power/ground branch geometry and wire lengths depend on actual hull placement and are assigned during mechanical/harness layout.

## 7. Strip cutting / mounting rule

For every physical emitter:

- retain the complete BTF-LIGHTING manufacturer-defined cuttable pixel section;
- retain its local SMD support/decoupling components;
- verify DIN/DOUT arrow direction before soldering;
- electrically insulate the rear/cut copper pads from metallic paint, copper tape, foil, or conductive structure;
- provide strain relief so fine data wires do not load the flexible-strip pads.

## 8. Power-envelope policy

The exact current of the installed 14-pixel set will be measured later. Until that measurement exists:

- firmware must support a configurable global brightness/current limit;
- bench testing begins at conservative brightness;
- all-pixels-full-output is not an assumed normal operating mode;
- final MT3608/Q1/battery/wire thermal acceptance uses measured integrated load, not a seller headline current rating.

C2 remains a **470 µF target** until integrated 5 V rail behavior is observed with all 14 pixels.

## 9. What remains mechanical, not electrical

Frozen here:

- 14 physical pixels;
- LED14–LED27 reference designators;
- logical-zone membership;
- serial data order.

Still to establish from the actual hull:

- exact millimeter coordinates/orientation;
- which hull half each emitter mounts to;
- exact diffuser/light-pipe relationship;
- power/ground branch points;
- wire gauge, color, and cut length;
- adhesive/strain-relief method.

These mechanical details may alter wire lengths/routing but must not silently change the frozen logical map or physical emitter count.
