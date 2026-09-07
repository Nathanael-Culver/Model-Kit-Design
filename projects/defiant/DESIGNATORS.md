# USS Defiant — Reference Designators

**Document status:** **FROZEN v1.1**  
**Applies to:** all subsequent netlists, schematics, wire lists, assembly instructions, bench layouts, photographs, and firmware documentation.

## 1. Numbering rules

- Once a reference designator appears in this frozen document, it is never reassigned to a different physical component.
- Removed parts are marked `DNP` or `SUPERSEDED`; their numbers are never reused.
- Logical lighting zones `P0–P8` are firmware/functional names, **not physical component reference designators**.
- Physical SK6812 emitter references are assigned only after the actual emitter count/order is confirmed.

## 2. Designator classes

| Prefix | Class |
|---|---|
| U | IC/module/controller/regulator/buffer |
| Q | MOSFET/transistor |
| D | diode |
| R | resistor |
| C | capacitor |
| LED | physical LED / addressable emitter |
| BT | battery |
| RX | wireless-power receiver assembly |
| TX | wireless-power transmitter assembly |
| SW | switch/reed switch |
| TH | thermistor |
| J | connector/header |
| TP | test point |

## 3. Primary modules / assemblies — frozen

| Ref | Component | Function | Status |
|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | master MCU / Wi-Fi / BLE / OTA / deep sleep | **FROZEN** |
| BT1 | 103450 3.7 V 2500 mAh LiPo | internal battery | **FROZEN** |
| RX1 | XKT high-current wireless-power receiver, apparent XKT-3168 IC | wireless power / charge input / presence source | **FROZEN identity class; exact module revision OPEN** |
| TX1 | XKT-412 wireless-power transmitter | external charging/power base | **FROZEN** |
| U2 | MT3608 boost-converter module | switched battery -> 5 V lighting rail | **FROZEN** |
| U3 | MFRC522 NFC breakout | memory-crystal/NFC reader | **FROZEN** |
| U4 | Texas Instruments SN74AHCT1G125DBVR | one 3.3 V -> 5 V SK6812 data buffer | **FROZEN** |
| U5 | optional 1S LiPo protection module/device | used only if BT1 is proven unprotected | **RESERVED / DNP unless required** |

## 4. MOSFETs — frozen

| Ref | Part | Function | Status |
|---|---|---|---|
| Q1 | AO3401A P-channel | lighting subsystem BAT+ high-side disconnect | **FROZEN** |
| Q2 | AO3400A N-channel | Q1 gate-pull helper controlled by `PERIPH_EN` | **FROZEN** |
| Q3 | AO3400A N-channel | pulse phaser PH0 low-side switch | **FROZEN** |
| Q4 | AO3400A N-channel | pulse phaser PH1 low-side switch | **FROZEN** |
| Q5 | AO3400A N-channel | pulse phaser PH2 low-side switch | **FROZEN** |
| Q6 | AO3400A N-channel | pulse phaser PH3 low-side switch | **FROZEN** |
| Q7 | AO3401A P-channel | MFRC522 +3.3 V high-side disconnect | **FROZEN** |
| Q8 | AO3400A N-channel | Q7 gate-pull / NFC-enable helper | **FROZEN** |
| Q9 | AO3400A N-channel | wireless-power-present NFC hardware inhibit | **FROZEN** |

Purchased inventory remains sufficient: frozen design currently consumes 2 of 10 AO3401A devices and 7 of 10 AO3400A devices.

## 5. Diodes — frozen

| Ref | Part | Function | Status |
|---|---|---|---|
| D1 | Nexperia PMEG2010ER,115 Schottky | RX1 wireless-power isolation into U1 external 5 V / charging path | **FROZEN function; final polarity proven in netlist** |

## 6. Physical LEDs

### Pulse phasers — frozen

| Ref | Functional name | Component | Status |
|---|---|---|---|
| LED10 | PH0 | prewired white 0805 LED | **FROZEN** |
| LED11 | PH1 | prewired white 0805 LED | **FROZEN** |
| LED12 | PH2 | prewired white 0805 LED | **FROZEN** |
| LED13 | PH3 | prewired white 0805 LED | **FROZEN** |

