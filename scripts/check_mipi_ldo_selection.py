"""Read-only CMS-013 installed inventory and alternative arithmetic screen.

Usage: python scripts/check_mipi_ldo_selection.py <fresh-kicadxml-export>
Sources, conditions and exclusions: design/mipi_ldo_selection.md.
No native CAD writes. Passing arithmetic does not clear integration HOLD.
"""

import argparse
from decimal import Decimal as D
import xml.etree.ElementTree as ET


def screen(path):
    root = ET.parse(path).getroot()
    components = {c.attrib["ref"]: c for c in root.findall("./components/comp")}
    pins = {}
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            key = (node.attrib["ref"], node.attrib["pin"])
            if key in pins:
                raise ValueError(f"Duplicate exported node: {key}")
            pins[key] = net.attrib["name"]
    expected = {
        "U23": "LT3042IMSE#PBF",
        "C108": "CL32B226MOJNNNE", "C109": "CL32B226MOJNNNE",
        "C110": "GRM31C5C1H104JA01K", "R94": "RC0603FR-071KL",
        "R95": "RT0603BRD0718KL", "C111": "C1608X7R1H104K080AA",
    }
    for ref, mpn in expected.items():
        actual = components[ref].findtext(
            './fields/field[@name="Manufacturer_Part_Number"]')
        if actual != mpn:
            raise ValueError(f"{ref}: {actual!r} differs from installed baseline {mpn}")
    for pin in ("1", "2", "3", "6"):
        if pins.get(("U23", pin)) != "+3V3_MCU":
            raise ValueError(f"Changed U23 input/control pin {pin}")
    for pin in ("5", "8", "11"):
        if pins.get(("U23", pin)) != "GND":
            raise ValueError(f"Changed U23 grounded pin {pin}")
    output_members = {k for k, net in pins.items() if net == "+1V8_MIPI"}
    if output_members != {("U23", "9"), ("U23", "10"), ("C109", "1"),
                          ("R94", "2"), ("U1", "R2"), ("C111", "1")}:
        raise ValueError("Changed MIPI rail membership")
    set_net = pins[("U23", "7")]
    if {k for k, net in pins.items() if net == set_net} != {
            ("U23", "7"), ("C110", "1"), ("R95", "2")}:
        raise ValueError("Changed installed SET network")
    for ref in ("C108", "C109", "C110", "C111"):
        if pins.get((ref, "2")) != "GND":
            raise ValueError(f"Changed grounded capacitor pad {ref}.2")
    for ref in ("R94", "R95"):
        if pins.get((ref, "1")) != "GND":
            raise ValueError(f"Changed grounded resistor pad {ref}.1")
    if pins.get(("C108", "1")) != "+3V3_MCU":
        raise ValueError("Changed input bypass connection")
    for ref, value in {"C108": "22u", "C109": "22u", "C110": "100n",
                       "R94": "1k", "R95": "18k", "C111": "100n"}.items():
        if components[ref].findtext("value") != value:
            raise ValueError(f"Changed {ref} nominal value")

    vmin, vmax = D("1.764"), D("1.836")
    if not D("1.65") < vmin < vmax < D("1.95"):
        raise ValueError("Alternative settled DC range outside MCU operating range")
    headroom = D("3.151819680") - D("2.35")
    bleed_min = D("1.65") / (D(1000) * D("1.01") ** 2)
    bleed_max = D("1.95") / (D(1000) * D("0.99") ** 2)
    if bleed_min <= D(".001"):
        raise ValueError("Permanent load does not satisfy accuracy test load floor")
    cmin = D("22e-6") * D(".8") * D(".85") * D(".6")
    retention_floor = D("2.2e-6") / (D("22e-6") * D(".8") * D(".85"))
    if cmin <= D("2.2e-6"):
        raise ValueError("Conditional capacitance below alternative stability minimum")

    print("PASS: saved installed LT3042 inventory/connections; arithmetic screen only")
    print(f"LT3060 settled V / input-condition headroom: {vmin}..{vmax} / {headroom} V")
    print(f"R94 load screen: {bleed_min * 1000:.9f}..{bleed_max * 1000:.9f} mA")
    print(f"Conditional C109: {cmin * 1_000_000} uF; retention floor {retention_floor * 100:.9f}%")
    for bypass_nf in (D(100), D(10), D("4.7")):
        typical_ms = D(6) * bypass_nf / D(10)
        print(f"REF/BYP {bypass_nf} nF: {typical_ms} ms typical proportional screen")
    print("U2 reset charge-only minimum 8.148276 ms; no maximum LDO settling proof")
    planning_input = D(".0041") + bleed_max + D(".004") + D(".000003") + D(".0001")
    if planning_input >= D(".020"):
        raise ValueError("Alternative planning screen exceeds retained 20mA allocation")
    planning_loss = (D("3.393012496") - vmin) * (D(".0041") + bleed_max)
    planning_loss += D("3.393012496") * (D(".004") + D(".000003") + D(".0001"))
    print(f"Alternative planning input: {planning_input * 1000:.9f} mA; keep 20mA allocation")
    print(f"Allocated loss: {planning_loss * 1000:.9f} mW; test-board rise at 60 C/W: {planning_loss * 60:.9f} C")
    saving = D("9.12") - D("4.79")
    print(f"IC-only qty-one saving: ${saving} ({saving / D('9.12') * 100:.6f}%)")
    print("HOLD: startup/restart/slew, PHY noise/PDN, retention, actual hot current and sealed-case thermal")
    print("No replacement installed, purchase release or guaranteed runtime improvement")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", help="Fresh saved KiCad XML netlist")
    screen(parser.parse_args().netlist)
