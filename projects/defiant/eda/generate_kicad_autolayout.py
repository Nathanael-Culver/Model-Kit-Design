#!/usr/bin/env python3
"""Flow-aware, character-aware KiCad generation wrapper for the Defiant.

The semantic XML remains the hardware source of truth. This wrapper adds only
EDA presentation/ERC metadata:
- conservative text-aware symbol sizing and collision checks;
- subsystem-specific circuit-flow placement rather than arbitrary grid packing;
- direct orthogonal routing for safe two-terminal local nets, while preserving
  one explicit net label and one wire-ID annotation per routed net;
- automatic standard-sheet promotion when a flow lane needs more room;
- KiCad-only power-flow markers for supplies that pass through passive
  semiconductor pins, so ERC can understand the intended source path;
- passive classification of module/battery negative reference terminals to
  avoid falsely treating ground-return pins as competing power sources.

No presentation rule in this file is allowed to change electrical connectivity.
"""
import copy
import generate_kicad as g

# ---------------------------------------------------------------------------
# KiCad ERC and presentation metadata overrides.
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

            # Presentation-only side changes. They make the drawn current/data
            # flow face the adjacent device without changing any net or pin.
            if c['ref'].startswith('LED'):
                try:
                    n=int(c['ref'][3:])
                except ValueError:
                    n=-1
                # Bottom half of the 14-pixel snake is drawn right-to-left.
                if 21 <= n <= 27:
                    if p.get('name')=='DIN': p['side']='right'
                    if p.get('name')=='DOUT': p['side']='left'
            if c['ref'] in {'Q3','Q4','Q5','Q6'} and p.get('name')=='D':
                # Put phaser MOSFET drain toward the LED cathode.
                p['side']='left'
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
    active=[r for r in rows if r]
    needed=FLOW_TOP+FLOW_BOTTOM
    needed+=sum(_row_height(row,byref) for row in active)
    needed+=max(0,len(active)-1)*FLOW_GAP_Y
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
        return [
            _existing(['BT1','Q1','U2'],byref),
            _existing(['U5','R3','Q2','R4'],byref),
            _existing(['RX1','D1'],byref),
            _existing(['R1','R2'],byref),
        ], ['center','center','left','left'], [
            'BATTERY -> HIGH-SIDE SWITCH -> 5 V BOOST',
            'LIGHTING POWER-GATE CONTROL',
            'WIRELESS CHARGING / RECOVERY PATH',
            'WIRELESS-PRESENT DIVIDER / SYSTEM RETURN',
        ]
    if key=='controller':
        return [_existing(['U1'],byref)], ['center'], ['MASTER CONTROLLER / ALL GPIO ASSIGNMENTS']
    if key=='lighting':
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
        rows=[]; labels=[]
        for ch in range(4):
            rows.append(_existing([f'R{6+ch}',f'LED{10+ch}',f'Q{3+ch}',f'R{10+ch}'],byref))
            labels.append(f'PH{ch}: +5V -> R{6+ch} -> LED{10+ch} -> Q{3+ch} -> GND   |   R{10+ch} GATE PULL-DOWN')
        return rows,['center']*4,labels
    if key=='nfc':
        return [
            _existing(['Q7','R14','Q8','R15','R16'],byref),
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


def _annotation_text(key,label,y,index):
    return f' (text "{g.esc(label)}" (at 20 {max(29.0,y):.2f} 0) {g.eff(1.05)} (uuid {g.U(f"standalone:{key}:lane:{index}")}))'


def _pin_xy(d,x,y,p):
    c,lid,yp,geom=d
    side=p.get('side','left')
    px=x-geom['pin_outer'] if side=='left' else x+geom['pin_outer']
    py=y-yp[id(p)]
    return g.snap(px),g.snap(py)


def _direct_nets(key):
    if key=='power':
        return {'U2_VIN_SW'}
    if key=='lighting':
        return {'SK_DATA_5V','SK_DIN_FIRST'} | {f'SK_{i}_{i+1}' for i in range(14,27)}
    if key=='phasers':
        return {f'PH{i}_LED_ANODE' for i in range(4)} | {f'PH{i}_SINK' for i in range(4)}
    return set()


def _standalone_instance(c,lid,yp,geom,x,y,sch_uuid,tagbase,suppress_nets):
    """Original KiCad symbol instance, but omit per-pin label stubs for nets
    that will be drawn once as a direct routed connection on this sheet."""
    hw=geom['hw']; hh=geom['hh']; pin_outer=geom['pin_outer']
    sym_uuid=g.U(tagbase+':sym')
    o=['(symbol',f' (lib_id "{lid}")',f' (at {x:.2f} {y:.2f} 0)',
       ' (unit 1) (exclude_from_sim no) (in_bom yes) (on_board no)']
    if c.get('status')=='dnp': o.append(' (dnp yes)')
    o += [f' (uuid {sym_uuid})',
          f' (property "Reference" "{c["ref"]}" (at {x:.2f} {y-hh-4.0:.2f} 0) {g.eff(1.0)})',
          f' (property "Value" "{g.esc(c["part"])}" (at {x:.2f} {y+hh+5.0:.2f} 0) {g.eff(g.VALUE_FONT)})',
          f' (property "Footprint" "" (at {x} {y} 0) {g.eff(hide=True)})',
          f' (property "Datasheet" "" (at {x} {y} 0) {g.eff(hide=True)})',
          f' (property "DesignNote" "{g.esc(c.get("note",""))}" (at {x} {y} 0) {g.eff(0.8,hide=True)})']
    for p in c['pins']:
        o.append(f' (pin "{g.esc(p["number"])}" (uuid {g.U(tagbase+":pin:"+p["number"])}))')
    o += [f' (instances (project "{g.PROJECT}" (path "/{sch_uuid}" (reference "{c["ref"]}") (unit 1))))',')']

    graphics=[]
    for p in c['pins']:
        side=p.get('side','left')
        px=x-pin_outer if side=='left' else x+pin_outer
        py=y-yp[id(p)]
        if c.get('status') in ('dnp','external') or p.get('status')=='nc':
            graphics.append(g.nc(px,py,tagbase+':nc:'+p['number']))
            continue
        if p.get('net'):
            if p['net'] in suppress_nets:
                continue
            lx=px-g.LABEL_STUB if side=='left' else px+g.LABEL_STUB
            graphics.append(g.wire(px,py,lx,py,tagbase+':wire:'+p['number']))
            graphics.append(g.label(p['net'],lx,py,side,tagbase+':label:'+p['number']))
            if p.get('wire'):
                graphics.append(g.wire_id_text(p['wire'],(px+lx)/2.0,py-2.3,tagbase+':wireid:'+p['number']))
    return '\n'.join(o),graphics


def _route_two_pin_net(key,netname,endpoints,index):
    """Orthogonal route between exactly two local pin endpoints. One label names
    the net, so KiCad preserves the semantic net name. One wire ID is shown."""
    (d1,x1,y1,p1),(d2,x2,y2,p2)=endpoints
    a=_pin_xy(d1,x1,y1,p1); b=_pin_xy(d2,x2,y2,p2)
    ax,ay=a; bx,by=b
    tag=f'standalone:{key}:direct:{netname}'
    out=[]
    if abs(ay-by)<0.01:
        out.append(g.wire(ax,ay,bx,by,tag+':0'))
        mx=(ax+bx)/2.0; my=ay
    else:
        mx=g.snap((ax+bx)/2.0)
        out.append(g.wire(ax,ay,mx,ay,tag+':0'))
        out.append(g.wire(mx,ay,mx,by,tag+':1'))
        out.append(g.wire(mx,by,bx,by,tag+':2'))
        my=(ay+by)/2.0
    # Label at the midpoint names the electrical net without duplicate labels at
    # both components. Put it slightly above the route for readability.
    out.append(f'(label "{g.esc(netname)}" (at {mx:.2f} {g.snap(my-2.54):.2f} 0) {g.eff(g.LABEL_FONT)} (uuid {g.U(tag+":label")}))')
    wireids=[p.get('wire') for _,_,_,p in endpoints if p.get('wire')]
    wid=next((w for w in wireids if w),None)
    if wid:
        out.append(g.wire_id_text(wid,mx,g.snap(my+2.54),tag+':wireid'))
    return out


def _direct_routes(key,pos,direct_nets):
    bynet={n:[] for n in direct_nets}
    for d,x,y in pos:
        c=d[0]
        for p in c['pins']:
            n=p.get('net')
            if n in bynet and c.get('status') not in ('dnp','external') and p.get('status')!='nc':
                bynet[n].append((d,x,y,p))
    out=[]
    for i,n in enumerate(sorted(direct_nets)):
        eps=bynet.get(n,[])
        if len(eps)!=2:
            raise RuntimeError(f'Direct-route net {n} expected exactly 2 visible local endpoints, found {len(eps)}')
        out += _route_two_pin_net(key,n,eps,i)
    return out


def make_standalone_flow(key, comps):
    sch_uuid=g.U('standalone:'+key)

    # ERC-only PWR_FLAG helpers belong in the canonical flat drawing, not the
    # human build sheets. This keeps subsystem PDFs limited to physical parts.
    visible=[c for c in comps if c.get('eda_only')!='yes']
    defs=[]; prepared=[]
    for c in visible:
        lid,ld,yp,geom=g.libdef(c)
        defs.append(ld)
        prepared.append((c,lid,yp,geom))
    byref=_by_ref(prepared)
    rows,aligns,lane_labels=_flow_spec(key,byref)

    named={r for row in rows for r in row}
    remaining=[d[0]['ref'] for d in prepared if d[0]['ref'] not in named]
    if remaining:
        rows.append(remaining)
        aligns.append('center')
        lane_labels.append('ADDITIONAL / UNCLASSIFIED PHYSICAL ITEMS')

    paper,page_w,page_h=_choose_flow_page(rows,byref)
    pos,lane_centers=_layout_rows(rows,byref,page_w,page_h,aligns)
    direct=_direct_nets(key)

    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',
       f' (uuid {sch_uuid})',f' (paper "{paper}")',
       f' (title_block (title "USS Defiant - {key.title()}") (rev "2.5") (company "Model-Kit-Design"))',
       ' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]
    o += [' )',
          f' (text "GENERATED FROM ../eda/defiant-connectivity.xml - FLOW + NET-AWARE ROUTING - {paper}" (at 20 20 0) {g.eff()} (uuid {g.U("standalone:"+key+":banner")}))']

    active_rows=[r for r in rows if r]
    for i,(label,cy,row) in enumerate(zip(lane_labels,lane_centers,active_rows)):
        h=_row_height(row,byref)
        ly=cy-h/2.0-5.5
        if ly>25.0:
            o.append(_annotation_text(key,label,ly,i))

    for d,x,y in pos:
        c,lid,yp,geom=d
        si,graphics=_standalone_instance(c,lid,yp,geom,x,y,sch_uuid,f'standalone:{key}:{c["ref"]}',direct)
        o.append(' '+si.replace('\n','\n '))
        o += [' '+q for q in graphics]

    # Actual direct wires are emitted after symbols. The XML/KiCad flat-netlist
    # cross-check remains authoritative for connectivity; this view is a
    # deterministic presentation of those same named nets.
    o += [' '+q for q in _direct_routes(key,pos,direct)]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    print(f'{key}: selected {paper}; {len(prepared)} physical components; {len(direct)} direct-routed nets; collision check PASS')
    return '\n'.join(o)


g.make_standalone=make_standalone_flow

if __name__=='__main__':
    g.main()
