# USS Defiant — Part Identification, Packages, and Carrier Requirements

**Document status:** STEP 9c — MAJOR PART IDENTIFICATION CLOSED EXCEPT BATTERY PROTECTION

## 1. Exact active parts

| Ref/class | Exact part | Physical package / form | Mounting / carrier requirement | Status |
|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | XIAO module, 21 x 17.8 mm | no carrier; preserve RF antenna clearance | **VERIFIED** |
| BT1 | 103450 Li-Polymer, 3.7 V, 2500 mAh, 9.25 Wh | 10 x 34 x 50 mm pouch cell | padded/nonconductive restraint; do not clamp/puncture | **VERIFIED identity; protection OPEN** |
| U2 | adjustable MT3608 boost module | complete board with `VIN+`, `VIN-`, `VOUT+`, `VOUT-`; no exposed EN | mount complete module with insulation/strain relief | **PHYSICALLY VERIFIED** |
| U3 | black XFW-ETLIVE V602 compact RC522-class reader | compact 3.3 V SPI reader with integrated PCB antenna | no carrier; antenna faces intended crystal approach surface | **SELECTED / FROZEN** |
| U4 | TI `SN74AHCT1G125DBVR` | DBV / SOT-23-5 | purchased SOT-23-5 carrier; C1 local | **VERIFIED** |
| Q class | AOS `AO3400A` | SOT-23-3 | purchased SOT-23-3 carrier / PCB footprint | **VERIFIED** |
| Q class | AOS `AO3401A` | SOT-23-3 | purchased SOT-23-3 carrier / PCB footprint | **VERIFIED** |
| D1 | Nexperia `PMEG2010ER,115` | CFP3 / SOD123W | custom/protoboard pads; not SOT carrier | **VERIFIED** |
| TX1 | XKT-412 wireless-power transmitter + flat spiral coil | small transmitter PCB; `IN+`/`IN-` input and `OUT` coil connection visible | external charging base | **PHYSICALLY IDENTIFIED** |
| RX1 | XKT-3168 wireless-power receiver + flat spiral coil | receiver PCB with factory red/black DC leads | mount board/coil flat against charging surface area | **PHYSICALLY IDENTIFIED** |

## 2. U3 — selected NFC reader

Black XFW-ETLIVE V602 is the sole active Defiant reader.

Visible header order:

1. SDA / SS / CS
2. SCK
3. MOSI
4. MISO
5. IRQ
6. GND
7. RST
8. 3V3

IRQ remains NC. Green compact RC522 MINI V1.1 and large blue standard RC522 are spares only.

## 3. Wireless-power pair

### TX1

- PCB silk `XKT-412`.
- `IN+` / `IN-` are the supply end.
- `OUT` drives the flat spiral transmitter coil.
- external to ship.

### RX1

- receiver IC marking `XKT-3168` physically confirmed.
- flat spiral coil at resonant input end.
- factory red/black leads are the selected 5 V DC output leads.
- electrical load/thermal/polarity acceptance remains an integrated bench step, not a design-selection question.

## 4. Addressable lighting — exact stock and quantity frozen

Exact stock:

- BTF-LIGHTING SK6812 RGBW Natural White
- DC 5 V
- 144 LEDs/m
- 1 m / 3.28 ft
- IP30 black PCB
- individually addressable RGBW
- 5050-class package on flexible strip

**Defiant physical quantity is now frozen at 14 emitters: LED14–LED27.**

| Property | Status |
|---|---|
| Technology/color | SK6812 RGBW Natural White — VERIFIED |
| Supply | 5 V — VERIFIED |
| Form | 144 LED/m flexible strip — VERIFIED |
| Physical count | **14 — FROZEN** |
| Logical zones | 9, P0–P8 — FROZEN |
| Data topology | one serial bus — FROZEN |
| Physical order | LED14–LED27 — FROZEN in `LIGHTING-LAYOUT.md` |

Retain each complete manufacturer-defined cuttable pixel section and its local SMD support components.

## 5. Pulse-phaser LEDs

Exact stock:

- DiCUNO pre-wired SMD 0805 white LEDs
- 6.3 in / ~16 cm leads
- 7000–12000 K
- 240–280 mcd
- 2.8–3.3 V
- 20 mA listed
- 120° beam angle

Frozen current limit:

- R6 = R7 = R8 = R9 = **150 Ω, >=1/8 W**.

## 6. Battery protection status

BT1 identity/capacity are verified. Lead-end construction appears consistent with an end-mounted protection PCB but does not prove it.

- integral protection: **PROBABLE / NOT VERIFIED**;
- do not peel/cut the pouch or tape solely to inspect it;
- U5 remains conditional until safe evidence closes this item.

## 7. Purchased carrier boards

| Carrier | Intended devices | Status |
|---|---|---|
| SOT-23-3 breakout | AO3400A / AO3401A | purchased; pad orientation continuity-check before soldering |
| SOT-23-5 breakout | SN74AHCT1G125DBVR | purchased; pad orientation continuity-check |
| solderable prototyping board | passives/distribution/SOD123W/carrier interconnect | purchased; final board partition/layout OPEN |

## 8. Current conclusion

No active-component substitution is required. The physical SK6812 count is no longer open: **14 pixels**. Remaining work is physical placement, power distribution, harness sizing/lengths, battery-protection proof, carrier verification, and integrated bench acceptance.
