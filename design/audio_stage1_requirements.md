# Audio architecture study: Stage 1 requirements and feasibility

**Owner update, 2026-10-05:** PCM768/DSD512, premium Bluetooth audio and the
higher desktop output targets are now required. The authoritative new
[target contract and corrective plan](audio_external_review_2026-10-05.md#owner-adopted-target-contract)
supersedes the older optional-format, 2 W floor / 4 W stretch and 16 Vrms
language below. RA8P1 remains the application/system master. The existing
schematic does not yet implement these requirements; exact components,
continuous thermal capability and codec licenses remain engineering gates.

2026-10-04. Owner-directed architecture reset; hardware study only.

**Status: feasibility screen, not a selected architecture or output rating.**
No DAC, amplifier topology, charger, battery, or processor replacement is
selected by this record. Detailed audio schematic work is on hold until
Stages 2-6 close. Existing U34/K1 wiring and the unplaced FDN337N candidate
remain WIP; they are not evidence that the expanded requirements are met.
This study supersedes the old performance envelope and provisional component
direction in [audio_subsystem.md](audio_subsystem.md), while preserving its
history and electrical observations. Existing e-reader, camera, lighting,
speaker, battery and wet-port requirements remain in scope.

The owner clarified during this study: network music comes from their own
server, and our task is hardware. Commercial streaming-service integration
and DRM are therefore not requirements driving the platform decision. We
must provide suitable interfaces, resources and timing contracts; firmware
implementation is outside this study.

The owner delegated runtime and packaging budgeting to the designer and
reaffirmed broad headphone coverage. Initial engineering allocations are
>=10 hours local playback and >=8 hours own-server streaming, ordinary
IEM/headphone listening, display front light off. Report lighting, display
activity, speaker and high-power headphone cases separately. Investigate
20-30 Wh nominal battery energy without selecting a pack or cell topology:
at 80% usable energy the 20 Wh endpoint requires <=1.6 W local and <=2.0 W
streaming average, while 30 Wh permits <=2.4/3.0 W. These are designer
targets to validate against the complete board, not user-supplied dimensions
or promised runtime. Budget space/heat around the required e-paper assembly
and a passive heat-spreading enclosure; do not assume a dongle-sized case.

## 1. Feasibility verdict and requirements that need correction

The combined product is feasible in principle. Sustained desktop headphone
power in a portable, water-resistant enclosure is conditional on an explicit
thermal design and battery/size budget. Choosing a premium DAC does not close
those conditions.

| Owner objective | Stage 1 disposition |
| --- | --- |
| Quiet IEMs and demanding planars | Retain both; qualify noise and gain at millivolt outputs separately from watt-level output capability. A shared output stage and a separate IEM path both remain alternatives. |
| 16-600 ohms | Retain these resistive test points; extend low-power IEM qualification to at least 8-9 ohms and frequency-dependent/capacitive loads. Impedance alone is not compatibility. |
| >=2 W/channel into 32 ohms balanced | Reasonable desktop feasibility floor; 8 Vrms, 250 mArms, 354 mApeak per channel. Both channels driven, sustained operation required. |
| Investigate 3-4 W/channel into 32 ohms | Retain as a desktop stretch. Doubling 2 W to 4 W adds only 3.01 dB of headroom; justify against actual loads/EQ and heat. |
| >=8 Vrms high-impedance balanced | Keep as a floor, not a ceiling. Investigate 12-16 Vrms for useful future voltage margin; full DX5 II voltage parity is a different requirement. |
| Last headphone amplifier | Replace unlimited future compatibility with a documented voltage/current/thermal envelope. Electrostatic energizers, unusual sub-ohm loads and arbitrary future headphones cannot be covered by an ordinary headphone amplifier specification. |
| Excellent battery life and desktop power | Separate modes with independent noise, rail, gain and current limits. Desktop power must not be silently promised on battery or on every phone USB port. |
| Proper line output | Retain fixed and variable modes; initially investigate 2 Vrms SE / 4 Vrms differential into >=10 kohms. Connector allocation and simultaneous line/headphone use are open. |
| Balanced throughout | Evaluate as an engineering option, with loaded crosstalk, noise and distortion evidence. Four active output conductors help voltage capability but do not automatically improve audibility. |
| High-resolution / DSD / DSP | Provision stereo PCM through 192 kHz as an initial hardware requirement; higher rates and native DSD are optional investigation items. DSP and bit-perfect playback are separate operating contracts. |
| Water resistance | Preserve wet-port inhibition and exposed-contact protection. A sealed enclosure makes heat removal a first-order design input; no fan or vent is assumed. |

The Shure SE846 is specified at 9 ohms and 114 dB SPL/mW at 1 kHz. It
demonstrates why a 16-ohm lower bound would exclude a relevant sensitive IEM.
[Shure specifications](https://www.shure.com/ja-jp/insights/all-about-se846-gen2-a-more-sophisticated-listening-experience).

## 2. Current product evidence and its limits

Published clipping-power specifications establish scale, not sustained thermal
ratings. None of the sources below specifies a duration sufficient to prove
thermal equilibrium at rated power in our enclosure.

| Product | Evidence reviewed | Implication for this product |
| --- | --- | --- |
| FiiO KA17 | Manufacturer balanced desktop rating 650 mW/channel into 32 ohms at THD+N <1%; 90 mW into 300 ohms. External input is 5 V, >=1 A. Balanced residual noise <2.2 uVrms A-weighted; output impedance <1.5 ohms. | Our 2-4 W target is above this dongle's envelope. Its desktop setting does not demonstrate high-voltage USB-PD. Its noise/Zout are comparison data, not our IEM acceptance limits. |
| Questyle SIGMA | Japanese official representative specifies maximum 1.2 W into 32 ohms balanced, four current-mode amplifiers, an IEM mode and 4300 mAh battery. | Demonstrates useful portable segmentation. Published maximum power lacks a sustained-duration test; proprietary topology names do not establish a reproducible engineering benefit. SIGMA and SIGMA Pro must not be conflated. |
| TOPPING DX5 II | Official manual specifies balanced 6.4 W/channel into 32 ohms and 490 mW into 600 ohms, THD+N <1%; high-gain swing 48 Vpp. Low/high-gain balanced noise <1.6/<4.3 uVrms A-weighted. | 4 W/32 is 2.04 dB below its 6.4 W headline. Its high-impedance capability is about 17 Vrms, so 8 Vrms is about 6.5 dB below its voltage swing. Its high/low-gain noise difference reinforces separate IEM qualification. |

Sources: [KA17 parameters](https://www.fiio.com/ka17_parameters),
[SIGMA official Japanese announcement](https://questyle.jp/questyle%E3%80%8Csigma%E3%80%8D%E6%97%A5%E6%9C%AC%E5%88%9D%E7%99%BB%E5%A0%B4-%E6%8D%AE%E3%81%88%E7%BD%AE%E3%81%8D%E7%B4%9Atta%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A3/),
[DX5 II manual, headphone specifications](https://dl.topping.audio/um/dx5_ii.pdf).
These are manufacturer claims, not independently verified continuous output.

Independent evidence also matters for integration: L7Audiolab's original
iBasso DX240/AMP8Mk2 measurements report USB-associated interference in the
single-ended path that disappears without USB and improves with isolation.
This is one tested implementation, not proof that ours needs galvanic
isolation. It establishes battery-only, USB-data, PD-power and charging
measurements as separate acceptance conditions.
[Original measurement report](https://www.l7audiolab.com/f/ibasso-dx240a8m2/).

The DX5 II ASR review could not be read reliably through the research tool;
no secondhand SINAD/noise values from it are used. The HomeTheaterHifi DX5 II
review explicitly did not evaluate headphone outputs, so it is not used as
independent headphone-power evidence. Stage 2 must continue the laboratory
comparison; a short output sweep is still not a thermal soak.

## 3. Voltage/current envelope and representative resistive loads

All powers below are per channel. Voltages are differential RMS sinusoidal
output across the load. Current is load current, not half the current because
the circuit is balanced. Each active BTL leg carries the full load current.

`P = Vrms^2 / R; Irms = Vrms / R; Ipeak = sqrt(2) * Irms`.

| R (ohms) | At 8 Vrms: W | At 8 Vrms: Apeak | At 11.314 Vrms: W | At 11.314 Vrms: Apeak |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 4.000 | 0.707 | 8.000 | 1.000 |
| 32 | 2.000 | 0.354 | 4.000 | 0.500 |
| 50 | 1.280 | 0.226 | 2.560 | 0.320 |
| 80 | 0.800 | 0.141 | 1.600 | 0.200 |
| 150 | 0.427 | 0.075 | 0.853 | 0.107 |
| 300 | 0.213 | 0.038 | 0.427 | 0.053 |
| 600 | 0.107 | 0.019 | 0.213 | 0.027 |

These are **demands**, not promised output ratings. Holding the 32-ohm
voltage into 16 ohms would double power. Protection/current limiting must
prevent that assumption from becoming an unintended product specification.

For comparison in later stages, screen a floor envelope of 8 Vrms,
0.5 Apeak and 2 W/channel continuous cap, and a stretch envelope of
11.314 Vrms, 0.707 Apeak and 4 W/channel continuous cap. In each,
`Vavailable = min(Vlimit, Ipeak_limit * R / sqrt(2), sqrt(Pcap * R))`,
further limited by SOA and the actual thermal design. The floor delivers
2 W/16 and 2 W/32; the stretch delivers 4 W/16 and 4 W/32, then becomes
voltage-limited above 32 ohms. This does not select a circuit. High-impedance
12-16 Vrms extension should be costed separately with the same current and
continuous-power limits; it must not imply 8 W/32 at 16 Vrms.
16 Vrms would provide 0.853 W/300 and 0.427 W/600.

SE gets its own specification. Using one BTL leg gives half the differential
voltage and quarter the power at the same impedance, assuming unchanged
current capability; using an independent SE amplifier changes that result.
Never short an active balanced negative output to ground to obtain SE.
Connector insertion, mono plugs, adapter misuse and grounded line inputs
must be part of fault testing.

## 4. Listening reference and headphone screening

Use 75-80 dB equivalent reference levels with an engineering 20 dB transient
allowance as the initial sizing exercise; also examine a conservative
105 dB equivalent-sine peak-capacity screen and another 6 dB of EQ/uncertainty
reserve. These are electrical sizing scenarios, not recommended sustained
listening levels. Music crest factor, acoustic fitting, frequency-dependent
sensitivity and EQ make a one-frequency SPL calculation approximate.
EQ boost requires digital preattenuation to avoid clipping as well as analog
voltage headroom; flat sensitivity at 1 kHz cannot predict a bass boost exactly.

| Case and source basis | 100 dB equivalent: Vrms / mW | 105 dB equivalent: Vrms / mW | 111 dB equivalent: Vrms / mW |
| --- | ---: | ---: | ---: |
| Original Susvara, conservative RAA measured screen, 93.2 dB/V and 67.1 ohms | 2.188 / 71.3 | 3.890 / 225.6 | 7.762 / 898.0 |
| HD800S, manufacturer 102 dB/V and 300 ohms | 0.794 / 2.10 | 1.413 / 6.65 | 2.818 / 26.48 |
| Stealth, manufacturer approximately 90 dB/mW and 23 ohms | 0.480 / 10.0 | 0.853 / 31.6 | 1.702 / 125.9 |
| SE846, manufacturer 114 dB/mW and 9 ohms | 0.0189 / 0.0398 | 0.0337 / 0.1259 | 0.0672 / 0.5012 |

Sources: [RAA original Susvara measurements](https://reference-audio-analyzer.pro/en/report/hp/hifiman-susvara.php),
[Sennheiser HD800S specifications](https://support.sennheiser-hearing.com/hc/en-us/articles/38273432554141-HD-800S-Specifications),
[Dan Clark Stealth specifications](https://danclarkaudio.com/dcastealth-2.html?options=cart),
Shure source above.

RAA also reports substantially different sensitivity for a
[separate Susvara 2022 test](https://reference-audio-analyzer.pro/en/report/hp/1-susvara-2022.php).
Do not treat those samples/fixtures as interchangeable or infer a guaranteed
acoustic level. The conservative screen is useful for margin budgeting;
Stage 3 needs multiple measured difficult headphones, sensitivity uncertainty
and impedance curves. It must include HE6-class inefficient planars and
voltage-hungry dynamics, with explicit model revisions.

The conservative Susvara screen needs almost 8 Vrms for 105 dB plus the
6 dB reserve, while ordinary high-impedance dynamics can need far less.
This makes voltage margin more informative than a universal watts claim.
4 W/32 is useful reserve, but the case studies do not establish that every
planar needs 4 W continuously or that a different DAC architecture improves
drive. The IEM case shows why most listening occurs at radically lower levels.

## 5. Rail and thermal feasibility

For a symmetric BTL channel, each leg swings half the differential voltage:
`Vleg_peak = sqrt(2) * Vdiff_rms / 2`.
With an **assumed** 1.5 V per-leg output-stage headroom, the minimum rail
magnitudes are +/-7.16 V for 8 Vrms, +/-9.50 V for 11.314 Vrms, and
+/-12.81 V for 16 Vrms. These assumptions exclude tolerance, droop, output
protection drops and hot current-dependent swing. A real topology must prove
its headroom; merely changing a converter to these values is not sufficient.

Use an ideal Class-B BTL model to establish heat scale without choosing an
amplifier: `Pdc/channel = 4 * Vrail * Ipeak / pi` and
`Pheat/stereo = 2 * (Pdc/channel - Pload/channel)`.
At +/-10 V rails with the stretch envelope limited to 0.707 Apeak:

| R (ohms) | Available Vrms | W/channel | Ideal stereo output-stage heat (W) |
| ---: | ---: | ---: | ---: |
| 16 | 8.000 | 4.000 | 10.006 |
| 32 | 11.314 | 4.000 | 4.732 |
| 50 | 11.314 | 2.560 | 3.029 |
| 80 | 11.314 | 1.600 | 1.893 |
| 150 | 11.314 | 0.853 | 1.010 |
| 300 | 11.314 | 0.427 | 0.505 |
| 600 | 11.314 | 0.213 | 0.252 |

Add quiescent bias, drivers, DAC/I-V/filter, digital system, conversion loss
and charging heat. The low-load 16-ohm result is particularly costly because
the voltage has been current-limited while rails remain high. Rail reduction
at low impedance may help but requires stability/noise/transition analysis.
For this ideal model peak dissipation can occur below maximum output:
differentiate `4*Vrail*Vpk/(pi*R) - Vpk^2/(2*R)` to find
`Vpk = 4*Vrail/pi`, subject to the attainable swing/current limits.
Test intermediate levels as well as maximum power.

The stereo 4 W/32 point consumes 12.73 W at the amplifier rails. Assuming
90% rail conversion and an illustrative 3 W for the rest of the device gives
17.15 W external input before charging, of which about 9.15 W heats the
device. At the limited 4 W/16 point the same assumptions give 23.01 W input
and 15.01 W device heat before charging. Headphone output power is dissipated
mostly outside the enclosure; it is not all enclosure heat.

An illustrative 15 K enclosure temperature-rise budget would require about
1.64 K/W enclosure-to-ambient at the 32-ohm example and 1.00 K/W at the
16-ohm example. This is not a package theta-JA calculation or a declared
touch-temperature limit. It demands mechanical heat spreading and enclosure
area. Sustained capability cannot be approved until size/material/ambient
and battery-temperature limits are specified. A sealed enclosure cannot be
assumed to tolerate these watts just because the IC has thermal shutdown.

Class A is a serious comparator but not an assumed premium improvement.
For example, a four-leg push-pull stage biased at 0.25 A per leg on +/-10 V
draws approximately 20 W idle, before the rest of the device. Whether that
bias produces a particular Class-A load envelope is topology-dependent.
Its portable energy cost requires a demonstrated benefit.

## 6. Power strategy requirements, not a completed power tree

USB-C must negotiate external power before enabling desktop rails. A USB
data connection does not imply a suitable power contract. The examples above
already exceed a 5 V/1 A budget. Investigate a 30-45 W PD allocation with
15 V/3 A or an appropriate 20 V contract; these are budget candidates, not
selected mandatory profiles. Charge current must share the budget with the
amplifier, cameras, lights, display updates, radio and processor. At weak
sources or after PD loss, hardware limits must reduce output without clicks
or brownout; desktop capability cannot be silently retained.

Require external-source operation that does not continuously recharge a
discharging battery. Distinguish normal charger power-path load sharing from
true battery isolation/bypass: some chargers supplement a weak input from
the battery. Desktop sustain must not depend on that supplement. Define
battery-absent behavior, charge-off operation and rail sequencing in Stage 5.
Wet-port detection/inhibition must coordinate VBUS, CC/data protection,
power entry and headphone ground paths. Moisture detection alone is not a
waterproof-port qualification.

Battery example only: 3.7 V, 5 Ah is 18.5 Wh nominal, or 14.8 Wh assuming
80% usable energy. Eight hours requires average total input <=1.85 W; at
3 W it gives about 4.93 hours. Do not size runtime from headphone peak
power. The DAC/filter/amplifier idle power, active processor, memory, Wi-Fi,
front light and display updates can dominate portable use. Actual pack,
discharge curves, cold/aged capacity and converter efficiency remain open.

Domains to budget separately in Stage 5: host/digital, SDRAM/NOR/storage,
display/HV/touch/front light, camera/illumination, Wi-Fi/radio, USB/PD,
DAC digital, DAC analog/reference, clocks, I/V/filter/volume/line driver,
headphone amplifiers, speakers, charger/battery/gauge and always-on safety.
Switchers are acceptable where tested; low-noise LDOs/filters follow only
where PSRR/noise budgets and voltage headroom justify them. Ground-return
and USB/common-mode interference require more than a low DC-noise LDO.

## 7. IEM, line, protection and measurement contracts

Proposed complete-device targets for architecture scoring, not measured
claims or approved release specifications:

| Property | Proposed initial qualification target |
| --- | --- |
| IEM residual noise | <=1 uVrms unweighted 20 Hz-20 kHz at the jack with a connected digital source; 0.5 uV stretch. Report A-weighted separately, mute vs active zeros, and both outputs. At 50 mVrms, 1 uV corresponds to 94 dB SNR. |
| Output impedance | Prefer <=0.25 ohm SE and <=0.5 ohm differential BAL; investigate <=0.1/0.2 ohm. Include switches/relay contacts, current-sharing resistors and connector resistance. Measure over frequency. |
| Low-level matching | <=0.1 dB channel error at 1-50 mVrms, across gain/volume transitions. Include ADC/control quantization only where it affects the analog result. |
| Loaded THD+N | Initial screen <=-100 dB at 1 kHz, 1 Vrms into 32/300 ohms, 20 Hz-20 kHz measurement bandwidth; rated sustained output <=-90 dB. Sweep frequency, gain, level and load; <1% clipping-power figures must be separate. |
| Response | 20 Hz-20 kHz within +/-0.1 dB, filter mode specified, representative complex loads. Also measure out-of-band noise, not just audio-band response. |
| Line output | Initially 2 Vrms SE / 4 Vrms balanced fixed and variable, >=10 kohm load; investigate <=100 ohm source impedance, capacitive stability and >=115 dB SNR referenced to declared line level. |
| Other measurements | Loaded crosstalk >=90 dB at 1 kHz as an initial target; report 20 kHz. IMD, multitone, low-level linearity/dynamic range, jitter spectra, DC offset and pop waveform/energy require defined fixtures and bandwidths. |
| Continuous power | Both channels, specified load and gain, minimum 60 minutes and until thermal equilibrium; initial 25/35 C ambient screens. Test charging, USB and radio conditions, intermediate dissipation maxima, voltage droop and limiting. Mechanical limits must be fixed before calling this a product rating. |

Noise cannot be inferred from full-scale SINAD. A high-voltage amplifier
with digital attenuation can retain analog hiss; gain reduction, analog
attenuation or an optimized low-noise path must be evaluated independently.
Balanced noise from independent legs adds in quadrature, while common-mode
terms may cancel only to the extent of actual matching. Output series
attenuators cannot be accepted without their impedance/load/noise effects.
No target alone guarantees inaudibility for every IEM/user.

Require hardware default-disconnected outputs and independent DC detection,
rail-loss, overcurrent/short and overtemperature protection. Detect faults
on all four balanced conductors and both SE signals. Firmware crash, stuck
control pins, charger faults, one-rail loss and output-stage component
failure must not rely on a functioning main processor to remove power.
Set DC threshold, trip latency and allowed delivered fault energy against
actual loads; fast bass rejection is a filtering tradeoff, not permission
to ignore sustained DC. Failures of the disconnect/protection itself need
a defined fault model. Existing K1 coil/driver/DC detector is unfinished.

Line and headphone modes need explicit connector detection, default volume,
gain limits and mute/transition behavior. Fixed line level must not suddenly
appear at an inserted IEM. Dedicated line buffers are a serious option;
reusing a headphone path requires loaded noise/distortion/impedance and
mode-fault evidence. Simultaneous SE/BAL/line operation is not yet assumed.

## 8. Digital hardware and clocking feasibility

ESP32-C6 is not an adequate sole controller for the proposed USB DAC: its
USB Serial/JTAG block is fixed-function and cannot become UAC2. Its radio
is Bluetooth LE, not Bluetooth Classic; ordinary A2DP/LDAC/aptX support
cannot be assumed. BLE version branding does not qualify LE Audio hardware
and stack support. [Espressif USB documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/usb-serial-jtag-console.html),
[C6 datasheet](https://documentation.espressif.com/esp32-c6_datasheet_en.html).

The actual board already uses RA8P1 as host, C6 as radio, and external RAM
and storage. RA8P1 offers a 1 GHz M85, a 250 MHz M33 variant, USB HS/FS,
I2S and SDHI; this makes MCU local-file/DSP/own-server playback a credible
hardware candidate, not a benchmarked implementation. External memory
bandwidth, USB DMA/endpoint resources, clock feedback and radio-host
throughput must be verified. Do not substitute the firmware repository's
RA8D2 evaluation-board identity for this RA8P1 design.
[Renesas RA8P1 hardware overview](https://www.renesas.com/en/products/ra8p1).

Uncompressed stereo 192 kHz x 24-bit is 9.216 Mbit/s payload, or
12.288 Mbit/s when transported as 32-bit samples. Size radio interconnect,
DMA and buffers with protocol/arbitration margin. At 64 I2S bits/frame,
192 kHz requires 12.288 MHz BCLK; 176.4 kHz requires 11.2896 MHz.
The prior SSI review establishes an 80 ns minimum period (12.5 MHz) for
the considered RA8P1 slave route, with setup/hold qualification still open.
384 kHz at 64 bits/frame requires 24.576 MHz, so it cannot simply be enabled
on that route. A different interface/USB bridge would need its own review.
[Existing timing review](audio_review.md),
[RA8P1 hardware manual](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware).

UAC2 asynchronous playback should measure real consumption in the DAC clock
domain and provide bounded feedback/buffering; USB frame timing is not the
audio master clock. Current Windows has a native UAC2 driver (introduced in
Windows 10 1703), including requirements that affect descriptors/feedback.
Native DSD/vendor ASIO is a separate support question; do not infer it from
PCM driverless operation. Phone USB power/roles and adapter compatibility
need physical tests. [Microsoft UAC2 requirements](https://learn.microsoft.com/en-us/windows-hardware/drivers/audio/usb-2-0-audio-drivers).

Provision the 44.1 and 48 kHz rate families and clean clock-domain crossings;
dual oscillators vs PLL/ASRC remain architecture alternatives. Oscillator
headline jitter alone is not total DAC sampling jitter. The elementary
sine model `SNRjitter = -20*log10(2*pi*f*tj)` gives approximately 118 dB
for 20 kHz and 10 ps RMS, but DAC clock recovery and phase-noise spectra
determine the actual result. Require measured sidebands/noise rather than
an unlimited oscillator-price target.

DSP resources should cover at least ten PEQ bands/channel, balance,
ReplayGain/loudness/crossfeed and bounded user filters; this is a hardware
capacity contract, not a firmware implementation commitment. Determine
worst-case precision/headroom and transport buffering in Stage 4. Native
DSD plus arbitrary PCM DSP is not a simultaneous bit-perfect mode: choose
conversion or DSP bypass. A DAC's 32-bit input does not establish 32-bit
analog accuracy. No FPGA, dedicated DSP or Linux processor is selected now.

Own-server streaming removes a major reason to require commercial-service
app infrastructure. Linux remains a comparator where its drivers, library
management or networking justify energy/boot/BOM cost. Do not add it merely
because this is a premium player. Commercial-service research is retained
only as context: Spotify's commercial eSDK process and current Linux Soloist
option have different integration/update requirements; neither is a new
owner requirement or a claimed feature of this board.

## 9. Architecture gates and remaining work

Stage 1 cannot prove continuous thermal operation, firmware capacity,
supplier lifecycle or measured transparency without later design/bench work.
Exact enclosure dimensions, pack choice and product ambient limits remain
design work. Use the runtime allocations above and multiple difficult
headphones rather than waiting for an owner model list. Stage 3 should screen
roughly 16 Vrms high-impedance swing and 0.707 Apeak low-impedance current as
a broad-coverage desktop candidate, with 2 W/32 as the floor and 4 W/32 as a
conditional stretch. At low impedance voltage must fall to the current/heat
limit. These proposed limits do not select a DAC or authorize final CAD.

| Stage | Required next evidence/deliverable |
| --- | --- |
| 2: >=3 architectures | Compare complete ESS, AKM and another serious path (Cirrus/TI/ADI or ladder where justified), including I/V vs voltage output, filtering, line/IEM paths, clocks, power, cost and availability. Explicitly quantify ladder linearity, matching/drift/monotonicity, calibration and NOS/reconstruction tradeoffs. No assumed sonic advantage for R-2R, delta-sigma, price or brand. |
| 3: independent amplifier study | Integrated, composite/discrete AB, Class A, current-feedback/current-mode and implementable error-correction alternatives; feedback stability, BTL/SE derivation, output sharing, gain/volume/noise, SOA and fault protection. Additional measured difficult headphones and verified thermal rail/current envelope. Proprietary Questyle/THX names are not schematics. |
| 4: platform/interfaces | RA8P1+C6, alternative MCU and heterogeneous/Linux hardware comparison. Memory/radio/storage/USB resources, 192 kHz timing, DSP budget, codec decode benchmark requirements, sample-rate changes, USB async clock crossings and Bluetooth requirements. Firmware is a separate task. |
| 5: complete power architecture | PD contract/input limits, battery/charger/load sharing or isolation, rail converters, references/clocks/analog supply noise, weak-source fallback, simultaneous system loads, moisture protection and thermal/battery-aging budget. |
| 6: selection | Recommend one complete architecture and a runner-up, with quantified reasons and triggers to switch; resolve owner mechanical limits. No final DAC selection before this step. |
| 7: component/electrical design | Exact parts and alternatives, voltage/current/hot tolerances, cost/availability/lifecycle, loop/analog simulations, hardware protection, native schematic, ERC/BOM/PDF. Plan controlled-impedance routing, solid return planes, analog/RF partitioning, current paths and thermal interfaces; detailed PCB/footprints remain the later project milestone. |

Independent Stage 1 arithmetic review found no numerical errors and identified
the missing intermediate-load power cap: voltage/current limits alone would
allow 5.66 W near 22.6 ohms. The explicit Pcap above resolves this; calculation
checks cover that load and the high-voltage extension at 32 ohms. Continuous
limits may be lower after mechanical/thermal qualification.

For every major selected part, Stage 7 must record function, alternatives,
design-specific justification, limitations, power, heat, price, supply risk
and whether the benefit is plausibly audible or primarily measurable.
Maintainability, replaceable battery, recoverable firmware/update paths and
stable USB interoperability support the long-term objective more directly
than purchasing a DAC with an unused headline sample rate.

## 10. Reproduction and checkpoint boundary

Run `python scripts/check_audio_stage1.py` for load, rail, ideal heat,
headphone sensitivity, battery and SNR arithmetic. It checks representative
known values and stereo energy conservation. It is not SPICE, a compliance
test, a continuous-power guarantee or confirmation of part suitability.

All source observations are dated 2026-10-04 and linked at their use above.
Calculations and proposed limits are our engineering analysis. No schematic,
symbol, footprint or native BOM changes are made by this stage. The review
PDF was refreshed and all 15 pages visually reviewed; every rendered page
is identical to the prior checkpoint. Read-only CLI ERC remains 103 errors
and 15 warnings (118 findings); the four existing ignored-check categories
were unchanged. This is an unchanged incomplete-design baseline, not a pass.
