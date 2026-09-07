# USS Defiant — Bill of Materials

**Document status:** STEP 1 RECONSTRUCTED / PURCHASE-RECORD VERIFICATION COMPLETE WHERE EVIDENCE EXISTS  
**Rule:** purchased inventory is not automatically assigned to the Defiant. Exact module variant, package, or physical quantity is never guessed from a generic part family.

## A. Core Defiant hardware

| Ref class | Item | Exact part / identification | Package / form | Defiant use | Status |
|---|---|---|---|---|---|
| U | MCU | Seeed Studio XIAO ESP32-C3 | XIAO development module, approx. 21 x 17.8 mm | Master controller; Wi-Fi/BLE; deep sleep; OTA; one addressable-lighting data bus; phasers; NFC; wake/power control | **LOCKED / KEEP**; exact board identity established by project history |
| BT | LiPo | 103450 Li-Polymer, 3.7 V nominal, 4.2 V charge, 2500 mAh, 9.25 Wh | 10 x 34 x 50 mm pouch cell, PH2.0 2-pin lead shown in supplied manual | Main battery; remains connected to XIAO | **VERIFIED** from supplied manual; manual does **not** establish integral protection PCB, so protection status remains OPEN |
| TX | Wireless transmitter | XKT-412 | transmitter module + coil | External wireless-power base | **LOCKED / KEEP**; exact board revision still to identify physically |
| RX | Wireless receiver | matching XKT high-current receiver; sold as 5 V / 2 A; IC marking appears `XKT-3168` | receiver module + coil | Wireless charging/recovery power and wireless-power-present source | **LOCKED / KEEP**; exact board/pad identity and real load capability still to verify physically |
| U | Boost converter | MT3608 adjustable boost-converter module | breakout module using MT3608-family boost IC | Battery -> 5 V lighting rail | **LOCKED / KEEP**; exact carrier revision and EN accessibility still to verify physically |
| U | NFC reader | MFRC522 13.56 MHz reader module | breakout board | Future Star Trek memory-crystal control | **LOCKED / KEEP**; exact breakout variant/header order still to verify physically |
| LED | Addressable lighting | SK6812 RGBW | exact purchased emitter/package form OPEN | All non-phaser animated/color lighting on the addressable serial data bus; current logical map is P0–P8 | **LOCKED technology / KEEP**; 9 logical zones are established, but the exact **physical SK6812 emitter count/package** still needs confirmation and must not be inferred from the logical-zone count |
| LED | Pulse phasers | prewired 0805 white LEDs | 0805 LED with leads | Four independently controlled pulse-phaser channels | **LOCKED count: 4 / KEEP**; exact Vf/current and whether the leads include series resistance remain OPEN |

### Addressable-lighting quantity note

The authoritative functional design currently has **9 logical SK6812-controlled zones (P0–P8) on the addressable lighting data bus** plus **4 non-addressable pulse-phaser LEDs**. Historical material includes an older reference to a larger physical SK6812 count, so the BOM deliberately does **not** equate 9 logical zones with 9 physical emitters until the physical lighting layout is reconstructed/confirmed.

## B. Exact purchased semiconductor inventory — verified from DigiKey invoice 131193174, 2026-08-19

| Proposed class | Manufacturer part | DigiKey part | Purchased qty | Exact package / description | Intended Defiant role | Disposition |
|---|---|---|---:|---|---|---|
| U | Texas Instruments `SN74AHCT1G125DBVR` | `296-4708-1-ND` | 25 | DBV / SOT-23-5; single buffer; 4.5–5.5 V supply | 3.3 V XIAO -> 5 V SK6812 data level translation; normally one device per independent SK6812 data line | **VERIFIED / KEEP**; SOT-23-5 carrier or PCB footprint required |
| Q | Alpha & Omega `AO3400A` | `785-1000-1-ND` | 10 | SOT-23-3; N-channel MOSFET; invoice description 30 V / 5.7 A | Four independent pulse-phaser low-side switches; helper switching where required | **VERIFIED / KEEP**; SOT-23 carrier/PCB required |
| Q | Alpha & Omega `AO3401A` | `785-1001-1-ND` | 10 | SOT-23-3; P-channel MOSFET; invoice description -30 V / -4 A | High-side power switching where the frozen architecture requires it | **VERIFIED / KEEP**; SOT-23 carrier/PCB required |
| SW | Littelfuse `MDSR-10-15-20` | `HE561-ND` | 10 | axial glass reed switch; SPST-NO; invoice description 350 mA / 140 V | Purchased inventory; no current Defiant function | **VERIFIED PURCHASE / NOT ASSIGNED** |
| D | Nexperia `PMEG2010ER,115` | `1727-5192-1-ND` | 10 | CFP3 / SOD123W; 20 V, 1 A Schottky | Power-path/isolation use where required | **VERIFIED / KEEP**; solderable PCB/protoboard footprint required, not SOT-23 carrier |
| TH | Murata `NCU18XH103F60RB` | `490-16279-1-ND` | 10 | 0603; 10 kΩ NTC; B=3380 K | Purchased inventory; no current Defiant function | **VERIFIED PURCHASE / NOT ASSIGNED** |

