# USS Defiant — Bench Development Layout

**Document status:** **FROZEN DEVELOPMENT SEQUENCE / PHYSICAL BREADBOARD POSITIONS FLEXIBLE**

The bench build must reproduce the final net names, reference designators, GPIO map, and power behavior without pretending the bench wiring is the final hull harness.

## 1. Bench goals

- prove each electrical subsystem before permanent installation;
- expose measurement points that will disappear after sealing;
- keep battery/boost/lighting current paths separate from fragile signal wiring;
- allow firmware/Codex development against the real final pin map;
- preserve all final reference designators.

## 2. Bench zones

Arrange the bench in six functional zones:

### Zone A — U1 controller

- U1 XIAO ESP32-C3
- USB available for initial firmware/debugging
- BT1 connection only after battery protection status is accepted
- D0–D10 labeled with their frozen functions

### Zone B — central control/power island prototype

Prototype the same circuit that will later become the hull control island:

- Q1/Q2/R3/R4
- D1/R1/R2
- U4/R5/C1
- Q3–Q6/R10–R13
- Q7/Q8/R14–R16
- R18
- C2

Use the purchased SOT carriers and solderable protoboard. Label each carrier by reference designator before soldering.

### Zone C — U2 / switched 5 V

- U2 MT3608
- input behind Q1/Q2
- output adjusted to 5.0 V before LED connection
- temporary test points for `U2_VIN_SW`, `+5V_LIGHT_SW`, and GND

### Zone D — lighting load

Begin with one complete SK6812 cut section, then expand to the final 14-pixel chain:

`LED14 -> LED15 -> ... -> LED27`

Maintain the exact frozen physical index order even on the bench so firmware mapping is tested against the final design.

Use temporary 5 V/GND distribution rails rather than forcing current through all cut sections in series.

### Zone E — phasers

- LED10–LED13
- R6–R9 = 150 Ω
- Q3–Q6
- factory LED leads may remain full length on bench

### Zone F — NFC / wireless power

- U3 black V602 on switched 3.3 V
- RX1 XKT-3168 and TX1 XKT-412 kept physically movable for alignment/coexistence testing
- keep U3 antenna and XKT coils separated at first, then move toward final-like geometry during coexistence tests

## 3. Mandatory bench test points

Use temporary labeled test leads/pads for:

- TP-BAT: `BAT+`
- TP-GND: system ground
- TP-U2VIN: `U2_VIN_SW`
- TP-5V: `+5V_LIGHT_SW`
- TP-3V3: `+3V3_ALWAYS`
- TP-NFC3V3: `+3V3_NFC_SW`
- TP-WLC: `WLC_5V_RAW`
- TP-WLCSENSE: `WLC_PRESENT`
- TP-SKRAW: `SK_DATA_RAW`
- TP-SK5V: U4 output before R5

These TP names are bench labels, not new permanent reference designators unless later promoted.

## 4. Staged build sequence

### Stage B1 — U1 only

- boot firmware;
- verify frozen GPIO constants;
- verify safe output defaults;
- verify Wi-Fi/BLE/OTA framework.

### Stage B2 — power-control island without U2/load

- Q1/Q2 default OFF;
- Q7/Q8 default OFF;
- PH0–PH3 gates default OFF;
- verify `PERIPH_EN` behavior.

### Stage B3 — U2

- connect U2 behind Q1;
- set exactly 5.0 V unloaded;
- verify OFF state when `PERIPH_EN` is LOW;
- add controlled dummy load before LEDs.

### Stage B4 — U4 + LED14

- verify boot with U4 unpowered;
- enable 5 V;
- verify one SK6812 at low brightness;
- test startup/shutdown sequencing.

### Stage B5 — full LED14–LED27 chain

- add all 14 pixels in frozen order;
- verify every physical index;
- verify P0–P8 logical mapping;
- verify global current/brightness limiter;
- record full-lighting load/temperature.

### Stage B6 — phasers

- add one channel first, then all four;
- verify default OFF and independent/sequential firing.

### Stage B7 — V602 NFC

- add Q7/Q8-switched supply and SPI;
- verify no unpowered backfeed;
- determine whether R17 is required;
- verify tag reads and UID events.

### Stage B8 — XKT charging/wake

- add RX1 -> D1 -> U1 charging/recovery path;
- add R1/R2 -> `WLC_PRESENT`;
- verify wireless wake and charging behavior;
- verify NFC coexistence while charging.

### Stage B9 — integrated endurance

Run the final firmware through:

- repeated boot/reset cycles;
- repeated deep-sleep/wake cycles;
- OTA updates;
- lighting demo loops;
- phaser sequences;
- NFC reads;
- wireless charging transitions;
- sustained thermal test.

## 5. Bench wiring rule

Bench jumpers may be longer and may use temporary connectors, but **do not create alternative GPIO assignments or different power topology**. If a test requires an electrical change, document it as a proposed engineering change rather than silently altering the final design.

## 6. Exit criteria

Bench development is complete only when:

- all 14 SK6812 pixels and all four phasers work on the final pin map;
- U3 V602 works and does not corrupt boot/deep-sleep;
- wireless charging wakes the ship and does not create unsafe/backfeed behavior;
- the firmware current/brightness cap is based on measured load;
- OTA works repeatedly;
- no subsystem depends on temporary USB/BOOT access for normal operation;
- the measured results are copied into `VALIDATION.md`/`TEST-PLAN.md` before hull installation.
