# RADIO-024: C6 SDIO migration

2026-10-05; EXT-B, YouTrack RA8HW-17 and RA8HW-9. Implementation contract
under qualification. The saved circuit still uses SCI0 Simple SPI; this record
does not claim that SDIO is wired or operating. RA8P1 remains system master.

## Allocation

Reassign the previously optional, unpopulated four-bit eMMC reservation to
the radio. Retain removable microSD on SDHI1_B and Octal NOR. Do not route
both an eMMC and the radio onto SDHI0_C as though they were independent buses.

| Function | U1 port / BGA289 ball | U3 GPIO / WROOM module contact |
| --- | --- | --- |
| SD0CLK_C | PD05 / C16 | GPIO19 / 17 |
| SD0CMD_C | PD04 / C14 | GPIO18 / 16 |
| SD0DAT0_C | PD03 / C15 | GPIO20 / 18 |
| SD0DAT1_C | PD02 / B17 | GPIO21 / 19 |
| SD0DAT2_C | PD01 / B16 | GPIO22 / 20 |
| SD0DAT3_C | P111 / E8 | GPIO23 / 21 |

Authority: [Renesas RA8P1 datasheet Rev 1.30, Table 1.17, 289-ball
column](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet) and
[Espressif WROOM-1/-1U datasheet v1.4, Table 3-1](https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf).
The 303-ball map is different. U1 P111 is unit B; PD01..PD05 are unit H.
All six host balls are unconnected in the checkpoint netlist. U3 contacts
16..21 presently have no-connect markers; remove those only as each native
connection is made. This is not permission to suppress ERC elsewhere.

### USB coexistence

PD04, PD03 and PD05 also offer USBHS_ID, USBHS_EXICEN and USBHS_OVRCURB.
They cannot simultaneously serve those alternate functions and SDIO.
Reserve PD06/C17 as an **unwired candidate** for USBHS_OVRCURA; reconcile
the completed USB/power pin budget before wiring it. EK SCI8 PD02/PD03
console assignments are also unavailable after this migration.

The RA8P1 User's Manual Rev 1.30 sections 38.2.1 and 38.2.3 (pages
2071-2073) make controller role software-selectable through SYSCFG.DCFM;
IDMON separately reports the ID input. Section 38.2.5 makes EXICEN an
external output control. Engineering inference: a fixed internal USB host
connection to the XU316 need not consume an OTG ID/EXICEN pair. Use explicit
host/device ownership and an independently protected supply path. Do not
configure these SDIO pads as USB pins. The complete USB mux, fault input,
VBUS detection and reset-state circuit is still pending; software role
selection alone does not establish safe power switching.

## Electrical architecture

Use 3.3 V signaling at both ends, with six bilateral isolation channels.
The existing TXU0304 fixed-direction SPI translator cannot perform this job.
Two **TMUX1511RSVR** devices, already used as U21/U22 on microSD, remain
an isolation candidate, not a selected complete interface. RADIO-025 found
insufficient guaranteed host-to-C6 high-level margin with a passive path;
resolve the DC gate below before placing them. Do not reuse microSD's
physical devices.

Proposed channel assignment, using fresh physical references when placed:

| Channel | First RSV16 device S / D / SEL | Second device S / D / SEL |
| --- | --- | --- |
| 1 | CLK: 2 / 3 / 1 | DAT2: 2 / 3 / 1 |
| 2 | CMD: 5 / 6 / 4 | DAT3: 5 / 6 / 4 |
| 3 | DAT0: 10 / 9 / 11 | Unused; SEL grounded |
| 4 | DAT1: 14 / 13 / 15 | Unused; SEL grounded |

On both devices pin 16 is +3V3_MCU, pin 8 GND, pins 7/12 package NC.
Add local 100 nF bypass per device. S/D are bilateral. Five CMD/DAT
pull-ups belong on +3V3_RADIO, not on an always-on supply. No CLK pull-up.
Select series damping and pull-up values from the final load/edge analysis;
do not copy the removable-card ESD bank onto an internal PCB link without
a reason. All six active SELs require a reset-safe common enable qualified
by valid radio supply, host reset, host request and service-mode exclusion.
Preserve the service UART, boot request and supervisor functions.

