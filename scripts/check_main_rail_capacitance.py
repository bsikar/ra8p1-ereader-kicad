"""Inventory saved KiCad XML capacitance; nominal values, not qualification.

Usage: python scripts/check_main_rail_capacitance.py <exported-netlist.xml>
Export with kicad-cli sch export netlist --format kicadxml. No CAD writes.
See design/main_rail_capacitance.md for scope and unresolved paths.
"""

import argparse
from collections import defaultdict
from decimal import Decimal
from math import log
import re
import xml.etree.ElementTree as ET


def capacitance(value):
    # KiCad value fields may append a slash-separated voltage rating.
    # Parse only the nominal capacitance; reject other attached syntax.
    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*([pnum])(?:F)?(?:\s+.*|/\d+(?:\.\d+)?V)?", value)
    if not match:
        raise ValueError(f"Unrecognized capacitance value: {value!r}")
    factors = {"p": "1e-12", "n": "1e-9", "u": "1e-6", "m": "1e-3"}
    return Decimal(match[1]) * Decimal(factors[match[2]])


def inventory(path):
    root = ET.parse(path).getroot()
    components = {c.attrib["ref"]: c for c in root.findall("./components/comp")}
    if len(components) != len(root.findall("./components/comp")):
        raise ValueError("Duplicate component references")
    pins = defaultdict(dict)
    for net in root.findall("./nets/net"):
        for node in net.findall("node"):
            ref, pin = node.attrib["ref"], node.attrib["pin"]
            if pin in pins[ref]:
                raise ValueError(f"Duplicate node {ref}.{pin}")
            pins[ref][pin] = net.attrib["name"]

    rail_caps = defaultdict(list)
    for ref, comp in components.items():
        if not re.fullmatch(r"C\d+", ref):
            continue
        cap = capacitance(comp.findtext("value", ""))
        connected = list(pins[ref].values())
        if len(connected) != 2:
            raise ValueError(f"Capacitor {ref} does not have two exported pads")
        if "GND" in connected:
            other = connected.copy()
            other.remove("GND")
            mpn = comp.findtext('./fields/field[@name="Manufacturer_Part_Number"]')
            rail_caps[other[0]].append((ref, cap, mpn or "UNSPECIFIED"))

    # Fail visibly if the known ferrite topology changes; do not silently
    # treat an arbitrary similarly named net as direct main-rail storage.
    assert pins["FB1"] == {"1": "+3V3_MCU", "2": "+3V3_USBHS_A"}
    totals = {}
    for rail in ("+3V3_MCU", "+3V3_USBHS_A", "+3V3_RADIO", "VDD_SD",
                 "+1V8_MIPI", "/RA8P1 internal core regulator/MCU_VCORE",
                 "AON_HOLD", "SYS_AON"):
        if rail not in rail_caps:
            raise ValueError(f"Expected rail missing from inventory: {rail}")
        groups = defaultdict(list)
        for ref, cap, mpn in rail_caps[rail]:
            groups[(cap, mpn)].append(ref)
        total = sum((c for _, c, _ in rail_caps[rail]), Decimal(0))
        totals[rail] = total
        print(f"\n{rail}: {len(rail_caps[rail])} capacitors, {total * 1_000_000:f} uF nominal")
        for (cap, mpn), refs in sorted(groups.items()):
            refs.sort(key=lambda ref: int(ref[1:]))
            print(f"  {','.join(refs)}: {len(refs)} x {cap * 1_000_000:f} uF; {mpn}")

    key_total = Decimal(0)
    for resistor in ("R27", "R28", "R29", "R30"):
        nets = list(pins[resistor].values())
        assert len(nets) == 2 and "+3V3_MCU" in nets
        nets.remove("+3V3_MCU")
        caps = rail_caps[nets[0]]
        assert caps, f"No filter capacitance behind {resistor}"
        key_total += sum((c for _, c, _ in caps), Decimal(0))
    passive = totals["+3V3_MCU"] + totals["+3V3_USBHS_A"]
    print(f"\nMain plus FB1 branch: {passive * 1_000_000:f} uF nominal")
    # These switches are not unconditional reverse isolation during collapse.
    # Inventory their storage without pretending to model transient conduction.
    for ref, expected in {
        "U4": {"A2": "+3V3_MCU", "B2": "+3V3_MCU",
               "A1": "+3V3_RADIO", "B1": "+3V3_RADIO"},
        "U17": {"2": "+3V3_MCU", "5": "VDD_SD"},
    }.items():
        for pin, rail in expected.items():
            if pins[ref].get(pin) != rail:
                raise ValueError(f"Changed switched-storage path: {ref}.{pin}")
    switch_storage = totals["+3V3_RADIO"] + totals["VDD_SD"]
    print(f"Radio plus SD output storage: {switch_storage * 1_000_000:f} uF nominal")
    print(f"Main/FB1/radio/SD stored-capacitance subtotal: {(passive + switch_storage) * 1_000_000:f} uF nominal")
    print("This subtotal is not an equivalent discharge capacitance or an isolation guarantee.")
    # RADIO-022: calculate from this export rather than a cached capacitor sum.
    # TI SLVSBS6A: typical 10%-90% rise at VIN=3.3V/25C, CIN=1uF,
    # COUT=0.1uF and ROUT=10ohm. Not a guaranteed board waveform.
    radio_cap = float(totals["+3V3_RADIO"])
    print(f"Radio nominal-cap linear slew screen: {radio_cap * 0.8 * 3.3 / 715e-6 * 1e3:.6f} mA")
    for resistance in (273, 325):
        print(f"Radio ideal QOD 90%-10% RC screen at {resistance}ohm: {resistance * radio_cap * log(9) * 1e3:.6f} ms")
    print("QOD resistance table conditions: ON=0, IOUT=2mA.")
    print("These screens exclude module storage and do not establish startup/off-time.")
    print(f"Four resistor-fed key filters: {key_total * 1_000_000:f} uF nominal (separate RC tails)")
    print("NOT QUALIFIED: 1mF effective ceiling, external module capacitance,")
    print("switched/regulator reverse paths, component service bounds and board parasitics.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", help="Fresh saved-project KiCad XML netlist")
    inventory(parser.parse_args().netlist)
