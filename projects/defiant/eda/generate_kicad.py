#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import json, uuid

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
K=ROOT/'kicad'; K.mkdir(exist_ok=True)
XML=BASE/'defiant-connectivity.xml'
PROJECT='USS-Defiant'

def U(): return str(uuid.uuid4())
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
    hh=max(5.08,(n-1)*1.27+2.54); hw=8.89
    name=f'{c["ref"]}_{c["part"].replace(" ","_").replace("/","_")[:24]}'
    lid='Defiant:'+name
    o=[f'(symbol "{lid}" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board no)',
       f' (property "Reference" "{c["ref"][0]}" (at 0 {hh+2.54:.2f} 0) {eff()})',
       f' (property "Value" "{esc(c["part"])}" (at 0 {-hh-2.54:.2f} 0) {eff(1.0)})',
       f' (property "Footprint" "" (at 0 0 0) {eff(hide=True)})',
       f' (property "Datasheet" "" (at 0 0 0) {eff(hide=True)})',
       f' (symbol "{name}_1_1" (rectangle (start {-hw} {hh:.2f}) (end {hw} {-hh:.2f}) (stroke (width 0.254) (type default)) (fill (type background)))']
    valid={'input','output','bidirectional','tri_state','passive','power_in','power_out','open_collector','open_emitter','no_connect','free'}
    for p in pins:
        side=p.get('side','left'); x=-11.43 if side=='left' else 11.43; ang=0 if side=='left' else 180
        typ=p.get('type','passive'); typ=typ if typ in valid else 'passive'
        o.append(f'  (pin {typ} line (at {x} {yp[id(p)]:.2f} {ang}) (length 2.54) (name "{esc(p["name"])}" {eff(1.0)}) (number "{esc(p["number"])}" {eff(1.0)}))')
    o+=[' ))']; return lid,'\n'.join(o),yp,hh

def label(net,x,y,side):
    ang=0 if side=='left' else 180
    return f'(label "{esc(net)}" (at {x:.2f} {y:.2f} {ang}) {eff(1.0)} (uuid {U()}))'
def nc(x,y): return f'(no_connect (at {x:.2f} {y:.2f}) (uuid {U()}))'

def instance(c,lid,yp,hh,x,y,path):
    o=['(symbol',f' (lib_id "{lid}")',f' (at {x:.2f} {y:.2f} 0)',' (unit 1) (exclude_from_sim no) (in_bom yes) (on_board no)']
    if c.get('status')=='dnp': o.append(' (dnp yes)')
    o += [f' (uuid {U()})',f' (property "Reference" "{c["ref"]}" (at {x:.2f} {y-hh-3:.2f} 0) {eff()})',f' (property "Value" "{esc(c["part"])}" (at {x:.2f} {y+hh+3:.2f} 0) {eff(1.0)})',f' (property "Footprint" "" (at {x} {y} 0) {eff(hide=True)})',f' (property "Datasheet" "" (at {x} {y} 0) {eff(hide=True)})']
    for p in c['pins']: o.append(f' (pin "{esc(p["number"])}" (uuid {U()}))')
    o += [f' (instances (project "{PROJECT}" (path "{path}" (reference "{c["ref"]}") (unit 1))))',')']
    labs=[]
    for p in c['pins']:
        side=p.get('side','left'); px=x-11.43 if side=='left' else x+11.43; py=y+yp[id(p)]
        if p.get('net'): labs.append(label(p['net'],px,py,side))
        elif p.get('status')=='nc' or c.get('status') in ('dnp','external'): labs.append(nc(px,py))
    if c.get('note'): labs.append(f'(text "{esc(c["ref"]+": "+c["note"])}" (at {x-15:.2f} {y+hh+8:.2f} 0) {eff(0.9)} (uuid {U()}))')
    return '\n'.join(o),labs

