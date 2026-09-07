# USS Defiant — Authoritative Netlist

**Document status:** **FORMAL v1.0 — TOPOLOGY COMPLETE / NOT YET DRAWING-APPROVED**  
**Architecture source:** `POWER-ARCHITECTURE.md` FROZEN v1.0  
**Designator source:** `DESIGNATORS.md` FROZEN v1.0  
**Drawing use:** PROHIBITED until Step 6 pin assignment, physical module verification, and Step 9 validation close the remaining blockers.

This file is the textual electrical source of truth. Drawings may only represent connections listed here; they may not invent or alter them.

## 1. Net naming rules

- power: `CELL+`, `CELL-`, `BAT+`, `+3V3_ALWAYS`, `+3V3_NFC_SW`, `+5V_LIGHT_SW`, `WLC_5V_RAW`, `SYS_5V_IN`, `GND`
- MCU signals: `PERIPH_EN`, `WLC_PRESENT`, `PH0_GATE`–`PH3_GATE`
- NFC SPI: `NFC_SCK`, `NFC_MOSI`, `NFC_MISO`, `NFC_CS`
- LED data: `SK_DATA_RAW`, `SK_DATA_5V`, `SK_DIN_FIRST`, and sequential inter-emitter data nets
- internal gate nodes: `LIGHT_GATE`, `NFC_GATE`, `NFC_EN_GATE`

Actual XIAO D0–D10 pin assignment is intentionally deferred to Step 6.

## 2. Battery / protection branch

### If BT1 is confirmed to contain integral protection — U5 DNP

- BT1 positive -> `BAT+`
- BT1 negative -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

### If BT1 is confirmed unprotected — U5 fitted

- BT1 positive -> `CELL+`
- BT1 negative -> `CELL-`
- `CELL+` -> U5 B+
- `CELL-` -> U5 B-
- U5 protected output P+ -> `BAT+`
- U5 protected output P- -> `GND`
- `BAT+` -> U1 BAT+
- `GND` -> U1 BAT-

Only one of these branches is assembled. U5 is never bypassed if an unprotected cell is used.

## 3. Common ground — `GND`

Connects:

- U1 GND / BAT-
- RX1 negative output/reference
- U2 IN- and OUT- / module ground
- U3 GND
- U4 pin 3
- Q2/Q3/Q4/Q5/Q6/Q8/Q9 sources
- all SK6812 grounds
- R2 lower end
- R4, R10–R13, R16 lower ends
- C1 and C2 negative/ground terminals
- any fitted U5 protected negative output P-

No intentionally isolated logic ground exists in this design.

## 4. Wireless-power / charging path

### RX1

- RX1 positive output -> `WLC_5V_RAW`
- RX1 negative output -> `GND`

Exact physical pad labels remain to be verified before soldering.

### D1 — PMEG2010ER Schottky isolation

- D1 **anode** -> `WLC_5V_RAW`
- D1 **cathode / marked-bar end** -> `SYS_5V_IN`
- `SYS_5V_IN` -> U1 5 V external-input pin/pad

This orientation permits wireless receiver current toward U1 while blocking reverse feed from U1's 5 V node toward RX1.

## 5. Wireless-present detector

- R1 = **130 kΩ**: `WLC_5V_RAW` -> `WLC_PRESENT`
- R2 = **180 kΩ**: `WLC_PRESENT` -> `GND`
- `WLC_PRESENT` -> U1 wake-capable GPIO, exact pin Step 6
- `WLC_PRESENT` -> Q9 gate

Nominal divider behavior:

- 4.5 V receiver output -> ~2.61 V at `WLC_PRESENT`
- 5.0 V -> ~2.90 V
- 5.5 V -> ~3.19 V
- 6.0 V -> ~3.48 V

This satisfies the ESP32-C3 3.3 V-domain logic-high requirement across the intended 5 V receiver range while remaining below the 3.6 V absolute input limit through approximately 6.2 V. RX1 must still be measured before final approval.

## 6. Lighting input power gate

### Q1 — AO3401A P-channel high-side switch

- Q1 source -> `BAT+`
- Q1 drain -> `U2_VIN_SW`
- Q1 gate -> `LIGHT_GATE`

### R3 — Q1 default-off pull-up

- R3 = **100 kΩ**: `LIGHT_GATE` -> `BAT+`

### Q2 — AO3400A Q1 gate helper

- Q2 drain -> `LIGHT_GATE`
- Q2 source -> `GND`
- Q2 gate -> `PERIPH_EN`

### R4 — Q2 default-off pull-down

- R4 = **100 kΩ**: `PERIPH_EN` / Q2 gate -> `GND`

Therefore:

