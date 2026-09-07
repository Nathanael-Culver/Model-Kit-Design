# USS Defiant — Test Plan

**Document status:** ACTIVE DRAFT  
**Rule:** no hull closure until every pre-close test is PASS and recorded.

## Phase 0 — identify exact hardware

- Photograph RX1 front/back and coil; record pad labels and IC marking.
- Photograph U2 MT3608 module front/back; trace/identify EN accessibility.
- Photograph U3 MFRC522 module front/back/header.
- Identify SK6812 physical package/form and direction markings.
- Measure/identify prewired 0805 LED polarity and any built-in resistor.
- Photograph carrier boards and protoboards with dimensions.

## Phase 1 — battery/XIAO baseline

1. Connect BT1 only to U1.
2. Verify normal boot.
3. Verify Wi-Fi/BLE function.
4. Measure active current.
5. Enter deep sleep and measure standby current.
6. Verify wake from a known-safe D0–D3 test input before attaching the wireless detector.

Record: battery voltage, current, firmware build, wake cause.

## Phase 2 — wireless power and recovery

1. Measure RX1 unloaded output with TX1 at several alignments/distances.
2. Load RX1 incrementally; record voltage/current/temperature.
3. Verify polarity and output pads.
4. Build the proposed isolation path to U1 external 5 V input.
5. Verify U1 can run from wireless input while BT1 is connected.
6. Verify BT1 charging behavior.
7. Verify no reverse voltage/current appears at RX1 when TX1 is absent.
8. Simulate low/depleted battery recovery and confirm wireless power restores a usable system state.

## Phase 3 — wireless-present detector

- Calculate divider/protection network.
- Measure GPIO-node voltage at minimum/nominal/maximum measured RX1 voltage.
- Confirm LOW/HIGH thresholds with margin.
- Measure detector current draw.
- Confirm chosen pin wakes U1 from deep sleep.
- Reset/power-cycle repeatedly with detector attached; verify no boot-mode failures.

## Phase 4 — switched power rails

### Lighting rail

- Inspect whether U2 EN can be used.
- Test selected EN or MOSFET gate circuit independently.
- Confirm default OFF with MCU disconnected/reset.
- Measure off-state current.
- Set output to 5.0 V before connecting LEDs.
- Load-test at expected and worst-case lighting current.
- Monitor U2 and switching-device temperature.

### NFC rail

- Verify default OFF.
- Measure off-state leakage.
- Turn on and verify stable 3.3 V at U3.
- Confirm SPI lines are not clamped when U3 is unpowered.
- Confirm power cycling reliably resets U3 if no dedicated RST GPIO is used.

## Phase 5 — logic buffer and one SK6812

1. Build one SN74AHCT1G125 on the intended carrier.
2. Add local bypass capacitor.
3. Feed 3.3 V data from U1 and power buffer at `+5V_LIGHT_SW`.
4. Verify buffer logic levels with meter/scope/logic analyzer if available.
5. Add the final series data resistor.
6. Test one SK6812 RGBW pixel at conservative brightness.
7. Verify data line remains benign when 5 V rail is off.

## Phase 6 — full P0–P8 lighting harness

After chain count is approved:

- build exact topology from `NETLIST.md`;
- verify every logical pixel P0–P8 individually;
- record physical-to-logical mapping;
- run all-white worst-case load test at an intentionally limited firmware current first;
- increase only to the final allowed brightness/current envelope;
- power-cycle repeatedly and check for random first-pixel behavior.

## Phase 7 — pulse phasers

For each PH0–PH3:

- verify LED polarity;
- determine whether prewired lead includes a resistor;
- calculate/select external current limiting if required;
- test MOSFET/default-OFF behavior;
- test static on/off;
- test intended pulse pattern/PWM;
- verify no visible glow during deep sleep/reset.

## Phase 8 — MFRC522/NFC

- read a known tag repeatedly at intended hull distance;
- test with lighting rail on/off;
- check for RF/read-range degradation from battery, copper tape, wiring, foil/light-blocking material and hull position;
- power-cycle U3 repeatedly;
- verify tag read after every cycle;
- verify no MCU boot failures with SPI wiring attached.

## Phase 9 — integrated bench harness

Run at least:

- cold boot on battery;
- cold boot on wireless power;
- battery + wireless power transition;
- deep sleep -> wireless wake;
- deep sleep -> normal wake method if implemented;
- all lighting modes;
- all four phasers independently;
- NFC reads;
- Wi-Fi/BLE control;
- OTA firmware update;
- repeated power cycles;
- sustained thermal/load test.

## Phase 10 — pre-close hull rehearsal

With all electronics installed but hull still reopenable:

- route exact harness;
- verify no pinched wires;
- verify coil alignment;
- verify NFC read distance through hull;
- verify wireless charging through final hull thickness;
- verify all lighting after light-blocking/paint;
- verify OTA again;
- photograph every component and wire ID in place;
- record final routed wire lengths.

## Phase 11 — closure acceptance

Do not close/seal until:

- all tests above PASS;
- firmware recovery/update path is proven without USB access;
- battery and electronics are mechanically secured/insulated;
- no component exceeds accepted thermal limits;
- photos and wire lengths are committed to the repository;
- a final continuity/polarity check passes immediately before power-on.
