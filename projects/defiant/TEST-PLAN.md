# USS Defiant — Test Plan

**Document status:** **ACTIVE — architecture, U3 selection, wireless module IDs, and 14-pixel lighting layout frozen**  
**Rule:** no hull closure until every pre-close test is PASS and recorded.

## Approved baseline

- Q9 is DNP; NFC is allowed while wireless charging is active.
- `WLC_PRESENT` on U1 D1/GPIO3 is the normal v1 deep-sleep wake source.
- Wi-Fi/BLE/NFC are not deep-sleep wake sources.
- U3 is the black XFW-ETLIVE V602.
- TX1 = XKT-412; RX1 = XKT-3168.
- Addressable lighting = **14 physical SK6812 RGBW pixels, LED14–LED27**, mapped to 9 logical zones.
- Bench arrangement follows `bench/BENCH-LAYOUT.md`.

## Phase 0 — remaining nonpowered physical checks

- determine BT1 integral-protection status;
- continuity-map SOT-23/SOT-23-5 carriers before soldering;
- inventory actual wire gauges/colors and passive stock;
- measure hull/component locations for final W067+ distribution branches and wire lengths.

The SK6812 count/order and major module identities are no longer Phase-0 unknowns.

## Phase 1 — U1 baseline

1. power U1 from a validated/protected battery path or suitable bench source;
2. verify normal boot and frozen GPIO mapping;
3. verify Wi-Fi/BLE/OTA framework;
4. measure active current;
5. enter deep sleep and measure baseline standby current;
6. verify D1/GPIO3 wake behavior with a safe logic source before integrated wireless test;
7. record firmware build and wake cause.

## Phase 2 — default-off control island

1. build Q1/Q2/R3/R4 without U2 load;
2. build Q7/Q8/R14–R16 without U3;
3. build Q3–Q6 gate networks without LEDs;
4. confirm all switched loads are hardware-default OFF with U1 reset/disconnected;
5. verify `PERIPH_EN` controls Q1/Q7 paths as intended.

## Phase 3 — U2 / switched 5 V

1. install U2 behind Q1;
2. set U2 to 5.0 V before connecting LEDs;
3. verify Q1 OFF state removes U2 input power;
4. dummy-load at realistic battery voltages;
5. record input/output current, voltage and temperature;
6. record Q1 carrier drop/temperature;
7. reinforce current path only if measurements justify it.

## Phase 4 — U4 + one SK6812

1. continuity-check U4 carrier orientation;
2. install U4 + C1=0.1 µF + R5=330 Ω;
3. with +5 V rail OFF, verify U4 does not disturb D9/GPIO9 boot;
4. perform repeated cold boots/resets;
5. enable 5 V and verify level translation;
6. connect LED14 only at conservative brightness;
7. confirm correct DIN/DOUT orientation and no startup glitch.

## Phase 5 — full LED14–LED27 chain

Build in the exact frozen order from `LIGHTING-LAYOUT.md`:

`LED14 -> LED15 -> ... -> LED27`

Then:

1. verify all 14 physical indices individually;
2. verify P0–P8 logical grouping exactly;
3. verify top/bottom deflector act together as P0;
4. verify paired chillers/crystals act as their logical zones;
5. exercise fades/animations without blocking behavior;
6. measure current at several controlled global brightness levels;
7. establish and record the final firmware current/brightness cap;
8. validate C2/5 V rail stability;
9. monitor U2/Q1/battery/wiring/LED temperatures.

## Phase 6 — pulse phasers

R6–R9 are frozen at 150 Ω >=1/8 W.

1. determine one DiCUNO LED's polarity electrically;
2. connect through 150 Ω from controlled 5.0 V;
3. verify approximate 11–15 mA behavior;
4. test one Q3-style switch channel;
5. verify reset/deep-sleep default OFF;
6. duplicate for Q4–Q6;
7. test independent, sequential, burst and all-phaser patterns.

## Phase 7 — V602 power-off / boot test

1. confirm U3 header order;
2. connect SPI and switched-power circuitry;
3. leave U3 rail OFF and measure U3 3V3 relative to GND;
4. compare deep-sleep current with Phase-1 baseline;
5. check D6/D8/D10 backfeed into U3;
6. verify R18 holds D0/GPIO2 safely high;
7. perform at least 50 cold boot/reset cycles;
8. determine whether R17 is required;
9. stop and correct the interface if U3 back-powers or corrupts boot.

## Phase 8 — V602 normal operation

1. power U3 through Q7/Q8;
2. verify stable switched 3.3 V;
3. read a known tag repeatedly;
4. record UID and firmware/version register if available;
5. test intended read distance/orientation;
6. test with lighting operating.

## Phase 9 — integrated XKT / charging / wake

The XKT pair is treated as the selected 5 V / 2 A hardware. Characterization happens here rather than blocking design work.

1. confirm RX1 red/black polarity before permanent connection;
2. observe unloaded/loaded receiver voltage at final-like alignment;
3. connect RX1 -> D1 -> U1 charging/recovery path;
4. verify charge/run behavior and D1 temperature/drop;
5. verify no reverse feed toward RX1 with TX1 absent;
6. connect R1/R2 `WLC_PRESENT` path;
7. verify D1/GPIO3 wake;
8. run at least 50 deep-sleep -> wireless-wake cycles;
9. ensure firmware does not sleep/wake-loop while charging remains present;
10. record coil alignment sensitivity and heating.

## Phase 10 — NFC while charging

1. establish baseline V602 read reliability with TX1 OFF;
2. enable wireless charging at final-like geometry;
3. repeat reads at multiple tag positions/orientations;
4. record any read-distance/reliability change;
5. monitor U3/RX1 temperature and instability;
6. add mitigation only if a measured problem exists.

## Phase 11 — integrated bench endurance

Run:

- battery cold boot;
- boot with wireless power present;
- battery/wireless transitions;
- repeated deep sleep/wake;
- all 14-pixel lighting modes;
- all phaser modes;
- NFC with charging OFF and ON;
- Wi-Fi/BLE control;
- OTA;
- repeated reset/power cycles;
- sustained thermal/load test;
- final deep-sleep current with all peripherals attached.

## Phase 12 — pre-close hull rehearsal

- place components per `MECHANICAL-LAYOUT.md`;
- build final front/port/starboard power branches from `POWER-DISTRIBUTION.md`;
- assign W067+ and measure final harness lengths;
- verify no pinched wires or seam crossings;
- dry-close the hull;
- verify charging through hull;
- verify V602 through hull with charging OFF and ON;
- verify Wi-Fi/BLE;
- verify lighting after interior light blocking/paint;
- verify OTA again;
- photograph every installed component/wire ID.

## Phase 13 — closure acceptance

Do not seal until:

- all release blockers are PASS;
- OTA/recovery works without routine USB/BOOT access;
- battery/electronics are secured and insulated;
- thermal limits are acceptable;
- final photos/wire data are committed;
- final continuity/polarity/short checks pass.
