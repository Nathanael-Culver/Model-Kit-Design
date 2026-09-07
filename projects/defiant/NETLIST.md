# USS Defiant — Authoritative Netlist

**Document status:** **FORMAL v1.3 — Step-9b physical evidence incorporated / NOT YET DRAWING-APPROVED**  
**Architecture source:** `POWER-ARCHITECTURE.md` FROZEN v1.1  
**Designator source:** `DESIGNATORS.md` FROZEN v1.3  
**Pin source:** `PINOUT.md` FROZEN v1.0  
**Drawing use:** PROHIBITED until physical validation closes the remaining blockers.

## 1. U1 XIAO ESP32-C3 — frozen signal assignment

| XIAO pin | GPIO | Net | Direction |
|---|---:|---|---|
| D0 | GPIO2 | `NFC_MISO` | input |
| D1 | GPIO3 | `WLC_PRESENT` | input / deep-sleep wake |
| D2 | GPIO4 | `PH0_GATE` | output |
| D3 | GPIO5 | `PH1_GATE` | output |
| D4 | GPIO6 | `PH2_GATE` | output |
| D5 | GPIO7 | `PH3_GATE` | output |
| D6 | GPIO21 | `NFC_CS` | output |
| D7 | GPIO20 | `PERIPH_EN` | output |
| D8 | GPIO8 | `NFC_SCK` | output |
| D9 | GPIO9 | `SK_DATA_RAW` | output |
| D10 | GPIO10 | `NFC_MOSI` | output |

No spare exposed GPIO remains.

## 2. Battery / protection branch

If BT1 has integral protection, U5 is DNP:

- BT1 positive -> `BAT+`
- BT1 negative -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

If BT1 is unprotected, U5 must be fitted:

- BT1 positive -> `CELL+` -> U5 B+
- BT1 negative -> `CELL-` -> U5 B-
- U5 P+ -> `BAT+`
- U5 P- -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

Current photograph strongly suggests an end-mounted protection PCB but does not prove it; this branch decision remains OPEN.

## 3. Common ground

`GND` connects U1, RX1 negative, U2 IN-/OUT-, U3 GND, U4 pin 3, Q2/Q3/Q4/Q5/Q6/Q8 sources, all SK6812 grounds, sensing-divider return, pull-down resistors, and capacitor returns.

Q9 is DNP and has no electrical connection.

## 4. Wireless-power / charging path

- RX1 positive -> `WLC_5V_RAW`
- RX1 negative -> `GND`
- D1 anode -> `WLC_5V_RAW`
- D1 cathode / marked-bar end -> `SYS_5V_IN`
- `SYS_5V_IN` -> U1 5 V external-input pin/pad

D1 permits RX1 -> U1 current and blocks reverse feed toward RX1.

## 5. Wireless-present detector / wake

- R1 = 130 kΩ: `WLC_5V_RAW` -> `WLC_PRESENT`
- R2 = 180 kΩ: `WLC_PRESENT` -> `GND`
- `WLC_PRESENT` -> U1 D1 / GPIO3 only

Approved v1 wake policy:

- applying/enabling wireless charging wakes the ship;
- Wi-Fi/BLE/NFC do not wake U1 from deep sleep.

Actual RX1 maximum output voltage remains to be measured before attaching this divider to U1.

## 6. Lighting input power gate

### Q1 AO3401A

- source -> `BAT+`
- drain -> `U2_VIN_SW`
- gate -> `LIGHT_GATE`

### R3

- 100 kΩ: `LIGHT_GATE` -> `BAT+`

### Q2 AO3400A

- drain -> `LIGHT_GATE`
- source -> `GND`
- gate -> `PERIPH_EN`

### R4

- 100 kΩ: `PERIPH_EN` -> `GND`

`PERIPH_EN` -> U1 D7/GPIO20.

## 7. U2 MT3608 — physical board identified

Photographed U2 is the common adjustable MT3608 board with visible pads:

