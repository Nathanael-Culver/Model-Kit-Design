#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import json, uuid, re, math

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
K=ROOT/'kicad'; K.mkdir(exist_ok=True)
XML=BASE/'defiant-connectivity.xml'
PROJECT='USS-Defiant'
NS=uuid.UUID('9ac8ff9b-cf8e-4ea4-a2e1-5fa7d3d94f70')

# KiCad drafting geometry. These values are intentionally generous because the
# generated drawings must remain readable on a phone and must not depend on a
# human cleaning up collisions after generation.
GRID=1.27
PIN_PITCH=5.08
PIN_LEN=5.08
LABEL_STUB=15.24
PIN_FONT=0.90
LABEL_FONT=0.90
VALUE_FONT=0.90
CHAR_MM=0.72          # conservative average rendered character width at 1 mm text
PAGE_GAP_X=12.70
PAGE_GAP_Y=15.24
PAGE_MARGIN_X=20.32
PAGE_MARGIN_Y=22.86


def U(tag): return str(uuid.uuid5(NS,tag))
def esc(s): return str(s).replace('\\','\\\\').replace('"','\\"')
def eff(sz=1.27,hide=False): return f'(effects (font (size {sz} {sz}))'+(' hide' if hide else '')+')'
def snap(v): return round(v/GRID)*GRID

def text_width(s, size=1.0):
    return max(0.0, len(str(s))*CHAR_MM*size)

def parse():
    r=ET.parse(XML).getroot(); out=[]
    for c in r.find('components'):
        d=dict(c.attrib)
        d['pins']=[dict(p.attrib) for p in c.findall('pin')]
        out.append(d)
    return out

def side_pins(pins, side):
    return [p for p in pins if p.get('side','left')==side]

def ypos(pins):
    ans={}
    for side in ('left','right'):
        a=side_pins(pins,side)
        top=(len(a)-1)*PIN_PITCH/2.0
        for i,p in enumerate(a):
            ans[id(p)]=round(top-i*PIN_PITCH,2)
    return ans

def geometry(c):
    pins=c['pins']
    left=side_pins(pins,'left'); right=side_pins(pins,'right')
    max_pin_name=max([len(p.get('name','')) for p in pins] or [1])
    max_pin_num=max([len(p.get('number','')) for p in pins] or [1])

    # Body width grows with the longest pin name/number rather than remaining
    # fixed. U1 therefore gets a much wider body than a resistor or LED pixel.
    hw=max(17.78, 8.0 + text_width('M'*max_pin_name, PIN_FONT)/2.0 + text_width('M'*max_pin_num, PIN_FONT)/4.0)
    n=max(len(left),len(right),1)
    hh=max(7.62, (n-1)*PIN_PITCH/2.0 + 5.08)
    pin_outer=hw+PIN_LEN

    def external_width(side):
        a=left if side=='left' else right
        labels=[p.get('net','') for p in a if p.get('net') and c.get('status') not in ('dnp','external') and p.get('status')!='nc']
        wireids=[p.get('wire','') for p in a if p.get('wire')]
        label_w=max([text_width(x,LABEL_FONT) for x in labels] or [0])
        wire_w=max([text_width(x,0.72) for x in wireids] or [0])
        return PIN_LEN+LABEL_STUB+max(label_w,wire_w)+5.08

    left_ext=external_width('left'); right_ext=external_width('right')
    body_w=2*hw
    value_w=text_width(c.get('part',''),VALUE_FONT)+5.08
    visual_w=max(body_w+left_ext+right_ext, value_w+10.16)
    visual_h=2*hh+20.32
    return {
        'hw':snap(hw),'hh':snap(hh),'pin_outer':snap(pin_outer),
        'left_ext':left_ext,'right_ext':right_ext,
        'visual_w':snap(visual_w),'visual_h':snap(visual_h),
    }

