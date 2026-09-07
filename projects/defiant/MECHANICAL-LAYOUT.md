# USS Defiant — Mechanical / Harness Layout

**Document status:** BLOCKED UNTIL ELECTRICAL SCHEMATIC APPROVAL

No final coordinates, wire lengths or adhesive placements are authoritative yet.

## Required physical measurements/photos

Capture the opened hull with a scale/ruler and identify:

- available cavity dimensions and depth by hull section;
- BT1 envelope and safe restraint area;
- RX1 receiver-board and coil dimensions;
- intended transmitter/receiver coil alignment surface and hull thickness;
- U1, U2 and U3 board dimensions including connector/header clearance;
- NFC antenna face/orientation and distance to outer hull;
- LED1–LED13 intended emitter/fiber locations;
- interior structural ribs/posts that constrain routing;
- seam/glue zones that wires must not cross;
- areas receiving conductive copper tape, foil or metallic paint;
- service/test access while the hull is still open.

## Layout priorities

1. wireless-power coil alignment and separation from conductive material;
2. battery protection and mechanical restraint;
3. NFC antenna read range and separation from metal/copper/battery where practical;
4. short, clean high-current lighting power paths;
5. short SK6812 data path from buffer to first pixel;
6. low-stress wire routes with no pinch points at hull seams;
7. access for testing before closure;
8. thermal spacing around boost converter and high-current parts.

## Harness design process

After schematic approval:

1. place components in annotated hull photos/CAD;
2. assign actual mounting locations and orientation;
3. define harness corridors;
4. map every `Wxxx` wire onto a route;
5. measure routed length from the physical hull;
6. add service/termination allowance to generate cut length;
7. commit the measurements to `WIRE-LIST.md`;
8. produce physical harness drawings from the same wire IDs.

## Mounting table

| Ref | Final location | Orientation | Mount method | Clearance/insulation | Status |
|---|---|---|---|---|---|
| U1 | TBD | TBD | TBD | antenna/OTA RF clearance required | OPEN |
| BT1 | TBD | TBD | TBD | protect pouch from compression/sharp edges | OPEN |
| RX1 | TBD | coil face aligned to charging surface | TBD | keep conductive materials clear until tested | OPEN |
| U2 | TBD | TBD | TBD | thermal/load test required | OPEN |
| U3 | TBD | antenna toward intended crystal approach surface | TBD | RF range test through hull required | OPEN |
| U4+ | TBD | near first SK6812 data entry preferred | carrier/protoboard TBD | local bypass capacitor | OPEN |
| LED1–LED13 | TBD from lighting geometry | TBD | TBD | light blocking/diffusion/fiber as applicable | OPEN |
