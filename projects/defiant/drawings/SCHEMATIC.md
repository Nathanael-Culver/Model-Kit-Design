# USS Defiant — Electrical Schematic

**Current drawing revision:** **v1.1 PRE-RELEASE**  
**Drawing status:** engineering schematic complete enough for design/bench use; **NOT final assembly release**.

## Authoritative sources

This schematic is derived from and must remain consistent with:

- `../POWER-ARCHITECTURE.md` FROZEN v1.2
- `../DESIGNATORS.md` FROZEN v1.6
- `../NETLIST.md` FORMAL v1.5
- `../PINOUT.md` FROZEN v1.0
- `../CONNECTIONS.md` FORMAL v1.4
- `../LIGHTING-LAYOUT.md` FROZEN v1.0
- `../WIRE-LIST.md` FORMAL v1.2

## Sheet 1 — Power / charging / wake / switched rails

Shows:

- BT1 103450 LiPo;
- conditional U5 1S protection branch;
- Q1 AO3401A / Q2 AO3400A MT3608 battery-side disconnect;
- U2 MT3608 to `+5V_LIGHT_SW`;
- RX1 XKT-3168 -> D1 PMEG2010ER -> U1 charging/recovery path;
- R1 130 kΩ / R2 180 kΩ `WLC_PRESENT` divider;
- U1 relevant battery/5V/3V3/PERIPH_EN/wake connections.

## Sheet 2 — Addressable lighting

Shows:

- U1 D9/GPIO9 `SK_DATA_RAW`;
- U4 SN74AHCT1G125 + C1 0.1 µF;
- R5 330 Ω;
- complete 14-pixel data chain LED14 through LED27;
- W054-W066 inter-emitter data links;
- `+5V_LIGHT_SW` and GND distribution concept;
- C2 470 µF target;
- P0-P8 logical mapping.

## Sheet 3 — NFC / SPI / pin map

Shows:

- complete U1 D0-D10 function map;
- black V602 U3 SPI interface;
- R18 10 kΩ GPIO2/NFC_MISO pull-up;
- Q7 AO3401A / Q8 AO3400A NFC power gate;
- R14/R15/R16;
- R17 10 kΩ target on V602 reset, pending bench decision;
- Q9 DNP;
- boot/deep-sleep constraints.

## Sheet 4 — Pulse phasers

Shows four independent channels:

- PH0: U1 D2/GPIO4 -> Q3 -> LED10, R6/R10;
- PH1: U1 D3/GPIO5 -> Q4 -> LED11, R7/R11;
- PH2: U1 D4/GPIO6 -> Q5 -> LED12, R8/R12;
- PH3: U1 D5/GPIO7 -> Q6 -> LED13, R9/R13;
- R6-R9 = 150 Ω >=1/8 W;
- R10-R13 = 100 kΩ gate pull-downs.

## Pre-release limitations

The circuit topology is drawn now because physical hull dimensions do not affect the electrical schematic. Final release is still gated by the validation items that can materially alter installation/release details, including:

- BT1 protection/discharge proof;
- XKT/D1 integrated charging acceptance;
- U2/Q1 load/thermal test;
- V602 unpowered backfeed/reset/boot test;
- boot/wake testing on strap-sensitive GPIOs;
- measured 14-pixel current envelope / firmware current cap;
- final physical power-distribution and harness geometry.

Any future electrical change must first update the authoritative text/netlist and then increment the schematic revision.
