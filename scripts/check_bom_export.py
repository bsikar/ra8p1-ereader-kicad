#!/usr/bin/env python3
"""Audit a native per-reference CSV export against a saved KiCad XML netlist.

This checks export fidelity, not component suitability, stock or qualification.
Generate the CSV in KiCad with Group symbols disabled; never repair it here.
"""

import argparse
import csv
from pathlib import Path
import xml.etree.ElementTree as ET


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('netlist', type=Path)
    parser.add_argument('--bom', type=Path,
                        default=Path(__file__).resolve().parents[1]
                        / 'exports/ereader_rev1_bom.csv')
    args = parser.parse_args()
    components = {}
    excluded = set()
    for comp in ET.parse(args.netlist).getroot().findall('./components/comp'):
        ref = comp.attrib['ref']
        properties = {p.attrib['name'] for p in comp.findall('property')}
        if 'exclude_from_bom' in properties:
            excluded.add(ref)
            continue
        fields = {f.attrib['name']: f.text or ''
                  for f in comp.findall('./fields/field')}
        fields.update({
            'Reference': ref, 'Qty': '1',
            'Value': comp.findtext('value', ''),
            'Footprint': comp.findtext('footprint', ''),
            'Datasheet': comp.findtext('datasheet', ''),
            'DNP': 'DNP' if 'dnp' in properties else '',
            'Exclude from BOM': '',
            'Exclude from Board': ('Excluded from board'
                                   if 'exclude_from_board' in properties else ''),
        })
        components[ref] = fields
    with args.bom.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        rows = list(reader)
    required = {'Reference', 'Qty', 'Value', 'Manufacturer_Part_Number',
                'Selection_Basis', 'Sourcing_Snapshot', 'Procurement_Status'}
    if not required.issubset(headers):
        raise ValueError(f'Missing BOM columns: {sorted(required - set(headers))}')
    seen = set()
    for row in rows:
        ref = row['Reference']
        if ref in seen or ref not in components:
            raise ValueError(f'Duplicate, grouped, excluded or unknown reference: {ref}')
        seen.add(ref)
        for column in headers:
            if row[column] != components[ref].get(column, ''):
                raise ValueError(f'{ref}: CSV {column!r} differs from saved netlist')
    if seen != components.keys():
        raise ValueError(f'Missing BOM references: {sorted(components.keys() - seen)}')
    print(f'BOM fidelity PASS: {len(rows)} references, {len(headers)} columns; '
          f'{len(excluded)} native BOM exclusions.')
    print('Component selection, live sourcing and electrical qualification remain separate.')


if __name__ == '__main__':
    main()
