#!/usr/bin/env python3
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parent
xml=BASE/'defiant-connectivity.xml'; xsd=BASE/'defiant-connectivity.xsd'
doc=etree.parse(str(xml)); etree.XMLSchema(etree.parse(str(xsd))).assertValid(doc)
root=ET.parse(xml).getroot(); errors=[]; refs=set()
for c in root.find('components'):
    ref=c.attrib['ref']
    if ref in refs: errors.append('duplicate reference '+ref)
    refs.add(ref); nums=set()
    for p in c.findall('pin'):
        if p.attrib['number'] in nums: errors.append(f'duplicate pin {ref}:{p.attrib["number"]}')
        nums.add(p.attrib['number'])
        if c.attrib.get('status')=='active' and p.attrib.get('status')=='active' and not p.attrib.get('net'):
            errors.append(f'active pin without net {ref}:{p.attrib["number"]}')
if errors:
    print('FAIL'); print('\n'.join(errors)); raise SystemExit(1)
print(f'PASS: XML schema valid; {len(refs)} component records; semantic pin checks passed.')
