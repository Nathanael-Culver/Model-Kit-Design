# USS Defiant — Test Plan

**Document status:** **STEP 9 VALIDATION PLAN — ACTIVE / POLICY DECISIONS CLOSED**  
**Rule:** no schematic release until drawing blockers are closed; no hull closure until every pre-close test is PASS and recorded.

## Approved policy baseline

- Q9 is **DNP**; NFC is allowed while wireless charging is active.
- `WLC_PRESENT` on U1 D1/GPIO3 is the **normal v1 deep-sleep wake source**.
- Wi-Fi/BLE/NFC are not deep-sleep wake sources; they become available after wireless-power wake.

## Phase 0 — identify exact hardware before powered integration

- Photograph BT1 lead/protection end; determine whether integral cell protection is present and verify discharge capability if documented.
- Photograph RX1 front/back/coil; record pad labels and IC marking.
- Photograph U2 MT3608 front/back; record pads/dimensions.
- Photograph U3 MFRC522 front/back/header and onboard regulator/resistors.
- Identify SK6812 form, direction, physical count, and local bypass capacitance.
- Measure/identify one prewired 0805 LED polarity and built-in resistor status.
- Photograph/continuity-map SOT-23/SOT-23-5 carriers and protoboards.

## Phase 1 — battery/XIAO baseline

1. Connect only validated/protected BT1 path to U1.
2. Verify normal boot and Wi-Fi/BLE.
3. Measure active current.
4. Enter deep sleep and measure standby current.
5. Verify GPIO3/D1 wake with a safe 3.3 V source before RX1 divider hardware.
6. Record boot/deep-sleep baseline current, battery voltage, firmware build, and wake cause.

## Phase 2 — RX1 measurement before MCU sense connection

1. Power TX1 with verified supply.
2. Measure RX1 unloaded output at several alignments/distances.
3. Record highest raw receiver voltage.
4. Load RX1 incrementally; record voltage/current/temperature.
5. Verify polarity/pads.
6. Confirm measured voltage envelope is compatible with R1/R2 before connecting `WLC_PRESENT` to U1.

## Phase 3 — D1 / XIAO charging and recovery

1. Build RX1 -> D1 -> U1 5 V path with appropriate copper area.
2. Verify D1 polarity.
3. Verify U1 can run while BT1 is connected and wireless input is present.
4. Verify BT1 charging behavior.
5. Measure D1 drop/temperature during run + charge.
6. Verify no reverse voltage/current at RX1 with TX1 absent.
7. Simulate low-battery recovery without automatically applying full lighting load.

## Phase 4 — WLC_PRESENT / approved wake workflow

After RX1 voltage is proven safe:

- build R1/R2;
- measure `WLC_PRESENT` at measured min/nominal/max RX1 voltage;
- confirm GPIO thresholds with margin;
- confirm D1/GPIO3 wakes U1 from deep sleep;
- verify the normal workflow: **sleeping ship -> apply/enable charging field -> ship wakes**;
- run at least 50 wireless-on/off deep-sleep wake cycles;
- verify Wi-Fi/BLE/NFC become available after wake;
- ensure firmware does not create an immediate sleep/wake loop while `WLC_PRESENT` remains HIGH.

There is intentionally no Wi-Fi/BLE/NFC deep-sleep wake test in v1.

## Phase 5 — lighting high-side gate / MT3608

1. Build Q1/Q2/R3/R4 without load.
2. Confirm hardware default OFF with MCU reset/disconnected.
3. Verify `PERIPH_EN` controls Q1 cleanly.
4. Install U2 behind Q1.
5. Set U2 to 5.0 V before LEDs.
6. Dummy-load at realistic LiPo voltages, including low battery.
7. Measure input current/output voltage/temperature.
8. Measure Q1 carrier voltage drop/temperature.
9. Reinforce carrier current path if required.
10. Confirm off-state current with Q1 open.

