# USS Defiant — XIAO ESP32-C3 Pin Map

**Document status:** MCU HARDWARE VERIFIED / PROJECT ALLOCATION PROVISIONAL  
**Rule:** only the `Approved allocation` table becomes authoritative after architecture freeze.

## 1. Verified XIAO pin map

| XIAO pin | ESP32-C3 GPIO | Native/board function | Deep-sleep GPIO wake on XIAO | Reset/boot concern |
|---|---:|---|---|---|
| D0 / A0 | GPIO2 | ADC1_CH2 | Yes | strapping pin; Espressif recommends pull-up |
| D1 / A1 | GPIO3 | ADC1_CH3 | Yes | no XIAO strapping warning |
| D2 / A2 | GPIO4 | ADC1_CH4 / JTAG MTMS | Yes | JTAG function; ordinary GPIO after configuration |
| D3 / A3 | GPIO5 | ADC2_CH0 / JTAG MTDI | Yes | JTAG; Seeed warns A3 ADC2 reliability |
| D4 / SDA | GPIO6 | I2C SDA / JTAG MTCK | No | JTAG function |
| D5 / SCL | GPIO7 | I2C SCL / JTAG MTDO | No | JTAG function |
| D6 / TX | GPIO21 | UART0 TX | No | ROM/bootloader text may appear here at boot |
| D7 / RX | GPIO20 | UART0 RX | No | UART0 RX |
| D8 / SCK | GPIO8 | SPI clock capable | No | strapping pin |
| D9 / MISO | GPIO9 | SPI data capable / BOOT | No | critical BOOT strapping pin; onboard pull-up; must not be forced low at reset |
| D10 / MOSI | GPIO10 | SPI data / FSPICS0 alternate | No | no XIAO strapping warning |

## 2. Project pin requirements

Minimum current functional requirements if there is one SK6812 data chain and four independent phasers:

| Function | GPIO count |
|---|---:|
| wireless-power-present wake input | 1 |
| SK6812 data | 1 |
| pulse phasers PH0–PH3 | 4 |
| MFRC522 SPI (SCK, MOSI, MISO, CS) | 4 |
| switched-peripheral enable | 1 if lighting and NFC gates share control; 2 if independent |
| MFRC522 reset | 0 only if hardware reset is tied appropriately and power cycling is used; otherwise 1 |

One-chain + shared-enable + no MCU-controlled RC522 reset = **11 GPIO**, exactly the number exposed by the XIAO. Independent lighting/NFC enables or an additional SK6812 data chain exceed the native pin budget unless another existing function can be combined or additional hardware is introduced.

This is a critical architecture constraint and is why no pin map may be frozen before chain count and power-gate granularity are confirmed.

## 3. Rejected historical pin maps

Older project drafts are **SUPERSEDED** because they conflict:

- one 2025 draft placed SK6812 on D8 and phasers on D3–D6;
- another used SK6812 on D7 while also allocating RFID functions to D6/D7;
- an older MFRC522 mapping claimed SS GPIO7/D7, SCK GPIO6/D6, MOSI GPIO10/D10, MISO GPIO9/D9, RST GPIO2/D2, which conflicts with other assignments and places an externally driven SPI signal on BOOT pin D9.

These are evidence of what **not** to copy into a drawing.

## 4. Candidate A — pin-budget proof only

This candidate demonstrates that the locked functions can fit **only under the assumptions of one SK6812 chain, a shared peripheral-power enable, and no MCU-controlled MFRC522 reset**. It is not yet approved.

| XIAO pin | Candidate function | Why | Validation required |
|---|---|---|---|
| D0 / GPIO2 | `NFC_MISO` | input from power-gated NFC; can keep GPIO2 from driving a phaser gate | verify unpowered U3 does not clamp/drive; preserve recommended boot pull-up |
| D1 / GPIO3 | `WLC_PRESENT` | wake-capable non-strapping pin | divider thresholds, leakage, wake polarity |
| D2 / GPIO4 | `PH0_GATE` | ordinary output | default-off hardware pull state |
| D3 / GPIO5 | `PH1_GATE` | ordinary output | default-off hardware pull state |
| D4 / GPIO6 | `PH2_GATE` | ordinary output | default-off hardware pull state |
| D5 / GPIO7 | `PH3_GATE` | ordinary output | default-off hardware pull state |
| D6 / GPIO21 | `NFC_CS` | boot UART text is harmless only while U3 is power-gated | verify U3 remains off through boot |
| D7 / GPIO20 | `PERIPH_PWR_EN` | avoids TX boot chatter on the enable line | external default-OFF resistor; shared-gate architecture approval |
| D8 / GPIO8 | `NFC_SCK` | strap pin can be used if external circuit is high impedance during reset | verify U3 off/high-Z during strap sampling |
| D9 / GPIO9 | `SK6812_DATA_RAW` | onboard BOOT pull-up is compatible with high-impedance buffer input; avoids attaching a pull-down MOSFET gate to GPIO9 | verify U4 unpowered-input behavior; no external circuit may pull D9 low at reset |
| D10 / GPIO10 | `NFC_MOSI` | ordinary output | verify SPI routing in firmware |

### Candidate MFRC522 reset treatment

`U3 RST` would be tied to the switched 3.3 V NFC rail through an appropriate pull-up/reset network so that power cycling U3 provides hardware reset. Exact module behavior must be checked before this is accepted.

## 5. Approved allocation

**NONE YET.**

The final table is intentionally blank until:

- physical SK6812 chain count is confirmed;
- U2 power gating implementation is chosen;
- separate vs shared peripheral enable is approved;
- U3 exact module and power-off SPI behavior are bench checked;
- boot tests pass with all peripherals attached.
