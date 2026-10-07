#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Nominal-model SPICE investigation of the quiet headphone path and its protection.

Requires ngspice and separately obtained TI models in sim/models (not redistributed).
Every result is a typical-model screen at 27 C, never a hardware qualification.
Run from anywhere: sim/.venv/bin/python sim/run_all.py
"""
import json
import math
import random
import re
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM = Path(__file__).resolve().parent
OUT = SIM / "out"
OUT.mkdir(exist_ok=True)
RESULTS = {}


def run(name, netlist, timeout=600):
    path = OUT / f"{name}.cir"
    path.write_text(netlist)
    proc = subprocess.run(["ngspice", "-b", str(path)], cwd=SIM, capture_output=True,
                          text=True, timeout=timeout)
    text = proc.stdout + proc.stderr
    (OUT / f"{name}.log").write_text(text)
    values = {}
    for key, val in re.findall(r"^\s*([a-z_][a-z0-9_]*)\s*=\s*([-+0-9.eE]+)", text, re.M | re.I):
        values[key.lower()] = float(val)
    thd = re.findall(r"THD:\s*([-+0-9.eE]+)\s*%", text)
    if thd:
        values["thd_percent"] = float(thd[-1])
    if "fatal" in text.lower() or "simulation interrupted" in text.lower():
        raise RuntimeError(f"{name}: ngspice failed, see {path.with_suffix('.log')}")
    return values


def table(name):
    return np.loadtxt(OUT / name)


# --------------------------------------------------------------------------- quiet chain
# DAC pin model: Thevenin source at Vcm with 390 ohm (docs: typical per-pin output
# impedance). The +/-1.525 V open-circuit swing (0.924*AVCC p-p at AVCC=3.3 V) is an
# ASSUMPTION to confirm against the ES9039Q2M datasheet output-stage reference.
CHAIN = """* quiet single-ended chain: DAC model -> I/V -> diff-to-SE -> attenuator -> OPA1622
.include models/OPA161x.LIB
.include models/OPA1622.LIB
.param rdac=390 vfs=1.525 vcm={vcm}
.param rfp={rfp} rfn={rfn} cf=1.3n
.param r1={r1} r2={r2} r3={r3} r4={r4} cd=1.5n
.param ra={ra} rb={rb} rl={rl} cl={cl}
VP vp 0 {vp}
VN vn 0 {vn}
VCM vcm 0 {vcmsrc}
VSIG sig 0 dc 0 ac {ac} sin(0 {amp} 1k 4m)
EDP dp vcm sig 0 {{vfs}}
EDN dn vcm sig 0 {{-vfs}}
RDP dp sp {{rdac}}
RDN dn sn {{rdac}}
CDP sp 0 15p
CDN sn 0 15p
{xivp}
RFP sp ivp {{rfp}}
CFP sp ivp {{cf}}
{xivn}
RFN sn ivn {{rfn}}
CFN sn ivn {{cf}}
R1 ivp dm {{r1}}
R2 dm line {{r2}}
C2 dm line {{cd}}
R3 ivn dpl {{r3}}
R4 dpl 0 {{r4}}
C4 dpl 0 {{cd}}
{xdif}
RA line att {{ra}}
RB att 0 {{rb}}
{xbuf}
RRLY amp out 0.1
RL out 0 {{rl}}
CL out 0 {{cl}}
ITEST 0 out dc 0 ac {itest}
"""

ATTEN = {"0dB": (1e-3, 1e9), "-20dB": (360.0, 40.0)}
NOM = dict(rfp=392, rfn=392, r1=499, r2=499, r3=499, r4=499)


REAL = dict(xivp="XIVP vcm sp vp vn ivp OPA161x", xivn="XIVN vcm sn vp vn ivn OPA161x",
            xdif="XDIF dpl dm vp vn line OPA161x", xbuf="XBUF att amp vp vn amp OPA1622")
IDEAL = dict(xivp="EIVP ivp 0 vcm sp 1e7", xivn="EIVN ivn 0 vcm sn 1e7",
             xdif="EDIF line 0 dpl dm 1e7", xbuf="EBUF amp 0 att 0 1")


def chain(gain, rl, cl="1n", ac=1, amp=0, itest=0, mode="linear", **over):
    """mode linear: DAC common mode set to 0 V (the TI models do not find a DC point with the
    1.65 V bias; small-signal response and noise are unchanged). mode ramp: true 1.65 V bias,
    supplies ramped for a uic transient. mode ideal: ideal op-amps for resistor-only DC error."""
    ra, rb = ATTEN[gain]
    p = dict(NOM, ra=ra, rb=rb, rl=rl, cl=cl, ac=ac, amp=amp, itest=itest, **REAL)
    p.update(vp="5", vn="-5", vcm=0, vcmsrc="0")
    if mode == "ramp":
        p.update(vp="pwl(0 0 1m 5)", vn="pwl(0 0 1m -5)", vcm=1.65, vcmsrc="pwl(0 0 1m 1.65)")
    if mode == "ideal":
        p.update(IDEAL, vcm=1.65, vcmsrc="1.65")
    p.update(over)
    return CHAIN.format(**p)


def quiet_chain():
    res = {}
    fig, ax = plt.subplots(figsize=(7, 4))
    for gain in ATTEN:
        for rl in (16, 32, 300):
            tag = f"{gain}_{rl}ohm"
            r = run(f"chain_ac_{tag}", chain(gain, rl) + f"""
