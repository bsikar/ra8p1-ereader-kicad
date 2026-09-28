#!/usr/bin/env python3
"""Read-only CMS-017 camera bandwidth screen, not interface qualification.

Sources, electrical assumptions and exclusions: design/camera_timing_budget.md.
All rates are decimal MB/s; frame storage is binary MiB. No CAD files are read
or written. Blanking, arbitration, refresh and processing add further demand.
"""

from fractions import Fraction


CEU_MIN_PERIOD_NS = Fraction("11.5")  # RA8P1 DS Rev.1.30 Table 2.77, VCC >=2.7V
CEU_MAX_CLOCK_HZ = Fraction(1_000_000_000) / CEU_MIN_PERIOD_NS
BUS_BYTES_PER_CLOCK = 1  # selected 8-bit route


def main() -> None:
    print("CMS-017: necessary-condition screen; no mode is electrically qualified")
    print(f"CEU period-only ceiling: {float(CEU_MAX_CLOCK_HZ / 1_000_000):.6f} MHz")
    for clock_mhz in (24, 48, 96):
        period = Fraction(1000, clock_mhz)
        status = "within period limit only" if period >= CEU_MIN_PERIOD_NS else "REJECT"
        print(f"{clock_mhz} MHz: period {float(period):.6f} ns; {status}")

    print("\nUncompressed 16-bit/pixel payload on the 8-bit bus:")
    print("Mode             MB/s      Two frames MiB   48MHz payload-only   CEU ceiling")
    for name, width, height, fps in (
        ("VGA30", 640, 480, 30),
        ("720p30", 1280, 720, 30),
        ("1080p30", 1920, 1080, 30),
        ("5MP7.5", 2592, 1944, Fraction(15, 2)),
        ("5MP15", 2592, 1944, 15),
    ):
        frame_bytes = width * height * 2
        payload = frame_bytes * fps
        at_48 = "REJECT" if payload > 48_000_000 * BUS_BYTES_PER_CLOCK else "not excluded"
        at_limit = "REJECT" if payload > CEU_MAX_CLOCK_HZ * BUS_BYTES_PER_CLOCK else "not excluded"
        print(f"{name:12} {float(payload / 1_000_000):10.6f}"
              f" {2 * frame_bytes / 2**20:17.6f}   {at_48:18}   {at_limit}")

    print("\nExcluded overhead: blanking, bus stalls/refresh, copies, processing,")
    print("MIPI traffic, display/audio/radio/storage. JPEG size is not bounded here.")
    print("PCLKA/jitter, sensor timing, DC levels and power sequencing remain open.")


if __name__ == "__main__":
    main()
