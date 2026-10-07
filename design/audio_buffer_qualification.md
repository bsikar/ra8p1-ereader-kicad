# BUF634A candidate: pin-map and parallel sharing investigation

2026-10-05. Bounded Stage 7 investigation for
[RA8HW-4](https://youtrack.locked.cv/issue/RA8HW-4).
**HOLD: no parallel power bank or output rating is qualified.**

The project-local `Audio_Devices:BUF634AIDRBR` is an unplaced native KiCad
candidate derived from bundled `Amplifier_Buffer:BUF634AxDRB`.
The exact ordering code is the DRB VSON package; its footprint is deliberately
blank pending mechanical qualification. Preserve upstream attribution in
`libs/symbols/KICAD_LIBRARY_LICENSE.md`.

## Pin evidence and integration contract

Authority: [TI BUF634A SBOS948F](https://www.ti.com/lit/ds/symlink/buf634a.pdf),
Rev F, page 3, Figure 6-2 and Table 6-1. All nine pads occur once.

| Pad | Function | KiCad model |
| --- | --- | --- |
| 1 | BW | Input; mode selection requires stability qualification. |
| 2, 5, 8 | NC, no internal connection | Three separate hidden no-connect pins retained from upstream. |
| 3 | VIN | Input, displayed with conventional subscript. |
| 4 | V- | Power input. |
| 6 | VO | Output; conventional triangle retains an unnamed output pin. |
| 7 | V+ | Power input. |
| 9 | Exposed thermal pad, V- | Power input, explicitly renamed V- from THPAD. |

Pad 9 heat-spreading copper must connect to V-, including when the rail is
negative relative to system ground. It is not a ground pad. Package/thermal
acceptance and assembled-board heat spreading remain open.

## What the four-buffer arithmetic does and does not establish

Four buffers per leg would ideally divide a 0.707107 A peak load into
176.777 mA each. The earlier 25% allowance would raise one to 220.971 mA.
That is an assumed allowance, not evidence that these devices actually share.

For an elementary linear screen, each branch is a common driven source plus
an independent offset `e_i`, with series resistance `r_i`. KCL gives:

```
v = (sum(e_i/r_i) - Iload) / sum(1/r_i)
I_i = (e_i - v) / r_i
```

With equal `r`, this reduces to `I_i = Iload/4 + (e_i - mean(e))/r`.
The shared composite feedback changes the common drive to correct the summed
output; it does not separately null the differences between branch offsets.

Using a signed +/-65 mV offset screen, one positive and three negative offsets
give a 97.5 mV deviation from their mean. With illustrative 0.22 ohm ballast:

| Assumed total branch resistance | Worst branch at 0.707107 A load peak | Interpretation |
| --- | --- | --- |
| 5.22 ohms (5 ohm typical DC Rout plus ballast) | 195.455 mA | Optimistic linear approximation; not a guaranteed hot/current-dependent resistance. |
| 7.22 ohms (7 ohm typical DC Rout plus ballast) | 190.281 mA | Different operating-mode approximation; not proof of stability or sharing. |
| 0.22 ohms (external ballast only) | 619.959 mA | Sensitivity bound disproving qualification from ballast alone; not a prediction that a real current-limited BUF delivers this current. |

The ballast-only zero-load screen gives 443.182 mA circulating in the worst
branch. Real limits and nonlinearities change this result; therefore this
screen is a reason to investigate, not a device failure prediction.

The equal-resistance model needs at least **1.33154 ohms total branch resistance**
to keep that offset corner below the nominal 250 mA screen, or **2.20617 ohms**
to hold the assumed 25% imbalance. These are not proposed final ballast values.
If the first resistance came entirely from external ballast, the two BTL banks
would contribute about 0.66577 ohm before feedback and require additional
headroom, dissipation and loop-gain analysis. Common feedback can reduce the
load-facing impedance without eliminating circulating branch current.

`python scripts/check_audio_buffer_sharing.py` checks positive/negative load
peaks and zero load across 16 signed-offset corners and 16 +/-1% ballast corners.
Its KCL solver is checked against equal sharing, a two-source circulation
case, an unequal-resistor current divider and the independent analytic formula.
No undocumented guaranteed minimum Rout or hot offset bound is introduced.

## Datasheet limits and gates

The offset ceiling used above is from the 25 C electrical table. Typical drift
is characterized, without a full-temperature maximum usable for this proof.
The stated 250 mA drive and 5/7 ohm DC output resistances are typical entries;
the latter are measured at 10 mA. Do not extrapolate them into a guaranteed
linear resistance at 100–200 mA or near clipping.

The wide-bandwidth table at 25 C, +/-15 V and RL=100 ohms gives 2.0 V
typical / 2.2 V maximum headroom at 100 mA and 2.2 V typical / 2.5 V maximum
at 150 mA. These maxima are not guaranteed hot values. Hot swing, gain spread and converter droop still require
proof. Internal thermal shutdown is a fault feature, not a continuous thermal
rating. The [Stage 6 power budget](audio_architecture_selection.md) already
includes the substantial wide-bandwidth bank idle energy.

The manufacturer's composite examples establish a single-buffer starting
point. They do not establish a four-parallel bank in this implementation.
Do not treat global offset correction as independent branch control.

Before bank wiring, compare manufacturer-supported parallel arrangements,
separate closed-loop composite branches with ballast, and the discrete AB
fallback. Close hot offset/gain/current sharing, reactive headphone/cable
stability, compensation, clipping recovery, all-source noise, disconnected
load behavior and independent buffer faults. Then qualify sustained heat and
hardware disconnect response. No qualified simulation or bench proof has occurred.

The previously recorded distributor snapshot was 529 shown in stock and
$4.08 qty1 / $3.086 qty10 cut tape, not a reel-only minimum purchase:
[exact DigiKey ordering code](https://www.digikey.com/en/products/detail/texas-instruments/BUF634AIDRBR/13627165).
It is a dated, unreserved snapshot, not an availability guarantee or purchase.

This checkpoint adds a library asset and engineering evidence; it adds no
physical schematic component and does not change the native BOM.

## Separate-loop comparison and next circuit direction

2026-10-05 follow-up. Reject the original common-controller bank as the
implementation basis. Investigate **one unity-gain OPA1656/BUF634A composite
loop per buffer**, sensing that buffer's output **before its own ballast**.
Place any required signal gain upstream of the parallel loops. Four such
branches form each leg; four legs form the stereo BTL output. This is a
prototype direction, not approval to wire an electrically released bank.

Manufacturer basis:

- [TI SBOA127](https://www.ti.com/lit/an/sboa127/sboa127.pdf), pp4-6,
  explains independently controlled parallel outputs with nonzero ballast.
  Its THS3091 demonstration is not a headphone-bank reference; gain mismatch
  is explicitly outside that report's calculations.
- [OPA1656 SBOS901C](https://www.ti.com/lit/ds/symlink/opa1656.pdf), p24,
  establishes a single wide-bandwidth BUF composite. Its illustrated gain
  is 2. Unity operation, coupled parallel loops and reactive loads still
  require compensation/phase-margin verification in this implementation.
- [TI SBOA553A](https://www.ti.com/document-viewer/lit/html/SBOA553A/GUID-FD98F59B-E23C-4563-9D38-EF3E6AB3E2C6)
  establishes a leader/follower alternative for OPA593. It removes separate
  gain-divider matching, but adds a coupled master loop and leader-failure
  concerns. It is not a tested four-branch OPA1656/BUF circuit.

The own-output loop suppresses buffer offset through feedback instead of
assuming that nominal buffer Rout limits circulation. It leaves controller
offset and finite loop error; it does not make different branches identical.
Separate gain-2 loops also leave signal-dependent divider mismatch.

### Reproducible static sensitivity screen

Use an illustrative **+/-3mV total output-referred DC error allocation per
branch**, and 0.22 ohm ballast with **+/-1% total** resistance variation.
The controller's 25C +/-1mV offset and characterized 2uV/C drift limit give
2.4mV at noise gain 2 after a 100C change. The remainder is an allocation
for bias, supply/common-mode and finite-loop errors, not a guaranteed sum.
Neither hot input-bias limits nor actual composite loop gain have been closed.
Unity operation conservatively retains the same 3mV allocation.

For gain-2 comparison, use equal nominal 500-ohm feedback/gain resistors,
including their output current. [Vishay ACAS AT document 28770](https://www.vishay.com/docs/28770/acasat.pdf),
Rev15-Jun-2026, defines relative limits about a medial axis: +/-0.05% and
+/-5ppm/K are **per-element** matching/tracking limits, not the complete
RF/RG ratio limit. With 100K change, per-element error is 0.001; calculate
`G = 1 + (1+e)/(1-e)`, rather than silently halving mismatch. The separate
aged screen adds 0.00125 per element, the 8000h STANDARD-mode rated-load
relative-drift ceiling. It is a conservative combined sensitivity case,
not a lifetime prediction at 125C. [Vishay's explanation](https://www.vishay.com/docs/28194/incresarr.pdf)
also shows why temperature and aging cannot be excluded from divider analysis.
No exact array ordering code is selected or procurement-qualified here.

`check_audio_buffer_sharing.py` enumerates 4096 independent DC/gain/ballast
corners and positive/negative peak plus zero load for each four-branch case.
The source amplitude includes nominal ballast drop. Gain-divider current
is conservatively added in magnitude. The static external-ballast model
excludes AC loop mismatch, nonlinear drive, clipping and device faults.

| Load / investigated power | Gain 2 fresh branch peak | Gain 2 aged branch peak | Unity branch peak |
| --- | --- | --- | --- |
| 16 ohms / 4W | 244.733mA | 293.528mA | 199.999mA |
| 32 ohms / 4W | 210.488mA | 279.259mA | 147.442mA |
| 50 ohms / 4W | 200.775mA | 286.632mA | 122.065mA |
| 80 ohms / 3.2W | 181.311mA | 278.367mA | 92.334mA |
| 150 ohms / 1.707W | 147.758mA | 245.169mA | 58.838mA |
| 300 ohms / 0.853W | 128.796mA | 226.245mA | 39.698mA |
| 600 ohms / 0.427W | 119.352mA | 216.782mA | 30.128mA |

The gain-2 aged example exceeds the nominal 250mA comparison at several
loads; it is not an acceptable 4W bank proof. Its 2W/32 screen is 203.488mA.
Unity cells remove external gain-divider mismatch and divider current;
they do not remove finite bandwidth/phase differences between branches.
The roughly 200mA low-load result provides no margin below a 200mA design
allocation and does not convert typical 250mA into a guaranteed hot rating.
Hot SOA/swing proof must set the final load/rail ceiling or change the stage.

Four 0.22-ohm ballasts give nominal 0.055 ohm per leg, 0.11 ohm differential,
before contact, trace and closed-loop impedance. Keep feedback before the
disconnect. Ballast resistance, pulse/continuous rating and thermal drift
need exact parts. Opening one of four branches while retaining the full
0.707A envelope raises the unity screen to **257.098mA**. A failed branch
must trigger hardware shutdown/disconnect; continued operation is not rated.
A buffer stuck at a rail is a different, more severe fault absent from this
linear model. Independent DC/rail/current/temperature protection remains required.

### Energy and alternative disposition

The revised direction requires 16 precision loop cores rather than four.
Allocate four additional upstream gain cores until the signal chain is fixed:
16 BUF + 20 OPA cores yield **5.992W typical idle at +/-14V**, 5.136W at
+/-12V, 4.280W at +/-10V, and 2.140W at +/-5V. Mixed maximum-bias screening
is 8.176W at +/-14V; BUF's 25C maximum is not a full-temperature guarantee.
The quiet path keeps this whole bank off. Full-bank portable operation is
an inefficient candidate and cannot inherit the quiet-playback runtime.

The revised ideal power screen, retaining 90% conversion, 3W other loads,
4.55W charging and 10% margin, is 36.10W at 4W/16, 33.81W at 4W/32, and
33.61W at 4W/50. These exclude circulation, dynamic loop/ballast losses and
exact converter behavior. Weak host sources still derate charge/output.

| Approach | Disposition for this design |
| --- | --- |
| Common driver, open-loop BUF outputs | Rejected as the wiring basis: buffer offset sharing lacks a guaranteed bound. |
| Independent gain-2 composite branches | Static fresh screen is insufficient for the long-term 4W envelope with this illustrative array. Requires materially tighter complete ratio drift or calibration and its failure analysis. |
| Independent unity composite branches, upstream gain | First prototype investigation: removes external divider mismatch from sharing; costs sixteen loop cores and substantial idle power. Validate unity and coupled-loop stability before native bank wiring. |
| Composite leader/follower | Runner-up if shared gain or ballast compensation is needed. Transfer-function stability, startup and leader/follower faults require a specific four-branch design. |
| Single high-current IC per leg / discrete AB | Retain [Stage 3 alternatives](audio_amplifier_study.md). Integrated rail/noise/SOA tradeoffs and discrete bias/hot-SOA proof remain; revisit if unity-bank power/thermal burden is unacceptable. |

Next gate is a specific unity-cell compensation and fault-protection design,
followed by coupled-loop review and prototype measurement. A static screen
does not establish loaded THD+N, noise, continuous power or enclosure temperature.

### Nominal AC investigation, 2026-10-05: compensation hold

The direct own-output unity cell is **not ready for bank wiring**. A bounded
ngspice 46 shared-library investigation uses TI's unmodified
[OPA1656 PSpice package SBOMAW6](https://www.ti.com/lit/zip/SBOMAW6)
(library final 1.3, August 25, 2022) and
[BUF634A package SBOMB63](https://www.ti.com/lit/zip/SBOMB63)
(library Rev A, November 20, 2020). The separately obtained library hashes,
runtime/code-model hashes, generated netlists, warnings, DC operating points
and numerical results are in `audio_composite_ac_results.json`.
Vendor models/binaries are not redistributed. PSpice compatibility and seven
bundled ngspice code models, including xtradev's switch support, are required.

The test cell is OPA1656 driving BUF634A at +/-12V, feedback from its own
BUF output before a 0.22-ohm ballast, with 32 ohms and optional capacitance
after the ballast. A 32-ohm branch screen approximates four branches per leg
into 16 ohms BTL (N*R/2); it does not model the coupled four-loop bank.
The 10Hz closed-loop gain is 0.993173 because of the external ballast.
An AC source inserted between sense and inverting input gives the voltage
return-ratio approximation T=-V(sense)/V(fb). Downward 0dB crossings use
log-frequency interpolation with unwrapped phase; no crossover is not a pass.

| Added output capacitance | Approximate crossover | Apparent phase margin | Absolute closed-loop response peak |
| --- | --- | --- | --- |
| 0 | 18.7344MHz | 59.8578 degrees | 0.82157dB |
| 100pF | 19.8038MHz | 55.2696 degrees | 0.91413dB |
| 1nF | about 23.08MHz | about -17.8 degrees | 15.46dB |

These are small-signal nominal-model results, not measured bandwidth or
positive stability qualification. gmin=1e-10 and 1e-11 with rshunt=1e12
reproduce the warning. The initial 9505ab7 harness incorrectly archived a
separate `.op` solution before AC recomputed its bias. Those historical DC
values are superseded; they were not the operating points of the AC results.
The corrected harness uses `.options keepopinfo` and reads the retained `op1`
vectors from the AC run, as specified by the
[ngspice manual, DC/OP options](https://ngspice.sourceforge.io/docs/ngspice-43-manual.pdf).
In the corrected direct-feedback 1nF runs, AC output bias is -58.467mV
(closed) versus +16.402mV (injected) at gmin=1e-10, and +1.488mV versus
-57.133mV at gmin=1e-11. The numerical operating point is not trustworthy
enough to certify that phase margin or a physical oscillation frequency.
The severe peaking and negative apparent margin justify a compensation HOLD;
AC response around an unstable equilibrium is not normal playback behavior.

Additional model limitations remain unresolved: BUF's four-port model has
no BW-control terminal; TI's
[model support discussion](https://e2e.ti.com/support/amplifiers-group/amplifiers/f/amplifiers-forum/959097/buf634a-any-estimate-of-minimum-short-circuit-current-limit)
confirms the then-current model lacked power-adjust bandwidth control.
A bare-buffer reference circuit at 1V input, +/-12V and 1kohm gave about
1.19983V output, matching the package's included PSpice report. That result
cannot bound production offset against the datasheet's +/-65mV limit.
Likewise nominal modeled current limiting does not guarantee hot SOA,
thermal shutdown, maximum continuous current or output-device faults.

Reproduce the bounded screen with separately obtained models extracted into
one directory preserving `opa1656/OPA1656.LIB` and `buf634a/buf634a_a.lib`:

```sh
python scripts/investigate_audio_composite_ac.py --library <ngspice-shared-library> --code-models <existing-code-model-directory> --models <model-directory> --output <result.json>
```

The code-model directory must be free of whitespace for these ngspice
commands. NumPy is required. Each of twelve cases has a 30-second subprocess
limit; missing/changed models, vectors, model errors and hangs are never
hardware passes. Exit 0 means the investigation ran, **not** qualification;
timeouts/errors in workers produce UNKNOWN and exit 3. The committed result
normalizes only model include paths and runtime log text for portability.

The follow-up below investigates local high-frequency feedback from the precision amplifier
output through a capacitor, with resistive feedback from the buffer output,
as described in TI [SBOA065/AB101](https://www.ti.com/lit/an/sboa065/sboa065.pdf).
That older BUF634 application note is a compensation principle, not proof
for this modern bank. Include feedback-resistor noise/bias error, capacitor
tolerance, cable/connector parasitics, rail/startup corners, small/large-signal
steps, four-loop interaction and fault recovery. If model operating points
cannot be reconciled, use a bench prototype before trusting positive results.

The OPA1656IDR native library candidate has its eight-pin SOIC map checked
against [SBOS901C page 3](https://www.ti.com/lit/ds/symlink/opa1656.pdf), three
units rendered, and no footprint or schematic placement. FET inputs reduce
feedback bias-error sensitivity; 53MHz nominal GBW and 3.9mA typical per-core
bias motivate investigation, not final selection. OPA1612 and discrete AB
remain alternatives. +/-2.25V to +/-18V recommended rails and 5mA maximum
per-core hot bias constrain the power design; short-circuit headline current
does not qualify continuous drive. Exact sourcing/BOM fields and the complete
noise, hot-drive, thermal and protection comparison remain open before use.

### Local compensation and coupled-loop screen, 2026-10-05

**Investigation only; bank wiring and output ratings remain HOLD.**
The voltage-feedback arrangement from
[TI SBOA065/AB101](https://www.ti.com/lit/an/sboa065/sboa065.pdf), pp2-4,
uses Rf from each BUF output to its own OPA inverting input, and Cf from
that OPA output to the same inverting input. Feedback remains before each
0.22-ohm ballast. This creates a local high-frequency feedback path around
the precision amplifier. It is an old BUF634 principle, not a qualified
modern parallel headphone-bank reference.

`audio_composite_compensation_cases.json` defines 35 isolated runs, including
single cells and four independently controlled cells driving a shared
8-ohm-to-ground load at +/-12 V. That half-circuit load approximates one
leg of a 16-ohm BTL load; a grounded shunt capacitance does not reproduce
the complete floating headphone, other BTL leg or cable return paths.
4nF/40nF bus capacitances are deliberate stress cases, not measured cables.
Four-cell mismatch alternates +/-1% Rf/ballast and +/-5% Cf between cells;
this is one pattern, not exhaustive independent component/device corners.

For the coupled screen, four AC injections produce input-port matrix A and
returned-feedback matrix B at each frequency. With low input admittance,
`B = -L A` gives the approximate voltage return-ratio matrix `L = -B inv(A)`.
All four eigenmodes are followed across log frequency; the report archives
sampled mode traces. Individual injection columns are not scalar loop gains
and receive no standalone phase-margin claim. Frequency grids, finite data,
matrix conditioning and common retained AC bias are checked. A bias spread
over 1uV rejects the group. The reported maximum condition is about 17;
retained voltage bias is identical across each group's four columns.

| Rf / Cf | Bus capacitance | Weakest apparent modal margin | Absolute closed-loop peak |
| --- | --- | --- | --- |
| 100 ohms / 1nF | 4nF | 44.723 degrees | 4.345dB |
| 100 ohms / 1nF | 40nF | 64.069 degrees | 1.539dB |
| 1kohm / 47pF | 4nF | 71.461 degrees | 2.760dB |
| 1kohm / 47pF | 40nF | 82.677 degrees | 4.759dB |

The first row's conditional single-cell injection gives 61.760 degrees
while the four-port screen finds the weaker 44.723-degree mode. Checking
only one loop would miss this interaction. For 1kohm/47pF with 4nF,
all four crossings are at 16.302-17.480MHz; their apparent margins are
71.461-85.209 degrees. Repeating its closed and four injection runs at
gmin=1e-11 changes the weakest margin by less than 0.000001 degree and
the retained closed-loop output bias from 501.490 to 501.352uV.
The 100-ohm single-cell 1nF comparison is likewise reproduced at both gmin
values. Nodeset values are numerical starting hints, not forced DC supplies.
Convergence still falls back through failed stepping attempts; the warnings
are preserved. Consistent numerical roots are not physical DC guarantees.

The matrix reconstruction was also checked against an independent analytic
four-port example: `L = (8I + 2*ones)/(1+j*f/10000)`, with a deliberately
nonorthogonal excitation basis. Its three difference modes have gain 8 and
one common mode gain 16. Computed crossings match the closed-form
`10000*sqrt(gain^2-1)` within 0.003%, and phase margins within 0.002 degree.
A deliberately changed bias root is rejected. This verifies the matrix
arithmetic, not the TI macromodel or a generalized Nyquist stability proof.
Positive apparent margins alone do not establish all closed-loop poles,
physical parasitic/device corners, startup or large-signal stability.

Use **1kohm / 47pF as the next prototype compensation candidate**, not a
final network. Its MHz peaking is still material, particularly at 40nF;
improved modal margin does not automatically mean the flattest response.
At the nearest 20kHz sweep bin (19.953kHz), the two bus-capacitance runs give gains 0.993178/0.993205 and
phases -0.05105/-0.06518 degree. Their maximum branch-current deviation
from equal sharing is about 0.361mA per input volt. That includes unequal
ballast load sharing, not only zero-load circulating current. Scaling it
to 5.657Vpeak gives about 2.04mA in this linear nominal 16-ohm BTL screen;
it must not simply be substituted for the earlier independent DC-error bound.

The 1kohm resistor alone has about 4.07nV/sqrtHz thermal noise at 300K,
or 0.575uVrms integrated over 20Hz-20kHz before transfer-function shaping.
OPA1656's 25 C 20pA maximum input bias would contribute 20nV across it;
no corresponding guaranteed hot-bias ceiling has been established.
These numbers do not include buffer residual noise, upstream stages,
source impedance, supplies, EMI or correlated noise. Exact resistor and
C0G capacitor ordering codes, tolerance/drift and procurement remain open.

Current numerical evidence is `audio_composite_compensation_results.json`;
the direct comparison was regenerated in `audio_composite_ac_results.json`
with the corrected retained-bias method. Run the same bounded harness with:

```sh
python scripts/investigate_audio_composite_ac.py --library <ngspice-shared-library> --code-models <existing-code-model-directory> --models <model-directory> --cases design/audio_composite_compensation_cases.json --output <result.json>
```

Vendor models remain separately obtained and hash-checked. Code-model/runtime
hashes, generated circuits, warnings, actual AC bias and results are archived;
only include paths and irrelevant version-banner text are normalized.
No native component or wire is added by this study. Next run bounded small/
large-signal steps and clipping recovery, then include full BTL/reactive
loads, device spread/hot swing, parasitics and independent hardware fault
disconnect. The conditional 3mV DC allocation, hot SOA, complete noise and
sealed-enclosure thermal/power limits remain unresolved.

Follow-up [transient investigation](audio_composite_transient.md) retains all
fourteen pulse cases. Fast small pulses show 33.6–42.3% overshoot; slower
large pulses complete, but both overdrive/clipping attempts time out. Eight
complete waveforms do not resolve six UNKNOWN cases or qualify hot sharing,
full BTL, faults or continuous power. Bank wiring remains HOLD.

2026-10-05 correction: the portable composite-bank +/-5 V proposal is
superseded by an investigation of **+/-6 V**. OPA1656's positive input
common-mode ceiling is V+ minus 2.25 V; unity commands for 4 Vrms balanced
exceed that ceiling at +/-5 V. Quiet OPA1622 rails remain a separate domain.
The historical +15 V recovery command at +/-12 V exceeds absolute input
voltage and is invalid as qualification; two corrected +/-11 V cases
timed out, so recovery remains UNKNOWN. See [rail/common-mode correction](audio_composite_rails.md).
