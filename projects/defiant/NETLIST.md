# USS Defiant — Authoritative Netlist

**Document status:** DRAFT v0.1 / NOT APPROVED  
**Drawing use:** PROHIBITED until this file is marked APPROVED.

This file is the textual electrical source of truth. A drawing may improve readability but may not invent or alter a connection.

## 1. Net naming rules

- power: `BAT+`, `+3V3_*`, `+5V_*`, `GND`
- MCU signals: functional uppercase names such as `WLC_PRESENT`, `PH0_GATE`
- SPI: `NFC_SCK`, `NFC_MOSI`, `NFC_MISO`, `NFC_CS`
- LED data: `SK_DATA_RAW`, `SK_DATA_5V`, and inter-pixel `SK_DOUT_n`
- switched control: `PERIPH_PWR_EN` or separate names if architecture requires them
- unresolved nets are prefixed `OPEN_` and must not appear in released drawings

## 2. Locked / verified net segments

These connections follow directly from locked requirements or exact component identity.

### `GND`

Required common reference connecting:

- BT1 negative
- U1 GND
- RX1 output negative/reference once pad identity is physically verified
- U2 input/output ground
- U3 GND
- all SK6812 grounds
- all pulse-phaser switch returns
- U4 pin 3 GND and any additional logic-buffer grounds
- sensing-divider ground

**Validation:** no isolated logic ground is permitted unless explicitly introduced later.

### `BAT+`

- BT1 positive -> U1 battery positive pad: **LOCKED**
- BT1 positive -> lighting-boost input/gate path: **LOCKED FUNCTION, exact switching endpoints OPEN**

### `WLC_5V_RAW`

- RX1 positive output -> `WLC_5V_RAW`: **FUNCTION LOCKED, exact receiver pad label OPEN**
- branch to wireless-presence detector: **LOCKED FUNCTION**
- branch to validated XIAO charging/external-input isolation path: **LOCKED FUNCTION, exact diode/pad endpoints PROVISIONAL**

### `+5V_LIGHT_SW`

Source: U2 boost-converter output after the selected enable/gating topology.  
Consumers:

- all SK6812 VDD pins
- SN74AHCT1G125 buffer VCC pins serving SK6812 chains
- any pulse-phaser LED supply only if final current design chooses the 5 V rail

Behavior: **must be 0/off during deep sleep.**

### `+3V3_NFC_SW`

Source: switched 3.3 V path.  
Consumer: U3 MFRC522 module VCC/3.3 V input.  
Behavior: **must be off during deep sleep.**

## 3. Exact logic-buffer pin identity

For each `SN74AHCT1G125DBVR` used:

| Pin | Name | Net rule |
|---:|---|---|
| 1 | OE | active-low enable; final net TBD; must not allow unwanted LED data during unsafe power states |
| 2 | A | corresponding 3.3 V MCU raw data net |
| 3 | GND | `GND` |
| 4 | Y | corresponding 5 V SK6812 data net |
| 5 | VCC | `+5V_LIGHT_SW` |

Each buffer requires local bypassing in the final passive netlist; capacitor value/designator remains OPEN pending inventory reconstruction.

## 4. Reconstructed lighting logical map

The following logical pixel identities are preserved regardless of physical wiring topology:

| Ref | Logical index | Function |
|---|---:|---|
| LED1 | P0 | deflector top + bottom |
| LED2 | P1 | port bussard |
| LED3 | P2 | starboard bussard |
| LED4 | P3 | port warp chiller/grille |
| LED5 | P4 | starboard warp chiller/grille |
| LED6 | P5 | port impulse crystals, both |
| LED7 | P6 | starboard impulse crystals, both |
| LED8 | P7 | port impulse engine |
| LED9 | P8 | starboard impulse engine |

Pulse phasers:

| Ref | Logical name |
|---|---|
| LED10 | PH0 |
| LED11 | PH1 |
| LED12 | PH2 |
| LED13 | PH3 |

## 5. Candidate one-chain SK6812 net segment — NOT APPROVED

This is retained only because the MCU pin budget makes chain count architecture-critical. Do not treat it as the accepted physical chain until the prior decision is verified.

```text
U1 SK_DATA_RAW -> U4 pin 2 A
U4 pin 4 Y -> R_DATA -> LED1 DIN
LED1 DOUT -> LED2 DIN
LED2 DOUT -> LED3 DIN
LED3 DOUT -> LED4 DIN
LED4 DOUT -> LED5 DIN
LED5 DOUT -> LED6 DIN
LED6 DOUT -> LED7 DIN
LED7 DOUT -> LED8 DIN
LED8 DOUT -> LED9 DIN
LED9 DOUT -> no connection / test pad optional
```

All LED1–LED9 VDD -> `+5V_LIGHT_SW`; all grounds -> `GND`.

Historical data resistor value: 330 Ω, pending final verification and designator assignment.

## 6. Phaser channels — topology requirement, endpoints OPEN

Each PH0–PH3 must be independently controllable and default OFF at reset/deep sleep.

Expected channel form using already-purchased switching parts if the prewired LEDs require external low-side switching:

```text
LED supply -> current limiting as required -> LED anode
LED cathode -> N-channel MOSFET drain
MOSFET source -> GND
MCU PHx_GATE -> gate network -> MOSFET gate
```

Do **not** assign resistor values until the actual prewired 0805 LED forward voltage/current and any built-in series resistor are verified.

## 7. MFRC522 interface requirement

Minimum SPI nets:

- `NFC_SCK`
- `NFC_MOSI`
- `NFC_MISO`
- `NFC_CS`
- `GND`
- `+3V3_NFC_SW`

`RST` handling is OPEN. Candidate A in `PINOUT.md` ties reset into the switched-power reset behavior rather than consuming another GPIO. `IRQ` is not currently required unless a future low-power architecture explicitly needs it.

## 8. Power-gate netlist branches — OPEN pending module inspection

### U2 lighting rail

Exactly one of these will become authoritative:

- `U2_EN_CONTROL`: MCU controls MT3608 EN if usable on purchased module; or
- `U2_INPUT_GATE`: AO3401A/AO3400A hardware high-side gate physically disconnects U2 VIN.

### U3 NFC rail

Expected high-side switch between `+3V3_ALWAYS` and `+3V3_NFC_SW`; final Q/R pins and control polarity remain OPEN.

## 9. Wireless-presence detector — OPEN component values

Required logical connection:

```text
WLC_5V_RAW -> voltage-limiting/divider network -> WLC_PRESENT -> wake-capable U1 GPIO
                                      |
                                     GND
```

Constraints:

- GPIO node must remain within ESP32-C3 absolute/recommended input range.
- divider leakage must be acceptable when wireless power is absent/present.
- selected pin must wake from deep sleep.
- detector must not corrupt boot straps.

## 10. Netlist blockers

This file cannot advance to APPROVED until:

- exact RX1, U2 and U3 module pin labels are photographed/verified;
- SK6812 physical chain count is confirmed;
- U1 approved GPIO allocation exists;
- power-gate topology is frozen;
- passive values are assigned;
- phaser LED electrical properties are verified;
- every component pin in `CONNECTIONS.md` has a defined net or explicit NC/DNP state;
- `VALIDATION.md` reports no ERROR items.