.control
ac dec 50 10 10meg
meas ac g1k find vdb(out) at=1k
meas ac g20 find vdb(out) at=20
meas ac g20k find vdb(out) at=20k
wrdata out/chain_ac_{tag}.txt vdb(out)
noise v(out) VSIG dec 50 20 20k
setplot noise2
print onoise_total
.endc
.end
""")
            d = table(f"chain_ac_{tag}.txt")
            g1k = r["g1k"]
            below = np.flatnonzero((d[:, 0] > 1e3) & (d[:, 1] < g1k - 3))
            fs_vrms = 10 ** (g1k / 20) / math.sqrt(2)
            noise = r["onoise_total"]
            res[tag] = {"gain_1k_db": g1k, "full_scale_vrms": fs_vrms,
                        "dev_20hz_db": r["g20"] - g1k, "dev_20khz_db": r["g20k"] - g1k,
                        "f3_hz": float(d[below[0], 0]) if len(below) else None,
                        "noise_20_20k_uvrms": noise * 1e6,
                        "dnr_db": 20 * math.log10(fs_vrms / noise)}
            if rl == 32:
                ax.semilogx(d[:, 0], d[:, 1] - g1k, label=f"{gain} gain, 32 ohm")
    ax.axvspan(20, 20e3, alpha=0.08)
    ax.set(xlabel="Hz", ylabel="dB re 1 kHz", ylim=(-6, 1), title="Quiet chain frequency response")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "chain_response.png", dpi=130); plt.close(fig)

    # output impedance seen by the headphone (signal off, 1 A AC test current)
    r = run("chain_zout", chain("0dB", 1e6, cl="1p", ac=0, itest=1) + """
.control
ac dec 20 20 100k
meas ac z1k find vm(out) at=1k
meas ac z20k find vm(out) at=20k
.endc
.end
""")
    res["zout_ohm"] = {"1kHz": r["z1k"], "20kHz": r["z20k"]}

    # 1 kHz full-scale transient: distortion sanity check and supply power
    thd = {}
    for gain, rl in (("-20dB", 16), ("-20dB", 32), ("0dB", 32), ("0dB", 300)):
        # the vendor models are fragile during the supply ramp: try integrator settings in turn
        for opts in ("", ".options method=gear", ".options rshunt=1e10 cshunt=1e-15",
                     ".options method=gear rshunt=1e10 cshunt=1e-15"):
            r = run(f"chain_tran_{gain}_{rl}", chain(gain, rl, ac=0, amp=1, mode="ramp") + opts + """
