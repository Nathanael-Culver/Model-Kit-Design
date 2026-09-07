# USS Defiant — Evidence and Source Register

This file records where design facts came from. A claim should not be promoted from RECONSTRUCTED/OPEN to VERIFIED without a source here or physical bench evidence.

## Purchase / physical evidence

| Source ID | Source | Relevant facts |
|---|---|---|
| SRC-P001 | DigiKey invoice 131193174, 2026-08-19 | Purchased SN74AHCT1G125DBVR x25; AO3400A x10; AO3401A x10; MDSR-10-15-20 x10; PMEG2010ER,115 x10; NCU18XH103F60RB x10 |
| SRC-P002 | 103450 Li-Polymer specification PDF | 3.7 V nominal, 4.2 V charge, 2500 mAh, 10 x 34 x 50 mm, >=500-cycle specification; supplied manual does not establish integral protection PCB |
| SRC-H001 | Model Kits project history, 2026-02-22 | Accepted nine addressable zones P0–P8; accepted four independent non-addressable pulse-phaser LEDs |
| SRC-H002 | Earlier Defiant project history, 2025 | 330 Ω SK6812 data resistor and 470 µF 5 V bulk capacitor repeatedly used; older GPIO assignments conflict and are not authoritative |
| SRC-H003 | Model Kits project history, 2025-04-28 | Previously linked BTF-LIGHTING SK6812 RGBW strip identified as 5 V, 5050 package, 144 LEDs/m, black IP30 PCB, 1 m. Treat as RECONSTRUCTED until compared with current physical stock. |
| SRC-H004 | Model Kits project history, 2025-04-28 | Previously linked HiLetgo MT3608 module described at roughly 36 x 17 x 14 mm; treat dimensions/module style as RECONSTRUCTED until current board is measured. |
| SRC-H005 | Model Kits project history, 2025-04-28 | Previously linked DiCUNO prewired white 0805 LEDs described as 2.0 x 1.25 mm, ~16 cm leads, up to 20 mA, ~240–280 mcd, 20°; treat as RECONSTRUCTED until current stock/vendor package is checked. |

## Manufacturer / technical references

| Source ID | Manufacturer | Document / fact used |
|---|---|---|
| SRC-M001 | Seeed Studio | XIAO ESP32-C3: 21 x 17.8 mm module, 11 GPIO, Wi-Fi/BLE, 3.7 V battery input/charging, single-sided component layout, external RF antenna, documented deep-sleep operation |
| SRC-M002 | Espressif | ESP32-C3 boot/strapping: GPIO2, GPIO8 and GPIO9 are strapping pins; GPIO9 must remain high for normal SPI boot; GPIO2 pull-up is recommended; strap states are sampled at reset |
| SRC-M003 | Texas Instruments | SN74AHCT1G125DBVR: DBV/SOT-23-5, approx. 2.9 x 2.8 mm package family; 4.5–5.5 V VCC; TTL-compatible inputs; pin 1 OE, pin 2 A, pin 3 GND, pin 4 Y, pin 5 VCC |
| SRC-M004 | Alpha & Omega Semiconductor | AO3400A: N-channel, SOT-23, approx. 2.9 x 2.8 mm package; AO3401A: P-channel, SOT-23, approx. 2.9 x 2.8 mm package |
| SRC-M005 | Nexperia | PMEG2010ER: CFP3/SOD123W; approx. 2.6 x 1.7 x 1.0 mm; pin 1 K/cathode, pin 2 A/anode; marking bar is cathode |
| SRC-M006 | NXP | MFRC522 IC recommended analog/digital supply is nominal 3.3 V (2.5–3.6 V for the main supplies); exact breakout implementation still requires identification |
| SRC-M007 | Aerosemi MT3608 datasheet | MT3608 IC: SOT-23-6; pin 4 EN, high=on/low=off; IC input range 2–24 V; actual purchased module may or may not expose EN |
| SRC-M008 | Littelfuse | MDSR-10 family: axial sub-miniature reed switch with approximately 10.2 mm glass-body class; exact purchased suffix is MDSR-10-15-20 |
| SRC-M009 | Murata / DigiKey purchase data | NCU18XH103F60RB is a 10 kΩ NTC in 0603 / 1608 metric package |

## Source hierarchy

For conflicts, use this precedence:

1. physical measurement/photograph of the exact purchased part
2. exact manufacturer datasheet for the exact MPN
3. purchase invoice/order record
4. later explicitly accepted project decision
5. earlier project history
6. generic module listings / seller claims
7. assumptions — never authoritative
