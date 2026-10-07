"""LIS2DTW12 conditional interface screen; no CAD or qualification claim.

ST DS12825 Rev4 Tables 4/7; allocations in design/sensor_alternative.md.
Startup, off-time, configured bus timing and installed leakage remain open.
"""

import argparse
import xml.etree.ElementTree as ET

from check_sensor_alternative import rise_time


def audit_connections(root):
    """Check saved U26 topology; does not approve the replacement symbol."""
    components = {c.get("ref"): c for c in root.findall("./components/comp")}
    pin_nets = {}
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            key = (node.get("ref"), node.get("pin"))
            assert key not in pin_nets, f"Duplicate contact: {key}"
            pin_nets[key] = net.get("name")
    expected = {
        "1": "/SENS_SCL", "2": "+3V3_MCU", "3": "+3V3_MCU",
        "4": "/SENS_SDA", "6": "GND", "7": "GND", "8": "GND",
        "9": "+3V3_MCU", "10": "+3V3_MCU", "12": "/SENS_INT1",
    }
    for pin, net in expected.items():
        assert pin_nets.get(("U26", pin)) == net, f"U26.{pin} must connect to {net}"
    for pin in ("5", "11"):
        name = pin_nets.get(("U26", pin))
        assert name and name.startswith("unconnected-"), f"Review unused U26.{pin}"
        assert sum(n == name for n in pin_nets.values()) == 1
    for pin, net in (("K13", "/SENS_SCL"), ("R16", "/SENS_SDA"),
                     ("D11", "/SENS_INT1")):
        assert pin_nets.get(("U1", pin)) == net, f"Host contact U1.{pin} changed"
    for ref, value, lower in (("C115", "10u", "GND"),
                              ("C117", "100n", "GND"),
                              ("C118", "100n", "GND"),
                              ("R102", "3.3k", "/SENS_SCL"),
                              ("R103", "3.3k", "/SENS_SDA")):
        assert components[ref].findtext("value") == value, f"Review {ref} value"
        assert pin_nets.get((ref, "1")) == "+3V3_MCU", f"Review {ref} supply"
        assert pin_nets.get((ref, "2")) == lower, f"Review {ref} return/signal"
    part = components["U26"].findtext("value")
    print(f"Saved U26 topology passes; installed value: {part}")
    print("This does not verify pin types, metadata, placement or recovery behavior.")
    if part != "LIS2DTW12TR":
        print("Replacement remains pending; this export contains the prior sensor.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--netlist", help="Optional current KiCad XML export for topology audit")
    args = parser.parse_args()
    if args.netlist:
        audit_connections(ET.parse(args.netlist).getroot())
    rail_min, rail_max = 3.151819680, 3.393012496
    # ALS-005 shared LIS2DTW12/OPT4001 bus, superseding the prior 4.7k screen.
    resistance_min = 3300 * 0.99 * 0.99 * 0.95
    resistance_max = 3300 * 1.01 * 1.01 * 1.05
    leakage = 17e-6  # Acceptance allocation, not a device specification.
    capacitance_min, capacitance_max = 25e-12, 70e-12
    assert 1.62 < rail_min < rail_max < 3.6
    high_margin = rail_min - 0.2 - 0.8 * rail_max
    low_margin = 0.2 * rail_min - 0.2
    assert high_margin > 0 and low_margin > 0
    high_floor = rail_min - resistance_max * leakage
    sink = rail_max / resistance_min + leakage
    assert high_floor > 0.7 * rail_max and sink < 3e-3
    rise_min = rise_time(resistance_min, capacitance_min, rail_max, -leakage)
    rise_max = rise_time(resistance_max, capacitance_max, rail_min, leakage)
    assert 20e-9 < rise_min <= rise_max < 300e-9
    # Sensor low/high minima from Table7. Fall time is an allocated ceiling.
    slack = 1 / 400e3 - (1.3e-6 + 0.6e-6 + rise_max + 300e-9)
    assert slack > 0
    print("LIS2DTW12 conditional interface screen passes; qualification open")
    print(f"IRQ margins high/low: {high_margin:.9f}/{low_margin:.9f} V")
    print(f"Bus high floor: {high_floor:.9f} V; sink ceiling: {sink*1e3:.6f} mA")
    print(f"Allocated rise: {rise_min*1e9:.6f}..{rise_max*1e9:.6f} ns")
    print(f"400kHz period slack: {slack*1e9:.6f} ns")
    print("Does not establish startup, power-cycle or divider/filter timing.")


if __name__ == "__main__":
    main()