.control
tran 2u 14m 0 2u uic
meas tran vrms rms v(out) from=4m to=14m
meas tran ipos avg i(vp) from=4m to=14m
meas tran ineg avg i(vn) from=4m to=14m
meas tran vpk max v(out) from=4m to=14m
meas tran ivmax max v(ivp) from=4m to=14m
meas tran ivmin min v(ivp) from=4m to=14m
.endc
.end
""")
            if "vrms" in r:
                break
        else:
            thd[f"{gain}_{rl}ohm"] = "UNKNOWN: transient did not complete"
            continue
        pin = 5 * (-r["ipos"]) + 5 * r["ineg"]
        pout = r["vrms"] ** 2 / rl
        thd[f"{gain}_{rl}ohm"] = {"vout_rms": r["vrms"], "pout_mw": pout * 1e3,
                                  "ipeak_ma": r["vpk"] / rl * 1e3, "iv_stage_out_min_v": r["ivmin"],
                                  "iv_stage_out_max_v": r["ivmax"],
                                  "rail_power_mw": pin * 1e3, "heat_mw": (pin - pout) * 1e3}
    res["fullscale_1khz"] = thd

    # DC offset at the jack from resistor tolerance (the 1.65 V DAC common mode is the driver)
    random.seed(1)
    offs = {}
    for tol in (0.01, 0.001):
        vals = []
        for _ in range(200):
            p = {k: v * (1 + random.uniform(-tol, tol)) for k, v in NOM.items()}
            run("chain_dc", chain("0dB", 32, ac=0, mode="ideal", **p) + "\n.control\nop\nprint v(out)\n.endc\n.end\n")
            vals.append(float(re.search(r"v\(out\)\s*=\s*([-+0-9.eE]+)",
                                        (OUT / "chain_dc.log").read_text()).group(1)))
        offs[f"{tol*100:g}%"] = {"max_abs_mv": max(map(abs, vals)) * 1e3,
                                 "sigma_mv": float(np.std(vals)) * 1e3}
    res["dc_offset_0dB_gain"] = offs
    RESULTS["quiet_chain"] = res


# --------------------------------------------------------------------------- stability
STAB = """* OPA1622 unity buffer loop gain into cable capacitance
.include models/OPA1622.LIB
VP vp 0 5
VN vn 0 -5
VIN inp 0 dc 0 {vin}
XU inp inm vp vn o OPA1622
LFB o inm {lfb}
CT vt inm {ct}
VT vt 0 dc 0 ac {vt}
RISO o out {riso}
RL out 0 {rl}
CL out 0 {cl}
"""


def stability():
    res = {}
    fig, ax = plt.subplots(figsize=(7, 4))
    for riso in (0.01, 0.33, 1.0):
        for rl in (32, 1e6):
            for cl in ("100p", "1n", "10n", "100n"):
                tag = f"riso{riso}_rl{'open' if rl > 1e5 else int(rl)}_cl{cl}"
                r = run("stab_" + tag, STAB.format(vin="", lfb="1e9", ct="1e9", vt=1,
                                                   riso=riso, rl=rl, cl=cl) + """
.control
ac dec 100 100 500meg
let t = -v(o)/v(inm)
let tdb = db(t)
let tph = 180/pi*cph(t)
meas ac fc when tdb=0 fall=1
meas ac ph find tph when tdb=0 fall=1
.endc
.end
""")
                s = run("step_" + tag, STAB.format(vin="pulse(0 0.1 1u 10n 10n 50u 100u)",
                                                   lfb="1n", ct="1f", vt=0, riso=riso, rl=rl, cl=cl) + """
