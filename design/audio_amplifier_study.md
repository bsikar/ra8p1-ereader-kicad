# Audio Stage 3: headphone amplifier alternatives and qualification envelope

2026-10-04 research checkpoint. **No amplifier topology or part is selected.**
This is a feasibility/architecture study following
[Stage 1](audio_stage1_requirements.md), not a circuit qualification or a
continuous output rating. No schematic, library, BOM, footprint or PDF changes
are made by this document. Existing OPA1622/INA1620 ideas and U34/K1 are WIP.
Firmware implementation is out of scope; hardware must provide the interfaces,
independent protection and deterministic mode-transition contracts.

The meaningful shortlist is (1) a precision amplifier with multiple integrated
buffers inside its feedback loop, (2) a precision amplifier with a discrete
Class-AB output stage, and (3) separate low-power IEM and high-current desktop
paths. A high-current current-feedback IC is another serious desktop comparator.
Class A and local error correction deserve evaluation but are not automatically
better. Stage 6 must compare these with the converter, power and enclosure study
before any final CAD changes.

## Electrical envelope and actual headphone cases

Screen balanced desktop output at **16 Vrms maximum, 0.707 Apeak maximum and
4 W/channel continuous maximum**, with 2 W/32 as the minimum architecture
objective. These are simultaneous limits, not three independent product claims.
Use `V = min(16, R*0.70710678/sqrt(2), sqrt(4*R))` and then apply actual hot
output swing, SOA, protection and thermal limits. Both legs carry full load
current and each sees an effective load of R/2 in symmetric BTL operation.

| Load ohms | Available Vrms | W/channel | Apeak | Ideal stereo heat on fixed +/-14 V rails, W | Maximum ideal heat over allowed amplitude, W |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 8.000 | 4.000 | 0.707 | 17.209 | 17.209 |
| 32 | 11.314 | 4.000 | 0.500 | 9.825 | 9.825 |
| 50 | 14.142 | 4.000 | 0.400 | 6.260 | 6.355 |
| 80 | 16.000 | 3.200 | 0.283 | 3.684 | 3.972 |
| 150 | 16.000 | 1.707 | 0.151 | 1.965 | 2.118 |
| 300 | 16.000 | 0.853 | 0.075 | 0.982 | 1.059 |
| 600 | 16.000 | 0.427 | 0.038 | 0.491 | 0.530 |

Heat uses ideal Class B, `Pdc/ch = 4*Vrail*Ipeak/pi`; output-stage stereo
heat is `2*(Pdc/ch-Pload/ch)`. Bias, converter loss, DAC, drivers, host/radio,
display and charging add heat. At 50 ohms and above, the dissipation maximum
occurs at 12.604 Vrms on +/-14 V, below the endpoint. A thermal test only at
clipping misses it. This table demonstrates that a fixed high-voltage rail is
an unattractive low-impedance operating mode, even when current capability is
ample. At the same 4 W/16, +/-8 V gives 6.405 W ideal stereo output-stage heat;
it is an illustrative lower-rail comparator, not proved 0.707 A hot swing.
For 16 Vrms BTL, each leg must swing 11.314 Vpeak. +/-14 V leaves 2.686 V
for stage/protection headroom before supply tolerance/droop. A device that
needs more headroom cannot meet it on these rails.

Lower-power IEM qualification extends to 8-9 ohms. Applying the desktop
current ceiling blindly to 9 ohms would produce 2.25 W/channel and 20.709 W
ideal stereo heat on +/-14 V: explicitly prohibit this in IEM mode. Rated
IEM voltage/current limits need independent hardware enforcement and must be
far below the high-power path. The 4 W cap also needs a real implementation:
an RMS/thermal limiter, load-aware voltage ceilings, or a conservatively rated
fixed envelope. Voltage and instantaneous current limits alone do not enforce
constant continuous power at every impedance.

Use equivalent sine peak-capacity screens of 100 dB, 105 dB, and 111 dB
(105 plus 6 dB EQ/sensitivity reserve), not recommended sustained listening
levels. Conversion from voltage sensitivity is `V=10^((L-Sv)/20)`; from
power sensitivity `P[mW]=10^((L-SmW)/10)`. Music crest factor, acoustic seal,
sample variation and frequency-dependent EQ prevent an SPL guarantee.

