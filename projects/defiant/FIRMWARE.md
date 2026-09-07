# USS Defiant — Firmware Architecture

**Document status:** BLUEPRINT / authoritative hardware-policy notes current through Step 9

## Required capabilities

- Wi-Fi/BLE control after hull sealing.
- OTA firmware update without routine physical USB/BOOT access.
- deep-sleep standby.
- wireless-power-present wake/recovery behavior.
- controlled switched-rail sequencing.
- nine logical addressable lighting zones P0–P8.
- four independent pulse-phaser outputs PH0–PH3.
- MFRC522 NFC support for memory-crystal controls.
- safe fallback behavior after reset/brownout.

## Approved wake policy

For v1, `WLC_PRESENT` on U1 D1/GPIO3 is the **normal deep-sleep wake source**.

While U1 is in deep sleep:

- Wi-Fi is off;
- BLE is off;
- MFRC522 is power-gated off;
- therefore Wi-Fi/BLE/NFC cannot wake the model.

Normal user workflow is to apply/enable the wireless charging field, which wakes U1. Once awake, Wi-Fi/BLE/NFC controls become available.

Do not add timer wake, reed wake, touch wake, or another wake path without an approved hardware/firmware change.

## NFC while charging policy

Q9 is DNP. Firmware must **not** treat `WLC_PRESENT` as a mandatory NFC-disable signal.

NFC may operate while wireless charging is active. Bench validation must test read range/reliability in that condition. If actual interference is observed, report and mitigate the measured problem rather than assuming charging and NFC are incompatible.

## Target state machine

| State | Purpose |
|---|---|
| `BOOT_SAFE` | force safe outputs; inspect reset/wake/power state before loads |
| `RECOVERY_CHARGE` | charging present with low/unstable battery; keep heavy lighting conservative/off |
| `IDLE_CONNECTED` | radio/control available |
| `SHOW` | lighting/effects operation |
| `NFC_SCAN` | power U3, initialize reader, scan/act on memory crystal; allowed while charging |
| `OTA` | maintain stable power/radio and safe load behavior during update |
| `PRE_SLEEP` | blank outputs, shut switched rails, configure WLC wake |
| `DEEP_SLEEP` | minimum standby draw; wait for WLC_PRESENT wake |

## Startup safety sequence

1. configure power/phaser outputs safely before enabling loads;
2. hold `PERIPH_EN` LOW initially;
3. drive `SK_DATA_RAW` LOW before lighting rail enable;
4. read reset/wake cause and `WLC_PRESENT`;
5. enter recovery mode when supply/battery conditions require it;
6. enable only needed rails after safe initialization;
7. initialize SK6812 only after 5 V rail/U4 are valid;
8. initialize MFRC522 only after +3V3_NFC_SW is stable.

## Pre-sleep sequence

1. turn all logical lighting zones off;
2. turn PH0–PH3 off;
3. drive `SK_DATA_RAW` LOW;
4. shut down/stop NFC activity;
5. put SPI outputs into a benign state that cannot back-power U3;
6. deassert `PERIPH_EN`;
7. verify switched rails collapse where practical;
8. configure D1/GPIO3 `WLC_PRESENT` as wake source;
9. enter deep sleep.

Firmware should avoid entering deep sleep while `WLC_PRESENT` is already HIGH unless immediate/repeated wake is intentionally handled.

## Lighting logical API

Use logical names rather than scattered physical indices:

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

Physical SK6812 mapping belongs in one configuration structure.

## Frozen GPIO constants

Firmware `hardware_config.h` must use ESP32-C3 GPIO numbers:

```cpp
PIN_NFC_MISO    = 2;
PIN_WLC_PRESENT = 3;
PIN_PH0         = 4;
PIN_PH1         = 5;
PIN_PH2         = 6;
PIN_PH3         = 7;
PIN_NFC_CS      = 21;
PIN_PERIPH_EN   = 20;
PIN_NFC_SCK     = 8;
PIN_SK_DATA     = 9;
PIN_NFC_MOSI    = 10;
```

Explicitly configure MFRC522 SPI routing; do not assume default Arduino SPI pins.

## Test firmware phases

1. GPIO/default-state test.
2. WLC_PRESENT voltage/wake test.
3. switched-rail test.
4. one SK6812 + U4 test.
5. full physical-to-logical lighting-map test.
6. PH0–PH3 test.
7. MFRC522 power-cycle/SPI/backfeed test.
8. **MFRC522 read test while XKT charging is active.**
9. Wi-Fi/BLE/web control test.
10. OTA test.
11. repeated deep-sleep -> WLC wake test.
12. integrated final build.

## Configuration/source-of-truth rule

Pin numbers, pixel count/order, power-control polarity and timing constants must be centralized in firmware configuration and remain consistent with `PINOUT.md`, `NETLIST.md`, and the approved architecture. Firmware must not recreate the removed Q9 inhibit in software as a mandatory policy.