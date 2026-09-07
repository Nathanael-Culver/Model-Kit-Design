# USS Defiant — Bill of Materials

**Document status:** RECONSTRUCTION IN PROGRESS  
**Rule:** purchased inventory is not automatically assigned to the Defiant unless project history or physical evidence ties it to this build.

## A. Committed / known Defiant hardware

| Ref class | Item | Exact part / identification | Package / form | Qty in Defiant | Voltage domain | Intended purpose | Mounting / carrier | Status |
|---|---|---|---|---:|---|---|---|---|
| U | MCU | Seeed Studio XIAO ESP32-C3 | 21 x 17.8 mm XIAO module | 1 | LiPo / onboard 3.3 V | Controller, Wi-Fi/BLE, deep sleep, OTA | Final mounting TBD; direct wiring expected | LOCKED; exact board verified by project history |
| BT | LiPo | 103450 Li-Polymer, 3.7 V nominal, 4.2 V charge, 2500 mAh, 9.25 Wh | 10 x 34 x 50 mm pouch cell | 1 | BAT | Main energy storage | Hull restraint/insulation TBD | VERIFIED from battery specification PDF |
| RX | Wireless receiver | XKT high-current receiver; sold as 5 V / 2 A; receiver IC marking appears `XKT-3168` | module/coil assembly | 1 | WIRELESS_5V candidate | Receive inductive power | Physical board/pad map TBD | LOCKED hardware; exact module variant OPEN |
| TX | Wireless transmitter | XKT-412 | transmitter module/coil assembly | external | external supply | Inductive power transmitter | Outside model | LOCKED hardware; exact board revision OPEN |
| U | Boost module | MT3608 adjustable boost converter module | breakout module containing MT3608 SOT-23-6 IC | 1 | BAT -> +5V_LIGHT | 5 V lighting rail | Module mounting TBD | LOCKED hardware; carrier variant/EN access OPEN |
| U | NFC module | MFRC522 13.56 MHz reader module | breakout board | 1 | +3V3_NFC | Future memory-crystal controls | Hull placement/antenna clearance TBD | LOCKED; exact breakout variant OPEN |
| LED | Addressable LED | SK6812 RGBW | exact package/board form TBD | 9 accepted addressable zones | +5V_LIGHT | Deflector/bussards/chillers/crystals/impulse engines | Physical emitter/fiber arrangement TBD | Pixel map RECONSTRUCTED; package/chain count OPEN |
| LED | Pulse phaser LED | prewired 0805 white LED | 0805 LED with leads | 4 | switched LED supply | Four independent pulse phasers | Direct/fiber coupling TBD | LOCKED count; exact Vf/current/resistor configuration OPEN |

## B. Verified purchased semiconductor inventory relevant to the design

Recovered from DigiKey invoice 131193174 dated 2026-08-19.

| Proposed ref class | Manufacturer part | DigiKey part | Purchased qty | Package | Key identity | Defiant allocation | Carrier requirement |
|---|---|---|---:|---|---|---|---|
| U | Texas Instruments `SN74AHCT1G125DBVR` | `296-4708-1-ND` | 25 | DBV / SOT-23-5 | single 4.5–5.5 V TTL-input 3-state buffer | intended for 3.3 V MCU -> 5 V SK6812 data level shifting; final quantity follows final chain count | SOT-23-5 carrier board or solderable PCB footprint |
| Q | Alpha & Omega `AO3400A` | `785-1000-1-ND` | 10 | SOT-23-3 | N-channel MOSFET, 30 V, 5.7 A headline rating | intended switching/gate-driver inventory; exact Defiant channel assignment not yet frozen | SOT-23 carrier board or PCB footprint |
| Q | Alpha & Omega `AO3401A` | `785-1001-1-ND` | 10 | SOT-23-3 | P-channel MOSFET, -30 V, -4 A headline rating | intended high-side switching inventory; exact Defiant channel assignment not yet frozen | SOT-23 carrier board or PCB footprint |
| SW | Littelfuse `MDSR-10-15-20` | `HE561-ND` | 10 | axial glass reed switch | SPST-NO, 350 mA, 140 V | purchased inventory; no current Defiant assignment proven | direct through-hole/lead mounting |
| D | Nexperia `PMEG2010ER,115` | `1727-5192-1-ND` | 10 | CFP3 / SOD123W | 20 V, 1 A Schottky rectifier; pin 1 K/cathode, pin 2 A/anode; marking bar = cathode | intended power-path/protection inventory; exact Defiant diode placement not yet frozen | solderable proto board/PCB footprint; not a SOT-23 carrier |
| TH | Murata `NCU18XH103F60RB` | `490-16279-1-ND` | 10 | 0603 | 10 kΩ NTC, B=3380 K | purchased inventory; no current Defiant assignment proven | 0603 PCB/proto footprint |

## C. Passive components and assembly hardware

| Item | Known detail | Status |
|---|---|---|
| SK6812 data series resistor | 330 Ω appears consistently in prior Defiant design history | RECONSTRUCTED; physical inventory/source not yet verified |
| 5 V rail bulk capacitor | 470 µF across 5 V/GND appears in prior design history | RECONSTRUCTED; value to be revalidated for final rail and physical inventory |
| Phaser current resistors | older drafts conflict: one used 470 Ω; another transistor-era draft used 100–150 Ω | SUPERSEDED/OPEN; must be recalculated from actual prewired LED specification |
| Gate resistors / pull resistors | exact values not yet recovered | OPEN |
| Logic-buffer bypass capacitor | required by normal IC design practice but exact purchased value/source not yet reconstructed | OPEN; do not assign inventory yet |
| SOT-23 / SOT-23-5 carrier boards | purchased | carrier type/footprint dimensions to be photographed/measured |
| solderable prototyping boards | purchased | exact board model/dimensions OPEN |
| hookup wire | purchased | gauges/colors inventory OPEN |
| copper tape | considered for space-constrained distribution | not automatically part of frozen design; mechanical decision OPEN |
| adhesives/heat-shrink/insulation | assembly hardware on hand | exact selection OPEN |

## D. Explicit exclusions

- TTP223 capacitive-touch module — **NOT USED**.
- Speaker/audio hardware — **NOT USED** in this build.

## E. BOM verification tasks

Before the BOM can be marked APPROVED, add photographs or labels for:

1. XKT receiver front/back and coil, including all pad labels and IC markings.
2. MT3608 module front/back, especially the EN implementation.
3. MFRC522 module front/back and header labels.
4. SK6812 emitter/package form actually purchased.
5. Prewired 0805 LED packaging/specification and a close-up of any inline resistor.
6. SOT-23 and SOT-23-5 carrier boards.
7. resistor/capacitor assortment actually intended for this build.
8. wire colors/gauges available.
