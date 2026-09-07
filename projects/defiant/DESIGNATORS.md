# USS Defiant — Reference Designators

**Document status:** **FROZEN v1.2**  
**Applies to:** all subsequent netlists, schematics, wire lists, assembly instructions, bench layouts, photographs, and firmware documentation.

## 1. Numbering rules

- Once a reference designator appears here, it is never reassigned to a different physical component.
- Removed parts are marked `DNP` or `SUPERSEDED`; their numbers are never reused.
- Logical lighting zones `P0–P8` are firmware/functional names, not physical component references.
- Physical SK6812 emitter references begin at LED14 after actual emitter count/order is confirmed.

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

## 3. Primary modules / assemblies

| Ref | Component | Function | Status |
|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | master MCU / Wi-Fi / BLE / OTA / deep sleep | **FROZEN** |
| BT1 | 103450 3.7 V 2500 mAh LiPo | internal battery | **FROZEN** |
| RX1 | XKT high-current wireless-power receiver, apparent XKT-3168 IC | wireless power / charge input / wake-presence source | **FROZEN identity class; exact module revision OPEN** |
| TX1 | XKT-412 wireless-power transmitter | external charging/power base | **FROZEN** |
| U2 | MT3608 boost-converter module | switched battery -> 5 V lighting rail | **FROZEN** |
| U3 | MFRC522 NFC breakout | memory-crystal/NFC reader | **FROZEN** |
| U4 | TI SN74AHCT1G125DBVR | 3.3 V -> 5 V SK6812 data buffer | **FROZEN** |
| U5 | optional 1S LiPo protection module/device | used only if BT1 is unprotected | **RESERVED / DNP unless required** |

## 4. MOSFETs

| Ref | Part | Function | Status |
|---|---|---|---|
| Q1 | AO3401A P-channel | lighting BAT+ high-side disconnect | **FROZEN** |
| Q2 | AO3400A N-channel | Q1 gate helper controlled by `PERIPH_EN` | **FROZEN** |
| Q3 | AO3400A N-channel | PH0 low-side switch | **FROZEN** |
| Q4 | AO3400A N-channel | PH1 low-side switch | **FROZEN** |
| Q5 | AO3400A N-channel | PH2 low-side switch | **FROZEN** |
| Q6 | AO3400A N-channel | PH3 low-side switch | **FROZEN** |
| Q7 | AO3401A P-channel | MFRC522 +3.3 V high-side disconnect | **FROZEN** |
| Q8 | AO3400A N-channel | Q7 gate helper / NFC enable | **FROZEN** |
| Q9 | AO3400A N-channel | former wireless-power-present NFC inhibit | **DNP — user-approved Step-9 removal; number never reused** |

Active frozen design consumes 2 of 10 AO3401A devices and 6 of 10 AO3400A devices.

## 5. Diodes

| Ref | Part | Function | Status |
|---|---|---|---|
| D1 | Nexperia PMEG2010ER,115 Schottky | RX1 isolation into U1 external 5 V / charging path | **FROZEN** |

## 6. Physical LEDs

| Ref | Function | Component | Status |
|---|---|---|---|
| LED10 | PH0 | prewired white 0805 LED | **FROZEN** |
| LED11 | PH1 | prewired white 0805 LED | **FROZEN** |
| LED12 | PH2 | prewired white 0805 LED | **FROZEN** |
| LED13 | PH3 | prewired white 0805 LED | **FROZEN** |

- LED1–LED9 are **SUPERSEDED placeholders — never reuse**.
- LED14+ are reserved for actual physical SK6812 emitters in serial-chain order.

## 7. Resistors

| Ref | Function | Value/status |
|---|---|---|
| R1 | `WLC_5V_RAW` -> `WLC_PRESENT` divider upper | 130 kΩ |
| R2 | `WLC_PRESENT` -> GND divider lower | 180 kΩ |
| R3 | Q1 gate -> BAT+ default-OFF pull-up | 100 kΩ |
| R4 | `PERIPH_EN` / Q2 gate -> GND pull-down | 100 kΩ |
| R5 | U4 output -> first SK6812 DIN | 330 Ω |
| R6 | PH0 current limit | TBD / possible DNP |
| R7 | PH1 current limit | TBD / possible DNP |
| R8 | PH2 current limit | TBD / possible DNP |
| R9 | PH3 current limit | TBD / possible DNP |
| R10 | Q3 gate pull-down | 100 kΩ |
| R11 | Q4 gate pull-down | 100 kΩ |
| R12 | Q5 gate pull-down | 100 kΩ |
| R13 | Q6 gate pull-down | 100 kΩ |
| R14 | Q7 gate -> +3V3_ALWAYS default-OFF pull-up | 100 kΩ |
| R15 | `PERIPH_EN` -> Q8 gate conditioning | 10 kΩ |
| R16 | Q8 gate -> GND default-OFF pull-down | 100 kΩ |
| R17 | U3 reset/NRSTPD bias | 10 kΩ target / possible DNP |
| R18 | D0/GPIO2 `NFC_MISO` -> +3V3_ALWAYS boot pull-up | 10 kΩ |

No resistor is required solely for Q9 because Q9 is DNP.

## 8. Capacitors

| Ref | Function | Value/status |
|---|---|---|
| C1 | U4 local VCC bypass | 0.1 µF ceramic |
| C2 | +5V_LIGHT_SW bulk capacitor | 470 µF target; revalidate after physical load known |

## 9. Spare purchased parts

Purchased but not installed unless a later approved change requires them:

- MDSR-10-15-20 reed switches
- NCU18XH103F60RB NTCs
- unused AO3400A / AO3401A / PMEG2010ER / SN74AHCT1G125 inventory
- the physical AO3400A that would otherwise have been Q9

## 10. Connector/test-point numbering

`J1+` and `TP1+` remain unassigned until a real physical/service need is proven.

## 11. Summary

- U1–U4 active; U5 conditional
- BT1, RX1, TX1 active
- Q1–Q8 active
- **Q9 DNP permanently**
- D1 active
- LED10–LED13 active
- LED14+ reserved for physical SK6812s
- R1–R18 and C1–C2 retained as assigned
- LED1–LED9 permanently superseded