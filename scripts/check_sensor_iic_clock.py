"""Conditional RA8P1 IIC divider screen; not an accepted clock plan.

Authority: R01UH1064EJ0130 Rev1.30, pp2384, 2386, 2402-2403.
The provisional PCLKB range must be established by the system clock design.
"""

from check_sensor_alternative import rise_time


def main():
    pclkb_min, pclkb_max = 49.5e6, 50.5e6
    cks, nf, brh, brl = 1, 2, 23, 31
    assert 0 <= brh <= 31 and 0 <= brl <= 31
    assert min(brh, brl) >= nf + 1
    phi_min, phi_max = pclkb_min / 2**cks, pclkb_max / 2**cks
    # HUM equation (5): SCLE=1, NFE=1, CKS != 000.
    high_cycles, low_cycles = brh + 2 + nf, brl + 2 + nf
    high_min, low_min = high_cycles / phi_max, low_cycles / phi_max
    assert high_min >= .6e-6 and low_min >= 1.3e-6
    rmin, rmax = 3300 * .99 * .99 * .95, 3300 * 1.01 * 1.01 * 1.05
    rise_min = rise_time(rmin, 25e-12, 3.393012496, -17e-6)
    rise_max = rise_time(rmax, 70e-12, 3.151819680, 17e-6)
    # Zero fall time deliberately screens the highest possible clock rate.
    # It is not an assertion that a zero fall time is permitted electrically.
    rate_max = 1 / (high_min + low_min + rise_min)
    rate_min = 1 / ((high_cycles + low_cycles) / phi_min + rise_max + 300e-9)
    assert rate_max <= 400e3
    # Compare the manufacturer's illustrative 400kbps tuple at the same
    # provisional corners: an example is not a whole-bus acceptance proof.
    example_rate = 1 / ((11 + 2 + nf + 29 + 2 + nf) / phi_max + rise_min)
    assert example_rate > 400e3
    print(f'Candidate ICBRH=0x{0xe0 | brh:02X}, ICBRL=0x{0xe0 | brl:02X}; CKS=001, NF=01')
    print(f'Conditional SCL high >= {high_min*1e6:.6f}us; low >= {low_min*1e6:.6f}us')
    print(f'Conditional unstretched rate {rate_min/1e3:.6f}..{rate_max/1e3:.6f}kHz')
    print(f'HUM illustrative 400kbps tuple reaches {example_rate/1e3:.6f}kHz at allocated fast corner')
    print('PCLKB synthesis, device setup/hold, edge limits and recovery remain unqualified.')


if __name__ == '__main__':
    main()
