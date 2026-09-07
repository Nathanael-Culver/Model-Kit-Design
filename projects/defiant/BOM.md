# USS Defiant — Bill of Materials

**Document status:** STEP 9c — PURCHASE RECORDS + CURRENT PHYSICAL IDENTIFICATION INCORPORATED  
**Rule:** purchased inventory is not automatically assigned to the Defiant; exact active parts and quantities below are authoritative where marked FROZEN/VERIFIED.

## A. Core Defiant hardware

| Ref | Item | Exact part / identification | Package / form | Defiant use | Status |
|---|---|---|---|---|---|
| U1 | MCU | Seeed Studio XIAO ESP32-C3 | 21 x 17.8 mm module | master controller; Wi-Fi/BLE; OTA; deep sleep | **FROZEN / VERIFIED** |
| BT1 | LiPo | 103450, 3.7 V, 2500 mAh, 9.25 Wh | 10 x 34 x 50 mm pouch | main battery | **FROZEN identity; protection status OPEN** |
| TX1 | wireless transmitter | XKT-412 | transmitter PCB + flat spiral coil | external wireless-power base | **PHYSICALLY IDENTIFIED / FROZEN** |
| RX1 | wireless receiver | XKT-3168 receiver, selected 5 V / 2 A hardware | receiver PCB + flat spiral coil | charging/recovery + WLC_PRESENT source | **PHYSICALLY IDENTIFIED / FROZEN** |
| U2 | boost converter | adjustable MT3608 module | complete PCB with VIN+/VIN-/VOUT+/VOUT- | battery -> switched 5 V lighting rail | **PHYSICALLY IDENTIFIED / FROZEN** |
| U3 | NFC reader | black XFW-ETLIVE V602 RC522-class 3.3 V SPI reader | compact reader PCB + integrated antenna | memory-crystal control | **USER SELECTED / FROZEN** |
| U4 | level shifter | TI SN74AHCT1G125DBVR | SOT-23-5 on carrier | XIAO 3.3 V -> SK6812 5 V data | **VERIFIED / FROZEN** |
| LED14–LED27 | addressable lighting | BTF-LIGHTING SK6812 RGBW Natural White | 5 V, 144 LED/m, IP30 black flexible strip | 14 physical emitters mapped to P0–P8 | **COUNT/TYPE FROZEN** |
| LED10–LED13 | pulse phasers | DiCUNO prewired white 0805 LEDs | 0805 with ~6.3 in leads | four independent phaser channels | **COUNT/TYPE FROZEN** |

### Addressable-lighting quantity

The final physical count is **14 SK6812 RGBW emitters** on one serial data bus, mapped to 9 logical zones:

- P0 deflector: 2
- P1/P2 bussards: 1 each
- P3/P4 warp chillers: 2 each
- P5/P6 impulse crystals: 2 each
- P7/P8 impulse engines: 1 each

See `LIGHTING-LAYOUT.md` for LED14–LED27 chain order.

## B. Exact purchased semiconductor inventory — DigiKey invoice 131193174, 2026-08-19

| Proposed class | Manufacturer part | DigiKey part | Purchased qty | Exact package / description | Defiant role | Disposition |
|---|---|---|---:|---|---|---|
| U | TI `SN74AHCT1G125DBVR` | `296-4708-1-ND` | 25 | DBV / SOT-23-5; single AHCT buffer | U4 SK6812 level translation | **VERIFIED / KEEP** |
| Q | AOS `AO3400A` | `785-1000-1-ND` | 10 | SOT-23-3 N-channel | Q2/Q3–Q6/Q8 helper/switch functions | **VERIFIED / KEEP** |
| Q | AOS `AO3401A` | `785-1001-1-ND` | 10 | SOT-23-3 P-channel | Q1/Q7 high-side switches | **VERIFIED / KEEP** |
| SW | Littelfuse `MDSR-10-15-20` | `HE561-ND` | 10 | axial reed switch | spare inventory | **NOT ASSIGNED** |
| D | Nexperia `PMEG2010ER,115` | `1727-5192-1-ND` | 10 | CFP3 / SOD123W, 20 V / 1 A Schottky | D1 wireless-input isolation | **VERIFIED / KEEP** |
| TH | Murata `NCU18XH103F60RB` | `490-16279-1-ND` | 10 | 0603 10 kΩ NTC | spare inventory | **NOT ASSIGNED** |

The recovered DigiKey invoice contains **no ordinary resistors or capacitors**.

## C. Frozen / selected passives

| Ref/value | Function | Status |
|---|---|---|
| R1 130 kΩ | WLC_PRESENT divider upper | FROZEN |
| R2 180 kΩ | WLC_PRESENT divider lower | FROZEN |
| R3 100 kΩ | Q1 gate pull-up | FROZEN |
| R4 100 kΩ | PERIPH_EN pull-down | FROZEN |
| R5 330 Ω | SK6812 data series resistor | FROZEN |
| R6–R9 150 Ω >=1/8 W | phaser current limit | FROZEN |
| R10–R13 100 kΩ | phaser gate pull-downs | FROZEN |
| R14 100 kΩ | Q7 gate pull-up | FROZEN |
| R15 10 kΩ | NFC enable conditioning | FROZEN |
| R16 100 kΩ | NFC enable pull-down | FROZEN |
| R17 10 kΩ target | V602 RST bias | bench-confirm / possible DNP |
| R18 10 kΩ | GPIO2/NFC_MISO boot pull-up | FROZEN |
| C1 0.1 µF ceramic | U4 local bypass | FROZEN |
| C2 470 µF target, >=6.3 V | switched 5 V bulk capacitor | target; validate under 14-pixel load |

## D. Assembly / interconnect inventory

| Item | Status / use |
|---|---|
| SOT-23-3 carrier boards | purchased; Q1–Q8 as applicable; continuity-map before soldering |
| SOT-23-5 carrier boards | purchased; U4 |
| solderable prototyping boards | purchased; central control/power/distribution candidate |
| hookup wire | on hand; exact gauge/color inventory still to freeze |
| copper tape | optional low-profile distribution; keep clear of RX1/TX1 and U3 antenna areas until validated |
| heat-shrink/insulation/adhesive | assembly supplies; final methods remain mechanical-layout decisions |

## E. Spare / excluded hardware

| Item | Status |
|---|---|
| green compact RC522 MINI V1.1 | spare, not installed |
| large blue standard RFID-RC522 | spare, not installed |
| TTP223 touch module | EXCLUDED |
| speaker/audio hardware | EXCLUDED |
| reed switches | spare, not assigned |
| NTC thermistors | spare, not assigned |
| historical SN74AHCT125N DIP references | not authoritative for final build |
| Q9 | DNP; designator never reused |

## F. Remaining inventory facts to close

1. BT1 integral-protection proof.
2. exact carrier-board pad orientation/dimensions.
3. resistor/capacitor stock confirmation against the frozen values above.
4. wire gauges/colors on hand.
5. final protoboard/distribution-board dimensions.

## G. Conclusion

The active BOM is sufficiently defined for physical placement and harness design. No new active IC/module purchase is currently required. The addressable-lighting quantity is no longer open: **14 SK6812 RGBW pixels**.
