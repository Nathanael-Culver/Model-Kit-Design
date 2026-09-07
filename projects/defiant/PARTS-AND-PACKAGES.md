# USS Defiant — Part Identification, Packages, and Carrier Requirements

**Document status:** STEP 9b PHYSICAL EVIDENCE UPDATE — MAJOR MODULE IDENTIFICATION CLOSED EXCEPT BATTERY PROTECTION

This document answers: what exact part is it, what physical package/form is it, and what does it need in order to be mounted/wired in the Defiant.

## 1. Parts with exact identity/package established

| Ref/class | Exact part | Physical package / size | Mounting / carrier requirement | Status |
|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | XIAO module, 21 x 17.8 mm | no carrier required; preserve antenna clearance | **VERIFIED** |
| BT1 | 103450 Li-Polymer, 3.7 V, 2500 mAh, 9.25 Wh | pouch cell, nominal 10 x 34 x 50 mm | padded/nonconductive restraint; do not clamp/puncture | **VERIFIED identity/electrical/size; protection still OPEN** |
| U2 | adjustable MT3608 boost-converter module, exact current board photographed | complete small module with trimmer and pads visibly labeled `VIN+`, `VIN-`, `VOUT+`, `VOUT-`; no external EN pad visible | no semiconductor carrier; mount complete module with insulated mechanical restraint | **PHYSICAL BOARD VERIFIED** |
| U3 | **black XFW-ETLIVE V602 compact RC522-class reader** | compact 3.3 V SPI reader with integrated PCB antenna; approximately 36 x 25 x 4 mm class | no carrier; mount complete board flat with antenna clearance from metal/copper/battery/charging coil as layout permits | **SELECTED / FROZEN** |
| U4 | TI `SN74AHCT1G125DBVR` | DBV / SOT-23-5 | purchased SOT-23-5 carrier required for hand-wired build; C1 local | **VERIFIED** |
| Q class | AOS `AO3400A` | SOT-23-3 | purchased SOT-23-3 carrier / PCB footprint | **VERIFIED** |
| Q class | AOS `AO3401A` | SOT-23-3 | purchased SOT-23-3 carrier / PCB footprint | **VERIFIED** |
| D1 class | Nexperia `PMEG2010ER,115` | CFP3 / SOD123W | not compatible with SOT carrier; custom/protoboard pads | **VERIFIED** |
| TX1 | **XKT-412 wireless-power transmitter board + flat spiral coil** | small green transmitter PCB; photographed `IN+`/`IN-` supply end and `OUT` coil end | external base assembly; secure board/coil and keep coil flat/centered | **PHYSICALLY IDENTIFIED** |
| RX1 | **XKT-3168 wireless-power receiver board + flat spiral coil** | green receiver PCB with visible `XKT-3168` IC, 330 inductor, rectification/regulation components, factory red/black DC leads | no carrier; mount board/coil flat and mechanically restrained inside hull | **PHYSICALLY IDENTIFIED; output still meter-verify** |

## 2. NFC reader selection

Three RC522-class boards were physically shown on 2026-09-06.

### U3 — selected black XFW-ETLIVE V602

The user explicitly selected the **black XFW-ETLIVE V602** for the Defiant.

Visible header order:

1. SDA / SS / CS
2. SCK
3. MOSI
4. MISO
5. IRQ
6. GND
7. RST
8. 3V3

Relevant board facts:

- 3.3 V SPI reader;
- compact integrated PCB antenna;
- approximately 36 x 25 x 4 mm class;
- photographed IC marking appears consistent with an FM17522/RC522-compatible device;
- IRQ is not required and remains NC.

**Status: FROZEN as U3.** Remaining work is bench validation of reset, read range, unpowered-SPI/backfeed, boot behavior, and wireless-charging coexistence.

### Spare readers

- Green compact RC522 MINI V1.1-style: viable but not selected; retain as spare.
- Large blue standard RFID-RC522: electrically usable but too large for preferred Defiant installation; retain as spare.

## 3. Wireless-power modules — exact pair identified

### TX1 — XKT-412 transmitter

Photographs now establish:

- PCB silk `XKT-412`;
- red/black supply wires terminate at the board end visibly marked `IN+` / `IN-`;
- the opposite end is marked `OUT` and connects to the flat spiral transmitter coil through the resonant network;
- this board is external to the ship and belongs in the charging stand/base.

