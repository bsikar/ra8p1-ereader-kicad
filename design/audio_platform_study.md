# Audio Stage 4: hardware platform and interface study

**2026-10-05 external-review update:** the native-only transport preference is
reopened by [the disposition record](audio_external_review_2026-10-05.md).
RA8P1 remains system master. The sixteen-BUF634A bank is a research
comparator; no high-power implementation is selected. PCM768/DSD512, premium Bluetooth and the higher desktop envelope are
now owner-required. XU316 is the primary high-rate bridge candidate;
its exact package and routing are not selected.
Earlier recommendations below remain traceable study history, not a design
freeze. Use the revised work plan for the next implementation steps.

2026-10-04. Research and proposed qualification contracts; no platform selection,
schematic modification, firmware implementation or performance certification.
Read with [Stage 1](audio_stage1_requirements.md),
[interface reservations](camera_storage_interfaces.md),
[radio interface](radio_interface.md) and [audio timing review](audio_review.md).

The owner specifies streaming from their own server and assigns this task to
hardware. Commercial-service DRM, applications and offline service downloads
do not drive processor selection. Local lossless decoding, networking and DSP
remain hardware capacity requirements; their implementation is separate work.
Preserve the e-paper assembly/controller/HV supply, touch, warm/cool front light,
two cameras, front illumination/rear flashlight, speakers, battery, wet-port
inhibition and five physical buttons. A new processor cannot silently remove
any of them to make the audio path easier.

## Evidence and limits

