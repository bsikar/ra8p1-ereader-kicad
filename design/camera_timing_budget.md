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
