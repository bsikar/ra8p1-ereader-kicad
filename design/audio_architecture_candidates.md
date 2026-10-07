# Audio architecture study: Stage 2 conversion and analog alternatives

2026-10-04. Research checkpoint; **no architecture or component is selected**.

This record applies the owner-approved scope in
[Stage 1](audio_stage1_requirements.md): own-server streaming, hardware work,
quiet IEMs, conventional demanding headphones, 3.5 mm SE / 4.4 mm balanced,
proper line output, and portable plus USB-PD desktop operation. All existing
e-reader/camera/illumination/speaker/wet-port requirements remain. Initial
10-hour local / 8-hour streaming allocations mean that audio idle consumption
matters even when headphone output is only milliwatts. The 2 W/32-ohm floor,
4 W stretch, current/power limits, and possible 16 Vrms high-impedance mode
are amplifier requirements; none requires a particular DAC brand.

Detailed CAD remains behind the Stage 6 selection gate. This document makes
no schematic/library/BOM changes and does not qualify existing U34/K1.
Stage 3 owns the final amplifier comparison; Stage 5 owns the power tree.

## 1. Evidence and comparison discipline

DAC DNR, SNR and THD+N below are manufacturer typical claims under their
specified conditions, not complete-player measurements. Different output
levels, weighting, bandwidths and reference circuits prevent a direct
leaderboard. Minimum/maximum limits must replace typical values at component
qualification. Mono summing can improve uncorrelated noise by approximately
3 dB but doubles converter resources; it does not automatically remove
correlated reference or digital noise, distortion or headphone-amplifier hiss.

| Family screened | Useful evidence | Consequence for this product |
| --- | --- | --- |
| ESS ES9039Q2M | Current public v0.2.3, differential outputs, 130 dBA DNR, -120 dB THD+N at 48 kHz on a **10 Vrms evaluation output**; 54/64/78 mW typical active power in the documented clock modes. | Strong portable conversion candidate. The 10 V reference result is not a promise of -120 dB at 2 V or at the headphone jack. Current/voltage-mode possibilities need an explicit front-end comparison. |
| AKM AK4497S | Differential voltage output; 129 dB SNR / -117 dB THD+N at 2 Vrms; 131 dB / -113 dB at 2.7 Vrms. | Serious current-generation alternative with less external I/V work, but increasing output does not improve every performance metric. |
| AKM AK4499EX + AK4191 | Separated digital modulator and switched-resistor analog DAC; 135 dBA stereo / -124 dB THD+N under its documented reference conditions. | Serious maximum-performance comparator with extra chips, reference load and I/V work. It is a noise-shaped multibit architecture, not a conventional NOS binary ladder. |
| Cirrus CS43198 | Pseudodifferential voltage outputs, 130 dBA / 127 dB unweighted DNR, -115 dB typical PCM THD+N, 0.55 uVrms A-weighted idle noise under its table conditions. | Serious low-power comparator; balanced-at-conversion needs more than one stereo chip or a downstream phase splitter. |
| TI PCM1792A | Advanced Segment differential current output; 127 dB stereo DNR at 2 V, 129 dB at 4.5 V; 0.0004% THD+N. | Mature, documented 192 kHz alternative; do not confuse its 132 dB high-voltage mono condition with normal stereo performance. |
| ADI AD1955 | Multibit delta-sigma, differential current output; 120 dBA stereo DNR, -110 dB THD+N; production status. | A viable mature baseline, not evidence of a performance/power advantage over the newer parts. |
| TI DAC11001B | Precision 20-bit R-2R, external bipolar reference/buffer, SPI rather than native I2S. | A reproducible ladder comparator exists; the conversion interface, reference, filtering and dynamic settling are substantial system work. |