## Phase 6 — U4 and one SK6812

1. Build U4 on verified carrier.
2. Add C1=0.1 µF at VCC/GND.
3. Verify carrier orientation against datasheet.
4. With +5 V rail OFF, confirm U4 does not disturb D9/GPIO9 boot.
5. Perform repeated cold boots/resets with U4 attached/off.
6. Set `SK_DATA_RAW` LOW before enabling 5 V.
7. Verify 3.3 V -> 5 V translation.
8. Add R5=330 Ω and one SK6812 at conservative brightness.
9. Verify local pixel bypass capacitance.
10. Check for startup glitches.

## Phase 7 — pulse phasers

Using one actual prewired LED first:

1. determine polarity electrically;
2. determine whether inline resistance exists;
3. measure Vf at safe test current;
4. calculate R6–R9 or mark DNP;
5. test one Q3-style channel;
6. verify default OFF during reset/deep sleep;
7. duplicate for Q4–Q6;
8. test intended pulse sequences/no sleep glow.

## Phase 8 — MFRC522 power-off / boot test

1. Verify exact U3 header and RST/NRSTPD circuitry.
2. With U3 OFF and SPI connected, measure U3 VCC.
3. Compare deep-sleep current with Phase-1 baseline.
4. Check whether D6/D8/D10 source current into unpowered U3.
5. Verify R18 holds D0/GPIO2 safely high.
6. Perform at least 50 cold boot/reset cycles with U3 attached/off.
7. Perform at least 50 deep-sleep -> WLC_PRESENT wake cycles.
8. Stop and correct the specific interface if U3 back-powers or corrupts boot.

## Phase 9 — MFRC522 normal operation and charging coexistence

After Phase 8 passes:

- power U3 through Q7/Q8;
- verify stable supply and switched-power reset;
- read a known tag repeatedly;
- verify explicit SPI pins;
- test intended hull read distance;
- test with lighting operating.

### Required Q9-DNP coexistence test

1. verify **no Q9/W013/W053 inhibit connection is fitted**;
2. measure baseline NFC read distance/reliability with TX1 OFF;
3. activate wireless charging at final-like coil alignment;
4. repeat NFC reads at multiple tag positions/orientations;
5. record any change in read distance, reliability, RX1/U3 temperature, or instability;
6. add interference mitigation only if measured performance is unacceptable.

## Phase 10 — full SK6812 chain / power envelope

- assign LED14+ refs and remaining W-numbers;
- verify physical emitters and P0–P8 mapping;
- verify local decoupling;
- measure chain current at controlled brightness;
- set safe firmware brightness/current envelope;
- validate C2 and 5 V stability;
- monitor U2/Q1/carrier/battery/wires/LED temperatures.

## Phase 11 — integrated bench harness

Run at least:

- battery cold boot;
- boot with wireless power present;
- battery/wireless transitions;
- deep sleep -> wireless wake;
- repeated sleep/wake cycles;
- all lighting/phaser modes;
- NFC with charging OFF and ON;
- Wi-Fi/BLE control;
- OTA;
- repeated resets/power cycles;
- sustained thermal/load test;
- final deep-sleep current with all peripherals attached.

## Phase 12 — pre-close hull rehearsal

- define final BAT+/GND/+5V/+3V3 distribution;
- assign W-numbers to new distribution jumpers;
- route/measure final harness;
- verify no pinched wires;
- verify high-current path margin;
- verify charging through final hull;
- verify NFC through hull with charging OFF and ON;
- verify RF/Wi-Fi/BLE;
- verify lighting after light-blocking/paint;
- verify OTA again;
- photograph every installed component/wire ID.

## Phase 13 — closure acceptance

Do not seal until all drawing-release and pre-close tests pass, OTA/recovery works without routine USB/BOOT access, battery/electronics are secured/insulated, thermal limits are acceptable, final photos/wire data are committed, and final continuity/polarity/short checks pass.