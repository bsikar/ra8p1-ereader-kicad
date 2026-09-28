#!/usr/bin/env python3
"""Read-only CMS-017/018 camera interface screens, not qualification.

Sources, electrical assumptions and exclusions: design/camera_timing_budget.md.
All rates are decimal MB/s; frame storage is binary MiB. No CAD files are read
or written. Blanking, arbitration, refresh and processing add further demand.
"""

from fractions import Fraction


CEU_MIN_PERIOD_NS = Fraction("11.5")  # RA8P1 DS Rev.1.30 Table 2.77, VCC >=2.7V
CEU_MAX_CLOCK_HZ = Fraction(1_000_000_000) / CEU_MIN_PERIOD_NS
BUS_BYTES_PER_CLOCK = 1  # selected 8-bit route


def dc_screen() -> None:
    """Compare documented voltage limits without scaling OV5640 outputs."""
    host_min, host_max = Fraction('3.151819680'), Fraction('3.393012496')
    # OV5640 Table 8-3 values at the documented 1.8V condition, 25pF load.
    # Not guaranteed ratios valid at arbitrary DOVDD or module supply.
    sensor_voh, sensor_vol = Fraction('1.62'), Fraction('0.18')
    host_vih = Fraction('0.8') * host_max
    host_vil = Fraction('0.2') * host_min
    direct_high = sensor_voh - host_vih
    direct_low = host_vil - sensor_vol
    assert direct_high < 0 < direct_low
    print('\nCMS-018: sensor 1.8V-condition DC screen; direct CEU wiring REJECTED')
    print(f'Host worst VIH/VIL: {float(host_vih):.9f}/{float(host_vil):.9f} V')
    print(f'Direct high/low margins: {float(direct_high):.9f}/{float(direct_low):.9f} V')

    # SN74AXC8T245 candidate only; no rail, package or circuit selected.
    camera_io = Fraction('1.8')
    translator_input_high = sensor_voh - Fraction('0.65') * camera_io
    translator_input_low = Fraction('0.35') * camera_io - sensor_vol
    # B supply follows the SAME main rail as receiver; <=100uA static load.
    translator_output_high = host_min - Fraction('0.1') - Fraction('0.8') * host_min
    translator_output_low = Fraction('0.2') * host_min - Fraction('0.1')
    assert min(translator_input_high, translator_input_low,
               translator_output_high, translator_output_low) > 0
    print(f'AXC input high/low margins at exactly 1.8V: '
          f'{float(translator_input_high):.6f}/{float(translator_input_low):.6f} V')
    print(f'AXC output high/low margins, same host rail, <=100uA: '
          f'{float(translator_output_high):.9f}/{float(translator_output_low):.9f} V')
    delay_spread = Fraction('5') - Fraction('0.5')
    print(f'AXC independent-path delay spread allocation: {float(delay_spread):.3f} ns')
    print(f'Sensor minimum setup/hold needed before other skew: '
          f'{float(Fraction(2) + delay_spread):.3f}/'
          f'{float(Fraction("3.5") + delay_spread):.3f} ns')
    print('Not qualified: actual camera I/O envelope, load/edges, skew, isolation and sequencing.')


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
    dc_screen()


if __name__ == "__main__":
    main()
