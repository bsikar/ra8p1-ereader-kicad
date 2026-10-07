#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check pulse metrics against analytic steps; not amplifier qualification."""
import math

import numpy as np

from investigate_audio_composite_ac import transient_summary


def main():
    tau, step = 100e-9, 1e-9
    case = dict(stop_s=12e-6, delay_s=2e-6, rise_s=10e-9,
                width_s=5e-6, fall_s=10e-9, amplitude_v=1, load_ohm=32)
    time = np.arange(0, case['stop_s'] + step / 2, step)
    start = case['delay_s'] + case['rise_s']
    end = start + case['width_s'] + case['fall_s']
    expected = tau * math.log(1000)
    for sign in (1, -1):
        # Independent analytic one-pole step pair at start/end.
        rising = np.where(time >= start, -np.expm1(-np.maximum(time-start, 0)/tau), 0)
        falling = np.where(time >= end, -np.expm1(-np.maximum(time-end, 0)/tau), 0)
        output = sign * (rising - falling)
        signals = {'out': output, 'vbranch0#branch': output / 32}
        case['amplitude_v'] = sign
        result = transient_summary(case, time, signals, 1)
        assert result['overshoot_percent'] < 1e-6
        for field in ('settling_after_input_rise_s', 'recovery_after_input_fall_s'):
            assert abs(result[field] - expected) <= 2 * step, (field, result[field])
        signals['out'] = output + np.where(time >= end, sign * .1, 0)
        assert transient_summary(case, time, signals, 1)['recovery_after_input_fall_s'] is None
        try:
            transient_summary(case, time[:-1000], {k:v[:-1000] for k,v in signals.items()}, 1)
        except ValueError:
            pass
        else:
            raise AssertionError('Truncated waveform was accepted')
    print('Transient metric checks PASS: analytic settling, both signs, recovery failure, truncation.')
    print('No amplifier/model/bench qualification is inferred.')


if __name__ == '__main__':
    main()
