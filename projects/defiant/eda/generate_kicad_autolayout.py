#!/usr/bin/env python3
"""Run the Defiant KiCad generator with automatic subsystem page sizing.

The underlying generator computes conservative visual envelopes from pin-name,
pin-number, net-label, wire-ID, value, and symbol dimensions. This wrapper
selects the smallest KiCad page that fits those envelopes without collisions.
"""
import generate_kicad as g


def make_standalone_auto(key, comps):
    sch_uuid=g.U('standalone:'+key)
    defs=[]; prepared=[]
    for c in comps:
        lid,ld,yp,geom=g.libdef(c)
        defs.append(ld)
        prepared.append((c,lid,yp,geom))

    candidates=[
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
       f' (title_block (title "USS Defiant - {key.title()}") (rev "2.2") (company "Model-Kit-Design"))',
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
    print(f'{key}: selected {paper}; {len(prepared)} components; collision check PASS')
    return '\n'.join(o)


g.make_standalone=make_standalone_auto

if __name__=='__main__':
    g.main()
