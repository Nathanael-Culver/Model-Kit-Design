# USS Defiant — Step 9 Static Electrical Audit

**Status:** STATIC AUDIT COMPLETE / PHYSICAL VALIDATION PENDING  
**Date:** 2026-09-06  
**Scope:** cross-check frozen architecture, netlist, GPIO map, designators, connection tables, wire list, device electrical limits, reset/deep-sleep behavior, power paths, and obvious implementation hazards.  
**Important:** this audit does not silently revise a frozen architecture. Items requiring a functional architecture change are raised for explicit approval first.

## 1. Executive finding

No static review found a catastrophic short, reversed MOSFET topology, duplicate GPIO, wrong MFRC522 supply voltage, or intrinsically incompatible logic-level scheme.

The core design remains viable:

- XIAO ESP32-C3 always connected to the LiPo;
- Q1/Q2 true high-side disconnect for MT3608;
- one SK6812 RGBW data bus through U4 SN74AHCT1G125;
- four AO3400A low-side phaser channels;
- MFRC522 on a switched 3.3 V rail;
- wireless receiver isolated into XIAO 5 V input and sensed on a wake-capable GPIO.

However, the drawing gate must remain closed because several physical facts are still unknown and two functional-policy questions need explicit acceptance.

## 2. Static checks that pass

### 2.1 GPIO uniqueness

`PINOUT.md` assigns exactly one project function to each D0–D10. No duplicate GPIO exists.

### 2.2 Deep-sleep wake pin selection

`WLC_PRESENT` on D1/GPIO3 is valid for ESP32-C3 deep-sleep GPIO wake. GPIO0–GPIO5 are RTC-capable deep-sleep wake GPIOs; GPIO3 is not a strapping pin.

### 2.3 Strap-pin strategy

- D9/GPIO9 is the critical BOOT strap and is connected only to U4 input A, with no external pull-down.
- D0/GPIO2 receives R18 10 kΩ pull-up as an explicit boot-high bias.
- D8/GPIO8 is used for NFC SCK, but GPIO8 does not determine normal SPI boot when GPIO9 is held high.

Physical attached-peripheral boot tests are still mandatory.

### 2.4 U4 level shifting

SN74AHCT1G125 is appropriate for 3.3 V -> 5 V SK6812 data because its VIH requirement is TTL-class and its input-voltage rating tolerates the MCU-side level. U4 is powered from the same switched 5 V rail as the SK6812 chain, has C1 local bypass, and drives the chain through R5 330 Ω.

Firmware requirement: drive `SK_DATA_RAW` LOW before asserting `PERIPH_EN`, and return it LOW before dropping the lighting rail.

### 2.5 Lighting high-side gate

Q1 AO3401A source=`BAT+`, drain=`U2_VIN_SW`, gate=`LIGHT_GATE` is the correct P-channel high-side orientation. Q2 AO3400A provides source-referenced gate pull-down. R3 defaults Q1 OFF and avoids the full-charge direct-GPIO P-MOS problem.

At LiPo voltages, AO3401A has adequate gate drive and low enough RDS(on) for the expected class of load, subject to actual current/thermal/carrier validation.

### 2.6 Phaser switching

Q3–Q6 AO3400A low-side topology is electrically correct. 3.3 V gate drive is within a region for which the part has specified low RDS(on). R10–R13 provide hardware default-OFF behavior.

The channel remains blocked from final approval only because R6–R9 cannot be chosen until the actual prewired LEDs are identified/measured.

### 2.7 NFC high-side gate

Q7 AO3401A + Q8 AO3400A provides a valid default-OFF 3.3 V high-side switch. R14 pulls Q7 gate to its source; R16 defaults Q8 off. The MFRC522 remains on the 3.3 V domain, not the 5 V lighting rail.

### 2.8 Wireless input diode

D1 PMEG2010ER orientation is correct for source-to-XIAO isolation:

`RX1 WLC_5V_RAW -> D1 anode -> D1 cathode/bar -> U1 5V`

The part is a 20 V / 1 A low-VF Schottky. Its electrical rating is plausible for XIAO run + charge current, but final thermal/current margin depends on measured system current and mounting copper.

### 2.9 WLC_PRESENT divider mathematics

R1=130 kΩ and R2=180 kΩ gives approximately:

- 4.5 V raw -> 2.61 V sense
- 5.0 V raw -> 2.90 V
- 5.5 V raw -> 3.19 V
- 6.0 V raw -> 3.48 V

The divider gives a valid logic-HIGH around the intended 5 V receiver output. There is little overvoltage margin above roughly 6 V, so RX1 raw voltage must be measured **before** connecting the divider to U1.

### 2.10 Common-ground architecture

No intentional isolated ground exists, and all power/signal domains resolve to system GND.

## 3. Physical blockers that remain

### 3.1 BT1 protection and discharge capability

Two distinct properties still need proof:

1. whether the exact 103450 pack contains a protection PCB; and
2. whether its documented/actual discharge capability comfortably supports the worst-case MT3608 input current.

If unprotected, U5 becomes mandatory. Even if protected, discharge capability still requires validation.

### 3.2 RX1 exact voltage and current

Do not connect `WLC_PRESENT` to U1 until RX1 unloaded and realistically loaded maximum output voltage is measured. Also verify receiver polarity, alignment behavior, heating, and charge-path performance.

### 3.3 U2 actual load capability

The purchased MT3608 module must be tested from realistic LiPo voltages, especially near the low end. Output-current marketing claims cannot be used as design limits.

### 3.4 Q1 carrier-board current path

Q1 is the only SOT-23 device in this design carrying the full lighting-boost **input** current. Generic SOT-23 breakout traces/pads may become the current/thermal bottleneck before the AO3401A itself does.

