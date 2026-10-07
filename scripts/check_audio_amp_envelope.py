#!/usr/bin/env python3
"""Stage 3 load, ideal BTL heat and noise calculations, not part qualification."""
from math import isclose, log10, pi, sqrt
from check_audio_stage1 import envelope, heat_stereo, load_point, spl_point


def close(actual, expected):
    if not isclose(actual, expected, rel_tol=1e-7, abs_tol=1e-9):
        raise ValueError(f"{actual} != {expected}")


def maximum_heat_point(resistance, available_voltage, rail):
    # Analytic maximum of ideal sinusoidal Class-B heat over allowed amplitudes.
    voltage = min(available_voltage, 4 * rail / pi / sqrt(2))
    return voltage, heat_stereo(resistance, voltage, rail)[0]


def main():
    close(envelope(32, 16, sqrt(.5), 4)[1], 4)
    close(envelope(16, 16, sqrt(.5), 4)[1], 4)
    close(envelope(50, 16, sqrt(.5), 4)[1], 4)
    close(envelope(600, 16, sqrt(.5), 4)[1], 256 / 600)
    print("Desktop screen: R | Vrms | W/ch | Apeak | stereo heat +/-14 V | maximum heat / Vrms")
    for resistance in (9, 14, 16, 32, 50, 80, 150, 300, 600):
        voltage, power, current = envelope(resistance, 16, sqrt(.5), 4)
        heat, dc = heat_stereo(resistance, voltage, 14)
        worst_v, worst_heat = maximum_heat_point(resistance, voltage, 14)
        close(dc - heat, 2 * power)
        # Independent numerical sweep must agree with the analytic maximum.
        sweep = max(heat_stereo(resistance, voltage * i / 2000, 14)[0]
                    for i in range(2001))
        if abs(worst_heat - sweep) > 1e-5:
            raise ValueError("Dissipation maximum does not match amplitude sweep")
        print(f"{resistance:3} | {voltage:.4f} | {power:.4f} | {current:.4f} | {heat:.4f} | {worst_heat:.4f} / {worst_v:.4f}")
    print("Headphone screens, equivalent sine SPL; not listening recommendations:")
    cases = (("HE-6 velour conservative measured L", 89.0, 43.3),
             ("Susvara Stage1 measured screen", 93.2, 67.1),
             ("HD800S manufacturer", 102, 300),
             ("LCD-5 original manufacturer", 90-10*log10(.001*14), 14),
             ("SE846 manufacturer", 114-10*log10(.001*9), 9))
    for name, sensitivity, resistance in cases:
        for level in (80, 100, 105, 111):
            v, p, i = spl_point(sensitivity, resistance, level)
            print(f"{name} / {level}: {v:.4f} Vrms, {p:.6f} W, {i:.4f} Apeak")
    close(spl_point(89, 43.3, 111)[1], 3.6602614144598484)
    print("Flat 2.8 nV/rtHz amplifier-only approximation over 20-20000 Hz:")
    for gain in (1, 2, 4):
        noise = 2.8e-9 * sqrt(19980) * sqrt(2) * gain
        print(f"Independent BTL legs / noise gain {gain}: {noise*1e6:.4f} uVrms; 50 mV SNR {20*log10(.05/noise):.3f} dB")
    print("Ideal current-limited BTL power/32 at 130 mApeak:", .130**2*32/2)
    print("4-leg idle at +/-14 V: 12 BUF634A wide-BW +4 OPA1656 cores:", 28*(12*.0085+4*.0039), "W typical")
    print("4-leg ADA4870 idle at +/-14 V using 32.5 mA assumption:", 4*28*.0325, "W")
    print("16 ohm 4 W ideal stereo heat +/-8 V:", heat_stereo(16, 8, 8)[0], "W")
    print("Illustrative rail fault 14 V /9 ohm /5 ms:", 14**2/9*.005, "J; relay/detector latency NOT qualified")
    print("Stage 3 arithmetic checks passed. No CAD or circuit qualification performed.")


if __name__ == "__main__":
    main()
