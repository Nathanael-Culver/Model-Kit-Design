# USS Defiant — Firmware Architecture

**Document status:** BLUEPRINT ONLY / NO FINAL FIRMWARE YET

Firmware implementation begins only after the approved pin map exists.

## Required capabilities

- Wi-Fi/BLE control after hull sealing.
- OTA firmware update without routine physical USB/BOOT access.
- deep-sleep standby.
- wireless-power-present wake/recovery behavior.
- controlled switched-rail sequencing.
- nine logical addressable lighting zones P0–P8.
- four independent pulse-phaser outputs PH0–PH3.
- MFRC522 NFC support for future memory-crystal controls.
- safe fallback behavior after reset/brownout.

## Target state machine

| State | Purpose |
|---|---|
| `BOOT_SAFE` | GPIOs high impedance/default safe; detect reset cause and power conditions before enabling loads |
| `RECOVERY_CHARGE` | wireless power present with low battery/unstable supply; keep heavy lighting load disabled |
| `IDLE_CONNECTED` | radio/control available, peripherals selectively enabled |
| `SHOW` | normal lighting animation/control |
| `NFC_SCAN` | power U3, initialize reader, scan/act on memory crystal |
| `OTA` | maintain stable radio/power conditions and inhibit risky load transitions during update |
| `PRE_SLEEP` | blank phasers/LED data, shut down switched rails, configure wake source |
| `DEEP_SLEEP` | minimum standby draw |

## Startup safety sequence

1. Do not enable switched loads in static/global constructors.
2. Configure power/phaser controls to known OFF states immediately.
3. Read reset/wake cause.
4. Read wireless-power-present.
5. If supply conditions indicate recovery, enter `RECOVERY_CHARGE`.
6. Otherwise enable only the rails required for the requested mode.
7. Initialize SK6812 only after the 5 V rail and logic buffer are valid.
8. Initialize MFRC522 only after the switched 3.3 V rail is stable.

## Lighting logical API

Firmware must refer to lighting by logical names, not hard-coded physical descriptions scattered through animations:

- `P0_DEFLECTOR`
- `P1_BUSSARD_PORT`
- `P2_BUSSARD_STARBOARD`
- `P3_CHILLER_PORT`
- `P4_CHILLER_STARBOARD`
- `P5_IMPULSE_CRYSTALS_PORT`
- `P6_IMPULSE_CRYSTALS_STARBOARD`
- `P7_IMPULSE_ENGINE_PORT`
- `P8_IMPULSE_ENGINE_STARBOARD`
- `PH0`–`PH3`

The physical chain mapping must live in one configuration structure derived from the approved netlist.

## Test firmware phases

1. GPIO/default-state tester.
2. wireless-present/wake tester.
3. switched-rail tester.
4. single SK6812 + level-shifter tester.
5. full P0–P8 pixel-map tester.
6. PH0–PH3 independent output tester.
7. MFRC522 power-cycle/SPI tester.
8. integrated control/OTA test build.
9. final feature firmware.

## Configuration/source-of-truth rule

Pin numbers, pixel count/order, power-control polarity and timing constants must be centralized in one hardware configuration file under `firmware/`. Code must not duplicate electrical facts independently of `PINOUT.md` and `NETLIST.md`.
