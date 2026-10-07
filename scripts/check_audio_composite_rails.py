#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Unity composite command/rail and portable power screens; not qualification."""
from math import isclose, sqrt
from check_audio_stage1 import envelope, heat_stereo


def command_peak(resistance, balanced_vrms):
    # Two independently ballasted BTL legs: 0.22/4 = 0.055 ohm per leg.
    return balanced_vrms / sqrt(2) * (1 + .11 / resistance)


def main():
    print('OPA1656 SBOS901C p6: linear common-mode V- .. V+ - 2.25V.')
    print('Absolute input p4: V- - 0.5 .. V+ + 0.5V; not functional limits.')
    assert 15 > 12 + .5
    assert -12 <= -11 <= 12 - 2.25
    assert 11 > 12 - 2.25 and 11 < 12 + .5
    print('Historical +15V command at +/-12V is invalid electrical overstress.')
    print('Portable: R | capped BTL Vrms | command peak | minimum positive rail | +/-6V CM margin')
    for resistance in (16, 32, 50, 80, 150, 300, 600):
        voltage, power, current = envelope(resistance, 4, .25, .5)
        command = command_peak(resistance, voltage)
        rail_min = command + 2.25
        assert command < 6 - 2.25
        if resistance >= 32:
            assert command > 5 - 2.25
        print(f'{resistance:3} | {voltage:.6f} | {command:.6f} | {rail_min:.6f} | {6-rail_min:.6f}')
    print('Desktop: R | rails | target Vrms | command peak | positive CM margin')
    for resistance, rail in ((16, 10), (32, 12), (50, 14), (80, 14), (150, 14), (300, 14), (600, 14)):
        voltage, power, current = envelope(resistance, 16, sqrt(.5), 4)
        margin = rail - 2.25 - command_peak(resistance, voltage)
        assert margin > 0
        print(f'{resistance:3} | +/-{rail} | {voltage:.6f} | {command_peak(resistance,voltage):.6f} | {margin:.6f}')
    bias = 2 * 6 * (16*.0085 + 20*.0039)
    assert isclose(bias, 2.568)
    _, dc = heat_stereo(32, 4, 6)
    system = (dc + bias) / .9 + 3
    heat = system - 2 * 4**2 / 32
    runtime = (3.7 * 6 * .8) / system
    print(f'Full bank +/-6V typical idle {bias:.6f}W; 0.5W/ch32 ideal amp DC {dc:.6f}W.')
    print(f'90% conversion + 3W other loads: battery {system:.6f}W, heat {heat:.6f}W, 17.76Wh runtime {runtime:.6f}h.')
    print('No hot drive, droop, stability, current sharing or continuous thermal rating is proved.')


if __name__ == '__main__':
    main()
