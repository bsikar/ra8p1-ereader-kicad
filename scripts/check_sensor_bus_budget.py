"""Read-only SENS-003 candidate calculations; not schematic acceptance.

Inputs and outstanding conditions are recorded in design/sensors.md.
Run with Python 3; no external packages or CAD writes.
"""

from math import log


def main():
    v_min, v_max = 3.15182, 3.39301  # conditional main-rail design envelope
    r_nom = 2400.0  # candidate: one pullup on each side of each bus switch
    r_min = r_nom * 0.99 * 0.99  # 1% initial, 100ppm/K over 100K assumption
    r_max = r_nom * 1.01 * 1.01
    ron_max = 4.5
    leakage = 15.05e-6  # ADXL 10uA + host 5uA + switch 50nA screening budget
    r_parallel_min, r_parallel_max = r_min / 2, r_max / 2
    sink = (v_max - 0.4) / r_parallel_min + leakage
    low_remote = 0.4 + sink * ron_max
    high_min = v_min - leakage * (r_parallel_max + ron_max)
    rise_min = log(7 / 3) * r_parallel_min * 25e-12
    rise_max = log(7 / 3) * (r_parallel_max + ron_max) * 100e-12
    c_min = 20e-9 / (log(7 / 3) * r_parallel_min)
    c_max = 120e-9 / (log(7 / 3) * (r_parallel_max + ron_max))
    # Even a modest branch-to-branch supply mismatch can source current into
    # the lower rail through two pullups. Include this in regulator review.
    rail_cross_current = (v_max - v_min) / (2 * r_min)
    # Illustrative off-state discharge target, not a selected resistor/switch.
    # Use the full-temperature powered-off bound, not the 25C 10nA row.
    injection = 3 * 2e-6
    discharge_r_max = 1000.0
    equilibrium = injection * discharge_r_max
    discharge_c_max = 1e-6
    to_50mv = discharge_r_max * discharge_c_max * log(
        (v_max - equilibrium) / (0.05 - equilibrium)
    )
    assert sink < 3e-3 and low_remote < 0.3 * v_min
    assert high_min > 0.7 * v_max
    assert 20e-9 <= rise_min <= rise_max <= 120e-9
    assert equilibrium < 0.05
    # The two pullups bridge unequal rails when the bilateral switch is on.
    # ADXL367 Table 5 permits no positive margin above VDDIO on digital pins.
    # Zero leakage and equal nominal pullups are a valid counterexample.
    mixed_high = (v_max + v_min) / 2
    assert mixed_high > v_min
    print("SENS-003 arithmetic reproduced; dual-domain pullups REJECTED")
    print(f"Counterexample: bus {mixed_high:.6f} V > sensor VDDIO {v_min:.6f} V")
    for label, value, unit in [
        ("each pullup minimum", r_min, "ohm"),
        ("each pullup maximum", r_max, "ohm"),
        ("total sink screen", sink * 1e3, "mA"),
        ("remote low ceiling", low_remote, "V"),
        ("high floor", high_min, "V"),
        ("25pF minimum rise", rise_min * 1e9, "ns"),
        ("100pF maximum rise", rise_max * 1e9, "ns"),
        ("screened capacitance lower bound", c_min * 1e12, "pF"),
        ("screened capacitance upper bound", c_max * 1e12, "pF"),
        ("rail cross-current ceiling", rail_cross_current * 1e6, "uA"),
        ("illustrative off-state equilibrium", equilibrium * 1e3, "mV"),
        ("illustrative discharge to 50mV", to_50mv * 1e3, "ms"),
        ("discharge plus required hold", to_50mv * 1e3 + 300, "ms"),
    ]:
        print(f"{label}: {value:.6f} {unit}")

    # Revised candidate: one 2.4k pullup per line, both on sensor VDDIO.
    # No host-domain pullups are permitted across the enabled pass switch.
    single_rise_min = log(7 / 3) * r_min * 25e-12
    single_rise_max = log(7 / 3) * (r_max + ron_max) * 50e-12
    assert 20e-9 < single_rise_min < single_rise_max < 120e-9
    print("Single-domain pullup candidate, 25..50pF:",
          f"{single_rise_min*1e9:.6f}..{single_rise_max*1e9:.6f} ns")

    # External RC ramp screen: all capacitance bounds below are acceptance
    # allocations, not guaranteed product limits inferred from nominal data.
    ramp_r_min, ramp_r_max = 91 * 0.99 * 0.99, 91 * 1.01 * 1.01
    ramp_c_min, ramp_c_max = 30e-6, 70e-6
    # Historical unloaded calculation only: this targets 90% of the input,
    # not 90% of the lower loaded sensor voltage. Do not use it as acceptance.
    ramp_min = ramp_r_min * ramp_c_min * log((v_max - 0.05) / (0.1*v_max))
    # 1mA non-bus allocation; both pullups held low indefinitely, VOL=0
    # maximizes load. This is a hypothetical DC model, not ADXL max current.
    rail_loaded = (v_min - ramp_r_max*1e-3) / (1 + 2*ramp_r_max/r_min)
    irq_high = 0.9 * rail_loaded
    host_gpio_high = 0.8 * v_max
    assert irq_high < host_gpio_high  # reveals need for IRQ translation
    print(f"Historical unloaded 90%-input charge: {ramp_min*1e3:.6f} ms (not acceptance)")
    print(f"Loaded sensor rail screen: {rail_loaded:.6f} V")
    print(f"Direct IRQ high screen REJECTED: {irq_high:.6f} < {host_gpio_high:.6f} V")
    print(f"Historical RC allocation (superseded below): {ramp_c_min*1e6:.0f}..{ramp_c_max*1e6:.0f} uF")

    # SENS-007 passive bleeder. The 5% lifetime drift and 8uA injection
    # bounds are circuit acceptance allocations, not claims of qualification.
    bleed_min = 4700 * 0.99 * 0.99 * 0.95
    bleed_max = 4700 * 1.01 * 1.01 * 1.05
    injection_max = 8e-6
    off_floor = injection_max * bleed_max
    assert off_floor < 0.05
    discharge_time = bleed_max * ramp_c_max * log(
        (v_max - off_floor) / (0.05 - off_floor)
    )
    hold_time = 0.300
    restart_delay = 3.0
    assert discharge_time + hold_time < restart_delay
    # Include bleeder load in the hypothetical 91ohm feed calculation.
    loaded_with_bleed = (v_min - ramp_r_max * 1e-3) / (
        1 + ramp_r_max * (2 / r_min + 1 / bleed_min)
    )
    bus_high = loaded_with_bleed - leakage * (r_max + ron_max)
    assert bus_high > 0.7 * v_max
    print("Passive 4.7k bleeder screen (conditional, not restart acceptance):")
    print(f"  resistance envelope: {bleed_min:.6f}..{bleed_max:.6f} ohm")
    print(f"  off-state equilibrium at 8uA: {off_floor*1e3:.6f} mV")
    print(f"  discharge to 50mV: {discharge_time:.6f} s")
    print(f"  discharge plus 300ms hold: {discharge_time+hold_time:.6f} s")
    print(f"  candidate restart delay: {restart_delay:.1f} s")
    print(f"  maximum on-state bleeder current: {v_max/bleed_min*1e3:.6f} mA")
    print(f"  maximum resistor dissipation: {v_max**2/bleed_min*1e3:.6f} mW")
    print(f"  loaded supply with bleeder: {loaded_with_bleed:.6f} V")
    print(f"  IIC high floor with bleeder: {bus_high:.6f} V")

    # SENS-008: compare the fastest no-load envelope with the lowest allowed
    # 90%-of-sensor-rail target. Ignoring the always-present bleeder here
    # accelerates the model and is conservative for a minimum-rise bound.
    # Vsource <= v_max, Vinitial <= 50mV, and no positive current injection.
    target = 0.9 * loaded_with_bleed
    charge_factor = ramp_r_min * log((v_max - 0.05) / (v_max - target))
    old_loaded_bound = charge_factor * ramp_c_min
    required_c = 4e-3 / charge_factor
    revised_c_min = 40e-6
    revised_loaded_bound = charge_factor * revised_c_min
    assert old_loaded_bound < 4e-3 < revised_loaded_bound
    assert revised_c_min <= ramp_c_max
    print("Loaded-rail ramp review (conditional on stated voltage/current envelopes):")
    print(f"  90% sensor target floor: {target:.6f} V")
    print(f"  old 30uF lower bound: {old_loaded_bound*1e3:.6f} ms; insufficient proof")
    print(f"  minimum capacitance for 4ms lower bound: {required_c*1e6:.6f} uF")
    print(f"  revised 40uF lower bound: {revised_loaded_bound*1e3:.6f} ms")
    print("  revised effective capacitance allocation: 40..70uF; no part qualified")


if __name__ == "__main__":
    main()
