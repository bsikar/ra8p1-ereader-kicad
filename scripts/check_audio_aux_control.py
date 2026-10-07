"""Audit the audio auxiliary 5 V control/status interface; never writes CAD.

Checks the saved KiCad XML netlist for the exact AUDIO_AUX_REQ, AUDIO_AUX_PG,
permission and clamp partitions, then repeats the conditional DC screens
recorded in design/audio_auxiliary_5v.md. Passing does not qualify startup,
collapse, transient, hot-leakage or headphone-protection behavior.
"""

import argparse
from math import isclose
import xml.etree.ElementTree as ET

EXPECTED = {
    'AUDIO_AUX_REQ': {('U1', 'N5'), ('U37', '1'), ('R122', '1')},
    'AUDIO_AUX_PG': {('U1', 'A16'), ('U36', '2'), ('R118', '2')},
    'AUDIO_AUX_EN': {('U36', '14'), ('R117', '1'), ('R123', '2'), ('U38', '6')},
    'U37_Y': {('U37', '4'), ('R123', '1')},
    'Q5_DRAIN': {('Q5', '3'), ('R121', '2'), ('U37', '6')},
    'Q5_GATE': {('Q5', '1'), ('R119', '2'), ('R120', '2')},
    'U38_SENSE': {('U38', '1'), ('R124', '2'), ('R125', '1')},
    'U38_CT': {('U38', '5'), ('C143', '2')},
}
ON_NET = {
    'GND': {('U37', '3'), ('U37', '2'), ('R122', '2'), ('R117', '2'),
            ('U38', '2'), ('R125', '2'), ('C143', '1'), ('Q5', '2')},
    '+3V3_MCU': {('U37', '5'), ('R118', '1'), ('R121', '1'), ('R124', '1')},
    'SYS_AON': {('U38', '3'), ('U38', '4'), ('C142', '1'),
                ('U36', '12'), ('U36', '13')},
}


def check_netlist(path):
    nets = {}
    for net in ET.parse(path).getroot().findall('./nets/net'):
        members = frozenset((n.get('ref'), n.get('pin')) for n in net.findall('node'))
        nets[net.get('name')] = members
    by_node = {node: name for name, members in nets.items() for node in members}
    for label, members in EXPECTED.items():
        names = {by_node.get(node) for node in members}
        assert len(names) == 1 and None not in names, (label, names)
        name = names.pop()
        assert nets[name] == members, (label, name, sorted(nets[name]))
        print(f'{label}: {name} = {sorted(members)}')
    for name, members in ON_NET.items():
        assert members <= nets[name], (name, sorted(members - nets[name]))
    reset = next(n for n in nets if n.endswith('MCU_RESET_N'))
    assert not nets[reset] & {m for s in EXPECTED.values() for m in s}
    permit = nets[by_node[('R120', '1')]]
    assert permit == {('Q3', '3'), ('R68', '2'), ('R69', '2'),
                      ('U13', 'A1'), ('R120', '1')}, sorted(permit)
    print('Netlist partitions PASS; no AUDIO_AUX load on', reset)


def check_arithmetic():
    vmin, vmax = 3.151819680019, 3.393012496197   # conditional +3V3_MCU
    rmin, rmax = 10000*.99*.99, 10000*1.01*1.01   # RC0603FR, 1%, 100ppm x 100C
    # SN74LVC1G97 SCES416N table 6.5, linear between 3.0 V and 4.5 V rows.
    vtp_max = 1.87 + (vmax-3)/1.5*(2.74-1.87)
    vtm_min = 0.84 + (vmin-3)/1.5*(1.41-0.84)
    # RA8P1 R01DS0439EJ0130 table 2.7: other outputs, |IOH|=|IOL|=1 mA.
    req_load = vmax/rmin + 5e-6
    assert req_load < 1e-3
    req_high_margin = (vmin-0.5) - vtp_max
    req_low_margin = vtm_min - 0.5
    hiz = (1e-6 + 5e-6)*rmax             # |ITSI| + U37 II through R122
    # TPS63070 SLVSC58B EN: rising max 0.83 V, falling min 0.67 V, 0.2 uA.
    # TPS3890 SLVSD65A RESET: 0.25 V at 0.4 mA, 250 nA high-Z leakage.
    leak = 0.2e-6 + 0.25e-6
    corners = []
    for r117 in (rmin, rmax):
        for r123 in (rmin, rmax):
            par = r117*r123/(r117+r123)
            for sign in (-1, 1):
                corners.append((2.4*r117/(r117+r123) + sign*leak*par,
                                0.45*r117/(r117+r123) + sign*leak*par))
    en_high = min(c[0] for c in corners)
    en_low = max(c[1] for c in corners)
    clamp_sink = vmax/rmin + 0.2e-6
    # P904 status input: VIH/VIL 0.8/0.2 VCC; PG VOL 0.4 V at 1 mA.
    pg_high_margin = 0.2*vmin - (1e-6 + 0.2e-6)*rmax
    pg_low_margin = 0.2*vmin - 0.4
    results = {
        'VT+ max': (vtp_max, 2.097947248), 'VT- min': (vtm_min, 0.897691478),
        'REQ load A': (req_load, 0.000351190439),
        'REQ high margin': (req_high_margin, 0.553872432),
        'REQ low margin': (req_low_margin, 0.397691478),
        'Hi-Z IN1 V': (hiz, 0.061206),
        'EN high min': (en_high, 1.173753075), 'EN low max': (en_low, 0.231748875),
        'Clamp sink A': (clamp_sink, 0.000346390439),
        'PG high margin': (pg_high_margin, 0.618122736),
        'PG low margin': (pg_low_margin, 0.230363936),
    }
    for name, (actual, target) in results.items():
        assert isclose(actual, target, abs_tol=2e-9), (name, actual)
        print(f'{name}: {actual:.9f}')
    assert hiz < vtm_min and en_high > 0.83 and en_low < 0.67
    assert clamp_sink < 0.4e-3 and 0.25 < 0.67
    assert min(req_high_margin, req_low_margin, pg_high_margin, pg_low_margin) > 0
    print('Conditional DC screens PASS; transient and hot-leakage qualification open.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', help='saved KiCad XML netlist')
    args = parser.parse_args()
    if args.netlist:
        check_netlist(args.netlist)
    check_arithmetic()


if __name__ == '__main__':
    main()
