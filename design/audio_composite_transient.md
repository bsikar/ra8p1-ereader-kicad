# Composite amplifier transient investigation

2026-10-05, [YouTrack RA8HW-4](https://youtrack.locked.cv/issue/RA8HW-4).
**UNKNOWN / HARDWARE HOLD. No bank wiring or continuous output rating accepted.**

The nominal [AC candidate](audio_buffer_qualification.md) now has bounded
pulse tests. Same separately obtained TI OPA1656/BUF634A models, ngspice 46
runtime and code-model hashes are in `audio_composite_transient_results.json`.
No proprietary models/binaries are committed. All fourteen original cases
are in `audio_composite_transient_cases.json`; failures are retained.

Each unity loop uses 1kohm feedback from its BUF output and 47pF local
feedback from OPA output, before 0.22ohm ballast, ideal +/-12V supplies.
Four-loop cases drive 8ohms to ground and 4nF/40nF shunt capacitance.
These are one-leg half-circuit screens for 16ohm BTL, without a floating
headphone/opposite leg, real cable, converter or hot device. Alternating
+/-1% Rf/ballast and +/-5% Cf is not exhaustive production/device spread.
Nodesets are numerical starting hints, not forced DC supplies.

## Results

Eight waveforms complete, five workers time out at 30 seconds, one aborts
with initial `fbnet3` timestep too small and zero rows. Gear completes cases
that trapezoidal integration cannot; this is not physical stability proof.
Failed dynamic-gmin/true-gmin/source-stepping warnings remain in evidence.

| Complete four-loop Gear case | Overshoot versus measured plateau | Settling after rise / recovery after fall | Maximum branch peak |
| --- | --- | --- | --- |
| 0.1V, 10ns edges, 4nF, maximum step 2ns | 33.5578% | 158.297ns / 157.664ns | 9.139mA |
| Same, 40nF | 42.2539% | 666.065ns / 667.545ns | 24.736mA |
| +5.695745V, 1us edges, 4nF | 0.7889% | 80.583ns / 78.322ns | 188.336mA |
| -5.695745V, 1us edges, 4nF | 0.8242% | 78.441ns / 79.347ns | 188.363mA |

Large pulses target +/-5.657V after ballast, with plateaus +5.657355V and
-5.656347V including approximately +0.504mV initial model bias. They last
only 5us: **not continuous 4W/ch**, hot sharing, clipping recovery or output
acceptance. Maximum branch deviations from equal sharing are 7.293/6.395mA
on positive/negative pulses, excluding independent device/DC corners. Typical
250mA datasheet drive is not a guaranteed hot rating.

Reducing the small 4nF pulse's maximum step from 2ns to 1ns changes overshoot
by 0.00849 percentage point and settling by 0.174ns. Shorter 0.7us pulses
repeat about 33.564% overshoot. Two single-cell trapezoidal cases complete
with 33.459% / 34.417% overshoot. Fast-edge overshoot remains material despite
positive apparent AC modal margins. Investigate actual reconstruction/input
bandwidth and compensation; slower favorable pulses do not qualify startup,
fast commands or faults.

The 15V overdrive test **times out with both trapezoidal and Gear integration**.
Clipping/recovery is UNKNOWN. No overload-recovery or bank-wiring acceptance
is inferred. If numerical convergence remains unresolved, prototype measurement
is required before trusting favorable nominal model results.

## Reproduction and checks

`investigate_audio_composite_ac.py` adds transient pulse mode, trap/Gear and
optional diagnostic logs. It rejects aborted, incomplete, nonfinite,
nonmonotonic or unresolved waveforms. Settling uses initial/late-plateau medians
and `max(10uV, 0.1% measured amplitude)` tolerance; negative pulses use signed
normalization. No recovery returns null, not zero. Full grids determine
metrics; downsampled archived traces (~800 points) can miss extrema in plots.

```sh
python scripts/investigate_audio_composite_ac.py --library <ngspice-shared-library> --code-models <existing-code-model-directory> --models <model-directory> --cases design/audio_composite_transient_cases.json --logs <scratch-log-directory> --output <scratch-result.json>
python scripts/check_audio_transient_metrics.py
```

Isolated workers have a 30-second bound. Exit 3/UNKNOWN indicates some cases
failed; exit 0 still means investigation only. Origin batch/index is retained.
Old timeout command paths are normalized to compact timeout records, and
the abort retains filtered original solver diagnostics. Numerical data is
unchanged. No failed case was silently removed.

The metric check independently supplies positive/negative exponential steps
with known `tau*ln(1000)` settling, persistent recovery error and truncation.
An unchanged AC case reproduces 2.759584dB peak, short Gear pulse reproduces
exactly, and latest abort detection rejects the known trapezoidal failure.
These validate processing/regressions, not macromodel authenticity.

Next close input bandwidth/compensation, clipping/startup, full BTL/reactive
and parasitic cases, independent hardware fault disconnect, hot SOA/swing/
sharing, noise/distortion and sealed-enclosure continuous thermal limits.
Retain discrete AB fallback if bank complexity/idle energy cannot be justified.
