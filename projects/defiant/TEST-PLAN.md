# USS Defiant — Test Plan

**Document status:** **STEP 9 VALIDATION PLAN — ACTIVE**  
**Rule:** no schematic release until drawing blockers are closed; no hull closure until every pre-close test is PASS and recorded.

## Phase 0 — identify exact hardware before powered integration

- Photograph BT1 lead/protection end; determine whether integral cell protection is present and recover/verify discharge capability if documented.
- Photograph RX1 front/back and coil; record pad labels and IC marking.
- Photograph U2 MT3608 module front/back; record actual pad labels and dimensions. EN is not used as the primary sleep control in the frozen architecture.
- Photograph U3 MFRC522 module front/back/header and any onboard regulator/resistors.
- Identify SK6812 physical package/form, direction markings, physical emitter count, and whether each used strip/pixel section retains local bypass capacitance.
- Measure/identify one prewired 0805 LED polarity and any built-in resistor.
- Photograph SOT-23/SOT-23-5 carrier boards and protoboards with dimensions.
- Continuity-check carrier pad numbering/orientation before installing any semiconductor.

**Decision checks before final architecture release:**

- Explicitly choose whether Q9 charging-present hard NFC inhibit is KEEP or DNP.
- Explicitly accept wireless-power-present as the normal deep-sleep wake workflow, or request another wake strategy before hardware release.

## Phase 1 — battery/XIAO baseline

1. Connect only the validated/protected BT1 path to U1.
2. Verify normal boot.
3. Verify Wi-Fi/BLE function.
4. Measure active current.
5. Enter deep sleep and measure standby current.
6. Verify GPIO3/D1 wake using a known-safe 3.3 V test source before attaching RX1 divider hardware.
7. Record boot/deep-sleep current as the baseline to compare against later peripheral backfeed tests.

Record: battery voltage, current, firmware build, wake cause.

## Phase 2 — wireless receiver measurement BEFORE MCU sense connection

1. Power TX1 with the correct verified supply.
2. Measure RX1 unloaded output at several alignments/distances.
3. Record the **highest raw receiver voltage observed**.
4. Load RX1 incrementally; record voltage/current/temperature.
5. Verify output polarity and pad identity.
6. Confirm the measured raw-voltage envelope is compatible with R1/R2 before connecting `WLC_PRESENT` to U1. Recalculate the divider if required; do not connect an over-limit node to the MCU just to test it.

## Phase 3 — D1 / XIAO wireless charging and recovery

1. Build RX1 -> D1 -> U1 5 V path with appropriate copper area around D1.
2. Verify correct D1 polarity before power.
3. Verify U1 can run from wireless input while BT1 is connected.
4. Verify BT1 charging behavior.
5. Measure D1 voltage drop and temperature during simultaneous XIAO operation + charging.
6. Verify no reverse voltage/current appears at RX1 when TX1 is absent.
7. Simulate low-battery recovery and confirm wireless input returns the controller to a usable/recharge state without automatically applying full lighting load.

## Phase 4 — WLC_PRESENT detector / wake

After Phase 2 proves the raw voltage safe for the selected divider:

- build R1/R2;
- measure `WLC_PRESENT` at minimum/nominal/maximum measured RX1 voltage;
- confirm LOW/HIGH thresholds with margin;
- confirm D1/GPIO3 wakes U1 from deep sleep;
- confirm firmware does not attempt to remain in deep sleep while `WLC_PRESENT` is already HIGH unless immediate wake is intended;
- run repeated wireless-on/off wake cycles.

## Phase 5 — lighting high-side gate and MT3608

1. Build Q1/Q2/R3/R4 first without U2 load.
2. Confirm default OFF with MCU disconnected/reset.
3. Verify `PERIPH_EN` turns Q1 fully on/off.
4. Install U2 behind Q1.
5. Set U2 to 5.0 V before LEDs are attached.
6. Use a controlled/dummy load and test from realistic LiPo voltages, including the low end.
7. Measure U2 input current, output voltage, efficiency behavior where practical, and temperature.
8. Measure Q1 carrier source-to-drain voltage drop and carrier/MOSFET temperature.
9. Reinforce the Q1 carrier current path if the carrier copper is inadequate.
10. Confirm off-state current with U2 physically disconnected by Q1.

## Phase 6 — U4 logic buffer and one SK6812

