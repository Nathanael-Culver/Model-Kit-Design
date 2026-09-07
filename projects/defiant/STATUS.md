# USS Defiant Electronics — Engineering Status

**Scale:** 1/1000  
**Repository role:** canonical source of truth  
**Current phase:** **Step 9 — static electrical audit complete; physical validation pending**  
**Drawing gate:** **CLOSED**

## Workflow progress

| Step | Status |
|---|---|
| 1. Reconstruct purchased BOM | **COMPLETE enough to proceed** |
| 2. Identify part numbers/packages/carriers | **COMPLETE enough to proceed** |
| 3. Freeze electrical architecture | **COMPLETE — FROZEN v1.0**, subject only to explicitly approved audit changes |
| 4. Freeze reference designators | **COMPLETE — FROZEN v1.1** |
| 5. Formal netlist | **COMPLETE enough to proceed — FORMAL v1.1** |
| 6. XIAO pin map | **COMPLETE — FROZEN v1.0** |
| 7. Master wire list | **COMPLETE enough to proceed — FORMAL v1.0**, base harness W001–W053 assigned |
| 8. Per-module pin tables | **COMPLETE enough to proceed — FORMAL v1.0** |
| 9. Static electrical validation | **COMPLETE — CONDITIONAL PASS**; physical/decision blockers remain |
| 9b. Bench/physical validation | **NEXT** |
| 10+. Final drawings/layout/closure firmware validation | gated |

Detailed Step-9 reasoning is preserved in `STEP9-AUDIT.md`. `VALIDATION.md` is the authoritative pass/blocker register and `TEST-PLAN.md` gives the required bench sequence.

## Static-audit result

No static review found a catastrophic short, reversed high-side MOSFET topology, duplicate GPIO, wrong MFRC522 voltage domain, or incompatible SK6812 level-shift scheme.

Core design remains viable:

- U1 XIAO stays permanently connected to BT1.
- RX1 feeds U1 charging/recovery through D1 and provides `WLC_PRESENT` wake.
- Q1/Q2 physically disconnect U2/5 V lighting from the battery in sleep.
- one SK6812 serial bus uses U4 SN74AHCT1G125 level translation.
- Q3–Q6 independently switch four pulse-phaser LEDs.
- U3 MFRC522 is on a switched 3.3 V rail.
- total U1 GPIO allocation remains exactly 11/11 with no expander.

## Two explicit policy decisions now blocking final architecture release

### 1. Q9 charging -> NFC hard inhibit

Current architecture forces NFC OFF whenever wireless power is present. Static audit found no project requirement that proves this is desirable, and it could prevent memory-crystal control while the model is on an active charging stand.

Before changing anything in the frozen architecture, choose:

- **KEEP Q9:** NFC intentionally unavailable while charging; or
- **DNP Q9:** allow NFC while charging and test coexistence/interference physically.

### 2. Normal deep-sleep wake workflow

Current defined wake source is `WLC_PRESENT` only. While U1 is in deep sleep, Wi-Fi/BLE are off and U3 is unpowered, so neither remote radio control nor an NFC tag can wake it.

Explicitly confirm whether **applying/enabling wireless charging power to wake the ship** is acceptable as the normal wake method. A different instantaneous off-stand wake path would require a deliberate architecture change.

## Remaining physical blockers before drawing release

1. BT1 integral-protection status and discharge capability.
2. RX1 exact pad polarity and measured unloaded/loaded maximum voltage/current/temperature.
3. D1 wireless-input charging/recovery and reverse-current/thermal test.
4. U2 actual 5 V load capability from realistic LiPo voltages.
5. Q1 SOT-23 carrier current/thermal capability.
6. U3 exact header/reset circuitry and unpowered-SPI backfeed/deep-sleep-current behavior.
7. Prewired phaser LED resistor/Vf/current configuration; close R6–R9.
8. Physical SK6812 emitter count/order, local decoupling, load and firmware brightness/current envelope.
9. repeated cold-boot/reset/deep-sleep-wake tests on GPIO2/GPIO8/GPIO9.
10. final physical BAT+/GND/+5V/+3V3 distribution implementation and any resulting W-numbers.
11. OTA/control/integrated thermal testing before closure.
12. carrier pad numbering/orientation continuity-check before soldering semiconductors.

## Drawing release criteria

The drawing gate opens only when:

- any approved architecture changes from VAL-033/VAL-034 are incorporated consistently;
- architecture/designators/pinout are coherent;
- `NETLIST.md` is drawing-approved;
- `CONNECTIONS.md` defines every fitted component pin;
- `WIRE-LIST.md` covers every applicable discrete harness connection;
- `VALIDATION.md` contains no unresolved ERROR and no hardware-critical/decision blocker required for drawing correctness.
