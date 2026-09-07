# USS Defiant — Reference Designators

**Document status:** **FROZEN v1.3**  
**Applies to:** all subsequent netlists, schematics, wire lists, assembly instructions, bench layouts, photographs, and firmware documentation.

## 1. Numbering rules

- Once a reference designator appears here, it is never reassigned to a different physical component.
- Removed parts are marked `DNP` or `SUPERSEDED`; their numbers are never reused.
- Logical lighting zones `P0–P8` are firmware/functional names, not physical component references.
- Physical SK6812 emitter references begin at LED14 after actual emitter count/order is confirmed.

## 2. Primary modules / assemblies

| Ref | Component | Function | Status |
|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | master MCU / Wi-Fi / BLE / OTA / deep sleep | **FROZEN** |
| BT1 | 103450 3.7 V 2500 mAh LiPo | internal battery | **FROZEN identity; protection status OPEN** |
| RX1 | XKT high-current wireless-power receiver, apparent XKT-3168 IC | wireless power / charge input / wake-presence source | **FROZEN identity class; exact module revision OPEN** |
| TX1 | XKT-412 wireless-power transmitter | external charging/power base | **FROZEN** |
| U2 | photographed adjustable MT3608 boost-converter module | switched battery -> 5 V lighting rail | **FROZEN / physical pad form VERIFIED** |
| U3 | compact RC522-class 3.3 V SPI reader | memory-crystal/NFC reader | **FROZEN function; black XFW-ETLIVE V602 primary candidate, green RC522 MINI V1.1 alternate; bench selection OPEN** |
| U4 | TI SN74AHCT1G125DBVR | 3.3 V -> 5 V SK6812 data buffer | **FROZEN** |
| U5 | optional 1S LiPo protection module/device | used only if BT1 is unprotected | **RESERVED / DNP unless required** |

The large blue standard RFID-RC522 board is **not selected** for normal Defiant installation due its larger footprint.

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

| Ref | Function | Component | Status |
|---|---|---|---|
| LED10 | PH0 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED11 | PH1 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED12 | PH2 | DiCUNO prewired white 0805 LED | **FROZEN** |
| LED13 | PH3 | DiCUNO prewired white 0805 LED | **FROZEN** |

- LED1–LED9 are **SUPERSEDED placeholders — never reuse**.
- LED14+ are reserved for actual physical BTF-LIGHTING SK6812 RGBW emitters in serial-chain order.

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
| R17 | U3 reset/NRSTPD bias | 10 kΩ target / possible DNP after exact compact-board test |
| R18 | D0/GPIO2 `NFC_MISO` -> +3V3_ALWAYS boot pull-up | 10 kΩ |

R6–R9 are based on the verified DiCUNO white-LED listing (2.8–3.3 V, 20 mA) and the regulated 5.0 V lighting rail. 150 Ω yields approximately 11–15 mA.

## 7. Capacitors

| Ref | Function | Value/status |
|---|---|---|
| C1 | U4 local VCC bypass | 0.1 µF ceramic |
| C2 | +5V_LIGHT_SW bulk capacitor | 470 µF target; revalidate after physical load known |

The exact BTF-LIGHTING 144 LED/m SK6812 strip is now physically/product-identified; retain each manufacturer's complete cuttable pixel section and its local SMD components.

## 8. Spare / alternate purchased parts

- green compact RC522 MINI V1.1 board: viable U3 alternate until bench selection closes
- large blue standard RFID-RC522: electrical fallback, mechanically disfavored
- MDSR-10-15-20 reed switches
- NCU18XH103F60RB NTCs
- unused AO3400A / AO3401A / PMEG2010ER / SN74AHCT1G125 inventory
- the AO3400A formerly assigned Q9 remains spare; Q9 itself stays DNP

## 9. Summary

- U1/U2/U4 active and identified; U3 compact candidate class identified, final black-vs-green selection pending bench test
- U5 conditional on BT1 protection proof
- Q1–Q8 active; Q9 DNP
- LED10–LED13 exact DiCUNO parts; R6–R9 now fixed at 150 Ω
- LED14+ reserved for physical SK6812s
- no reference numbers are renumbered or reused