1. Build U4 on the verified SOT-23-5 carrier.
2. Add C1=0.1 µF immediately adjacent to U4 VCC/GND.
3. Verify U4 pin orientation from device datasheet, not carrier silkscreen alone.
4. With `+5V_LIGHT_SW` OFF, confirm U4 does not disturb D9/GPIO9 boot behavior.
5. Cold-boot/reset U1 repeatedly with U4 attached and unpowered.
6. Set `SK_DATA_RAW` LOW before enabling the 5 V rail.
7. Enable the rail and verify 3.3 V->5 V logic translation.
8. Add R5=330 Ω and one physical SK6812 at conservative brightness.
9. Verify the pixel section has local bypass capacitance; add local ceramic bypass if it does not.
10. Power-cycle repeatedly and check for random first-pixel startup behavior.

## Phase 7 — pulse phasers

Before installing all four channels, use one actual prewired LED:

1. determine polarity electrically rather than relying only on lead color;
2. determine whether an inline/current-limiting resistor is already present;
3. measure Vf at a safe test current;
4. calculate R6–R9 or formally mark them DNP if the factory lead already contains appropriate limiting;
5. test one Q3-style channel first;
6. verify default OFF during reset/deep sleep;
7. duplicate for Q4–Q6 after the first channel passes;
8. test intended pulse sequences and verify no visible sleep/reset glow.

## Phase 8 — MFRC522 power-off / boot test BEFORE normal NFC testing

This phase is mandatory before calling the GPIO map release-safe.

1. Verify exact U3 header labels and RST/NRSTPD circuitry.
2. With U3 rail OFF and SPI physically connected, measure U3 VCC relative to GND.
3. Measure deep-sleep current and compare with the Phase-1 baseline.
4. Check whether D6/D8/D10 source current into the unpowered module.
5. Measure D0/GPIO2 while U3 is OFF and verify R18 keeps it safely high.
6. Perform at least 50 cold boot/reset cycles with U3 attached/off.
7. Perform at least 50 deep-sleep -> `WLC_PRESENT` wake cycles.
8. If U3 is back-powered or a strap pin is corrupted, stop and correct that specific interface before proceeding.

## Phase 9 — MFRC522 normal operation

After Phase 8 passes:

- power U3 through Q7/Q8 control;
- verify stable U3 supply voltage;
- verify RST/switched-power reset works every cycle;
- read a known tag repeatedly;
- verify explicitly routed SCK/MOSI/MISO/CS pins;
- test intended read distance through the hull;
- test with lighting operating;
- if Q9 is retained, verify NFC is intentionally disabled during charging;
- if Q9 is DNP, test NFC and wireless charging simultaneously for interference/read-range/thermal issues.

## Phase 10 — full SK6812 chain / power envelope

After physical count/order is known:

- assign LED14+ references and remaining W-numbers;
- verify each physical emitter and each logical P0–P8 mapping;
- verify local decoupling for every emitter/strip section;
- measure full chain current at controlled brightness levels;
- establish a safe firmware maximum brightness/current envelope;
- run all-white/RGBW worst-case tests only within the measured safe envelope;
- validate C2 bulk capacitance and 5 V rail stability;
- monitor U2, Q1, carrier, battery, wires, and LEDs for heating/voltage drop.

## Phase 11 — integrated bench harness

Run at least:

- cold boot on battery;
- cold boot on wireless power;
- battery + wireless power transition;
- deep sleep -> wireless wake;
- repeated sleep/wake cycles;
- all lighting modes;
- all four phasers independently;
- NFC reads according to the final Q9 policy;
- Wi-Fi/BLE control;
- OTA firmware update;
- repeated resets/power cycles;
- sustained thermal/load test;
- deep-sleep current measurement with every final peripheral physically attached.

## Phase 12 — pre-close hull rehearsal

With all electronics installed but hull still reopenable:

- define the final BAT+/GND/+5V/+3V3 distribution implementation;
- add W-numbers for any discrete distribution jumpers;
- route exact harness and record final lengths/gauges/colors;
- verify no pinched wires;
- verify Q1/high-current paths have adequate mechanical and electrical margin;
- verify wireless coil alignment through final hull thickness;
- verify NFC read distance and charging/NFC coexistence according to final policy;
- verify RF/Wi-Fi/BLE through the final hull;
- verify all lighting after light-blocking/paint;
- verify OTA again;
- photograph every component and wire ID in place.

## Phase 13 — closure acceptance

Do not close/seal until:

- all drawing-release validation items are PASS;
- all integrated/pre-close tests above PASS;
- firmware recovery/update path is proven without routine USB/BOOT access;
- battery and electronics are mechanically secured and insulated;
- battery, U2, Q1/carrier, D1, and other parts stay within accepted thermal limits;
- final photos and wire data are committed to the repository;
- a final continuity/polarity/short check passes immediately before power-on.