- `VIN+` -> `U2_VIN_SW`
- `VIN-` -> `GND`
- `VOUT+` -> `+5V_LIGHT_SW`
- `VOUT-` -> `GND`

No external EN pad is visible on the actual board. The design therefore retains the already-frozen Q1/Q2 battery-side input disconnect; do not modify the MT3608 IC itself for normal assembly.

Adjust/load-test U2 to 5.0 V before LEDs are connected.

## 8. +5 V lighting rail

`+5V_LIGHT_SW` feeds:

- U4 pin 5
- all physical SK6812 VDD pins
- R6–R9 phaser branches
- C2 positive

C2 target = 470 µF, >=6.3 V; 10 V preferred if size permits.

## 9. U4 SN74AHCT1G125

| U4 pin | Connection |
|---:|---|
| 1 OE | `GND` |
| 2 A | `SK_DATA_RAW` = U1 D9/GPIO9 |
| 3 GND | `GND` |
| 4 Y | `SK_DATA_5V` |
| 5 VCC | `+5V_LIGHT_SW` |

- C1 = 0.1 µF ceramic between VCC and GND, local to U4.
- R5 = 330 Ω from `SK_DATA_5V` to `SK_DIN_FIRST`.

## 10. Physical SK6812 chain — exact strip verified

Exact stock is BTF-LIGHTING SK6812 RGBW Natural White, 5 V, 144 LED/m, black IP30 flexible strip.

One serial chain only:

```text
SK_DIN_FIRST -> LED14 DIN
LED14 DOUT -> LED15 DIN
LED15 DOUT -> LED16 DIN
... -> final physical SK6812
```

Every physical SK6812 section:

- VDD -> `+5V_LIGHT_SW`
- GND -> `GND`
- retain the complete manufacturer-defined cut section and its local SMD support components

Physical emitter count/order remains OPEN. P0–P8 are firmware logical zones and may map to one or multiple physical emitters.

## 11. Pulse-phaser channels — current limiting closed

Exact LEDs are DiCUNO prewired white 0805 devices, listed 2.8–3.3 V forward voltage and 20 mA maximum/listed current. No series resistor is specified or shown in the prewired product.

Use **150 Ω, >=1/8 W** for each channel. At 5.0 V this gives approximately 11.3–14.7 mA across the listed Vf range.

### PH0

- `+5V_LIGHT_SW` -> **R6 = 150 Ω** -> LED10 anode
- LED10 cathode -> Q3 drain
- Q3 source -> `GND`
- Q3 gate -> `PH0_GATE` -> U1 D2/GPIO4
- R10 = 100 kΩ `PH0_GATE` -> `GND`

### PH1

- `+5V_LIGHT_SW` -> **R7 = 150 Ω** -> LED11 anode
- LED11 cathode -> Q4 drain
- Q4 source -> `GND`
- Q4 gate -> `PH1_GATE` -> U1 D3/GPIO5
- R11 = 100 kΩ `PH1_GATE` -> `GND`

### PH2

- `+5V_LIGHT_SW` -> **R8 = 150 Ω** -> LED12 anode
- LED12 cathode -> Q5 drain
- Q5 source -> `GND`
- Q5 gate -> `PH2_GATE` -> U1 D4/GPIO6
- R12 = 100 kΩ `PH2_GATE` -> `GND`

### PH3

- `+5V_LIGHT_SW` -> **R9 = 150 Ω** -> LED13 anode
- LED13 cathode -> Q6 drain
- Q6 source -> `GND`
- Q6 gate -> `PH3_GATE` -> U1 D5/GPIO7
- R13 = 100 kΩ `PH3_GATE` -> `GND`

Before duplicating all four physical channels, verify one actual LED's polarity and operation with current limiting; R6–R9 no longer remain unspecified.

## 12. NFC high-side gate

### Q7 AO3401A

- source -> `+3V3_ALWAYS`
- drain -> `+3V3_NFC_SW`
- gate -> `NFC_GATE`

### R14

- 100 kΩ: `NFC_GATE` -> `+3V3_ALWAYS`

