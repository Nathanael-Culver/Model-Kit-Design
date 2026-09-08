#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import json, uuid, re

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
K=ROOT/'kicad'; K.mkdir(exist_ok=True)
XML=BASE/'defiant-connectivity.xml'
PROJECT='USS-Defiant'
NS=uuid.UUID('9ac8ff9b-cf8e-4ea4-a2e1-5fa7d3d94f70')

def U(tag): return str(uuid.uuid5(NS,tag))
def esc(s): return str(s).replace('\\','\\\\').replace('"','\\"')
def eff(sz=1.27,hide=False): return f'(effects (font (size {sz} {sz}))'+(' hide' if hide else '')+')'

def parse():
    r=ET.parse(XML).getroot(); out=[]
    for c in r.find('components'):
        d=dict(c.attrib); d['pins']=[dict(p.attrib) for p in c.findall('pin')]; out.append(d)
    return out

def ypos(pins):
    ans={}
    for side in ('left','right'):
        a=[p for p in pins if p.get('side','left')==side]
        top=(len(a)-1)*1.27
        for i,p in enumerate(a): ans[id(p)]=round(top-i*2.54,2)
    return ans

def libdef(c):
    pins=c['pins']; yp=ypos(pins)
    n=max(sum(p.get('side')=='left' for p in pins),sum(p.get('side')=='right' for p in pins),1)
    hh=max(5.08,(n-1)*1.27+2.54); hw=10.16
    # KiCad library IDs are deliberately restricted to a conservative character set.
    # Human-readable punctuation remains in the Value field instead.
    safe=re.sub(r'[^A-Za-z0-9_]+','_',c['part']).strip('_')[:32] or 'Part'
    name=f'{c["ref"]}_{safe}'
    lid='Defiant:'+name
    prefix=''.join(ch for ch in c['ref'] if ch.isalpha()) or 'U'
    o=[f'(symbol "{lid}" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board no)',
       f' (property "Reference" "{prefix}" (at 0 {hh+2.54:.2f} 0) {eff()})',
       f' (property "Value" "{esc(c["part"])}" (at 0 {-hh-2.54:.2f} 0) {eff(1.0)})',
       f' (property "Footprint" "" (at 0 0 0) {eff(hide=True)})',
       f' (property "Datasheet" "" (at 0 0 0) {eff(hide=True)})',
       f' (symbol "{name}_1_1" (rectangle (start {-hw} {hh:.2f}) (end {hw} {-hh:.2f}) (stroke (width 0.254) (type default)) (fill (type background)))']
    valid={'input','output','bidirectional','tri_state','passive','power_in','power_out','open_collector','open_emitter','no_connect','free'}
    for p in pins:
        side=p.get('side','left'); x=-12.70 if side=='left' else 12.70; ang=0 if side=='left' else 180
        typ=p.get('type','passive'); typ=typ if typ in valid else 'passive'
        o.append(f'  (pin {typ} line (at {x} {yp[id(p)]:.2f} {ang}) (length 2.54) (name "{esc(p["name"])}" {eff(1.0)}) (number "{esc(p["number"])}" {eff(1.0)}))')
    o+=[' ))']; return lid,'\n'.join(o),yp,hh

def label(net,x,y,side,tag):
    # Local labels are used on the complete flat schematic. Same-name labels on
    # that single sheet are the electrical net; no visual line crossing is needed.
    ang=180 if side=='left' else 0
    return f'(label "{esc(net)}" (at {x:.2f} {y:.2f} {ang}) {eff(0.95)} (uuid {U(tag)}))'
def nc(x,y,tag): return f'(no_connect (at {x:.2f} {y:.2f}) (uuid {U(tag)}))'

def instance(c,lid,yp,hh,x,y,sch_uuid,tagbase):
    sym_uuid=U(tagbase+':sym')
    o=['(symbol',f' (lib_id "{lid}")',f' (at {x:.2f} {y:.2f} 0)',' (unit 1) (exclude_from_sim no) (in_bom yes) (on_board no)']
    if c.get('status')=='dnp': o.append(' (dnp yes)')
    o += [f' (uuid {sym_uuid})',f' (property "Reference" "{c["ref"]}" (at {x:.2f} {y-hh-3:.2f} 0) {eff()})',f' (property "Value" "{esc(c["part"])}" (at {x:.2f} {y+hh+3:.2f} 0) {eff(1.0)})',f' (property "Footprint" "" (at {x} {y} 0) {eff(hide=True)})',f' (property "Datasheet" "" (at {x} {y} 0) {eff(hide=True)})']
    for p in c['pins']: o.append(f' (pin "{esc(p["number"])}" (uuid {U(tagbase+":pin:"+p["number"])}))')
    o += [f' (instances (project "{PROJECT}" (path "/{sch_uuid}" (reference "{c["ref"]}") (unit 1))))',')']
    labs=[]
    for p in c['pins']:
        side=p.get('side','left'); px=x-12.70 if side=='left' else x+12.70; py=y+yp[id(p)]
        if p.get('net'): labs.append(label(p['net'],px,py,side,tagbase+':label:'+p['number']))
        elif p.get('status')=='nc' or c.get('status') in ('dnp','external'): labs.append(nc(px,py,tagbase+':nc:'+p['number']))
    if c.get('note'):
        labs.append(f'(text "{esc(c["ref"]+": "+c["note"])}" (at {x-16:.2f} {y+hh+8:.2f} 0) {eff(0.8)} (uuid {U(tagbase+":note")}))')
    return '\n'.join(o),labs