def libdef(c):
    pins=c['pins']; yp=ypos(pins); g=geometry(c)
    hw=g['hw']; hh=g['hh']; pin_outer=g['pin_outer']
    safe=re.sub(r'[^A-Za-z0-9_]+','_',c['part']).strip('_')[:32] or 'Part'
    name=f'{c["ref"]}_{safe}'
    lid='Defiant:'+name
    prefix=''.join(ch for ch in c['ref'] if ch.isalpha()) or 'U'
    o=[f'(symbol "{lid}" (pin_names (offset 1.5)) (exclude_from_sim no) (in_bom yes) (on_board no)',
       f' (property "Reference" "{prefix}" (at 0 {hh+2.54:.2f} 0) {eff(1.0)})',
       f' (property "Value" "{esc(c["part"])}" (at 0 {-hh-3.81:.2f} 0) {eff(VALUE_FONT)})',
       f' (property "Footprint" "" (at 0 0 0) {eff(hide=True)})',
       f' (property "Datasheet" "" (at 0 0 0) {eff(hide=True)})',
       f' (property "DesignNote" "{esc(c.get("note",""))}" (at 0 0 0) {eff(0.8,hide=True)})',
       f' (symbol "{name}_1_1" (rectangle (start {-hw:.2f} {hh:.2f}) (end {hw:.2f} {-hh:.2f}) (stroke (width 0.254) (type default)) (fill (type background)))']
    valid={'input','output','bidirectional','tri_state','passive','power_in','power_out','open_collector','open_emitter','no_connect','free'}
    for p in pins:
        side=p.get('side','left'); x=-pin_outer if side=='left' else pin_outer; ang=0 if side=='left' else 180
        typ=p.get('type','passive'); typ=typ if typ in valid else 'passive'
        o.append(f'  (pin {typ} line (at {x:.2f} {yp[id(p)]:.2f} {ang}) (length {PIN_LEN:.2f}) (name "{esc(p["name"])}" {eff(PIN_FONT)}) (number "{esc(p["number"])}" {eff(PIN_FONT)}))')
    o+=[' ))']
    return lid,'\n'.join(o),yp,g

def label(net,x,y,side,tag):
    # Place labels beyond a visible wire stub. Text extends away from the symbol.
    ang=180 if side=='left' else 0
    return f'(label "{esc(net)}" (at {x:.2f} {y:.2f} {ang}) {eff(LABEL_FONT)} (uuid {U(tag)}))'

def nc(x,y,tag): return f'(no_connect (at {x:.2f} {y:.2f}) (uuid {U(tag)}))'

def wire(x1,y1,x2,y2,tag):
    return f'(wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) (stroke (width 0) (type default)) (uuid {U(tag)}))'

def wire_id_text(wid,x,y,tag):
    return f'(text "{esc(wid)}" (at {x:.2f} {y:.2f} 0) {eff(0.72)} (uuid {U(tag)}))'

def instance(c,lid,yp,g,x,y,sch_uuid,tagbase):
    hw=g['hw']; hh=g['hh']; pin_outer=g['pin_outer']
    sym_uuid=U(tagbase+':sym')
    o=['(symbol',f' (lib_id "{lid}")',f' (at {x:.2f} {y:.2f} 0)',' (unit 1) (exclude_from_sim no) (in_bom yes) (on_board no)']
    if c.get('status')=='dnp': o.append(' (dnp yes)')
    o += [f' (uuid {sym_uuid})',
          f' (property "Reference" "{c["ref"]}" (at {x:.2f} {y-hh-4.0:.2f} 0) {eff(1.0)})',
          f' (property "Value" "{esc(c["part"])}" (at {x:.2f} {y+hh+5.0:.2f} 0) {eff(VALUE_FONT)})',
          f' (property "Footprint" "" (at {x} {y} 0) {eff(hide=True)})',
          f' (property "Datasheet" "" (at {x} {y} 0) {eff(hide=True)})',
          f' (property "DesignNote" "{esc(c.get("note",""))}" (at {x} {y} 0) {eff(0.8,hide=True)})']
    for p in c['pins']:
        o.append(f' (pin "{esc(p["number"])}" (uuid {U(tagbase+":pin:"+p["number"])}))')
    o += [f' (instances (project "{PROJECT}" (path "/{sch_uuid}" (reference "{c["ref"]}") (unit 1))))',')']

    graphics=[]
    for p in c['pins']:
        side=p.get('side','left')
        px=x-pin_outer if side=='left' else x+pin_outer
        py=y-yp[id(p)]  # library symbol Y is inverted when transformed onto the sheet
        if c.get('status') in ('dnp','external') or p.get('status')=='nc':
            graphics.append(nc(px,py,tagbase+':nc:'+p['number']))
            continue
        if p.get('net'):
            lx=px-LABEL_STUB if side=='left' else px+LABEL_STUB
            graphics.append(wire(px,py,lx,py,tagbase+':wire:'+p['number']))
            graphics.append(label(p['net'],lx,py,side,tagbase+':label:'+p['number']))
            if p.get('wire'):
                graphics.append(wire_id_text(p['wire'],(px+lx)/2.0,py-2.3,tagbase+':wireid:'+p['number']))
    return '\n'.join(o),graphics

