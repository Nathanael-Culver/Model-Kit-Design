#!/usr/bin/env python3
"""Generate VeSys-style harness documentation from the Defiant semantic EDA model.

Electrical connectivity remains authoritative in ../eda/defiant-connectivity.xml.
This file adds physical-documentation concepts only: harness branches, wire
classes, provisional assembly zones, and endpoint overrides for distribution
nodes that are not represented as physical component pins in the EDA model.

Outputs are deterministic text/SVG files suitable for Git diffs and automated
validation. Exact wire lengths/colors/final gauges are intentionally OPEN until
hull measurements are available.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import html
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EDA_XML = ROOT / "eda" / "defiant-connectivity.xml"
TOPOLOGY_XML = HERE / "harness-topology.xml"
OUT = HERE / "generated"
OUT.mkdir(exist_ok=True)

DNP = {"W013", "W053"}
STATUS = {
    "W001": "CONDITIONAL-BT1-PROTECTED",
    "W002": "CONDITIONAL-BT1-PROTECTED",
    "W003": "CONDITIONAL-BT1-UNPROTECTED",
    "W004": "CONDITIONAL-BT1-UNPROTECTED",
    "W005": "CONDITIONAL-BT1-UNPROTECTED",
    "W006": "CONDITIONAL-BT1-UNPROTECTED",
    "W019": "IMPLEMENTATION-CONDITIONAL",
    "W020": "IMPLEMENTATION-CONDITIONAL",
    "W022": "IMPLEMENTATION-CONDITIONAL",
    "W026": "GEOMETRY-OPEN",
    "W027": "GEOMETRY-OPEN",
    "W051": "IMPLEMENTATION-CONDITIONAL",
    "W052": "IMPLEMENTATION-CONDITIONAL",
}
NET_OVERRIDES = {
    "W026": "+5V_LIGHT_SW",
    "W027": "GND",
    "W013": "WLC_PRESENT",
    "W053": "GND",
}


def parse_connectivity():
    root = ET.parse(EDA_XML).getroot()
    by_wire = defaultdict(list)
    component_parts = {}
    for c in root.find("components"):
        ref = c.attrib["ref"]
        component_parts[ref] = c.attrib.get("part", "")
        for p in c.findall("pin"):
            wid = p.attrib.get("wire")
            if not wid:
                continue
            by_wire[wid].append({
                "ref": ref,
                "pin": p.attrib.get("number", ""),
                "pin_name": p.attrib.get("name", ""),
                "net": p.attrib.get("net", ""),
                "pin_status": p.attrib.get("status", "active"),
            })
    return by_wire, component_parts


def parse_topology():
    root = ET.parse(TOPOLOGY_XML).getroot()
    classes = {c.attrib["id"]: dict(c.attrib) for c in root.find("wire-classes")}
    nodes = {n.attrib["id"]: dict(n.attrib) for n in root.find("nodes")}
    branch_by_wire = {}
    branches = []
    for b in root.find("branches"):
        bd = dict(b.attrib)
        wires = []
        for w in b.findall("wire"):
            wd = dict(w.attrib)
            wires.append(wd)
            branch_by_wire[wd["ref"]] = {
                "branch": bd["id"],
                "branch_name": bd.get("name", ""),
                "region": bd.get("region", ""),
                "class": wd.get("class", bd.get("class", "")),
            }
        bd["wires"] = wires
        branches.append(bd)
    overrides = {}
    ovroot = root.find("endpoint-overrides")
    if ovroot is not None:
        for w in ovroot:
            overrides[w.attrib["ref"]] = dict(w.attrib)
    zones = []
    zroot = root.find("assembly-zones")
    if zroot is not None:
        for z in zroot:
            zones.append(dict(z.attrib))
    return classes, nodes, branches, branch_by_wire, overrides, zones


def endpoint_text(e, parts):
    ref = e["ref"]
    pin = e["pin"]
    name = e.get("pin_name", "")
    part = parts.get(ref, "")
    detail = f"{ref}.{pin}"
    if name and name != pin:
        detail += f" ({name})"
    if part:
        detail += f" - {part}"
    return detail


def build_records():
    by_wire, parts = parse_connectivity()
    classes, nodes, branches, branch_by_wire, overrides, zones = parse_topology()
    records = []
    errors = []

    refs = sorted(branch_by_wire, key=lambda w: int(w[1:]))
    expected = [f"W{i:03d}" for i in range(1, 67)]
    missing = [w for w in expected if w not in branch_by_wire]
    if missing:
        errors.append("Topology missing reserved wire IDs: " + ", ".join(missing))

    for wid in refs:
        meta = branch_by_wire[wid]
        endpoints = by_wire.get(wid, [])
        override = overrides.get(wid)

        if override:
            from_ep = override.get("from", "OPEN")
            to_ep = override.get("to", "OPEN")
        elif len(endpoints) == 2:
            from_ep = endpoint_text(endpoints[0], parts)
            to_ep = endpoint_text(endpoints[1], parts)
        elif wid in DNP:
            from_ep = "DNP"
            to_ep = "DNP"
        else:
            from_ep = endpoint_text(endpoints[0], parts) if endpoints else "OPEN"
            to_ep = "OPEN"
            errors.append(f"{wid}: active/conditional wire has {len(endpoints)} semantic endpoints and no endpoint override")

        nets = {e.get("net", "") for e in endpoints if e.get("net")}
        net = NET_OVERRIDES.get(wid)
        if not net:
            if len(nets) == 1:
                net = next(iter(nets))
            elif len(nets) > 1:
                errors.append(f"{wid}: endpoints disagree on net: {sorted(nets)}")
                net = "ERROR"
            else:
                net = "OPEN"

        status = "DNP-SUPERSEDED" if wid in DNP else STATUS.get(wid, "ACTIVE")
        wire_class = meta["class"]
        class_info = classes.get(wire_class, {})
        gauge = class_info.get("preferred-gauge", "OPEN")
        if status.startswith("DNP"):
            gauge = "N/A"

        records.append({
            "wire_id": wid,
            "branch": meta["branch"],
            "branch_name": meta["branch_name"],
            "region": meta["region"],
            "class": wire_class,
            "preferred_gauge": gauge,
            "color": "OPEN",
            "routed_length_mm": "OPEN",
            "cut_length_mm": "OPEN",
            "net": net,
            "from": from_ep,
            "to": to_ep,
            "status": status,
        })

    return records, errors, classes, branches, zones


def write_csv(records):
    cols = [
        "wire_id", "branch", "branch_name", "region", "class",
        "preferred_gauge", "color", "routed_length_mm", "cut_length_mm",
        "net", "from", "to", "status",
    ]
    with (OUT / "WIRE-SCHEDULE.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(records)


def write_markdown(records):
    lines = [
        "# USS Defiant - Generated Harness Wire Schedule",
        "",
        "Generated from `eda/defiant-connectivity.xml` + `harness/harness-topology.xml`.",
        "",
        "**Lengths, colors, and final gauges remain OPEN until hull measurements and load validation.**",
        "",
        "| ID | Branch | Class | Target gauge | Net | From | To | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            f"| {r['wire_id']} | {r['branch']} | {r['class']} | {r['preferred_gauge']} | "
            f"`{r['net']}` | {r['from']} | {r['to']} | {r['status']} |"
        )
    (OUT / "WIRE-SCHEDULE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_endpoint_matrix(records):
    with (OUT / "PIN-ENDPOINT-MATRIX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["wire_id", "net", "endpoint_A", "endpoint_B", "branch", "status"])
        for r in records:
            w.writerow([r["wire_id"], r["net"], r["from"], r["to"], r["branch"], r["status"]])


def esc(s):
    return html.escape(str(s), quote=True)


def write_overview_svg(records, branches, zones):
    # Functional topology only; this is intentionally not a dimensioned hull drawing.
    W, H = 1600, 980
    boxes = {
        "Z-VENTRAL": (70, 170, 280, 180),
        "Z-CENTRAL": (555, 155, 500, 300),
        "Z-DORSAL": (1260, 170, 270, 180),
        "Z-LIGHT": (360, 650, 880, 190),
        "Z-PHASER": (70, 650, 240, 190),
    }
    zone_map = {z["id"]: z for z in zones}
    branch_map = {b["id"]: b for b in branches}
    counts = defaultdict(int)
    for r in records:
        if not r["status"].startswith("DNP"):
            counts[r["branch"]] += 1

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="980" viewBox="0 0 {W} {H}">',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111}.box{fill:#fff;stroke:#111;stroke-width:3}.wire{fill:none;stroke:#111;stroke-width:5}.future{fill:none;stroke:#555;stroke-width:4;stroke-dasharray:12 10}.title{font-size:30px;font-weight:700}.sub{font-size:20px;font-weight:700}.lab{font-size:16px}.small{font-size:13px}.tag{fill:#fff;stroke:#111;stroke-width:2}</style>',
        '<text x="55" y="55" class="title">USS Defiant - Functional Harness Topology</text>',
        '<text x="55" y="86" class="lab">VeSys-style functional view - not dimensioned - W067+ final power branches remain open</text>',
    ]

    for zid, (x,y,w,h) in boxes.items():
        z = zone_map.get(zid, {"name": zid, "members": ""})
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="box"/>')
        out.append(f'<text x="{x+w/2}" y="{y+35}" class="sub" text-anchor="middle">{esc(z.get("name",zid))}</text>')
        members = z.get("members", "")
        # Wrap members by commas to avoid long overlapping text.
        tokens = [t.strip() for t in members.split(",") if t.strip()]
        rows=[]; current=[]; current_len=0
        for t in tokens:
            if current and current_len + len(t) + 2 > 42:
                rows.append(", ".join(current)); current=[t]; current_len=len(t)
            else:
                current.append(t); current_len += len(t)+2
        if current: rows.append(", ".join(current))
        yy=y+70
        for row in rows[:6]:
            out.append(f'<text x="{x+18}" y="{yy}" class="small">{esc(row)}</text>')
            yy += 22

    def path(points, cls="wire"):
        pts=" ".join(f"{x},{y}" for x,y in points)
        out.append(f'<polyline points="{pts}" class="{cls}"/>')

    # Bundle routes between functional zones. These are topology lines, not individual conductors.
    path([(350,250),(555,250)])  # WLC -> central
    path([(805,455),(805,650)])  # central -> lighting
    path([(555,370),(310,370),(310,650)])  # central -> phaser
    path([(1055,250),(1260,250)]) # central -> NFC
    path([(555,220),(475,220),(475,510),(930,510),(930,455)]) # internal battery/primary path cue

    labels = [
        (390,222,"H-WLC",f"{counts['H-WLC']} conductors", "PWR-B / SIG-B"),
        (825,535,"H-SKDATA",f"{counts['H-SKDATA']} conductors", "30 AWG target"),
        (340,510,"H-PHASER",f"{counts['H-PHASER']} conductors", "factory lead / 30 AWG"),
        (1090,222,"H-NFC",f"{counts['H-NFC']} conductors", "26/30 AWG target"),
        (575,475,"H-BAT / H-CTRL",f"{counts['H-BAT']+counts['H-CTRL']} defined conductors", "central island"),
    ]
    for x,y,a,b,c in labels:
        width=max(170, 9*max(len(a),len(b),len(c))+30)
        out.append(f'<rect x="{x}" y="{y}" width="{width}" height="76" rx="8" class="tag"/>')
        out.append(f'<text x="{x+12}" y="{y+23}" class="sub">{esc(a)}</text>')
        out.append(f'<text x="{x+12}" y="{y+45}" class="small">{esc(b)}</text>')
        out.append(f'<text x="{x+12}" y="{y+64}" class="small">{esc(c)}</text>')

    # Future final lighting power branches.
    path([(805,455),(1110,575),(1110,650)], "future")
    out.append('<rect x="1130" y="548" width="365" height="76" rx="8" class="tag"/>')
    out.append('<text x="1142" y="573" class="sub">H-LIGHT-PWR-FUTURE</text>')
    out.append('<text x="1142" y="595" class="small">W067+ front / port / starboard +5V &amp; GND</text>')
    out.append('<text x="1142" y="614" class="small">assigned only after hull measurements</text>')

    out.append('<text x="55" y="920" class="lab">Solid = defined functional harness branch. Dashed = reserved future physical distribution branch.</text>')
    out.append('<text x="55" y="948" class="lab">The electrical source of truth remains defiant-connectivity.xml; this drawing adds physical branch/bundle organization only.</text>')
    out.append('</svg>')
    (OUT / "HARNESS-OVERVIEW.svg").write_text("\n".join(out), encoding="utf-8")


def write_validation(records, errors):
    active = [r for r in records if not r["status"].startswith("DNP")]
    dnp = [r for r in records if r["status"].startswith("DNP")]
    unresolved = [r for r in active if r["from"] == "OPEN" or r["to"] == "OPEN" or r["net"] == "OPEN"]
    lines = [
        "# USS Defiant - Harness Generation Validation",
        "",
        f"- Defined W001-W066 records: **{len(records)}**",
        f"- Active/conditional records: **{len(active)}**",
        f"- DNP/superseded records: **{len(dnp)}** ({', '.join(r['wire_id'] for r in dnp)})",
        f"- Unresolved active endpoints/nets: **{len(unresolved)}**",
        f"- Generator errors: **{len(errors)}**",
        "",
    ]
    if errors:
        lines.append("## Errors")
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("**RESULT: PASS - all currently defined W001-W066 conductors resolve to a functional branch and two endpoints or an approved distribution-node override.**")
    lines += [
        "",
        "## Intentionally open physical data",
        "",
        "- routed/cut lengths",
        "- wire colors",
        "- final gauge acceptance after load testing",
        "- splice/junction physical coordinates",
        "- W067+ front/port/starboard lighting power-distribution conductors",
    ]
    (OUT / "HARNESS-VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("\n".join(errors))


def main():
    records, errors, classes, branches, zones = build_records()
    write_csv(records)
    write_markdown(records)
    write_endpoint_matrix(records)
    write_overview_svg(records, branches, zones)
    write_validation(records, errors)
    print(f"Generated {len(records)} wire records in {OUT}")


if __name__ == "__main__":
    main()