.control
tran 2n 40u
meas tran vmax max v(out)
meas tran vfin find v(out) at=39u
wrdata out/step_""" + tag + """.txt v(out)
.endc
.end
""")
                over = max(0.0, (s["vmax"] - s["vfin"]) / s["vfin"] * 100)
                res[tag] = {"crossover_mhz": r.get("fc", float("nan")) / 1e6,
                            "phase_margin_deg": 180 + r["ph"] if "ph" in r else None,
                            "step_overshoot_percent": over}
                if rl > 1e5 and cl == "10n":
                    d = table(f"step_{tag}.txt")
                    ax.plot(d[:, 0] * 1e6, d[:, 1] * 1e3, label=f"Riso {riso} ohm")
    ax.set(xlabel="us", ylabel="mV", xlim=(0, 12), title="100 mV step, 10 nF cable, no headphone")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "buffer_step.png", dpi=130); plt.close(fig)
    RESULTS["buffer_stability"] = res


# --------------------------------------------------------------------------- protection
# Proposed (new, unbuilt) hardware DC/rail-fault detector driving the existing Q4/K1.
# Comparators are behavioural open-drain switches; the relay is a current-operated switch
# with worst-case catalog pickup/release levels and a 3 ms mechanical delay.
PROT = """* headphone DC / rail fault detector + relay driver
.param lcoil={lcoil} rl={rl} vth=0.1 offs={offs}
VAUX aux 0 5
VREF ref 0 2.5
* amplifier outputs and rails are stimulus here (fault injection)
BL ampl 0 V = {left}
BR ampr 0 V = 0
BVP vpos 0 V = {vpos}
BVN vneg 0 V = {vneg}
* per-channel DC sense: level shift to ref/2 and 0.3 Hz low-pass
RL1 ampl sl 470k
RL2 sl ref 470k
CLs sl 0 2.2u
RR1 ampr sr 470k
RR2 sr ref 470k
CRs sr 0 2.2u
* window references: 1.25 V +/- vth/2
BHI whi 0 V = 1.25 + vth/2
BLO wlo 0 V = 1.25 - vth/2
* rail monitors (trip if |rail| < 4.5 V)
RP1 vpos mp 100k
RP2 mp 0 100k
RN1 vneg mn 200k
RN2 mn ref 100k
.func od(p,m,node) {{ node/50 * 0.5*(1+tanh(4000*((m)-(p)+offs))) }}
* open-drain comparators pull FAULT_N low
B1 fn 0 I = od(v(whi), v(sl), v(fn))
B2 fn 0 I = od(v(sl), v(wlo), v(fn))
B3 fn 0 I = od(v(whi), v(sr), v(fn))
B4 fn 0 I = od(v(sr), v(wlo), v(fn))
B5 fn 0 I = od(v(mp), 2.25, v(fn))
B6 fn 0 I = od(0.1667, v(mn), v(fn))
RFN aux fn 1meg
CFN fn 0 1u
* gate comparator: gate may be high only if FAULT_N has recharged and the MCU asks
BREQ req 0 V = {req}
RG1 req gate 1k
RG2 gate 0 10k
B7 gate 0 I = od(v(fn), 2.5, v(gate))
* existing relay driver: U35 3 V, K1 coil, Q4, D13
VCOIL v3 0 3
RCOIL v3 c1 91
LCOIL c1 drain {{lcoil}} ic=0
M4 drain gate 0 0 fdn337 w=1 l=1
.model fdn337 nmos level=1 vto=0.7 kp=10 lambda=0.01 cgso=300p cgdo=50p
D13 0 drain smf12a
.model smf12a d(bv=14 ibv=1m rs=0.5 cjo=300p)
* relay contact: operate 26.4 mA, release 3.3 mA, 3 ms mechanical delay
BIC ic 0 V = i(VCOIL)*-1
RIC ic 0 1k
S1 st 0 ic 0 coilsw
.model coilsw sw(vt=14.85m vh=11.55m ron=1 roff=1e9)
VST s5 0 1
RST s5 st 1k
BSTN stn 0 V = 1 - v(st)
TD1 stn 0 dly 0 z0=1k td=3m
RTD dly 0 1k
S2 ampl hp dly 0 contact
.model contact sw(vt=0.5 vh=0.1 ron=0.1 roff=1e9)
RHP hp 0 {{rl}}
BPW pw 0 V = v(hp)*v(hp)/{{rl}}
"""


def protection():
    res = {}
    base = dict(lcoil=0.2, rl=32, offs=0, vpos="5", vneg="-5", req="3.3")
    fault_t = 4.0
    step = lambda v: f"time > {fault_t} ? {v} : 0"
    cases = {
        "startup_no_fault": dict(left="0"),
        "audio_20hz_4vpk": dict(left="4*sin(2*pi*20*time)"),
        "audio_10hz_4vpk": dict(left="4*sin(2*pi*10*time)"),
        "dc_fault_4v5_32ohm": dict(left=step(4.5)),
        "dc_fault_4v5_16ohm": dict(left=step(4.5), rl=16),
        "dc_fault_neg4v5": dict(left=step(-4.5)),
        "dc_fault_1v": dict(left=step(1.0)),
        "dc_fault_0v2": dict(left=step(0.2)),
        "dc_fault_4v5_offset+5mV": dict(left=step(4.5), offs=0.005),
        "dc_fault_4v5_coil_0H05": dict(left=step(4.5), lcoil=0.05),
        "dc_fault_4v5_coil_0H5": dict(left=step(4.5), lcoil=0.5),
        "neg_rail_lost": dict(left=step(4.0), vneg=f"time > {fault_t} ? 0 : -5"),
        "mcu_request_dropped": dict(left="0", req=f"time > {fault_t} ? 0 : 3.3"),
    }
    fig, axes = plt.subplots(3, 1, figsize=(7, 6.5), sharex=True)
    for name, over in cases.items():
        p = dict(base); p.update(over)
        tag = re.sub(r"[^a-z0-9]+", "_", name.lower())
        r = run("prot_" + tag, PROT.format(**p) + f"""
