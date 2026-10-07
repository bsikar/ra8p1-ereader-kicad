#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Brighton Sikarskie
"""Linear offset/ballast screens; not a BUF634A hot-device guarantee."""
from itertools import product
from math import isclose, sqrt
from check_audio_stage1 import envelope


def branch_currents(offsets, resistances, load_current):
    if len(offsets) != len(resistances) or not offsets:
        raise ValueError("One positive resistance per branch is required")
    if any(r <= 0 for r in resistances):
        raise ValueError("Branch resistances must be positive")
    # KCL for Thevenin sources with a common drive term omitted: it cancels.
    node = (sum(e / r for e, r in zip(offsets, resistances)) - load_current)
    node /= sum(1 / r for r in resistances)
    currents = tuple((e - node) / r for e, r in zip(offsets, resistances))
    if not isclose(sum(currents), load_current, abs_tol=1e-12):
        raise ValueError("Branch currents violate KCL")
    return currents


def check_close(actual, expected):
    if not isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError(f"{actual} != {expected}")


def corner_peak(ballast, output_resistance, tolerance=.01):
    peak = 0.0
    # 16 offset corners x 16 external resistor corners x 3 load states.
    # Rout is an assumed equal linear resistance, not a tolerance guarantee.
    for offsets in product((-.065, .065), repeat=4):
        for signs in product((-1, 1), repeat=4):
            resistances = tuple(output_resistance + ballast * (1+tolerance*s)
                                for s in signs)
            for load in (-sqrt(.5), 0, sqrt(.5)):
                peak = max(peak, *(abs(i) for i in
                           branch_currents(offsets, resistances, load)))
    return peak


def closed_branch_peak(count, load_peak, leg_peak, dc_budget, element_error,
                       feedback_total=1000, ballast=.22, tolerance=.01):
    """Conditional voltage-loop screen, not a dynamic or guaranteed device model.

    Each branch senses its own buffer output BEFORE its ballast. For gain 2,
    RF/RG=(1+error)/(1-error); element_error is per element about the array
    medial axis, NOT a resistor-ratio tolerance. Zero feedback_total denotes
    a unity follower with no gain-divider output current or ratio mismatch.
    """
    peak = circulation = 0.0
    states = tuple(product((-1, 1), repeat=3))  # DC, ratio, ballast signs
    for corners in product(states, repeat=count):
        resistances = tuple(ballast*(1+tolerance*s[2]) for s in corners)
        for load_sign in (-1, 0, 1):
            signal = load_sign*leg_peak
            sources = tuple(s[0]*dc_budget + signal*(
                (1+(1+s[1]*element_error)/(1-s[1]*element_error))/2
                if feedback_total else 1) for s in corners)
            currents = branch_currents(sources, resistances, load_sign*load_peak)
            # Conservative triangle bound: gain-divider load plus load sharing.
            feedback = tuple(abs(v)/feedback_total if feedback_total else 0
                             for v in sources)
            worst = max(abs(i)+f for i, f in zip(currents, feedback))
            peak = max(peak, worst)
            if load_sign == 0:
                circulation = max(circulation, worst)
    return peak, circulation


def closed_loop_screens():
    # Illustrative 100K element temperature change. The DC allocation includes
    # offset/drift and reserves margin for unqualified bias/PSRR/finite-loop gain.
    dc_budget = .003
    fresh_error = .0005 + 5e-6*100
    aged_error = fresh_error + .00125  # 8000h STANDARD relative drift, per element
    print("Conditional own-output loops: R | P/ch | G2 fresh A | G2 aged A | unity A")
    for resistance in (16, 32, 50, 80, 150, 300, 600):
        voltage, power, load = envelope(resistance, 16, sqrt(.5), 4)
        leg = voltage*sqrt(2)/2 + load*.22/4
        fresh, _ = closed_branch_peak(4, load, leg, dc_budget, fresh_error)
        aged, _ = closed_branch_peak(4, load, leg, dc_budget, aged_error)
        unity, circulating = closed_branch_peak(4, load, leg, dc_budget, 0, 0)
        print(f"{resistance:3} | {power:.6f} | {fresh:.9f} | {aged:.9f} | {unity:.9f}")
        assert unity < .250  # Conditional typical-current comparison, not qualification.
        if resistance == 16:
            assert aged > .250
            assert isclose(circulating, .0045/(.22*.99), abs_tol=1e-12)
            # Independent analytic corner: positive-offset branch at low R,
            # other three negative-offset branches at high R, positive load.
            r_low, r_high = .22*.99, .22*1.01
            analytic = (load + 3*(2*dc_budget)/r_high)/(1+3*r_low/r_high)
            check_close(unity, analytic)
    floor_load = sqrt(2*2/32)
    floor_leg = sqrt(2*2*32)/2 + floor_load*.22/4
    floor, _ = closed_branch_peak(4, floor_load, floor_leg, dc_budget, aged_error)
    print(f"2W/32 aged gain-2 branch screen: {floor:.9f} A")
    failed_open, _ = closed_branch_peak(3, sqrt(.5), 8, dc_budget, 0, 0)
    assert failed_open > .250
    print(f"One of four branches open, unity full low-load envelope: {failed_open:.9f} A")
    print("4096 DC/gain/ballast corners x 3 load states per four-branch case.")
    print("Unity means no external ratio mismatch; AC loop mismatch is unmodeled.")
    print("The low-load unity result is effectively 200mA; no extra margin is implied.")


def main():
    # Independent elementary circuit cases validate the KCL solver.
    check_close(branch_currents((0, 0), (1, 3), 1)[0], .75)
    check_close(branch_currents((.1, -.1), (2, 2), 0)[0], .05)
    for i in branch_currents((.02,)*4, (.22,)*4, .4):
        check_close(i, .1)
    load = sqrt(.5)
    ideal = load/4
    spread = .065 - (.065-3*.065)/4
    check_close(spread, .0975)
    for resistance in (.22, 5.22, 7.22):
        actual = branch_currents((.065, -.065, -.065, -.065),
                                 (resistance,)*4, load)
        check_close(actual[0], ideal+spread/resistance)
    check_close(branch_currents((.065, -.065, -.065, -.065),
                               (.22,)*4, 0)[0], .0975/.22)
    print(f"Load peak {load:.9f} A; ideal branch {ideal:.9f} A")
    print("Screen | nominal worst branch A | 1% ballast corner worst A")
    for label, rout in (("ballast-only sensitivity bound", 0),
                        ("5 ohm typical DC Rout approximation", 5),
                        ("7 ohm typical DC Rout approximation", 7)):
        nominal = ideal+spread/(rout+.22)
        print(f"{label} | {nominal:.9f} | {corner_peak(.22, rout):.9f}")
    required = spread/(.250-ideal)
    allowance = spread/(.25*ideal)
    print(f"Total equal branch resistance for 250mA screen: {required:.9f} ohm")
    print(f"Total equal branch resistance for 25% sharing screen: {allowance:.9f} ohm")
    print(f"Ballast-only BTL series contribution (before feedback): {2*required/4:.9f} ohm")
    check_close(corner_peak(.22, 0, 0), ideal+spread/.22)
    if corner_peak(.22, 0) <= .250:
        raise ValueError("Expected ballast-only counterexample was lost")
    print("768 corners per screen checked. Hot sharing, dynamic Rout/gain,")
    print("current limits, compensation and real-device behavior remain unqualified.")
    closed_loop_screens()


if __name__ == "__main__":
    main()
