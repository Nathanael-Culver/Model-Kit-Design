#!/usr/bin/env python3
"""Character-aware KiCad generation wrapper for the Defiant.

The semantic XML remains the hardware source of truth. This wrapper adds only
EDA presentation/ERC metadata:
- conservative text-aware layout and collision checks;
- automatic A4/A3/A2/A1/A0 page promotion;
- KiCad-only power-flow markers for supplies that pass through passive
  semiconductor pins, so ERC can understand the intended source path;
- passive classification of module/battery negative reference terminals to
  avoid falsely treating ground-return pins as competing power sources.
None of these adjustments changes electrical connectivity.
"""
import copy
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
# Presentation-layer page sizing.
# ---------------------------------------------------------------------------

def make_standalone_auto(key, comps):
    sch_uuid=g.U('standalone:'+key)
    defs=[]; prepared=[]
    for c in comps:
        lid,ld,yp,geom=g.libdef(c)
        defs.append(ld)
        prepared.append((c,lid,yp,geom))

    # Smallest usable standard sheet first. This improves phone readability and
    # avoids giving a single-controller page a huge mostly-empty A3 canvas.
    candidates=[
        ('A4',297.0,210.0),
        ('A3',420.0,297.0),
        ('A2',594.0,420.0),
        ('A1',841.0,594.0),
        ('A0',1189.0,841.0),
    ]
    last_error=None
    for paper,page_w,page_h in candidates:
        try:
            pos,_=g.pack_layout(prepared,page_w,page_h,start_y=38.0)
            g.assert_nonoverlap(pos)
            break
        except RuntimeError as exc:
            last_error=exc
    else:
        raise RuntimeError(f'No standard page fits {key}: {last_error}')

    o=['(kicad_sch',' (version 20250114)',' (generator "openai_model_kit_eda")',
       f' (uuid {sch_uuid})',f' (paper "{paper}")',
       f' (title_block (title "USS Defiant - {key.title()}") (rev "2.3") (company "Model-Kit-Design"))',
       ' (lib_symbols']
    o += ['  '+d.replace('\n','\n  ') for d in defs]
    o += [' )',
          f' (text "GENERATED FROM ../eda/defiant-connectivity.xml - CHARACTER-AWARE AUTOLAYOUT - {paper}" (at 20 20 0) {g.eff()} (uuid {g.U("standalone:"+key+":banner")}))']
    for d,x,y in pos:
        c,lid,yp,geom=d
        si,graphics=g.instance(c,lid,yp,geom,x,y,sch_uuid,f'standalone:{key}:{c["ref"]}')
        o.append(' '+si.replace('\n','\n '))
        o += [' '+q for q in graphics]
    o += [' (sheet_instances (path "/" (page "1")))',')']
    print(f'{key}: selected {paper}; {len(prepared)} displayed EDA components; collision check PASS')
    return '\n'.join(o)


g.make_standalone=make_standalone_auto

if __name__=='__main__':
    g.main()
