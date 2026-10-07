#!/usr/bin/env python3
"""Reproduce Stage 1 feasibility arithmetic; no device qualification or CAD edits.

Units: ohms, volts RMS differential, amperes peak, watts per channel.
Class-B model assumes four ideal output legs in a stereo BTL amplifier.
Rail/headroom, efficiency, battery and system-power values are assumptions.
"""

from math import isclose, log10, pi, sqrt


def require_close(actual, expected, label):
    if not isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-8):
        raise ValueError(f"{label}: {actual} != {expected}")


def load_point(resistance, voltage):
    if resistance <= 0 or voltage < 0:
        raise ValueError("Nonphysical load or voltage")
    return voltage**2 / resistance, sqrt(2) * voltage / resistance


def envelope(resistance, voltage_limit, peak_current_limit, continuous_power_limit):
    voltage = min(voltage_limit, peak_current_limit * resistance / sqrt(2),
                  sqrt(continuous_power_limit * resistance))
    power, current = load_point(resistance, voltage)
    return voltage, power, current


def heat_stereo(resistance, voltage, rail):
    # Each channel is two opposite-phase legs, each supplied by +/- rail.
    power, current = load_point(resistance, voltage)
    if voltage * sqrt(2) / 2 > rail:
        raise ValueError("Output exceeds ideal BTL rail swing")
    dc_per_channel = 4 * rail * current / pi
    return 2 * (dc_per_channel - power), 2 * dc_per_channel


def spl_point(sensitivity_db_v, resistance, equivalent_sine_spl):
    # Approximate electrical screen, not a broadband acoustic guarantee.
    voltage = 10 ** ((equivalent_sine_spl - sensitivity_db_v) / 20)
    power, current = load_point(resistance, voltage)
    return voltage, power, current


def main():
    require_close(load_point(32, 8)[0], 2, "2 W/32 ohm")
    require_close(load_point(32, sqrt(128))[1], 0.5, "4 W peak current")
    require_close(envelope(16, sqrt(128), sqrt(0.5), 4)[1], 4,
                  "Stretch low-load current limit")
    require_close(envelope(32, 16, sqrt(0.5), 4)[1], 4,
                  "High-Z voltage extension does not permit 8 W/32 ohm")
    require_close(envelope(sqrt(128) * 2, sqrt(128), sqrt(0.5), 4)[1], 4,
                  "Intermediate impedance remains power-limited")
    require_close(heat_stereo(32, sqrt(128), 10)[0], 16 * 10 / pi * 0.25 - 8,
                  "Independent ideal Class-B supply integral")
    print("Loads: R | 8 V: W, Apeak | 11.314 V: W, Apeak | stretch V, W | stereo heat W at +/-10 V")
    for resistance in (16, 32, 50, 80, 150, 300, 600):
        p8, i8 = load_point(resistance, 8)
        p4, i4 = load_point(resistance, sqrt(128))
        v, p, _ = envelope(resistance, sqrt(128), sqrt(0.5), 4)
        heat, dc = heat_stereo(resistance, v, 10)
        require_close(dc - heat, 2 * p, "Stereo energy conservation")
        print(f"{resistance:3} | {p8:.4f}, {i8:.4f} | {p4:.4f}, {i4:.4f} | {v:.4f}, {p:.4f} | {heat:.4f}")
    print("BTL minimum rail magnitude with assumed 1.5 V headroom per leg:")
    for v in (8, sqrt(128), 16):
        print(f"{v:.4f} Vrms: +/-{sqrt(2) * v / 2 + 1.5:.4f} V")
    print("Headphone voltage/power/peak current at equivalent-sine levels:")
    for name, sensitivity, resistance in (
        ("Susvara RAA screen", 93.2, 67.1),
        ("HD800S manufacturer", 102, 300),
        ("Stealth manufacturer", 90 - 10 * log10(0.001 * 23), 23),
        ("SE846 manufacturer", 114 - 10 * log10(0.001 * 9), 9),
    ):
        for level in (100, 105, 111):
            v, p, i = spl_point(sensitivity, resistance, level)
            print(f"{name}, {level} dB: {v:.4f} V, {p*1000:.4f} mW, {i:.4f} Apeak")
    heat, dc = heat_stereo(32, sqrt(128), 10)
    input_power = dc / 0.90 + 3
    print(f"Illustrative stereo 4 W/32: {dc:.4f} W amp DC; {input_power:.4f} W external before charging")
    print(f"Illustrative 5 Ah 3.7 V, 80% usable: {5*3.7*0.8:.2f} Wh; 8h ceiling {5*3.7*0.8/8:.3f} W")
    for energy in (20, 30):
        print(f"{energy} Wh nominal at 80% usable: local 10h {energy*.8/10:.2f} W, streaming 8h {energy*.8/8:.2f} W")
    heat16, dc16 = heat_stereo(16, 8, 10)
    for name, input_w, output_w in (("32 ohm", input_power, 8),
                                  ("16 ohm", dc16 / .9 + 3, 8)):
        device_heat = input_w - output_w
        print(f"{name}: input {input_w:.4f} W, device heat {device_heat:.4f} W, 15 K rise screen {15/device_heat:.4f} K/W")
    print(f"2 W -> 4 W headroom improvement: {10*log10(2):.4f} dB")
    print(f"Noise 1 uV at 50 mV: {20*log10(0.05/1e-6):.4f} dB SNR")


if __name__ == "__main__":
    main()