.options method=gear reltol=1e-4
.control
tran 20u 5.2 0 20u uic
meas tran t_close when v(dly)=0.5 cross=1
meas tran t_gate when v(gate)=0.7 fall=1 td={fault_t}
meas tran t_open when v(dly)=0.5 cross=2
meas tran vdrain_pk max v(drain)
meas tran e_hp integ v(pw) from={fault_t} to=5.2
meas tran closed_end find v(dly) at=5.19
wrdata out/prot_{tag}.txt v(hp) v(gate) i(VCOIL) v(sl)
.endc
.end
""", timeout=900)
        opened = r.get("t_open")
        res[name] = {
            "relay_closes_at_s": r.get("t_close"),
            "closed_at_end": r.get("closed_end", 0) > 0.5,
            "detect_ms": (r["t_gate"] - fault_t) * 1e3 if "t_gate" in r else None,
            "contact_open_ms_after_fault": (opened - fault_t) * 1e3 if opened else None,
            "energy_into_headphone_mj": r.get("e_hp", 0) * 1e3,
            "q4_drain_peak_v": r.get("vdrain_pk"),
        }
        if name == "dc_fault_4v5_32ohm":
            d = table(f"prot_{tag}.txt")
            t = (d[:, 0] - fault_t) * 1e3
            m = (t > -5) & (t < 25)
            axes[0].plot(t[m], d[m, 1]); axes[0].set_ylabel("headphone V")
            axes[1].plot(t[m], d[m, 3]); axes[1].set_ylabel("Q4 gate V")
            axes[2].plot(t[m], -d[m, 5] * 1e3); axes[2].set_ylabel("coil mA")
            axes[2].set_xlabel("ms after amplifier output jumps to +4.5 V DC")
            axes[0].set_title("DC fault: detect, release relay, disconnect (32 ohm)")
            for a in axes:
                a.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "protection_fault.png", dpi=130); plt.close(fig)
    RESULTS["protection"] = res


# --------------------------------------------------------------------------- enable logic
EN = """* auxiliary 5 V enable chain: P107 request, Q5 permission, U37 gate, U38 supervisor clamp
.param vdd=3.3
VSYS sys 0 pwl(0 0 1m 0 2m 3.8)
V33 v33 0 pwl(0 0 5m 0 7m 3.3 40m 3.3 40.2m 2.8 45m 2.8 45.2m 3.3 90m 3.3 95m 0)
VPERM permsrc 0 pwl(0 0 8m 0 8.1m 3.3 60m 3.3 60.1m 0 70m 0 70.1m 3.3)
* MCU pin: Hi-Z until 20 ms, then drives high, low at 80 ms, high again at 85 ms (stuck high)
VDRV drvctl 0 pwl(0 0 20m 0 20.01m 1)
VLVL lvl 0 pwl(0 1 80m 1 80.01m 0 85m 0 85.01m 1)
BP107 p107i 0 V = v(v33)*v(lvl)
SP p107i req drvctl 0 pin
.model pin sw(vt=0.5 vh=0.1 ron=50 roff=1e9)
R122 req 0 10k
* Q5 permission inverter
R120 permsrc g5 1k
R119 g5 0 1meg
M5 in2 g5 0 0 dmn2056 w=1 l=1
.model dmn2056 nmos level=1 vto=0.75 kp=8 cgso=300p cgdo=40p
R121 v33 in2 10k
* U37 SN74LVC1G97 as Y = IN1 AND NOT IN2, Schmitt inputs (typ 1.6/1.0 V), output follows VCC
.func schm(x, s) {{ 0.5*(1+tanh(40*((x) - (1.6 - 0.6*(s))))) }}
B1S s1 0 V = schm(v(req), v(s1f))
R1S s1 s1f 1k
C1S s1f 0 5p
B2S s2 0 V = schm(v(in2), v(s2f))
R2S s2 s2f 1k
C2S s2f 0 5p
BY yint 0 V = v(v33) * v(s1f) * (1 - v(s2f))
RY yint y 25
R123 y en 10k
R117 en 0 10k
CEN en 0 10p
* U38 TPS389001: SENSE divider 33k/20k, 1.15 V threshold, ~1.1 ms release, open-drain RESET on EN
R124 v33 sense 33k
R125 sense 0 20k
BOK ok 0 V = 0.5*(1+tanh(2000*(v(sense) - (1.156 - 0.006*v(okf)))))
ROK ok okf 1k
COK okf 0 100p
DCT ctd ok dfast
.model dfast d(rs=10 n=0.01)
RCT ok ctd 1k
CCT ctd 0 1.6u
BRST en 0 I = v(en)/100 * 0.5*(1-tanh(50*(v(ctd)-0.5))) * 0.5*(1+tanh(20*(v(sys)-1.5)))
"""


def enable_logic():
    r = run("enable_logic", EN + """