**Important correction:** this recovered DigiKey invoice contains **no ordinary resistors or capacitors**. If those parts came from DigiKey, they were from another order that has not yet been recovered. Do not attribute the passive inventory to invoice 131193174.

## C. Reconstructed passive / interconnect / assembly inventory

These items are known from project history or the user's current inventory statements, but exact purchase records or package photographs have not yet been recovered.

| Item | Reconstructed detail | Current status |
|---|---|---|
| SK6812 data series resistor | historical design repeatedly used **330 Ω** | value is a design-history datum, not yet a verified purchased part; revalidate during netlist step |
| 5 V lighting bulk capacitor | historical design repeatedly used **470 µF** | design-history datum; exact voltage rating/package/inventory OPEN |
| logic-buffer bypass capacitor | local ceramic decoupling required for SN74AHCT1G125 | value/package to be assigned during circuit design; inventory OPEN |
| phaser current-limit resistors | older drafts disagree (including 100–150 Ω and 470 Ω references) | **NOT FROZEN**; calculate from the actual prewired LED once verified |
| MOSFET pull/gate resistors | required values depend on final switch topology | **NOT FROZEN** |
| SOT-23-3 carrier boards | purchased/on hand | exact carrier footprint/dimensions/photo OPEN |
| SOT-23-5 carrier boards | purchased/on hand | exact carrier footprint/dimensions/photo OPEN |
| solderable prototyping boards | purchased/on hand | exact model/dimensions OPEN |
| hookup wire | wire inventory exists; prior project history references fine-gauge wire including 26/30 AWG | exact gauges/colors/insulation type must be inventoried physically before wire-list freeze |
| copper tape | available/considered for space-constrained power distribution | optional mechanical/interconnect material; do not place near NFC/wireless coils without test |
| heat-shrink / insulation / adhesive | assembly supplies | exact products and permanent mounting method remain mechanical-layout decisions |

## D. Historical / spare parts that are not part of the current frozen concept

| Item | Status |
|---|---|
| TTP223 capacitive-touch module | **EXCLUDED** from this build |
| speaker/audio hardware | **EXCLUDED** from this build |
| reed switches (`MDSR-10-15-20`) | purchased spare inventory; no present Defiant function |
| 10 kΩ NTC thermistors (`NCU18XH103F60RB`) | purchased spare inventory; no present Defiant function |
| any historical `SN74AHCT125N` DIP reference | not the verified DigiKey part; current verified level-shifter purchase is `SN74AHCT1G125DBVR` SOT-23-5. Treat DIP references as historical/unverified inventory unless physically found |

## E. What is verified enough to proceed to Step 2

The **component families and intended major hardware are reconstructed well enough to proceed**. The following exact-identity items still require physical photos/labels before their pin-level entries can be marked VERIFIED:

1. RX1 XKT receiver — front/back, coil, output-pad labels, IC marking.
2. TX1 XKT-412 transmitter — front/back and connector/pad labels if relevant to the project documentation.
3. U2 MT3608 module — front/back; exact pad labels; determine whether EN is exposed/accessible.
4. U3 MFRC522 module — front/back; exact header order and board variant.
5. SK6812s — packaging or close-up showing exact package/form, plus actual number of physical emitters intended for the hull.
6. One prewired 0805 phaser LED — packaging/close-up and resistance measurement or vendor specification.
7. SOT-23-3 and SOT-23-5 carrier boards — front/back with scale.
8. Passive assortment — resistor/capacitor values actually on hand.
9. Wire inventory — gauges and colors actually on hand.
10. BT1 battery — physical photo of lead end/body to determine whether a protection PCB is visibly integrated; the supplied manual itself does not document protection circuitry.

## F. Step-1 conclusion

- **No major purchased component is currently rejected.**
- **No new active component is currently required.**
- Exact DigiKey semiconductor purchase quantities/packages are verified.
- Battery electrical/physical specification is verified, but protection-circuit status is not.
- Module-level exact variants and several assembly/passive details remain `OPEN` pending physical evidence; they must be resolved before pin-level netlist/schematic release, but they do not prevent moving to the next engineering step.