The actual design MCU is **R7KA8P1KFLCAC#UC0, RA8P1**, not the firmware
repository's RA8D2 evaluation board. Its manufacturer page confirms dual cores,
1 GHz M85 / 250 MHz secondary maximum clocks, double/single/half floating point,
2 MiB RAM, 16 DMA channels, two SDHI and two SSI peripherals, USB HS and FS,
SDRAM interface, MIPI CSI and parallel camera interface. The temperature grade
is 0-95 C junction. The page marks UC0 Active and lists UC1 as a replacement;
silicon/errata and ordering-code review must precede any substitution.
[Exact Renesas part](https://www.renesas.com/en/products/ra8p1/part-details/r7ka8p1kflcac-uc0).

The RA8P1 datasheet describes ten USBHS pipes and DMA-driven SSIE FIFOs.
Its stated 50 MHz audio source-clock capability does **not** overturn the
separate external serial-clock AC timing restriction. The project review of
HUM Table 70.75 retains an 80 ns minimum BCLK period and unfinished setup/hold
closure. Power tables distinguish core-domain dynamic current, regulator/leak
current and external supply current: do not multiply a core-domain IDD entry
by 3.3 V and call it measured chip input power.
[RA8P1 datasheet Rev.1.30](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet),
[hardware manual](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware).

Renesas explicitly lists RA8P1 support in its PAUD driver, with Audio 1.0 and
2.0 support. This establishes an available software foundation, **not** proof
that asynchronous feedback, 192 kHz stereo, composite descriptors and every
phone already work. FSP's separate composite driver documentation lists a
limited set of combinations without PAUD; simultaneous audio + storage/debug
cannot be assumed to be an out-of-box supported combination.
[Renesas PAUD](https://renesas.github.io/fsp/group___u_s_b___p_a_u_d.html),
[composite driver](https://renesas.github.io/fsp/group___u_s_b___c_o_m_p_o_s_i_t_e.html).

## Serious alternatives to score in Stage 6

| Candidate | Role and defensible benefit | Main liabilities / decision trigger |
| --- | --- | --- |
| P-A: existing RA8P1 + C6; native RA8 USBHS and SSIE | One main host handles storage/UI/PCM/DSP; C6 handles radio. Preserves current camera and memory work; avoids an always-active second audio processor. | UAC2 feedback and SSI timing must close; radio link speed is an actual bottleneck; shared-memory/DMA contention and active power require measurements. Retain as a candidate if these contracts pass. |
| P-B: existing RA8P1 + C6 + XU316 audio processor | XMOS owns USB/UAC2/audio clocks and optionally DSP; RA8P1 retains e-reader/cameras/library control. Separates USB deadlines from camera/UI activity. Can be power-gated or bypassed in local playback if the complete switching sequence is proven. | Extra rails, boot flash/debug, clock-domain transfer, source arbitration and energy. If USB audio goes directly to the DAC, RA8 DSP cannot process it unless a return path is provided. A bypass path is a design feature, not an assumption. Useful if native USB/SSI deadlines fail or a verified independent DSP path is valuable. |
| P-C: RT1170-class host + C6 or appropriate radio + XU316 | A serious alternate MCU baseline with manufacturer USB/SAI/camera support and established peripheral ecosystem; XMOS gives the same USB isolation of responsibilities as P-B. | Wholesale pinmux, memory, camera, boot and power redesign. Does not fix low-noise analog design. No reason to replace RA8P1 solely because another MCU has a familiar SDK; require a measured power/latency/interface advantage. |
| P-D: RA8P1 e-reader/safety host + i.MX8ULP application/audio companion | Linux-capable AP offers richer filesystem/network/library ecosystem, while independent MCU supervision and existing camera routes remain. Application and audio domains can sleep independently where supported. | DDR/PMIC/storage/IPC and boot/update complexity; duplicate host resources. Replacing RA8P1 entirely would reopen the parallel-camera interface and every preserved product function. Without commercial app/DRM requirements, justify Linux with actual power/workload/interoperability data. |

XMOS documents UAC1/UAC2, asynchronous mode and its USB-audio reference design.
The XU316 family has 1 MiB on-chip SRAM and programmable I/O. Its 0.9 V core
power figures are **budgetary**, 203 mW typical / 750 mW maximum for the 600 MHz
grade under stated conditions, excluding additional analog/I/O/board loads.
High-speed USB analog rails add load; the typical core number is not a complete
bridge budget. Different package variants have different I/O voltage support;
the QF60B/TQ128 choice must follow the actual interface requirement.
[XMOS XU316 datasheet](https://www.xmos.com/documentation/XM-015129-PC/html/rst/XU316-1024.html),
[USB audio guide](https://www.xmos.com/file/sw_usb_audio-sw_usb_audio-design-guide),
[manufacturer reference repository](https://github.com/xmos/sw_usb_audio).

RT1170 provides an M7 up to 1 GHz and M4 up to 400 MHz, 2 MiB SRAM, external
memory support, two USB controllers, audio interfaces, and MIPI/parallel camera
interfaces. Exact variant/package and clock timing matter; no pin-compatible
substitution is implied. New A/B silicon documentation and migration notes
also require revision-specific review.
[NXP RT1170 family](https://www.nxp.com/products/i.MX-RT1170),
[industrial datasheet](https://www.nxp.com/docs/en/data-sheet/IMXRT1170IEC.pdf).

i.MX8ULP integrates A35 application cores, M33 and audio DSP resources in separate
power domains. NXP's AN13914 reports approximately 425 mW SoC rail sum for its
full-frequency MP3 playback case and 224 mW for the reduced-bus case. These
are 128 kbit/s MP3 examples, not 192 kHz lossless/DSP measurements; external DDR,
wireless, storage, conversion loss and our analog subsystem are not that rail
sum. It would be incorrect to reject Linux as inherently multiwatt or to treat
the reduced-bus example as this product's runtime.
[NXP i.MX8ULP](https://www.nxp.com/products/i.MX8ULP),
[AN13914, Tables 11-12](https://www.nxp.com/docs/en/application-note/AN13914.pdf),
[AN13951 power-domain strategy](https://www.nxp.com/docs/en/application-note/AN13951.pdf).

## PCM, USB and physical resource budget

The following numbers are our arithmetic for **stereo**. Packed 24-bit samples
are distinct from a 32-bit transport container; high-resolution file bitrate
is not a fixed FLAC compression ratio.

| Rate | 24-bit PCM payload | 32-bit-container payload / memory rate | 64-bit/frame BCLK |
| ---: | ---: | ---: | ---: |
| 44.1 kHz | 2.1168 Mbit/s | 2.8224 Mbit/s / 352.8 kB/s | 2.8224 MHz |
| 48 kHz | 2.304 Mbit/s | 3.072 Mbit/s / 384 kB/s | 3.072 MHz |
| 96 kHz | 4.608 Mbit/s | 6.144 Mbit/s / 768 kB/s | 6.144 MHz |
| 176.4 kHz | 8.4672 Mbit/s | 11.2896 Mbit/s / 1.4112 MB/s | 11.2896 MHz |
| 192 kHz | 9.216 Mbit/s | 12.288 Mbit/s / 1.536 MB/s | 12.288 MHz |

192 kHz BCLK leaves only 1.73% frequency margin to 12.5 MHz; that is not a
setup/hold timing margin. Current SSI1_B reservation is P702/F13 BCLK input,
P701/F15 LRCLK input and P700/F12 TX data. Prior RA-to-DAC timing assumed a
50% duty clock, 20 ns maximum RA transmit delay only in the qualified >=2.7 V
domain, and 25 ns at lower voltage. Recalculate against the eventual DAC,
actual voltage, duty cycle, load, skew, flight time and jitter; close LRCLK
and hold as well as data setup. 384 kHz at 64 bits/frame needs 24.576 MHz and
is excluded on this route. The new DAC choice may change clock direction,
but must not create contention at reset or during source changes.

At USB high speed, 192 kHz stereo in 32-bit containers averages 192 bytes
per 125 us microframe (24 stereo frames); provision at least one extra frame,
200 bytes, for a positive clock-rate deviation. This is a sizing floor,
not a descriptor ready for release. At full speed the same format needs
1536 bytes per 1 ms frame, beyond a single 1023-byte FS isochronous transaction;
even packed 24-bit needs 1152 bytes. Therefore 192 kHz stereo needs USBHS.
Define a lower-rate fallback descriptor set; do not let full-speed negotiation
retain an impossible stream. Protocol basis:
[USB 2.0 specification](https://www.usb.org/document-library/usb-20-specification).
See also the explicit frame/microframe and 1023-byte FS transfer description in
[Microsoft isochronous transfer documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/transfer-data-to-isochronous-endpoints).

Reserve a playback OUT endpoint, feedback IN endpoint and control endpoint,
with an explicit pipe/FIFO/DMA allocation; any capture, HID or update endpoint
is additional. The number of pipes does not prove every pipe supports every
transfer type. USB SOF capture and actual DAC-domain consumption measurement
must be physically available. If counting SSI DMA words, establish a frame
boundary and FIFO occupancy correction rather than treating a burst transfer
as instantaneous DAC consumption. Feedback must track the audio clock, not
the CPU clock. Use one coherent source clock in descriptors, explicit feedback,
and tested suspend/resume/stop/rate transitions.
[Microsoft native UAC2 requirements](https://learn.microsoft.com/en-us/windows-hardware/drivers/audio/usb-2-0-audio-drivers).

Do not tie audio sampling to the Wi-Fi packet arrival clock. Own-server input
is a buffered file/stream; compressed decode produces PCM into the independent
DAC-domain playback buffer. Bit-perfect operation excludes EQ, gain changes
and sample-rate conversion except explicitly declared bypass operations.
Native DSD remains optional: there is no requirement to add FPGA hardware for
it. DSD with PCM DSP requires conversion or a bypass contract. Physical DSD
pin modes, supported clocks and rate limits must be verified after DAC selection.

## C6 radio is useful, but current transport speed is insufficient

C6 offers 2.4 GHz Wi-Fi; its USB Serial/JTAG is fixed function and cannot serve
as the programmable UAC2 device. Its published 150 Mbit/s Wi-Fi PHY rate is
not host-link goodput. At 3.3 V, the datasheet's 78 mA RX example is about
257 mW, with CPU idle/peripherals disabled; 354 mA TX example is about 1.17 W
at 100% transmit duty. Neither is the complete streaming average. Bursty
buffer fills, signal strength, retransmissions and host transport need
measurement. [C6 datasheet](https://documentation.espressif.com/esp32-c6_datasheet_en.html),
[fixed USB block](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/usb-serial-jtag-console.html).

Current stable ESP-IDF C6 documentation explicitly excludes Bluetooth Classic
and marks ESP-BLE-ISO and ESP-BLE-AUDIO unsupported. Thus the present C6 can
provide control BLE/Wi-Fi, but cannot be approved for ordinary A2DP/LDAC/aptX
or LE Audio playback. This is stronger evidence than inferring features from
a Bluetooth 5.3 label. If wireless headphones become required, revisit the
radio subsystem; the preliminary S31 datasheet is an investigation candidate,
not a stocked drop-in replacement.
[Espressif C6 support matrix](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/ble/overview.html).

The placed/reviewed host transport uses SCI0 Simple SPI, not SDIO and not UART:
P601/P4 clock, P603/P1 COPI, P602/P2 CIPO, P604/N2 GPIO CS; READY/HANDSHAKE
are retained. Its initial 5 MHz evaluation point allows at most 5 Mbit/s in
one direction **before** framing and gaps, less than 9.216 Mbit/s packed or
12.288 Mbit/s containerized 192 kHz stereo. Full duplex does not double a
one-direction receive budget. Compression cannot be assumed to make every
lossless file fit. Even 96 kHz packed PCM nearly consumes the raw 5 MHz link.

Define >=20 Mbit/s sustained useful host receive capacity as an initial
192 kHz hardware transport target, including control traffic reserve. For
illustration, 50% payload efficiency would require 24.576 MHz SPI to carry
12.288 Mbit/s PCM, and 40 MHz to meet that 20 Mbit/s useful target. These are
arithmetic requirements, not a statement that SCI0 + translator + C6 can run
there. The existing TXU0304 round-trip delay, C6 output delay, SCI receive
setup, duty/load and cache/DMA scheduling must close at the chosen rate.
If they do not, examine SDIO or a different radio interface rather than
silently reducing the product's maximum file/stream format.

Espressif documents SDIO transports and presents measured hosted-network
throughput; its C6/Linux SDIO results exceed the target in the published setup.
That is not a RA8P1 SCI benchmark. SDHI0_C's optional managed-storage reservation
could be reconsidered for radio only after package pinmux, SDIO support and
power isolation are verified; microSD SDHI1_B remains mandatory.
[ESP-Hosted transport guidance](https://github.com/espressif/esp-hosted-mcu/blob/main/docs/getting-started-mcu.md),
[Espressif measured Linux transport results](https://github.com/espressif/esp-hosted-linux),
[SDIO protocol](https://github.com/espressif/esp-hosted/blob/master/esp_hosted_fg/docs/sdio_protocol.md).

## Memory, storage and camera coexistence

At 192 kHz, a 64-frame stereo float32/32-bit block is 512 bytes and lasts
333.3 us; a 256-frame block is 2048 bytes and lasts 1.333 ms. Double-buffer
storage is twice those values. A 100 ms PCM ring requires 153600 bytes;
five seconds require 7.68 MB. Put short audio/DMA buffers and latency-critical
DSP state in qualified internal SRAM; place long network/file prefetch and
images in external SDRAM. Internal SRAM is not automatically uniformly DMA
accessible or coherent: choose regions, MPU/cache properties and ownership
boundaries explicitly. Never claim real-time safety from total RAM size alone.

Current 64 MiB SDRAM is enough for sensible audio buffering by capacity, but
camera/display bandwidth dominates. A 1448 x 1072 display image takes
776128 bytes at packed 4-bit gray, 1.552 MB at 8-bit gray, or 4.657 MB RGB888,
before double buffers/artwork. An illustrative 1920 x 1080 camera at 30 fps
and two bytes/pixel produces 124.416 MB/s **per camera**, before reads,
conversion or compression. These are stress examples, not selected sensor
modes. Audio's 1.536 MB/s is small in comparison but must receive bounded
service latency. Scheduling camera capture at lower rates or forbidding
concurrent high-rate capture is a product contract to define, not an excuse
to drop a camera.

Preserve 4-bit native microSD, current NOR and SDRAM. Bulk SD latency, flash
erase/program stalls, cache misses, and camera bus arbitration require
prefetch rather than immediate block fetch inside a playback interrupt.
NOR firmware/assets capacity does not replace mass storage for a music
library. A 192 kHz 24-bit stereo hour of uncompressed PCM is 4.1472 GB;
filesystem/card capacity and sustained read qualification must follow the
actual use case. [Renesas SDHI driver](https://renesas.github.io/fsp/group___s_d_h_i.html).

Current SDRAM design's 250 mA branch allocation is a maximum design budget,
not a playback average: the selected ISSI -7 active table itself has a
210 mA figure with outputs open. Clock-gating/self-refresh and correct
burst behavior are important to battery life. Do not scale that figure
linearly with playback sample rate or call external memory free.
See CMS-010B and the complete ISSI sourcing/timing record in
[camera/storage interfaces](camera_storage_interfaces.md).

## DSP capacity and precision contract

Ten biquads per channel at 192 kHz evaluate 3.84 million sections/second.
Using five multiplies and four adds per section gives 19.2 million multiplies
and 15.36 million adds/second, excluding loads, stores, coefficients, block
control, crossfeed, resampling, decoding and USB/network service. Operation
count is not CPU cycles. At 250 MHz, a 30% CPU budget permits only 19.53
cycles/section before those additional operations; at 1 GHz it permits
78.125. Benchmark the actual optimized implementation and memory placement
at power-efficient clocks before deciding a dedicated DSP is required.

Provide sufficient capacity for float64 coefficient generation and numerical
reference, with float32/Helium, float64 processing or high-precision Q31 as
serious execution alternatives. Float32 has 24 significant bits; recursive
high-Q low-frequency filters at 192 kHz can accumulate coefficient/state error.
Do not promise arbitrary filters are transparent merely because arithmetic
is floating point. Compare impulse/step response, response error, limit
behavior and quantization against float64 reference. Q31 needs explicitly
scaled coefficients, wide states/accumulators and overflow bounds.
CMSIS supplies floating-point biquads and a Q31 form with 64-bit states;
the choice must follow tested numerical error and runtime, not word size alone.
[Arm biquad documentation](https://arm-software.github.io/CMSIS-DSP/v1.14.3/group__BiquadCascadeDF2T.html),
[Arm high-precision fixed-point implementation](https://github.com/ARM-software/CMSIS_4/blob/master/CMSIS/DSP_Lib/Source/FilteringFunctions/arm_biquad_cascade_df1_32x64_q31.c),
[current CMSIS-DSP](https://github.com/ARM-software/CMSIS-DSP).

Bound user filters and aggregate gain. For an illustrative +12 dB aggregate
EQ boost, +6 dB positive ReplayGain and +3 dB mixing allowance, reserve
21 dB by appropriate preattenuation; this is a test scenario, not a mandatory
fixed attenuation. Summed peak frequency response, internal states and filter
transients must be checked. Unlimited positive gain or unbounded convolution
cannot have a finite hardware guarantee. Preserve mute/safe gain when data
contains NaN/overflow or control transitions are interrupted.

Loudness, balance and crossfeed add modest processing compared with long FIR
or resampling, but speaker mode needs a qualified 192-to-48 kHz path or a
host rate change. Do not add a dedicated DSP/FPGA merely for ten PEQ bands.
Long user FIRs and DSD conversion are separately bounded options, not covered
by the biquad operation count. ReplayGain metadata parsing is firmware scope;
the hardware contract is adequate precision, gain range and buffer capacity.

## Qualification gates, energy and sourcing

No platform has passed the following tests. A provisional Stage 6 recommendation
may identify a preferred platform and fallback; final integration/performance
release requires these tests, and interface timing must close before wiring:

1. Native RA8P1 UAC2 high-speed stereo at every rate family through 192 kHz,
   explicit feedback and exact FIFO/pipe allocation, across USB hosts/phones;
   measure consumption/feedback, suspend/resume and clock changes. Record an
   actual interface timing closure; class-driver availability is insufficient.
2. Sustained own-server transport >=20 Mbit/s useful data at a defensible signal
   strength, with BLE control/retransmission and UI load, plus bounded gaps
   absorbed by declared buffering. Capture host SCI timing and powered-off
   isolation at the selected speed. Use raw/incompressible data as well as FLAC.
3. Stereo ten-band PEQ at 192 kHz plus crossfeed/balance/gain with numerical
   comparison, exact worst-case CPU cycles and active power. Benchmark lossless
   decode separately; require combined worst-case service time <=50% of the
   processing block period as an initial engineering margin, zero underruns
   during documented stress, and bounded refill after storage/network stalls.
4. Coexistence: camera modes, e-paper refresh, front lights, touch, five buttons,
   NOR access, microSD and radio interrupt bursts. Define concurrent camera
   modes, memory arbitration and DMA priorities. Native interface reservations
   are necessary but do not prove throughput or interrupt latency.
5. Power measured at battery/system entry: local 44.1/48 and 192 kHz, Wi-Fi
   buffered streaming, DSP on/off, display/light/camera activity, USB DAC,
   standby and wake. Preserve Stage 1's 10-hour local / 8-hour streaming
   allocations and 20-30 Wh investigation; compute runtime using complete
   board average power, aged/cold capacity and conversion losses.
6. Recovery and output safety independent of application OS: watchdogs,
   firmware-independent forced off, secure/recoverable update, hardware
   headphone DC/rail/thermal disconnect and wet-port inhibition. A Linux
   companion must not acquire sole responsibility for these functions.

Architecture power comparisons must include processor + active/retained RAM,
boot/storage, radio, bridge, regulators and clocks. Power-gate unused NPU,
cameras, GPU/interface blocks and radio where actual wake/retention contracts
permit. The 20 Wh Stage 1 endpoint permits only 1.6 W complete local average;
an audio bridge consuming a few hundred milliwatts can materially reduce
runtime even if it simplifies USB. Conversely, retaining a large host at
full speed without measured need may consume more than an optimized companion.

No exact new platform component is selected, so all-new BOM costs remain
unapproved. Manufacturer sourcing observations are dated and not reservations:

| Part family | Approximate price / sourcing evidence | Open commercial gate |
| --- | --- | --- |
| Existing RA8P1 UC0 | Exact manufacturer page lists Active; aggregated inventory includes Mouser 314 and DigiKey 1 when read. It does not expose an exact price. A different FLCAB listing shows about $18, which is context only and cannot populate the FLCAC BOM. | Exact single-unit quote, MOQ distributor terms, UC0/UC1 change/errata and production horizon. |
| C6 | Existing radio circuit/module sourcing is retained. No new price or replacement selection is asserted. | Active module exact ordering code, antenna/enclosure and verified transport. |
| XU316 | Manufacturer lists current family/reference documentation; no silicon unit price was exposed. The $245 evaluation board is not a chip quote. | Authorized single-piece stock/price, package/grade and firmware/tool support. |
| RT1170 | Manufacturer lists Active family variants; RT1172CVM8A budgetary figure is $8.89 at 10k, not an RT1176 single-unit quote. | Exact dual-core revision/package choice and authorized stock/price; no inherited camera timing approval. |
| i.MX8ULP | Current NXP family/power notes reviewed; exact part price unavailable in returned page. | SoC + DDR + PMIC + boot storage + wireless total quote, availability and lifecycle, not SoC price alone. |

Price-context sources: [Renesas other ordering code](https://www.renesas.com/en/products/ra8p1/part-details/r7ka8p1kflcab-uc0),
[NXP budgetary RT1172](https://www.nxp.com/part/MIMXRT1172CVM8A),
[XMOS evaluation board](https://www.xmos.com/xk-audio-316-mc-ab).
Unavailable prices are explicitly open rather than invented estimates.

The engineering disposition is to benchmark the present host candidate and
retain the dedicated bridge and heterogeneous alternatives for Stage 6.
This is a research order, not a final processor recommendation. Own-server
streaming does not itself demand Linux; demanding headphones do not demand
a different digital processor. Clock-domain integrity, deadlines, energy
and preserved peripheral support determine the hardware decision. These
benefits are reliability/resource benefits; no processor brand establishes
an audible improvement if delivered PCM and clock behavior are equivalent.

Arithmetic was independently reproduced with Python during this study.
No firmware, CAD, symbol, native BOM or export is changed by this file.