### Addressable lighting

`LED1–LED9` appeared in early reconstruction as if each logical P0–P8 zone were one physical LED. That assumption is not sufficiently supported.

- `LED1–LED9` are now **SUPERSEDED PLACEHOLDERS — NEVER REUSE**.
- Physical SK6812 emitters will begin at **LED14** and increase in serial-chain order after the hull lighting layout confirms the actual physical emitter count and grouping.
- Logical zones remain permanently named `P0` through `P8` and may map to one or more physical LED refs.

## 7. Resistors — assigned by fixed function

| Ref | Function | Current value status |
|---|---|---|
| R1 | `WLC_5V_RAW` -> `WLC_PRESENT` divider upper resistor | 130 kΩ formal starting value |
| R2 | `WLC_PRESENT` -> GND divider lower resistor | 180 kΩ formal starting value |
| R3 | Q1 gate -> BAT+ default-OFF pull-up | 100 kΩ |
| R4 | Q2 gate / `PERIPH_EN` -> GND default-OFF pull-down | 100 kΩ |
| R5 | U4 output -> first SK6812 data input series resistor | 330 Ω |
| R6 | LED10 / PH0 current-limit resistor | TBD; may become DNP if prewired LED includes verified resistor |
| R7 | LED11 / PH1 current-limit resistor | TBD; may become DNP if prewired LED includes verified resistor |
| R8 | LED12 / PH2 current-limit resistor | TBD; may become DNP if prewired LED includes verified resistor |
| R9 | LED13 / PH3 current-limit resistor | TBD; may become DNP if prewired LED includes verified resistor |
| R10 | Q3 / PH0 gate default-OFF pull-down | 100 kΩ |
| R11 | Q4 / PH1 gate default-OFF pull-down | 100 kΩ |
| R12 | Q5 / PH2 gate default-OFF pull-down | 100 kΩ |
| R13 | Q6 / PH3 gate default-OFF pull-down | 100 kΩ |
| R14 | Q7 gate -> +3V3_ALWAYS default-OFF pull-up | 100 kΩ |
| R15 | `PERIPH_EN` -> Q8 gate control/conditioning resistor | 10 kΩ |
| R16 | Q8 gate -> GND default-OFF pull-down | 100 kΩ |
| R17 | U3 MFRC522 reset/NRSTPD bias connection | 10 kΩ target; may be DNP if exact breakout already provides suitable bias |
| R18 | D0/GPIO2 `NFC_MISO` -> +3V3_ALWAYS boot-strapping pull-up | **10 kΩ — added by frozen Step-6 pin assignment** |

## 8. Capacitors — assigned by fixed function

| Ref | Function | Current value status |
|---|---|---|
| C1 | U4 SN74AHCT1G125 local VCC bypass | 0.1 µF ceramic |
| C2 | +5V_LIGHT_SW bulk capacitor near lighting distribution | 470 µF target; revalidate against physical emitter count/load |

Additional passives, if electrically justified later, receive the next unused numbers and are never inserted by renumbering existing parts.

## 9. Spare purchased parts — not Defiant reference assignments

The following are documented inventory but are not installed in the frozen architecture, so they do not receive active Defiant designators:

- MDSR-10-15-20 reed switches
- NCU18XH103F60RB 10 kΩ NTC thermistors
- unused AO3400A / AO3401A / PMEG2010ER / SN74AHCT1G125 stock

## 10. Connector/test-point numbering

No permanent final-hull connector is currently required beyond the battery/module leads already part of their assemblies. `J1+` and `TP1+` remain unassigned until a later netlist/bench-layout step proves one useful.

## 11. Frozen designator summary

Active/conditional frozen references:

- `U1–U4` active; `U5` reserved conditional battery protection
- `BT1`, `RX1`, `TX1`
- `Q1–Q9`
- `D1`
- `LED10–LED13` pulse phasers
- `LED14+` reserved for confirmed physical SK6812 chain members
- `R1–R18`
- `C1–C2`

`LED1–LED9` are permanently **SUPERSEDED** and must not appear as physical LEDs in new drawings.
