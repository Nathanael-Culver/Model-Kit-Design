# USS Defiant — Reference Designators

**Document status:** **FROZEN v1.6**  
**Applies to:** all subsequent netlists, schematics, wire lists, assembly instructions, bench layouts, photographs, and firmware documentation.

## 1. Numbering rules

- Once a reference designator appears here, it is never reassigned to a different physical component.
- Removed parts are marked `DNP` or `SUPERSEDED`; their numbers are never reused.
- Logical lighting zones `P0–P8` are firmware/functional names, not physical component references.
- Physical SK6812 emitter references are now frozen as LED14–LED27.

## 2. Primary modules / assemblies

| Ref | Component | Function | Status |
|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | master MCU / Wi-Fi / BLE / OTA / deep sleep | **FROZEN** |
| BT1 | 103450 3.7 V 2500 mAh LiPo | internal battery | **FROZEN identity; protection status OPEN** |
| RX1 | **XKT-3168 wireless-power receiver module + flat spiral coil** | wireless power / charge input / wake-presence source | **FROZEN / PHYSICALLY IDENTIFIED; electrical characterization deferred to integrated bench validation** |
| TX1 | **XKT-412 wireless-power transmitter module + flat spiral coil** | external charging/power base | **FROZEN / PHYSICALLY IDENTIFIED** |
| U2 | photographed adjustable MT3608 boost-converter module | switched battery -> 5 V lighting rail | **FROZEN / physical pad form VERIFIED** |
| U3 | **black XFW-ETLIVE V602 compact 3.3 V SPI RC522-class reader** | memory-crystal/NFC reader | **FROZEN / USER SELECTED** |
| U4 | TI SN74AHCT1G125DBVR | 3.3 V -> 5 V SK6812 data buffer | **FROZEN** |
| U5 | optional 1S LiPo protection module/device | used only if BT1 is unprotected | **RESERVED / DNP unless required** |

The green compact RC522 MINI V1.1-style board is retained as a spare only. The large blue standard RFID-RC522 board is not selected for Defiant installation.

## 3. MOSFETs

| Ref | Part | Function | Status |
|---|---|---|---|
| Q1 | AO3401A P-channel | lighting BAT+ high-side disconnect | **FROZEN** |
| Q2 | AO3400A N-channel | Q1 gate helper controlled by `PERIPH_EN` | **FROZEN** |
| Q3 | AO3400A N-channel | PH0 low-side switch | **FROZEN** |
| Q4 | AO3400A N-channel | PH1 low-side switch | **FROZEN** |
| Q5 | AO3400A N-channel | PH2 low-side switch | **FROZEN** |
| Q6 | AO3400A N-channel | PH3 low-side switch | **FROZEN** |
| Q7 | AO3401A P-channel | U3 +3.3 V high-side disconnect | **FROZEN** |
| Q8 | AO3400A N-channel | Q7 gate helper / NFC enable | **FROZEN** |
| Q9 | AO3400A N-channel | former wireless-power-present NFC inhibit | **DNP — number never reused** |

## 4. Diodes

| Ref | Part | Function | Status |
|---|---|---|---|
| D1 | Nexperia PMEG2010ER,115 Schottky | RX1 isolation into U1 external 5 V / charging path | **FROZEN** |

## 5. Physical LEDs

### Pulse phasers

| Ref | Function | Component | Status |
|---|---|---|---|
| LED10 | PH0 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED11 | PH1 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED12 | PH2 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED13 | PH3 | DiCUNO prewired white 0805 LED | **FROZEN** |

LED1–LED9 are **SUPERSEDED placeholders — never reuse**.

### Addressable SK6812 RGBW emitters — 14 physical pixels frozen

The nine logical zones use fourteen physical BTF-LIGHTING SK6812 RGBW pixels. Compact single optical features get one emitter; elongated/paired features get two.