[TI SCDS390B Rev B](https://www.ti.com/lit/ds/symlink/tmux1511.pdf) supplies
the RSV16 pin map. At valid supply it gives 4.5 ohm maximum on resistance
and 6 pF maximum on capacitance under their stated tests. Powered-off leakage
is bounded at 2 uA with VDD=0 and signal up to 3.6 V. Its 67 ps propagation
and 10 ps skew are **typical**, not worst-case timing guarantees. Supply
turn-off can take 4 us under the specified 1 us falling-supply test; control
transition is at most 55 ns at 2.5..5.5 V under the specified load. Therefore
power removal alone cannot prove fast fault isolation. Analyze supervisor
assertion, gate delay, rail slew, capacitor hold-up and total injection.

TXS0206A was also examined. Its dedicated SD function is attractive, but
its B-to-A data delay can be 5.1 ns at 3.3/3.3 V, and its enable must be
held low until both supplies are stable. It does not remove the sequencing
proof. [TI SCES833B, sections 6.11 and 10](https://www.ti.com/lit/gpn/txs0206a).
It also fails as a remedy for the DC issue: section 6.3 requires CMD/DAT
VIH >= VCCI-0.2 V and VIL <=0.15 V. At 3.3 V, the high threshold is 3.1 V,
above the RA SD-output minimum. It is not selected.

### RADIO-025 DC compatibility gate

RA8P1 Rev 1.30 Table 2.7 specifies SD_A/B/C channel 0 and SD_B channel 1
VOH >=0.75*VCC at 2 mA and VOL <=0.125*VCC at 3 mA for VCC >=2.7 V.
Table 2.4 specifies SD input VIH=0.625*VCC and VIL=0.25*VCC.
The C6 chip datasheet v1.5 DC table at 3.3 V/25 C gives VIH=0.75*VDD
and VIL=0.25*VDD. Thus the equal-supply host-to-C6 high-level screen has
**zero guaranteed margin before switch/trace losses**. This is a missing
guarantee, not a claim that every physical board fails. Pull-ups and light
loading cannot justify inventing an improved guaranteed RA VOH curve.
The generic non-SD output row must not replace the SD-specific row.
[C6 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf).

The NXS0506 and NVT4857UK SD translators were screened, but their host-side
supplies stop at 1.95 V. They require a different host I/O voltage allocation,
including checking P111 and PD01..05 supply domains, rather than a drop-in
3.3 V substitution. No bank voltage change is authorized by this screen.
[Nexperia NXS0506](https://assets.nexperia.com/documents/data-sheet/NXS0506.pdf),
[NXP NVT4857UK](https://www.nxp.com/docs/en/data-sheet/NVT4857UK.pdf).

Procurement checked 2026-10-05: TI lists TMUX1511 active; DigiKey lists
82,239 TMUX1511RSVR in stock, cut-tape quantity one at USD 0.77 (10: 0.552;
100: 0.4345). Two ICs cost USD 1.54 at singles before tax/shipping. Stock
is unreserved and not a longevity guarantee. Existing native library sourcing
fields retain their earlier dated snapshot until the new instances are placed.
[Manufacturer](https://www.ti.com/product/TMUX1511),
[exact distributor offer](https://www.digikey.com/en/products/detail/texas-instruments/TMUX1511RSVR/9954161).

## Timing and throughput gates

Use <=400 kHz initialization and initially qualify four-bit operation at
25 MHz; pursue 50 MHz after actual endpoint and board timing closure.
Raw four-bit SDR capacity is 12.5 MB/s at 25 MHz, 25 MB/s at 50 MHz,
before command/CRC/turnaround/network overhead. Stereo PCM768 in 32-bit
containers consumes 6.144 MB/s; raw capacity is not guaranteed streaming
throughput. Buffering, Wi-Fi conditions and concurrent storage/camera traffic
still require system validation.

RA8P1 datasheet Table 2.76 specifies 20 ns minimum SD clock cycle at
VCC/VCC2 >=2.7 V, 50% duty, 3 ns maximum clock edge, output timing
-7..+4 ns, input setup 4.5 ns and hold 1.5 ns under the stated high-drive
settings. Figure 2.107 places output changes relative to the falling clock
edge and input sampling at the rising edge. At 25 MHz, the host's latest
+4 ns output leaves 16 ns to the next rising edge; its earliest -7 ns next
change leaves 13 ns after that sample. At 50 MHz those windows shrink to
6 ns and 3 ns. These exclude receiver setup/hold, board skew, path delay and
uncertainty; they are not closed timing margins.

Espressif C6 TRM v1.2 section 34.2 supports 0..50 MHz. Section 34.5.6
(page 1115) describes independent sample/output edge selection and its
register override priority. It does not provide numerical input setup/hold
or output-delay limits there. Obtain the applicable endpoint timing limits
or record explicit characterization bounds before claiming worst-case
25/50 MHz closure. TRM prose says FRC_SDIO22 where its register table on
page 1151 calls the rising-edge field FRC_SDIO20; use the actual register
definition when writing the later firmware contract.
[Espressif TRM](https://documentation.espressif.com/esp32-c6_technical_reference_manual_en.pdf).

U3 GPIO4/MTMS and GPIO5/MTDI select sample and output edges at reset; both
float by default. RADIO-025 now fits R114 pull-up on GPIO4 and R115 pull-down
on GPIO5, selecting rising-edge sample/falling-edge drive (WROOM Table 4-4).
GPIO4 retains the current SPI DATA_READY path through U25 until transport
migration. GPIO5's obsolete no-connect marker is removed. Remove the old
status loading when migrating; do not claim that these straps implement SDIO.
SDIO DAT1 provides the native host interrupt mechanism. Preserve a separate
status GPIO only if the hosted protocol actually requires it and allocate
it outside the strap group.

The pinned firmware's SDHI memory-card initialization sets SDIO_MODE=0.
It is not evidence of an implemented SDIO driver. Future firmware must
handle CMD5/52/53, CCCR/FBR, DAT1 IRQ, DMA/cache ownership, enumeration,
reset/recovery and bus width/speed negotiation. No firmware changes are
part of this hardware task.

## Native migration sequence and completion criteria

1. Resolve edge/DC levels, pull-ups, load budget and hardware enable gate.
2. Place the qualified interface and support parts with fresh references;
   if the bilateral candidate survives the DC gate, retain its package NC,
   grounded unused SELs and verified RSV map.
3. Replace SCI0 SPI and old DATA_READY/handshake routing through the MCU,
   root hierarchy and radio sheet. Wire the six SDHI0_C paths; remove the
   superseded U5/U25 circuitry only after preserved service functions are
   traced. Do not leave two driven transports attached to one GPIO.
4. Update optional eMMC reservation, native notes and power/capacitance/BOM
   budgets. Verify every endpoint with a fresh netlist, preserving all
   unrelated net partitions. Inspect all PDF pages and changed-sheet detail.
5. Compare ERC identities, not just counts; retain open electrical issues
   without suppression. Commit/push the coherent migration checkpoint.

Until these gates pass, neither SDIO implementation nor target radio
throughput is complete. This work is one dependency of the active full
electrical-design goal, not a replacement for the remaining audio/power,
display/camera/illumination and whole-system integration work.

## RADIO-025 strap implementation and qualification

R114/R115 use 10k, 1% RC0603FR-0710KL: R114.1 to +3V3_RADIO,
R114.2 to U3.4/U25.5; R115.1 to U3.5, R115.2 to GND.
The current U25 data input's weak pull-down is included in its 2 uA
125 C input-current limit under the stated rail-input test; it is not an
unbounded opposing resistor. Its 2.5 uA partial-power-down limit must also
be covered during sequencing. [TI TXU0102 Rev A, section 7.5](https://www.ti.com/lit/ds/symlink/txu0102.pdf).

Use Rmax=10k*1.01*1.01=10201 ohm and Rmin=10k*0.99*0.99=9801 ohm
for initial tolerance plus a 1% temperature allowance. A **12 uA adverse
leakage allocation**, not a measured all-corner C6 guarantee, produces
0.122412 V error. At the C6 documented 3.3 V DC test point, high is
3.177588 V versus 2.475 V threshold and low is 0.122412 V versus 0.825 V:
0.702588 V conditional margin in either direction. Do not extrapolate this
25 C table into an unqualified complete temperature guarantee.
Opposite-state drive at 3.6 V draws at most 0.367310 mA (rounded upward) and dissipates
1.322314 mW per resistor. Keep conflicting internal pulls/JTAG disabled
through strap sampling. Reset setup/hold, pad leakage across temperature,
ramp behavior and the future SDIO isolation circuit remain open.

Procurement exception discovered during fresh RADIO-025 validation:
DigiKey's 2026-10-05 page now reports **zero stock**, with 5,000 expected
2026-11-09, although MOQ1 cut tape is priced at USD 0.10. The copied native
September stock snapshot is historical and no longer proves availability.
R114/R115 and all existing instances of this MPN require sourcing refresh
or a qualified stocked substitute before purchase; this checkpoint is WIP.
[Exact offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0710KL/729827).

Fresh RADIO-025 netlist confirms those four resistor connections and preserves
every earlier pin partition. Native BOM export matches 307 included references
and four exclusions, all 19 columns. ERC identities remain 103 errors and
15 warnings, with no suppression added. All 15 PDF pages were rendered and
reviewed; only page 6 differs, with straps and the updated note inspected at
readable scale. These results validate this WIP checkpoint, not the SDIO bus.

## RADIO-026 sourcing refresh

The 2026-10-05 review found a quantity-one alternative distributor offer for
the **same** RC0603FR-0710KL; no electrical substitution is needed on this
evidence. [Mouser's exact listing](https://www.mouser.com/en/ProductDetail/603-RC0603FR-0710KL)
was returned by the search index with a last-week crawl: 2,782,034 stock,
cut tape minimum/multiple one, USD 0.10/1, 0.014/10 and 0.008/100.
The direct short-URL fetch timed out, so this is explicitly indexed evidence,
not a live inventory reservation. DigiKey's zero-stock finding remains valid
for that separate offer. Recheck stock, price and lifecycle before purchase.

Through the native Symbol Fields Table, all 47 matching instances received
the Mouser order code, link, price/stock and replacement sourcing snapshot.
Individual circuit selection and qualification notes were preserved. The
September snapshots are superseded; neither distributor inventory nor this
metadata edit establishes circuit qualification or remaining product life.

Fresh netlist comparison confirms identical connectivity and exactly those
four metadata fields changed for those 47 references. Native BOM fidelity
passes for 307 included references, four exclusions and 19 columns. ERC
identities remain 103 errors and 15 warnings without additional suppression.
All 15 refreshed PDF pages were rendered and reviewed; their pixels match
the previous checkpoint. SDIO voltage/timing and reset qualification remain
open; the six data/clock paths have not been installed.

## RADIO-027: preserve SDRAM rails; screen passive regeneration

Do not lower VCC or VCC2 to 1.8 V to accommodate a low-voltage-host SDIO
translator. [RA8P1 datasheet Rev 1.30, Table 2.2, page 45](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet)
requires VCC/VCC_DCDC >=3.00 V when SDRAM is used, and standard-mode VCC2
>=3.00 V when 32-bit SDRAM is used. Table 2.4 assigns SDRAM D00..D19 to
VCC and D20..D31 to VCC2. The generic 1.62 V minimum and the SD-interface
1.8 V operating rows do not override these conditions. This rules out that
workaround for the current memory architecture, not every possible RA8P1
system architecture.

[TI LSF0108 Rev M, sections 8.4.1 and 9.2.2](https://www.ti.com/lit/ds/symlink/lsf0108.pdf)
describes pass switches with independently selected pull-up levels. A lower
bias can isolate high states, allowing pull-ups to restore both sides to
their supplies. It is not an active buffer. TI estimates data rate as
1/(6RC); the driving pad must sink the sum of both pull-up currents.
Do not infer maximum data rate from propagation delay alone.

Illustrative engineering screen, **not a component selection or timing
guarantee**: equal 2.32k pull-ups with 1% initial tolerance and both supplies
at the allocated 3.393012496197 V maximum draw <=2.954557 mA with a zero-volt
low. This nearly consumes the RA SD-output 3 mA characterization current
before leakage and temperature allowances. With an assumed 10 pF receiver
load, the nominal RC tail from 1.8 V to the 3.3 V C6 input's 2.475 V high
threshold takes 13.869819 ns: R*C*ln((3.3-1.8)/(3.3-2.475)). This excludes
time to reach 1.8 V, switch effects, clock-path skew and receiver setup.
TI's conservative rate estimate is only 7.183908 Mbit/s per channel for
that R/C example. Neither number qualifies the planned 25 MHz bus.

Decision: retain the existing SPI wiring. LSF0108 has not established a
qualified fast replacement, and lowering the host banks would break a
documented SDRAM operating condition. A viable next solution must establish
DC margins, both-direction timing, initialization/turnaround and powered-off
isolation together. Do not repeatedly re-open the rejected host-voltage
workaround without changing the memory architecture. Other subsystem work
can continue independently of this interface qualification.

Checkpoint validation: native Save All regenerated only the audio child's
file UUID and persisted the BOM table's Procurement_Status grouping setting.
Fresh netlist components, library parts and complete net partitions match
RADIO-026; BOM fidelity passes for 307 included references, four exclusions
and 19 columns. ERC findings remain identical (103 errors, 15 warnings).
All 15 exported PDF pages were rendered, reviewed and found pixel-identical
to the previous export. Clock and external-review arithmetic checks pass.
These checks preserve the WIP circuit; they do not qualify SDIO operation.

## Earlier RADIO-024 checkpoint verification

Native RADIO-024 annotation added; no component or wire changed. Save All
also regenerated the audio child file's UUID without changing its contents
otherwise. Fresh exported netlist preserves every net partition from the
preceding checkpoint; the native BOM still matches all 305 included physical
references and four exclusions. ERC identities remain unchanged at 103 errors
and 15 warnings, with no new suppression. All 15 PDF pages were rendered and
reviewed; only radio page 6 differs, and its new note was inspected at readable
scale. Clock and external-review calculation checks pass. These results
verify the checkpoint, not SDIO operation or whole-design completion.
