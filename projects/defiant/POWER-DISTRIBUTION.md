# USS Defiant — Physical Power Distribution Strategy

**Document status:** **FROZEN topology / wire gauges and exact branch lengths pending physical measurement**  
**Applies to:** final harness, central protoboard/control assembly, LED power distribution, and mechanical layout.

## 1. Design goal

Keep high-current paths short and low resistance while keeping the sealed model serviceable during assembly. The SK6812 **data line is serial**, but power/ground are distributed separately so lighting current does not have to pass through every tiny cut-strip copper section.

## 2. Central power/control island

Use one compact solderable protoboard/control assembly as the electrical hub for as many of these as practical:

- Q1/Q2 lighting power gate and R3/R4;
- D1 and R1/R2 wireless-present divider;
- U4 level shifter, R5 and C1;
- Q3–Q6 phaser MOSFETs and gate pull-downs;
- Q7/Q8 NFC power gate and R14–R16;
- R18 GPIO2 pull-up;
- C2 switched-5-V bulk capacitor;
- BAT+/GND/+5V/+3V3 distribution junctions.

U2 MT3608 may mount immediately beside this assembly rather than on it if height/fit is better.

This avoids eight separate loose SOT carrier boards and multiple free-air splice points. Purchased SOT carriers may be mounted/wired onto the protoboard as subassemblies.

## 3. Battery distribution

```text
BT1 protected output / U5 P+/P-
        │
        ├──> U1 BAT input
        │
        └──> Q1 high-side lighting gate -> U2 MT3608
```

- `BAT+` and GND are common junctions, not MCU-current paths.
- Lighting current must not be routed through a XIAO ground/power pad as a pass-through.
- If BT1 is confirmed protected, U5 is DNP.
- If BT1 is unprotected, U5 becomes mandatory and the junctions move to its protected P+/P- side.

## 4. Switched 5 V distribution

U2 `VOUT+` creates `+5V_LIGHT_SW` at the central control island.

From that node, split into four functional branches:

1. **front/deflector branch** — LED14/LED15;
2. **port lighting branch** — LED16–LED21;
3. **starboard lighting branch** — LED22–LED27;
4. **local control/phaser branch** — U4, C2, and R6–R9.

The port and starboard branches are independent power trunks even though the serial data chain crosses from LED21 to LED22.

## 5. Ground distribution

Use the same branch structure for GND:

- central high-current ground junction at/near U2 output return and battery return;
- front lighting return;
- port lighting return;
- starboard lighting return;
- local phaser/control return;
- low-current U1/U3/RX1 signal/power returns tied to the same system ground without forcing lighting current through them.

The goal is a common electrical ground with controlled current paths, not isolated grounds.

## 6. 3.3 V distribution

`+3V3_ALWAYS` from U1 is low-current control power only.

It feeds:

- Q7 source through W050;
- R14 pull-up;
- R18 GPIO2 pull-up;
- any other explicitly documented low-current control bias.

U3 receives power only from `+3V3_NFC_SW` via Q7/W048.

Do not use U1 3.3 V for SK6812s, phasers, or MT3608 loads.

## 7. Wireless-power path

RX1 remains electrically separate from the lighting rail:

```text
RX1 5 V output
  ├──> D1 -> U1 5V/VBUS charging/recovery path
  └──> R1/R2 -> WLC_PRESENT -> U1 D1/GPIO3
```

RX1 does not directly feed `+5V_LIGHT_SW`.

## 8. Preferred wire classes

These are **design targets**, not final cut-list values. Final gauge is frozen after inventory and load/thermal checks.

| Class | Circuits | Preferred gauge | Notes |
|---|---|---|---|
| PWR-A | battery main, Q1->U2 input, U2 main output/return | **24 AWG preferred** | if only 26 AWG is available, keep extremely short or use parallel conductors where mechanically sensible; validate thermally |
| PWR-B | front/port/starboard 5 V and GND lighting trunks | **26 AWG preferred** | short internal branches; final choice depends on measured 14-pixel load |
| SIG-A | SK6812 data W021–W023, W054–W066 | **30 AWG** | fine stranded/Kynar-class wire is appropriate; keep data/ground routing orderly |
| SIG-B | SPI, gates, WLC_PRESENT, low-current 3.3 V control | **30 AWG** | low current |
| PHASER | LED10–LED13 factory leads | factory fine leads | extend only if needed; current limited by R6–R9 |

If the on-hand wire differs, update the table based on actual inventory rather than buying replacements automatically.

## 9. Copper tape policy

Copper tape remains optional.

Good uses:

- short, wide low-profile 5 V/GND distribution on a flat interior surface where insulated and mechanically protected;
- local bus reinforcement on protoboard.

Avoid:

- directly under/over RX1 or TX1 coils;
- directly behind U3's NFC antenna;
- large closed conductive loops;
- exposed tape near strip pads or battery pouch.

Conventional insulated wire remains the default unless tape solves a real clearance problem.

## 10. Physical placement separation rules

- RX1 coil: ventral/bottom charging surface, as flat as possible.
- U3 NFC antenna: preferably dorsal/top surface, facing the memory-crystal approach direction.
- Do not place BT1 directly behind either inductive/NFC antenna if avoidable; its foil pouch can interfere with magnetic fields.
- Keep XIAO RF antenna clear of BT1, copper tape, RX1 coil, U3 antenna, and large ground/power copper where practical.
- Keep U2 and high-current switching parts away from the battery pouch and provide some air/thermal clearance.

## 11. W067+ rule

W067 and above are reserved for the final physical power/ground branch segments and distribution jumpers.

Do **not** assign them until component positions are measured in the actual hull. Once assigned, they are permanent just like W001–W066.

## 12. What is now frozen vs open

Frozen:

- central distribution concept;
- separate front/port/starboard lighting power branches;
- common-ground strategy;
- no direct RX1->lighting feed;
- one central power/control island preferred;
- wire-class strategy.

Open pending actual hull measurements:

- exact board dimensions and placement coordinates;
- exact splice/junction locations;
- W067+ endpoints;
- final gauge/color per wire;
- routed/cut lengths;
- whether any copper tape is actually needed.
