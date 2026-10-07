"""OPT4001 integration audit and conditional bus screen; no CAD writes.

TI SBOS993A Rev A; allocations and limitations in design/ambient_light.md.
"""

import argparse
import copy
import xml.etree.ElementTree as ET

from check_sensor_alternative import rise_time


def contacts(root):
    result = {}
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            key = (node.get('ref'), node.get('pin'))
            assert key not in result, f'Duplicate contact {key}'
            result[key] = net.get('name')
    return result


def component_record(component):
    """Ignore XML formatting whitespace, preserving all actual field content."""
    for element in component.iter():
        if element.text is not None and not element.text.strip():
            element.text = None
        if element.tail is not None and not element.tail.strip():
            element.tail = None
    return ET.tostring(component)


def pullup_identity_record(component):
    """Preserve everything except the explicitly replaced value/source fields."""
    component = copy.deepcopy(component)
    changed_fields = {'Datasheet', 'Description', 'DigiKey_Part_Number',
                      'DigiKey_URL', 'Manufacturer_Part_Number',
                      'Selection_Basis', 'Sourcing_Snapshot'}
    for name in ('value', 'datasheet', 'description'):
        component.find(name).text = '<replaced>'
    for field in component.findall('./fields/field'):
        if field.get('name') in changed_fields:
            field.text = '<replaced>'
    for prop in component.findall('property'):
        if prop.get('name') in changed_fields:
            prop.set('value', '<replaced>')
    return component_record(component)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', required=True)
    parser.add_argument('--baseline', help='299-component ALS checkpoint before pullup replacement')
    args = parser.parse_args()
    root = ET.parse(args.netlist).getroot()
    nets = contacts(root)
    expected = {
        ('U32', '1'): '+3V3_MCU', ('U32', '2'): 'GND',
        ('U32', '4'): 'GND', ('U32', '5'): '/SENS_SCL',
        ('U32', '8'): '/SENS_SDA', ('U32', '7'): 'Net-(U32-INT)',
        ('C124', '1'): '+3V3_MCU', ('C124', '2'): 'GND',
        ('R112', '1'): '+3V3_MCU', ('R112', '2'): 'Net-(U32-INT)',
    }
    for contact, name in expected.items():
        assert nets.get(contact) == name, f'Review {contact}: expected {name}'
    for pin in ('3', '6'):
        name = nets[('U32', pin)]
        assert name.startswith('unconnected-')
        assert list(nets.values()).count(name) == 1
    components = {c.get('ref'): c for c in root.findall('./components/comp')}
    for ref, value in (('U32', 'OPT4001DTSR'), ('C124', '100n'), ('R112', '10k')):
        assert components[ref].findtext('value') == value
    # Inventory the entire saved bus, so an added peripheral cannot silently
    # inherit this three-device planning envelope.
    for name, expected_contacts in {
        '/SENS_SCL': {('R102', '2'), ('U1', 'K13'), ('U26', '1'), ('U32', '5')},
        '/SENS_SDA': {('R103', '2'), ('U1', 'R16'), ('U26', '4'), ('U32', '8')},
    }.items():
        actual = {contact for contact, net in nets.items() if net == name}
        assert actual == expected_contacts, f'Bus inventory changed: {name}: {actual}'
    assert components['U26'].findtext('value') == 'LIS2DTW12TR'
    for ref in ('R102', 'R103'):
        assert components[ref].findtext('value') == '3.3k'
        assert components[ref].findtext("./fields/field[@name='Manufacturer_Part_Number']") == 'RC0603FR-073K3L'
        assert components[ref].findtext("./fields/field[@name='DigiKey_Part_Number']") == '311-3.30KHRCT-ND'
        assert nets[(ref, '1')] == '+3V3_MCU'
    if args.baseline:
        old_root = ET.parse(args.baseline).getroot()
        old_components = {c.get('ref'): c for c in old_root.findall('./components/comp')}
        assert len(old_components) == 299 and set(components) == set(old_components)
        changed = set()
        for ref, component in old_components.items():
            if component_record(component) != component_record(components[ref]):
                changed.add(ref)
                assert ref in {'R102', 'R103'}, f'Unexpected component change: {ref}'
                assert component.findtext('value') == '4.7k'
                assert pullup_identity_record(component) == pullup_identity_record(components[ref]), ref
        assert changed == {'R102', 'R103'}
        assert contacts(old_root) == nets, 'Pin-to-net inventory changed'
        print('All 297 other complete component records and all contacts preserved; only R102/R103 replaced')
    print('Saved U32/C124/R112 topology passes; circuit qualification remains open')

    vmin, vmax = 3.151819680, 3.393012496
    rmin = 3300 * .99 * .99 * .95
    rmax = 3300 * 1.01 * 1.01 * 1.05
    # Existing 60pF plus a provisional 10pF sensor/route reserve.
    # 3pF TI typical pin capacitance is NOT a guaranteed upper bound.
    # Extra 2uA leakage likewise is an allocation, not a full-temperature limit.
    capacitance, leakage = 70e-12, 17e-6
    rise = rise_time(rmax, capacitance, vmin, leakage)
    ceiling = capacitance * 300e-9 / rise
    high = vmin - rmax * leakage
    sink = vmax / rmin + leakage
    slack = 1 / 400e3 - (1.3e-6 + .6e-6 + rise + 300e-9)
    assert 1.6 < vmin < vmax < 3.6
    assert high > .7 * vmax and sink < 3e-3
    assert .32 < .3 * vmin
    fast = rise_time(rmin, 25e-12, vmax, -leakage)
    assert 20e-9 < fast <= rise < 300e-9 and slack > 0
    print(f'Installed 3.3k conditional rise: {fast*1e9:.6f}..{rise*1e9:.6f} ns')
    print(f'Conditional capacitance ceiling: {ceiling*1e12:.6f} pF')
    print(f'400kHz minimum-pulse period slack: {slack*1e9:.6f} ns; conditional only')
    print(f'Conditional bus high floor: {high:.9f} V; sink ceiling {sink*1e3:.6f} mA')
    # INT has no MCU input load in polling mode; evaluate hypothetical low draw.
    int_rmin = 10000 * .99 * .99
    print(f'INT-low pull-up draw ceiling: {vmax/int_rmin*1e3:.6f} mA')
    print(f'INT pull-up dissipation ceiling: {vmax**2/int_rmin*1e3:.6f} mW')
    historical_rise = rise_time(4700 * 1.01 * 1.01 * 1.05, capacitance, vmin, leakage)
    assert historical_rise > 300e-9
    print(f'Historical 4.7k expanded-bus rise: {historical_rise*1e9:.6f} ns; FAIL')
    print('Pull-up comparison, same conditional allocations (3.3k installed):')
    for nominal in (3900, 3300, 2700, 2200):
        candidate_min = nominal * .99 * .99 * .95
        candidate_max = nominal * 1.01 * 1.01 * 1.05
        slow = rise_time(candidate_max, capacitance, vmin, leakage)
        fast = rise_time(candidate_min, 25e-12, vmax, -leakage)
        candidate_sink = vmax / candidate_min + leakage
        candidate_slack = 1 / 400e3 - (1.3e-6 + .6e-6 + slow + 300e-9)
        assert 20e-9 < fast <= slow < 300e-9
        assert candidate_sink < 3e-3 and candidate_slack > 0
        print(f'{nominal} ohm: rise {fast*1e9:.3f}..{slow*1e9:.3f} ns; '
              f'sink {candidate_sink*1e3:.6f} mA; '
              f'period slack {candidate_slack*1e9:.3f} ns')
    print('No bus speed, leakage, power transient or installed passive is qualified.')


if __name__ == '__main__':
    main()