def layout_grid(comps, origin_x, origin_y, cols=4, dx=58, dy=45):
    positions=[]
    for i,c in enumerate(comps):
        col=i%cols; row=i//cols
        positions.append((c,origin_x+col*dx,origin_y+row*dy))
    return positions

def make_standalone(key,comps):
    sch_uuid=U('standalone:'+key)
    defs=[]; prepared=[]
    for c in comps:
        lid,ld,yp,hh=libdef(c); defs.append(ld); prepared.append((c,lid,yp,hh))
    cols=5 if key=='lighting' else 4
    dx=52 if key=='lighting' else 62
    dy=42
    pos=layout_grid(prepared,40,42,cols,dx,dy)
    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {sch_uuid})',' (paper "A3")',f' (title_block (title "USS Defiant - {key.title()}") (rev "2.0") (company "Model-Kit-Design"))',' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]; o += [' )',f' (text "GENERATED FROM ../eda/defiant-connectivity.xml" (at 20 20 0) {eff()} (uuid {U("standalone:"+key+":banner")}))']
    for d,x,y in pos:
        c,lid,yp,hh=d
        si,labs=instance(c,lid,yp,hh,x,y,sch_uuid,f'standalone:{key}:{c["ref"]}')
        o.append(' '+si.replace('\n','\n ')); o += [' '+q for q in labs]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    return '\n'.join(o)

def make_flat(comps):
    sch_uuid=U('flat-root')
    defs=[]; prep={}
    for c in comps:
        lid,ld,yp,hh=libdef(c); defs.append(ld); prep[c['ref']] = (c,lid,yp,hh)
    groups={k:[prep[c['ref']] for c in comps if c['sheet']==k] for k in ('power','controller','lighting','phasers','nfc')}
    regions={
        'power':(45,45,4,60,45),
        'controller':(330,45,2,78,55),
        'phasers':(520,45,4,58,45),
        'lighting':(45,280,7,52,42),
        'nfc':(520,280,4,62,45),
    }
    headers={'power':'POWER / CHARGING','controller':'CONTROLLER','phasers':'PHASERS','lighting':'ADDRESSABLE LIGHTING','nfc':'NFC'}
    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {sch_uuid})',' (paper "A1")',' (title_block (title "USS Defiant 1/1000 - Complete Electrical Connectivity") (rev "2.0") (company "Model-Kit-Design"))',' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]; o += [' )']
    o.append(f' (text "CANONICAL FLAT CONNECTIVITY - generated from ../eda/defiant-connectivity.xml" (at 20 20 0) {eff(1.2)} (uuid {U("flat:banner")}))')
    for key,items in groups.items():
        ox,oy,cols,dx,dy=regions[key]
        o.append(f' (text "{headers[key]}" (at {ox-10} {oy-15} 0) {eff(1.5)} (uuid {U("flat:header:"+key)}))')
        for d,x,y in layout_grid(items,ox,oy,cols,dx,dy):
            c,lid,yp,hh=d
            si,labs=instance(c,lid,yp,hh,x,y,sch_uuid,f'flat:{c["ref"]}')
            o.append(' '+si.replace('\n','\n ')); o += [' '+q for q in labs]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    return '\n'.join(o), sch_uuid

def main():
    comps=parse()
    # Canonical complete flat schematic: ERC and XML/netlist comparison run here.
    flat,root_uuid=make_flat(comps)
    (K/'USS-Defiant.kicad_sch').write_text(flat,encoding='utf-8')
    # Standalone subsystem views are exported for easier phone review.
    for key in ('power','controller','lighting','phasers','nfc'):
        (K/f'{key}.kicad_sch').write_text(make_standalone(key,[c for c in comps if c['sheet']==key]),encoding='utf-8')
    pro={'board':{},'boards':[],'erc':{'erc_exclusions':[],'meta':{'version':0},'rule_severities':{'duplicate_reference':'error','pin_not_connected':'error','multiple_net_names':'error','unannotated':'error'}},'libraries':{'pinned_footprint_libs':[],'pinned_symbol_libs':[]},'meta':{'filename':'USS-Defiant.kicad_pro','version':1},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.8,'via_drill':0.4,'wire_width':6,'bus_width':12,'schematic_color':'rgba(0, 0, 0, 0.000)','pcb_color':'rgba(0, 0, 0, 0.000)'}],'meta':{'version':3},'net_colors':None,'netclass_assignments':None,'netclass_patterns':[]},'schematic':{'annotate_start_num':0,'meta':{'version':1},'page_layout_descr_file':'','plot_directory':''},'sheets':[[root_uuid,'Root']],'text_variables':{}}
    (K/'USS-Defiant.kicad_pro').write_text(json.dumps(pro,indent=2),encoding='utf-8')
    print(f'Generated complete flat KiCad schematic with {len(comps)} components plus 5 standalone subsystem views in {K}')

if __name__=='__main__': main()
