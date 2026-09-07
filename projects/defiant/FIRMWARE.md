# USS Defiant — Firmware Architecture

**Document status:** BLUEPRINT / authoritative hardware-policy notes current through physical-lighting freeze

## Required capabilities

- Wi-Fi/BLE control after hull sealing.
- OTA firmware update without routine physical USB/BOOT access.
- deep-sleep standby.
- wireless-power-present wake/recovery behavior.
- controlled switched-rail sequencing.
- nine logical addressable lighting zones P0–P8 implemented by **14 physical SK6812 RGBW pixels**.
- four independent pulse-phaser outputs PH0–PH3.
- MFRC522-compatible NFC support using U3 black XFW-ETLIVE V602.
- safe fallback behavior after reset/brownout.

## Approved wake policy

For v1, `WLC_PRESENT` on U1 D1/GPIO3 is the normal deep-sleep wake source.

While U1 is in deep sleep:

- Wi-Fi is off;
- BLE is off;
- U3 is power-gated off;
- Wi-Fi/BLE/NFC therefore do not wake the model.

Normal workflow is to apply/enable the wireless charging field, which wakes U1. Once awake, Wi-Fi/BLE/NFC controls become available.

## NFC while charging policy

Q9 is DNP. Firmware must not treat `WLC_PRESENT` as a mandatory NFC-disable signal. U3 may operate while wireless charging is active; integrated validation checks actual coexistence.

## Target state machine

| State | Purpose |
|---|---|
| `BOOT_SAFE` | force safe outputs; inspect reset/wake/power state before loads |
| `RECOVERY_CHARGE` | charging present with low/unstable battery; keep heavy lighting conservative/off |
| `IDLE_CONNECTED` | radio/control available |
| `SHOW` | lighting/effects operation |
| `NFC_SCAN` | power U3, initialize reader, scan/act on memory crystal |
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
8. initialize U3 only after `+3V3_NFC_SW` is stable.

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

Avoid entering deep sleep while `WLC_PRESENT` is already HIGH unless immediate/repeated wake is intentionally handled.

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

## Frozen physical pixel configuration

`PHYSICAL_PIXEL_COUNT = 14`.

Physical indices are chain order:

| Index | Ref | Logical zone | Feature |
|---:|---|---|---|
| 0 | LED14 | P0 | deflector top |
| 1 | LED15 | P0 | deflector bottom |
| 2 | LED16 | P1 | port bussard |
| 3 | LED17 | P3 | port chiller forward |
| 4 | LED18 | P3 | port chiller aft |
| 5 | LED19 | P5 | port impulse crystal A |
| 6 | LED20 | P5 | port impulse crystal B |
| 7 | LED21 | P7 | port impulse engine |
| 8 | LED22 | P8 | starboard impulse engine |
| 9 | LED23 | P6 | starboard impulse crystal B |
| 10 | LED24 | P6 | starboard impulse crystal A |
| 11 | LED25 | P4 | starboard chiller aft |
| 12 | LED26 | P4 | starboard chiller forward |
| 13 | LED27 | P2 | starboard bussard |

Authoritative logical mapping:

```cpp
P0_DEFLECTOR                  = {0, 1};
P1_BUSSARD_PORT               = {2};
P2_BUSSARD_STARBOARD          = {13};
P3_CHILLER_PORT               = {3, 4};
P4_CHILLER_STARBOARD          = {11, 12};
P5_IMPULSE_CRYSTALS_PORT      = {5, 6};
P6_IMPULSE_CRYSTALS_STARBOARD = {9, 10};
P7_IMPULSE_ENGINE_PORT        = {7};
P8_IMPULSE_ENGINE_STARBOARD   = {8};
```

Do not assume `zone_number == pixel_index`.

## Lighting power/current policy

- All 14 pixels share one SK6812 data bus.
- Firmware must provide a configurable global brightness/current limit.
- Default development brightness must be conservative until the integrated 14-pixel current draw and MT3608/battery temperatures are measured.
- Effects should avoid unnecessary simultaneous maximum RGBW output.
- A future measured current limit belongs in centralized configuration, not scattered effect code.

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

Explicitly configure NFC SPI routing; do not assume default Arduino SPI pins.

## Test firmware phases

1. GPIO/default-state test.
2. WLC_PRESENT/wake test.
3. switched-rail test.
4. one SK6812 + U4 test.
5. full LED14–LED27 chain and logical-zone mapping test.
6. PH0–PH3 test.
7. V602 power-cycle/SPI/backfeed test.
8. V602 read test while XKT charging is active.
9. Wi-Fi/BLE/web control test.
10. OTA test.
11. repeated deep-sleep -> WLC wake test.
12. integrated final build/current/thermal test.

## Configuration/source-of-truth rule

Pin numbers, physical pixel count/order, logical mapping, power-control polarity and timing constants must be centralized in firmware configuration and remain consistent with `PINOUT.md`, `NETLIST.md`, and `LIGHTING-LAYOUT.md`. Firmware must not recreate the removed Q9 inhibit in software as a mandatory policy.
