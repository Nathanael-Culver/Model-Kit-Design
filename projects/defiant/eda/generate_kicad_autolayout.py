#!/usr/bin/env python3
"""Flow-aware, character-aware KiCad generation wrapper for the Defiant.

The semantic XML remains the hardware source of truth. This wrapper adds only
EDA presentation/ERC metadata:
- conservative text-aware symbol sizing and collision checks;
- subsystem-specific circuit-flow placement rather than arbitrary grid packing;
- automatic standard-sheet promotion when a flow lane needs more room;
- KiCad-only power-flow markers for supplies that pass through passive
  semiconductor pins, so ERC can understand the intended source path;
- passive classification of module/battery negative reference terminals to
  avoid falsely treating ground-return pins as competing power sources.

No presentation rule in this file is allowed to change electrical connectivity.
"""
import copy
import math
import generate_kicad as g

# ---------------------------------------------------------------------------
# KiCad ERC modeling overrides. These are EDA metadata only.
# ---------------------------------------------------------------------------
_original_parse = g.parse
_original_libdef = g.libdef
_original_instance = g.instance

PIN_TYPE_OVERRIDES = {
    ('BT1', '-'): 'passive',
    ('RX1', '-'): 'passive',
    ('U2', 'VOUT-'): 'passive',
}

ERC_FLAGS = [
    {
        'ref':'PF1','part':'PWR_FLAG - ERC only','sheet':'power','status':'active','eda_only':'yes',
        'note':'KiCad ERC marker: power reaches U2_VIN_SW through Q1; no physical part.',
        'pins':[{'number':'1','name':'PWR_FLAG','type':'power_out','side':'right','status':'active','net':'U2_VIN_SW'}],
    },
    {
        'ref':'PF2','part':'PWR_FLAG - ERC only','sheet':'power','status':'active','eda_only':'yes',
        'note':'KiCad ERC marker: power reaches SYS_5V_IN through D1; no physical part.',
        'pins':[{'number':'1','name':'PWR_FLAG','type':'power_out','side':'right','status':'active','net':'SYS_5V_IN'}],
    },
    {
        'ref':'PF3','part':'PWR_FLAG - ERC only','sheet':'nfc','status':'active','eda_only':'yes',
        'note':'KiCad ERC marker: power reaches +3V3_NFC_SW through Q7; no physical part.',
        'pins':[{'number':'1','name':'PWR_FLAG','type':'power_out','side':'right','status':'active','net':'+3V3_NFC_SW'}],
    },
    {
        'ref':'PF4','part':'PWR_FLAG - ERC only','sheet':'power','status':'active','eda_only':'yes',
        'note':'KiCad ERC marker: common GND is the system return/reference; no physical part.',
        'pins':[{'number':'1','name':'PWR_FLAG','type':'power_out','side':'right','status':'active','net':'GND'}],
    },
]


def parse_with_erc_metadata():
    comps=copy.deepcopy(_original_parse())
    for c in comps:
        for p in c['pins']:
            override=PIN_TYPE_OVERRIDES.get((c['ref'],p['number']))
            if override:
                p['type']=override
    comps.extend(copy.deepcopy(ERC_FLAGS))
    return comps


def libdef_with_eda_only(c):
    lid,definition,yp,geom=_original_libdef(c)
    if c.get('eda_only')=='yes':
        definition=definition.replace('(in_bom yes)','(in_bom no)',1)
    return lid,definition,yp,geom


def instance_with_eda_only(c,lid,yp,geom,x,y,sch_uuid,tagbase):
    definition,graphics=_original_instance(c,lid,yp,geom,x,y,sch_uuid,tagbase)
    if c.get('eda_only')=='yes':
        definition=definition.replace('(in_bom yes)','(in_bom no)',1)
    return definition,graphics


g.parse=parse_with_erc_metadata
g.libdef=libdef_with_eda_only
g.instance=instance_with_eda_only

# ---------------------------------------------------------------------------
# Flow-aware presentation layer.
# ---------------------------------------------------------------------------