| Physical ref | Chain index | Logical zone | Physical function | Status |
|---|---:|---|---|---|
| LED14 | 0 | P0 | deflector — top | **FROZEN** |
| LED15 | 1 | P0 | deflector — bottom | **FROZEN** |
| LED16 | 2 | P1 | port bussard | **FROZEN** |
| LED17 | 3 | P3 | port warp chiller — forward | **FROZEN** |
| LED18 | 4 | P3 | port warp chiller — aft | **FROZEN** |
| LED19 | 5 | P5 | port impulse crystal — forward / crystal A | **FROZEN** |
| LED20 | 6 | P5 | port impulse crystal — aft / crystal B | **FROZEN** |
| LED21 | 7 | P7 | port impulse engine | **FROZEN** |
| LED22 | 8 | P8 | starboard impulse engine | **FROZEN** |
| LED23 | 9 | P6 | starboard impulse crystal — aft / crystal B | **FROZEN** |
| LED24 | 10 | P6 | starboard impulse crystal — forward / crystal A | **FROZEN** |
| LED25 | 11 | P4 | starboard warp chiller — aft | **FROZEN** |
| LED26 | 12 | P4 | starboard warp chiller — forward | **FROZEN** |
| LED27 | 13 | P2 | starboard bussard | **FROZEN** |

The physical data route intentionally snakes from the central deflector down the port side, crosses the aft hull once, then returns forward along starboard. Firmware maps these non-contiguous physical indices back to logical P0–P8 zones.

## 6. Resistors

| Ref | Function | Value/status |
|---|---|---|
| R1 | `WLC_5V_RAW` -> `WLC_PRESENT` divider upper | 130 kΩ |
| R2 | `WLC_PRESENT` -> GND divider lower | 180 kΩ |
| R3 | Q1 gate -> BAT+ default-OFF pull-up | 100 kΩ |
| R4 | `PERIPH_EN` / Q2 gate -> GND pull-down | 100 kΩ |
| R5 | U4 output -> first SK6812 DIN | 330 Ω |
| R6 | PH0 current limit | **150 Ω, >=1/8 W** |
| R7 | PH1 current limit | **150 Ω, >=1/8 W** |
| R8 | PH2 current limit | **150 Ω, >=1/8 W** |
| R9 | PH3 current limit | **150 Ω, >=1/8 W** |
| R10 | Q3 gate pull-down | 100 kΩ |
| R11 | Q4 gate pull-down | 100 kΩ |
| R12 | Q5 gate pull-down | 100 kΩ |
| R13 | Q6 gate pull-down | 100 kΩ |
| R14 | Q7 gate -> +3V3_ALWAYS default-OFF pull-up | 100 kΩ |
| R15 | `PERIPH_EN` -> Q8 gate conditioning | 10 kΩ |
| R16 | Q8 gate -> GND default-OFF pull-down | 100 kΩ |
| R17 | U3 V602 RST bias | 10 kΩ target / possible DNP after reset test |
| R18 | D0/GPIO2 `NFC_MISO` -> +3V3_ALWAYS boot pull-up | 10 kΩ |

## 7. Capacitors

| Ref | Function | Value/status |
|---|---|---|
| C1 | U4 local VCC bypass | 0.1 µF ceramic |
| C2 | +5V_LIGHT_SW bulk capacitor | 470 µF target; validate under the frozen 14-pixel load |

Retain each BTF-LIGHTING manufacturer's complete cuttable pixel section and its local SMD components.

## 8. Spare / alternate purchased parts

- green compact RC522 MINI V1.1-style board: **spare / not installed**
- large blue standard RFID-RC522: **spare / not installed**
- MDSR-10-15-20 reed switches
- NCU18XH103F60RB NTCs
- unused AO3400A / AO3401A / PMEG2010ER / SN74AHCT1G125 inventory
- the AO3400A formerly assigned Q9 remains spare; Q9 itself stays DNP

## 9. Summary

- U3 = black XFW-ETLIVE V602
- RX1 = XKT-3168; TX1 = XKT-412
- U5 conditional on BT1 protection proof
- Q1–Q8 active; Q9 DNP
- LED10–LED13 = four pulse phasers
- **LED14–LED27 = fourteen frozen physical SK6812 RGBW emitters**
- no reference numbers are renumbered or reused
