# USS Defiant — XIAO ESP32-C3 Pin Map

**Document status:** **FROZEN v1.0 — FINAL FUNCTIONAL GPIO ASSIGNMENT**  
**Release status:** pin map is authoritative for firmware/netlist/wire-list work; physical boot/backfeed tests remain required before final schematic release.

## 1. XIAO hardware map

| XIAO pin | ESP32-C3 GPIO | Relevant board/native function | Project concern |
|---|---:|---|---|
| D0 / A0 | GPIO2 | ADC1_CH2 | strapping pin; pull-up recommended |
| D1 / A1 | GPIO3 | ADC1_CH3 | wake-capable, non-strapping |
| D2 / A2 | GPIO4 | ADC1_CH4 / JTAG | ordinary GPIO after boot |
| D3 / A3 | GPIO5 | ADC2_CH0 / JTAG | ordinary GPIO after boot |
| D4 / SDA | GPIO6 | I2C SDA / JTAG | ordinary GPIO after boot |
| D5 / SCL | GPIO7 | I2C SCL / JTAG | ordinary GPIO after boot |
| D6 / TX | GPIO21 | UART0 TX | ROM/boot text may appear at reset |
| D7 / RX | GPIO20 | UART0 RX | ordinary GPIO for this design |
| D8 / SCK | GPIO8 | SPI-capable | strapping pin; GPIO8 value does not block normal SPI boot when GPIO9 remains high |
| D9 / MISO | GPIO9 | BOOT / SPI-capable | critical boot strap; must remain HIGH/not be externally forced low at reset |
| D10 / MOSI | GPIO10 | SPI-capable | ordinary GPIO for this design |

## 2. Final approved allocation

| XIAO pin | GPIO | Frozen signal | Direction | Why this assignment |
|---|---:|---|---|---|
| **D0** | **GPIO2** | `NFC_MISO` | input | input-only project role on the GPIO2 strap pin; add explicit pull-up and verify unpowered U3 does not clamp it low |
| **D1** | **GPIO3** | `WLC_PRESENT` | input / wake | wake-capable non-strapping pin; safest place for the wireless-power wake signal |
| **D2** | **GPIO4** | `PH0_GATE` | output | ordinary output with hardware 100 kΩ pull-down |
| **D3** | **GPIO5** | `PH1_GATE` | output | ordinary output with hardware 100 kΩ pull-down |
| **D4** | **GPIO6** | `PH2_GATE` | output | ordinary output with hardware 100 kΩ pull-down |
| **D5** | **GPIO7** | `PH3_GATE` | output | ordinary output with hardware 100 kΩ pull-down |
| **D6** | **GPIO21** | `NFC_CS` | output | boot UART chatter is harmless because U3 is physically unpowered during reset/boot |
| **D7** | **GPIO20** | `PERIPH_EN` | output | non-strapping and not boot-TX; hardware pull-down guarantees default OFF |
| **D8** | **GPIO8** | `NFC_SCK` | output | strap pin is acceptable because U3 is unpowered at reset; final boot test still required |
| **D9** | **GPIO9** | `SK_DATA_RAW` | output | deliberately connected only to U4's high-impedance/over-voltage-tolerant input; avoids putting a powered-down module or MOSFET pull-down on the critical BOOT pin |
| **D10** | **GPIO10** | `NFC_MOSI` | output | ordinary output and natural SPI-role choice |

## 3. GPIO2 / D0 protection rule

Because D0/GPIO2 is a strapping pin and Espressif recommends it be pulled high, add:

- `R18 = 10 kΩ`
- R18 from `NFC_MISO` / D0 to `+3V3_ALWAYS`

This pull-up is weak enough that the MFRC522 can drive MISO low normally (~0.33 mA load at 3.3 V) but gives GPIO2 a defined HIGH bias during reset and while U3 is unpowered.

**Bench requirement:** with U3 physically connected but unpowered, confirm D0 remains HIGH enough for reliable boot. If the exact breakout clamps MISO strongly while unpowered, that is a hardware-validation failure and must be corrected before final assembly; the pin map must not be silently changed.

## 4. Critical boot-state behavior

### D9 / GPIO9 — `SK_DATA_RAW`

GPIO9 is the most critical strap. Normal SPI boot requires it HIGH.

