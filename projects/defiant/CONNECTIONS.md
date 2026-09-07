# USS Defiant — Per-Component Connection Tables

**Document status:** PARTIAL / NOT APPROVED  
Every physical electrical pin must eventually have exactly one of: named net, `NC`, `DNP`, or explicit test-only assignment.

## U1 — Seeed Studio XIAO ESP32-C3

| Pin/pad | ESP GPIO | Current net | Status/notes |
|---|---:|---|---|
| BAT+ pad | — | `BAT+` | LOCKED |
| BAT- pad | — | `GND` | LOCKED |
| 5V/VBUS | — | `OPEN_SYS_5V_IN` | PROVISIONAL wireless recovery/charging input path |
| 3V3 | — | `+3V3_ALWAYS` | PROVISIONAL net name; actual load budget to validate |
| GND | — | `GND` | LOCKED |
| D0 | GPIO2 | OPEN | wake-capable; strapping pin; Candidate A=`NFC_MISO` |
| D1 | GPIO3 | OPEN | wake-capable; Candidate A=`WLC_PRESENT` |
| D2 | GPIO4 | OPEN | wake-capable; Candidate A=`PH0_GATE` |
| D3 | GPIO5 | OPEN | wake-capable; Candidate A=`PH1_GATE` |
| D4 | GPIO6 | OPEN | Candidate A=`PH2_GATE` |
| D5 | GPIO7 | OPEN | Candidate A=`PH3_GATE` |
| D6 | GPIO21 | OPEN | UART0 TX at boot; Candidate A=`NFC_CS` only while NFC rail is off during boot |
| D7 | GPIO20 | OPEN | Candidate A=`PERIPH_PWR_EN` |
| D8 | GPIO8 | OPEN | strapping pin; Candidate A=`NFC_SCK` |
| D9 | GPIO9 | OPEN | BOOT strapping pin; Candidate A=`SK_DATA_RAW`; must not be pulled low at reset |
| D10 | GPIO10 | OPEN | Candidate A=`NFC_MOSI` |
| RESET | CHIP_EN | no permanent external connection planned | service/test access only if mechanically feasible |
| BOOT | GPIO9 switch | onboard function | do not obstruct boot behavior |

## BT1 — 103450 LiPo

| Pin/lead | Net | Status |
|---|---|---|
| + | `BAT+` | LOCKED |
| - | `GND` | LOCKED |

## RX1 — XKT wireless-power receiver

Exact board must be photographed before pin names are treated as verified.

| Pad | Net | Status |
|---|---|---|
| positive output pad | `WLC_5V_RAW` | FUNCTION LOCKED / physical label OPEN |
| negative output pad | `GND` | FUNCTION LOCKED / physical label OPEN |
| coil pads/leads | receiver coil | purchased assembly; exact labels OPEN |

## U2 — MT3608 boost-converter module

Module-level pads must be verified from the exact board.

| Module pad | Net | Status |
|---|---|---|
| IN+ | `BAT+` through selected gate topology | OPEN implementation |
| IN- | `GND` | expected / verify board |
| OUT+ | `+5V_LIGHT_SW` | LOCKED function |
| OUT- | `GND` | expected / verify board |
| EN | `OPEN_LIGHT_PWR_EN` if accessible | OPEN; bare MT3608 IC pin 4 is EN, but board access unknown |

Bare MT3608 IC reference only: pin 1 SW, pin 2 GND, pin 3 FB, pin 4 EN, pin 5 VIN, pin 6 NC. Do not wire to IC pins unless the purchased module is intentionally modified.

## U3 — MFRC522 breakout

Exact header spelling/order must be verified physically. Required functions are:

| Function | Net | Status |
|---|---|---|
| 3.3 V/VCC | `+3V3_NFC_SW` | LOCKED function |
| GND | `GND` | LOCKED |
| SCK | `NFC_SCK` | required |
| MOSI | `NFC_MOSI` | required |
| MISO | `NFC_MISO` | required |
| SDA/SS/CS | `NFC_CS` | required; exact breakout label to verify |
| RST | `OPEN_NFC_RST` | OPEN; Candidate A uses switched-power reset/pull network |
| IRQ | NC unless future architecture explicitly uses it | provisional NC |

## U4 — SN74AHCT1G125DBVR

Exact pinout verified for DBV/SOT-23-5.

| Pin | Name | Net | Status |
|---:|---|---|---|
| 1 | OE | `OPEN_SK_BUF_OE` | OPEN; active low |
| 2 | A | `OPEN_SK_DATA_RAW` | OPEN until final GPIO/chain allocation |
| 3 | GND | `GND` | VERIFIED |
| 4 | Y | `OPEN_SK_DATA_5V` | OPEN until final chain allocation |
| 5 | VCC | `+5V_LIGHT_SW` | intended / PROVISIONAL until chain count frozen |

Additional buffers will receive U5, U6... only if final chain count requires them.

## AO3400A inventory — future Q designators

Exact SOT-23 pin identity for AO3400A:

| Pin | Name |
|---:|---|
| 1 | Gate |
| 2 | Source |
| 3 | Drain |

No specific Q number/net is assigned until power/phaser topology freezes.

## AO3401A inventory — future Q designators

Exact SOT-23 pin identity for AO3401A:

| Pin | Name |
|---:|---|
| 1 | Gate |
| 2 | Source |
| 3 | Drain |

No specific Q number/net is assigned until power-gate topology freezes.

## D inventory — PMEG2010ER,115

| Pin | Name | Net | Status |
|---:|---|---|---|
| 1 | K / cathode | OPEN | marking bar side; candidate downstream side of wireless-input isolation |
| 2 | A / anode | OPEN | candidate `WLC_5V_RAW` side |

A diode receives a final D designator only when its circuit position is approved.

## LED1–LED9 — SK6812 logical pixels

Physical SK6812 package pin numbering is OPEN until the exact purchased form is identified. Logical requirements for every pixel:

- VDD -> `+5V_LIGHT_SW`
- GND -> `GND`
- DIN/DOUT -> chain topology to be frozen

Logical assignments are fixed in `NETLIST.md` / `STATUS.md` as P0–P8.

## LED10–LED13 — prewired 0805 white pulse phasers

| Lead | Net | Status |
|---|---|---|
| anode | OPEN phaser supply/current-limit net | exact prewire resistance unknown |
| cathode | OPEN switched sink net | exact switching topology OPEN |

Do not infer polarity from wire color until one sample is electrically verified.
