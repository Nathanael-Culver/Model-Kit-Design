# USS Defiant — Evidence and Source Register

This file records where design facts came from. A claim should not be promoted from RECONSTRUCTED/OPEN to VERIFIED without a source here or physical bench evidence.

## Purchase / physical evidence

| Source ID | Source | Relevant facts |
|---|---|---|
| SRC-P001 | DigiKey invoice 131193174, 2026-08-19 | Purchased SN74AHCT1G125DBVR x25; AO3400A x10; AO3401A x10; MDSR-10-15-20 x10; PMEG2010ER,115 x10; NCU18XH103F60RB x10 |
| SRC-P002 | 103450 Li-Polymer specification PDF | 3.7 V nominal, 4.2 V charge, 2500 mAh, 10 x 34 x 50 mm, >=500-cycle specification; supplied manual does not establish integral protection PCB |
| SRC-P003 | User-supplied current-part photographs, 2026-09-06 | Exact BT1 label visibly reads 103450 / 3.7 V / 2500 mAh / 9.25 Wh. Lead-end construction strongly suggests an end-mounted board under tape, but protection function is not proven from the photograph alone. |
| SRC-P004 | User-supplied MT3608 photograph, 2026-09-06 | Actual U2 board is the common small adjustable MT3608 module with clearly marked `VIN+`, `VIN-`, `VOUT+`, `VOUT-`; no external EN pad is visible. Confirms external Q1/Q2 input disconnect remains the appropriate sleep-isolation design. |
| SRC-P005 | User-supplied DiCUNO product screenshots, 2026-09-06 | Exact pulse-phaser stock is DiCUNO pre-wired white SMD 0805, 6.3 in leads. White LED listing: 7000–12000 K, 240–280 mcd, 2.8–3.3 V, 20 mA, 120°. Listing/photo shows direct prewired leads and does not specify/include a series resistor. |
| SRC-P006 | User-supplied BTF-LIGHTING product screenshot, 2026-09-06 | Exact addressable stock is BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, 3.28 ft / 1 m, IP30, black PCB. Product image shows cuttable single-pixel strip sections with local SMD support components. |
| SRC-P007 | User-supplied RFID module photographs, 2026-09-06 | Three reader boards on hand: standard large blue RFID-RC522; compact black XFW-ETLIVE V602 board with 8-pin `SDA/SCK/MOSI/MISO/IRQ/GND/RST/3V3` header; compact green RC522 MINI V1.1-style board with 7-pin `NSS/SCK/MOSI/MISO/RST/GND/3.3V` header. Large blue board is not preferred for the Defiant due size. |
| SRC-H001 | Model Kits project history, 2026-02-22 | Accepted nine addressable zones P0–P8; accepted four independent non-addressable pulse-phaser LEDs |
| SRC-H002 | Earlier Defiant project history, 2025 | 330 Ω SK6812 data resistor and 470 µF 5 V bulk capacitor repeatedly used; older GPIO assignments conflict and are not authoritative |
| SRC-H003 | Model Kits project history, 2025-04-28 | Previously linked BTF-LIGHTING SK6812 RGBW strip identified as 5 V, 5050 package, 144 LEDs/m, black IP30 PCB, 1 m; now corroborated by SRC-P006. |
| SRC-H004 | Model Kits project history, 2025-04-28 | Previously linked HiLetgo-style MT3608 module described at roughly 36 x 17 x 14 mm; current board identity/form corroborated by SRC-P004, exact measured dimensions still to record. |
| SRC-H005 | Model Kits project history, 2025-04-28 | Previously linked DiCUNO prewired white 0805 LEDs; current product identity/specification corroborated by SRC-P005. |

## Manufacturer / technical references

| Source ID | Manufacturer / technical source | Document / fact used |
|---|---|---|
| SRC-M001 | Seeed Studio | XIAO ESP32-C3: 21 x 17.8 mm module, 11 GPIO, Wi-Fi/BLE, 3.7 V battery input/charging, single-sided component layout, external RF antenna, documented deep-sleep operation |
| SRC-M002 | Espressif | ESP32-C3 boot/strapping: GPIO2, GPIO8 and GPIO9 are strapping pins; GPIO9 must remain high for normal SPI boot; GPIO2 pull-up is recommended; strap states are sampled at reset |
| SRC-M003 | Texas Instruments | SN74AHCT1G125DBVR: DBV/SOT-23-5, approx. 2.9 x 2.8 mm package family; 4.5–5.5 V VCC; TTL-compatible inputs; pin 1 OE, pin 2 A, pin 3 GND, pin 4 Y, pin 5 VCC |
| SRC-M004 | Alpha & Omega Semiconductor | AO3400A: N-channel, SOT-23; AO3401A: P-channel, SOT-23 |
| SRC-M005 | Nexperia | PMEG2010ER: CFP3/SOD123W; pin 1 K/cathode, pin 2 A/anode; marking bar is cathode |
| SRC-M006 | NXP | MFRC522 supply is nominal 3.3 V class; SPI interface used by project |
| SRC-M007 | Aerosemi MT3608 datasheet | MT3608 IC EN is pin 4; actual purchased module does not expose an obvious EN pad, so module-input gating is retained |
| SRC-M008 | Littelfuse | MDSR-10 family axial reed switch |
| SRC-M009 | Murata / DigiKey purchase data | NCU18XH103F60RB is a 10 kΩ NTC in 0603 / 1608 metric package |
| SRC-M010 | XFW-ETLIVE mini RC522 product documentation / current third-party references | Compact XFW-ETLIVE RC522-class module is approximately 36 x 25 x 4 mm, 3.3 V SPI, integrated PCB antenna. Current black V602 board is a viable compact U3 candidate. |
| SRC-M011 | MFRC522 community libraries | FM17522 is a known RC522-compatible second-source/clone supported by common MFRC522 libraries; exact IC readback should still be recorded during bench test. |

## Source hierarchy

For conflicts, use this precedence:

1. physical measurement/photograph of the exact purchased part
2. exact manufacturer datasheet for the exact MPN
3. purchase invoice/order record
4. later explicitly accepted project decision
5. earlier project history
6. generic module listings / seller claims
7. assumptions — never authoritative