PAPERS=[
    ('A4',297.0,210.0),
    ('A3',420.0,297.0),
    ('A2',594.0,420.0),
    ('A1',841.0,594.0),
    ('A0',1189.0,841.0),
]
FLOW_MARGIN_X=25.4
FLOW_TOP=48.0
FLOW_BOTTOM=24.0
FLOW_GAP_X=15.24
FLOW_GAP_Y=18.0


def _by_ref(prepared):
    return {d[0]['ref']:d for d in prepared}


def _existing(refs, byref):
    return [r for r in refs if r in byref]


def _row_width(row, byref, gap=FLOW_GAP_X):
    ds=[byref[r] for r in row]
    return sum(d[3]['visual_w'] for d in ds) + max(0,len(ds)-1)*gap


def _row_height(row, byref):
    return max((byref[r][3]['visual_h'] for r in row), default=0.0)


def _rows_fit(rows, byref, page_w, page_h):
    usable=page_w-2*FLOW_MARGIN_X
    if any(_row_width(row,byref)>usable for row in rows if row):
        return False
    needed=FLOW_TOP+FLOW_BOTTOM
    needed+=sum(_row_height(row,byref) for row in rows if row)
    needed+=max(0,len([r for r in rows if r])-1)*FLOW_GAP_Y
    return needed<=page_h


def _layout_rows(rows, byref, page_w, page_h, row_align=None):
    """Place geometry-aware rows; each row may be left/center/right aligned."""
    rows=[r for r in rows if r]
    row_align=row_align or ['center']*len(rows)
    if len(row_align)<len(rows):
        row_align=row_align+['center']*(len(rows)-len(row_align))
    y=FLOW_TOP
    pos=[]
    lane_centers=[]
    for idx,row in enumerate(rows):
        h=_row_height(row,byref)
        rw=_row_width(row,byref)
        align=row_align[idx]
        if align=='left':
            x=FLOW_MARGIN_X
        elif align=='right':
            x=page_w-FLOW_MARGIN_X-rw
        else:
            x=(page_w-rw)/2.0
        cy=y+h/2.0
        lane_centers.append(cy)
        for ref in row:
            d=byref[ref]
            w=d[3]['visual_w']
            cx=g.snap(x+w/2.0)
            pos.append((d,cx,g.snap(cy)))
            x+=w+FLOW_GAP_X
        y+=h+FLOW_GAP_Y
    if y+FLOW_BOTTOM>page_h:
        raise RuntimeError(f'Flow layout needs {y+FLOW_BOTTOM:.1f} mm on {page_h:.1f} mm page')
    g.assert_nonoverlap(pos)
    return pos,lane_centers


def _flow_spec(key,byref):
    """Return ordered visual lanes. Connectivity still comes entirely from XML."""
    if key=='power':
        # Main battery/boost path, gate-control network, wireless charge path,
        # then wireless-present divider / ERC markers.
        return [
            _existing(['BT1','Q1','U2'],byref),
            _existing(['U5','R3','Q2','R4','PF1'],byref),
            _existing(['RX1','D1','PF2'],byref),
            _existing(['R1','R2','PF4'],byref),
        ], ['center','center','left','left'], [
            'BATTERY -> HIGH-SIDE SWITCH -> 5 V BOOST',
            'LIGHTING POWER-GATE CONTROL',
            'WIRELESS CHARGING / RECOVERY PATH',
            'WIRELESS-PRESENT DIVIDER / SYSTEM RETURN',
        ]
    if key=='controller':
        return [_existing(['U1'],byref)], ['center'], ['MASTER CONTROLLER / ALL GPIO ASSIGNMENTS']
    if key=='lighting':
        # The actual data chain is left-to-right across the first pixel row,
        # then snakes back right-to-left across the second row.
        return [
            _existing(['U4','C1','R5','C2'],byref),
            _existing([f'LED{i}' for i in range(14,21)],byref),
            _existing([f'LED{i}' for i in range(27,20,-1)],byref),
        ], ['left','center','center'], [
            'DATA LEVEL SHIFT / LOCAL 5 V SUPPORT',
            'SK6812 DATA CHAIN: LED14 -> LED20',
            'SK6812 DATA CHAIN CONTINUED: LED21 -> LED27  (DRAWN RIGHT-TO-LEFT)',
        ]
    if key=='phasers':
        # Each row is one complete independent channel. The current-limit
        # resistor and LED lead into the MOSFET; the 100k is the gate pull-down.
        rows=[]; labels=[]
        for ch in range(4):
            rows.append(_existing([f'R{6+ch}',f'LED{10+ch}',f'Q{3+ch}',f'R{10+ch}'],byref))
            labels.append(f'PH{ch}: +5V -> R{6+ch} -> LED{10+ch} -> Q{3+ch} -> GND   |   R{10+ch} GATE PULL-DOWN')
        return rows,['center']*4,labels
    if key=='nfc':
        return [
            _existing(['Q7','R14','Q8','R15','R16','PF3'],byref),
            _existing(['R18','U3','R17'],byref),
        ], ['left','center'], [
            'SWITCHED 3.3 V NFC POWER GATE',
            'V602 READER / SPI / RESET & GPIO2 BOOT BIAS',
        ]
    return [list(byref.keys())],['center'],[key.upper()]