- `PERIPH_EN = LOW/floating` -> Q2 off -> R3 pulls Q1 gate to BAT+ -> U2 disconnected
- `PERIPH_EN = HIGH` -> Q2 on -> Q1 gate pulled low -> U2 connected to BAT+

## 7. U2 MT3608 lighting rail

Functional module pads:

- U2 IN+ -> `U2_VIN_SW`
- U2 IN- -> `GND`
- U2 OUT+ -> `+5V_LIGHT_SW`
- U2 OUT- -> `GND`

U2 is adjusted to **5.0 V output before lighting is attached**.

The design does not rely on MT3608 EN for sleep isolation. Any EN pin present on the exact board remains in the board's normal enabled configuration unless bench inspection proves a required change.

## 8. +5 V lighting distribution

`+5V_LIGHT_SW` feeds:

- U4 pin 5 VCC
- every physical SK6812 VDD
- LED10–LED13 anode/current-limit branches
- C2 positive terminal

C2 target = **470 µF**, polarized bulk capacitor, rated **at least 6.3 V; 10 V preferred if physical size permits**. Final capacitance may be increased after physical SK6812 count/load testing without changing C2's designator/function.

## 9. U4 SK6812 level shifter

U4 = SN74AHCT1G125DBVR:

| U4 pin | Device pin | Connection |
|---:|---|---|
| 1 | OE, active low | `GND` — hardware enabled whenever U4 is powered |
| 2 | A | `SK_DATA_RAW` from U1 GPIO assigned in Step 6 |
| 3 | GND | `GND` |
| 4 | Y | `SK_DATA_5V` |
| 5 | VCC | `+5V_LIGHT_SW` |

The AHCT input is over-voltage tolerant with VCC from 0–5.5 V, so the always-powered 3.3 V MCU data pin does not require a separate power-off isolation device when U4's switched 5 V supply is absent.

### C1 — U4 local bypass

- C1 = **0.1 µF ceramic**
- C1 one side -> U4 pin 5 / `+5V_LIGHT_SW`
- C1 other side -> U4 pin 3 / `GND`
- place physically next to U4 carrier

### R5 — SK6812 series data resistor

- R5 = **330 Ω**
- R5 input -> `SK_DATA_5V`
- R5 output -> `SK_DIN_FIRST`

330 Ω is now the formal starting value, consistent with the reconstructed design and normal addressable-LED data-line practice. Change only if bench integrity testing proves necessary.

## 10. Physical SK6812 serial chain

The architecture has exactly **one data chain**, but the exact physical emitter count/order is still a mechanical-layout input.

Physical references begin at LED14:

```text
SK_DIN_FIRST -> LED14 DIN
LED14 DOUT -> LED15 DIN
LED15 DOUT -> LED16 DIN
...
final physical SK6812 DOUT -> NC unless a later test pad is deliberately assigned
```

For every physical SK6812:

- VDD -> `+5V_LIGHT_SW`
- GND -> `GND`
- DIN/DOUT -> serial chain as above

Logical firmware zones P0–P8 map onto one or more physical emitters; they are not electrical nets and do not determine emitter count.

## 11. Pulse-phaser channels

### PH0

- `+5V_LIGHT_SW` -> R6 -> LED10 anode
- LED10 cathode -> Q3 drain
- Q3 source -> `GND`
- Q3 gate -> `PH0_GATE`
- R10 = **100 kΩ**: `PH0_GATE` -> `GND`

### PH1

- `+5V_LIGHT_SW` -> R7 -> LED11 anode
- LED11 cathode -> Q4 drain
- Q4 source -> `GND`
- Q4 gate -> `PH1_GATE`
- R11 = **100 kΩ**: `PH1_GATE` -> `GND`

### PH2

- `+5V_LIGHT_SW` -> R8 -> LED12 anode
- LED12 cathode -> Q5 drain
- Q5 source -> `GND`
- Q5 gate -> `PH2_GATE`
- R12 = **100 kΩ**: `PH2_GATE` -> `GND`

### PH3

- `+5V_LIGHT_SW` -> R9 -> LED13 anode
- LED13 cathode -> Q6 drain
- Q6 source -> `GND`
- Q6 gate -> `PH3_GATE`
- R13 = **100 kΩ**: `PH3_GATE` -> `GND`

R6–R9 remain **VALUE TBD / CONDITIONAL DNP** until one actual prewired LED is identified/measured. If the prewired LED already contains an appropriate resistor, the corresponding R6–R9 positions become DNP; otherwise all four receive the calculated identical value unless measured LED variation justifies otherwise.

## 12. NFC high-side power gate and wireless inhibit

### Q7 — AO3401A NFC high-side switch