The selected load is U4 pin 2 (`A`) only. U4 is SN74AHCT1G125 and its input is high impedance/over-voltage tolerant while its switched 5 V supply is absent. There is **no pull-down** on this line.

Required bench test:

- reset/power-cycle U1 repeatedly with U4 connected and `+5V_LIGHT_SW` OFF;
- verify normal SPI boot every time;
- verify no measurable path pulls GPIO9 low during the strap-sampling interval.

Do **not** place a phaser MOSFET gate, `PERIPH_EN`, MFRC522 output, or other pull-down load on D9.

### D8 / GPIO8 — `NFC_SCK`

GPIO8 is a strap pin, but its state is not decisive for normal SPI boot when GPIO9 is HIGH. U3 is hardware-unpowered during reset, so this is the least risky remaining use of D8. Boot cycling with the exact U3 breakout remains mandatory.

### D6 / GPIO21 — `NFC_CS`

ROM/bootloader output may appear on D6/GPIO21. Therefore it is **not** used for `PERIPH_EN` or any MOSFET power gate. U3 is unpowered during reset, so boot UART transitions cannot select or command it.

## 5. SPI routing

The project does not rely on the XIAO silkscreen's default SPI trio as a fixed bus. ESP32-C3 GPIO routing permits the MFRC522 SPI signals to use the frozen assignments:

- SCK = D8 / GPIO8
- MOSI = D10 / GPIO10
- MISO = D0 / GPIO2
- CS = D6 / GPIO21

Firmware must explicitly instantiate/configure SPI with these pins rather than assuming Arduino default pin macros.

## 6. Pin-budget proof

| Function | Count |
|---|---:|
| `WLC_PRESENT` | 1 |
| `PERIPH_EN` | 1 |
| `SK_DATA_RAW` | 1 |
| PH0–PH3 | 4 |
| NFC SPI | 4 |
| **Total** | **11 / 11** |

No free exposed GPIO remains in the frozen design.

Any future feature requiring another GPIO must first remove/combine an existing function or trigger a documented architecture change. No pin sharing may be introduced silently.

## 7. Firmware constants

Firmware `hardware_config.h` must resolve to:

```cpp
PIN_NFC_MISO    = 2;   // D0 / GPIO2
PIN_WLC_PRESENT = 3;   // D1 / GPIO3
PIN_PH0         = 4;   // D2 / GPIO4
PIN_PH1         = 5;   // D3 / GPIO5
PIN_PH2         = 6;   // D4 / GPIO6
PIN_PH3         = 7;   // D5 / GPIO7
PIN_NFC_CS      = 21;  // D6 / GPIO21
PIN_PERIPH_EN   = 20;  // D7 / GPIO20
PIN_NFC_SCK     = 8;   // D8 / GPIO8
PIN_SK_DATA     = 9;   // D9 / GPIO9
PIN_NFC_MOSI    = 10;  // D10 / GPIO10
```

These are ESP32-C3 GPIO numbers, not ordinal D-pin numbers.

## 8. Superseded historical maps

All older mappings are **SUPERSEDED**, including versions that placed:

- SK6812 on D7 or D8;
- phasers on D3–D6;
- MFRC522 MISO on D9/BOOT;
- MFRC522 reset on a dedicated MCU pin.

Only the table in section 2 is authoritative.

## 9. Step-6 acceptance tests still required

The assignment is frozen, but final drawing release requires physical tests:

1. D1/GPIO3 wakes U1 reliably from deep sleep when `WLC_PRESENT` rises.
2. D0/GPIO2 + R18 remains boot-safe with U3 connected and unpowered.
3. D8/GPIO8 remains boot-safe with U3 connected and unpowered.
4. D9/GPIO9 remains HIGH/boot-safe with U4 connected and unpowered.
5. D6 boot chatter cannot energize or command U3 while U3 is off.
6. `PERIPH_EN` D7 remains LOW through reset because R4 holds it off.
7. all four phaser outputs remain LOW through reset because R10–R13 hold them off.
8. firmware configures non-default MFRC522 SPI pin routing correctly.

## 10. Step-6 conclusion

**The functional GPIO map is now frozen and contains exactly one function per exposed XIAO GPIO.** It deliberately assigns the critical GPIO9 BOOT pin to the electrically least intrusive available load and reserves the safest wake-capable non-strap pin for wireless-power wake.