Before final assembly:

- inspect carrier copper width/thickness;
- measure voltage drop and heating under worst-case input current;
- reinforce source/drain current paths with appropriately sized copper/wire if required.

Q2/Q3–Q9 do not carry comparable current in this design.

### 3.5 D1 mounting thermal path

D1 can conduct the XIAO operating current plus battery-charge current. The SOD123W device rating assumes useful PCB thermal spreading. Verify temperature/drop on the actual proto-board implementation rather than treating 1 A as a guaranteed no-layout-conditions limit.

### 3.6 MFRC522 exact breakout / unpowered I/O

This is the most important boot/backfeed uncertainty.

With U3 power-gated off, D6/D8/D10 can still present logic levels to its SPI inputs, and R18 pulls MISO/D0 high. The exact breakout may contain series resistors, regulator circuitry, pull resistors, and input-clamp paths that alter behavior.

Required measurements:

- U3 VCC while nominally OFF with SPI attached;
- current into each SPI pin while U3 is OFF;
- D0/GPIO2 voltage during reset;
- repeated cold boots with U3 attached/off;
- deep-sleep current with U3 attached/off.

If the module back-powers or corrupts a strap pin, fix that specific interface before changing the MCU or adding unrelated hardware.

### 3.7 MFRC522 reset

Verify the exact breakout reliably restarts after switched-power cycling with RST/NRSTPD biased to the switched rail. If its onboard circuit already provides the required bias, R17 can be DNP.

### 3.8 Phaser LED current limiting

Still the only presently explicit `ERROR`: identify one actual prewired 0805 LED, determine polarity and whether a resistor is already in series, then calculate R6–R9.

### 3.9 SK6812 physical count and local decoupling

The single data-bus architecture is settled, but final load is impossible to calculate without the physical emitter count.

Also verify the actual purchased SK6812 form:

- if cut from flexible strip and each pixel section retains its local bypass capacitor, no new per-pixel capacitor is needed;
- if bare SK6812 packages are used without local decoupling, add local ceramic decoupling at each physical emitter before schematic release.

C2=470 µF is bulk rail capacitance and is not a substitute for local pixel bypassing.

### 3.10 SK6812 power-budget / firmware cap

Worst-case RGBW current depends on the exact SK6812 variant and physical emitter count. After measuring one emitter and the final chain, establish a firmware maximum-brightness/current envelope rather than allowing an unrestricted theoretical all-channel maximum.

### 3.11 Distribution-node physical implementation

Electrical nodes are defined, but the final control-board/protoboard layout must still define the actual GND, +5 V, BAT+, and 3.3 V distribution copper/jumpers. Any discrete jumper created by that layout receives a new W-number.

## 4. Functional-policy blockers requiring explicit approval

### 4.1 Q9 hard NFC inhibit while wireless charging is present

Current frozen architecture contains:

`NFC_POWER = PERIPH_EN AND NOT WLC_PRESENT`

Q9 therefore forces the MFRC522 OFF whenever the wireless-power receiver is active.

The static audit finds **no user requirement establishing that NFC must be disabled while charging**. This inhibit was introduced as a conservative interference measure, but it has a functional downside: if the ship normally sits on an active wireless charging stand, the future memory-crystal NFC controls can never work while it is on that stand.

**Recommendation:** do not finalize Q9 until the user explicitly chooses one of:

A. KEEP Q9 — NFC is intentionally unavailable whenever charging is active; or
B. DNP Q9 — allow NFC while charging and test whether the two inductive systems coexist acceptably. If interference is later demonstrated, solve the demonstrated problem then.

No architecture/netlist change is made by this audit without approval.

### 4.2 Deep-sleep wake user experience

The current hardware has only one defined wake source: `WLC_PRESENT`.

When U1 is in deep sleep:

- Wi-Fi is off;
- BLE is off;
- MFRC522 is power-gated off;
- therefore Wi-Fi, BLE, and an NFC tag cannot wake the ship.

The ship can wake by applying wireless power, or firmware could implement a later timer-wake policy at the cost of additional standby activity. A different instantaneous off-stand wake method would be an architecture change.

Before final firmware/closure, explicitly confirm that **"apply/enable the wireless charging field to wake the ship"** is an acceptable normal wake workflow.

## 5. Deep-sleep / boot-specific tests

In addition to ordinary cold boot, perform at least 50 cycles each of:

- battery cold boot with all peripherals attached;
- reset with U3 OFF and U4 OFF;
- lighting rail enable/disable;
- deep sleep -> WLC_PRESENT wake;
- deep sleep -> wake -> deep sleep repetitions;
- removal/reapplication of wireless power.

Watch specifically for:

- accidental GPIO9 download mode;
- GPIO2 low during strap sampling;
- phaser flashes during reset;
- brief unintended lighting-rail turn-on;
- partial U3 power while its rail is OFF;
- increased deep-sleep current after SPI is connected.

Firmware must not enter deep sleep while `WLC_PRESENT` is already HIGH unless immediate wake is intentionally desired.

## 6. Static audit release decision

### Static circuit result

**CONDITIONAL PASS.** The core electrical topology is coherent and uses the purchased parts appropriately.

### Drawing release

**DENIED / gate remains CLOSED.** Reasons:

- phaser current limiting is unresolved;
- exact U3 power-off/boot behavior is unverified;
- RX1 voltage/charge path is unverified;
- battery protection/discharge capability is unverified;
- U2 load/thermal capability is unverified;
- physical SK6812 count/decoupling/load is unverified;
- Q1 carrier current capability is unverified;
- Q9 charging/NFC policy needs explicit user approval;
- normal deep-sleep wake workflow needs explicit user acceptance.

No unrelated component substitution is justified by the static audit.
