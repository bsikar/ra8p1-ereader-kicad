# External audio review: dispositions and revised work order

2026-10-05. Owner-supplied review assessed against CAD checkpoint 76bcde6,
firmware submodule 6196bf4 and manufacturer sources. This is a hardware
architecture correction record, not approval of the supplied recommendations
or a completed schematic. The review's imperative wording is third-party
advice. The owner subsequently explicitly adopted **PCM768/DSD512, premium
Bluetooth audio and the higher desktop output envelope as required**.
These replace the earlier optional-format and 2 W floor / 4 W stretch targets.
Specific recommended parts remain candidates, and the review's factual and
thermal errors remain corrected below. No firmware implementation is in scope.


## Owner-adopted target contract

- Stereo PCM through 768 kHz in up to 32-bit containers; native DSD64-512
  and DoP through DSD256. Preserve bit-perfect bypass; no unbenchmarked
  full-DSP promise at 768 kHz or on native DSD. Ordinary PCM DSP through
  192 kHz remains a required capacity/benchmark contract.
- Premium Bluetooth audio reception with SBC/AAC, LDAC, aptX HD/Adaptive,
  and qualification of aptX Lossless and LE Audio on the exact licensed
  image. These are required engineering work, not implied by QCC5181 alone.
  Per-role LE Audio and optional wireless-headphone transmission must be
  specified explicitly; receiver codec support cannot stand in for encoding.
- Externally powered balanced targets: 7.6 W/ch at 16 ohms, 6.4 W/ch at
  32 ohms, 4.3 W/ch at 64 ohms, 1 W/ch at 300 ohms and 0.5 W/ch at
  600 ohms. Provide >=17.32051 Vrms and >=1.0 A peak where required,
  with engineering margin. The review alternates burst and continuous
  language at 16 ohms: investigate sustained capability as the product goal
  and report a separately measured burst envelope; do not claim continuous
  acceptance from a short burst. Both channels, 35 C ambient and <=0.01%
  THD+N at rated continuous output form the proposed qualification contract.
  The published Topping <1% figures are comparison data, not proof of this
  stricter result. All intermediate load/level points require safe limiting.
- Quiet IEM operation, battery runtime, hardware protection and the complete
  e-reader functions remain required. Do not meet the higher desktop target
  by silently dropping these requirements or drawing unbudgeted battery power.

## Decisions that can be made now

- Keep RA8P1 as application/system master, C6 for Wi-Fi/control, microSD,
  both cameras, e-paper/frontlight, illumination, sensors and speakers.
- Keep the separate quiet OPA1622 path and ES9039Q2M conversion candidate.
  Neither is a completed or measured analog chain.
- Demote the sixteen-BUF634A bank from preferred implementation to research
  comparator. Its recorded idle power, sharing and recovery gaps justify
  reopening the amplifier choice even without the proposed higher ratings.
  Preserve its symbols and calculations as evidence; it is not wired as a bank.
- Make SDIO pin/timing/isolation assessment the next radio transport study.
  The 5 MHz SPI bring-up point is not an accepted lossless-streaming transport.
- Reopen Stage 6 transport/power selection before additional high-power CAD.
  Investigate XU316 as the primary high-rate bridge; compare a native <=192 kHz
  low-power fallback using explicit modes,
  energy and control/data routes. Do not freeze a package from a stock listing.
- Retain host-power-first/surplus-charge/full-battery-off requirements and
  independent protection. The review does not close the charger defaults,
  battery isolation, wet-port or thermal work already recorded.

## Findings checked against evidence

