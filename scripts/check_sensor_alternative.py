"""LIS2DW12 integration screening; no CAD writes or acceptance claim.

Sources and conditional allocations: design/sensor_alternative.md.
"""

from math import log


def rise_time(resistance, capacitance, supply, leakage_sink):
    """30%-70% crossing time for a lumped RC with constant signed leakage.

    Positive leakage sinks current, negative leakage injects current.
    This conditional model does not qualify device leakage or PCB parasitics.
    """
    final_voltage = supply - resistance * leakage_sink
    assert final_voltage > 0.7 * supply
    return resistance * capacitance * log(
        (final_voltage - 0.3 * supply) / (final_voltage - 0.7 * supply)
    )


def main():
    vmin, vmax = 3.15182, 3.39301
    # Conservative independent-corner screen despite a proposed common rail.
    irq_high_margin = (vmin - 0.2) - 0.8 * vmax
    irq_low_margin = 0.2 * vmin - 0.2
    assert 1.62 < vmin < vmax < 3.6
    assert irq_high_margin > 0 and irq_low_margin > 0

    # SENS-011 shared-rail IIC0 candidate. No bus switch or second pullup.
    # 1% initial, 100ppm/K over 100K, and 5% service drift allocation.
    # Leakage and capacitance are acceptance allocations, not measured limits.
    pull_min = 4700 * 0.99 * 0.99 * 0.95
    pull_max = 4700 * 1.01 * 1.01 * 1.05
    bus_leak = 15e-6
    bus_c_min, bus_c_max = 25e-12, 60e-12
    rise_min = rise_time(pull_min, bus_c_min, vmin, -bus_leak)
    rise_max = rise_time(pull_max, bus_c_max, vmin, bus_leak)
    zero_leak_rise_max = log(7 / 3) * pull_max * bus_c_max
    assert rise_max > zero_leak_rise_max
    # Zero VOL bounds pullup current more conservatively than using 0.4V.
    sink_max = vmax / pull_min + bus_leak
    bus_high_min = vmin - pull_max * bus_leak
    assert sink_max < 3e-3  # no assumption of FMPE enhanced drive
    assert bus_high_min > 0.7 * vmax
    assert 0.4 < 0.3 * vmin
    assert 20e-9 < rise_min <= rise_max < 300e-9
    # Static two-lines-low draw, separate from the MEMS supply current.
    bus_low_current = 2 * vmax / pull_min

    # SENS-020: receiver timing envelope, not ICBRL/ICBRH register values.
    # ST DS11811 Rev9 Table7; Renesas Rev1.30 Table2.66 Fast mode, FMPE=0.
    # Both device thresholds refer to their shared supply. Signed leakage
    # envelopes require qualification over the complete rising transition.
    fast_period = 1 / 400e3
    scl_low_min, scl_high_min = 1.3e-6, 0.6e-6
    fall_max = 300e-9  # acceptance limit, not a demonstrated waveform
    fall_min_all_rails = 20e-9 * vmax / 5.5
    edge_period = scl_low_min + scl_high_min + rise_max + fall_max
    period_slack = fast_period - edge_period
    assert period_slack > 0
    assert fast_period / 2 < scl_low_min  # 50% at 400kHz is insufficient
    c_ceiling = bus_c_max * 300e-9 / rise_max
    # Worst NF=11/NFE=1 receiver coefficients in Table2.66.
    # To use ST's 600ns high and 100ns setup minima without additional
    # margin, IIC internal reference cycle must be <=50ns (>=20MHz).
    tiic_limit = min((scl_high_min - 300e-9) / 6, 100e-9 - 50e-9)
    assert 12 * tiic_limit + 600e-9 < fast_period
    assert 6 * tiic_limit + 300e-9 < scl_low_min
    assert tiic_limit + 300e-9 < 600e-9  # bus wakeup disabled

    # Existing SYS-007 allocations, not guaranteed installed limits.
    rmax = 22 * 1.01 * 1.01 / 2 + 0.2
    cmax = 1e-3
    hold_existing = 46.589403e-3
    source_stop = 10e-3
    below_threshold_hold = 10e-3
    target = 0.09  # Strictly below the ST 100mV threshold.
    # First prove the existing allocation is insufficient even with no backfeed.
    fall_no_injection = rmax * cmax * log(3.6 / target)
    needed_no_injection = source_stop + fall_no_injection + below_threshold_hold
    assert needed_no_injection > hold_existing

    # Screening alternative: add two 100uF reservoir capacitors (not placed).
    # Original effective-C factors and initial-voltage/charge allocations retained.
    # KEMET T491: 10uA per 100uF/10V part at 25C, x10 at 85C,
    # x1.25 endurance screen. Two added parts need 250uA, not 100uA.
    chold6_min = 6 * 100e-6 * 0.9**3
    ihold_revised = 1.942e-3 + 2 * 10e-6 * 10 * 1.25
    hold6 = (chold6_min * (3.013705831 - 2.7) - 1e-6) / ihold_revised
    # Preserve PWR-006's 1.5mA key-filter return allocation separately from
    # the new 1mA allowance for other backfeed. Neither is a measured bound.
    injection_alloc = 1.5e-3 + 1e-3
    floor = injection_alloc * rmax
    assert floor < target
    fall_injection = rmax * cmax * log((3.6 - floor) / (target - floor))
    required = source_stop + fall_injection + below_threshold_hold
    assert hold6 < required < 0.2

    # Native draft now has four 220uF/10V T491D227K010AT parts.
    # Remove the old bank leakage before adding the new bank and 100uA reserve.
    non_cap_control = 1.125e-3 - 500e-6
    bank_leakage = 4 * 22e-6 * 10 * 1.25
    control = non_cap_control + bank_leakage + 100e-6
    path_max = 102.24
    initial = 3.263705831 - max(0.250, control * path_max)
    bank_min = 4 * 220e-6 * 0.9**3
    bank_max = 4 * 220e-6 * 1.1**3
    hold220 = (bank_min * (initial - 2.7) - 1e-6) / (control + 817e-6)
    steady = 3.70 - 0.250 - control * path_max
    assert steady > 3.25
    recharge = path_max * bank_max * log(steady / (steady - 3.25))
    assert required < hold220 < 0.2
    assert recharge < 1.0

    # SENS-016: native C115 is EEE-FN1C100R, 10uF/16V aluminum.
    # Panasonic FN, 01-Sep-25: +/-20% initial at 20C/120Hz,
    # +/-10% after soldering and +/-30% after endurance at 20C.
    # Multiplying independent factors is an allocation screen, NOT a
    # manufacturer guarantee of combined service or temperature extremes.
    bulk_screen_min = 10e-6 * 0.8 * 0.9 * 0.7
    bulk_screen_max = 10e-6 * 1.2 * 1.1 * 1.3
    bulk_leak_20c = max(0.01 * 10 * 16, 3) * 1e-6
    assert vmax < 16 and bulk_screen_min > 0
    # Included within the existing 1mF total, never added outside that limit.
    other_main_c_allowance = cmax - bulk_screen_max
    assert other_main_c_allowance > 0

    print("LIS2DW12 native draft: conditional arithmetic, qualification open")
    print(f"C115 service-factor screen at 20C: {bulk_screen_min*1e6:.3f}..{bulk_screen_max*1e6:.3f} uF")
    print(f"C115 catalog leakage at 20C after 2min rated voltage: {bulk_leak_20c*1e6:.3f} uA")
    print(f"Other main-rail capacitance allowance: {other_main_c_allowance*1e6:.3f} uF")
    print(f"IRQ high margin: {irq_high_margin:.6f} V")
    print(f"IRQ low margin: {irq_low_margin:.6f} V")
    print(f"IIC pullup envelope: {pull_min:.6f}..{pull_max:.6f} ohm")
    print(f"IIC rise allocation: {rise_min*1e9:.6f}..{rise_max*1e9:.6f} ns")
    print(f"Historical zero-leakage rise ceiling: {zero_leak_rise_max*1e9:.6f} ns")
    print(f"Conditional capacitance ceiling for 300ns rise: {c_ceiling*1e12:.6f} pF")
    print(f"Required fall-time envelope over all rails: {fall_min_all_rails*1e9:.6f}..300 ns")
    print(f"400kHz period slack at minimum pulses / worst allocated edges: {period_slack*1e9:.6f} ns")
    print(f"IIC reference minimum for minimum ST pulses with worst filter: {1/tiic_limit/1e6:.6f} MHz")
    print("No peripheral divider/filter register configuration is qualified.")
    print(f"IIC sink ceiling: {sink_max*1e3:.6f} mA")
    print(f"IIC high floor: {bus_high_min:.6f} V")
    print(f"IIC both-low pullup current: {bus_low_current*1e3:.6f} mA")
    print(f"Existing hold allocation: {hold_existing * 1e3:.6f} ms")
    print(f"Needed without backfeed: {needed_no_injection * 1e3:.6f} ms; FAIL")
    print(f"Corrected six-capacitor hold screen: {hold6 * 1e3:.6f} ms; FAIL")
    print(f"Main-rail equilibrium at 2.5mA return/injection: {floor * 1e3:.6f} mV")
    print(f"Needed with 2.5mA return/injection: {required * 1e3:.6f} ms")
    print(f"Four 220uF bank leakage screen: {bank_leakage * 1e3:.6f} mA")
    print(f"Four 220uF control allocation: {control * 1e3:.6f} mA")
    print(f"Four 220uF hold screen: {hold220 * 1e3:.6f} ms")
    print(f"Conditional hold margin: {(hold220-required) * 1e3:.6f} ms")
    print(f"Recharge model steady voltage: {steady:.6f} V")
    print(f"Recharge model time to 3.25V: {recharge:.6f} s")


if __name__ == "__main__":
    main()
