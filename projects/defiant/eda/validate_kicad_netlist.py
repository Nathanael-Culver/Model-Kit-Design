#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'defiant-connectivity.xml'
if len(sys.argv) != 2:
    print('usage: validate_kicad_netlist.py <kicad-exported-netlist.xml>')
    raise SystemExit(2)
NETLIST=Path(sys.argv[1])

def norm_net(name):
    # KiCad's XML netlist prefixes local flat-sheet labels with '/'.
    # The semantic source stores the human net name without that hierarchy marker.
    return name[1:] if name.startswith('/') else name

src=ET.parse(SOURCE).getroot()
kicad=ET.parse(NETLIST).getroot()

source_components={c.attrib['ref']: c for c in src.find('components')}
active_refs={ref for ref,c in source_components.items() if c.attrib.get('status')=='active'}

kc_components={c.attrib['ref']: c for c in kicad.findall('./components/comp')}
missing=sorted(active_refs-set(kc_components))

kc_pin_net={}
for net in kicad.findall('./nets/net'):
    name=norm_net(net.attrib.get('name',''))
    for node in net.findall('node'):
        kc_pin_net[(node.attrib['ref'],node.attrib['pin'])]=name

errors=[]
if missing:
    errors.append('Active component(s) missing from KiCad netlist: '+', '.join(missing))

checked_pins=0
for ref in sorted(active_refs):
    c=source_components[ref]
    for p in c.findall('pin'):
        expected=p.attrib.get('net')
        if not expected or p.attrib.get('status')=='nc':
            continue
        checked_pins+=1
        actual=kc_pin_net.get((ref,p.attrib['number']))
        if actual is None:
            errors.append(f'{ref}:{p.attrib["number"]} {p.attrib["name"]} missing from KiCad nets; expected {expected}')
        elif actual != expected:
            errors.append(f'{ref}:{p.attrib["number"]} {p.attrib["name"]}: KiCad={actual}, source={expected}')

# This explicitly prevents the previous false-positive condition where KiCad
# parsed a hierarchy whose electrical pages were effectively empty.
if len(kc_components) < len(active_refs):
    errors.append(f'KiCad netlist contains only {len(kc_components)} components; source has {len(active_refs)} active components')
if checked_pins == 0 or len(kc_pin_net) == 0:
    errors.append('KiCad netlist contains no usable electrical pin/net connectivity')

if errors:
    print('FAIL: KiCad/source connectivity mismatch')
    for e in errors:
        print(' - '+e)
    raise SystemExit(1)

print(f'PASS: KiCad netlist contains {len(kc_components)} components and {len(kc_pin_net)} connected pins.')
print(f'PASS: {checked_pins} active source pin/net assignments exactly match KiCad export.')
