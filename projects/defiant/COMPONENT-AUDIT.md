# USS Defiant — Component Audit

**Status:** engineering review baseline  
**Purpose:** determine whether the purchased component plan should be kept, modified, or replaced before architecture freeze.

## Executive conclusion

The existing component plan is fundamentally sound. No controller replacement, GPIO expander, alternate LED architecture, or major subsystem redesign is currently justified.

The preferred baseline is:

- XIAO ESP32-C3 remains the sole controller.
- All nine SK6812 RGBW pixels use one serial data line unless physical hull routing later proves that impractical.
- Four prewired white phaser LEDs remain four independent non-addressable channels.
- AO3400A devices provide the four phaser low-side switches and may also be used as helper/gate-driver devices where needed.
- AO3401A devices provide high-side power switching where true load disconnect is required.
- SN74AHCT1G125 provides the 3.3 V-to-5 V SK6812 data translation.
- MT3608 remains the 5 V lighting boost converter.
- MFRC522 remains the NFC reader.
- XKT wireless-power hardware remains the charging/recovery system.

The main work still required is verification and exact implementation, not replacement of the major components.

## Component-by-component audit

| Component | Verdict | Recommended role / action | Remaining verification |
|---|---|---|---|
| Seeed Studio XIAO ESP32-C3 | **KEEP** | Master MCU; Wi-Fi/BLE, OTA, deep sleep, SK6812 control, phasers, NFC, wake/power control | Final GPIO map and boot-state validation |
| 103450 3.7 V 2500 mAh LiPo | **KEEP** | Main internal battery permanently connected to XIAO battery input | Confirm whether exact pack includes hardware protection PCB; confirm fit/mounting |
| XKT-412 transmitter | **KEEP** | External wireless-power transmitter | Confirm actual supply requirements and coil alignment during bench test |
| Matching XKT receiver / apparent XKT-3168 | **KEEP** | Wireless charging/recovery input and wireless-power-present source | Photograph exact board/pads; load-test real output; do not rely blindly on seller 5 V/2 A claim |
| MT3608 boost module | **KEEP** | Generate switched 5 V lighting rail from LiPo | Identify exact module; measure load capability; prefer true input power-gating if EN alone does not fully isolate the output/load path |
| MFRC522 module | **KEEP** | NFC memory-crystal reader | Identify exact breakout; measure sleep/power-down current; decide between its hardware power-down function and external high-side power gate |
| 9 x SK6812 RGBW | **KEEP** | Nine individually addressable lighting zones on one serial data line | Confirm exact physical package/form and final physical chain order |
| 4 x prewired 0805 white LEDs | **KEEP** | Four independent pulse-phaser channels | Verify polarity, forward voltage, target current, and whether the leads already contain series resistance |
| AO3400A N-MOSFET | **KEEP** | Four phaser low-side switches; helper/gate-driver duties if needed | Assign exact Q designators after architecture freeze; verify gate pull/default-off network |
| AO3401A P-MOSFET | **KEEP** | High-side power/load switching where true rail isolation is required | Assign exact gate topology and Q designators after rail architecture is frozen |
| SN74AHCT1G125DBVR | **KEEP** | 3.3 V XIAO data -> 5 V SK6812 data buffer; one device needed for a one-chain design | Add local bypass capacitor; determine OE treatment; mount on SOT-23-5 carrier |
| PMEG2010ER Schottky | **KEEP** | Candidate isolation/protection diode in wireless-input/XIAO power path | Freeze exact placement and polarity after wireless power bench test |
| MDSR-10 reed switch | **NOT REQUIRED CURRENTLY** | Keep as inventory; do not add to Defiant without a specific function | None unless a later magnetic-control requirement is intentionally added |
| 10 kΩ NTC | **NOT REQUIRED CURRENTLY** | Keep as inventory; optional future temperature monitoring only | No need to spend GPIO/ADC resources unless thermal testing reveals a real need |
| SOT-23 / SOT-23-5 carrier boards | **KEEP** | Adapt purchased SMD MOSFETs/buffer for hand assembly | Verify exact footprint orientation before soldering |
| Solderable prototyping boards | **KEEP** | Bench development and possibly final small carrier sections if they physically fit | Final model should use only as much board area as needed |
| Resistors/capacitors | **KEEP / VERIFY VALUES** | Data series resistor, MOSFET gate pulls, wireless-present divider, IC bypassing, rail bulk capacitance, LED current limiting as required | Reconstruct actual inventory; calculate exact values rather than inheriting conflicting old drafts |
| Hookup wire | **KEEP** | Power, signal and LED harness | Record available colors/gauges; choose gauge by actual current/path rather than blanket rule |
| Copper tape | **OPTIONAL** | Space-saving power/ground distribution only where mechanically useful | Avoid near NFC antenna/wireless charging coil until tested; do not use merely because it is available |

## Recommended architecture after audit

No additional GPIO expander is recommended.

### Addressable lighting

The nine SK6812 pixels should be treated as **one addressable data chain** unless hull routing later creates a compelling mechanical reason to split it. Nine logical lighting zones therefore consume one XIAO GPIO, not nine.

### Phaser lighting

The four prewired 0805 white LEDs remain ordinary independent channels. Each should use its own AO3400A low-side switching channel so PH0–PH3 can fire independently.

### Lighting power

The MT3608 remains the 5 V lighting converter. The final sleep architecture should provide a genuinely dead lighting subsystem. If the exact purchased MT3608 module does not provide acceptable true load isolation through its EN implementation, use the already-purchased AO3401A/AO3400A devices to gate its battery input rather than replacing the converter.

### NFC power

Keep the MFRC522. First test the exact breakout's hardware power-down/sleep consumption. If sufficiently low, use the MFRC522's own power-down/reset mechanism and avoid an unnecessary external rail switch. If the breakout wastes meaningful standby current, use an AO3401A high-side switch. This is a bench-test decision, not a component-replacement decision.

### SK6812 data translation

Use one SN74AHCT1G125 for the single data chain. Power it from the switched 5 V lighting rail and provide local decoupling. This keeps the buffer off whenever the lighting rail is physically off.

### Wireless power

Retain the XKT hardware. The receiver must be characterized under the actual coil spacing and representative load before its seller current rating is used in any power budget. Use the receiver output both for the charging/recovery path and, through a safe divider/protection network, for the wireless-present wake signal.

## Items that may still require purchase

No additional active IC is currently justified.

Possible small passive/protection purchases depend on what is already on hand:

- 0.1 uF ceramic capacitor(s) for local logic decoupling;
- appropriate resistor values for MOSFET gate pulls and wireless-present voltage divider;
- exact phaser current-limiting resistors if the prewired LEDs do not already include them;
- final 5 V bulk capacitor value after load testing;
- a tiny 1-cell LiPo protection board **only if** the exact battery is confirmed to be an unprotected cell.

## Audit decision

**KEEP THE EXISTING CORE PARTS.**

The better path is to finish identifying and characterizing the exact modules, then freeze the architecture. The project does not currently need another controller, GPIO expander, alternate wireless-power system, alternate LED controller, or new NFC technology.