### Q8 AO3400A

- drain -> `NFC_GATE`
- source -> `GND`
- gate -> `NFC_EN_GATE`

### R15 / R16

- R15 = 10 kΩ: `PERIPH_EN` -> `NFC_EN_GATE`
- R16 = 100 kΩ: `NFC_EN_GATE` -> `GND`

Q9 is DNP. Therefore `NFC_POWER = PERIPH_EN`, including while wireless charging is active.

## 13. U3 compact RC522-class reader

The large blue standard RC522 is mechanically disfavored and not the intended final U3.

Two compact boards on hand fit the frozen electrical interface:

### Primary candidate — black XFW-ETLIVE V602

Visible header order:

1. SDA / SS / CS
2. SCK
3. MOSI
4. MISO
5. IRQ
6. GND
7. RST
8. 3V3

- IRQ -> NC
- other functions map directly to the nets below
- integrated antenna / compact board class
- board family is approximately 36 x 25 x 4 mm
- photographed IC appears RC522-compatible / FM17522-class; bench firmware-version readback required

### Alternate — green RC522 MINI V1.1-style

Visible header order:

1. NSS
2. SCK
3. MOSI
4. MISO
5. RST
6. GND
7. 3.3V

No IRQ is exposed, which is acceptable because IRQ is unused.

### Frozen functional mapping for either compact board

| U3 function | Net | U1 endpoint |
|---|---|---|
| VCC / 3.3 V | `+3V3_NFC_SW` | switched supply |
| GND | `GND` | GND |
| SCK | `NFC_SCK` | D8 / GPIO8 |
| MOSI | `NFC_MOSI` | D10 / GPIO10 |
| MISO | `NFC_MISO` | D0 / GPIO2 |
| SDA/SS/NSS/CS | `NFC_CS` | D6 / GPIO21 |
| IRQ | NC if present | none |
| RST | reset-bias network | none |

### R17

- target 10 kΩ from U3 RST -> `+3V3_NFC_SW`
- may become DNP if the selected compact board already provides suitable reset bias and power-cycle behavior

### R18

- 10 kΩ from `NFC_MISO` / U1 D0/GPIO2 -> `+3V3_ALWAYS`

Final black-vs-green selection is a bench/mechanical choice based on read range, reset behavior, unpowered-SPI backfeed, and fit—not an architecture change.

## 14. Required reset/deep-sleep states

| Net | Required hardware state |
|---|---|
| `PERIPH_EN` | LOW via R4 |
| `LIGHT_GATE` | HIGH to BAT+ via R3 -> Q1 OFF |
| PH0–PH3 gates | LOW via R10–R13 |
| `NFC_GATE` | HIGH via R14 -> Q7 OFF |
| `NFC_EN_GATE` | LOW via R16 |
| `WLC_PRESENT` | LOW via R2 when RX1 absent |
| `NFC_MISO` / D0 | HIGH-biased via R18 when U3 not driving |
| `+5V_LIGHT_SW` | OFF |
| `+3V3_NFC_SW` | OFF |

## 15. Remaining blockers before drawing approval

1. BT1 protection/discharge capability proof;
2. RX1 pad identity/loaded voltage/current/temperature;
3. D1 charging/recovery/reverse-current/thermal test;
4. U2 load/thermal test and Q1 carrier-current test;
5. compact U3 black-vs-green selection after backfeed/reset/read-range test;
6. D0/D8 boot safety with selected U3 attached/off;
7. D9 boot safety with U4 attached/off;
8. D1/GPIO3 wireless deep-sleep wake test;
9. physical SK6812 emitter count/order and full lighting load;
10. integrated charging/NFC coexistence and final distribution implementation.

## 16. Current conclusion

The exact MT3608 board form, addressable-strip product, and phaser LED product are now identified. The only prior electrical `ERROR`—phaser current limiting—is closed with R6–R9 = 150 Ω. Two compact RC522 boards are viable without changing the frozen GPIO map or architecture.
