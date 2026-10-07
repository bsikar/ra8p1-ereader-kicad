# Unity composite common-mode and portable rail correction

2026-10-05, [YouTrack RA8HW-4](https://youtrack.locked.cv/issue/RA8HW-4)
and [RA8HW-18](https://youtrack.locked.cv/issue/RA8HW-18). Investigation only.

[TI OPA1656 SBOS901C](https://www.ti.com/lit/ds/symlink/opa1656.pdf), Rev C,
p6 specifies linear input common-mode V- through V+ minus 2.25V. Rail-to-rail
output does not imply rail-to-rail input. For the proposed independent unity
loops, the command is `Vbalanced_rms/sqrt(2)*(1+0.11/R)` including the two
four-way 0.22ohm ballast banks. Signal gain upstream does not remove this limit.

| Load ohm | Portable balanced Vrms | Command peak V | Minimum positive rail V |
| --- | --- | --- | --- |
| 16 | 2.828427 | 2.013750 | 4.263750 |
| 32 | 4.000000 | 2.838150 | 5.088150 |
| 50 | 4.000000 | 2.834650 | 5.084650 |
| 80 | 4.000000 | 2.832316 | 5.082316 |
| 150 | 4.000000 | 2.830501 | 5.080501 |
| 300 | 4.000000 | 2.829464 | 5.079464 |
| 600 | 4.000000 | 2.828946 | 5.078946 |

Retain the 4Vrms / 0.25Apeak / 0.5W/ch portable caps and investigate
**+/-6V bank rails**, replacing +/-5V. At 32ohms nominal positive CM margin
is 0.911850V. Converter tolerance/droop and hot BUF swing remain gates;
this is not a final regulator choice or guaranteed output envelope. Quiet
OPA1622 rails are a separate domain and are not changed by this correction.

Desktop command CM margins are 2.054255V at 16ohms/+/-10V, 1.722500V at
32ohms/+/-12V and 1.728000V at 50ohms/+/-14V. At 80/150/300/600ohms,
the 16Vrms/+/-14V target leaves only 0.420735/0.427995/0.432143/0.434217V.
Positive rail minimum, droop and upstream gain-stage CM must be included;
nominal margin is not permission to claim hot 16Vrms capability.

Sixteen BUF634A at 8.5mA plus twenty OPA1656 cores at 3.9mA give **2.568W
typical idle** at +/-6V. Stereo 0.5W/ch into 32ohms consumes 2.700949W in
the ideal Class-B output model. With 90% conversion and 3W other device
load, battery input is **8.854388W**, device heat **7.854388W** and an
assumed 17.76Wh usable pack lasts **2.005785h**. Ballast/circulation/dynamic
losses are excluded; this is an optimistic screen, not runtime acceptance.
Quiet listening must keep the whole bank off to pursue the long-runtime goal.
Hot bias, sealed-case steady heat and pack current still need closure.

## Recovery-test correction

P4 absolute input voltage is V- minus 0.5V through V+ plus 0.5V. The
historical +15V command at +/-12V exceeds that limit and is **invalid as a
recovery qualification test**, independent of its solver timeout. Historical
evidence is retained with that interpretation; it must not be repeated on
hardware. Phase-reversal protection does not grant overstress permission.

Two corrected +/-11V Gear cases stay within absolute input voltage limits.
-11V stays within linear CM; +11V deliberately exceeds the 9.75V positive
linear CM ceiling. Both timed out after 30 seconds. Clipping/recovery remains
UNKNOWN. This screen does not prove input current, fault safety or hot SOA.
Cases/results are in `audio_composite_overload_cases.json` and
`audio_composite_overload_results.json`. The harness now rejects commands
outside absolute input voltage before running the transient solver.

`python scripts/check_audio_composite_rails.py` reproduces all seven load
screens, desktop margins and energy math. Bench/circuit acceptance remains
separate from arithmetic and vendor macromodel processing.
