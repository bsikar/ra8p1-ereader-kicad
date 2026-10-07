#!/usr/bin/env python3
"""Architecture-stage energy/input screens; assumptions, not hardware ratings."""
from math import isclose, pi, sqrt
from check_audio_stage1 import envelope, heat_stereo


def bank_screen():
    """Retained common-controller screen and revised separate-loop candidates."""
    bias_current = 16 * .0085 + 4 * .0039
    assert isclose(bias_current, .1516)
    print("Historical common-controller screen (sharing rejected): R | rails | idle W | heat W | input W")
    for resistance, rail, expected_input in ((16, 10, 34.574621),
                                             (32, 12, 31.982224),
                                             (50, 14, 31.478435)):
        voltage, power, peak = envelope(resistance, 16, sqrt(.5), 4)
        _, dc = heat_stereo(resistance, voltage, rail)
        bias = 2 * rail * bias_current
        device_heat = (dc + bias) / .9 + 3 - 2 * power
        input_charge = ((dc + bias) / .9 + 3 + 4.55 / .9) * 1.1
        assert isclose(input_charge, expected_input, abs_tol=1e-6)
        print(f"{resistance:3} | +/-{rail} | {bias:.4f} | {device_heat:.6f} | {input_charge:.6f}")
        if resistance == 16:
            print(f"15K rise screen: {15 / device_heat:.6f} K/W")
    print(f"+/-14V maximum-bias screening estimate: {28 * (16 * .012 + 4 * .005):.3f} W")
    # 4W/32 requires 8V peak per leg. +/-10V leaves only 2V headroom;
    # the buffer's relevant typical curves need more. Ballast/hot swing are open.
    assert isclose(sqrt(4 * 32) * sqrt(2) / 2, 8)
    print("32-ohm stretch investigates +/-12V; actual hot swing/sharing remain unqualified.")
    print("Own-output unity loops, 16 BUF + 16 loop cores + 4 upstream cores:")
    candidate_bias = 16*.0085 + 20*.0039
    assert isclose(candidate_bias, .214)
    for resistance, rail in ((16, 10), (32, 12), (50, 14)):
        voltage, power, peak = envelope(resistance, 16, sqrt(.5), 4)
        _, dc = heat_stereo(resistance, voltage, rail)
        bias = 2*rail*candidate_bias
        # Same ideal Class-B model as the earlier screen. Circulating-current
        # loss, dynamic loop power, resistor losses and exact rails are excluded.
        heat = (dc+bias)/.9 + 3 - 2*power
        required = ((dc+bias)/.9 + 3 + 4.55/.9)*1.1
        print(f"{resistance:3} | +/-{rail} | {bias:.4f} | {heat:.6f} | {required:.6f}")
    print(f"+/-14V separate-loop mixed maximum-bias screen: {28*(16*.012+20*.005):.3f} W")
    print("Upstream four cores are a provisional allocation; exact gain chain is open.")


def main():
    print("Stage 5 ideal screen, excludes bank bias and actual buffer headroom:")
    print("R | V | P/ch | rails | amp DC | rail average A | device heat | input incl 4.55W charge")
    for resistance in (16, 32, 50, 80, 150, 300, 600):
        voltage, power, peak = envelope(resistance, 16, sqrt(.5), 4)
        # Two rail ranges; choose higher only when the swing requires it.
        rail = 10 if voltage * sqrt(2) / 2 + 1.5 <= 10 else 14
        heat, dc = heat_stereo(resistance, voltage, rail)
        average = dc / (2 * rail)
        assert isclose(average, 4 * peak / pi)
        device_heat = dc / .9 + 3 - 2 * power
        input_charge = (dc / .9 + 3 + 4.55 / .9) * 1.10
        print(f"{resistance:3} | {voltage:.3f} | {power:.3f} | +/-{rail} | {dc:.3f} | {average:.3f} | {device_heat:.3f} | {input_charge:.3f}")
    assert 3.2 <= 5.5 < 15 < 20  # Existing TPS63806 input ceiling must be preserved.
    usable_wh = 3.7 * 6 * .8
    print(f"Existing pack energy assumption: {usable_wh:.2f} usable Wh")
    for label, power in (("local target", 1.65), ("streaming target", 2.0),
                         ("local miss", 2.2), ("streaming miss", 2.7)):
        print(f"{label}: {power:.2f} W -> {usable_wh / power:.2f} h")
    print(f"Low-rail 16-ohm stereo peak per rail: {2 * sqrt(.5):.3f} A")
    print(f"0.6V LDO drop / two rails at 0.9003A: {2 * .6 * 4 * sqrt(.5) / pi:.3f} W")
    print(f"1S 3.2V / 90% 6W portable bus: {6 / (.9 * 3.2):.3f} A")
    print(f"2S 6.4V / 90% same bus: {6 / (.9 * 6.4):.3f} A")
    bank_screen()


if __name__ == "__main__":
    main()
