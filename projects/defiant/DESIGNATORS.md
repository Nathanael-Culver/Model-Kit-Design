# USS Defiant — Reference Designators

**Document status:** ACTIVE CONVENTION; assignments partially provisional.

## Designator classes

| Prefix | Class |
|---|---|
| U | IC/module/controller/regulator/buffer |
| Q | MOSFET/transistor |
| D | diode |
| R | resistor |
| C | capacitor |
| LED | discrete/addressable LED |
| BT | battery |
| RX | wireless-power receiver assembly |
| TX | wireless-power transmitter assembly |
| SW | switch/reed switch |
| TH | thermistor |
| J | connector/header/test connector |
| TP | test point |

## Assigned primary assemblies

| Ref | Component | Status |
|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | LOCKED |
| BT1 | 103450 3.7 V 2500 mAh LiPo | LOCKED |
| RX1 | XKT high-current wireless-power receiver, apparent XKT-3168 IC | LOCKED hardware / exact variant OPEN |
| TX1 | XKT-412 wireless-power transmitter | LOCKED hardware / external to ship |
| U2 | MT3608 boost-converter module | LOCKED hardware / module revision OPEN |
| U3 | MFRC522 NFC breakout | LOCKED hardware / module revision OPEN |
| U4 | first SN74AHCT1G125DBVR SK6812 data buffer | PROVISIONAL until physical SK6812 chain count is confirmed |
| LED1–LED9 | addressable lighting zones P0–P8 respectively | RECONSTRUCTED mapping |
| LED10–LED13 | pulse phasers PH0–PH3 respectively | LOCKED count |

## Semiconductor allocation not yet frozen

The purchased AO3400A/AO3401A devices are not assigned Q numbers to specific power-gate functions until `POWER-ARCHITECTURE.md` is frozen. This prevents reference designators from implying a circuit that has not been approved.

Expected allocation classes after freeze:

- one low-side switching device per independent pulse-phaser channel if required by the final LED/current arrangement;
- one or more high-side power-gate devices for switched rails if the purchased module EN pins cannot implement the required isolation;
- N-channel helper/gate-driver devices where required for safe P-channel high-side control.

## Passive numbering rule

Passive designators are assigned only after their function/value is frozen in the netlist. Numbers are never reused after deletion; obsolete parts are marked `DNP` or `SUPERSEDED` so historical drawings remain traceable.
