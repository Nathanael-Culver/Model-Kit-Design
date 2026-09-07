# USS Defiant — Electrical Validation Register

**Document status:** ACTIVE  
**Release rule:** no final schematic/CAD drawing while any `ERROR` item is unresolved.

Severity:

- `ERROR` — would make the design electrically invalid or unsafe.
- `BLOCKER` — prevents architecture/netlist approval.
- `WARNING` — design can proceed only with an explicit mitigation/test.
- `PASS` — checked and currently satisfied.

| ID | Check | Result | Finding / required action |
|---|---|---|---|
| VAL-001 | common ground | PASS requirement | U1, U2, U3, lighting, receiver sensing and phaser returns must share `GND`; final netlist must prove every ground pin is present |
| VAL-002 | MFRC522 voltage | PASS requirement | MFRC522 main supply is a 3.3 V-class device; do not power U3 from the 5 V lighting rail |
| VAL-003 | SK6812 logic level | PASS concept / component count OPEN | SN74AHCT1G125 at 5 V provides TTL-compatible input behavior suitable for 3.3 V MCU data level shifting; one buffer needed per independent data line |
| VAL-004 | XIAO boot pins | BLOCKER | GPIO2/D0, GPIO8/D8 and GPIO9/D9 are strapping pins; GPIO9 must not be forced low at reset and GPIO2 pull-up guidance must be respected |
| VAL-005 | D6 boot chatter | WARNING | D6/GPIO21 is UART0 TX and can emit ROM/boot text; do not use it for a power-enable signal that would react to boot chatter |
| VAL-006 | wireless-present input voltage | ERROR until detector exists | `WLC_5V_RAW` must never connect directly to a 3.3 V GPIO; divider/protection values must be calculated and tested |
| VAL-007 | wireless-present wake capability | BLOCKER | selected XIAO pin must be D0–D3; Candidate A uses D1/GPIO3 |
| VAL-008 | pin budget | BLOCKER | one SK chain + four phasers + RC522 SPI + wireless wake + one shared power enable consumes all 11 exposed GPIOs; a second power-enable GPIO, RC522 reset GPIO, or extra SK data line exceeds native capacity |
| VAL-009 | MT3608 shutdown implementation | BLOCKER | exact purchased module must be inspected to decide usable EN control vs external input power gate |
| VAL-010 | battery-domain P-MOS direct drive | WARNING | directly driving an AO3401A gate from a 3.3 V GPIO while its source can be 4.2 V may not guarantee hard OFF; use a validated topology such as an N-channel helper or module EN |
| VAL-011 | power-on defaults | BLOCKER | lighting, NFC and phaser channels must be hardware-default OFF before firmware configures GPIOs |
| VAL-012 | XIAO external 5 V path | BLOCKER | proposed wireless 5 V input/isolation path must follow Seeed guidance and be bench-verified for charge/recovery and reverse-current behavior |
| VAL-013 | Schottky polarity | PASS component identity | PMEG2010ER pin 1/marking bar is cathode; pin 2 is anode; final D placement remains OPEN |
| VAL-014 | phaser current limiting | ERROR until LED spec known | exact prewired 0805 electrical configuration is unknown; do not reuse old 470 Ω or 100–150 Ω values without measurement/specification |
| VAL-015 | logic-buffer bypass | BLOCKER | each SN74AHCT1G125 requires local decoupling; exact capacitor value/source/designator must be assigned before netlist approval |
| VAL-016 | SK6812 bulk capacitance | WARNING | historical 470 µF 5 V rail capacitor must be revalidated against final physical rail/load; inventory/source still unverified |
| VAL-017 | SK6812 chain count | BLOCKER | nine logical pixels are recovered, but final physical chain count is not yet conclusively recovered |
| VAL-018 | RC522 power-off I/O | BLOCKER | verify power-gated module does not clamp/drive SPI lines while unpowered, especially if a strap pin is used |
| VAL-019 | RC522 reset strategy | BLOCKER | confirm whether switched-power reset can replace a dedicated MCU RST GPIO on the exact module |
| VAL-020 | MT3608 output capability | WARNING | “2 A” is not a guaranteed 5 V output-current rating from a single-cell LiPo; load-test the complete purchased module at expected battery voltage and lighting load |
| VAL-021 | XKT receiver rating | WARNING | seller 5 V/2 A claim must be treated as unverified until measured under realistic coil alignment/load |
| VAL-022 | diode/backfeed paths | BLOCKER | validate no path backfeeds RX1, U2 output, or powered-down U3 through signal pins |
| VAL-023 | duplicate GPIO use | BLOCKER | final approved pin table must contain exactly one primary project function per GPIO unless sharing is intentional and explicitly documented |
| VAL-024 | OTA after sealing | BLOCKER for final assembly | test Wi-Fi/BLE control and OTA update repeatedly before closing hull; no firmware path may require physical BOOT/USB access for routine updates |

## Required final validation pass

Before schematic release, review every component pin and every named net for:

1. duplicate GPIO assignments;
2. missing ground/power pins;
3. wrong voltage domains;
4. MOSFET source/drain/gate orientation;
5. diode polarity;
6. power-up default state;
7. reset/boot strap interactions;
8. unpowered-device backfeeding;
9. regulator/receiver current and thermal margin;
10. wake-source operation;
11. wire-level endpoint completeness;
12. explicit NC/DNP state for every unused pin.