- Q7 source -> `+3V3_ALWAYS`
- Q7 drain -> `+3V3_NFC_SW`
- Q7 gate -> `NFC_GATE`

### R14 — Q7 default-off pull-up

- R14 = **100 kΩ**: `NFC_GATE` -> `+3V3_ALWAYS`

### Q8 — AO3400A Q7 gate helper

- Q8 drain -> `NFC_GATE`
- Q8 source -> `GND`
- Q8 gate -> `NFC_EN_GATE`

### R15 / R16 — Q8 control

- R15 = **10 kΩ**: `PERIPH_EN` -> `NFC_EN_GATE`
- R16 = **100 kΩ**: `NFC_EN_GATE` -> `GND`

### Q9 — AO3400A wireless-power NFC inhibit

- Q9 drain -> `NFC_EN_GATE`
- Q9 source -> `GND`
- Q9 gate -> `WLC_PRESENT`

Behavior:

- PERIPH_EN low -> Q8 off -> Q7 off
- PERIPH_EN high + WLC_PRESENT low -> Q8 on -> Q7 on -> NFC powered
- WLC_PRESENT high -> Q9 clamps Q8 gate low -> Q7 remains off regardless of PERIPH_EN

Thus the hardware truth condition is:

`NFC_POWER = PERIPH_EN AND NOT WLC_PRESENT`

No new logic IC or extra MCU GPIO is used.

## 13. U3 MFRC522 interface

Functional connections, independent of physical header order:

- U3 3.3 V/VCC -> `+3V3_NFC_SW`
- U3 GND -> `GND`
- U3 SCK -> `NFC_SCK`
- U3 MOSI -> `NFC_MOSI`
- U3 MISO -> `NFC_MISO`
- U3 SDA/SS/CS -> `NFC_CS`
- U3 IRQ -> **NC**
- U3 RST/NRSTPD -> reset-bias arrangement below

### R17 — NFC reset bias

- R17 target = **10 kΩ** from U3 RST/NRSTPD -> `+3V3_NFC_SW`
- R17 may become DNP if the exact breakout is confirmed to contain a suitable onboard pull-up and reliably resets from supply cycling

There is no MCU reset GPIO for U3.

Before NFC power is removed, firmware must place MCU SPI outputs into a benign state to avoid signal-pin backfeed. Exact behavior is validated after Step 6 pin assignment and physical U3 verification.

## 14. U1 functional signal list entering Step 6

U1 must provide exactly these 11 signal roles:

1. `WLC_PRESENT` — input / deep-sleep wake
2. `PERIPH_EN` — output, active high
3. `SK_DATA_RAW` — output
4. `PH0_GATE` — output
5. `PH1_GATE` — output
6. `PH2_GATE` — output
7. `PH3_GATE` — output
8. `NFC_SCK` — output
9. `NFC_MOSI` — output
10. `NFC_MISO` — input
11. `NFC_CS` — output

No other MCU GPIO function is permitted without an approved architecture change.

## 15. Net-level default states

| Net | Required hardware state at reset/deep sleep |
|---|---|
| `PERIPH_EN` | LOW via R4 |
| `LIGHT_GATE` | pulled to BAT+ via R3 -> Q1 OFF |
| `PH0_GATE` | LOW via R10 |
| `PH1_GATE` | LOW via R11 |
| `PH2_GATE` | LOW via R12 |
| `PH3_GATE` | LOW via R13 |
| `NFC_GATE` | pulled to +3V3_ALWAYS via R14 -> Q7 OFF |
| `NFC_EN_GATE` | LOW via R16 unless PERIPH_EN actively drives through R15 |
| `WLC_PRESENT` | LOW via R2 when RX1 absent |
| `+5V_LIGHT_SW` | OFF |
| `+3V3_NFC_SW` | OFF |

## 16. Step-5 open items

The electrical topology is now formal. These remaining items prevent the netlist from being marked drawing-APPROVED but do not prevent Step 6:

1. Step 6 actual XIAO D0–D10 assignment.
2. Exact physical SK6812 emitter count/order.
3. R6–R9 values or DNP decision from actual prewired LEDs.
4. Exact RX1 pad polarity/loaded voltage verification.
5. Exact U2 board pad verification and 5 V load test.
6. Exact U3 header/RST-board behavior verification.
7. BT1 protected/unprotected determination and therefore U5 DNP/FITTED decision.
8. Bench verification of default-off states and no backfeed.

## 17. Step-5 conclusion

**The circuit topology and named nets are complete enough to proceed to GPIO assignment.** No unresolved item currently requires a new active component or architectural redesign. Step 6 must assign exactly one of the 11 functional signal roles above to each XIAO D0–D10 pin and then test the resulting boot/strap behavior.