def pack_layout(prepared,page_w,page_h,start_y=35.0):
    # Use a conservative uniform cell based on the largest complete visual
    # envelope (symbol + pin names + pin numbers + wire stubs + net labels).
    maxw=max(d[3]['visual_w'] for d in prepared) if prepared else 50
    maxh=max(d[3]['visual_h'] for d in prepared) if prepared else 40
    cellw=maxw+PAGE_GAP_X; cellh=maxh+PAGE_GAP_Y
    usable_w=page_w-2*PAGE_MARGIN_X
    cols=max(1,int(usable_w//cellw))
    rows=math.ceil(len(prepared)/cols) if prepared else 0
    required_h=start_y+rows*cellh+PAGE_MARGIN_Y
    if required_h>page_h:
        raise RuntimeError(f'Generated layout needs {required_h:.1f} mm height on {page_h} mm page; enlarge page or reduce density')
    used_w=min(cols,len(prepared))*cellw if prepared else 0
    left=max(PAGE_MARGIN_X,(page_w-used_w)/2.0+cellw/2.0)
    pos=[]
    for i,d in enumerate(prepared):
        col=i%cols; row=i//cols
        x=snap(left+col*cellw)
        y=snap(start_y+cellh/2.0+row*cellh)
        pos.append((d,x,y))
    return pos, rows*cellh

def assert_nonoverlap(pos):
    boxes=[]
    for d,x,y in pos:
        c,lid,yp,g=d
        w=g['visual_w']; h=g['visual_h']
        box=(x-w/2,y-h/2,x+w/2,y+h/2,c['ref'])
        for a in boxes:
            if not (box[2]+1.0<a[0] or a[2]+1.0<box[0] or box[3]+1.0<a[1] or a[3]+1.0<box[1]):
                raise RuntimeError(f'Estimated schematic text/symbol collision: {box[4]} vs {a[4]}')
        boxes.append(box)

def make_standalone(key,comps):
    sch_uuid=U('standalone:'+key)
    defs=[]; prepared=[]
    for c in comps:
        lid,ld,yp,g=libdef(c); defs.append(ld); prepared.append((c,lid,yp,g))

    # A3 is enough for most subsystems. Lighting uses A2 because 14 long SK6812
    # values plus net labels benefit from extra room rather than dense packing.
    if key=='lighting':
        paper='A2'; page_w,page_h=594.0,420.0
    else:
        paper='A3'; page_w,page_h=420.0,297.0
    pos,_=pack_layout(prepared,page_w,page_h,start_y=38.0)
    assert_nonoverlap(pos)

    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {sch_uuid})',f' (paper "{paper}")',f' (title_block (title "USS Defiant - {key.title()}") (rev "2.2") (company "Model-Kit-Design"))',' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]
    o += [' )',f' (text "GENERATED FROM ../eda/defiant-connectivity.xml - CHARACTER-AWARE AUTOLAYOUT" (at 20 20 0) {eff()} (uuid {U("standalone:"+key+":banner")}))']
    for d,x,y in pos:
        c,lid,yp,g=d
        si,graphics=instance(c,lid,yp,g,x,y,sch_uuid,f'standalone:{key}:{c["ref"]}')
        o.append(' '+si.replace('\n','\n ')); o += [' '+q for q in graphics]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    return '\n'.join(o)

