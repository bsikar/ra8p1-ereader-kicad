#!/usr/bin/env python3
"""Check SERVICE-025 saved topology and conditional off-state envelope.

This does not qualify actual aggregate leakage, storage or mode sequencing.
Usage: python scripts/check_service_discharge.py <saved KiCad XML netlist>
"""
import math
import sys
import xml.etree.ElementTree as ET


def main():
    root = ET.parse(sys.argv[1]).getroot()
    comps = {c.attrib['ref']: c for c in root.findall('./components/comp')}
    pins = {}
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):
            pins[node.attrib['ref'], node.attrib['pin']] = net.attrib['name']
    for ref in ('R110', 'R111'):
        comp = comps[ref]
        fields = {f.attrib['name']: f.text for f in comp.findall('./fields/field')}
        assert comp.findtext('value') == '1k', ref
        assert fields['Manufacturer_Part_Number'] == 'RC0603FR-071KL', ref
        assert pins[ref, '1'].endswith('SERVICE_VIO'), ref
        assert pins[ref, '2'] == 'GND', ref
    rmin = 1000 * .99 * .99
    rmax = 1000 * 1.01 * 1.01
    injection = 60e-6  # Allocation, not a demonstrated circuit bound.
    ceiling = injection * rmax / 2
    single_open = injection * rmax
    assert ceiling < .1 and single_open < .1
    current = 3.465 / (rmin / 2)
    dissipation = 3.465 ** 2 / rmin
    assert current < .020
    assert dissipation < .1  # Rating at 70 C only; hot derating remains open.
    # Constant-injection RC screen, not guaranteed turn-off timing.
    time = rmax / 2 * 100e-9 * math.log((3.465-ceiling)/(.1-ceiling))
    print(f'SERVICE-025 conditional PASS: pair {rmin/2:.2f}..{rmax/2:.2f} ohm; '
          f'off {ceiling*1e3:.3f} mV; single-open {single_open*1e3:.3f} mV.')
    print(f'Fixture pair {current*1e3:.6f} mA; each {dissipation*1e3:.3f} mW; '
          f'nominal-C screen {time*1e6:.3f} us.')
    print('HOLD: actual leakage/storage, rail transitions, fixture budget, '
          'hot derating and physical recovery tests.')


if __name__ == '__main__':
    main()
