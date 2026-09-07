# USS Defiant — Step 9 Static Electrical Audit

**Status:** **STATIC AUDIT COMPLETE / POLICY DECISIONS CLOSED / PHYSICAL VALIDATION PENDING**  
**Date:** 2026-09-06

## Executive result

No static review found a catastrophic short, reversed MOSFET topology, duplicate GPIO, wrong MFRC522 supply voltage, or incompatible SK6812 logic-level scheme.

Core design remains viable:

- XIAO ESP32-C3 permanently connected to LiPo;
- Q1/Q2 true high-side disconnect for MT3608;
- one SK6812 RGBW data bus through U4 SN74AHCT1G125;
- four AO3400A low-side phaser channels;
- MFRC522 on a switched 3.3 V rail;
- wireless receiver isolated into XIAO 5 V input and sensed on D1/GPIO3.

## Static checks that pass

- GPIO assignment is one-to-one across D0–D10.
- D1/GPIO3 is an appropriate non-strap deep-sleep wake input.
- D9/GPIO9 is connected only to the relatively nonintrusive U4 input, with no external pull-down.
- D0/GPIO2 has R18 10 kΩ boot-high bias.
- U4 AHCT level shifting and C1/R5 arrangement are appropriate.
- Q1/Q2 high-side lighting gate topology is correct.
- Q3–Q6 low-side phaser topology is correct.
- Q7/Q8 switched 3.3 V NFC gate is correct.
- D1 polarity is correct for RX1 -> U1 isolation.
- R1/R2 divider math is appropriate near nominal 5 V, subject to measuring RX1 maximum output.
- Common-ground architecture is coherent.

## Approved policy decisions

### Q9 charging/NFC inhibit

The user explicitly approved the audit recommendation to **remove the hard charging-to-NFC inhibit**.

- Q9 is permanently **DNP**.
- W013 and W053 are permanently DNP and never reused.
- `WLC_PRESENT` no longer connects into the NFC power-gate circuit.
- NFC power is controlled by `PERIPH_EN` through Q7/Q8.
- NFC may operate while wireless charging is active.

Required consequence: bench-test NFC reliability/read range while XKT charging is active. Add interference mitigation only if a real failure is observed.

### Deep-sleep wake workflow

The user explicitly approved **wireless charging presence as the normal v1 deep-sleep wake method**.

While U1 is asleep:

- Wi-Fi is off;
- BLE is off;
- U3 MFRC522 is power-gated off;
- therefore radio/NFC control does not wake the ship.

Normal workflow:

1. apply/enable the wireless charging field;
2. RX1 produces `WLC_5V_RAW`;
3. R1/R2 raises `WLC_PRESENT`;
4. D1/GPIO3 wakes U1;
5. after safe startup, Wi-Fi/BLE/NFC/lighting become available.

No second wake architecture is required for v1.

## Physical blockers still open

1. BT1 protection PCB status and discharge capability.
2. RX1 exact pad polarity, unloaded/loaded voltage/current, alignment sensitivity and heating.
3. D1 charge/recovery/reverse-feed/thermal behavior.
4. U2 actual 5 V load and thermal capability from realistic LiPo voltages.
5. Q1 carrier-board current capability.
6. U3 exact breakout, reset behavior, unpowered SPI backfeed and deep-sleep current.
7. Phaser LED polarity/current/resistor configuration; R6–R9 remains the explicit unresolved electrical ERROR.
8. Physical SK6812 count/order/local decoupling/load.
9. Repeated cold-boot/reset/deep-sleep->WLC wake strap behavior.
10. Final physical power/ground distribution implementation.
11. NFC/XKT coexistence while charging.
12. OTA/control/integrated thermal tests before hull closure.

## Drawing release decision

**STATIC CIRCUIT: CONDITIONAL PASS.**  
**DRAWING GATE: CLOSED.**

The gate is now held closed only by physical/electrical validation and the unresolved phaser-current-limit error, not by architecture-policy decisions.

No unrelated component substitution is justified.