.control
tran 5u 100m
wrdata out/enable_logic.txt v(en) v(v33) v(req) v(permsrc) v(sys) v(sense)
.endc
.end
""")
    d = table("enable_logic.txt")
    t, en, v33, req, perm = d[:, 0], d[:, 1], d[:, 3], d[:, 5], d[:, 7]
    # allowed = supply valid for >1.6 ms, permission present, request high
    valid = v33 * 20 / 53 > 1.150
    allowed = valid & (perm > 0.75) & (req > 1.0)
    viol = (~allowed) & (en > 0.67)
    # thresholds are the model's own (U38 falling, Q5 Vto, U37 low); ignore 20 us around each edge
    edges = np.flatnonzero(np.diff(allowed.astype(int)) == -1)
    for e in edges:
        viol[(t >= t[e] - 20e-6) & (t < t[e] + 20e-6)] = False
    on = en > 0.83
    rel = t[np.flatnonzero((t > 45.2e-3) & on)[0]] - 45.2e-3 if np.any((t > 45.2e-3) & on) else None
    RESULTS["enable_logic"] = {
        "en_high_level_v": float(np.median(en[(t > 25e-3) & (t < 39e-3)])),
        "en_above_0v67_while_not_allowed_samples": int(np.count_nonzero(viol)),
        "en_max_before_request_v": float(en[t < 20e-3].max()),
        "en_max_during_brownout_v": float(en[(t > 40.4e-3) & (t < 45e-3)].max()),
        "release_after_brownout_ms": rel * 1e3 if rel else None,
        "en_max_during_final_collapse_v": float(en[t > 95e-3].max()),
    }
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for col, lab in ((3, "+3V3_MCU"), (7, "MAIN_RUN_PERMIT"), (5, "P107 request"), (1, "AUDIO_AUX_EN")):
        ax.plot(t * 1e3, d[:, col], label=lab, lw=2 if col == 1 else 1)
    ax.axhline(0.83, ls=":", c="k"); ax.axhline(0.67, ls=":", c="k")
    ax.set(xlabel="ms", ylabel="V", title="Auxiliary 5 V enable chain (dotted: U36 EN thresholds)")
    ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "enable_logic.png", dpi=130); plt.close(fig)


# --------------------------------------------------------------------------- class-AB heat
def classab_heat():
    """Ideal class-B arithmetic (docs: Pdc = 8*Vs*Ip/pi for stereo BTL). Not SPICE."""
    fig, ax = plt.subplots(figsize=(7, 4))
    out = {}
    for vs in (10, 12, 15, 18):
        vmax = 2 * (vs - 2.5)                      # differential peak with 2.5 V headroom per leg
        pmax = min(7.6, vmax ** 2 / 2 / 16)
        p = np.linspace(0.01, pmax, 200)
        ip = np.sqrt(2 * p / 16)
        heat = 8 * vs * ip / math.pi - 2 * p
        ax.plot(p, heat, label=f"+/-{vs} V rails")
        out[f"+/-{vs}V"] = {"max_w_per_ch": float(pmax), "worst_heat_w": float(heat.max()),
                            "at_w_per_ch": float(p[heat.argmax()])}
    ax.set(xlabel="output W per channel into 16 ohm (both channels)", ylabel="amplifier heat W",
           title="Ideal class-AB balanced stage: heat vs output (bias excluded)")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "classab_heat.png", dpi=130); plt.close(fig)
    RESULTS["classab_heat_ideal_16ohm"] = out


if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["quiet_chain", "stability", "protection", "enable_logic", "classab_heat"]
    for name in todo:
        print("running", name, flush=True)
        globals()[name]()
    (OUT / f"results_{'_'.join(todo)}.json" if sys.argv[1:] else OUT / "results.json").write_text(
        json.dumps(RESULTS, indent=1))
    print(json.dumps(RESULTS, indent=1))