Sources: [ESS current DAC lineup](https://www.esstech.com/products-overview/digital-to-analog-converters/sabre-audiophile-dacs/),
[ES9039Q2M v0.2.3 datasheet](https://www.esstech.com/wp-content/uploads/2026/05/ES9039Q2M_Datasheet_v0.2.3.pdf),
[AK4497S product](https://www.akm.com/us/en/products/audio/audio-dac/ak4497svq/),
[AK4499EX datasheet](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4499exeq/ak4499exeq-en-datasheet-myakm.pdf),
[CS43198 datasheet](https://statics.cirrus.com/pubs/proDatasheet/CS43198_DS1156F2.pdf),
[PCM1792A product](https://www.ti.com/product/PCM1792A),
[AD1955 product](https://www.analog.com/en/products/ad1955.html),
[DAC11001B datasheet](https://www.ti.com/lit/ds/symlink/dac11001b.pdf).

These sources establish candidate plausibility, not an audible brand
signature. No evidence reviewed establishes that matched linear DACs with
equivalent filtering, levels and noise have an inherent ESS/AKM/Cirrus/ladder
sound. A sonic claim needs controlled level-matched listening evidence;
electrical faults, response differences and hiss remain testable engineering
differences.

## 2. Four serious conversion-to-output architectures

The branches below share the same RA8P1/C6 hardware study and asynchronous
USB clock-domain contract. A separate USB bridge remains a Stage 4 option.
All require independent hardware mute/DC/overcurrent/thermal protection,
clock/rail-loss handling, source/gain detection and a fail-safe connector
mode interlock. Line buffers branch before the power headphone amplifier.
Do not connect a balanced negative conductor to ground for SE or line use.

### A. Low-power ESS differential current-conversion path

`Audio clock domain -> one ES9039Q2M -> four low-noise I/V cells ->`
`differential reconstruction/filter -> matched analog gain/attenuation ->`
`four power-amplifier legs -> four-pole disconnect -> 4.4 mm`.

A parallel high-impedance branch feeds dedicated balanced line buffers at
4 Vrms differential. A precision differential-to-SE stage supplies 2 Vrms
line and a separate low-noise SE/IEM headphone stage. Simultaneous use stays
conditional on loading, power and safe mode control; nothing connects a
power output directly to a ground-referenced line input.

The I/V option keeps DAC output nodes near an appropriate fixed bias, with
common-mode removal in the differential filter. The alternative is to use
the DAC as a voltage source into a high-impedance differential filter,
avoiding I/V stages. Screen both on loaded linearity, output-node common
mode, noise, output resistance, capacitance and out-of-band behavior. The
datasheet's 390-ohm typical per-pin output impedance is not a headphone
output impedance or justification for directly driving a jack.

Complete-chain benefit: modest DAC-core energy and genuine differential
conversion with one chip. Cost: I/V/filter bias consumption and feedback
stability; adding more op-amps can erase the core's power advantage. Large
MCLK, supply sensitivity and clock-mode transitions need qualification.
Stage 7 must choose transimpedance resistors from actual current swing,
allowable DC/common mode and hot amplifier output headroom, then compensate
DAC/input capacitance and verify loop gain. No old resistor network is
approved by this study.

### B. AKM voltage-output path, with a high-performance two-chip variant

**B1:** `Audio clock domain -> one AK4497S -> differential voltage LPF /`
`common-mode translation -> matched attenuation/gain -> protected BTL amp`.

Dedicated differential line buffers and a differential-to-SE line/IEM
branch preserve the same output contracts as A. This removes the four
current-conversion cells; it does not remove reference decoupling, active
filtering, common-mode control, volume or output protection. Keep the two
signal phases rather than collapsing to SE and recreating them for 4.4 mm.

The manufacturer's normal-load table gives 60 mA on the combined 5 V
analog rails, 1 mA per reference, 1 mA AVDD and 7/18 mA TVDD at
44.1/192 kHz with the internal LDO. Our arithmetic is approximately
336/373 mW before the external filter, regulators and clock. This is
**not** a 26 mW mobile DAC. Heavy-load mode raises consumption; normal mode
requires high-impedance AC loading. Its reference circuits include SE and
differential filters and specify external bias rather than permission to
load the common-voltage pins.
[AK4497S manufacturer datasheet, supply table and external circuits](https://www.mouser.com/pdfdocs/ak4497svq-en-full-datasheet.pdf).

**B2:** `Audio clock domain -> AK4191 -> multibit interface -> AK4499EX ->`
`four I/V cells -> differential reconstruction/gain -> same output branches`.

This targets converter/reference margin rather than more headphone watts.
The analog chip alone dissipates 308/343 mW in the documented modes, before
AK4191, external reference generation and I/V. Its specified differential
current swing is 72.8 mApp at the stated 0 dBr definition, and its reference
draw is part of the energy budget. Its interchannel gain mismatch can reach
0.3 dB, so Stage 1's <=0.1 dB complete-device matching requires calibration
or a qualified tighter result. Bias, startup and I/V compliance must follow
the manufacturer's external circuit conditions.
[AK4499EX electrical and reference-circuit conditions](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4499exeq/ak4499exeq-en-datasheet-myakm.pdf).

B1 and B2 offer different complexity/performance trades; neither is
automatically preferable because of the brand. B2's physical digital/analog
separation can help placement, but both remain connected through power,
ground and high-speed signals. It is not galvanic isolation. AK4498EX with
AK4191 is another voltage-output variant worth revisiting if B1 clocking
or physical isolation requirements justify the second chip. It shares the
129 dB / -117 dB published class, not AK4499EX's headline envelope.
[AKM 2025 production announcement](https://www.akm.com/global/en/about-us/news/2025/20250618-ak4497s-ak4498ex/).

### C. Cirrus portable-first voltage path with separate desktop power stage

`Audio clock domain -> one CS43198 -> pseudodifferential reference-sensing`
`filter/buffer -> dedicated quiet SE/IEM stage and line branch`;
`parallel differential driver -> attenuation/gain -> protected BTL amp`.

This is an honest single-conversion stereo path with differential signaling
introduced at the driver. If maintaining opposite phases from conversion
is a hard scoring requirement, use **two** CS43198s, one stereo converter
per audio channel, mapping the same sample into both outputs with one phase
inverted. Their clocks, latency, inversion sequencing and mute must be
matched. Then drive four filters/amp legs and derive SE through an explicit
differential receiver. Never treat REFA/REFB as an actively driven inverted
audio output. Dual conversion's small energy/area cost may be reasonable,
but requires an actual interface and phase-accuracy test.

Cirrus lists 26 mW operation and a 2 Vrms capability; these headlines must
not be paired unconditionally with the -115 dB distortion entry. DS1156F2
at OUT_FS=11 and +1dB_EN=0 lists 4.90 Vpp (~1.73 Vrms) and -115 dB typical;
the boosted +1dB_EN=1 case lists 5.70 Vpp (~2.02 Vrms) and -105 dB. For the
lower-distortion comparator use the unboosted mode and obtain line level
with a qualified downstream gain stage. Dual-core baseline is approximately 52 mW before
drivers and rail conversion, not a measured complete-chain figure.
[Cirrus product specifications](https://www.jp.cirrus.com/products/cs43198/).
Its high-impedance output needs an external power amplifier for demanding
headphones. The manufacturer's QFN evaluation schematic explicitly brings
out AOUT and REF signals, supply pumps and load fixtures; that reference
is more reliable than distributor metadata saying simply "differential".
[CDB43198 schematic/layout](https://statics.cirrus.com/pubs/manual/CDB43198_REV_B_Schematic_Layout.pdf).

Benefits: low converter idle power and no external current I/V. Costs:
charge-pump switching management, reference sensing, phase splitting or a
second chip, and a narrower commercial ambient envelope (datasheet
-20 to +70 C). Chip branding does not establish adequate IEM hiss once
gain, resistors, switches and the power stage are included. Route the
portable IEM path so the high-current desktop stage can actually power
down without back-powering from analog inputs or jack connections.

### D. Precision integrated R-2R with programmable interpolation

`Audio clock domain -> interpolation/dither -> deterministic I2S-to-SPI`
`bridge -> two DAC11001B -> reference/output buffers -> analog LPF ->`
`gain/attenuation -> differential power driver plus separate SE/IEM/line`.

Two chips provide true stereo but are single-ended conversion; a
differential driver supplies BTL. Four DACs would provide two independently
converted opposite phases/channel, with simultaneous LDAC updates,
matched references and a larger cost/clock/area burden. Neither is a
discrete hand-matched resistor ladder. A fully discrete binary/segmented
ladder is a research variant requiring precision arrays, switching,
reference drivers, calibration and a verified temperature model.

TI provides a full current reference, TIDA-060031, with I2S-to-SPI conversion,
reference buffers, output filtering and separate line/headphone paths.
Manufacturer bench results show DAC11001B about -111 dB THD+N at
1 kHz/48 kHz and -108 dB at 1 kHz/192 kHz, but **-47 dB at 10 kHz/48 kHz**
and -92 dB at 10 kHz/192 kHz under the stated bandwidths. This supports a
serious ladder comparator while rejecting an assumption that its good
1 kHz result automatically holds across the band. Its measured line level
is about 2.1 Vrms; the documented idle noise is about 1.9 uVrms. These are
manufacturer reference-board results, not independent laboratory results
or our future hardware. Investigate interpolation/filter/settling changes
before claiming compliance with our full-band target.
[TI design guide and test tables](https://www.ti.com/lit/pdf/TIDUEV2),
[TI complete reference schematic](https://www.ti.com/lit/pdf/SLVRBX0).

The DAC11001B's unbuffered ladder requires positive/negative references,
high-voltage supplies and an output buffer. Its advertised 1 us settling,
20-bit monotonicity, 50 MHz SPI and temperature-calibration facility are
useful starting conditions, not a 24-bit audio guarantee.
[DAC11001B architecture and calibration](https://www.ti.com/lit/ds/symlink/dac11001b.pdf).
At 192 kHz, four 32-bit update frames demand 24.576 Mbit/s before gaps;
384 kHz demands 49.152 Mbit/s, leaving little margin below 50 MHz. Two
chips halve transport demand. Actual framing/LDAC and simultaneous
conversion, settling and host bridge timing remain gates. DSD requires
conversion to a multibit sequence; it is not a native input of this DAC.

## 3. Mature TI and ADI alternatives

PCM1792A can replace the converter in the current-output architecture A,
with its own four I/V cells, reference/bias, filter and clock ratios.
It draws approximately 205 mW at 44.1 kHz and 335 mW at 192 kHz;
the analog rail is 5 V and digital 3.3 V. External digital filtering and
DSD options exist, and its SSOP package is larger than the small QFNs.
It offers a well-documented baseline rather than a low-power advantage.
[PCM1792A supply/timing/reference circuits](https://www.ti.com/lit/ds/symlink/pcm1792a.pdf).
[TIPD177](https://www.ti.com/tool/TIPD177) demonstrates differential-current
conversion, SE summing and headphone drive with verified reference files;
its topology and output rating must not be copied unchanged into this
more powerful balanced requirement.

AD1955 likewise uses current I/V and filtering. Typical DAC power is
210 mW on 5 V analog/digital supplies; its 192 kHz and external-filter
interfaces are adequate for the initial sample-rate contract. Digital
logic thresholds must be checked against RA8P1 rather than inferred from
"I2S" compatibility. The manufacturer still labels it production and
lists a starting 1k-unit price of $11.48; that is not a one-piece quote.
[AD1955 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad1955.pdf),
[AD1955 lifecycle/list price](https://www.analog.com/en/products/ad1955.html).
Neither this older DAC nor its multibit label creates an intrinsic sonic
advantage. They remain alternatives if procurement, verified reference
behavior or manufacturability outweigh the newer candidates' margin.

## 4. Analog path, volume and noise budget common to the alternatives

Separate the small-signal chain from the headphone power amplifier. I/V
compensation is a feedback/stability problem, not just resistor sizing.
Voltage-output DACs still need loading, common-mode translation and
out-of-band filtering; low op-amp voltage noise alone does not prove they
are easier to implement. Delta-sigma ultrasonic shaped noise can consume
slew/current margin or be rectified/intermodulated in later stages. Specify
wideband output noise and filter attenuation as well as audio-band THD+N.
Current-output nodes must stay inside compliance even at startup and loss
of one rail; protect headphones from downstream faults independently.

OPA1612 and OPA1656 are reference-supported small-signal candidates, not
selected parts. OPA1612 has approximately 1.1 nV/sqrt(Hz) voltage noise and
3.6 mA/channel bias; OPA1656's FET inputs have approximately
2.9 nV/sqrt(Hz) and 3.9 mA/channel. Both allow +/-2.25 to +/-18 V.
Bipolar current noise/bias can favor lower source impedances; FET inputs
can favor a higher-impedance volume/filter node. Their drive limits do
not meet the desktop power requirement as bare output stages.
[OPA1612 datasheet](https://www.ti.com/lit/ds/symlink/opa1612.pdf),
[OPA1656 datasheet](https://www.ti.com/lit/ds/symlink/opa1656.pdf).

Illustrative arithmetic, not an approved circuit: eight 3.6 mA amplifier
channels on +/-5 V consume 288 mW idle; on +/-12 V they consume 691 mW.
Use the **total** positive-to-negative voltage times quiescent current.
Adding a DAC, clocks, references and line buffers can make support circuits
dominate mobile conversion energy. Disable unused branches and investigate
lower small-signal rails; do not force every audio op-amp onto desktop
headphone rails. Hot maximum supply current, load power and regulator
losses belong in the later worst-case budget.

Our independent flat-band noise calculations use
`en_R = sqrt(4*k*T*R*B)` at 300 K and B = 19,980 Hz:
100 ohms contributes 0.182 uVrms, 1 kohm 0.575 uVrms, and 10 kohms
1.819 uVrms for a directly presented resistor. Real feedback/filter
resistors have noise-transfer gains and bandwidths; add them accordingly.
A 1 kohm source plus ideal unity-noise-gain 1.1 nV/sqrt(Hz) amplifier is
already about 0.596 uVrms before current noise and 1/f noise. Two such
uncorrelated balanced legs give 0.843 uVrms before DAC and output-stage
contributions. The <=1 uV **unweighted** jack target is therefore a whole
chain design constraint. A-weighted chip noise cannot be inserted as an
unweighted budget value. Two independent 0.55 uV A-weighted channels would
give 0.778 uV differential at unity gain in the same weighting, before
downstream noise; correlation and phase mapping must be measured.

Use digital volume for fine resolution/ramping and DSP headroom, together
with matched analog gain/coarse attenuation or an optimized IEM path.
Digital attenuation lowers the music but does not attenuate noise generated
after conversion. Assess three implementations without selecting yet:

1. Matched switched resistor network before a low-noise buffer, with
   low source impedance, resistor noise budget and contact/switch
   distortion qualification. Four balanced phases must change coherently.
2. PGA/analog volume IC, checking its own input/output noise, gain range,
   supply/common-mode limits and near-zero channel matching. A convenient
   volume-control IC can consume the entire IEM noise allocation.
3. DAC fine attenuation plus analog feedback gain switching and a
   dedicated IEM branch, with controlled break-before-make, mute and
   DC settling. Switching feedback can momentarily open a loop; hardware
   limits and transition sequencing are required.

Do not use a large series resistor at the headphone jack as the main IEM
attenuator: it increases output impedance and interacts with impedance
curves. Pre-amplifier attenuation also cannot suppress the power stage's
own noise. DAC reference full-scale changes are a fourth option only if
linear/noise behavior, calibration and safe transitions are validated.

Provide dedicated line buffers from the small-signal branch; target
2 Vrms SE / 4 Vrms balanced into >=10 kohms with <=100 ohm source impedance
and capacitive stability. Fixed line mode bypasses user attenuation through
an explicit hardware route or gain setting, while variable mode retains
volume. Hardware default mute and jack/type interlock must prevent a fixed
line level from appearing at an IEM. A 4.4 mm line connection requires
documented ground/shield handling, not a grounded headphone adapter.

## 5. Quantified ladder / multibit / NOS comparison

"Multibit" does not mean "R-2R", and R-2R does not mean "NOS".
Modern delta-sigma devices commonly employ multibit internal elements,
oversampling and mismatch shaping. An R-2R DAC can use a digital
interpolation filter; a delta-sigma DAC can expose bypass options.
Architecture alone does not determine time-domain response or audibility.

| Issue | Noise-shaped integrated DAC | Precision ladder / discrete variant |
| --- | --- | --- |
| Low-level linearity | Internal calibration/mismatch shaping; evaluate idle tones, dither, near-zero codes and filter modes. | Static INL/DNL, transition glitches and reference modulation remain; low noise alone does not prove good code accuracy. |
| Out-of-band behavior | Shaped ultrasonic noise needs reconstruction/analog bandwidth control. | Sampling images, settling and switching glitches need reconstruction; no automatic freedom from ultrasonic energy. |
| Reference/temperature | Supply/reference noise and drift still matter; no brand exemption. | Precision reference buffering and ratio tracking are central; discrete thermal gradients and switch resistance add difficult matching terms. |
| Power/area/BOM | One low-power chip can integrate filtering and interface; I/V may add several cells. | Separate serial bridge/interpolation, references, buffers and possibly four DACs/arrays; core alone is an inadequate energy comparison. |
| Manufacture/calibration | Validate the manufacturer's intended reference circuit, gains and tolerances. | Integrated trimmed ladder gives a reproducible baseline; a discrete ladder needs matching, calibration coverage, calibration retention and hot/aged verification. |
| Filter flexibility | Built-in choices/custom modes vary by part. | Arbitrary interpolation is feasible, but costs hardware processing and does not establish superior sound. |

Independent numerical screen: one full-scale LSB is 15.259 ppm at 16 bits,
3.815 ppm at 18, 0.954 ppm at 20 and 0.0596 ppm at 24. Half-LSB accuracy
halves those budgets. These are **system output-error budgets**, not a claim
that every resistor only needs that tolerance. Major-carry weighting,
switches, parasitics and correlated ratio errors determine real INL/DNL.
A nominal 0.01% resistor is 100 ppm; that label alone does not establish
20-bit linearity. Even 0.1 ppm/K ratio drift over 40 K is 4 ppm, about
4.2 full-scale 20-bit LSBs. Global gain drift is different from nonlinear
ratio drift and may be correctable without improving DNL. An integrated
trimmed ladder can be much better than a hand-assembled network, but the
same distinctions still apply to its reference and output electronics.

An ideal full-scale sine's quantization SNR is `6.02*N+1.76` dB:
approximately 122.2 dB for 20 bits. This says nothing about analog noise or
dynamic distortion; the TI reference results above demonstrate the gap.
Oversampling and dither may improve in-band quantization behavior; they
do not repair unknown static nonlinearity or insufficient settling.
Calibration needs traceable transfer characterization and temperature
coverage, rather than just a zero and gain measurement. Bit-perfect
24-bit input truncation to 20 bits is not 24-bit analog conversion.

For ideal zero-order-hold NOS,
`H(f) = sin(pi*f/fs)/(pi*f/fs)`. At 20 kHz the droop is -3.168 dB for
44.1 kHz, -2.640 dB for 48 kHz, -0.156 dB for 192 kHz and -0.0388 dB
for 384 kHz, before an analog filter. The first image of a 20 kHz tone
at 44.1 kHz lies at 24.1 kHz. Thus ordinary NOS at base sample rates fails
our +/-0.1 dB response target and burdens the analog filter with a narrow
transition. Correcting droop alone does not remove images. Oversampling
or a sharp reconstruction filter addresses the engineering problem;
calling image energy or droop an intrinsic sonic improvement is unsupported.
The core choice and interpolation rate must respect actual transport,
settling and power budgets.

## 6. Procurement and lifecycle screen

Observed 2026-10-04 through manufacturer/distributor pages; cached/indexed
inventory can lag actual stock. These are research snapshots, not live
cart quotes, reserved stock, purchases or future availability guarantees.
Prices exclude tax/freight/tariffs. Obtain a current one-piece authorized
cut-tape quote before Stage 6 selection, and retain a schematic-compatible
alternative where practical. Different converter families are not pin swaps.

| Part | Observed source/price/quantity | Risk / implication |
| --- | --- | --- |
| ES9039Q2M | [Mouser regional page](https://br.mouser.com/pt/ProductDetail/ESS-Technology/ES9039Q2M?qs=sGAEpiMZZMtgJDuTUz7Xu6CnpjQCp2EFkEWlPs77jGWacSsWCjNXNw%3D%3D): USD18.70 qty1, 628 shown, cut tape listed. | ESS lists active/new-design recommended. Conflicting aggregator stock is not used to claim unavailable; refresh distributor quote before selection. |
| AK4497SVQ | [DigiKey](https://www.digikey.com/en/products/detail/asahi-kasei-microdevices-akm/AK4497SVQ/26255928): USD41.05 qty1 CT, 607 shown, 22-week standard lead time. | New production generation; manufacturer 250-piece packing quantity does **not** prohibit distributor one-piece cut tape. Full verified application/EVB documentation and reference capacitor area remain gates. |
| AK4499EXEQ | [DigiKey category listing](https://www.digikey.com/en/products/filter/data-acquisition/adcs-dacs-special-purpose/768?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLJANmTAFZEqyBfeoA): USD68.82 qty1 CT, 805 shown. | Additional AK4191 and I/V/reference costs; manufacturer mass-production status is not a long-term supply guarantee. |
| AK4191EQ | [DigiKey](https://www.digikey.com/en/products/detail/asahi-kasei-microdevices-akm/AK4191EQ/18109637): USD11.54 qty1 CT, 260 shown. | B2 converter pair is approximately USD80.36 before reference/I/V/filters; firm quote still required. |
| CS43198-CNZR | [DigiKey](https://www.digikey.com/en/products/detail/cirrus-logic-inc/CS43198-CNZR/7430362): USD18.19 qty1 CT, 481 shown, 20-week standard lead time. | Active, two chips approximately USD36.38 converter-only. Commercial temperature limit and correct pseudodifferential topology need attention. Do not substitute obsolete CS4399. |
| PCM1792ADB | [DigiKey listing](https://www.digikey.in/en/products/detail/texas-instruments/PCM1792ADB/1573317): 211 shown in indexed regional listing; single-piece USD price not verified. | TI active, mature package/reference support; refresh stock/quote, no lifespan inferred from age. |
| AD1955 | [ADI](https://www.analog.com/en/products/ad1955.html): production, starting USD11.48 at 1k units. | One-piece stock/price not verified; this is a quantity list price. Documentation maturity helps reproducibility but not supply longevity. |
| DAC11001B | [Mouser US BPFBT](https://www.mouser.com/en/ProductDetail/Texas-Instruments/DAC11001BPFBT?qs=doiCPypUmgGMYjFfmnds9Q%3D%3D): USD142.07 qty1 CT, 350 shown, 16-week estimated factory lead time. [DigiKey PFBR](https://www.digikey.com/en/products/detail/texas-instruments/DAC11001BPFBR/18158712): not normally stocked, USD85.1235 at 1000. | One-piece authorized cut tape is listed; do not confuse reel packing with minimum purchase. Two/four chips are USD284.14/568.28 before references/bridge. Confirm exact suffix and quote. |

High component cost can be justified by guaranteed behavior, lower noise,
stable references or easier qualification. This screen does not demonstrate
an audible advantage from a USD68 DAC over a USD19 DAC. Neither price nor
newness establishes better battery life, headphone drive or reliability.

## 7. Stage 6 decision inputs and unresolved gates

Carry **A, B1/B2, C and D** into the combined architecture score. No final
DAC or analog topology is selected here. A and C plausibly protect runtime;
B1 offers a straightforward differential voltage chain; B2 offers more
converter margin with support-power cost; D provides a documented ladder
experiment with significant high-frequency/transport gates. These are
engineering inferences from the evidence above, not measured complete-player
performance or a runner-up designation.

Before final component integration/rating release, close: complete idle/playing energy including clocks and
references; unweighted active-zero IEM noise; matched gain/volume transition
behavior; wideband out-of-band response and loaded full-band THD+N; DC/common
mode and rail-loss faults; SSI/USB/bridge clock compatibility; line/headphone
connector routing; reference/filter capacitor volume; genuine authorized
small-quantity supply and document access. A stage should not claim completion
of full reference-board replication or independent continuous-power testing
merely because a public datasheet and schematic were reviewed.

Any performance advantage at -115 versus -120 dB converter distortion is
primarily engineering margin until complete-path measurements and controlled
listening demonstrate otherwise. Avoid spending the portable power budget
on a higher DAC headline while the high-gain amplifier hisses or the sealed
enclosure cannot sustain the output envelope. The final selection belongs
to Stage 6 after independent amplifier/platform/power studies. A provisional
architecture recommendation may proceed from this research; it must retain
unperformed measurement, sourcing and timing checks as explicit hold points
rather than assert that the reference behavior has been reproduced.