### RX1 — XKT-3168 receiver

Photographs now establish:

- receiver controller IC marking clearly reads **`XKT-3168`**;
- the flat spiral receive coil is connected at the resonant-input end;
- the opposite end carries factory red/black DC output leads;
- onboard parts include a 330-marked inductor, Schottky/rectifier device and 100 µF-class capacitors consistent with regulated receiver output circuitry.

**What remains open is electrical characterization, not identification:**

1. meter-confirm red lead positive / black lead negative before any connection;
2. measure unloaded receiver voltage at best alignment and while misaligned;
3. measure loaded voltage/current and heating;
4. validate the R1/R2 `WLC_PRESENT` divider against the highest measured raw voltage;
5. only then connect RX1 to D1/U1 and the wake detector.

## 4. Addressable lighting — exact stock confirmed

Exact current stock:

- **BTF-LIGHTING SK6812 RGBW Natural White**
- DC 5 V
- 144 LEDs/m
- 3.28 ft / 1 m
- IP30
- black PCB
- individually addressable RGBW
- 5050-class package on flexible strip

The product image shows each cuttable pixel section carrying local SMD support components. During actual cutting, retain the complete manufacturer-defined pixel section and its local components.

| Property | Status |
|---|---|
| Technology / color | SK6812 RGBW Natural White — **VERIFIED** |
| Supply | 5 V — **VERIFIED** |
| Form | 144 LED/m flexible strip, black IP30 — **VERIFIED** |
| Local support components | visible per section — **VERIFIED FORM** |
| Physical emitter count in Defiant | **OPEN** |
| Data topology | one serial bus — **FROZEN** |

Do not infer physical count from P0–P8.

## 5. Pulse-phaser LEDs — exact stock confirmed

Exact product shown:

- DiCUNO pre-wired SMD 0805 white LEDs
- 6.3 in / approximately 16 cm leads
- white: 7000–12000 K
- 240–280 mcd
- 2.8–3.3 V forward-voltage specification
- 20 mA listed current
- 120° beam angle

No series resistor is shown or specified.

### Frozen current limit

For the regulated 5.0 V lighting rail:

- **R6 = R7 = R8 = R9 = 150 Ω**
- minimum power rating: **1/8 W** or greater

At 5.0 V and LED Vf of 2.8–3.3 V, 150 Ω gives approximately **11.3–14.7 mA**.

Before installing all four, verify one physical LED's polarity and diode behavior with a current-limited bench test.

## 6. Battery protection status

The BT1 photograph confirms the exact label and shows a stiff/dark structure under the taped lead end that is **consistent with** an end-mounted protection PCB. However, the photograph does not expose enough circuitry to prove the function.

Therefore:

- identity/capacity are VERIFIED;
- integral protection is **PROBABLE but not yet VERIFIED**;
- do **not** peel or cut the pouch/tape solely to inspect it;
- close this item using a better edge-on lead-end photograph, original seller specification, or other safe evidence.

U5 remains conditional until this is closed.

## 7. Purchased carrier boards

| Carrier type | Intended devices | Status |
|---|---|---|
| SOT-23-3 breakout/carrier | AO3400A, AO3401A | purchased; pad numbering/orientation still continuity-check before soldering |
| SOT-23-5 breakout/carrier | SN74AHCT1G125DBVR | purchased; pad numbering/orientation still continuity-check |
| solderable prototyping board | passives/distribution/SOD123W integration | purchased; exact physical distribution layout still OPEN |

## 8. Step-9b conclusion

Physical evidence now closes almost all module identity questions:

- U2 exact board form and pad labels confirmed.
- U3 black XFW-ETLIVE V602 selected/frozen.
- **TX1 exact XKT-412 transmitter and RX1 exact XKT-3168 receiver are physically identified.**
- exact SK6812 strip confirmed.
- exact pulse-phaser LEDs confirmed; R6–R9 fixed at 150 Ω.

Still open before final drawings: battery protection proof, RX1 electrical characterization, U3 reset/backfeed/boot/read-range/coexistence tests, physical SK6812 emitter count/order, load/thermal tests, carrier orientation, and final distribution layout.
