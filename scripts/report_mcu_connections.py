"""Read a KiCad XML netlist and report MCU ball ownership without editing CAD.

An open or singleton net is deliberately not called a free pin. Peripheral
reservations, voltage domains and reset behavior need separate qualification.
"""
import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    tree = ET.parse(args.netlist)
    component = next(c for c in tree.findall(".//components/comp") if c.get("ref") == "U1")
    source = component.find("libsource")
    part = next(p for p in tree.findall(".//libparts/libpart")
                if p.get("lib") == source.get("lib") and p.get("part") == source.get("part"))
    pins = {p.get("num"): p for p in part.findall("pins/pin")}
    if len(pins) != 289 or len(part.findall("pins/pin")) != 289:
        raise ValueError("Expected exactly 289 distinct MCU package pins")
    port = re.compile(r"^P[0-9A-D][0-9]{2}$")
    authority = root / "firmware/docs/pinouts/ra8p1_bga289_mipi.txt"
    expected = {}
    for line in authority.read_text(encoding="utf-8").splitlines():
        cells = line.split()
        if len(cells) == 18 and cells[0] in "ABCDEFGHJKLMNPRTU":
            for number, name in enumerate(cells[1:], 1):
                if port.fullmatch(name):
                    expected[f"{cells[0]}{number}"] = name
    actual = {ball: pin.get("name").split("/")[0] for ball, pin in pins.items()
              if port.fullmatch(pin.get("name").split("/")[0])}
    if len(expected) != 199 or actual != expected:
        raise ValueError("Cached MCU GPIO map differs from the 199-port BGA289 reference")
    nets = {}
    for net in tree.findall(".//nets/net"):
        nodes = net.findall("node")
        for node in nodes:
            if node.get("ref") == "U1":
                ball = node.get("pin")
                if ball in nets:
                    raise ValueError(f"MCU ball {ball} occurs on multiple nets")
                nets[ball] = (net.get("name"), nodes)
    reservations = {
        "P106": "Implemented SD_PWR_REQ; not free (microSD power interface)",
        "P107": "AUDIO_AUX_REQ GPIO output to U37 request gate; permission and U38 clamp are hardware",
        "P904": "AUDIO_AUX_PG GPIO input, polling; not headphone protection",
        "P108": "Historical optional MMC DAT6; expansion unresolved, not automatically free",
        "P109": "Historical optional MMC DAT5; expansion unresolved, not automatically free",
        "P110": "Historical optional MMC DAT4; expansion unresolved, not automatically free",
        "PD01": "RADIO-024 SDHI0_C DAT2",
        "PD02": "RADIO-024 SDHI0_C DAT1",
        "PD03": "RADIO-024 SDHI0_C DAT0",
        "PD04": "RADIO-024 SDHI0_C CMD",
        "PD05": "RADIO-024 SDHI0_C CLK",
        "P111": "RADIO-024 SDHI0_C DAT3",
        "PD06": "RADIO-024 USBHS_OVRCURA candidate",
        "P700": "SSI1_B TX; high-rate transport must be reconciled",
        "P701": "SSI1_B LRCLK; high-rate transport must be reconciled",
        "P702": "SSI1_B BCLK; high-rate transport must be reconciled",
        "P814": "USB FS DM/DP pair; USB ownership pending",
        "P815": "USB FS DM/DP pair; USB ownership pending",
    }
    rows = []
    counts = Counter()
    for ball, name in actual.items():
        net_name, nodes = nets.get(ball, ("not exported", []))
        peers = [f"{n.get('ref')}.{n.get('pin')}" for n in nodes
                 if (n.get("ref"), n.get("pin")) != ("U1", ball)]
        if peers:
            state = "connected"
        elif net_name.startswith("unconnected-") or not nodes:
            state = "open"
        else:
            state = "named singleton"
        counts[state] += 1
        rows.append(f"| {name} | {ball} | {pins[ball].get('type')} | {state} | "
                    f"{net_name} | {', '.join(peers) or '-'} | {reservations.get(name, '-')} |")
    text = ["# Saved MCU connection audit", "",
            f"MCU: {component.findtext('value')}; 289 unique pins and 199 GPIO ball names",
            "match the checked-in BGA289 pinout derived from Renesas Table 1.17.",
            "This comparison checks the cached symbol against that reference; it does",
            "not independently qualify the reference generator or peripheral functions.", "",
            f"Netlist SHA256: `{hashlib.sha256(args.netlist.read_bytes()).hexdigest()}`.",
            f"Counts: {dict(counts)}.", "",
            "Open means no exported electrical peer, not available for reassignment.",
            "Named singletons retain their intended ownership even without a receiver.",
            "The netlist does not prove whether an open pin has a no-connect marker.",
            "Reservations below are incomplete and must be reconciled with all subsystem",
            "contracts before assigning audio enable/status, DAC control or protection.",
            "SSI1_B cannot carry PCM768 in 64-bit stereo frames: 49.152 MHz exceeds",
            "the currently documented 12.5 MHz SSI limit. Keep XU316 transport work open.", "",
            "Reservation authorities: [radio SDIO](radio_sdio_migration.md),",
            "[camera/storage interfaces](camera_storage_interfaces.md), and",
            "[audio platform](audio_platform_study.md). These records distinguish",
            "future reservations from saved native wiring. Re-run after CAD changes:", "",
            "`python scripts/report_mcu_connections.py NETLIST.xml --output design/mcu_connection_audit.md`", "",
            "| Port | Ball | Cached type | Electrical state | Net | Other package pins | Documented reservation |",
            "| --- | --- | --- | --- | --- | --- | --- |", *rows, ""]
    args.output.write_text("\n".join(text), encoding="utf-8")
    print(f"MCU map comparison PASS; 199 ports; {dict(counts)}")
    print("No open pin is automatically approved as free. See", args.output)


if __name__ == "__main__":
    main()
