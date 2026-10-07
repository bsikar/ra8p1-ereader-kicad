#!/usr/bin/env python3
"""Reproduce external-review transport and ideal stereo BTL power screens.

No hot-device, converter, protocol, noise or enclosure acceptance is implied.
"""
import math


def stereo_supply(rail, peak_current):
    # Four balanced legs; each draws rail*mean(abs(load current)).
    return 8 * rail * peak_current / math.pi


def main():
    print('Stereo PCM, 32-bit containers; +1 frame is a sizing floor only')
    for rate in (192000, 384000, 705600, 768000):
        average = rate * 8 / 8000
        packet_floor = (math.ceil(rate / 8000) + 1) * 8
        assert packet_floor <= 1024
        print(f'{rate} Hz: {average:.1f} B/microframe, '
              f'{packet_floor} B floor, BCLK {64*rate/1e6:.4f} MHz')
    assert 64 * 192000 <= 12.5e6 < 64 * 384000
    assert math.isclose(44100 * 512 * 2 / 8 / 8000, 705.6)
    assert 44100 * 256 / 16 == 705600  # DoP: 16 DSD bits/channel/frame.
    print('Proposed load points: ohms, W/ch, differential Vrms, peak A/ch')
    for load, power in ((16, 7.6), (32, 6.4), (64, 4.3), (300, 1), (600, .5)):
        voltage = math.sqrt(power * load)
        peak = math.sqrt(2 * power / load)
        assert math.isclose(voltage ** 2 / load, power)
        print(f'{load}: {power:.3f}, {voltage:.6f}, {peak:.6f}')
    print('16 ohm, 7.6 W/ch; rail, ideal output DC, bias allowance, amp heat, '
          'source with charging and margin (W)')
    peak = math.sqrt(2 * 7.6 / 16)
    for rail in (10, 12, 15, 18):
        dc = stereo_supply(rail, peak)
        # Independently integrate four leg rail currents over a sinusoidal cycle.
        n = 100000
        numeric = sum(4 * rail * abs(peak * math.sin(2*math.pi*(k+.5)/n))
                      for k in range(n)) / n
        assert math.isclose(numeric, dc, rel_tol=1e-8)
        # 32.5mA is an illustrative allocation extrapolated from ADI's table,
        # not a guaranteed bias at these rails or over temperature.
        idle = 4 * 2 * rail * .0325
        heat = dc + idle - 2 * 7.6
        source = (dc + idle + 5 + 10) / .9 * 1.2
        assert heat > 0
        print(f'+/-{rail} V: {dc:.6f}, {idle:.6f}, {heat:.6f}, {source:.6f}')
    assert stereo_supply(18, peak) > 2 * 7.6 / .55
    print('PASS conditional arithmetic; rail swing/SOA, full supply budget and '
          'thermal qualification remain open.')


if __name__ == '__main__':
    main()