| ID | Disposition | Consequence / closure evidence |
| --- | --- | --- |
| EXT-01 | Confirmed radio bottleneck | 5 Mbit/s raw cannot carry worst-case 9.216 Mbit/s packed stereo 24/192, or 12.288 Mbit/s in 32-bit containers. Compression cannot guarantee the gap disappears. Prove >=20 Mbit/s useful payload for the existing 192 kHz target. |
| EXT-02 | Confirmed serial-clock boundary on the reviewed RA route | Existing HUM Table 70.75 analysis uses 80 ns minimum BCLK. 64Fs gives 12.288 MHz at 192 kHz and 49.152 MHz at 768 kHz. The latter requires another serial engine. Closing setup/hold at 192 kHz is still necessary. |
| EXT-03 | USB arithmetic valid; system proof missing | PCM768 stereo requires 768 bytes per HS microframe on average. Provision at least 776 bytes for one extra frame; real feedback range, service interval, pipe/FIFO/DMA and host behavior must be verified. Bandwidth alone proves neither UAC2 support nor gapless playback. |
| EXT-04 | Firmware class gap confirmed narrowly | At pinned 6196bf4, `ra8_usb_paud.c` identifies UAC1 and `ra8_usb_haud.h` limits sample rate to 192000. Those class APIs do not establish UAC2 high-rate operation. This review does not certify the entire HAL or claim every feedback mechanism is absent from the whole repository. |
| EXT-05 | XU316 is credible, exact proposed package needs revision review | Manufacturer QF60A I/O is 1.8 V only; QF60B has 3.3 V left/right/top domains and 1.8 V bottom. Compare B and TQ128 port availability against clocks, DSD, Bluetooth, RA return path, flash, recovery and control. A is not electrically interchangeable with B. |
| EXT-06 | USB mux proposal is incomplete | D+/D- switching does not switch VBUS, determine PD roles, isolate two sources or provide wet-port protection. Define attach detection for each host, a valid XU VBUS-sense source, internal host session power, disconnected defaults and muted handover. Never connect external PD voltage to an internal USB 5 V domain. |
| EXT-07 | External-input RA DSP path omitted from proposed diagram | When the PC owns XU's USB port, RA cannot simultaneously host that same device. A control UART is not an audio return path. Provide bounded bidirectional PCM (potentially SSI <=192 kHz with an RX reservation), or put that DSP in XU, or explicitly limit DSP by mode. The present SSI reservation has TX only. |
| EXT-08 | Bluetooth module is conditional | Feasycom publishes codec and digital-interface documentation, but exact image, licensed source/sink roles, aptX Lossless and LE Audio functions require confirmation. Codec capability is not universal transmitter capability. Separate Wi-Fi/BT RF coexistence and antenna budgets are needed. |
| EXT-09 | Benchmark comparison needs correction | Topping's specified maximum balanced powers use THD+N <1%, whereas the proposed acceptance target uses <=0.01%. These are different tests. Published table does not establish our 35 C sustained sealed-enclosure rating. DX5 II's SE headphone jack is 6.35 mm, not the review's claimed 3.5 mm. |
| EXT-10 | Higher output arithmetic mostly correct | 7.6 W/16 ohms needs 11.027 Vrms and 0.97468 A peak. 1 W/300 and 0.5 W/600 require 17.32051 Vrms; 17.3 Vrms is slightly below both strict targets. Protection, connector resistance and tolerance need additional margin. |
| EXT-11 | ADA4870 is a comparator, not a ready headphone solution | Four active legs have substantial bias power. Datasheet current, offset, control reference and short-circuit behavior need attention; see below. Discrete AB is another candidate, not a demonstrated winner. |
| EXT-12 | Fixed 55% efficiency does not qualify 65 W input | Recalculate Class-AB rail current versus load and level. Adaptive rails or lower charging/output may make 65 W appropriate; +/-18 V at low impedance does not support the supplied budget assumptions. |
| EXT-13 | High-rate clock idea is directionally valid | 45.1584/49.152 MHz provide 64Fs clocks at 705.6/768 kHz. Confirm ESS synchronous mode, clock ratio, duty/setup/hold, XU port mapping and muted clock switching. A nominal oscillator frequency alone does not establish a valid DAC mode. |
| EXT-14 | New exact-part sourcing is not accepted | Apply the existing four-part lifecycle/MOQ1/fit/value audit to every added part and module support BOM. No new exact code is approved by this review; sample offers and codec marketing are not procurement evidence. |