def make_flat(comps):
    sch_uuid=U('flat-root')
    defs=[]; prep={}
    for c in comps:
        lid,ld,yp,g=libdef(c); defs.append(ld); prep[c['ref']]=(c,lid,yp,g)
    groups={k:[prep[c['ref']] for c in comps if c['sheet']==k] for k in ('power','controller','lighting','phasers','nfc')}
    headers={'power':'POWER / CHARGING','controller':'CONTROLLER','lighting':'ADDRESSABLE LIGHTING','phasers':'PHASERS','nfc':'NFC'}

    # A0 gives the canonical all-in-one connectivity drawing enough room that
    # labels never have to be compressed merely to make the page fit.
    page_w,page_h=1189.0,841.0
    ycursor=40.0
    all_positions=[]; group_headers=[]
    for key in ('power','controller','lighting','phasers','nfc'):
        items=groups[key]
        pos,height=pack_layout(items,page_w,page_h,start_y=ycursor+12.0)
        # pack_layout returns coordinates from the requested start; retain only
        # this group's coordinates and move the next group below its last row.
        all_positions.extend(pos)
        group_headers.append((key,30.0,ycursor))
        max_bottom=max((y+d[3]['visual_h']/2 for d,x,y in pos), default=ycursor+20)
        ycursor=max_bottom+PAGE_GAP_Y+18.0
    if ycursor>page_h-PAGE_MARGIN_Y:
        raise RuntimeError(f'Flat schematic exceeds A0 page height: {ycursor:.1f} mm')
    assert_nonoverlap(all_positions)

    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {sch_uuid})',' (paper "A0")',' (title_block (title "USS Defiant 1/1000 - Complete Electrical Connectivity") (rev "2.2") (company "Model-Kit-Design"))',' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]; o += [' )']
    o.append(f' (text "CANONICAL FLAT CONNECTIVITY - generated from ../eda/defiant-connectivity.xml" (at 20 20 0) {eff(1.2)} (uuid {U("flat:banner")}))')
    for key,x,y in group_headers:
        o.append(f' (text "{headers[key]}" (at {x:.2f} {y:.2f} 0) {eff(1.5)} (uuid {U("flat:header:"+key)}))')
    for d,x,y in all_positions:
        c,lid,yp,g=d
        si,graphics=instance(c,lid,yp,g,x,y,sch_uuid,f'flat:{c["ref"]}')
        o.append(' '+si.replace('\n','\n ')); o += [' '+q for q in graphics]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    return '\n'.join(o),sch_uuid

def main():
    comps=parse()
    flat,root_uuid=make_flat(comps)
    (K/'USS-Defiant.kicad_sch').write_text(flat,encoding='utf-8')
    for key in ('power','controller','lighting','phasers','nfc'):
        (K/f'{key}.kicad_sch').write_text(make_standalone(key,[c for c in comps if c['sheet']==key]),encoding='utf-8')

    pro={'board':{},'boards':[],'erc':{'erc_exclusions':[],'meta':{'version':0},'rule_severities':{'duplicate_reference':'error','pin_not_connected':'error','multiple_net_names':'error','unannotated':'error','lib_symbol_issues':'ignore'}},'libraries':{'pinned_footprint_libs':[],'pinned_symbol_libs':[]},'meta':{'filename':'USS-Defiant.kicad_pro','version':1},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.8,'via_drill':0.4,'wire_width':6,'bus_width':12,'schematic_color':'rgba(0, 0, 0, 0.000)','pcb_color':'rgba(0, 0, 0, 0.000)'}],'meta':{'version':3},'net_colors':None,'netclass_assignments':None,'netclass_patterns':[]},'schematic':{'annotate_start_num':0,'meta':{'version':1},'page_layout_descr_file':'','plot_directory':''},'sheets':[[root_uuid,'Root']],'text_variables':{}}
    (K/'USS-Defiant.kicad_pro').write_text(json.dumps(pro,indent=2),encoding='utf-8')
    print(f'Generated character-aware KiCad schematic with {len(comps)} components and collision-checked subsystem views in {K}')

if __name__=='__main__':
    main()
