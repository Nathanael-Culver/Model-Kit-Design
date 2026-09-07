# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 9b — bench / physical validation**  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | COMPLETE enough to proceed |
| 2. Identify part numbers/packages/carriers | COMPLETE enough to proceed |
| 3. Freeze electrical architecture | **FROZEN v1.1** |
| 4. Freeze reference designators | **FROZEN v1.2** |
| 5. Formal netlist | **FORMAL v1.2** |
| 6. XIAO pin map | **FROZEN v1.0** |
| 7. Master wire list | **FORMAL v1.1**; W001–W053 reserved, W013/W053 DNP |
| 8. Per-module pin tables | **FORMAL v1.1** |
| 9. Static electrical validation | **COMPLETE — CONDITIONAL PASS** |
| 9a. Architecture-policy decisions | **COMPLETE / APPROVED** |
| 9b. Bench / physical validation | **NEXT / ACTIVE** |
| 10+. Final drawings/layout/closure validation | gated |

## Approved Step-9 decisions

1. **Q9 is DNP.** NFC is allowed while wireless charging is active. W013 and W053 are permanently DNP and never reused.
2. **Wireless charging presence is the normal deep-sleep wake method for v1.** Wi-Fi/BLE/NFC do not wake a sleeping ship; they become available after the charging field wakes U1.

These decisions are incorporated into `POWER-ARCHITECTURE.md`, `DESIGNATORS.md`, `NETLIST.md`, `CONNECTIONS.md`, `WIRE-LIST.md`, `VALIDATION.md`, and `STEP9-AUDIT.md`.

## Frozen XIAO assignment

| XIAO | GPIO | Signal |
|---|---:|---|
| D0 | 2 | `NFC_MISO` |
| D1 | 3 | `WLC_PRESENT` / deep-sleep wake |
| D2 | 4 | `PH0_GATE` |
| D3 | 5 | `PH1_GATE` |
| D4 | 6 | `PH2_GATE` |
| D5 | 7 | `PH3_GATE` |
| D6 | 21 | `NFC_CS` |
| D7 | 20 | `PERIPH_EN` |
| D8 | 8 | `NFC_SCK` |
| D9 | 9 | `SK_DATA_RAW` |
| D10 | 10 | `NFC_MOSI` |

## Remaining physical blockers before drawing release

1. BT1 protection status and discharge capability.
2. RX1 exact pads and measured unloaded/loaded output/current/temperature.
3. D1 charging/recovery/reverse-current/thermal test.
4. U2 5 V load/thermal test from realistic battery voltage.
5. Q1 carrier-board current/thermal capability.
6. U3 header/reset behavior and unpowered-SPI backfeed/deep-sleep-current test.
7. Prewired phaser LED resistor/Vf/current configuration; finalize R6–R9.
8. Physical SK6812 count/order/local decoupling/load and firmware current limit.
9. Repeated boot/reset/deep-sleep -> wireless-wake testing on strap pins.
10. NFC read reliability while wireless charging is active.
11. Final BAT+/GND/+5V/+3V3 distribution implementation and resulting W-numbers.
12. SOT carrier pad-orientation continuity check before semiconductor soldering.
13. OTA/control/integrated thermal testing before hull closure.

`VALIDATION.md` is the authoritative blocker register. `TEST-PLAN.md` defines the bench sequence.

## Drawing release criteria

The drawing gate opens only when:

- architecture/designators/pinout/netlist remain coherent;
- `NETLIST.md` is drawing-approved;
- `CONNECTIONS.md` defines every fitted component pin;
- `WIRE-LIST.md` covers every discrete harness connection required by final layout;
- `VALIDATION.md` has no unresolved ERROR and no hardware-critical blocker required for drawing correctness.