Primary sources: [RA8P1 HUM](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware),
[XU316 datasheet v2.0.0](https://www.xmos.com/documentation/XM-015129-PC/html/rst/XU316-1024.html),
[TI TMUXHS221](https://www.ti.com/product/TMUXHS221),
[ESS ES9039Q2M v0.2.2](https://www.esstech.com/wp-content/uploads/2025/06/ES9039Q2M_Datasheet_v0.2.2.pdf),
[Topping manual, English amplifier table p37](https://dl.topping.audio/um/dx5_ii.pdf).
The XU datasheet was available as manufacturer-indexed content; direct HTML
retrieval failed. Its complete latest revision remains a component-design gate.
TI also lists TMUXHS221F as a newer protected alternative; compare it rather
than silently adopting either mux. Mux fault protection is not moisture sensing.

## Radio redesign boundary

The current optional SDHI0_C reservation is CLK PD05/C16, CMD PD04/C14,
DAT0 PD03/C15, DAT1 PD02/B17, DAT2 PD01/B16 and DAT3 P111/E8. MicroSD
SDHI1_B stays assigned. These are existing reservations, not a newly verified
alternate-function map. The EK SCI8 console uses PD02/PD03 and must move.
Reconcile all final functions and native U1 pin names before wiring.

Espressif's C6 SDIO slave uses fixed GPIO18/19/20/21/22/23 for
CMD/CLK/D0/D1/D2/D3. Verify exposure on the exact WROOM module and remove
only the corresponding obsolete SPI/no-connect assignments in a reviewed
native migration. GPIO4/5 boot-time edge straps, module power switching,
pull-ups, SDIO interrupts, reset/recovery and off-state injection need review.
Four-bit SDR at 25 MHz is 12.5 MB/s raw; 25 MB/s requires 50 MHz. Neither
is measured goodput. The 20 Mbit/s goal is 2.5 MB/s useful payload, and does
not qualify worst-case network PCM768 (49.152 Mbit/s in 32-bit containers).

[C6 datasheet](https://documentation.espressif.com/esp32-c6_datasheet_en.html)
and [Espressif SDIO protocol](https://github.com/espressif/esp-hosted/blob/master/esp_hosted_fg/docs/sdio_protocol.md)
support investigating this transport. TXS0206A is only a candidate: qualify
clock feedback, load, bidirectional timing and isolation using the
[TI datasheet](https://www.ti.com/lit/ds/symlink/txs0206a.pdf). Do not place an
auto-direction shifter merely because it is described as an SD-card part.

## Bluetooth and clock ownership

The [FSC-BT1058 AT manual, section 5.3.4](https://document.feasycom.com/docs/audio/BT1058_EN/latest/_downloads/7180088450bb78ac84f71b268c5e9d52/FSC-BT1058_AT_Command_Set.pdf)
lists AAC/SBC/aptX/Adaptive/HD/LDAC with an explicit source/encoding caveat.
Its wording must be clarified per codec and firmware image; it is not a
guarantee of LDAC transmission to headphones. The
[module datasheet](https://document.feasycom.com/docs/datasheet/BT1058/FSC-BT1058_Datasheet_EN.pdf)
gives digital master/slave timing and a configurable I/O supply domain.
Electrical slave capability does not prove the supplied audio firmware can
follow our clock indefinitely. Define source clock ownership and drift
handling: module-clock-following DAC mode, a qualified ASRC, or adaptive
clocking. Simply writing "QCC -> XU/ASRC" leaves a missing subsystem.
ASRC use also means that mode is not bit-perfect. Document recovery/update
access and module charger-pin handling; do not accidentally enable a second
battery charger. Vendor inquiries require owner-authorized communication.

Native DSD is not universally driverless UAC2 interoperability. Specify
OS/driver/container support per source. DSD256 DoP needs 705.6 kHz PCM
framing at 16 payload bits per channel/frame; DSD512 DoP would need
1.4112 MHz, outside a PCM768 ceiling. Native DSD512 bandwidth is 705.6
bytes/HS microframe on average. DSP on DSD requires conversion or bypass.
Speaker output needs its own supported-rate path and SRC/rate-negotiation
contract; high-rate clocks cannot simply be applied to the existing speaker
branch. Hardware compatibility and firmware implementation remain distinct.

## Corrected power screen

For stereo balanced Class B with four driven legs, rail magnitude Vs and
sinusoidal peak load current Ip, ideal output-stage DC input is
`Pdc = 8*Vs*Ip/pi`. Each leg carries the full load current, not half.
An illustrative Class-AB bias allowance is `Pidle = 4*2*Vs*Iq`.
Then amplifier heat is `Pdc + Pidle - 2*Pout`. This approximate screen
excludes driver, ballast, fault, converter and dynamic losses; it is not a
device simulation or a guaranteed efficiency.

At 7.6 W/channel into 16 ohms, use the review's 5 W other load, 10 W
charging, 90% conversion and 20% source margin. Allocate 32.5 mA per leg
for illustration, derived from ADA4870's +/-20 V, 25 C table; it is not a
guaranteed quiescent current at every rail below.

| Rails | Ideal signal-stage DC W | Bias allowance W | Amplifier heat W | Source incl. charge and margin W |
| --- | ---: | ---: | ---: | ---: |
| +/-10 V | 24.820 | 2.600 | 12.220 | 56.560 |
| +/-12 V | 29.784 | 3.120 | 17.704 | 63.872 |
| +/-15 V | 37.230 | 3.900 | 25.930 | 74.840 |
| +/-18 V | 44.676 | 4.680 | 34.156 | 85.808 |

Low-rail swing/current/SOA has NOT been qualified. The table explains why
load-dependent rails matter; it does not select +/-10 V. At +/-18 V the
no-charge source screen is 60.396 W before the 20% margin, and the amplifier
alone dissipates about 34.16 W. Converter and other-device heat increases
enclosure load. Charging adds battery/charger heat; stored energy is not
itself enclosure heat. A 65 W label does not close this system budget.

For SPR 20 V, more than 60 W requires current above 3 A and a qualified
5 A electronically marked cable/contract. Input selection, inrush, OVP,
reverse blocking, source-loss behavior and rail discharge must cover both
ports. Do not add two port wattages without an actual combining architecture.
Maintain battery-independent desktop operation and shed charging first.
See [TI's SPR/EPR power-range overview](https://www.ti.com/lit/ta/ssztd49a/ssztd49a.pdf)
and [TI cable-current qualification guidance](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1334427/tps65987d-evaluating-an-usb-pd-source-chipset-usb-pd-source-controller-and-matching-dc-dc-converter-for-up-to-20v5a-and-stand-alone-mode).

[ADA4870 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/ADA4870.pdf)
does not establish the review's claimed adjustable current limit: it describes
typical 1.2 A short protection when ON floats after enable; holding ON low
disables that protection. Control thresholds reference VEE, not board ground.
The listed offset can exceed the proposed headphone DC limit. Its 1 A drive
and 32.5 mA bias are not a hot 0.975 A-per-leg continuous guarantee. An
external precision loop, independent DC disconnect, safe controls and hot SOA
assessment remain necessary. This device is a possible comparator only.

`python scripts/check_audio_external_review.py` reproduces the transport,
load and rail-power arithmetic, cross-checking supply power by numerical
integration. Source/thermal assumptions remain explicit. Final ratings need
a load sweep, including intermediate output where Class-AB heat can peak,
both channels, 35 C ambient, time-to-equilibrium and touch/battery limits.

## Implementation order and acceptance gates

1. **EXT-A / RA8HW-4, RA8HW-18:** owner adoption recorded;
   finish the mode matrix with separate burst and continuous limits,
   weighting/bandwidth/distortion conditions and portable energy budgets.
2. **EXT-B / RA8HW-17, RA8HW-9:** complete SDIO package pin allocation and
   electrical timing/isolation/recovery proof. Then replace the native radio
   link in one connectivity-reviewed checkpoint; keep microSD/cameras intact.
3. **EXT-C / RA8HW-4, RA8HW-9:** compare native transport with XU316, select
   a port/voltage-qualified package, draw the external/local/BT/DSP/speaker
   mode matrix and USB VBUS/detach ownership. Exact boot flash, rails, clock
   and debug parts receive the full sourcing audit before native placement.
4. **EXT-D / RA8HW-4, RA8HW-18:** compare discrete AB and integrated power
   candidates with adaptive-rail options at all loads, including hot SOA,
   idle energy, compensation, output Z and fault clearing. Establish enclosure
   heat limits before promising the review's sustained ratings.
5. **EXT-E / RA8HW-18:** finish dual-input PD selection, bounded digital
   preregulation, battery isolation, reset-safe charger/NTC and wet inhibition.
   Size the source and cable from EXT-D; do not freeze 65 W by analogy.
6. **EXT-F / RA8HW-4:** complete DAC/I-V/filter/attenuation, line/quiet paths,
   independent DC/rail/overcurrent/temperature disconnect and jack interlocks.
   Higher line maxima remain a separate proposal to justify against load and gain needs.
7. **EXT-G / RA8HW-9:** native integration, exact-source BOM, full PDF/ERC,
   corner calculations and a prototype validation matrix. No documentary
   check closes physical noise, power, ingress, stability or fault tests.

These entries map to existing YouTrack ownership; they are not claims that
new issues or comments were posted. The adopted requirements are not implemented yet. Current schematic/BOM stays at 305
included references, 79 selected codes and two unresolved references. The
26 unplaced/archived symbols remain separate. No new IC was added by this
review. The existing PDF depicts the current incomplete implementation;
the earlier bank note/architecture is superseded by this disposition record
until a qualified replacement is implemented natively.

Checkpoint validation: new transport/load/rail calculations and independent
numerical integration pass; clock checks and `git diff --check` pass. All
15 native PDF pages were regenerated, rendered and visually reviewed and
are pixel-identical to the prior export. ERC finding records remain identical:
103 errors, 15 warnings and four existing ignored check categories. No
schematic, native BOM or submodule source was changed in this checkpoint.
