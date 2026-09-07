# USS Defiant — Part Identification, Packages, and Carrier Requirements

**Document status:** STEP 2 COMPLETE WHERE EVIDENCE EXISTS / MODULE-LEVEL PHYSICAL VERIFICATION STILL OPEN

This document answers: what exact part is it, what physical package/form is it, and what does it need in order to be mounted/wired in the Defiant.

## 1. Parts with exact identity/package established

| Ref/class | Exact part | Physical package / size | Mounting / carrier requirement | Step-2 status |
|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | XIAO module, 21 x 17.8 mm; single-sided component layout; castellated/through-hole edge pads plus battery pads | **No carrier required.** Final model should use direct soldered wires/pads rather than tall header pins unless bench use requires headers. Mechanically secure the module separately and preserve antenna clearance. | **VERIFIED** |
| BT1 | 103450 Li-Polymer, 3.7 V nominal, 2500 mAh, 9.25 Wh | pouch cell, 10 x 34 x 50 mm; supplied manual shows PH2.0-style two-wire connector/lead | **No carrier.** Requires padded/nonconductive restraint; do not clamp or puncture pouch. Final electrical termination may be direct lead/connector depending hull layout. Protection-PCB status remains OPEN. | **VERIFIED electrical/size; protection OPEN** |
| U4 class | Texas Instruments `SN74AHCT1G125DBVR` | DBV, SOT-23-5, approx. 2.9 x 2.8 mm body | **Carrier/adapter required for hand-wired build.** Use purchased SOT-23-5 breakout/carrier or an equivalent PCB footprint. Add local bypass capacitor on the same carrier/board. | **VERIFIED** |
| Q class | Alpha & Omega `AO3400A` | SOT-23-3, approx. 2.9 x 2.8 mm body | **Carrier/adapter required for hand wiring.** Use purchased SOT-23-3 breakout/carrier or dedicated PCB footprint. | **VERIFIED** |
| Q class | Alpha & Omega `AO3401A` | SOT-23-3, approx. 2.9 x 2.8 mm body | **Carrier/adapter required for hand wiring.** Use purchased SOT-23-3 breakout/carrier or dedicated PCB footprint. | **VERIFIED** |
| D class | Nexperia `PMEG2010ER,115` | CFP3 / SOD123W, two-terminal SMD, approx. 2.6 x 1.7 x 1.0 mm | **Not compatible with SOT-23 carriers.** Mount on a small SOD123/SOD123W pad area, custom PCB, or carefully prepared solderable proto-board pads. Dedicated breakout optional, not inherently required. | **VERIFIED** |
| SW spare | Littelfuse `MDSR-10-15-20` | axial glass reed switch; MDSR-10 family has approx. 10.2 mm glass body | **No carrier required.** Through-hole/lead mounting with strain relief if ever used. Not assigned to current Defiant architecture. | **VERIFIED purchase / spare** |
| TH spare | Murata `NCU18XH103F60RB` | 0603 / 1608 metric SMD NTC, 10 kΩ | **Carrier or PCB footprint required if used.** Too small for direct standard perfboard-hole mounting without adapter/pads. Not assigned to current Defiant architecture. | **VERIFIED purchase / spare** |

## 2. Reconstructed purchased module/form details that still need physical confirmation

| Part | Best reconstructed identification | Package/form | Mounting requirement | Remaining verification |
|---|---|---|---|---|
| U2 MT3608 | HiLetgo-style adjustable MT3608 boost module previously linked in project history | reconstructed module approximately **36 x 17 x 14 mm**; screw-adjust trimmer; generic module rather than bare MT3608 IC | **No semiconductor carrier.** Mount the complete module to hull/protoboard with insulated mechanical restraint. Do not rely on the module's solder joints as structural support. | Photograph exact purchased board front/back; record actual dimensions and whether MT3608 EN is accessible or tied on-board. |
| U3 MFRC522 | MFRC522 13.56 MHz SPI breakout module | complete reader PCB with printed loop antenna; exact board revision/size/header order not yet established | **No carrier.** Mount complete module flat, with antenna face/orientation controlled and kept clear of nearby metal/copper/battery as testing requires. | Photograph front/back and header labels; measure board/antenna dimensions. |
| TX1 XKT-412 | XKT-412 wireless-power transmitter | complete transmitter PCB + external coil | **No carrier.** External base assembly; coil mechanically fixed and centered relative to RX1. | Photograph exact board/coil and record dimensions/pad/connector labels. |
| RX1 XKT receiver | high-current matching receiver sold as 5 V / 2 A; receiver IC marking appears `XKT-3168` | complete receiver PCB + coil | **No carrier.** Module/coil assembly mechanically fixed inside hull; coil must remain flat and aligned to final charging surface. | Photograph front/back/coil, confirm IC marking, pad polarity, actual board/coil dimensions, and loaded output. |

