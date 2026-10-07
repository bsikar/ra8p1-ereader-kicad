#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate isolated KiCad simulation schematics for the audio study circuits.

Each project in this folder is standalone: open the .kicad_pro, then Inspect > Simulator.
Symbols come from KiCad's stock Simulation_SPICE and Device libraries. TI op-amp models
are referenced from ../../models and are not redistributed. These are study circuits,
not part of the e-reader design, and their values are nominal-model candidates.
"""
import copy
import json
import math
import uuid
from pathlib import Path

from sexp import Q, dump, find, parse

HERE = Path(__file__).resolve().parent
STOCK = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols")
G = 2.54
_libs = {}


CUSTOM = {}


def box_symbol(name, left, right, width=6):
    """Rectangular symbol with named pins; numbers run down the left side, then the right."""
    rows = max(len(left), len(right))
    h, w = (rows + 1) * G / 2, width * G / 2
    eff = ["effects", ["font", ["size", "1.27", "1.27"]]]
    pins, n = [], 0
    for side, names in ((-1, left), (1, right)):
        for i, pname in enumerate(names):
            n += 1
            y = h - (i + 1) * G
            pins.append(["pin", "passive", "line", ["at", f"{side * (w + G):g}", f"{y:g}", "0" if side < 0 else "180"],
                         ["length", "2.54"], ["name", Q(pname), eff], ["number", Q(str(n)), eff]])
    CUSTOM[name] = ["symbol", Q(name), ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"],
        ["property", Q("Reference"), Q("U"), ["at", "0", f"{h + 1.27:g}", "0"], eff],
        ["property", Q("Value"), Q(name), ["at", "0", f"{-h - 1.27:g}", "0"], eff],
        ["symbol", Q(f"{name}_0_1"), ["rectangle", ["start", f"{-w:g}", f"{h:g}"], ["end", f"{w:g}", f"{-h:g}"],
            ["stroke", ["width", "0.254"], ["type", "default"]], ["fill", ["type", "background"]]]],
        ["symbol", Q(f"{name}_1_1")] + pins]


def lib_symbol(lib, name):
    if lib == "Study":
        return CUSTOM[name]
    if lib not in _libs:
        _libs[lib] = parse((STOCK / f"{lib}.kicad_sym").read_text())
    for sym in find(_libs[lib], "symbol"):
        if sym[1] == name:
            return sym
    raise KeyError(name)


def uid():
    return Q(str(uuid.uuid4()))


def mm(v):
    return f"{round(v * G, 4):g}"


FONT = ["effects", ["font", ["size", "1.27", "1.27"]]]


class Part:
    def __init__(self, sch, lib, name, ref, x, y, rot, mirror):
        self.x, self.y, self.rot, self.mirror = x, y, rot, mirror
        self.pins = {}
        for sub in find(lib_symbol(lib, name), "symbol"):
            for pin in find(sub, "pin"):
                at = find(pin, "at")[0]
                self.pins[str(find(pin, "number")[0][1])] = (float(at[1]) / G, float(at[2]) / G)

    def p(self, number):
        px, py = self.pins[str(number)]
        if self.mirror == "x":
            py = -py
        if self.mirror == "y":
            px = -px
        a = math.radians(self.rot)
        rx = px * math.cos(a) - py * math.sin(a)
        ry = px * math.sin(a) + py * math.cos(a)
        return (round(self.x + rx, 3), round(self.y - ry, 3))


class Sch:
    def __init__(self, name, title, paper="A3"):
        self.name, self.title, self.paper = name, title, paper
        self.root = str(uuid.uuid4())
        self.used, self.items, self.gnd_count = {}, [], 0

    def sym(self, kind, ref, value, x, y, rot=0, mirror=None, ref_at=None, val_at=None, side="right", **sim):
        lib, name = kind.split(":")
        self.used.setdefault(kind, lib_symbol(lib, name))
        part = Part(self, lib, name, ref, x, y, rot, mirror)
        ang = "90" if rot in (90, 270) else "0"
        hidden = ref.startswith("#")
        horiz = rot in (90, 270)
        sgn = -1 if side in ("left", "below") else 1
        rx, ry = ref_at or ((-1.3, -0.9 * sgn) if horiz else (1.0 * sgn, -0.6))
        vx, vy = val_at or ((1.3, -0.9 * sgn) if horiz else (1.0 * sgn, 0.6))
        just = [] if horiz or ref_at or val_at else [["justify", "left" if sgn > 0 else "right"]]

        def prop(key, val, px, py, hide):
            eff = copy.deepcopy(FONT) + copy.deepcopy(just) + ([["hide", "yes"]] if hide else [])
            return ["property", Q(key), Q(val), ["at", mm(px), mm(py), ang], eff]

        props = [prop("Reference", ref, x + rx, y + ry, hidden),
                 prop("Value", value, x + vx, y + vy, hidden),
                 prop("Footprint", "", x, y, True), prop("Datasheet", "", x, y, True),
                 prop("Description", "", x, y, True)]
        base = {p[1]: p[2] for p in find(self.used[kind], "property") if p[1].startswith("Sim.")}
        base.update({"Sim." + k.capitalize(): v for k, v in sim.items()})
        props += [prop(k, v, x, y, True) for k, v in base.items()]
        node = ["symbol", ["lib_id", Q(kind)], ["at", mm(x), mm(y), str(rot)]]
        if mirror:
            node.append(["mirror", mirror])
        node += [["unit", "1"], ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"],
                 ["dnp", "no"], ["uuid", uid()]] + props
        node += [["pin", Q(n), ["uuid", uid()]] for n in part.pins]
        node.append(["instances", ["project", Q(self.name), ["path", Q("/" + self.root),
                     ["reference", Q(ref)], ["unit", "1"]]]])
        self.items.append(node)
        return part

    def w(self, *pts):
        """Wire through the points; a diagonal step becomes horizontal-then-vertical."""
        for a, b in zip(pts, pts[1:]):
            legs = [(a, b)] if a[0] == b[0] or a[1] == b[1] else [(a, (b[0], a[1])), ((b[0], a[1]), b)]
            for s, e in legs:
                self.items.append(["wire", ["pts", ["xy", mm(s[0]), mm(s[1])], ["xy", mm(e[0]), mm(e[1])]],
                                   ["stroke", ["width", "0"], ["type", "default"]], ["uuid", uid()]])

    def j(self, *pts):
        for p in pts:
            self.items.append(["junction", ["at", mm(p[0]), mm(p[1])], ["diameter", "0"],
                               ["color", "0", "0", "0", "0"], ["uuid", uid()]])

    def lab(self, net, p, rot=0, just="left"):
        self.items.append(["label", Q(net), ["at", mm(p[0]), mm(p[1]), str(rot)],
                           copy.deepcopy(FONT) + [["justify", just, "bottom"]], ["uuid", uid()]])

    def gnd(self, *pts):
        for p in pts:
            self.gnd_count += 1
            self.sym("Simulation_SPICE:0", f"#GND{self.gnd_count:02d}", "0", p[0], p[1])

    def text(self, body, x, y, size=1.27):
        self.items.append(["text", Q(body), ["exclude_from_sim", "no"], ["at", mm(x), mm(y), "0"],
                           ["effects", ["font", ["size", str(size), str(size)]], ["justify", "left", "top"]],
                           ["uuid", uid()]])

    # convenience two-pin parts ------------------------------------------------------------
    def r(self, ref, value, x, y, horiz=False, **kw):
        return self.sym("Device:R", ref, value, x, y, 90 if horiz else 0, **kw)

    def c(self, ref, value, x, y, horiz=False, **kw):
        return self.sym("Device:C", ref, value, x, y, 90 if horiz else 0, **kw)

    def opamp(self, ref, model, x, y, inverting_on_top=False):
        u = self.sym("Simulation_SPICE:OPAMP", ref, model, x, y, mirror="x" if inverting_on_top else None,
                     ref_at=(1.5, -2.2), val_at=(4, 2.2), device="SUBCKT",
                     library=f"../../models/{model}.LIB", name=model,
                     pins="1=IN+ 2=IN- 3=VCC 4=VEE 5=OUT")
        self.lab("VP", u.p(3), 0)
        self.lab("VN", u.p(4), 0)
        return u

    def cmp(self, ref, x, y):
        """Behavioural open-drain comparator drawn with the op-amp triangle."""
        u = self.sym("Simulation_SPICE:OPAMP", ref, "comparator", x, y, ref_at=(1.5, -2.2), val_at=(4, 2.2),
                     device="SUBCKT", library="../study_models.lib", name="CMP_OD",
                     pins="1=inp 2=inn 3=vcc 4=vee 5=out")
        self.lab("VAUX", u.p(3), 0)
        self.gnd(u.p(4))
        return u

    def src(self, net, value, x, y, kind="VDC", **sim):
        n = sum(1 for i in self.items if i[0] == "symbol" and "Simulation_SPICE:V" in str(i[1])) + 1
        v = self.sym(f"Simulation_SPICE:{kind}", f"V{n}", value, x, y, **sim)
        self.w(v.p(1), (x, y - 4)); self.lab(net, (x, y - 4), 90); self.gnd(v.p(2))
        return v

    def write(self):
        out = HERE / self.name
        out.mkdir(exist_ok=True)
        libs = []
        for kind, sym in self.used.items():
            s = copy.deepcopy(sym)
            s[1] = Q(kind)
            libs.append(s)
        doc = ["kicad_sch", ["version", "20250114"], ["generator", Q("eeschema")],
               ["generator_version", Q("9.0")], ["uuid", Q(self.root)], ["paper", Q(self.paper)],
               ["title_block", ["title", Q(self.title)], ["company", Q("Simulation study - not the product schematic")]],
               ["lib_symbols"] + libs] + self.items + [
               ["sheet_instances", ["path", Q("/"), ["page", Q("1")]]], ["embedded_fonts", "no"]]
        (out / f"{self.name}.kicad_sch").write_text(dump(doc) + "\n")
        pro = {"meta": {"filename": f"{self.name}.kicad_pro", "version": 3},
               "schematic": {"ngspice": {"fix_include_paths": True, "model_mode": 4}},
               "sheets": [[self.root, "Root"]], "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
               "text_variables": {}}
        (out / f"{self.name}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n")
        return out / f"{self.name}.kicad_sch"


# ------------------------------------------------------------------------------------------
def quiet_chain():
    s = Sch("quiet_chain", "Quiet headphone path (I/V, diff-to-SE, OPA1622)")
    s.text("QUIET HEADPHONE PATH (single-ended, one channel)\n\n"
           "DAC pins are modelled as +/-1.525 V sources behind 390 ohm (swing is an assumption to confirm).\n"
           "VCM is the DAC bias. Real value 1.65 V; drawn as 0 V because the TI OPA161x model does not\n"
           "find a DC operating point with the bias applied. Frequency response and noise are unaffected.\n"
           "Drawn in low gain (-20 dB: R9=360, R10=40). For 0 dB gain set R9=1m and R10=1000k.\n"
           "Run: Inspect > Simulator > Run. For noise use: .noise v(out) V1 dec 50 20 20k", 40, 60, 1.5)
    s.text(".ac dec 50 10 10meg", 40, 72, 2)
    s.text(".options rshunt=1e12", 40, 74, 2)

    v = s.sym("Simulation_SPICE:VSIN", "V1", "DAC code", 10, 36,
              params="dc=0 ampl=1 f=1k ac=1", ref_at=(0, 3.2), val_at=(0, 4.2))
    s.gnd(v.p(2)); s.w(v.p(1), (10, 30)); s.lab("sig", (10, 30), 90)

    def phase(y, tag, gain, n):
        e = s.sym("Simulation_SPICE:ESOURCE", f"E{n}", f"x{gain}", 20, y + 2,
                  params=f'type="E" model="{gain}"', ref_at=(-4.5, 1.5), val_at=(-4.5, 2.5))
        s.w(e.p(3), (18, y - 1)); s.lab("sig", (18, y - 1), 90)
        s.gnd(e.p(4))
        s.w(e.p(2), (20, y + 5), (21, y + 5)); s.lab("VCM", (21, y + 5))
        rd = s.r(f"R{n}", "390", 25.5, y, True)
        s.w(e.p(1), rd.p(1))
        u = s.opamp(f"U{n}", "OPA161x", 37, y + 1, inverting_on_top=True)
        cd = s.c(f"C{n}", "15p", 29, y + 2.5, side="left")
        s.w(rd.p(2), u.p(2)); s.w((29, y), cd.p(1)); s.gnd(cd.p(2))
        s.w(u.p(1), (33, y + 2)); s.lab("VCM", (33, y + 2), 180, "right")
        rf = s.r(f"R{n + 2}", "392", 37, y - 5, True)
        cf = s.c(f"C{n + 2}", "1.3n", 37, y - 9, True)
        s.w((32, y), (32, y - 5), rf.p(1)); s.w((32, y - 5), (32, y - 9), cf.p(1))
        s.w(rf.p(2), (42, y - 5), (42, y + 1)); s.w(cf.p(2), (42, y - 9), (42, y - 5)); s.w(u.p(5), (42, y + 1))
        s.j((29, y), (32, y), (32, y - 5), (42, y - 5), (42, y + 1))
        s.lab(f"iv{tag}", (42.5, y + 1))
        return (42, y + 1)

    ivp = phase(20, "p", "1.525", 1)
    ivn = phase(50, "n", "-1.525", 2)

    u = s.opamp("U3", "OPA161x", 60, 36, inverting_on_top=True)
    r1 = s.r("R5", "499", 50, 35, True); r3 = s.r("R7", "499", 50, 37, True, side="below")
    s.w(ivp, (46, 21), (46, 35), r1.p(1)); s.w(ivn, (46, 51), (46, 37), r3.p(1))
    s.w(r1.p(2), u.p(2)); s.w(r3.p(2), u.p(1))
    r2 = s.r("R6", "499", 60, 30, True); c2 = s.c("C5", "1.5n", 60, 26, True)
    s.w((54, 35), (54, 30), r2.p(1)); s.w((54, 30), (54, 26), c2.p(1))
    s.w(r2.p(2), (65, 30), (65, 36)); s.w(c2.p(2), (65, 26), (65, 30)); s.w(u.p(5), (65, 36))
    r4 = s.r("R8", "499", 53, 41.5, side="left"); c4 = s.c("C6", "1.5n", 55.5, 41.5)
    s.w((53, 37), r4.p(1)); s.w((55.5, 37), c4.p(1)); s.gnd(r4.p(2), c4.p(2))
    s.j((54, 35), (54, 30), (65, 30), (65, 36), (53, 37), (55.5, 37))
    s.lab("line", (65.5, 36))

    ra = s.r("R9", "360", 70, 36, True)
    s.w((65, 36), ra.p(1))
    b = s.opamp("U4", "OPA1622", 81, 37)
    s.w(ra.p(2), b.p(1))
    rb = s.r("R10", "40", 75, 39.5, side="left")
    s.w((75, 36), rb.p(1)); s.gnd(rb.p(2)); s.j((75, 36)); s.lab("att", (75.5, 36))
    s.w(b.p(2), (77, 38), (77, 43), (86, 43), (86, 37)); s.w(b.p(5), (86, 37))
    rr = s.r("R11", "0.1", 90, 37, True)
    s.text("relay K1 contact", 87.5, 39, 1.0)
    s.w((86, 37), rr.p(1)); s.j((86, 37))
    rl = s.r("R12", "32", 95, 40.5); cl = s.c("C7", "1n", 99, 40.5)
    s.w(rr.p(2), (102, 37)); s.w((99, 37), cl.p(1)); s.w((95, 37), rl.p(1)); s.gnd(rl.p(2), cl.p(2)); s.j((95, 37), (99, 37))
    s.lab("out", (100, 37))
    s.text("headphone\n+ cable", 93, 44.5, 1.0)

    for i, (name, val) in enumerate((("VP", "5"), ("VN", "-5"), ("VCM", "0"))):
        x = 10 + 8 * i
        src = s.sym("Simulation_SPICE:VDC", f"V{i + 2}", val, x, 70)
        s.w(src.p(1), (x, 66)); s.lab(name, (x, 66), 90); s.gnd(src.p(2))
    return s.write()


def protection():
    s = Sch("protection", "Headphone DC / rail-fault protection (proposed)")
    box_symbol("RELAY", ["COIL+", "COIL-"], ["COM", "NO"], 8)
    s.text("PROPOSED HEADPHONE PROTECTION (new circuit, not yet in the product schematic)\n\n"
           "Each amplifier output is level-shifted to 1.25 V and low-pass filtered at 0.3 Hz (R1-R4, C1-C2).\n"
           "U1-U4 trip if the filtered output leaves +/-100 mV DC. U5/U6 trip if either +/-5 V rail is below 4.5 V.\n"
           "Any trip discharges C3 (FAULT_N). U7 lets the MCU request reach Q4 only once C3 has recharged (~0.7 s).\n"
           "Q4, D1 and K1 are the driver, clamp and relay already drawn in the product schematic.\n"
           "Comparators and relay are behavioural models (study_models.lib); the relay opens when coil current\n"
           "falls below 3.3 mA, plus 3 ms. Coil inductance 0.2 H is an estimate.\n\n"
           "Stimulus: V7 steps the left amplifier output to +4.5 V DC at 100 ms. Plot HP_L, GATE, FAULT_N.\n"
           "The 2.4 s power-on delay is not visible here because this run starts from steady state.", 70, 52, 1.5)
    s.text(".tran 20u 200m", 70, 74, 2)

    def chan(y0, name, n):
        s.w((28, y0 + 4), (32.5, y0 + 4)); s.lab(f"AMP_{name}", (28, y0 + 4))
        rs = s.r(f"R{n}", "470k", 34, y0 + 4, True)
        rv = s.r(f"R{n + 1}", "470k", 38, y0 + 0.5)
        s.w(rv.p(1), (38, y0 - 2)); s.lab("VREF", (38, y0 - 2), 90)
        s.w(rv.p(2), (38, y0 + 4))
        c = s.c(f"C{(n + 1) // 2}", "2.2u", 41, y0 + 6.5)
        s.w((41, y0 + 4), c.p(1)); s.gnd(c.p(2))
        s.w(rs.p(2), (44, y0 + 4)); s.lab(f"S{name}", (42, y0 + 4))
        hi = s.cmp(f"U{n}", 52, y0); lo = s.cmp(f"U{n + 1}", 52, y0 + 9)
        s.w((44, y0 + 4), (44, y0 + 1), hi.p(2)); s.w((44, y0 + 4), (44, y0 + 8), lo.p(1))
        s.w(hi.p(1), (47, y0 - 1)); s.lab("WHI", (47, y0 - 1), 180, "right")
        s.w(lo.p(2), (47, y0 + 10)); s.lab("WLO", (47, y0 + 10), 180, "right")
        s.w(hi.p(5), (60, y0)); s.w(lo.p(5), (60, y0 + 9))
        s.j((38, y0 + 4), (41, y0 + 4), (44, y0 + 4), (60, y0), (60, y0 + 9))

    chan(16, "L", 1)
    chan(38, "R", 3)

    u5 = s.cmp("U5", 52, 60)
    rp1 = s.r("R5", "100k", 40, 55.5); rp2 = s.r("R6", "100k", 40, 62.5)
    s.w(rp1.p(1), (40, 53)); s.lab("VPOS", (40, 53), 90)
    s.w(rp1.p(2), rp2.p(1)); s.gnd(rp2.p(2)); s.w((40, 59), u5.p(1)); s.j((40, 59))
    s.w(u5.p(2), (47, 61)); s.lab("REF_2V25", (47, 61), 180, "right")
    u6 = s.cmp("U6", 52, 74)
    rn2 = s.r("R7", "100k", 40, 70.5); rn1 = s.r("R8", "200k", 40, 79.5)
    s.w(rn2.p(1), (40, 68)); s.lab("VREF", (40, 68), 90)
    s.w(rn2.p(2), rn1.p(1)); s.w(rn1.p(2), (40, 82), (41, 82)); s.lab("VNEG", (41, 82))
    s.w((40, 75), u6.p(2)); s.j((40, 75))
    s.w(u6.p(1), (47, 73)); s.lab("REF_0V167", (47, 73), 180, "right")
    s.w(u5.p(5), (60, 60)); s.w(u6.p(5), (60, 74))

    rfn = s.r("R9", "1000k", 60, 8.5)
    s.w(rfn.p(1), (60, 6)); s.lab("VAUX", (60, 6), 90)
    s.w(rfn.p(2), (60, 74))
    cfn = s.c("C3", "1u", 65, 15.5)
    s.w((60, 13), (65, 13), cfn.p(1)); s.gnd(cfn.p(2)); s.lab("FAULT_N", (60.5, 13))
    s.j((60, 13), (60, 25), (60, 38), (60, 47), (60, 60), (60, 29))

    u7 = s.cmp("U7", 72, 30)
    s.w((60, 29), u7.p(1)); s.w(u7.p(2), (67, 31)); s.lab("VREF", (67, 31), 180, "right")
    rg1 = s.r("R10", "1k", 79, 26.5); rg2 = s.r("R11", "10k", 79, 33.5)
    s.w(rg1.p(1), (79, 23)); s.lab("MCU_REQ", (79, 23), 90)
    s.w(rg1.p(2), rg2.p(1)); s.gnd(rg2.p(2))
    q = s.sym("Simulation_SPICE:NMOS", "Q4", "FDN337N", 88, 30, ref_at=(3.5, -0.6), val_at=(3.5, 0.6),
              params="vto=0.7 kp=10")
    s.w(u7.p(5), q.p(2)); s.j((79, 30)); s.lab("GATE", (81, 30))
    s.w(q.p(3), (89, 34)); s.gnd((89, 34))
    d = s.sym("Simulation_SPICE:D", "D1", "SMF12A", 95, 30, 270, ref_at=(2.5, -0.6), val_at=(2.5, 0.6),
              params="bv=14 ibv=1m rs=0.5 cjo=300p")
    s.w(q.p(1), (89, 26)); s.w(d.p(1), (95, 26), (89, 26)); s.w(d.p(2), (95, 34)); s.gnd((95, 34))
    k = s.sym("Study:RELAY", "K1", "G6K-2F-Y 3V", 100, 15.5, ref_at=(0, -3), val_at=(0, 3),
              device="SUBCKT", library="../study_models.lib", name="RELAY_G6K_3V",
              pins="1=cp 2=cn 3=com 4=no")
    s.w(k.p(1), (92, k.p(1)[1])); s.lab("COIL_3V", (92, k.p(1)[1]), 180, "right")
    s.w(k.p(2), (89, k.p(2)[1]), (89, 26)); s.j((89, 26)); s.lab("DRAIN", (90, k.p(2)[1]))
    s.w(k.p(3), (110, k.p(3)[1])); s.lab("AMP_L", (108, k.p(3)[1]))
    rhp = s.r("R12", "32", 112, 21.5)
    s.w(k.p(4), (112, k.p(4)[1]), rhp.p(1)); s.gnd(rhp.p(2)); s.lab("HP_L", (108, k.p(4)[1]))
    s.text("headphone", 114.5, 23.5, 1.0)

    vals = (("2.5k", "REF_2V25"), ("9.5k", "WHI"), ("1k", "WLO"), ("10.33k", "REF_0V167"), ("1.67k", None))
    s.w((14, 44), (14, 42)); s.lab("VREF", (14, 42), 90)
    for i, (val, tap) in enumerate(vals):
        y = 45.5 + 6 * i
        rr = s.r(f"R{13 + i}", val, 14, y)
        if i:
            s.w((14, y - 4.5), rr.p(1))
        if tap:
            s.w((14, y + 2.5), (16, y + 2.5)); s.lab(tap, (16, y + 2.5)); s.j((14, y + 2.5))
    s.gnd((14, 71))
    s.text("reference ladder (ideal values)", 8, 73, 1.0)

    for i, (net, val) in enumerate((("VAUX", "5"), ("VREF", "2.5"), ("VPOS", "5"), ("VNEG", "-5"),
                                    ("MCU_REQ", "3.3"), ("COIL_3V", "3"))):
        s.src(net, val, 10 + 8 * i, 100)
    s.src("AMP_L", "amp fault step", 60, 100, "VPWL", params='pwl="0 0 100m 0 100.01m 4.5"')
    s.src("AMP_R", "0", 70, 100)
    return s.write()


if __name__ == "__main__":
    for build in (quiet_chain, protection):
        print(build())
