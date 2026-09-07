# USS Defiant — Mechanical / Harness Layout

**Document status:** **CONCEPTUAL PLACEMENT FROZEN / EXACT COORDINATES AND LENGTHS OPEN**

The electrical architecture, 14-pixel lighting plan, and power-distribution strategy are now defined well enough to establish placement zones. Exact millimeter coordinates still require ruler/scale measurements of the actual opened hull.

## 1. Placement strategy

### Ventral/bottom hull

Preferred location for **RX1 receive coil**:

- coil face parallel to the charging-base surface;
- centered over a broad flat ventral region where practical;
- no copper tape, large ground plane, battery pouch, or NFC board directly behind it if avoidable;
- RX1 regulator PCB immediately adjacent to the coil rather than stacked over it.

This makes the charging stand approach from below and keeps the NFC antenna available on the opposite side of the model.

### Dorsal/top hull

Preferred location for **U3 black V602**:

- antenna face toward the top/dorsal exterior where memory crystals will be presented;
- as close to the outer plastic as practical;
- not directly overlapping RX1 coil or BT1;
- keep copper tape/foil/large wiring bundles out of the antenna footprint.

### Central electronics area

Create one **central power/control island** using solderable protoboard and the purchased SOT carriers where practical.

Preferred contents:

- Q1/Q2 + R3/R4;
- D1 + R1/R2;
- U4 + R5 + C1;
- Q3–Q6 + R10–R13;
- Q7/Q8 + R14–R16;
- R18;
- C2;
- BAT+/GND/+5V/+3V3 distribution junctions.

U2 MT3608 should sit immediately adjacent to this island so the battery/boost/high-current wiring remains short.

### U1 XIAO ESP32-C3

Place U1 near the central electronics area but orient its RF antenna toward an open hull edge/perimeter.

Avoid placing the antenna directly beneath/behind:

- BT1;
- RX1 coil;
- U3 antenna;
- broad copper-tape buses;
- large metal/foil areas.

### BT1 battery

BT1 is the largest rigid-volume item and should occupy a broad central/aft cavity where:

- the pouch lies flat;
- no mounting post or sharp edge presses into it;
- it does not need to bend;
- it does not directly overlap RX1 or U3 antenna footprints if avoidable;
- it can be restrained with padded/nonconductive material rather than hard clamping.

## 2. Lighting placement

Physical count/order is frozen in `LIGHTING-LAYOUT.md`:

- LED14 P0 deflector top
- LED15 P0 deflector bottom
- LED16 P1 port bussard
- LED17/18 P3 port chiller forward/aft
- LED19/20 P5 port impulse crystals A/B
- LED21 P7 port impulse engine
- LED22 P8 starboard impulse engine
- LED23/24 P6 starboard impulse crystals B/A
- LED25/26 P4 starboard chiller aft/forward
- LED27 P2 starboard bussard

Data route: front center -> port side -> aft cross-hull -> starboard side -> forward.

Power route is separate: front, port, and starboard power/ground branches from the central distribution area.

## 3. Phaser placement

LED10–LED13 remain four independent prewired 0805 white emitters.

- Mount each directly at its phaser aperture/light-pipe/fiber entry.
- Preserve enough factory lead length for shell movement during assembly.
- Keep R6–R9 and Q3–Q6 at the central control island unless a shorter local branch is clearly better.

## 4. Harness corridors

Plan four primary harness corridors:

1. **front corridor** — deflector LEDs and first SK6812 data entry;
2. **port corridor** — port bussard/chiller/crystals/impulse engine;
3. **starboard corridor** — starboard impulse engine/crystals/chiller/bussard;
4. **RF/power corridor** — RX1/U1/U2/BT1/U3 interconnects around the central electronics area.

Do not route wires across glue/seam lands unless there is a deliberate recessed channel.

## 5. Hull-half strategy

Because the model must be closed permanently:

- keep service slack between upper/lower hull electronics until final functional testing is complete;
- avoid connectors unless they solve a real assembly problem; every connector consumes space and creates another failure point;
- where a wire must cross between hull halves, route it through an existing internal opening or deliberate relief notch, not across a mating surface;
- perform a full dry-close with the harness installed before adhesive is applied.

## 6. Distribution / wire classes

See `POWER-DISTRIBUTION.md`.

Current design targets:

- 24 AWG preferred for the shortest main battery/boost/high-current runs;
- 26 AWG preferred for front/port/starboard lighting power trunks;
- 30 AWG for data, SPI, gates, sense and low-current 3.3 V;
- factory fine leads for phaser LEDs.

Final values depend on the actual wire inventory and measured load.

## 7. Required measurements before exact layout freeze

Capture the opened hull with a ruler or calipers and record:

- maximum usable length/width/depth of the central cavity;
- BT1 available footprint and depth;
- ventral RX1 coil mounting diameter/clearance;
- dorsal U3 footprint/clearance;
- central control-island maximum footprint;
- U2 maximum mounting envelope;
- distance from central island to front/port/starboard lighting corridors;
- seam/glue-zone widths;
- distances to every LED14–LED27 mounting site;
- usable space for wire turns and service slack.

## 8. Mounting table

| Ref/group | Preferred region | Orientation | Mount method | Status |
|---|---|---|---|---|
| RX1 coil | ventral/bottom flat hull | face toward charging base | thin nonmetallic adhesive/retainer | placement concept FROZEN; coordinates OPEN |
| RX1 PCB | adjacent to coil | flat, clear of moving/seam areas | insulated restraint | coordinates OPEN |
| U3 V602 | dorsal/top hull | antenna toward exterior | thin nonmetallic adhesive/retainer | placement concept FROZEN; coordinates OPEN |
| BT1 | central/aft cavity | flat pouch | padded restraint | coordinates OPEN |
| U1 | central/perimeter-facing | RF antenna toward open edge | insulated mount | coordinates OPEN |
| U2 | beside central control island | trimmer accessible until final set | insulated mount | coordinates OPEN |
| control island | central cavity | flat | protoboard mechanically secured | footprint OPEN |
| LED14–LED27 | feature-specific | emitter toward diffuser/light pipe | insulated strip segment mount | count/order FROZEN; coordinates OPEN |
| LED10–LED13 | phaser apertures | emitter toward light path | strain-relieved factory leads | locations functional; exact coordinates OPEN |

## 9. Copper tape

Copper tape is optional, not default.

If used, keep it out of RX1/TX1 magnetic coupling zones and out of U3's antenna footprint. Use conventional insulated wire unless tape solves a real clearance problem.

## 10. Next mechanical deliverable

The next layout freeze needs **one clear overhead photo of each open hull half with a ruler in frame**. From that, final component coordinates, W067+ power-branch IDs, wire lengths, and assembly sequence can be established without guessing.