def _choose_flow_page(rows,byref):
    last=None
    for paper,w,h in PAPERS:
        if _rows_fit(rows,byref,w,h):
            return paper,w,h
        last=(paper,w,h)
    raise RuntimeError(f'No standard page fits flow-aware rows; largest tried {last}')


def _annotation_text(key, label, y, page_w, index):
    return f' (text "{g.esc(label)}" (at 20 {max(29.0,y):.2f} 0) {g.eff(1.05)} (uuid {g.U(f"standalone:{key}:lane:{index}")}))'


def make_standalone_flow(key, comps):
    sch_uuid=g.U('standalone:'+key)
    defs=[]; prepared=[]
    for c in comps:
        lid,ld,yp,geom=g.libdef(c)
        defs.append(ld)
        prepared.append((c,lid,yp,geom))
    byref=_by_ref(prepared)
    rows,aligns,lane_labels=_flow_spec(key,byref)

    # Anything not mentioned in a flow spec is appended as a final lane so a
    # future XML component can never silently disappear from the drawing.
    named={r for row in rows for r in row}
    remaining=[d[0]['ref'] for d in prepared if d[0]['ref'] not in named]
    if remaining:
        rows.append(remaining)
        aligns.append('center')
        lane_labels.append('ADDITIONAL / UNCLASSIFIED EDA ITEMS')

    paper,page_w,page_h=_choose_flow_page(rows,byref)
    pos,lane_centers=_layout_rows(rows,byref,page_w,page_h,aligns)

    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',
       f' (uuid {sch_uuid})',f' (paper "{paper}")',
       f' (title_block (title "USS Defiant - {key.title()}") (rev "2.4") (company "Model-Kit-Design"))',
       ' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]
    o += [' )',
          f' (text "GENERATED FROM ../eda/defiant-connectivity.xml - FLOW-AWARE + CHARACTER-AWARE - {paper}" (at 20 20 0) {g.eff()} (uuid {g.U("standalone:"+key+":banner")}))']

    # Lane labels are intentionally above each row and outside the component
    # visual envelopes. They explain circuit intent without changing nets.
    for i,(label,cy,row) in enumerate(zip(lane_labels,lane_centers,[r for r in rows if r])):
        h=_row_height(row,byref)
        ly=cy-h/2.0-5.5
        if ly>25.0:
            o.append(_annotation_text(key,label,ly,page_w,i))

    for d,x,y in pos:
        c,lid,yp,geom=d
        si,graphics=g.instance(c,lid,yp,geom,x,y,sch_uuid,f'standalone:{key}:{c["ref"]}')
        o.append(' '+si.replace('\n','\n '))
        o += [' '+q for q in graphics]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    print(f'{key}: selected {paper}; {len(prepared)} displayed EDA components; flow-aware collision check PASS')
    return '\n'.join(o)


g.make_standalone=make_standalone_flow

if __name__=='__main__':
    g.main()