| Headphone and basis | 100 dB: Vrms / W | 105 dB: Vrms / W | 111 dB: Vrms / W / Apeak |
| --- | ---: | ---: | ---: |
| Original HE-6, velour pads, RAA conservative left-channel band average 89.0 dB/V, 43.3 ohms | 3.548 / 0.291 | 6.310 / 0.919 | 12.589 / 3.660 / 0.411 |
| Original Susvara, Stage 1 conservative measured screen 93.2 dB/V, 67.1 ohms | 2.188 / 0.0713 | 3.890 / 0.226 | 7.762 / 0.898 / 0.164 |
| HD800S, manufacturer 102 dB/V, 300 ohms | 0.794 / 0.00210 | 1.413 / 0.00665 | 2.818 / 0.0265 / 0.0133 |
| Original LCD-5, manufacturer 90 dB/mW, 14 ohms | 0.374 / 0.0100 | 0.665 / 0.0316 | 1.328 / 0.126 / 0.134 |
| SE846, manufacturer 114 dB/mW, 9 ohms | 0.0189 / 0.0000398 | 0.0337 / 0.000126 | 0.0672 / 0.000501 / 0.0106 |

The [original RAA HE-6 measurement](https://reference-audio-analyzer.pro/en/report/hp/hifiman-he-6.php)
identifies velour pads, HDM1/SF1 fixtures and channel-specific values. It is
**not HE6se or HE6se V2** and should not be relabeled as either. Using the less
sensitive channel is our conservative screen. The HE-6 case supports useful
margin beyond 8 Vrms: an 8 V ceiling misses the 111 dB reserve screen by about
3.94 dB. The 16 V /4 W envelope permits about 13.161 V at 43.3 ohms, providing
only about 0.39 dB beyond that reserve screen. It is broad coverage, not an
unlimited future-load promise. Additional EQ or low-frequency sensitivity
uncertainty can consume the reserve; qualification must use impedance curves
and frequency-specific measured sensitivity.

Other sources: [Susvara original RAA measurement](https://reference-audio-analyzer.pro/en/report/hp/hifiman-susvara.php),
[HD800S manufacturer specification](https://support.sennheiser-hearing.com/hc/en-us/articles/38273432554141-HD-800S-Specifications),
[LCD-5 manufacturer](https://www.audeze.com/products/lcd-5),
[SE846 manufacturer](https://www.shure.com/ja-jp/insights/all-about-se846-gen2-a-more-sophisticated-listening-experience).
Susvara/HD800S/SE846 inputs preserve Stage 1 provenance; this pass adds the
HE-6 measurement and original LCD-5 example. The LCD-5 source now describes
that model as legacy; future LCD variants must not inherit its electrical
specification. Electrostatic energizers and unusual near-zero-ohm ribbons
remain outside this conventional voltage-output headphone design.

## Serious amplifier comparators

Values below are manufacturer data under their stated conditions, not
complete-device measurements. A typical current, short-circuit rating, or
25 C waveform must never be treated as guaranteed low-distortion hot current.

| Candidate / function | Relevant source data | Fit and unresolved limits |
| --- | --- | --- |
| OPA1622 integrated audio driver | +/-2 to +/-18 V; 2.6 mA/core typical; 2.8 nV/sqrtHz at 1 kHz; +145/-130 mA typical drive/short-current scale; shutdown with reduced transients. | Strong low-power/IEM comparator, current alone inadequate for desktop. Input/feedback noise and hot swing still matter. |
| INA1620 integrated audio driver/resistor network | Same supply range and 2.6 mA/core typical; table labels +145/-130 mA **short-circuit** current. Matched resistors/EMI filtering add utility, not output watts. | Rail rating is not the blocker. Bare output paralleling is unacceptable; offset, sharing, stability and thermal limits require design. |
| OPA1656 + BUF634A composite | Actual manufacturer headphone reference; BUF634A +/-2.25 to +/-18 V, +/-250 mA continuous parameter; 1.5/8.5 mA typical low/wide-bandwidth bias. | Real scalable comparator; one buffer/leg cannot supply 0.354/0.5/0.707 Apeak. Parallel buffers and compensation must be proven. |
| Precision amplifier + LME49600 | Manufacturer closed-loop reference; 250 mA typical, 7.3/13.2 mA bias; +/-18 V ceiling. | Similar current-scaling issue and larger TO-263 footprint; higher idle burden than BUF634A comparator. |
| Precision amplifier + LMH6321 | 300 mA continuous subject to heat, programmable limit 10-300 mA, 11 mA typical bias, operating ceiling +/-16 V. | Useful current-limited composite comparator; needs multiple buffers for desktop. At +/-15 V, 300 mA sinking swing is only -10.3 V minimum at 25 C/-9.8 V hot, insufficient alone for 11.314 Vpeak per leg. |
| TPA6120A2 integrated current-feedback AB | +/-5 to +/-15 V recommended; 700 mA typical; 16 ohm recommended minimum load; 15 mA/core at +/-15 V; 10-100 ohm output resistor recommended. | Native reference conflicts with low output impedance. In BTL, 16 ohm headphones impose 8 ohm per leg, below recommended load. Needs new compensated implementation, thermal and noise evidence. |
| Precision amplifier + ADA4870 high-current CFB | 10-40 V supply, 1 A typical drive, 32.5 mA typical bias at +/-20 V; manufacturer composite example with ADA4637-1. | Serious desktop option with useful SOA documentation. Large idle burden, high input current noise, offset and loop compensation preclude adopting it as an IEM driver from its spot voltage-noise number. |
| OPA564 power amplifier/composite candidate | 7-24 V supply, 1.5 A, 39 mA typical bias; 102.8 nV/sqrtHz at 1 kHz; adjustable limit and thermal flag. | Direct IEM use is poor; +/-12 V ceiling gives too little guaranteed headroom for 16 Vrms BTL. A precision outer loop adds work and heat; not a leading portable comparator. |
| Precision amplifier + discrete AB emitter/source followers | Bias, transistor area and heatsinking can be chosen independently of signal gain. | Serious flexible option; must establish bias tracking, hot DC/pulsed SOA, second breakdown for BJTs, MOSFET linear-mode suitability, loop stability and manufacturing variation. More parts are justified only by measured envelope/energy benefit. |

Sources: [OPA1622 Rev B](https://www.ti.com/lit/ds/symlink/opa1622.pdf),
[INA1620 Rev B](https://www.ti.com/lit/ds/symlink/ina1620.pdf),
[OPA1656 composite, section 8.2.2](https://www.ti.com/lit/ds/symlink/opa1656.pdf),
[BUF634A Rev F](https://www.ti.com/lit/ds/symlink/buf634a.pdf),
[LME49600 Rev E](https://www.ti.com/lit/ds/symlink/lme49600.pdf),
[LMH6321 Rev D](https://www.ti.com/lit/ds/symlink/lmh6321.pdf),
[TPA6120A2 Rev B](https://www.ti.com/lit/ds/symlink/tpa6120a2.pdf),
[ADA4870 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/ada4870.pdf),
[OPA564 Rev E](https://www.ti.com/lit/ds/symlink/opa564.pdf).

At an optimistic 130 mApeak per leg, a BTL OPA1622/INA1620 channel has only
`Ipeak^2*32/2 = 0.270 W/32`. Even this is a calculation using typical limiter
scale, not a linear rating. Raising its rails does not solve current limits.
An illustrative six cores/leg would have 24 cores and substantial sharing,
noise, power and failure complexity. This is not a recommended six-core design.

The BUF634A composite reference uses the buffer in the OPA165x feedback loop;
wide-bandwidth mode is the reference condition for uncomplicated stability.
Changing to low-bias mode, adding buffers or switching gain invalidates an
assumption that that single-buffer reference proves our loop. Three buffers
per leg share 0.707 A as 0.236 A each ideally, leaving little sharing margin.
Twelve wide-mode buffers plus four OPA1656 cores on +/-14 V consume an
illustrative 3.293 W idle using typical currents, before the DAC. Low-bias
operation and/or power-gating a separate desktop bank therefore deserve
explicit comparison; no low-bias loop is qualified here. The
[BUF634A EVM schematics](https://www.ti.com/lit/pdf/SBOU256) provide a test
starting point, not a production solution; their default 50-ohm termination
must not be copied as a headphone source impedance.

Current-sharing ballast resistors, individual offsets and gain error must
be modeled. Never connect independently controlled outputs together simply
because they have the same nominal gain. A common precision loop around a
buffer bank with local ballast is distinct from independent amplifiers
fighting at a common output node. The summed current limit does not protect
one overloaded buffer if sharing is unequal or one device loses a rail.

Current-feedback describes an internal feedback topology, not a mandate to
drive headphones from a high-impedance current source. A conventional voltage
output with low impedance remains the required interface. The TPA6120A2
reference imposes specific feedback-resistor/stability constraints; reducing
its output resistor to meet our impedance budget needs simulation and bench
evidence. Its typical 0.9 uVrms output-noise headline is not a measured
20 Hz-20 kHz two-leg noise budget for our design.

ADA4870 supplies a precision-composite reference and SOA curves for a particular
board/heatsink at 25/85 C. Neither 1 A nor its 2.1 nV/sqrtHz voltage noise
at 100 kHz is a complete audio-band result. Four devices at +/-14 V using
32.5 mA as an illustrative bias consume 3.64 W idle; actual bias at those rails
needs measurement. Its inverting-input current noise and feedback resistors
matter. OPA564's guaranteed current/headroom, limiter overshoot and hot-current
derating also need examination if reconsidered; thermal shutdown is not an
acceptable normal operating cycle.

For discrete AB, [LT1166 manufacturer bias-system circuits](https://www.analog.com/media/en/technical-documentation/data-sheets/1166fa.pdf)
are one reproducible comparator: sense resistors set bias and current limit,
while an explicit compensated local loop controls external devices. This
does not establish IEM noise or eliminate hot SOA checks. Small sense resistors
reduce impedance but make current-limit/bias accuracy and layout important.
Generic switching MOSFET drain-current ratings do not establish linear SOA.
No output transistor has been selected.

Class A can avoid a crossover transition in its valid load/bias region; this
does not guarantee less total audible distortion than well-designed AB. The
Stage 1 illustrative four-leg 0.25 A bias on +/-10 V is 20 W idle, incompatible
with our portable energy allocation. Lower bias reduces the Class-A envelope.
Reject continuous high-power Class A as the default portable path unless a
quantified benefit outweighs that burden; an AB stage may remain Class A for
small signals without paying full-load Class-A idle power.

Implementable local error correction is a serious option.
[Cordell's original AES paper and circuit](https://www.cordellaudio.com/papers/MOSFET_Power_Amp.pdf)
demonstrate corrected output-stage distortion in a 50 W speaker amplifier.
The paper does not qualify a modern low-voltage headphone circuit. Its local
error/bias loop and main feedback loop require compensation, clipping recovery,
noise and hot stability analysis after rescaling. Composite global feedback
is another real way to reduce output-stage errors. Do not equate either with
a licensed THX design. [THX's primary description](https://www.thx.com/aaa)
identifies proprietary patented feed-forward technology; it provides no
qualified custom-board schematic in this study.
[Questyle's technology page](https://www.questyle.com/pages/technology)
is product/technology context, not a reproducible output-stage reference.
Neither brand proves an audible benefit over a transparent tested AB circuit.

## Noise, gain, volume, balanced and single-ended interfaces

The Stage 1 <=1 uVrms unweighted 20 Hz-20 kHz jack-noise objective corresponds
to 94 dB SNR at 50 mVrms; 0.5 uV gives 100 dB. Include DAC, I/V/filter,
attenuator, resistor Johnson noise, amplifier voltage/current noise, supplies,
switch leakage and RF demodulation. Measure active digital zeros, mute,
USB+PD+charging and Wi-Fi activity separately. A-weighted and unloaded SINAD
cannot substitute for this loaded low-level measurement.

Our flat-noise approximation with 2.8 nV/sqrtHz and two independent BTL legs
gives 0.560 uVrms at noise gain 1, 1.119 uV at 2 and 2.239 uV at 4, before
all other stages and 1/f noise. These are calculations, not device noise
guarantees. High gain can fail the IEM noise budget even with an excellent
amplifier. An inverting unity-signal-gain leg has noise gain 2; two unity-gain
voltage followers fed from a differential source have a different noise
budget. Do not sum all upstream noise as independent: some is correlated
between legs, and actual differential transfer determines cancellation.

Retain these candidates through Stage 6:

1. One scalable output stage, low/medium/high closed-loop gain and lower rails
   on battery; power-gated extra buffers in desktop mode. Advantage: fewer
   connector-routing stages. Risks: gain/buffer switches, compensation changes,
   leakage into disabled outputs, hot current sharing and high idle noise.
2. Optimized IEM stage plus separate high-power AB/composite path, both routed
   through qualified default-open disconnects. Advantage: high-current stage
   can be fully off for IEM listening. Risks: board area, selection contact
   resistance, charge injection, pop behavior and cross-path fault backfeed.
3. Shared precision front end, dedicated SE and four-leg balanced power stages,
   with explicit power-gating and independent protection. Advantage: both jack
   interfaces can have independent useful capability. Risks: greatest area and
   supply/control complexity; do not assume simultaneous outputs.

Use coarse analog gain/attenuation plus fine digital volume as a comparator.
An analog attenuator before the final amplifier reduces upstream noise but
does not reduce that amplifier's own noise. Large output-divider resistors
raise source impedance and make response dependent on IEM impedance. A
mechanical potentiometer's low-end matching is not assumed. Relay/resistor or
IC volume must prove <=0.1 dB channel error at 1-50 mV, transitions and contact
aging. Fail-open/stuck control states must not enable maximum gain.

A differential converter can feed a differential chain, but the SE interface
needs a defined derivation. One balanced leg gives half voltage and quarter
power at the same R only within its current/SOA limits. A differential-to-SE
stage followed by a dedicated amplifier is an alternative. Never short an
active negative leg to ground. A common-ground 3.5 mm return needs separate
high-current routing to avoid crosstalk; four output conductors remove that
shared cable return. Proper 2 V SE/4 V differential line outputs should have
their own buffer/level contract. Reusing a power stage requires line-load,
noise, stability and fixed-line/inserted-IEM mode-fault evidence.

## Hardware protection and continuous thermal qualification

Required hardware fault contract, to be closed before integration:

- Outputs default disconnected when unpowered, during reset and when logic
  control floats. Separate hardware healthy conditions must override MCU
  enable: all rails valid, no latched fault, safe temperature and DC state.
- Detect both differential DC and each conductor's DC relative to ground.
  Common-mode faults may cancel across a balanced transducer but remain
  hazardous during jack insertion or grounded adapter use. Monitor SE signals
  independently. Provide a fault latch and deliberate muted recovery.
- DC detection must reject normal 20 Hz bass without an excessive fault delay.
  Set threshold/filter/latency using permitted fault energy, not firmware
  convenience. Rail-loss and short/overcurrent paths need separate fast
  detection; a slow DC filter cannot serve every fault. Illustratively a
  14 V DC fault into 9 ohms for 5 ms delivers 0.109 J. This calculation does
  not assert that 5 ms is safe or that a selected relay can achieve it.
- Disconnect all four balanced output conductors and both SE signals. Check
  relay DC interruption/current rating, hot contact resistance/lifetime and
  coil release delay. A flyback diode can slow release; a clamp alternative
  must be designed from coil and transistor limits. Back-to-back MOSFET
  switches have their own distortion, Rds(on), SOA and fail-short fault model.
  K1's symbol or existing unfinished driver is not a safety qualification.
  Keep feedback defined while contacts are open: sensing only after a relay
  can leave a loop open and saturate the amplifier before reconnection. A DC
  servo may reduce normal offset but cannot replace independent fault removal.
- Current limits must include tolerance, short recovery and independent-leg
  faults, not just nominal sine current. Qualify cable shorts, mono/TRRS plugs,
  partial insertion, negative-to-ground adapter misuse, a grounded powered
  speaker input and hot-plug ESD. Device HBM ratings are not jack ESD ratings.
- Characterize input present with rails off, one rail absent, power loss,
  converter overshoot and output back-driving. Prevent inputs powering an
  inactive amplifier through clamps. Reference enable/flag levels to their
  actual supply domain; ground-referenced GPIO cannot be assumed compatible
  with negative-rail-referenced control pins.
- Mute and open disconnect before planned gain/rail/path changes; enable only
  after rail/offset settling. Forced PD loss must use an independent rail-good
  path and enough hold-up/release margin. Measure pops as voltage waveform and
  delivered load energy. Normal thermal operation must stay below shutdown,
  with battery and enclosure limits tighter than silicon survival limits.

Run both channels at loads 8/9/14/16/32/50/80/150/300/600 ohms, cable
capacitances and representative measured impedance curves. Determine steady
state (>=60 minutes and thermal equilibrium) at 25/35 C screens, both clipping
and maximum-dissipation amplitudes, charge on/off and weak/strong PD sources.
For each report rail ripple/droop, converter current, per-device temperature,
enclosure/battery temperature, limiting behavior, loaded THD+N and output
impedance over frequency. Steady-state thermal interfaces and sealed enclosure
area remain mechanical gates. No amp IC or reference board can waive them.

Independent original laboratory evidence:
[L7's Topping A90 report](https://www.l7audiolab.com/f/measurement-of-topping-a90-headphone-amp/)
describes measured 4.3 W/50 ohm balanced and 0.98 W/300 ohm balanced sweeps,
plus a 6.5 W/33 ohm balanced dashboard point with 110 dB SINAD; overload
protection interrupted output during testing. These are original electrical
measurements, not published hour-long enclosure thermal ratings. They show
that multiwatt low-distortion output is practical and protection behavior
affects power measurement; they do not prove our portable enclosure, topology
or 50 mV noise performance. Neither manufacturer headlines nor a short lab
sweep constitutes our continuous rating.

## Sourcing status and next decision gate

This is a candidate study, so no procurement or final BOM selection is implied.
Snapshot retrieved 2026-10-04; inventory is unreserved and may be cached:

| Candidate | Lifecycle evidence | Price/availability evidence and limitation |
| --- | --- | --- |
| OPA1622IDRCR | [TI ACTIVE](https://www.ti.com/product/OPA1622) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/OPA1622IDRCR/6553919): 4264 displayed, $7.43 quantity 1, $4.8432 quantity 100, cut tape; 20-week standard lead time displayed. Recheck exact suffix before purchase. |
| OPA1656 | [TI ACTIVE](https://www.ti.com/product/OPA1656) | OPA1656IDR shown as $2.99 related product on the same distributor page; exact stock/quantity quote not verified. |
| BUF634A | [TI ACTIVE](https://www.ti.com/product/BUF634A) | [Mouser BUF634AIDDAR](https://www.mouser.com/ProductDetail/Texas-Instruments/BUF634AIDDAR?qs=yqaQSyyJnNgwK76xZ3uCIA%3D%3D) search snapshot showed 635 and cut-tape option; price/full direct page could not be read reliably. Not a firm sourcing qualification. |
| LME49600, LMH6321, TPA6120A2, INA1620, OPA564 | Current TI pages ACTIVE | Exact suffix, small-quantity stock and unit quote pending; old datasheet date is not itself obsolescence. |
| ADA4870 | [ADI recommended for new designs](https://www.analog.com/en/products/ada4870.html) | Manufacturer 1ku starting list $12.66; not a one-unit distributor quote or stock commitment. |
| LT1166 | [ADI production](https://www.analog.com/en/products/lt1166.html) | Manufacturer 1ku starting list $3.39; external driver/output devices and precise small-quantity availability not selected. |

Stage 6 must compare measured/simulated IEM noise, loaded stability, low-level
matching, hot SOA, portable idle power, full-system heat, sourcing and complexity
for the three serious paths above. No final topology follows from this study.
If a common stage cannot meet the portable energy/noise allocations with a
stable low-power mode, the separate IEM/high-power path becomes substantially
more attractive despite extra area. If a discrete composite cannot outperform
an integrated buffer bank in the required envelope at defensible complexity,
the extra discrete circuitry is not justified by price or brand language.

Reproduce arithmetic with `python scripts/check_audio_amp_envelope.py`. It
checks the power cap, current/voltage envelope, independent heat-maximum sweep,
headphone screens and example idle/noise/fault-energy budgets. It is not SPICE,
a bench test, fault safety approval or evidence of production capability.
