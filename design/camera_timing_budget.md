# CMS-017: Second-camera timing and bandwidth screen

2026-09-27. Supplements CMS-016 in [camera allocation](camera_storage_interfaces.md).
This is a necessary-condition screen, not a selected operating mode or electrical
signoff. Native CEU host ports exist; the external circuit is still unplaced.

## Host timing limits

[Renesas RA8P1 datasheet Rev.1.30, Table 2.77, p205 and Figures 2.108/109, p206](https://www.renesas.com/en/document/dst/25574255)
requires, at VCC >=2.70V: clock period >=11.5ns, each clock phase >=40% of
the period, data/HD/VD setup >=2ns for rising-edge capture (2.5ns falling),
and hold >=3.5ns. The period-only ceiling is 86.956522MHz, not a practical
target. [Renesas FSP CEU documentation](https://renesas.github.io/fsp/group___c_e_u.html)
also limits VIO_CLK to the CEU operating clock PCLKA, including jitter.

The selected bus transfers one byte per clock. Its payload must fit below
both limits, with time for blanking. Memory arbitration imposes another
constraint. An 8-bit bus does not mean an 8-bit-per-pixel image: RGB565 and
YUV422 require two transfers per pixel.

## Sensor and assembly evidence

[OV5640 v2.03](https://cdn-learn.adafruit.com/assets/assets/000/118/994/original/OV5640_datasheet.pdf?1677598686=),
Table 8-5, printed p8-4, lists 48MHz typical and 96MHz maximum PCLK with
mode-specific footnotes. The 96MHz case exceeds the host period limit.
Its DVP Figure 6-7 and Table 6-7 describe frame/line timing; they do not
provide a bounded data-to-PCLK skew for the proposed assembly/interconnect.
Do not infer electrical setup/hold margin from a frame diagram or assume
that the onboard 24MHz input oscillator fixes output PCLK to 24MHz.

Table 7-2, printed p7-7, explicitly lists SCCB_ID register 0x3100 as R/W,
default 0x78. This is evidence of a sensor address register, beyond the
driver constructor argument discussed in CMS-016. It does not yet qualify
a shared-bus startup/recovery sequence. Both modules initially collide at
7-bit address 0x3C; reset, brownout and address restoration must be handled.
Retain independent control paths or a qualified mux until that is resolved.

The [Waveshare OV5640 schematic](https://files.waveshare.com/upload/1/1e/OV5640-Camera-Board-Schematic.pdf)
was visually inspected: DOVDD connects to 3.3V, so it does not close the
existing sensor-versus-assembly supply discrepancy. The
[Arducam OV5640D AF module Rev.1.0](https://blog.arducam.com/downloads/modules/OV5640/5Megapixel_OV5640D_AF_CMOS_Camera_Module_DS.pdf)
defines a different 22-contact interface; its contact table alone does not
establish output thresholds, timing or powered-off isolation. Neither is
selected as a replacement in this review.

## Reproducible payload screen

Run `python scripts/check_camera_budget.py`. The script uses exact fractions
for the clock limit and payload comparisons. Two-frame storage assumes
uncompressed 16-bit pixels with no stride padding. Rates exclude blanking,
refresh/stalls, copies, image processing, and all other system traffic.
“Not excluded” means only that this lower bound fits; it is not acceptance.

| Candidate mode | Active payload MB/s | Two frames MiB | 48MHz bus lower-bound screen | CEU period-only ceiling screen |
| --- | ---: | ---: | --- | --- |
| 640x480, 30fps | 18.432000 | 1.171875 | Not excluded | Not excluded |
| 1280x720, 30fps | 55.296000 | 3.515625 | Reject | Not excluded |
| 1920x1080, 30fps | 124.416000 | 7.910156 | Reject | Reject |
| 2592x1944, 7.5fps | 75.582720 | 19.221680 | Reject | Not excluded |
| 2592x1944, 15fps | 151.165440 | 19.221680 | Reject | Reject |

VGA30 is a useful low-bandwidth configuration to investigate, not an owner
requirement or a reduction of still-image capability. JPEG is a separate
variable-length transfer contract: choose a CEU-supported framing mode,
bound buffers, and define overflow recovery rather than assuming an average
compression ratio. Full-resolution still capture and concurrent MIPI
operation remain open.

## Required closure before external-camera placement

- Exact assembly and connector revision, operating rails, current/inrush,
  autofocus load, sequencing and guaranteed logic levels.
- PCLK duty/jitter and data/HD/VD skew at the selected mode and load; add
  level-translator skew, cable/trace skew and receiver setup/hold. The 22pF
  PCLK load on the Adafruit candidate is already present on its board.
- Independent SCCB access, reset/power-down control and all-off injection
  protection. Do not use software power-down as a physical power switch.
- Capture format, frame timing, PCLKA and actual memory-bandwidth allocation
  alongside MIPI, display, audio, radio and storage.

The four lighting channels retain separate current/thermal budgets; none
of these throughput calculations accounts for their battery load.

## CMS-018: DC levels and translation decision (2026-09-27)

Direct wiring is rejected for a camera using the documented 1.8V I/O
condition. RA8P1 Table 2.5, printed pp47-48, applies 0.8*VCC VIH and
0.2*VCC VIL to the remaining peripheral inputs, including CEU. Both host
VCC domains use the main rail; its conditional 3.151819680..3.393012496V
envelope requires a worst-case high of 2.714409997V and low below
0.630363936V. OV5640 Table 8-3, printed p8-3, gives VOH >=1.62V and
VOL <=0.18V at the documented conditions with 25pF output loading. The
resulting high margin is -1.094409997V; low margin is +0.450363936V.
These sensor numbers are not stated as supply-proportional formulas:
do not extrapolate them to 2.8V or 3.0V to approve a different module.

[TI SN74AXC8T245, SCES875C, January 2024](https://www.ti.com/lit/ds/symlink/sn74axc8t245.pdf)
is a translator candidate, not a placed or sourced part. Sections 5.3/5.5
give input thresholds 0.65/0.35 times supply in the 1.1..1.95V range.
At exactly 1.8V, both sensor-to-translator DC margins are 0.45V. With its
output supply on the host rail and static loading <=100uA, VOH >=VCCO-0.1V
and VOL <=0.1V give host margins >=0.530363936V. This does not qualify
dynamic edges, actual load, or sensor supply tolerance.

Section 5.11 gives A-to-B delay 0.5..5ns for 1.8-to-3.3V translation
under the specified test conditions. Allocate 4.5ns independent-path
spread; do not treat typical channel matching as a guaranteed bound.
Section 6 uses 15pF, generator slope <=1ns/V, and half-supply crossings;
receiver threshold/edge uncertainty is additional. OE/DIR reference VCCA;
pull OE high by default and qualify ramp isolation separately.

Our resulting rising-edge timing requirement is sensor setup >=6.5ns and
hold >=8ns, before cable/trace skew and jitter, if both clock and data
take such translator paths. That requirement is still unproven. Eleven
video signals need more than one eight-channel device; no inter-device
matching credit is assumed. SCCB is bidirectional open-drain and needs
its own suitable interface; this direction-controlled video candidate
does not resolve SCCB, reset, power-down, or autofocus supply.

`check_camera_budget.py` reproduces these margins with exact fractions.
Next implementation prerequisite: identify an assembly with documented
I/O rails and sufficient output timing, then qualify its regulator,
isolation, connector and operating mode together. The candidate breakout's
3.3V supply discrepancy remains unresolved; no camera-side circuitry was
placed on the strength of these screens.

### Alternative assembly lead

ST's [MB1379 A05 reference](https://www.st.com.cn/resource/en/schematic_pack/mb1379-2v8-a05-schematic.pdf),
dated August 19, 2020, names HDF5640-AF-V2.0 with separate AVDD/AF-VCC
2.8V, DVDD 1.5V, and selectable DOVDD 1.8/2.8V. This is a useful lead
for a camera supply architecture within the sensor's published range.
The [B-CAMS-OMV product](https://www.st.com/en/evaluation-tools/b-cams-omv.html)
bundles that daughterboard with an adapter; it is not a separately qualified
bare-flex procurement item. A05 text was retrieved, but local PDF download
and visual jumper tracing remain pending. Do not infer shipped configuration
from the selectable-voltage note.

A [Dogoozx catalogue listing](https://dgzx.hk/product/5mp-yuv-2k-1080p-ov5640-af-auto-focus-scan-code-camera-module-manufacturer-dvp/)
uses the same HDF5640-AF-V2.0 name, but no matching electrical drawing,
revision, guaranteed timing/current limits or distributor sourcing was
established. A matching name alone does not qualify a substitute. Next
research should trace the A05 rails and obtain an exact assembly contract,
rather than repeating the already rejected direct-1.8V connection.

Independent review reproduced CMS-018 arithmetic and checked TI's source
conditions. No schematic or BOM changes were made for this research checkpoint.

### Connector identity checkpoint (2026-09-27)

The A05 schematic's CN1 is the bare-camera connector, FPC05024-03200;
CN2 is the different 40-contact daughterboard interface. The following CN1
inventory is transcribed from the manufacturer text, pending visual trace
review. These are camera contact names, not assigned RA8 nets.

| Contact | Signal | Contact | Signal |
| --- | --- | --- | --- |
| 1 | STROB | 2 | DGND |
| 3 | SDA | 4 | AVDD |
| 5 | SCL | 6 | RESET |
| 7 | VSYNC | 8 | PWDN |
| 9 | HREF | 10 | DVDD |
| 11 | DOVDD | 12 | D9 |
| 13 | XCLK1 | 14 | D8 |
| 15 | DGND | 16 | D7 |
| 17 | PCLK | 18 | D6 |
| 19 | D2 | 20 | D5 |
| 21 | D3 | 22 | D4 |
| 23 | NC | 24 | AF-VCC |
| 25 | Shield | 26 | Shield |

The eight exposed sensor data contacts are D2..D9. Do not connect host
D0..D7 by matching identical suffixes; establish byte significance from
the selected sensor format and trace the daughterboard's PAR_D0..7 first.
Contact-side orientation, mating flex and shield treatment remain open.

[ST UM2779 Rev.1, sections 3.3 and 4.2](https://www.st.com/resource/en/user_manual/um2779-camera-module-bundle-for-stm32-boards-stmicroelectronics.pdf)
clarifies a separate adapter configuration: MB1683 JP1 selects 2.8/3.3V
only for its Waveshare CN4. It does not select MB1379 DOVDD. The adapter's
MB1379 CN2 table has 1.8V at contacts 1/2 and 2.8V at 39/40; those are
not the bare-flex numbering above. Its pins 23..30 carry host D0..D7.
Thus neither the bundle's advertised 3.3V input nor JP1 proves the bare
sensor's I/O voltage. Preserve the distinction when selecting a module.

Local retrieval of A05 failed with connection reset/timeout on both ST
domains; web text was available, but no visually reviewed local A05 drawing
was obtained. No native connector or supply circuit is accepted by this
inventory. Next action is visual A05 tracing or an exact module drawing,
not another assumption based on adapter supply labels.

### Translator procurement checkpoint (2026-10-04)

The AXC candidate remains unplaced. Current DigiKey US listings report zero
stock for [PWR](https://www.digikey.com/en/products/detail/texas-instruments/SN74AXC8T245PWR/8567230),
[RHLR](https://www.digikey.com/en/products/detail/texas-instruments/SN74AXC8T245RHLR/8571519)
and [RJWR](https://www.digikey.com/en/products/detail/texas-instruments/SN74AXC8T245RJWR/9608021).
Expected deliveries are not available inventory. Do not select these ordering
codes as sourced parts on the basis of older regional search results.

An alternative research candidate is Nexperia **74AVC8T245PW,118**.
[DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74AVC8T245PW-118/2056830)
reports 641 available, cut tape quantity 1 at USD1.10 and quantity 100 at
USD0.63160. This is an unreserved snapshot, not a purchase or lifetime guarantee.

[Nexperia Rev.8, 25 June 2024](https://assets.nexperia.com/documents/data-sheet/74AVC8T245.pdf),
Tables 2/3, specifies PW pins: VCCA 1; DIR 2; A1..8 3..10;
GND 11/12/13; B1..8 21..14; active-low OE 22; VCCB 23/24.
All three GND pins must be grounded. DIR high selects A-to-B for all eight
channels. OE and DIR reference VCCA. This is a separate device contract:
do not inherit AXC pin 11's DIR2 function or its delay limits.

Table 12 gives A-to-B delay 0.5..3.5ns at VCCA 1.65..1.95V,
VCCB 3.3V +/-0.3V and -40..85C under the specified test conditions.
No camera mode is accepted by this observation. Next checks are Table 13's
extended-temperature limits, DC margins across the selected camera rail,
test loading/edge conditions, ramp isolation and eleven-channel allocation.
The module supply and output timing contract remain unresolved. No new
native symbol, circuit or BOM entry is claimed by this checkpoint.

### AVC library candidate and conservative timing (2026-10-04)

Native KiCad now contains `Power_Devices:SN74AVC8T245PWR`, copied into the
project library and checked against [TI SCES517K, Table 4-1](https://www.ti.com/lit/ds/symlink/sn74avc8t245.pdf).
The 24 PW contacts use the pin inventory above, including all three grounds
and both VCCB contacts as visible native stacks. It is unplaced: no camera
circuit, new schematic reference or BOM acceptance follows from this import.
Footprint assignment and package qualification remain deferred.

[DigiKey's exact PWR listing](https://www.digikey.com/en/products/detail/texas-instruments/SN74AVC8T245PWR/864331)
reported Active, 15,975 available, cut tape MOQ 1, USD1.63/1 and USD0.95970/100
on 2026-10-04. This unreserved snapshot is recorded in hidden symbol fields.

TI section 5.5 explicitly covers independent VCCA/VCCB ranges 1.2..3.6V
for VOH >= VCCO-0.2V and VOL <=0.2V at <=100uA static output loading,
over both published temperature ranges. With B and the receiver on the same
host rail, each host margin is at least 0.430363936V. Sensor-to-A margins
are 0.45V at the documented exactly-1.8V sensor condition. These do not
establish camera output limits over a supply-tolerance range or dynamic edges.

TI section 5.8 gives A-to-B delays 0.5..3.9ns through 85C and 0.5..12.1ns
through 125C, for VCCA=1.8V +/-0.15V and VCCB=3.3V +/-0.3V.
The independent-path spread allocations are 3.4ns and 11.6ns respectively.
Rising-edge sensor setup/hold must therefore be at least 5.4/6.9ns or
13.6/15.1ns before other uncertainties. Use the broader table above 85C;
do not interpolate or assume typical clock/data channel matching.
`check_camera_budget.py` reproduces these conditional allocations.

Figure 6-1 uses 15pF loads, input slope >=1V/ns and half-rail timing
crossings. Receiver threshold crossing, actual cable/load, jitter and skew
need additional bounds. Section 5.3 limits input transitions to 5ns/V.
OE/DIR reference A; default-disable OE needs a pull-up to VCCA.
Ioff is bounded at +/-5uA when one supply is at zero under section 5.5's
conditions; this does not establish behavior throughout power ramps.
Eleven video signals require multiple devices and separately qualified
control, bypassing and unused-input treatment. SCCB remains separate.

The Nexperia alternative remains on hold: its Table 7 static output-level
rows specify equal VCCA/VCCB, so the VCCO-0.1V/0.1V limits have not been
accepted for this unequal-rail interface. Table 13's 125C A-to-B range is
0.5..3.9ns, but favorable timing alone cannot close the DC contract.
The exact camera assembly, its supply configuration and output timing are
still unresolved. No capture mode is qualified by this checkpoint.

Validation: all 24 physical symbol contacts matched the PW table exactly;
preexisting library symbols were unchanged. KiCad's SVG export was visually
reviewed. The full 14-page PDF was regenerated, visually reviewed and every
page render matched the prior checkpoint. ERC remains 99 errors and 11
warnings, with unfinished connections retained. Current exported U26 and
Hall topology checks, camera arithmetic, clock checks and diff whitespace
checks passed. The empty deferred Footprint field retains its inherited
position; populated hidden metadata is at the origin.