def make_child(key,comps,root_uuid,sheet_uuid,page):
    path=f'/{root_uuid}/{sheet_uuid}'
    defs=[]; data=[]
    for c in comps:
        lid,ld,yp,hh=libdef(c); defs.append(ld); data.append((c,lid,yp,hh))
    cols=4 if key=='lighting' else 3; xs=[45+60*i for i in range(cols)]; pos=[]; col=0; y=42
    for d in data:
        pos.append((*d,xs[col],y)); col+=1
        if col==cols: col=0; y+=48
    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {U()})',' (paper "A3")',f' (title_block (title "USS Defiant - {key.title()}") (rev "1.0") (company "Model-Kit-Design"))',' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]; o += [' )',f' (text "GENERATED FROM ../eda/defiant-connectivity.xml" (at 20 20 0) {eff()} (uuid {U()}))']
    for c,lid,yp,hh,x,y in pos:
        si,labs=instance(c,lid,yp,hh,x,y,path); o.append(' '+si.replace('\n','\n ')); o += [' '+q for q in labs]
    o += [f' (sheet_instances (path "{path}" (page "{page}")))',')']; return '\n'.join(o)

def main():
    comps=parse(); root_uuid=U()
    sheets={'power':('Power_Charging','power.kicad_sch',U(),'2'),'controller':('Controller','controller.kicad_sch',U(),'3'),'lighting':('Lighting','lighting.kicad_sch',U(),'4'),'phasers':('Phasers','phasers.kicad_sch',U(),'5'),'nfc':('NFC','nfc.kicad_sch',U(),'6')}
    for key,(name,fn,su,page) in sheets.items(): (K/fn).write_text(make_child(key,[c for c in comps if c['sheet']==key],root_uuid,su,page),encoding='utf-8')
    coords={'power':(35,45),'controller':(115,45),'lighting':(35,95),'phasers':(115,95),'nfc':(75,145)}
    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',f' (uuid {root_uuid})',' (paper "A3")',' (title_block (title "USS Defiant 1/1000 Electronics") (rev "1.0") (company "Model-Kit-Design"))',' (lib_symbols)']
    for key,(x,y) in coords.items():
        name,fn,su,page=sheets[key]; path=f'/{root_uuid}/{su}'
        o.append(f' (sheet (at {x} {y}) (size 55 28) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0)) (uuid {su}) (property "Sheetname" "{name}" (at {x} {y-1.5} 0) {eff()}) (property "Sheetfile" "{fn}" (at {x} {y+30} 0) {eff(1.0)}) (instances (project "{PROJECT}" (path "{path}" (page "{page}")))))')
    o += [f' (text "Generated from ../eda/defiant-connectivity.xml; run ERC before fabrication." (at 20 20 0) {eff()} (uuid {U()}))',' (sheet_instances (path "/" (page "1")))',')']
    (K/'USS-Defiant.kicad_sch').write_text('\n'.join(o),encoding='utf-8')
    pro={'board':{},'boards':[],'erc':{'erc_exclusions':[],'meta':{'version':0},'rule_severities':{'duplicate_reference':'error','pin_not_connected':'error','multiple_net_names':'error','unannotated':'error'}},'libraries':{'pinned_footprint_libs':[],'pinned_symbol_libs':[]},'meta':{'filename':'USS-Defiant.kicad_pro','version':1},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.8,'via_drill':0.4,'wire_width':6,'bus_width':12,'schematic_color':'rgba(0, 0, 0, 0.000)','pcb_color':'rgba(0, 0, 0, 0.000)'}],'meta':{'version':3},'net_colors':None,'netclass_assignments':None,'netclass_patterns':[]},'schematic':{'annotate_start_num':0,'meta':{'version':1},'page_layout_descr_file':'','plot_directory':''},'sheets':[[root_uuid,'Root']],'text_variables':{}}
    (K/'USS-Defiant.kicad_pro').write_text(json.dumps(pro,indent=2),encoding='utf-8')
    print('Generated KiCad project and 5 child sheets in',K)
if __name__=='__main__': main()