## 3. Lighting parts

### SK6812 RGBW

Project history previously linked a **BTF-LIGHTING 5 V SK6812 RGBW strip using 5050-package LEDs, 144 LEDs/m, black IP30 PCB**. This is useful reconstruction evidence but has not yet been independently re-confirmed against the exact material currently on the bench.

| Property | Current Step-2 status |
|---|---|
| LED technology | SK6812 RGBW — LOCKED |
| Supply | 5 V — LOCKED architecture |
| Reconstructed package | **5050 / 5.0 x 5.0 mm** SK6812 RGBW on flexible strip — RECONSTRUCTED |
| Reconstructed strip | BTF-LIGHTING, 144 LEDs/m, black IP30, 1 m — RECONSTRUCTED historical purchase/link |
| Physical emitter count in Defiant | **OPEN**; do not confuse 9 logical zones with 9 physical LEDs |
| Data topology | one addressable serial bus is the current architecture goal; exact physical emitter order/count to be frozen from hull layout |
| Carrier | **No separate carrier** if LEDs are cut from flexible strip. Cut individual/small strip sections at manufacturer cut points and provide strain relief to fine wires. |

### Pulse-phaser LEDs

Project history previously linked **DiCUNO prewired white 0805 LEDs** with reconstructed specifications: 0805 / 2.0 x 1.25 mm LED, approximately 16 cm leads, up to 20 mA, approximately 240–280 mcd, 20° viewing angle.

| Property | Current Step-2 status |
|---|---|
| Quantity | 4 — LOCKED |
| Package | 0805 / 2012 metric — RECONSTRUCTED |
| Form | prewired LED with fine leads — RECONSTRUCTED |
| Series resistor in leads | **OPEN**; do not assume one exists |
| Carrier | **None.** Mount LED directly at emitter/fiber location with insulated/strain-relieved leads. |

## 4. Purchased carrier boards

| Carrier type | Intended devices | Status |
|---|---|---|
| SOT-23-3 breakout/carrier | AO3400A, AO3401A | purchased; exact board dimensions/pin-label orientation need physical confirmation |
| SOT-23-5 breakout/carrier | SN74AHCT1G125DBVR | purchased; exact board dimensions/pin-label orientation need physical confirmation |
| solderable prototyping board | interconnect, passives, possibly SOD123W diode and carrier interconnection | purchased; exact hole pitch/board dimensions still to inventory |

### Carrier rule

Before any SOT device is soldered, verify the carrier's pad numbering against the **actual semiconductor datasheet pin numbers**. Do not trust silkscreen labels such as `G/S/D` or generic `1/2/3` until continuity/orientation is checked. This prevents mirrored SOT-23 carrier layouts from silently reversing source/drain or logic pins.

## 5. Parts that do not currently need a dedicated carrier

- XIAO ESP32-C3 module
- battery
- XKT transmitter module
- XKT receiver module
- MT3608 boost module
- MFRC522 module
- SK6812 flexible-strip sections
- prewired 0805 LEDs
- axial reed switches

These still require **mechanical mounting/strain relief**, which is handled later in `MECHANICAL-LAYOUT.md`; "no carrier" does not mean "leave loose in the hull."

## 6. Exact package facts that affect the later schematic/assembly

- `SN74AHCT1G125DBVR`: DBV/SOT-23-5; one level-shifter IC per independent SK6812 data line.
- `AO3400A`: SOT-23-3 N-channel MOSFET.
- `AO3401A`: SOT-23-3 P-channel MOSFET.
- `PMEG2010ER,115`: CFP3/SOD123W, **not** SOT-23.
- `NCU18XH103F60RB`: 0603/1608 metric.
- `MDSR-10-15-20`: axial glass through-hole device.
- XIAO: self-contained module; do not create an unnecessary carrier board unless the final mechanical layout specifically benefits from one.

## 7. Step-2 unresolved items

The exact IC-level parts are identified. The remaining unknowns are **physical module variants**, not conceptual architecture gaps:

1. exact MT3608 breakout revision/dimensions/EN accessibility;
2. exact MFRC522 breakout revision and header order;
3. exact XKT receiver/transmitter board and coil dimensions/pad labels;
4. exact currently-owned SK6812 strip/package confirmation and physical emitter count;
5. exact prewired 0805 LED lead/resistor configuration;
6. exact carrier-board layouts/dimensions;
7. exact protoboard dimensions.

These items are deliberately marked OPEN rather than guessed. They can be closed from photographs and measurements before physical layout and final pin-by-pin assembly documentation.

## 8. Step-2 conclusion

**No package/mounting discovery forces a component substitution.** The parts already purchased remain compatible with a hand-wired/carrier-board Defiant build. The tiny SMD parts are manageable specifically because the appropriate SOT carriers were purchased. The only unusual package is the PMEG2010ER SOD123W diode, which must not be placed on a SOT carrier.
