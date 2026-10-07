# Auxiliary audio 5 V converter draft

U36 TPS630701RNMR is placed in the native headphone schematic. VIN 12/13
and VOUT 7/8 are tied; FB 5 senses VOUT. GND 4, PGND 10, VSEL 15 and unused
FB2 6 are grounded. PS/SYNC 1 is now grounded for forced PWM.
L3 connects switching pins L1 11 and L2 9, separately from ground.
C132 is the dedicated VAUX 3-to-ground bypass.
The converter is incomplete; this checkpoint supplies no new working rail.
Its intended source is the bounded low-voltage system bus, never raw 20 V PD.

[TI SLVSC58B Rev B](https://www.ti.com/lit/ds/symlink/tps63070.pdf), sections
5, 6 and 9.3, specifies the fixed 5 V variant without output discharge,
2-16 V input, FB connected to output, VAUX used only for its bypass capacitor,
and an optional unused FB2 left open or grounded. Forced PWM requires PS/SYNC
low; VSEL must have a defined state. PG is open drain. The fixed-output LC
criterion requires effective Cout in uF at least fifteen times effective L
in uH. Evaluate tolerance, bias and temperature, not nominal capacitance alone.
The advertised switch current is not a guaranteed continuous output rating.

[DigiKey 296-47298-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS630701RNMR/6175215)
was Active with cut-tape MOQ1, stock 7,383 and USD 3.37/1 on 2026-10-05.
This unreserved snapshot does not establish future lifecycle.

Next implement the input capacitor bank, default-off enable,
power-good interface and bounded source connection.
Then establish total auxiliary load, bus bounds, startup/shutdown, backfeed,
fault behavior, ripple and converter/LDO dissipation across temperature.
U35 and its relay coil remain dependent on this unfinished source.
Independent hardware headphone protection and relay gating remain open.

## Passive selection constraints (2026-10-05)

Use a 1.5 uH nominal shielded inductor as the starting point. With +20%
inductance tolerance, Lmax is 1.8 uH and the fixed-output capacitance criterion
requires at least 27 uF effective output capacitance. A nominal 68 uF bank
therefore needs at least 39.706% retained capacitance across tolerance,
temperature, DC bias and aging. A generic 80% capacitance-loss assumption
gives only 13.6 uF and fails. Do not approve a bank by nominal value alone.

[Coilcraft XFL4020, document 745-1 revised 2026-03-10](https://www.coilcraft.com/getmedia/50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf)
lists XFL4020-152MEC at 1.5 uH +/-20%, 15.8 mOhm maximum DCR at 25 C,
and 4.1/4.4/4.6 A for 10/20/30% inductance drop at 25 C. These are not
guaranteed hot-current limits. Its 6.7/9.1 A thermal-reference currents do
not establish saturation margin or application temperature. Packaging C
replaces the legacy B suffix; C does not require buying a full reel.
TI's reference design uses this family, but that alone does not qualify it.

[XGL4020-152MEC](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xgl/xgl4020/xgl4020-152/)
is an alternative: 14.3 mOhm maximum DCR at 25 C, with 3.2/5.3/7.5 A
for 10/20/30% inductance drop. It has softer saturation, not uniformly
better inductance retention. Compare actual loss at 2.1..2.7 MHz and hot
inductance at the intended current. L3 is now placed as this prototype
candidate, with procurement HOLD and footprint deferred. It is not released
for production or electrically qualified.

Live distributor pages supersede cached search stock on 2026-10-05:
[LCSC C7417180](https://www.lcsc.com/product-detail/C7417180.html) showed
2,284 XGL4020-152MEC pieces, MOQ1/multiple1, USD5.9908/1 and 5.3022/10.
These are unreserved stock and price snapshots. The live Mouser XFL page
showed zero stock and a 40-week lead time; LCSC XFL C3033018 was out of stock.
The older DigiKey XGL listing said no longer available at DigiKey.
Manufacturer direct purchase availability was ambiguous. This expensive
quantity-one fallback still needs lifecycle and lower-cost supply review,
along with hot inductance, peak/fault current, loss and loop qualification.

The TI 4.15 A maximum current-limit figure applies to average positive input
current at VIN=5 V, VOUT=6.5 V and Tj=0..125 C. It is neither a peak-current
limit nor a general guaranteed load rating at the intended bus voltage.
The coil has only about 62 mA provisional demand; the rest of the auxiliary
load must be established before selecting the converter's operating ceiling.

For provisional VIN=3.2..4.5 V, VOUT=5 V and Lmin=1.2 uH, ideal boost ripple
is VIN*(1-VIN/VOUT)/(Lmin*fmin), giving 0.457143 A peak-to-peak at 3.2 V
and fmin=2.1 MHz. Peak current must include half of that ripple above the
average current. This approximation excludes mode transitions, startup,
inductance droop and faults; it cannot qualify protection or saturation.

TI section 6, section 8.4.5 and the electrical accuracy table consistently
define PS/SYNC low as forced PWM and high as PWM/PFM. Several application
curve captions reverse those labels. Follow the explicit pin/mode definitions;
do not infer low-load mode or efficiency from the conflicting captions.

Saved library checks confirm fifteen unique exact package pins and intended
electrical types, uniform 150 mil legs, grid endpoints, hidden metadata at
origin and blank footprint. The single-unit native SVG was visually reviewed.
The library asset is now instantiated as U36. C132 uses TDK
C1608X7R1H104K080AA, 100 nF +/-10%, 50 V X7R, -55..125 C, Production.
It is exclusively a VAUX bypass, not an auxiliary load. TI specifies 100 nF;
VAUX absolute maximum is 7 V. Effective capacitance and placement remain
subject to qualification. The inherited exact-part sourcing fields were
retained and its role-specific selection basis was updated natively.

Checkpoint verification: relay022 exported netlist confirms L3 pin 1 to
U36 pin 11 and L3 pin 2 to U36 pin 9, with no accidental ground connection
at either wire crossing. All prior component net memberships are unchanged
from relay021. VAUX remains separate from ground. BOM fidelity passes for
316 included references, 19 columns and four native exclusions. The full
fifteen-page PDF was reviewed; pages 1..14 render identically to the previous
commit, and page 15 shows the inductor and mode wiring. ERC still reports
106 errors and 15 warnings; unfinished VIN, EN and PG integration remains
visible. No ERC policy was changed. Clock arithmetic passes. Forced PWM
low-load battery efficiency remains to be evaluated.

## Output bank sizing screen (2026-10-05)

The starting output bank is four Samsung CL32B226MOJNNNE capacitors,
22 uF each, 16 V, X7R, +/-20%, 1210. C133-C136 are now placed and wired
in parallel between U36 VOUT/FB and ground. Procurement remains HOLD and
footprints remain deferred pending electrical and package qualification.
Samsung's live manufacturer page reports Mass Production and supplies
typical curves only. The observed bias curve retains approximately 73%
at 5.25 V; this visual estimate is not a guaranteed minimum.

For a provisional screen, allocate 60% retention for DC bias, 80% for
initial tolerance, 85% for temperature, and 90% for aging:
four * 22 * 0.60 * 0.80 * 0.85 * 0.90 = 32.3136 uF effective.
This exceeds the 27 uF fixed-output criterion by 5.3136 uF (19.68%).
Three such capacitors give only 24.2352 uF and fail this screen.
The 10% aging allocation is a design assumption, not a manufacturer
guarantee. Combined temperature/bias behavior and low AC measurement
amplitude can invalidate independently multiplied allowances. Obtain
manufacturer bounds or validate effective capacitance in the assembled
application before release. Also qualify loop response, ripple current,
startup/inrush and load-step recovery; this arithmetic does not prove them.

[Live Mouser USA offer](https://www.mouser.com/en/ProductDetail/Samsung-Electro-Mechanics/CL32B226MOJNNNE?qs=X6jEic%2FHinAKqc7HNTy2sg%3D%3D)
showed 1,363 available, MOQ1/multiple1, maximum order 610, cut tape
USD0.92/1 and 0.557/10. Factory lead time was 52 weeks, with possible
12% US tariff stated separately. Stock is unreserved and taxes/shipping
are excluded. Reel quantity 1000 is not purchase MOQ. Evaluate a second
source before production; stock today does not resolve longevity risk.

Native checkpoint relay024 confirms all four pin-1 terminals join U36
VOUT 7/8 and FB 5; all four pin-2 terminals join ground. Excluding this
bank, every earlier component pin partition is unchanged from relay023.
The C126-C129 quiet-rail drawing was reorganized into two compact banks
with grounds below the components; its net partitions and polarized
capacitor orientations are unchanged. BOM fidelity passes for 320 included
references, 19 columns and four native exclusions. All fifteen PDF pages
were reviewed; pages 1-14 render identically to the preceding checkpoint.
ERC remains 106 errors and 15 warnings; no findings were suppressed.
Clock arithmetic passes. The converter input and enable remain open.

## Input bulk checkpoint (2026-10-05)

C137/C138 are now native parallel 22 uF CL32B226MOJNNNE input bulk
capacitors. Both pin-1 terminals join U36 VIN 12/13 and both pin-2
terminals join ground. The same provisional allowances used above give
16.1568 uF combined; this is a sizing screen, not a guaranteed minimum.
Local high-frequency bypass selection, source impedance, input dips,
ripple/startup and combined bias/temperature/aging qualification remain
open. The bank remains HOLD with footprints deferred. U36 is not yet
connected to the system supply; EN and PG integration remain open.

relay025 netlist comparison proves every earlier component pin partition
unchanged. Native BOM export fidelity passes for 322 included references,
19 columns and four native exclusions. The updated 15-page PDF has been
rendered and page 15 visually inspected; pages 1-14 are pixel-identical
to relay024. ERC remains 106 errors and 15 warnings with no suppression
changes. Clock arithmetic passes. This checkpoint does not qualify the
converter or establish continuous output capability.

## Enable and power-good interface design bounds (2026-10-05)

TI SLVSC58B sections 7.5 and 8.4.2/8.4.3 were rechecked before control
integration. EN must be terminated: rising threshold 0.77..0.83 V,
falling threshold 0.67..0.73 V. Design the disabled level below 0.67 V
and enabled level above 0.83 V under all sequencing and leakage cases.
Use a local 10 kohm pull-down as the starting candidate, rather than
letting an unpowered controller leave EN floating. A direct logic drive
does not require the VIN-series resistor described by TI; a supply-fed
EN connection requires 1 kohm..1 Mohm series resistance. Do not tie EN
to the auxiliary output, or treat the pull-down as brownout protection.

For RC0603FR-0710KL (1%, +/-100 ppm/C), a conservative multiplicative
100 C excursion from 25 C gives 9801..10201 ohms. With 10201 ohms,
aggregate positive leakage must be below 65.68 uA to stay below 0.67 V.
This is a ceiling without added noise margin, not an approved leakage
budget. At a bounded 3.6 V control high and 9801 ohms the resistor draws
0.36731 mA and dissipates 1.32231 mW. Controller output voltage,
reset behavior, leakage, unpowered-pin tolerance and source sequencing
remain to be checked before connecting a specific RA8P1 signal. The TI
0.2 uA input-current entry must not be assumed to bound every external
leakage or transient. The local EN pull-down is implemented by the following checkpoint; the controller connection remains open.

PG is open drain, with 0.4 V maximum low specified at 1 mA. A 10 kohm
pull-up to the receiver's bounded 3.3 V domain is a starting choice;
at 3.6 V and 9801 ohms the sink current is below 0.368 mA. Receiver
VIL/VIH, leakage, bus capacitance, rise time and power-off behavior must
be verified. Do not pull PG to 5 V for a non-5-V-tolerant RA8P1 input.
The PG circuit is operational only with EN active and VIN above UVLO;
loss of VIN must not be interpreted as a guaranteed valid PG indication.

For fixed 5 V output in forced PWM (+/-1% static accuracy), the falling
PG threshold spans approximately 4.455..4.77225 V and the rising threshold
4.67775..4.97425 V from the stated percentage extremes. These static
bounds exclude transient delay and ripple. PG alone cannot certify that
the sensitive analog supply is safe or that headphones may connect.
Independent rail/DC monitoring, fault latching and relay release remain
required. TPS630701 has no output discharge: disabling EN does not prove
its output is discharged. External backfeed and stored energy need an
explicit shutdown/discharge design.

[YAGEO exact-part specification](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL)
confirms 10 kohm, 1%, +/-100 ppm/C, 0.1 W at 70 C, -55..155 C.
The direct Mouser page fetch timed out in this check; the earlier indexed
quantity-one offer is not refreshed live stock. Do not mark sourcing
approved from this failed fetch. No schematic, BOM or PDF change is
claimed by this interface study.


## Native enable pull-down checkpoint (2026-10-05)

R117, YAGEO RC0603FR-0710KL, is now placed in native KiCad as a 10 kohm
pull-down from U36 EN pin 14 to GND. Its manufacturer rationale and
procurement caveats replace the inherited OPA1622 enable metadata.
The controller signal remains unconnected pending reset, leakage and
power-off qualification. This does not implement the complete enable
sequence, discharge, brownout or headphone protection circuit.

The relay026 netlist confirms R117 pin 1 connects only to U36 EN14 and
pin 2 connects to GND; every pre-existing pin partition is unchanged.
Native BOM fidelity passes with 323 included references, 19 columns and
four exclusions. Clock arithmetic passes. The 15-page PDF is refreshed;
pages 1-14 remain pixel-identical to relay025 and page 15 is visually
reviewed. ERC has 119 outstanding violations, with no suppression added.
The clean, separate positive/negative bypass groups retain the earlier
C126-C129 layout correction and capacitor polarity.


## Native high-frequency bypass checkpoint (2026-10-05)

C139 and C140, TDK C1608X7R1H104K080AA (100 nF, 50 V, X7R),
are now added in native KiCad across U36 VIN12/13-to-GND and
VOUT7/8-to-GND respectively. TI SLVSC58B section 9.2.2.3 recommends
small ceramic capacitors close to both supply pin groups alongside
bulk capacitance. The 100 nF value is an engineering candidate, not
an exact value mandated by TI. These do not replace C137/C138 input
bulk or C133-C136 output bulk. Physical pin proximity, short returns,
effective capacitance, ESL, impedance/resonance and footprint remain
unqualified. The earlier quantity-one sourcing snapshot is retained
with its date and is not represented as refreshed live inventory.

The relay027 netlist verifies both connections and all pre-existing
pin partitions are unchanged relative to relay026. Native BOM fidelity
passes with 325 included references, 19 columns and four exclusions;
clock arithmetic passes. ERC still reports 119 outstanding violations.
No new suppression is added. The 15-page review PDF is refreshed;
pages 1-14 are pixel-identical to relay026, and page 15 is visually
reviewed. The positive/negative amplifier bypass groups retain their
clean layout and C129 positive terminal remains connected to GND.

[TI TPS63070/TPS630701 datasheet](https://www.ti.com/lit/ds/symlink/tps63070.pdf)

## Native relay supply connection checkpoint (2026-10-05)

The local AUDIO_AUX_5V labels now join U36 VOUT7/8 and FB5,
C133-C136/C140 positive terminals, and U35 IN1/EN3 with C130 pin 1.
This implements the auxiliary-output-to-relay-regulator connection only.
U36 input source and controller enable/status connections remain open;
independent relay fault gating and headphone protection remain unfinished.
No claim of a working or qualified power subsystem is made.

TPS7A20 recommended IN/EN range is 0-6 V (6.5 V absolute maximum),
so the intended regulated 5 V bus is suitable in steady state. Startup,
overshoot and failure behavior must also remain within the recommended
range. The existing conservative 5.25 V / 62 mA relay input allocation
is 325.5 mW; with a 3 V / 60 mA coil, the allocated regulator loss is
145.5 mW including the 2 mA overhead allowance. Sealed-enclosure thermal
performance still requires physical validation.

Netlist relay028 confirms exactly the intended two-net merge and no
other pin-partition changes relative to relay027. Native BOM fidelity
passes: 325 included references, 19 columns, four exclusions. Clock
arithmetic passes. ERC reports 118 outstanding findings (103 errors,
15 warnings); no suppression was added. The refreshed 15-page PDF has
pixel-identical pages 1-14, and page 15 was visually reviewed, including
the clean separate C126-C129 supply banks and negative-rail polarity.

[TI TPS7A20 datasheet](https://www.ti.com/lit/gpn/TPS7A20)

## Native power-good pull-up checkpoint (2026-10-05)

R118 (YAGEO RC0603FR-0710KL, 10 kOhm) connects U36 PG2 to
receiver-referenced +3V3_MCU through the local AUDIO_AUX_PG net.
The pull-up supply is implemented; the reserved receiver and hardware enable
gate remain unwired. At 3.63 V and 9801 ohm worst-case resistance,
sink current is below 0.371 mA,
below TI's 1 mA PG sink specification point. Receiver thresholds, leakage,
rise time and power-off behavior remain unqualified. PG does not replace
independent headphone DC/rail-fault protection.

The earlier relay029 netlist confirmed U36.2/R118.2 and an R118.1 logic-supply
singleton. The relay030 native checkpoint resolves that singleton to
+3V3_MCU, the same supply as the reserved MCU receiver. Removing R118
from the comparison leaves all previous pin
partitions unchanged. Exact-part sourcing fields retain their explicitly
indexed, unreserved snapshot; availability was not refreshed live.
Native BOM fidelity passes with 326 references, 19 columns and four
exclusions; clock arithmetic and MCU map comparison pass. ERC now has
117 outstanding findings: the isolated supply-label finding is removed,
with no added finding or suppression. The native 15-page PDF
was refreshed: pages 1-14 are pixel-identical, and the power-good region and
separate C126-C129 bypass banks were visually reviewed.

## Auxiliary controller ownership and sequencing decision (2026-10-05)

Reserve P107/N5 for AUDIO_AUX_REQ (GPIO output) and P904/A16 for
AUDIO_AUX_PG (GPIO input, polled). Both are open single-node nets in the
saved relay029 export; neither has a conflicting recorded owner in the
current design documents. These are implementation reservations, not
new native wires. P106/N6 is already SD_PWR_REQ and must not be reused.
P108-P110 retain unresolved historical MMC expansion reservations.
P200/C5 is input-only/NMI and must not be selected as an enable output.
P000/P001 are not assigned to audio here; their possible analog sensing
roles remain unresolved. This does not release any other pin.

Renesas R01DS0439EJ0130 Tables 1.17 and 2.6, pp26/31/51/52/54,
confirm A16=P904 (VCC domain), N5=P107 (VCC2 domain), and P200 input-only.
Use GPIO with peripheral selection disabled; no IRQ channel is claimed.
Both selected domains presently use the native +3V3_MCU source. R118's
receiver-referenced supply now joins that source in relay030. Receiver
wiring remains pending. Do not use the analog 5 V bus or AON_HOLD.

Conditional static status screen, using the main regulator's previously
calculated 3.151819680 V minimum (not a measured rail guarantee), ordinary
GPIO VIH=0.8*VCC and VIL=0.2*VCC, RA leakage allocation 1 uA and TI PG
high-impedance leakage 0.2 uA: Rmax=10201 ohm gives 12.2412 mV adverse
high-state drop. High margin is 0.618123 V; low margin versus PG VOL=0.4 V
is 0.230364 V. At 3.63 V and Rmin=9801 ohm, sink current is 0.370371 mA.
This is under TI's 1 mA test point. Renesas Tables 2.5/2.7 pp48/49/57
and TI SLVSC58B Table 7.5 are the authorities. Disable internal pulls.
The leakage screen is for specified powered conditions, not VCC=0.

R117 with 1.2 uA adverse leakage has only 12.2412 mV in the same resistor
corner, but this alone does not prove reset/off-state safety. Do not wire
AUDIO_AUX_REQ directly to EN as the sole shutdown mechanism. The next
native control stage must combine the request with hardware main-power
permission, default low without control supply, and preserve SYS-007's
existing held-domain current budget. Any new MAIN_PWR_EN load requires
rebudgeting; use its existing buffered path or a qualified separate buffer.

Sequencing contract for the next native implementation:

| Condition | Auxiliary converter | Headphone relay |
| --- | --- | --- |
| No main power permission, reset or missing control supply | Hardware EN low regardless of GPIO | Hardware drive low; contacts open |
| Valid source and request, rails starting | EN may assert | Remain open until independent DC/rail checks and delay pass |
| PG valid and all independent safety checks pass | Enabled | MCU request may permit connection; PG alone is insufficient |
| Converter VIN missing while MCU rail remains | EN cannot establish valid power | Open by independent rail/source monitor; never rely on PG alone |
| DC/rail/thermal fault or wet-port shutdown affecting source | Remove affected enables | Latched hardware disconnect overrides stuck MCU request |
| Normal shutdown | Disconnect first, then remove rails | Verify contact opening before unsafe rail collapse |

TI section 8.4.3 qualifies PG operation by EN and VIN above UVLO. Missing
VIN may leave a misleading pulled-up indication; even its EN-low table
entry does not establish absent-VIN operation. Stored output energy and
shutdown/backfeed remain separate checks. No native protection stage or
controller connection is claimed by this reservation and static screen.

[Renesas RA8P1 datasheet](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet)
[TI TPS63070/701 datasheet](https://www.ti.com/lit/ds/symlink/tps63070.pdf)

## Native MCU status connection checkpoint (2026-10-05)

AUDIO_AUX_PG now runs through matching Output/Input hierarchical labels,
imported root sheet pins and root-local status labels to U1 P904/A16.
The saved relay031 netlist contains exactly U36.2, R118.2 and U1.A16
on this status net. R118.1 remains on +3V3_MCU. Comparison against
relay030 shows only the intended receiver-net merge; all other component
pin partitions are unchanged. Earlier statements that the receiver is
unwired are historical and superseded by this checkpoint. R118's native
Selection_Basis still describes the earlier reservation and needs updating
in the next component metadata pass; the CSV faithfully retains that field.

MCU map comparison passes with 110 connected ports, 78 open ports and
11 named singletons. Native BOM fidelity passes for 326 references,
19 columns and four exclusions; clock arithmetic passes. ERC is 116
outstanding findings, one unconnected-pin finding removed with no added
finding or suppression. The full 15-page PDF was refreshed; only pages
1, 2 and 15 changed, and all three were rendered and inspected. The
separate C126-C129 bypass banks retain grounds below the components and
correct negative-rail polarity.

This status connection implements monitoring only. The hardware enable
gate, bounded source, independent fault disconnect and sequencing remain
open. Powered static margins do not qualify missing-VIN or unpowered
GPIO behavior. Full electrical implementation remains in progress.

## Auxiliary enable gate investigation (2026-10-05)

The relay031 saved netlist identifies the hardware permission candidate as
`/Main 3V3 digital supply/RUN_U13`: Q3.3, R68.2, R69.2 and U13.A1.
It is downstream of R68 and is directly clamped by held shutdown Q3.
U16.4/R68.1 is upstream of that clamp and MUST NOT be used as an
equivalent shutdown permission. MAIN_PWR_EN is the held control input;
adding another gate directly there also requires a new held-budget review.

No new gate is selected or placed by this investigation. A receiving gate
can disturb the existing main converter even when its own supply is absent.
In particular, do not copy a logic input's powered leakage into its Ioff
allocation or assume that an input on a separate rail is always a sink.

For a hypothetical 5 uA additional adverse input leakage, retaining the
PWR-004 resistor endpoints (.9801 and 1.0201), raw maximum 4.6 V and
allocated Q3 leakage 1 uA, the powered screens become:

| Screen | Conditional result |
| --- | ---: |
| U16 static source load, 4.6/(68k*.9801) + 6.2 uA | 75.220568 uA, below its 100 uA output test |
| RUN_U13 high at raw 3.2 V, (3.1 - 6.2uA*1k*1.0201)/(1 + 1k*1.0201/(68k*.9801)) | 3.047037 V |
| Zero raw, previous 2 uA U16 Ioff + 1 uA EN allocation + 5 uA new source, through 68k*1.0201 | 0.554934 V |
| Same zero-raw screen with a 10 uA new source allocation | 0.901768 V |

The latter two exceed U13's 0.4 V guaranteed low-input limit. They do not
prove a real device sources this current; they show that the existing
zero-raw proof cannot simply survive a new worst-case leakage allocation.
Q3's conditional shutdown clamp remains a separate mechanism, and its
timing must be evaluated through every independently powered rail state.

Primary-datasheet candidate review:

- [Nexperia 74LVC1G08 Rev 16.1](https://assets.nexperia.com/documents/data-sheet/74LVC1G08.pdf),
  Tables 6-7: 5.5 V tolerant inputs, 1 uA input leakage and 2 uA Ioff,
  but explicit input-transition limits remain. The 2.0 V VIH range stops
  at 3.6 V; the current control-rail screening maximum is 3.63 V. Do not
  silently extend that threshold range or certify slow shutdown edges.
- [TI SN74LV1T08 Rev F](https://www.ti.com/lit/ds/symlink/sn74lv1t08.pdf),
  sections 6.3/6.5: reduced thresholds are useful, but 20 ns/V input
  transition limits and the lack of a separately specified Ioff limit in
  the electrical table prevent an immediate default-off qualification.
- [TI SN74LVC1G97 Rev N](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf),
  sections 6.3/6.5: Schmitt thresholds and no listed input-transition
  constraint suit slow control edges; input leakage is 5 uA and Ioff
  10 uA. Threshold values are given at discrete supplies. Continuous-rail
  bounds and additional leakage must be resolved before selecting it.

Next design work: qualify a receiving/isolating control stage that preserves
U13's low-state proof, verify slow edges and continuous supply thresholds,
add a local request pulldown and bypass, then implement the hierarchy from
P107/N5. If the control supply is separate, verify every combination of
raw, held, main and auxiliary supply presence. Source validity and the
independent headphone disconnect are still separate requirements. Exact
order-code lifecycle, quantity-one stock and price checks follow only for
electrically viable candidates. This checkpoint changes documentation only;
the existing CAD, BOM and PDF remain at the verified relay031 checkpoint.

## Native permission isolation placement (2026-10-05)

Placed Q5 (DMN2056U-7) on the audio sheet with source pin 2 grounded.
Gate pin 1 and drain pin 3 remain open pending the complete gate network,
main-rail pull-up and request logic. This is a staged placement, not a
functional permission circuit. It does not enable U36 or the headphones.
The intended gate source is the post-Q3 RUN_U13 node identified above.
No added load has yet been connected to the main shutdown network.

The main regulator's conditional normal rail range is 3.151819680019 to
3.393012496197 V (static tolerance plus the existing 75 mV allocation in
main_regulator_tps63806.md). This supersedes the preceding use of 3.63 V
as a normal logic supply maximum. 3.63 V remains a separate screening
value; normal rail bounds do not cover arbitrary startup or fault states.
Continuous supply thresholds and slow-edge behavior still need resolution.

The Diodes DMN2056U datasheet DS38480 Rev 2-2 specifies G1/S2/D3,
20 V VDS and +/-8 V VGS. Its 45 milliohm limit at VGS=2.5 V, 1 uA
IDSS and +/-100 nA IGSS tests are at 25 C unless otherwise specified.
Do not treat those as hot leakage or shutdown qualification. Q5 reuses
an existing order code; its native sourcing fields retain the historical
2026-09-07 snapshot. A 2026-10-05 DigiKey review showed Active status,
46,058 stock and quantity-one cut tape at USD 0.39; this is a distributor
snapshot, not reserved stock or a future lifecycle guarantee.
Sources: https://www.diodes.com/datasheet/download/DMN2056U.pdf and
https://www.digikey.com/en/products/detail/diodes-incorporated/DMN2056U-7/7352909.

R118 native selection metadata now records the implemented P904/A16 PG
receiver. The saved relay032 netlist preserves every existing pin partition
and adds only Q5.2 to GND plus open Q5.1/Q5.3 nets. Native BOM fidelity
passes with 327 references, 19 columns and four exclusions; clock arithmetic
passes. ERC has 119 outstanding findings (previously 116): Q5 adds gate
unconnected/undriven and drain unconnected errors, with no suppression.
The refreshed 15-page PDF changes page 15 only; its layout and the separate
C126-C129 banks were visually inspected. Source, request/permission wiring,
logic thresholds, independent fault disconnect and sequencing remain open.

## Local isolation gate pulldown (2026-10-05)

Implemented R119, 1 MOhm YAGEO RC0603FR-071ML, between Q5 gate
pin 1 and GND. Q5 source pin 2 is grounded. The future series gate feed
and drain/request logic remain open; RUN_U13 has no added native load yet.
Historical sourcing fields remain explicitly subject to recheck.

For the planned 1 kOhm series feed, using resistor endpoint multipliers
0.9801 and 1.0201 and a project hot gate/board leakage allocation of 1 uA:

- Additional branch current <=4.6/(1M*0.9801)+1uA = 5.693399 uA.
- U16 source load <=4.6/(68k*0.9801)+1.2uA+5.693399uA = 75.913967 uA.
- RUN high >=(3.1-(1.2uA+5.693399uA)*1k*1.0201)
  /(1+1k*1.0201/(68k*0.9801)) = 3.046341 V.
- Q5 gate >=(3.046341-1uA*1k*1.0201)
  /(1+1k*1.0201/(1M*0.9801)) = 3.042154 V.
- Conservative zero-raw EN screen: 4uA*68k*1.0201 = 0.277467 V.
- Pulldown dissipation <=4.6^2/(1M*0.9801) = 21.589634 uW.

These are conditional screens for a planned complete branch, not a
qualification of the current incomplete circuit. The 1 uA hot allocation
requires validation; it is not a manufacturer hot leakage guarantee.
Startup, Miller coupling, edge timing and shutdown remain open.

Saved relay033 netlist: Q5.1/R119.2 share the gate net; Q5.2/R119.1
are grounded; Q5.3 remains open. All prior pin partitions are preserved.
Native BOM fidelity passes with 328 references, 19 columns and four
exclusions; clock arithmetic passes. ERC is 117 outstanding findings,
down from 119 because the gate pulldown resolves two gate findings, with
no suppression. PDF pages 1-14 are pixel-identical; page 15 and the
separate bypass banks were visually inspected. Implementation continues.

## Native permission series network (2026-10-05)

Implemented R120, 1 kOhm YAGEO RC0603FR-071KL, from the audio-sheet
MAIN_RUN_PERMIT hierarchical input to Q5 gate/R119. R120.1 is the
permission input; R120.2 shares Q5.1/R119.2. The parent-sheet pin,
post-Q3 RUN_U13 export and root connection are not yet implemented.
This network therefore still adds no load to the native main shutdown net.
Q5 drain and request logic remain open. R120's copied metadata was
corrected to its actual audio role; historical sourcing needs recheck.
The conditional complete-branch calculations above remain applicable only
once the source hierarchy is implemented and leakage/timing are qualified.

Saved relay034 netlist preserves all prior pin partitions after excluding
new R120. Native BOM fidelity passes with 329 references, 19 columns and
four exclusions; clock arithmetic passes. ERC is 119 outstanding findings:
the unfinished parent hierarchy and isolated permission feed remain visible,
without new suppression. PDF pages 1-14 are pixel-identical, and page 15
plus the gate detail were visually inspected. Next: implement the matching
parent pin and post-Q3 source hierarchy, then drain/request logic and the
independent protection circuit. Full electrical implementation is ongoing.

### Native main permission export checkpoint (2026-10-05)

Added an output hierarchical label `MAIN_RUN_PERMIT` on the existing clamped
`RUN_U13` net at U13 EN, and imported its output pin into the parent main-supply
sheet. Fresh `relay035.xml` confirms the source remains Q3.3, R68.2, R69.2,
and U13.A1. All component-pin partitions match relay034 exactly: this step
exports the source but does not yet connect it to audio R120.

The audio parent input pin and root connection remain next work. The root audio
block still needs enlargement before adding these ports. Q5 drain, request
logic, hot leakage and shutdown timing remain unfinished. ERC reports 121
messages (104 errors, 17 warnings), including the expected unconnected source
sheet pin and RUN_U13/MAIN_RUN_PERMIT naming warning; no new suppression was
introduced. KiCad regenerated the audio sheet file UUID on save, with no
component connectivity changes. The complete 15-page review PDF was refreshed
and pages 1 and 9 rendered and inspected. The previously cleaned C126-C129
bypass banks retain ground symbols below each bank.

## Connected permission and request-gate screen (2026-10-05)

Commit 6657af4 connected R120.1 to the post-Q3 permission through the root
hierarchy. The complete native source partition is Q3.3/R68.2/R69.2/
U13.A1/R120.1; U16.4 remains upstream of the clamp. Commit 970d7e9
preserved the enlarged root audio box, now 53.34 by 26.67 mm. Export
relay039 has exactly the same component-pin net partitions as relay038.
Earlier statements above that the root permission is open are historical.
Q5 drain and the request/enable stage remain open.

TI's April 2026 [SBAA808 interpolation brief](https://www.ti.com/document-viewer/lit/html/SBAA808/GUID-F7CBECE2-5469-41E4-AC23-D67A055422CD)
supports interpolating minimum/maximum table limits between supply points.
Its examples and linked devices are HC/HCS; applying its general guidance
to LVC Schmitt thresholds is an engineering interpretation, not an explicit
SN74LVC1G97-specific manufacturer confirmation. Do not apply this brief to
Nexperia parts. No extrapolation outside tabulated supplies is proposed.

The [SN74LVC1G97 Rev N](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf)
Table 1 gives Y=In1 when In2 is low, and Y=In0 when In2 is high.
Proposed DBV connections: In0 pin 3=GND; In1 pin 1=AUDIO_AUX_REQ;
In2 pin 6=Q5 drain with a local 10k pull-up; Y pin 4=U36 EN;
VCC pin 5=+3V3_MCU; GND pin 2=GND. Thus permission absent forces low,
and permission present allows the request. This is not yet native wiring.

At the conditional normal main rail 3.151819680019..3.393012496197 V,
linear interpolation of Table 6.5's 3 V and 4.5 V endpoints gives
VT+ maximum 2.097947248 V and VT- minimum 0.897691478 V, using
the opposite rail endpoints to conservatively compare independent bounds.
[RA8P1 Rev 1.30 Table 2.7](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet),
printed page 56, other-output row applies to GPIO P107/N5:
VOH >= VCC2-0.5 V and VOL <=0.5 V at 1 mA magnitude. Do not use the
SD-specific output row for this GPIO. Proposed 10k request pulldown plus
5 uA gate input allocation loads it by at most 0.351191 mA. Request
high >=2.651819680 V therefore has 0.553872432 V margin; low has
0.397691478 V margin. Reset requires internal pull-up disabled.

For the proposed Q5-drain 10k pull-up, resistor endpoints remain
0.9801..1.0201. Allocate 10 uA hot Q5/board off leakage plus 5 uA
logic input leakage: drain high >=3.151819680019-15u*10201=
2.998804680 V, 0.900857432 V above interpolated VT+ maximum.
The 10 uA allocation is a qualification requirement, not a Diodes hot
guarantee. On current <=3.393012496197/9801+5u=0.351191 mA;
using Q5's 25 C 45 milliohm test limit yields 15.804 uV drain low.
Do not use that resistance as a guaranteed hot value. For a defensible
hot low-state screen, effective Q5 on resistance must remain below
0.897691478/0.000351191=2556 ohms, including layout effects.

This advances the powered DC candidate screen only. Logic below 1.65 V
is not specified to hold a valid output. Ioff at zero VCC is not a guarantee
through brownout. Q5 gate near zero does not prove hot drain isolation from
its threshold-voltage test. Require startup/falling-rail hardware inhibition,
Q5 leakage/timing review and U36 EN loading/output limits before native
enable wiring. Independent headphone DC/rail/thermal disconnect remains
mandatory. The next step is to qualify that supply-valid clamp and then
place the gate, request pulldown, drain pull-up and local bypass in KiCad.

### 2026-10-05 native permission drain pull-up

R121 is now implemented in KiCad: 10k YAGEO RC0603FR-0710KL from
+3V3_MCU to Q5 drain pin 3. A straight vertical connection leaves space
for the request gate; its copied selection field was corrected to the
actual drain-pull-up role. The conditional loading and leakage bounds
above remain applicable, including the unresolved hot-leakage allocation.
The request gate, startup/brownout clamp and U36 enable connection remain
unfinished; this pull-up does not make the converter operational.

Saved relay041 netlist verifies the two R121 endpoints and preserves all
previous component-pin partitions when R121 is excluded. Native BOM
export fidelity passes: 330 included references, 19 columns, four native
exclusions. Clock arithmetic checks pass. ERC has 117 outstanding findings
(previously 118), without suppressing unfinished circuitry. The full
15-page PDF was refreshed and its root and audio pages visually inspected.

### 2026-10-05 native request-gate checkpoint

U37 SN74LVC1G97DBVR is now placed in the native audio sheet. Saved
relay042 verifies VCC pin 5 on +3V3_MCU, GND pin 2 and IN0 pin 3 on
GND, and IN2 pin 6 on the Q5.3/R121.2 drain partition. All earlier
component-pin partitions are preserved when the new U37 nodes are excluded.
IN1 pin 1 and Y pin 4 remain open. Local bypass, request pulldown and
hierarchy routing, output loading and startup/brownout inhibition remain
unfinished. U37 placement does not qualify or enable U36.

Native sourcing fields record the previously checked 2026-10-05 TI Active
and DigiKey cut-tape MOQ1 snapshot; inventory is unreserved. Footprints
remain deferred. Native BOM fidelity passes with 331 included references,
19 columns and four native exclusions; clock arithmetic passes. ERC has
120 outstanding findings: the previous 117 plus U37 IN1 unconnected,
IN1 not driven, and Y unconnected. These are retained, not suppressed.

Commit 437ab4f enlarged the root audio sheet box from 53.34 x 26.67 mm
to 53.34 x 68.58 mm while preserving its connections. Further corner
and edge drags did not register a width change; width remains 53.34 mm.
The complete 15-page review PDF was refreshed and its root and audio
pages rendered and inspected for this checkpoint. The C126-C129 bypass
banks still use separate ground symbols below each bank.

### 2026-10-05 native request pulldown and bypass checkpoint

C141 (TDK C1608X7R1H104K080AA, 100n) now bypasses U37 VCC5 to GND.
R122 (YAGEO RC0603FR-0710KL, 10k) now connects U37 IN1 pin 1 to GND.
Saved relay043 verifies both connections and preserves every existing
component-pin partition after excluding the two new components. R122's
native selection field records the conditional request loading calculation
above and the requirement to disable the MCU internal pull-up at reset.
The request hierarchy, output loading network, supply-valid hardware clamp
and U36 enable connection remain open. Neither addition proves startup or
brownout safety, or makes the converter operational.

Native BOM fidelity passes with 333 included references, 19 columns and
four native exclusions. Clock arithmetic passes. Unsuppressed ERC reports
118 findings (102 errors, 16 warnings), down from 120 because IN1 now has
the pulldown connection. The complete 15-page PDF was regenerated and the
changed audio page rendered and visually reviewed. Repeated root corner
drags did not register a further resize; root geometry remains unchanged.

### Enable-interface threshold correction and next circuit decision

Re-read [TPS63070 Rev B, section 7.5](https://www.ti.com/lit/ds/symlink/tps63070.pdf):
EN rising is 0.77..0.83 V and falling 0.67..0.73 V; input current maximum
is 0.2 uA. Do not transfer TPS63806's 1.2/0.4 V EN levels to U36.
The VSEL/synchronization rows are also different from EN. This removes
the mistaken concern that a 0.45 V logic low inherently fails U36 EN.

Using [SN74LVC1G97 Rev N, table 6.5](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf)
3 V output test limits (2.4 V high at -16 mA, 0.45 V low at 16 mA,
-40..125 C), a proposed 10k series resistor and existing R117 10k
pulldown screen as EN >=1.175002700 V high and <=0.230499250 V low.
Enumeration uses both resistor endpoints 0.9801/1.0201 and both signs
of 0.2 uA EN leakage. Threshold margins are 0.345002700/0.439500750 V.
Maximum hard-clamp source current is 3.393012496197/9801 =0.346190439 mA.
These are DC screens, not a validated clamp or an output guarantee below
the gate's specified supply range.

The diode-to-MCU_RESET_N proposal is superseded by a dedicated supervisor.
The existing U2 low-voltage reset-net sink allocation is approximately
0.3762 mA against the 0.4 mA test condition, so adding the proposed
0.3462 mA clamp load is not justified. BAT54 forward-voltage maxima at
25 C also do not establish a complete-temperature clamp guarantee.
No diode has been placed; do not add this load to MCU_RESET_N.

### Dedicated audio supply-valid supervisor: native WIP checkpoint

U38 TPS389001DSET is now placed using the existing editable library symbol.
[TI Rev A sections 6-7](https://www.ti.com/lit/ds/symlink/tps3890.pdf)
confirm DSE pins: SENSE1, GND2, MR3, VDD4, CT5, RESET6. Native wiring
connects GND2 to a separate ground symbol below the IC and ties MR3 to
its own VDD4 using a loop outside the symbol body. Two unintended interior
wire stubs were removed before export. Supply source, SENSE divider, local
100n bypass, CT capacitor and RESET-to-EN clamp remain unfinished.

The proposed supply is the same regulated 3.2..4.5 V system source as
U36 VIN, so U38 can monitor +3V3_MCU while powered independently of that
rail. U38's recommended VDD range is 1.5..5.5 V; do not connect it to raw
USB-PD VBUS. The 10k series resistor from U37 Y to U36 EN is still proposed.
U38 RESET6 would clamp EN directly, without a diode or MCU reset-net load.
Do not pull RESET up separately to SYS, which could force EN high.

The DC sink screen is 0.346190439 mA plus 0.2 uA EN leakage, below the
0.4 mA low-supply test current. Use conservative VOL <=0.3 V rather than
extending a lower-voltage test row; margin to U36's 0.67 V minimum falling
EN threshold is 0.37 V. This is a candidate DC screen, not qualification.
Startup and simultaneous rail collapse, assertion timing, partial-power
leakage/injection and the final SYS source integration remain open. A
33k/20k precision sensing divider and approximately 1n C0G CT capacitor
are candidates only; complete threshold/leakage/tolerance and timing
budgets before selecting or placing them. Independent headphone DC,
rail and thermal disconnect remains mandatory.

[TI orderable status](https://www.ti.com/product/TPS3890/part-details/TPS389001DSET)
is Active. The 2026-10-05
[DigiKey snapshot](https://www.digikey.com/en/products/detail/texas-instruments/TPS389001DSET/6110554)
records cut-tape MOQ1, 2090 stock, USD2.22 at one unit and 26-week lead;
TI direct inventory was unavailable. Stock is unreserved and must be
rechecked before ordering. Native fields identify the part as a WIP
candidate with circuit/transient qualification and footprint deferred.

Saved relay044 netlist verifies U38 GND2 and MR3/VDD4 and preserves all
earlier component-pin partitions after excluding U38. Native BOM fidelity
passes with 334 references, 19 columns and four native exclusions. Clock
arithmetic checks pass. Unsuppressed ERC reports 124 findings (108 errors,
16 warnings), six more than relay043: U38 SENSE and CT each unconnected
and undriven, VDD undriven and RESET unconnected. These explicitly retain
the unfinished work. The root audio box width has not changed; further
layout enlargement remains open.

The refreshed 15-page review PDF was rendered and visually inspected on
2026-10-05. Audio page 15 shows U38 with the MR/VDD loop outside its
body and GND below the symbol; no interior wire stubs remain. This is
a WIP export, not a release qualification.

### U38 local bypass: native checkpoint

C142 is now a native 100nF TDK C1608X7R1H104K080AA bypass from
U38 VDD4/MR3 to GND2. Its supply loop stays outside the symbol and its
ground symbol is below the capacitor. This implements the local ceramic
bypass recommended by TI TPS3890 Rev A sections 6 and 10. The proposed
3.2..4.5V SYS source remains unconnected; SENSE, CT and RESET integration
are still open. Updated native U38 fields explicitly retain those gaps.

Saved relay045 XML confirms C142 pin1 shares U38 pins3/4 and C142 pin2
shares U38 pin2 ground. All relay044 component-pin partitions remain
unchanged after excluding C142. Native BOM fidelity passes with 335
references, 19 columns and four native exclusions; clock arithmetic
passes. Unsuppressed ERC remains 124 findings (108 errors, 16 warnings).
These checks establish export fidelity and connectivity, not completed
startup, brownout or headphone protection qualification. Root audio
sheet width remains unchanged after unsuccessful GUI corner drags.

### 2026-10-06 sensing-divider and timing checkpoint

Native R124 (33k ERA-6ARW333V) and R125 (20k RG1608N-203-W-T1)
now connect +3V3_MCU through the divider to U38 SENSE1, with R125
returning to ground. C143 (1n C1608NP01H102J080AA) connects CT5 to
ground. R123 (10k) connects U37 Y to AUDIO_AUX_EN; U38 RESET6 shares
that enable net. U38 supply remains unconnected to its proposed system
source, and the overall enable/protection circuit is not complete.

These parts were copied from existing qualified-value candidates in the
radio sheet. Their inherited role/selection metadata still references that
circuit and must be corrected in the native GUI. Existing sourcing snapshots
are historical, not a current stock verification. Threshold, timing,
startup and collapse qualification remain open; placement is not approval
for production. The earlier enable DC screen also needs to include U38
RESET leakage in addition to U36 EN leakage.

Saved relay047 netlist verifies the new divider and CT connections. All
existing component-pin partitions are unchanged relative to relay046 after
excluding the three new references. Native BOM fidelity passes: 339 included
references, 19 columns, four exclusions. Clock arithmetic checks pass.
ERC with the existing project settings reports 119 findings (102 errors,
17 warnings); no exclusions were added. Existing ignored check categories
mean this is not an all-checks-enabled ERC pass. An unconnected wire endpoint
is among the outstanding warnings and requires native inspection/correction.

The full PDF was regenerated and the changed audio page rendered and visually
reviewed. New parts and ground symbols are readable and separated. The root
sheet box enlargement remains unfinished. This is a WIP checkpoint, not a
completed audio design or release package.

### 2026-10-06 auxiliary source integration

U36 VIN12/VIN13 and C137/C138/C139 input bypass now join SYS_AON.
U38 VDD4/MR3 and C142 pin1 join the same source. Native power symbols
were placed in KiCad; no PWR_FLAG or ERC exclusion was added.
SYS_AON is the low-voltage battery/charger system bus, not raw USB-PD.
Its upstream charger/source implementation remains open. The existing
converter calculations assume 3.2..4.5V and require reconciliation with the
final source limits, overshoot and brownout waveform before qualification.
U38's 1.5..5.5V recommended VDD range is confirmed in TI TPS3890 Rev A
section 7.3 (https://www.ti.com/lit/ds/symlink/tps3890.pdf). Its local bypass
and independent supply allow monitoring +3V3_MCU without powering U38
from that monitored rail. This connection does not prove fault timing.

relay049 XML verifies exactly the union of the earlier SYS_AON, U36 VIN
and U38 VDD component-pin sets. All other pin partitions remain identical
to relay047. BOM fidelity still passes for 339 included references and four
exclusions; only power symbols were added. ERC at unchanged settings reports
117 findings: 100 errors and 17 warnings. Upstream power remains undriven.
The 15-page PDF was regenerated and its changed audio page visually reviewed.
AUDIO_AUX_REQ hierarchy/processor integration, copied role metadata,
startup/collapse qualification and independent output protection remain open.

### 2026-10-06 MCU request and power-good connections

This checkpoint finishes the RA8P1-to-converter control and status
interface only. It does not finish the auxiliary supply, the SYS_AON source,
the headphone protection or the audio subsystem. Firmware is not implemented.
Statements above that the request hierarchy, U37 output or U38 divider/CT are
open are historical and superseded here.

Native connections, verified in a fresh saved XML netlist:

| Net | Component pins |
| --- | --- |
| /AUDIO_AUX_REQ | U1.N5 (P107), U37.1 IN1, R122.1 (R122.2 = GND) |
| /AUDIO_AUX_PG | U1.A16 (P904), U36.2 PG, R118.2 (R118.1 = +3V3_MCU) |
| Net-(Q5-D) | Q5.3, R121.2, U37.6 IN2 |
| Net-(U37-Y) | U37.4 Y, R123.1 |
| AUDIO_AUX_EN | R123.2, U36.14 EN, R117.1, U38.6 RESET |
| MAIN_RUN_PERMIT source | Q3.3, R68.2, R69.2, U13.A1, R120.1 (unchanged) |

Hierarchy: P107 drives an output hierarchical label `AUDIO_AUX_REQ` on
`mcu_interfaces.kicad_sch`; the root sheet imports it as an output pin on
the IO allocation block and as an input pin on the Headphone audio block;
root local labels join them; the audio sheet uses an input hierarchical label
at the R122/IN1 wire corner. PG reuses the existing output/input pair.
U37 IN0 stays on GND, so Y = IN1 only while Q5 pulls IN2 low; with permission
absent R121 forces IN2 high and Y low regardless of the GPIO. U38 RESET still
clamps EN directly, so neither firmware nor U37 can override permission or
the supply-valid clamp. MCU_RESET_N gains no load.

Pin suitability. RA8P1 R01DS0439EJ0130 Rev 1.30 Table 1.17 lists BGA289
N5 = P107 and A16 = P904; the native symbol matches the 199-port reference.
P107's alternates (CTS4_A, OM_0_CS0, ET1_INT, GPT/AGT, ADST0) are unused:
the NOR uses OM_0_CS1 on P104, no Ethernet or SCI4 is allocated, and the
saved audit and design records hold no other owner. P106 stays SD_PWR_REQ;
P200 (input-only/NMI) is not used. Port power domains come from the RA8D2
User's Manual R01UH1065EJ0130 Table 20.2 (p839): P100-P107 are VCC2 and
P902-P915 are VCC. The RA8P1 User's Manual R01UH1064 was not available
locally, so this relies on the documented pin compatibility of the two
groups (`firmware/docs/reference/ra8p1_vs_ra8d2.md`) and needs a direct
RA8P1 manual check. Both domains, U37 VCC and R118 are on +3V3_MCU.
The same manual (section 20.1 p837, PmnPFS p844) gives all pins except P209
as inputs after reset with PCR=0 (pull-up disabled) for P107 and P904.

Conditional DC screens (`python scripts/check_audio_aux_control.py
--netlist NETLIST.xml`), using the conditional +3V3_MCU range
3.151819680..3.393012496 V and 9801..10201 ohm resistor endpoints:

| Screen | Source limits | Result |
| --- | --- | --- |
| U37 thresholds | SCES416N Table 6.5, linear between 3.0/4.5 V rows | VT+ max 2.097947 V; VT- min 0.897691 V |
| P107 output load | 3.393/9801 + 5 uA U37 II | 0.351190 mA, under the 1 mA VOH/VOL test |
| P107 high | RA8P1 Table 2.7 p56: VOH >= VCC2-0.5 V | 0.553872 V above VT+ max |
| P107 low | VOL <= 0.5 V at 1 mA | 0.397691 V below VT- min |
| P107 Hi-Z (reset) | Table 2.7 p57 ITSI 1 uA + U37 II 5 uA, R122 max | IN1 <= 61.206 mV, 0.836 V margin |
| EN high (released) | U37 VOH 2.4 V test, R117/R123, 0.45 uA EN+RESET leakage | >= 1.173753 V vs 0.83 V rising max |
| EN low (Y low) | U37 VOL 0.45 V test, same divider | <= 0.231749 V vs 0.67 V falling min |
| U38 clamp | TPS3890 SLVSD65A VOL 0.25 V at 0.4 mA | sink <= 0.346390 mA; EN <= 0.25 V |
| P904 high | Table 2.5 p49 VIH 0.8 VCC; 1 uA + 0.2 uA leakage | 0.618123 V margin |
| P904 low | TPS63070 PG VOL 0.4 V at 1 mA; VIL 0.2 VCC | 0.230364 V margin |

The interpolation of LVC Schmitt limits remains the engineering
interpretation recorded earlier; the VOH/VOL rows for U37 are high-current
test points used as conservative bounds. U38 uses the same TPS389001 and
33k/20k network as RST-002, so its conditional SENSE thresholds are falling
3.000823..3.094473 V and rising 3.019119..3.113279 V, and C143 gives a
0.815..1.526 ms charge-only release delay
(`design/reset_coordination_tps3890.md` method). Its VDD (SYS_AON) is
independent of the monitored rail.

Powered/unpowered cases (static reasoning, not a transient proof):

- +3V3_MCU missing or below threshold with SYS_AON present: U1 and U37 are
  unpowered; U38 asserts RESET and holds EN <= 0.25 V; R117 also pulls EN low.
  R118 is referenced to the same missing rail, so PG cannot back-power P904.
- MCU in reset or GPIO unconfigured: P107 is Hi-Z with no pull-up; R122 holds
  IN1 low, so Y is low even with permission present.
- MAIN_RUN_PERMIT absent: Q5 is off and R121 forces IN2 high, so Y = IN0 = GND.
- SYS_AON missing: U36 has no input and U38 is below its 1.5 V operating
  minimum. EN may follow U37 only if +3V3_MCU survives without SYS_AON; that
  combination, U36 EN-with-VIN-absent limits and U38 RESET below VPOR still
  need confirmation against the final SYS_AON architecture.
- Firmware must not enable the P107 internal pull-up (-10..-300 uA, Table 2.7)
  and must treat PG as valid only with EN high and VIN present.

ERC and the dangling stub: the earlier unconnected-wire-endpoint warning was
the audio-sheet AUDIO_AUX_EN wire from R123 pin 2 (346.71 mm) extending to
360.68 mm past its label at 353.06 mm. The label already joined the net, so
the extra stub was trimmed natively to end at the label; no net changed.

Validation. KiCad CLI was not reachable from this session, so the saved
design was exported from the KiCad 10.0.6 schematic editor GUI: full XML
netlist (343 components), ERC report, native BOM and Plot-all-pages PDF.
The pre-change and post-change 339-component netlists differ only by the
intended merge of Net-(U37-IN1) {R122.1, U37.1} with the former U1.N5
singleton; J4/TP1-TP3 (BOM-excluded) sit on untouched sheets. Field edits
changed only R122-R125, C143, U37 and U38 role/procurement text; part numbers
and dated sourcing snapshots are unchanged and are labelled historical where
they predate this role. BOM fidelity passes for 339 references, 19 columns,
4 native exclusions. The MCU map passes with 111 connected, 77 open and
11 named singletons. ERC under unchanged project settings falls from 117
(100 errors, 17 warnings) to 115 (99 errors, 16 warnings): the P107
unconnected-pin error and the stub warning are gone, nothing is added, and
no exclusion was added. Four categories remain ignored by project settings.
The 15-page PDF changes only pages 1, 2 and 15 (pixel comparison); those
pages were rendered and inspected. Clock and other repository checks pass.

Remaining: the SYS_AON upstream source and its power-flag/ERC findings, U36
converter qualification, startup/collapse and transient timing of U37/U38/Q5,
hot leakage of Q5 and board, RA8P1 manual confirmation of the VCC2/VCC port
domains, firmware sequencing, and independent headphone DC/rail/thermal
disconnect.
