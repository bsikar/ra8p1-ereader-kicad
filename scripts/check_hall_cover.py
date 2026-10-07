"""Audit Hall cover integration and conditional margins; never writes CAD.

Authority and unresolved conditions: design/hall_cover.md, HALL-001.
"""

import argparse
import copy
import xml.etree.ElementTree as ET

from check_ambient_light import component_record, contacts


def partitions(root, excluded):
    """Compare connectivity without relying on generated net names/codes."""
    result = set()
    for net in root.findall('./nets/net'):
        members = frozenset((n.get('ref'), n.get('pin'))
                            for n in net.findall('node')
                            if (n.get('ref'), n.get('pin')) not in excluded
                            and n.get('ref') not in {'U33', 'C125'})
        if members:
            result.add(members)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', required=True)
    parser.add_argument('--baseline', help='299-component pre-Hall XML netlist')
    args = parser.parse_args()
    root = ET.parse(args.netlist).getroot()
    parts = {c.get('ref'): c for c in root.findall('./components/comp')}
    nets = contacts(root)
    expected = {('U33', '1'): '+3V3_MCU', ('U33', '3'): 'GND',
                ('U33', '2'): 'COVER_INT_N', ('U1', 'M12'): 'COVER_INT_N',
                ('C125', '1'): '+3V3_MCU', ('C125', '2'): 'GND'}
    for contact, name in expected.items():
        assert nets.get(contact) == name, f'{contact}: expected {name}'
    assert {p for p, name in nets.items() if name == 'COVER_INT_N'} == {
        ('U33', '2'), ('U1', 'M12')}
    assert parts['U33'].findtext('value') == 'DRV5032FADBZR'
    assert parts['C125'].findtext('value') == '220n'
    assert parts['U26'].findtext('value') == 'LIS2DTW12TR'
    # C125's sourcing replacement retains nominal value and topology;
    # require the exact updated ordering code, not a broadly similar MLCC.
    for ref, mpn, distributor, source_date in (
            ('U33', 'DRV5032FADBZR', '296-47765-1-ND', '2026-10-04'),
            ('C125', 'C1608X7R1H224K080AB', '445-7408-1-ND', '2026-10-05')):
        fields = {f.get('name'): f.text for f in parts[ref].findall('./fields/field')}
        assert fields['Manufacturer_Part_Number'] == mpn
        assert fields['DigiKey_Part_Number'] == distributor
        assert fields['Manufacturer_Name']
        assert 'HALL-001' in fields['Selection_Basis']
        assert fields['Sourcing_Snapshot'].startswith(source_date)
        assert 'Active' in fields['Sourcing_Snapshot']
    hall = root.find("./libparts/libpart[@lib='Sensors'][@part='DRV5032FADBZR']")
    assert hall is not None
    assert {(p.get('num'), p.get('type')) for p in hall.findall('./pins/pin')} == {
        ('1', 'power_in'), ('2', 'output'), ('3', 'power_in')}
    if args.baseline:
        old = ET.parse(args.baseline).getroot()
        old_parts = {c.get('ref'): c for c in old.findall('./components/comp')}
        assert len(old_parts) == 299 and len(parts) == 301
        assert set(parts) - set(old_parts) == {'U33', 'C125'}
        for ref, component in old_parts.items():
            assert component_record(copy.deepcopy(component)) == component_record(
                copy.deepcopy(parts[ref])), f'Unexpected existing part change: {ref}'
        assert contacts(old)[('U1', 'M12')].startswith('unconnected-')
        assert partitions(old, {('U1', 'M12')}) == partitions(root, {('U1', 'M12')})
        print('All 299 existing component records and other net partitions preserved')
    vmin, vmax = 3.151819680, 3.393012496
    assert 1.65 < vmin < vmax < 5.5
    high = vmin - .35 - .8 * vmax
    low = .2 * vmin - .3
    assert high > 0 and low > 0
    before_bias_aging = 220e-9 * .9 * .85
    required_retention = 100e-9 / before_bias_aging
    assert 0 < required_retention < 1
    print('Exact Hall pin map, part identities, cover net and local bypass pass')
    print(f'Conditional static margins: high {high:.9f} V; low {low:.9f} V')
    print(f'C125 before bias/aging: {before_bias_aging*1e9:.3f} nF; '
          f'required further retention {required_retention*100:.4f}%')
    print('Loading, sequencing, power, effective capacitance and magnet geometry remain open')


if __name__ == '__main__':
    main()
