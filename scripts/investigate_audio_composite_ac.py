#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded nominal-model investigation; never a hardware qualification gate.

Requires NumPy, an existing ngspice shared library and separately obtained TI
models. No vendor model or code-model binary is redistributed by this script.
Each case runs in an isolated process so a convergence hang becomes UNKNOWN.
"""
import argparse
import ctypes as ct
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

MODELS = {
    "opa1656/OPA1656.LIB": "9847ed60c62e792ee6f1c84899278a3c11ce71a6d21804bdd88f51199f1ba055",
    "buf634a/buf634a_a.lib": "63d75a17c849f6ac6fedf332a263505bff9a6b4d079237cfbe34d2ca4ba9a18a",
}
CODE_MODELS = ("analog", "spice2poly", "table", "xtradev", "xtraevt", "digital", "tlines")


def transient_summary(case, time, signals, branches):
    """Metrics for one finite pulse, relative to its measured initial/plateau levels."""
    stop, delay, rise, width, fall = (case[name] for name in
        ("stop_s", "delay_s", "rise_s", "width_s", "fall_s"))
    if (len(time) < 100 or time[0] != 0 or time[-1] < stop * 0.999999
            or not np.all(np.diff(time) > 0)
            or any(len(v) != len(time) or not np.all(np.isfinite(v)) for v in signals.values())):
        raise ValueError("Incomplete, nonfinite or nonmonotonic transient")
    initial = time < delay * 0.8
    plateau = (time > delay + rise + width * 0.8) & (time < delay + rise + width)
    high = (time >= delay + rise) & (time < delay + rise + width)
    recovery = time >= delay + rise + width + fall
    if any(np.count_nonzero(mask) < 10 for mask in (initial, plateau, high, recovery)):
        raise ValueError("Insufficient samples in pulse measurement windows")
    out = signals["out"]
    baseline, level = (float(np.median(out[mask])) for mask in (initial, plateau))
    delta = level - baseline
    if abs(delta) < 1e-6:
        raise ValueError("No resolved output pulse")
    direction = np.sign(delta)
    tolerance = max(1e-5, abs(delta) * 0.001)

    def settled_at(mask, reference, origin):
        selected = np.flatnonzero(mask)
        bad = selected[np.abs(out[selected] - reference) > tolerance]
        if len(bad) and bad[-1] == selected[-1]:
            return None
        return float(time[bad[-1] + 1] - origin) if len(bad) else float(time[selected[0]] - origin)

    currents = np.array([signals[f"vbranch{i}#branch"] for i in range(branches)])
    imbalance = currents - np.mean(currents, axis=0)
    ballast = 1 / sum(1 / (0.22 * (1 + ((-1 if i % 2 == 0 else 1) * 0.01
                        if case.get("component_mismatch") else 0))) for i in range(branches))
    ideal = baseline + case["amplitude_v"] * case.get("load_ohm", 32) / (
        case.get("load_ohm", 32) + ballast)
    sample = np.unique(np.r_[np.arange(0, len(time), max(1, len(time) // 800)), len(time) - 1])
    return {"baseline_v": baseline, "measured_plateau_v": level, "ideal_plateau_v": ideal,
            "plateau_error_v": level - ideal,
            "overshoot_percent": float(max(0, np.max(direction * (out[high] - level))) /
                                       abs(delta) * 100),
            "settling_tolerance_v": tolerance,
            "settling_after_input_rise_s": settled_at(high, level, delay + rise),
            "recovery_after_input_fall_s": settled_at(recovery, baseline, delay + rise + width + fall),
            "final_error_from_baseline_v": float(out[-1] - baseline),
            "maximum_branch_current_a": np.max(abs(currents), axis=1).tolist(),
            "maximum_branch_imbalance_a": np.max(abs(imbalance), axis=1).tolist(),
            "peak_output_abs_v": float(max(abs(out))),
            "sampled_time_s": time[sample].tolist(),
            "sampled_signals": {k: v[sample].tolist() for k, v in signals.items()}}


def worker(args, case):
    logs = []
    if args.diagnostic_log:
        args.diagnostic_log.write_text("", encoding="utf-8")
    callback_type = ct.CFUNCTYPE(ct.c_int, ct.c_char_p, ct.c_int, ct.c_void_p)
    exit_type = ct.CFUNCTYPE(ct.c_int, ct.c_int, ct.c_bool, ct.c_bool, ct.c_int, ct.c_void_p)

    @callback_type
    def output(message, _ident, _user):
        logs.append(message.decode(errors="replace"))
        if args.diagnostic_log:
            with args.diagnostic_log.open("a", encoding="utf-8") as stream:
                stream.write(logs[-1] + "\n")
        return 0

    @exit_type
    def controlled_exit(status, _immediate, _quit, _ident, _user):
        logs.append(f"controlled_exit={status}")
        return 0

    class Complex(ct.Structure):
        _fields_ = [("real", ct.c_double), ("imag", ct.c_double)]

    class Vector(ct.Structure):
        _fields_ = [("name", ct.c_char_p), ("type", ct.c_int), ("flags", ct.c_short),
                   ("real", ct.POINTER(ct.c_double)), ("complex", ct.POINTER(Complex)),
                   ("length", ct.c_int)]

    # Retain the directory handle while the DLL is loaded (Windows dependency resolution).
    dll_directory = os.add_dll_directory(str(args.library.parent)) if os.name == "nt" else None
    lib = ct.CDLL(str(args.library))
    lib.ngSpice_Init.argtypes = [ct.c_void_p] * 7
    lib.ngSpice_Command.argtypes = [ct.c_char_p]
    lib.ngSpice_Circ.argtypes = [ct.POINTER(ct.c_char_p)]
    lib.ngGet_Vec_Info.argtypes = [ct.c_char_p]
    lib.ngGet_Vec_Info.restype = ct.POINTER(Vector)
    if lib.ngSpice_Init(output, None, controlled_exit, None, None, None, None):
        raise RuntimeError("ngSpice_Init failed")

    def command(value):
        if lib.ngSpice_Command(value.encode()):
            raise RuntimeError(f"Command failed: {value}; {logs[-20:]}")

    def vector(name):
        pointer = lib.ngGet_Vec_Info(name.encode())
        if not pointer or pointer.contents.length <= 0:
            raise RuntimeError(f"Missing vector {name}; {logs[-20:]}")
        v = pointer.contents
        values = np.array([complex(v.complex[i].real, v.complex[i].imag)
                           for i in range(v.length)]) if v.complex else np.array(
                               [v.real[i] for i in range(v.length)])
        if not np.all(np.isfinite(values)):
            raise RuntimeError(f"Nonfinite vector {name}")
        return values

    for model in CODE_MODELS:
        path = (args.code_models / (model + ".cm")).as_posix()
        if any(char.isspace() for char in path):
            raise ValueError("Use a whitespace-free code-model directory for ngspice commands")
        command("codemodel " + path)
    command("set ngbehavior=ps")
    command("version")
    version_log = list(logs)
    if isinstance(case, list):
        case = dict(zip(("capacitance_f", "gmin", "mode"), case))
    cap, gmin, mode = (case[name] for name in ("capacitance_f", "gmin", "mode"))
    branches = case.get("branches", 1)
    rf, cf = case.get("feedback_r_ohm", 0), case.get("feedback_c_f", 0)
    load, rail = case.get("load_ohm", 32), case.get("rail_v", 12)
    mismatch = case.get("component_mismatch", False)
    seed = case.get("nodeset", False)
    if mode not in ("loop", "closed", "matrix", "transient") or branches not in (1, 4):
        raise ValueError("Supported cases: closed/loop/matrix/transient, one/four branches")
    if mode == "matrix" and (branches != 4 or case.get("injection_index") not in range(4)):
        raise ValueError("Matrix cases require four branches and injection_index 0..3")
    if bool(rf) != bool(cf):
        raise ValueError("Local feedback investigation requires both Rf and Cf")
    body = [f".options keepopinfo gmin={gmin} rshunt=1e12 itl1=500",
            f"Vin inp 0 dc 0 ac {1 if mode == 'closed' else 0}"]
    analysis = ".ac dec 200 10 1e9"
    if mode == "transient":
        amplitude, delay, rise, width, fall, stop, step = (case[name] for name in
            ("amplitude_v", "delay_s", "rise_s", "width_s", "fall_s", "stop_s", "max_step_s"))
        method = case.get("method", "trap")
        if (not all(np.isfinite(v) for v in (amplitude, delay, rise, width, fall, stop, step))
                or min(delay, rise, width, fall, step) <= 0 or amplitude == 0
                or stop <= delay + rise + width + fall or method not in ("trap", "gear")):
            raise ValueError("Invalid finite-pulse parameters")
        # OPA1656 SBOS901C p4: input absolute limits V- - 0.5 to V+ + 0.5.
        # Intentional common-mode overload is distinct from electrical overstress.
        if abs(amplitude) > rail + 0.5:
            raise ValueError("Command exceeds OPA1656 absolute input voltage limit; invalid recovery test")
        body[0] += f" method={method} reltol=1e-4"
        body[1] = f"Vin inp 0 dc 0 pulse(0 {amplitude} {delay} {rise} {fall} {width} {2*stop})"
        analysis = f".tran {step} {stop} 0 {step}"
    for index in range(branches):
        sense, drive, feedback = (f"{name}{index}" for name in ("sense", "drive", "fbnet"))
        injected = mode == "matrix" or (mode == "loop" and index == 0)
        inverse = f"fb{index}" if injected else feedback
        if injected:
            ac = 1 if index == case.get("injection_index", 0) else 0
            body += [f"Vtest{index} {inverse} {feedback} dc 0 ac {ac}"]
        direction = (-1 if index % 2 == 0 else 1) if mismatch else 0
        if rf:
            body += [f"Rf{index} {sense} {feedback} {rf * (1 + direction * 0.01):.12g}",
                     f"Cf{index} {drive} {feedback} {cf * (1 + direction * 0.05):.12g}"]
        else:
            body += [f"Vfeedback{index} {sense} {feedback} 0"]
        body += [f"Xop{index} inp {inverse} vp vn {drive} OPA1656",
                 f"Xbuf{index} {drive} {sense} vp vn BUF634A",
                 f"Vbranch{index} {sense} branch{index} 0",
                 f"Rb{index} branch{index} out {0.22 * (1 + direction * 0.01):.12g}"]
        if seed:
            body += [f".nodeset v({drive})=-0.2 v({sense})=0.00049 "
                     f"v({feedback})=0.00049" +
                     (f" v({inverse})=0.00049" if injected else "")]
    body += [f"Rload out 0 {load}"]
    if cap:
        body += [f"Cl out 0 {cap}"]
    lines = ["OPA1656 BUF634A own-output unity cell: nominal investigation",
             *[f'.include "{(args.models / path).as_posix()}"' for path in MODELS],
             f"Vp vp 0 {rail}", f"Vn vn 0 {-rail}", *body, analysis, ".end"]
    circuit = (ct.c_char_p * (len(lines) + 1))(*[line.encode() for line in lines], None)
    if lib.ngSpice_Circ(circuit):
        raise RuntimeError(f"Circuit load failed: {logs[-20:]}")
    command("run")
    errors = [line for line in logs if any(word in line.lower() for word in
              ("error", "controlled_exit=", "simulation(s) aborted", "timestep too small"))]
    if errors:
        raise RuntimeError(str(errors))
    if mode == "transient":
        names = ["inp", "out", "vp#branch", "vn#branch"] + [
            f"{name}{i}" for i in range(branches) for name in ("drive", "sense", "fbnet")]
        names += [f"vbranch{i}#branch" for i in range(branches)]
        return {"case": case, "mode": mode,
                "transient": transient_summary(case, vector("time").real,
                    {name: vector(name).real for name in names}, branches),
                "netlist": lines, "runtime_log": version_log,
                "warnings": [line for line in logs if "warning" in line.lower()],
                "solver_log": [line for line in logs if any(word in line.lower() for word in
                    ("linear solver", "stepping", "op finished", "data rows"))]}
    # KEEPOPINFO retains the actual AC bias solution. A separate .op could
    # converge to another root and must not be reported as the AC bias point.
    op_names = ["out", "vp#branch", "vn#branch"] + [
        f"{name}{index}" for index in range(branches)
        for name in ("drive", "sense", "fbnet")]
    op = {name: vector("op1." + name).real.tolist() for name in op_names}
    f = vector("frequency").real
    h = -vector("fbnet0") / vector("fb0") if mode == "loop" else vector("out")
    if (len(f) != len(h) or len(f) != 1601 or not np.all(np.diff(f) > 0)
            or not np.all(np.isfinite(h)) or not np.all(abs(h) > 0)):
        raise RuntimeError("Incomplete or nonmonotonic AC sweep")
    db = 20 * np.log10(np.abs(h))
    phase = np.unwrap(np.angle(h)) * 180 / np.pi
    crossings = []
    if mode == "loop":
        for i in np.where((db[:-1] >= 0) & (db[1:] < 0))[0]:
            fraction = -db[i] / (db[i + 1] - db[i])
            crossings.append({"frequency_hz": float(10 ** (np.log10(f[i]) + fraction *
                              np.log10(f[i + 1] / f[i]))),
                              "phase_margin_deg": float(180 + phase[i] + fraction *
                                                        (phase[i + 1] - phase[i]))})
    audio_index = int(np.argmin(abs(f - 20000)))
    currents = [vector(f"vbranch{index}#branch")[audio_index] for index in range(branches)]
    imbalance = [current - sum(currents) / branches for current in currents]
    result = {"case": case, "capacitance_f": cap, "gmin": gmin, "mode": mode, "operating_point": op,
            "gain_at_10hz": float(abs(h[0])), "peak_db": float(max(db)),
            "gain_at_20khz": float(abs(h[audio_index])),
            "phase_at_20khz_deg": float(phase[audio_index]),
            "peak_frequency_hz": float(f[int(np.argmax(db))]),
            "branch_20khz_a_per_v": [[float(v.real), float(v.imag)] for v in currents],
            "imbalance_20khz_a_per_v": [float(abs(v)) for v in imbalance],
            "downward_crossings": crossings, "netlist": lines,
            "warnings": [line for line in logs if "warning" in line.lower()],
            "runtime_log": version_log}
    if mode == "matrix":
        # A column excitation is not a scalar loop gain, nor a playback input.
        # Publish only its matrix data and actual bias point, not spurious
        # scalar margins (unexcited closed ports have fbnet/fb == 1).
        for key in ("gain_at_10hz", "peak_db", "gain_at_20khz", "phase_at_20khz_deg",
                    "peak_frequency_hz", "branch_20khz_a_per_v",
                    "imbalance_20khz_a_per_v", "downward_crossings"):
            del result[key]
        result["matrix_vectors"] = {
            "frequency": f.tolist(),
            "input": [[[float(v.real), float(v.imag)] for v in vector(f"fb{i}")]
                      for i in range(branches)],
            "returned": [[[float(v.real), float(v.imag)] for v in vector(f"fbnet{i}")]
                         for i in range(branches)]}
    return result


def matrix_summary(rows):
    """Return-ratio matrix from simultaneous voltage-port injections.

    B = -L A, where A and B are input and returned-feedback voltage matrices.
    Low input admittance is assumed. This is still a nominal-model screen.
    """
    if len(rows) != 4 or sorted(r["case"]["injection_index"] for r in rows) != list(range(4)):
        raise ValueError("Four complete injection cases required")
    rows = sorted(rows, key=lambda r: r["case"]["injection_index"])
    f = np.array(rows[0]["matrix_vectors"]["frequency"])
    if any(not np.array_equal(f, r["matrix_vectors"]["frequency"]) for r in rows):
        raise ValueError("Matrix sweep frequencies disagree")
    # Linear columns must describe the same bias point, not distinct roots.
    bias_spread = max(np.ptp([r["operating_point"][name][0] for r in rows])
                      for name in rows[0]["operating_point"] if "#branch" not in name)
    if not np.isfinite(bias_spread) or bias_spread > 1e-6:
        raise ValueError("Matrix columns disagree in AC bias; review convergence")
    def unpack(name):
        values = np.array([r["matrix_vectors"][name] for r in rows])
        # columns are excitation sources; rows are feedback ports.
        return (values[..., 0] + 1j * values[..., 1]).transpose(2, 1, 0)
    a, b = unpack("input"), unpack("returned")
    condition = np.linalg.cond(a)
    if not np.all(np.isfinite(condition)) or max(condition) > 1e9:
        raise ValueError("Ill-conditioned input-voltage matrix; no trustworthy loop result")
    loops = -np.matmul(b, np.linalg.inv(a))
    eigen = np.linalg.eigvals(loops)
    # Track modes by nearest complex value in log frequency; degenerate modes
    # are exchangeable. Archive sampled traces so the tracking can be reviewed.
    permutations = list(itertools.permutations(range(4)))
    for i in range(1, len(f)):
        order = min(permutations, key=lambda p: float(np.sum(abs(eigen[i, p] - eigen[i - 1]))))
        eigen[i] = eigen[i, order]
    if not np.all(np.isfinite(eigen)) or not np.all(abs(eigen) > 0):
        raise ValueError("Invalid return-ratio eigenvalues")
    db = 20 * np.log10(abs(eigen))
    phase = np.unwrap(np.angle(eigen), axis=0) * 180 / np.pi
    # Normalize low-frequency negative-feedback modes around zero degrees.
    phase -= np.round(phase[0] / 360) * 360
    crossings = []
    for mode in range(4):
        for i in np.where((db[:-1, mode] >= 0) & (db[1:, mode] < 0))[0]:
            x = -db[i, mode] / (db[i + 1, mode] - db[i, mode])
            crossings.append({"mode": mode, "frequency_hz": float(10 ** (np.log10(f[i]) + x *
                              np.log10(f[i + 1] / f[i]))), "phase_margin_deg": float(180 +
                              phase[i, mode] + x * (phase[i + 1, mode] - phase[i, mode]))})
    sample = np.arange(0, len(f), 40)
    return {"case": {k: v for k, v in rows[0]["case"].items() if k != "injection_index"},
            "maximum_voltage_bias_spread_v": float(bias_spread),
            "maximum_matrix_condition": float(max(condition)), "downward_crossings": crossings,
            "sampled_frequency_hz": f[sample].tolist(), "sampled_mode_db": db[sample].tolist(),
            "sampled_mode_phase_deg": phase[sample].tolist()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--code-models", type=Path, required=True)
    parser.add_argument("--models", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cases", type=Path, help="JSON list of explicit investigation cases")
    parser.add_argument("--logs", type=Path, help="Optional directory for worker convergence logs")
    parser.add_argument("--diagnostic-log", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    for attribute in ("library", "code_models", "models"):
        setattr(args, attribute, getattr(args, attribute).resolve())
    for relative, expected in MODELS.items():
        if hashlib.sha256((args.models / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Model hash mismatch: {relative}; review changed model before use")
    if args.worker:
        print(json.dumps(worker(args, json.loads(args.worker)), allow_nan=False))
        return 0
    if args.output is None:
        parser.error("--output required for investigation")
    report = {"status": "INVESTIGATION ONLY; HARDWARE HOLD", "model_sha256": MODELS,
              "library_sha256": hashlib.sha256(args.library.read_bytes()).hexdigest(),
              "code_model_sha256": {name: hashlib.sha256(
                  (args.code_models / (name + ".cm")).read_bytes()).hexdigest()
                  for name in CODE_MODELS},
              "bias_method": "AC: retained op1 via keepopinfo; transient: initial waveform sample",
              "cases": []}
    cases = json.loads(args.cases.read_text()) if args.cases else [
        (cap, gmin, mode) for gmin in (1e-10, 1e-11)
        for cap in (0, 1e-10, 1e-9) for mode in ("closed", "loop")]
    if args.logs:
        args.logs.mkdir(parents=True, exist_ok=True)
    for index, case in enumerate(cases):
        command = [sys.executable, str(Path(__file__).resolve()), "--library", str(args.library),
                   "--code-models", str(args.code_models), "--models", str(args.models),
                   "--worker", json.dumps(case)]
        if args.logs:
            command += ["--diagnostic-log", str(args.logs.resolve() / f"case-{index:03}.txt")]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30,
                                    check=True)
            report["cases"].append(json.loads(result.stdout))
        except subprocess.TimeoutExpired:
            report["status"] = "UNKNOWN; HARDWARE HOLD"
            report["cases"].append({"case": case, "error": "Worker exceeded 30-second limit",
                                    "error_kind": "timeout", "timeout_s": 30})
        except (subprocess.CalledProcessError, ValueError) as exc:
            report["status"] = "UNKNOWN; HARDWARE HOLD"
            report["cases"].append({"case": case, "error": str(exc),
                                    "stderr": getattr(exc, "stderr", None)})
    groups = {}
    for row in report["cases"]:
        if "matrix_vectors" in row:
            key = json.dumps({k: v for k, v in row["case"].items() if k != "injection_index"},
                             sort_keys=True)
            groups.setdefault(key, []).append(row)
    report["matrix_results"] = []
    for rows in groups.values():
        try:
            report["matrix_results"].append(matrix_summary(rows))
        except ValueError as exc:
            report["status"] = "UNKNOWN; HARDWARE HOLD"
            report["matrix_results"].append({"error": str(exc)})
        for row in rows:
            del row["matrix_vectors"]
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(report["status"])
    for case in report["cases"]:
        print({key: value for key, value in case.items()
               if key in ("case", "peak_db", "downward_crossings", "error")})
        if "transient" in case:
            print({key: value for key, value in case["transient"].items()
                   if not key.startswith("sampled_")})
    for matrix in report["matrix_results"]:
        print({key: value for key, value in matrix.items()
               if key in ("case", "maximum_matrix_condition", "downward_crossings", "error")})
    return 3 if report["status"].startswith("UNKNOWN") else 0


if __name__ == "__main__":
    sys.exit(main())
