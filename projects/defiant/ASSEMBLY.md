# USS Defiant — Assembly Sequence

**Document status:** **FROZEN PROCESS ORDER / exact adhesives and wire lengths still open**

This sequence is designed for a permanently sealed model where electronics cannot be serviced physically after closure.

## 1. Before permanent installation

1. Finish textual electrical/harness design and physical placement plan.
2. Build the staged bench harness from `bench/BENCH-LAYOUT.md`.
3. Complete required electrical/firmware validation in `TEST-PLAN.md`.
4. Verify OTA works repeatedly without USB/BOOT access.
5. Verify all 14 SK6812 pixels, four phasers, V602 NFC, wireless wake/charging, Wi-Fi/BLE and deep sleep.

## 2. Interior preparation

Before electronics obscure the plastic:

1. clean interior surfaces;
2. mask optical windows/light pipes that must remain clear;
3. apply interior light-blocking coat(s);
4. add reflective/light-diffusing treatment where useful;
5. leave adhesive/electronics mounting pads clean where paint would reduce bond strength;
6. verify all optical openings before installing electronics.

Do not use conductive metallic paint/foil/copper in RX1/U3 antenna areas without validated clearance.

## 3. Dry placement

1. place RX1 coil on the ventral charging surface;
2. place U3 V602 on the dorsal memory-crystal side;
3. place BT1, U1, U2 and the central control island;
4. place LED14–LED27 and LED10–LED13 at their optical features;
5. route temporary harness paths;
6. dry-close both hull halves;
7. correct every interference/pinch point before soldering final-length harnesses.

## 4. Final harness fabrication

1. assign W067+ to the final physical +5V/GND/distribution branches;
2. measure routed lengths from the actual hull;
3. add deliberate service/termination allowance;
4. cut/strip/tin wires according to `WIRE-LIST.md`;
5. build the central control island and U2 high-current path;
6. build front/port/starboard lighting power branches;
7. build SK6812 data chain W054–W066;
8. continuity/polarity-check every connection before applying power.

## 5. Installed-but-reopenable validation

Install electronics without permanently sealing the hull.

Verify:

- battery operation;
- wireless charging and wake;
- deep-sleep current;
- all 14 addressable pixels and logical-zone mapping;
- all four phasers;
- V602 NFC through actual hull plastic;
- NFC while charging;
- Wi-Fi/BLE control;
- OTA;
- repeated reset/sleep/wake cycles;
- thermal behavior;
- no light leaks requiring inaccessible interior correction.

## 6. Permanent securing

Only after installed-position tests pass:

1. secure BT1 with padded/noncompressive restraint;
2. secure RX1/U3/U1/U2/control island;
3. secure LED strip sections and phaser leads;
4. add strain relief to soldered flexible-strip pads;
5. insulate exposed copper/carrier pads;
6. secure harnesses away from seams/posts/sharp edges;
7. photograph the complete installed electronics with reference designators/wire IDs visible where possible.

## 7. Pre-close acceptance

Repeat the full final test set immediately before adhesive:

- continuity/short check;
- battery voltage and polarity;
- wireless charging/wake;
- lighting/phasers;
- NFC;
- Wi-Fi/BLE;
- OTA;
- deep sleep;
- dry-close one final time.

## 8. Hull closure

1. route service slack into safe cavities;
2. ensure no conductor crosses a mating/glue surface;
3. close and clamp the hull without adhesive first;
4. run a final powered functional check while clamped;
5. only then apply/complete permanent seam bonding.

## 9. Exterior finishing

After electronics are permanently enclosed and hull seams are structurally finished:

1. seam fill/sand;
2. exterior primer;
3. base colors;
4. detail painting;
5. clear coats/decals/weathering as appropriate;
6. final finish coat.

Protect illuminated clear parts and charging/NFC interaction areas from coatings that would impair their function.

## 10. Final acceptance

After exterior finishing:

- verify wireless wake/charging;
- verify all P0–P8 zones;
- verify PH0–PH3;
- verify V602 memory-crystal reads;
- verify Wi-Fi/BLE/web control;
- perform at least one OTA update or OTA validation cycle;
- run the normal demo/show mode and confirm no new thermal or optical issues.

The project is complete only after this final acceptance passes.
