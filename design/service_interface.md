# Production service interface

Revision 1 contract dated 2026-09-07, with native implementation checkpoints
below through 2026-10-05, for issues #824/#826. Drawn and netlist-verified
connections do not establish completed electrical or fixture qualification.
Retain one user power button. Programming uses protected copper contacts
and a fixture, not three additional user buttons. Read alongside
[boot/reset](boot_and_debug.md) and [radio circuitry](radio_interface.md).
Those records describe earlier SW1/SW2/SW3 revisions; the following contact
contract replaces their mechanical-button interpretation only.

## SERVICE-001: existing contacts and RA8P1 recovery

Each TP below is a TWO-contact copper pattern, normally open. Contact 1 is
the signal and contact 2 GND. Neither is a populated switch or a permanent
short. Keep the existing bias resistors; do not attach a pull-up from a
fixture supply to these signals. Fixture controls are open-drain sinks.

| Pattern | Contact 1 | Contact 2 | Function |
| --- | --- | --- | --- |
| TP1, replaces SW1 | SW_RESET_N, U2 MR pin 3 | GND | Delayed supervisor reset request |
| TP2, replaces SW2 | MCU_BOOT_MD, U1 P201/MD | GND | Select serial boot while RES is cycled |
| TP3, replaces SW3 | C6_BOOT_N, U3 contact 15/GPIO9 | GND | Select C6 download boot |

TP1 is NOT the direct MCU RES net. Use J1.10/MCU_RESET_N for the fixture's
controlled reset hold. Do not connect U2 MR to its RESET output. Keep the
no-capacitor RES implementation and existing supervisor release delay.

The selected 289-ball RA8P1 reuses two existing J1 contacts for SCI9 ROM
programming. No second MCU UART header or new MCU signal allocation is
needed. These contacts must not be driven by a debugger simultaneously.

| J1 contact | Existing debug name | SCI9 service use |
| --- | --- | --- |
| 1 | +3V3_MCU | Target voltage sense only; never fixture power injection |
| 6 | DBG_TDO_SWO, U1 E7/P209 | TXD9: MCU output to fixture RX |
| 8 | DBG_TDI, U1 C7/P208 | RXD9: fixture TX to MCU input |
| 10 | MCU_RESET_N, U1 D5/RES | Open-drain fixture reset |
| 3/5/9 | GND | Common reference |

J1.2/SWDIO and J1.4/SWCLK retain their debug roles; J1.7 remains NC/key.
SCI9 and SWD/JTAG are alternative fixture personalities, not concurrent
drivers. Keep all fixture MCU-facing outputs high impedance when the target
rail is absent. The radio translator below does not protect J1.

[RA8P1 HUM](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware),
Rev.1.30, sections 4.3-4.4 and 60.11, Tables 60.39-60.40, establishes the
SCI9 mapping and boot restrictions. MD low plus an external RES cycle
selects SCI/USB boot; POR alone is insufficient. USB ROM boot needs USBFS
DP/DM/VBUS, not the product USBHS port. SCI remains the no-crystal fallback:
allow up to 3 s for boot connection with neither main nor subclock present.
With main clock the listed maximum is 1 s; subclock-only is 2 s. USB requires
one of those external clock sources. Do not qualify unfinished crystals.
Lifecycle, authentication, TrustZone and boot configuration can restrict
access; these pads do not guarantee recovery from every security state.

## SERVICE-002: C6 fixture contacts and power ownership

J4 is the five-contact internal C6 service group, instantiated with the
project-local Connectors:Service_Contacts_05 symbol. It represents PCB copper
contacts, is excluded from the purchased-parts BOM and retained on the board.
Its physical pad footprint, geometry and access remain pending fixture and
enclosure mechanics. TP3 is separate BOOT access. Ground make-first/break-last
is a fixture requirement; the schematic drawing does not establish contact order.

| Contact | Net | Fixture action |
| --- | --- | --- |
| 1 | GND | Make first, break last |
| 2 | SERVICE_VIO | Supply 3.3 V logic reference; also selects service mode |
| 3 | SERVICE_TX | Fixture TX, idle high, into translator A1 |
| 4 | SERVICE_RX | Fixture RX, from translator A2Y |
| 5 | SERVICE_C6_RESET_N | Open-drain reset request, never push-pull high |

SERVICE_VIO powers only the translator A domain and feeds service-selector
inputs. It does not feed +3V3_MCU, +3V3_RADIO, J1.1 or the board power tree.
Power the board through its intended system-power path. A fixture must
provide the power-latch service control specified by the power design if
the single user button cannot maintain that path. Do not bypass the radio
load switch by injecting power at its output.

This is a service-only UART, not a transparent logging connector: applying
SERVICE_VIO explicitly takes radio ownership away from the host. Normal
operation requires SERVICE_VIO absent or actively held at 0 V. A separate
presence/mode contact is unnecessary under this restricted contract.

## SERVICE-003: exact radio arbitration

Use four additional TI SN74LVC1G97DBVR devices, retaining existing U7/U8
as the normal-path generators. This is a small, single-MPN implementation
of four independently controlled outputs, not a proof of globally minimum
gate count. A quad SN74LVC157A is not substituted without separately
closing its input-edge and powered-off interface requirements.

[DigiKey 296-15581-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G97DBVR/571196)
checked 2026-09-07: indexed stock 30,155, USD 0.23/0.16/0.12130 at
1/10/100 units. Four gates cost USD 0.92 at the single-unit snapshot,
excluding passives, translator, tax and shipping; stock is not reserved.

[TI SCES416N](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf),
sections 5, 6.5 and 8.4, is the pin/truth-table authority. DBV pin 6 selects
pin 3 when high, pin 1 when low. All inputs have Schmitt behavior. Ioff
is specified at VCC=0; it is not a sub-minimum-supply logic guarantee.

Native references U28/U29/U30/U31 correspond to the four role labels below.
EVERY added gate: pin 5 to +3V3_MCU, pin 2 to GND, pin 6 to SERVICE_VIO,
and one 100 nF local bypass from pin 5 to GND. Reuse the documented
TDK C1608X7R1H104K080AA selection. No gate output is tied to another output.

| Gate role | Pin 1 IN1: normal | Pin 3 IN0: service | Pin 4 Y destination |
| --- | --- | --- | --- |
| SERVICE_POWER | RADIO_PWR_EN host request | +3V3_MCU | RADIO_PWR_REQ_EFF -> R7 input |
| SERVICE_RESET | RADIO_MR_NORMAL_N, existing U7.4 | SERVICE_C6_RESET_N | RADIO_MR_N -> U6.3 |
| SERVICE_SPI | SPI_IO_EN_NORMAL, existing U8.4 | GND | SPI_IO_EN -> U5.8, U25.6 and existing R9 |
| SERVICE_UART | GND | C6_EN | SERVICE_UART_OE -> TXU0202.6 |

Reroute R7 away from the raw host request to SERVICE_POWER.4. Preserve
R7/R8's ON divider. Rename the old U7/U8 output nets as above and insert
the new gates; do not merely add new drivers to the old nets. U8 continues
to receive the RAW host RADIO_PWR_EN request, not RADIO_PWR_REQ_EFF.
U7 retains its MCU_RESET_N and host RADIO_RESET_REQ_N inputs.

Saved-netlist review, 2026-10-04: SPI_IO_EN presently contains U8.4,
U5.8, U25.6 and R9.1. U25 is the radio-to-host status translator, so
service isolation must disable it together with U5. Rename only the
normal generator side when inserting SERVICE_SPI; preserve U25.6 on
the effective output net. Acceptance requires verifying both OE pins,
the default pull-down and absence of the old U8 output on the effective
net. This corrects an omitted destination in the implementation table.
SERVICE-016 implements U28 power arbitration, SERVICE-017/018 implement
U29 reset arbitration and release bias, and SERVICE-019 implements U30 SPI
isolation. SERVICE-020 implements U31 UART enable selection.

U6 remains TPS389001DSET: upstream +3V3_MCU powers VDD pin 4;
SENSE pin 1 monitors the switched radio rail; RESET pin 6 drives C6_EN.
Service reset enters MR pin 3 through the mux. Neither the undervoltage
monitor nor its delayed release is bypassed. Do not directly drive C6_EN.

Use R110/R111, two parallel 1k resistors from SERVICE_VIO to GND
(effective 500 ohms), YAGEO RC0603FR-071KL; see SERVICE-025. Add 10k from SERVICE_C6_RESET_N to
+3V3_MCU. SERVICE_UART_OE needs a 47k pull-down to GND. Use 47k pull-up
resistors as specified below; their exact MPN/temperature rating remains
a BOM selection, not inferred from the 10k part.

Let S mean a valid high SERVICE_VIO, P the raw host power request,
R the normal U7 output, E the qualified C6_EN, and F fixture reset release.

| S | Effective power request | U6 MR | SPI OE | UART OE |
| --- | --- | --- | --- | --- |
| 0 | P | R | P AND E | 0 |
| 1 | 1 | F | 0 | E |

The steady-state table prevents a broken host from blocking service power
or reset and prevents SPI driving during service. It is NOT a glitch-free
handover guarantee: hold both processors in reset before changing S.

## SERVICE-004: TXU0202 directions and idle bias

Select TI TXU0202DCUR, DCU VSSOP-8, requested distributor identifier
296-TXU0202DCURCT-ND; verify its current sourcing before procurement.
Pin mapping follows [TI SCES942A](https://www.ti.com/lit/ds/symlink/txu0202.pdf),
sections 6 and 9. A and B are power domains, not interchangeable UART labels.

| Pin | Name | Connection |
| --- | --- | --- |
| 1 | B2 | U3.25 TXD0/GPIO16 |
| 2 | GND | Common GND |
| 3 | VCCA | SERVICE_VIO; 100 nF local bypass |
| 4 | A2Y | SERVICE_RX, fixture input |
| 5 | A1 | SERVICE_TX, fixture output |
| 6 | OE | SERVICE_UART_OE, 47k pull-down |
| 7 | VCCB | +3V3_RADIO; 100 nF local bypass |
| 8 | B1Y | U3.24 RXD0/GPIO17 |

Proposed bias: A1 to SERVICE_VIO through 10k; B2 to +3V3_RADIO through
10k; A2Y to SERVICE_VIO through 47k; B1Y to +3V3_RADIO through 47k.
Thus disconnected/high-impedance transmitters have a local idle-high
input, and disabled translator outputs also idle high. The translator's
internal weak pull-downs alone would instead permit a UART break level.
Do not connect either external pull to the opposite power domain.

OE is active high, qualified by both adapter presence and C6_EN. Its high
level is not supplied by an absent adapter. Rail-zero isolation and Ioff
are not permission to drive arbitrary signals during brownout. The
datasheet's floating-supply condition is not equivalent to this circuit's
resistively discharged SERVICE_VIO. Validate actual disconnect waveforms.
Added radio bypass is 0.1 uF nominal; update the load-switch discharge and
startup model. Include the new C6_EN gate input in its leakage budget.

## SERVICE-005: adapter contract and conditional arithmetic

No actual adapter is selected or qualified. Require SERVICE_VIO=3.3 V
+/-5%, at least 20 mA available, and common ground (SERVICE-025). Reject RS-232 levels,
5 V TTL adapters and adapters that source board power through UART pins.
Require fixture TX VOH >= VIO-0.1 V and VOL <=0.1 V at 0.5 mA, RX input
leakage <=10 uA, RX VIH <=0.7*VIO and VIL >=0.3*VIO. Reset outputs must
sink 1 mA at <=0.1 V, leak <=10 uA when released, and tolerate a live
3.6 V target when the fixture is off. These are acceptance requirements,
not characteristics attributed to a generic USB-UART adapter.

Use the existing 1% resistor plus 100 ppm/K, 100 K arithmetic envelope:
1k = 980.1..1020.1 ohm; 10k = 9801..10201 ohm; 47k = 46064.7..47944.7 ohm. The latter requires
an actual resistor meeting that specification. At <=100 uA loading, use
the devices' supply-wide VOH >= VCC-0.1 and VOL <=0.1 bounds. The 47k
output pulls allow that light-load screen; a 10k output pull would not.
Allocate 12 uA total additional output load including receiver and board.
Allocate 60 uA adverse current into absent SERVICE_VIO, and 20 uA adverse
current at released fixture reset. Each is a requirement to verify.

The following checks deliberately separate supply-wide output arithmetic
from the 3 V Schmitt threshold TEST POINT. Neither TI table gives a 3.3 V
DC threshold row: interpolation is not promoted to a guaranteed limit.
Resolve full rail-range input compatibility before release. The existing
U6 MR load-current qualification remains open under RADIO-015.

```sh
python3 - <<'PY'
from fractions import Fraction as F
from itertools import product

r10lo, r10hi = F(9801), F(10201)
r47lo, r47hi = 47*r10lo/10, 47*r10hi/10
assert F('3.6')/r47lo + F('0.000012') < F('0.0001')
assert F('0.000012')*r47hi < F('.89')  # OE low, 3 V test point
assert F('0.000060')*(r10hi/2) < F('.35')  # lowest listed gate VT-
assert F('3.465')/(r10lo/2) < F('.001')  # presence pull current
reset_high = F(3)-F('.000020')*r10hi
assert reset_high > F('1.87')  # gate VT+ at 3 V only
assert F(3)-F('.1') > F('1.92')  # OE high at 3 V test point
assert F('.1') < F('.89')  # OE low at 3 V test point
assert F('3.135')-F('.1') > F('.7')*F('3.465')
assert F('.1') < F('.3')*F('3.135')  # translator -> fixture RX
assert F('3.465')/r10lo + F('.000012') < F('.0005')

def mux(s, normal, service):
    return service if s else normal

for s, p, r, e, f in product((0, 1), repeat=5):
    got = (mux(s, p, 1), mux(s, r, f), mux(s, p & e, 0), mux(s, 0, e))
    want = (1, f, 0, e) if s else (p, r, p & e, 0)
    assert got == want
print('SERVICE PASS: 32 steady states and conditional DC screens only.')
print('Adapter, intermediate-rail thresholds, ramp and timing approval open.')
PY
```

## SERVICE-006: fixture sequence and release gates

1. Connect ground; put UART TX low or high impedance until its VIO is
   valid. Assert J1.10 MCU reset and fixture C6 reset with open-drain sinks.
   Short TP3.1 to TP3.2. Keep TP2 released for C6-only service.
2. Establish intended board power and hold MCU reset throughout C6 service.
   Apply SERVICE_VIO, select idle-high TX, and wait for a valid switched
   radio rail. U6 must remain able to veto EN while its SENSE is low.
3. Release SERVICE_C6_RESET_N. Confirm supply stabilization and EN timing;
   keep GPIO9 low through at least 3 ms after EN rises, with GPIO8 high.
   Release TP3 only after the strap interval. Program through UART0.
4. For exit, assert C6 reset again, then take adapter TX low/high impedance
   and remove SERVICE_VIO. Keep MCU reset held while the selector returns
   to normal and radio power/reset settle. Release fixture C6 reset and
   MCU reset last; disconnect ground last.

For RA8 SCI service instead, use TP2 low and J1.10 held low for at least
3 ms after VCC is valid, then release RES with MD still low. Respect the
ROM connection interval and do not share J1.6/J1.8 with an attached driving
debugger. SCI fixture voltage compatibility requires its own target-side
qualification; the C6 adapter contract is not automatic approval for J1.

Before declaring implementation complete: native pin/netlist review;
independent truth-table review; exact 47k/passive/fixture sourcing;
full-range threshold and all leakage bounds; U6 MR loading; unpowered
and brownout states; mode-change glitches; supervisor/strap timing;
updated radio charge/discharge load; pad ESD and mechanical access;
and physical recovery trials with host firmware absent. Authentication
restrictions and unfinished clocks remain outside this recovery claim.

## SERVICE-007: UART translator library checkpoint

The project-local `Power_Devices:TXU0202DCUR` symbol is now available.
It was created in the native KiCad Symbol Editor as an independent symbol;
the existing TXU0102DCUR and all other library symbols are unchanged.
TI [SCES942A Table 6-1](https://www.ti.com/lit/ds/symlink/txu0202.pdf)
establishes the DCU mapping: 1 B2 input, 2 GND, 3 VCCA, 4 A2Y tristate
output, 5 A1 input, 6 OE input, 7 VCCB, and 8 B1Y tristate output.
The drawing shows A1-to-B1Y and B2-to-A2Y separately. Supply pins use
power-input types; all eight pins occur once, with 150 mil legs and
100 mil connection grids. Visible fields and pin text are 50 mil.

Sourcing metadata identifies Texas Instruments TXU0202DCUR and
[DigiKey 296-TXU0202DCURCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/TXU0202DCUR/16677096).
This identifies an ordering code, not reserved stock or a price commitment.
The footprint remains blank pending the deferred package-qualification work.
The hidden Footprint and Datasheet fields retain inherited off-origin
positions; normalize those cosmetic positions before final library acceptance.

This checkpoint adds the library symbol only. SERVICE-003/004 wiring,
fixture contacts, bypass and bias resistors, and the SERVICE-006 acceptance
gates remain open. No new schematic instance or BOM row is claimed.
KiCad exported the symbol's unit for visual review. The refreshed complete
14-page schematic PDF is pixel-identical to the previously reviewed checkpoint;
native ERC remains 101 errors and 11 warnings. Clock arithmetic and the
SERVICE-005 32-state/conditional-DC checks pass with their stated limitations.

## SERVICE-008: native U27 placement WIP

U27 now instantiates the TXU0202DCUR on the radio sheet (PDF page 6).
Pin 8 B1Y has a wire stub named `C6_UART_RX`; the other end at U3.24
is not implemented yet. The other seven U27 pins remain visibly open.
This saves the beginning of circuit integration, not a working recovery
interface. SERVICE-003/004 supply, ground, enable, UART, bypass, bias and
fixture connections remain to be implemented and checked.

Native netlist review finds 278 components and confirms that every existing
net's pin membership is preserved. ERC is 114 errors and 12 warnings:
the added 13 errors and one warning all concern unfinished U27 connections.
The previous 101 errors and 11 warnings are unchanged. No ERC exclusions
or no-connect markers were added. KiCad also regenerated the orientation
sheet's document UUID on save; its drawing and connectivity are unchanged.

The complete 14-page PDF was regenerated and rendered. Page 6 adds U27 in
the open lower area; the other 13 pages are pixel-identical to the prior
reviewed export. Clock arithmetic and SERVICE-005 conditional checks pass.

## SERVICE-009: radio UART and ground wiring checkpoint

Native KiCad wiring now connects U27.8 (B1Y) to U3.24 (RXD0/GPIO17)
through `C6_UART_RX`, and U3.25 (TXD0/GPIO16) to U27.1 (B2)
through `C6_UART_TX`. U27.2 is connected to the existing global GND.
The exported netlist confirms these exact UART pairs and preserves all
other pin connectivity. No parts were added beyond the ground symbol.

This remains WIP: U27 VCCA, VCCB, OE, A1 and A2Y are open. Supply
bypass, idle bias, fixture contacts and SERVICE-003 arbitration remain
to be implemented; the recovery interface is not operational or qualified.

ERC is now 108 errors and 11 warnings, removing six errors and one
warning from SERVICE-008 with no added findings. No ERC exclusions or
no-connect markers were added. Native save again regenerated only the
orientation sheet's document UUID; its drawing and nets are unchanged.
The project also records the newly used ground-symbol designator.

The complete 14-page PDF was regenerated and rendered. Page 6 was
visually reviewed; the other 13 pages are pixel-identical to the previous
reviewed export. Clock arithmetic and SERVICE-005 conditional DC and
32-state checks pass, with their existing qualification limitations.

## SERVICE-010: translator supply routing checkpoint

U27.7 VCCB now joins the existing switched `+3V3_RADIO` net. U27.3
VCCA has a separate local `SERVICE_VIO` rail. Exact netlist comparison
confirms only this addition to the radio rail and preserves all other
pin connectivity. SERVICE_VIO currently contains only U27.3: its fixture
source, selector loads, discharge resistors and bypass are still open.
No power flag was added to conceal that unfinished supply source.

Native ERC is 105 errors and 12 warnings: three previous supply-pin errors
are resolved, and the isolated SERVICE_VIO label adds one expected warning.
The VCCA undriven-power error remains. The native save changed the
orientation sheet's document UUID only and recorded #PWR0242 in the
project designator inventory. No other drawing or net change is intended.

All 14 PDF pages were regenerated and rendered; page 6 was reviewed and
the other 13 pages are pixel-identical to SERVICE-009. Clock arithmetic and
SERVICE-005 conditional checks pass. Next, implement the two local 100 nF
bypass capacitors, idle-bias network, fixture-side signals and enable
arbitration. This supply-routing checkpoint does not qualify operation.

## SERVICE-011: local translator bypass checkpoint

C116 and C119 now provide separate 100 nF supply-to-ground bypasses for
U27 in the native schematic. C116.1 joins SERVICE_VIO and U27.3 (VCCA);
C119.1 joins +3V3_RADIO and U27.7 (VCCB). Both capacitor pin 2 returns
join GND and U27.2. Future PCB placement must keep C116 close to the
U27 3-to-2 pin pair and C119 close to the 7-to-2 pin pair, with short
return paths. Physical placement and transient qualification remain open.

Both use the existing sourced TDK C1608X7R1H104K080AA, 100 nF, 50 V,
X7R, +/-10%, preserving the explicitly dated sourcing snapshot. The added
nominal load is 0.1 uF on each supply; radio startup/load calculations still
need to include the completed service circuit. Footprints remain deferred.

The 280-component exported netlist preserves every previous net's pin
membership after excluding only C116/C119, and verifies all four new
capacitor terminals. Native ERC is 105 errors and 11 warnings: the isolated
SERVICE_VIO-label warning is removed, with no new findings. Its unfinished
fixture source still causes an undriven-power error; OE, fixture UART,
bias and arbitration remain open. No ERC exclusions, power flags or
no-connect markers were added.

All 14 PDF pages were regenerated and rendered. Page 6 was visually
reviewed; the other 13 pages are pixel-identical to SERVICE-010. Clock
arithmetic and SERVICE-005 conditional DC/32-state checks pass. KiCad's
save also regenerated the orientation sheet document UUID only and updated
the project designator inventory. This is an incremental WIP checkpoint.

## SERVICE-012: UART enable pull-down checkpoint

R104 now connects U27.6 (OE), named `SERVICE_UART_OE`, to GND through
47 kohm. It uses YAGEO RC0603FR-0747KL, 1%, 100 ppm/C, with the existing
2026-09-12 sourcing snapshot retained as historical, unreserved information.
Its description and procurement fields identify the U27 enable role;
footprint and installed leakage/sequencing qualification remain deferred.
The SERVICE-005 conditional resistance/leakage screen still applies.

The exported 281-component netlist verifies R104.1 = U27.6 and R104.2 =
GND. Excluding only R104 preserves every previous net's pin membership.
Native ERC is 103 errors and 11 warnings, with no new findings. The two
removed findings are U27 OE unconnected and undriven input; the resistor
provides a ground path but does not implement the SERVICE-003 enable gate.
Fixture UART, idle bias, fixture source and service arbitration remain open.
No ERC exclusions, power flags or no-connect markers were added.

All 14 PDF pages were regenerated and rendered. Page 6 was reviewed;
the other 13 pages are pixel-identical to SERVICE-011. The C116 ground
text was moved clear of the new signal wire. Clock arithmetic and the
SERVICE-005 conditional DC/32-state checks pass. KiCad's native save also
updated the designator inventory and regenerated only the orientation
sheet document UUID. This remains an incremental WIP checkpoint.

## SERVICE-013: UART output idle-bias checkpoint

R105 and R106 now implement the two 47 kohm output pull-ups from
SERVICE-004. R105.1 joins SERVICE_VIO / U27.3, and R105.2 joins
U27.4 (A2Y), now named SERVICE_RX. R106.1 joins +3V3_RADIO / U27.7,
and R106.2 joins C6_UART_RX / U27.8 (B1Y) / U3.24. The supplies
remain separate; SERVICE_RX crosses SERVICE_UART_OE without a junction.

Both resistors use YAGEO RC0603FR-0747KL, 1%, 100 ppm/C. Their
metadata identifies the output pull-up role and retains the dated,
unreserved 2026-09-12 sourcing snapshot. Footprints remain deferred.
The SERVICE-005 conditional resistance/leakage screen applies; this
checkpoint does not establish installed leakage or sequencing performance.

The 283-component native netlist verifies every new resistor terminal
and preserves all previous pin memberships after excluding R105/R106.
Native ERC is 102 errors and 11 warnings: U27.4 is no longer unconnected,
with no added findings. No ERC exclusions, power flags or no-connect
markers were added. The two 10 kohm input pull-ups, fixture TX/contact
integration, fixture supply source and SERVICE-003 arbitration remain
unfinished; the recovery interface is not yet operational or qualified.

The full 14-page PDF was regenerated and rendered. Page 6 was visually
reviewed, and the other 13 pages are pixel-identical to SERVICE-012.
Clock arithmetic and SERVICE-005 conditional DC/32-state checks pass.
KiCad's save updated the resistor designator inventory and regenerated
only the orientation sheet document UUID outside the radio drawing.

## SERVICE-014: Fixture UART input idle-bias checkpoint

R107 implements the fixture-side 10 kohm input pull-up from SERVICE-004.
R107.1 joins SERVICE_VIO / U27.3; R107.2 joins U27.5 (A1), now named
SERVICE_TX. Its crossing of SERVICE_UART_OE has no junction. R10 and
all prior connectivity are unchanged. The part is YAGEO RC0603FR-0710KL,
1%, 100 ppm/C, with the existing 2026-09-05 sourcing snapshot retained
as historical, unreserved information. Footprint qualification is deferred.

The exported 284-component netlist verifies both R107 terminals and
preserves every prior net's pin membership after excluding only R107.
Native ERC is 100 errors and 11 warnings, with no added findings. U27.5
is no longer unconnected or undriven because of its pull-up path; this
does not implement the fixture transmitter or establish a working service
interface. The radio-side 10 kohm input pull-up, fixture contacts/supply
and SERVICE-003 arbitration remain unfinished. Installed leakage and
sequencing qualification remain open. No ERC exclusions, power flags or
no-connect markers were added.

The complete 14-page PDF was regenerated and rendered. Page 6 was
visually reviewed; the other 13 pages are pixel-identical to SERVICE-013.
Clock arithmetic and SERVICE-005 conditional DC/32-state checks pass.
KiCad's save updated the designator inventory and regenerated only the
orientation sheet document UUID outside the radio drawing.

## SERVICE-015: radio UART input idle-bias checkpoint, 2026-10-04

R108 completes the second 10 kohm input pull-up from SERVICE-004.
R108.1 joins +3V3_RADIO / U27.7, and R108.2 joins C6_UART_TX /
U27.1 (B2) / U3.25. The crossing with C6_UART_RX has no junction.
It uses YAGEO RC0603FR-0710KL with the existing historical sourcing
fields copied from R107. Its supply remains separate from SERVICE_VIO.
The SERVICE-005 conditional bias requirements continue to apply.

The current 285-component native export verifies both resistor terminals.
Excluding R108 preserves every prior pin partition and all prior component
records. ERC finding identities and configured ignored checks are unchanged:
100 errors and 11 warnings. No exclusions, power flags or no-connect markers
were added. The complete 14-page PDF was refreshed; page 6 was visually
reviewed and the other 13 rendered pages are pixel-identical to SERVICE-014.
The main-rail inventory and sensor connection/arithmetic checks pass.

Both UART input pull-ups are now drawn. Fixture contacts/source, service-mode
discharge, reset bias and the four SERVICE-003 arbitration gates remain
unfinished. R104 does not substitute for the missing qualified OE driver.
This checkpoint does not establish an operational recovery interface.

## SERVICE-016: native service power selector, 2026-10-04

U28 instantiates Power_Devices:SN74LVC1G97DBVR as SERVICE_POWER.
Pin 1 receives raw RADIO_PWR_EN, pin 3 is tied high to +3V3_MCU,
pin 6 receives SERVICE_VIO, and pin 4 drives RADIO_PWR_REQ_EFF / R7.1.
Pin 5 uses +3V3_MCU and pin 2 GND. C120 is the local 100 nF
TDK C1608X7R1H104K080AA supply bypass; place it close to U28.5/2
in the deferred PCB work. Instance fields identify this service role and
retain historical, unreserved sourcing information.

The RADIO_PWR_EN hierarchical label was relocated from R7's input to
U28's normal-input wire, preserving U1.F16 and U8.6 on the raw request.
R7/R8's divider is unchanged. The saved 287-component netlist confirms
all six U28 pins and both C120 terminals. Its only change to existing
pin partitions is moving R7.1 from the raw request to the effective output.
No existing component record changed. Native ERC retains the same finding
identities: 100 errors and 11 warnings; no exclusions or power flags added.

The selector truth function follows TI SCES416N sections 5/8.4; this is a
steady-state wiring implementation, not completed service qualification.
SERVICE_VIO still lacks its fixture source and two discharge resistors.
Reset, SPI and qualified UART enable gates, reset bias, fixture contacts,
full rail-range thresholds, leakage, sequencing and recovery trials remain
open. Keep both processors in reset during mode changes as SERVICE-006
requires. The U28 supply current, input leakage and dynamic power must be
included in the final power budget; C120 adds 0.1 uF nominal to the main
rail inventory without qualifying its effective-capacitance ceiling.

The complete 14-page PDF was regenerated. Rendering the previous and current
PDFs with the same settings confirms only page 6 changed; its new selector,
bypass and R7 input label were visually reviewed. The other 13 pages are
pixel-identical. Main-rail inventory and sensor topology/arithmetic checks pass.

## SERVICE-017: native service reset selector, 2026-10-04

U29 instantiates Power_Devices:SN74LVC1G97DBVR as SERVICE_RESET.
Its pin 1 receives RADIO_MR_NORMAL_N / U7.4; pin 3 receives
SERVICE_C6_RESET_N; pin 6 selects with SERVICE_VIO. Pin 4 drives
RADIO_MR_N / U6.3 (MR), pin 5 uses +3V3_MCU, and pin 2 is GND.
C121 is the local 100 nF TDK C1608X7R1H104K080AA supply bypass.
Place it close to U29.5/2 during deferred PCB work. Exact ordering codes
and historical, unreserved sourcing fields are retained in native instances.

The former U7 output label is now RADIO_MR_NORMAL_N. This is the only
existing-pin migration: U7.4 leaves RADIO_MR_N and feeds U29.1.
U6's SENSE divider, timing capacitor and delayed RESET output are unchanged.
The 289-component saved export confirms all six U29 pins and both C121
terminals; every one of the previous 287 component records is unchanged.
Excluding the new components and the intended U7.4 migration preserves
every existing pin partition.

This is an incomplete integration checkpoint. SERVICE_C6_RESET_N still
lacks its 10 kohm MCU-rail pull-up and fixture contact/driver. Native ERC
therefore adds one undriven-input error at U29.3 and one isolated-label
warning for that input: 101 errors and 12 warnings. All 111 baseline
finding identities remain present; none were masked or excluded. The
reset bias is the next native addition. SERVICE_VIO source/discharge,
SPI and UART enable selectors, fixture contacts and full sequencing,
threshold, leakage and recovery qualification remain open. Hold both
processors in reset during mode changes; no glitch-free switching claim
follows from this steady-state mux wiring.

C121 adds 0.1 uF nominal to the main inventory, now 512.41 uF direct
and 522.41 uF including FB1. U29 current and switching load must also be
included in final power budgets. The capacitance ceiling remains conditional.

The full 14-page PDF was regenerated and rendered with matching baseline
settings. Only page 6 changed; U29, C121 and the renamed U7 output were
visually reviewed, and the other 13 pages are pixel-identical. Main-rail
inventory, sensor topology/conditional arithmetic and clock arithmetic pass.
Older RADIO-015 prose still names U7's former output; reconcile that native
annotation with SERVICE-017 during the next reset-bias integration pass.

## SERVICE-018: native service reset release bias, 2026-10-04

R109 is YAGEO RC0603FR-0710KL, 10 kohm, 1%, 100 ppm/C.
Pin 1 joins +3V3_MCU; pin 2 joins SERVICE_C6_RESET_N / U29.3.
Native fields retain the historical unreserved sourcing snapshot and identify
the conditional SERVICE-003/005 selection basis. With the existing 1%
tolerance and 1% temperature allocation, resistance is 9801..10201 ohm.
The 20 uA release-leakage allocation remains conditional; fixture open-drain
sink capability, installed leakage and sequencing are not yet qualified.

The saved 290-component export adds only R109. All 289 prior component
records and every prior pin-to-net assignment are unchanged. U6 SENSE,
timing capacitor and delayed RESET path remain intact. ERC removes only
the U29.3 undriven-input error and isolated-label warning: 100 errors and
11 warnings remain. No new finding, exclusion or power flag was added.
Native RADIO-015 now describes U7's normal output through U29 to U6;
its original calculations remain in design/radio_interface.md.

Main-rail inventory, sensor topology/conditional arithmetic and clock
arithmetic checks pass. The full 14-page PDF was refreshed; only page 6
changed and was visually reviewed. The other 13 pages render identically.
SPI and UART enable selectors, SERVICE_VIO source/discharge, fixture
contacts and full-rail threshold, leakage, sequencing and recovery
qualification remain unfinished. This is still an integration checkpoint.

## SERVICE-019: native service SPI isolation, 2026-10-04

U30 is TI SN74LVC1G97DBVR, using SCES416N sections 5, 6.5 and 8.4.
Pin 1 receives SPI_IO_EN_NORMAL / U8.4, pin 3 is GND, and pin 6
selects with SERVICE_VIO. Pin 4 drives effective SPI_IO_EN / U5.8,
U25.6 and R9.1; pin 5 uses +3V3_MCU and pin 2 is GND. Valid high
SERVICE_VIO selects grounded pin 3; valid low selects the normal U8
AND output. This is a steady-state function, not glitch-free arbitration.
C122 is TDK C1608X7R1H104K080AA, 100 nF, 50 V, X7R, 10%, directly
between +3V3_MCU and GND; place near U30.5/2 during deferred PCB work.
Native instances retain exact ordering codes and historical unreserved
sourcing snapshots. No current availability or reservation is implied.

The saved export contains 292 components. Relative to SERVICE-018, only
U30 and C122 are added. U8.4's intended migration from SPI_IO_EN to
SPI_IO_EN_NORMAL is the only existing-pin net change; U8's raw
RADIO_PWR_EN input remains intact. U30's six pins and both C122 terminals
are verified in the saved netlist. Native RADIO-016 and U8/U30 metadata
now distinguish normal and effective enable signals.

ERC remains 100 errors and 11 warnings with no new finding, exclusion or
power flag. SERVICE_VIO still lacks its source/contact and discharge bias;
the UART enable selector and fixture contacts remain unfinished. Full-rail
thresholds, mode-change sequencing, leakage, recovery behavior and final
power budgets remain qualification work. Hold both processors in reset
during mode changes per SERVICE-003; do not infer transition safety from
the truth table or ERC count.

C122 adds 0.1 uF nominal: main inventory is 512.51 uF direct and 522.51 uF
including FB1, with 555.01 uF stored across main/FB1/radio/SD branches.
These are nominal inventories, not a qualified effective-capacitance ceiling.
Main-rail inventory, sensor topology/conditional arithmetic and clock checks
pass. The complete 14-page schematic PDF is refreshed with this checkpoint.
Only page 6 changed and was visually reviewed; the other 13 pages render
identically to SERVICE-018.

## SERVICE-020: native service UART enable selector, 2026-10-04

U31 is TI SN74LVC1G97DBVR, using SCES416N sections 5, 6.5 and 8.4.
Pin 1 is GND, pin 3 receives C6_EN, and pin 6 selects with SERVICE_VIO.
Pin 4 drives SERVICE_UART_OE / U27.6 / R104.1; pin 5 uses +3V3_MCU
and pin 2 is GND. Valid high SERVICE_VIO selects C6_EN; valid low
selects GND, disabling the service translator in normal mode. This
steady-state truth table does not establish safe mode transitions.
C123 is TDK C1608X7R1H104K080AA, 100 nF, 50 V, X7R, 10%, between
+3V3_MCU and GND; place near U31.5/2 during deferred PCB work.
Native instances retain exact ordering codes and historical unreserved
sourcing snapshots; these do not establish current availability.

The saved export contains 294 components, adding only U31 and C123.
All 292 prior component records and every prior pin-to-net assignment
are unchanged. All six U31 pins and both C123 terminals are verified.
ERC remains 100 errors and 11 warnings with identical finding records;
no exclusion, power flag or masking was introduced.

C123 adds 0.1 uF nominal: main inventory is 512.61 uF direct and
522.61 uF including FB1, with 555.11 uF stored across main/FB1/radio/SD
branches. These inventories do not qualify effective capacitance or
discharge behavior. Main-rail inventory, sensor topology/conditional
arithmetic and clock checks pass. The full 14-page PDF was regenerated;
page 6 was visually reviewed and the other 13 pages render identically
to SERVICE-019.

SERVICE_VIO source/contact and dual 10 kohm discharge bias, fixture
contacts, full-rail thresholds, leakage, sequencing, recovery behavior
and final power budgets remain open. Hold both processors in reset
during mode changes per SERVICE-003. This is an integration checkpoint,
not a manufacturing-ready or transient-qualified circuit.

## SERVICE-021: native SERVICE_VIO discharge bias, 2026-10-04

Historical checkpoint; SERVICE-025 supersedes these discharge values.

R110 and R111 are YAGEO RC0603FR-0710KL, 10 kohm, 1%, 100 ppm/C.
Both pin 1 terminals join SERVICE_VIO and both pin 2 terminals join GND,
giving 5 kohm nominal in parallel. Native fields identify the conditional
SERVICE-003/005 basis and retain the historical unreserved sourcing snapshot.
With the existing 1% tolerance and 1% temperature allocation, each resistor
is 9801..10201 ohm and the parallel pair is 4900.5..5100.5 ohm.
At the 3.465 V fixture ceiling, maximum pair loading is 0.7071 mA;
each resistor dissipates at most 1.225 mW. The allocated 60 uA adverse
injection gives 0.30603 V at the maximum pair resistance. This is the
existing conditional DC screen, not a verified leakage or threshold bound.
Installed capacitance, fixture behavior, disconnect waveforms, intermediate
rail states and safe mode-change sequencing still require qualification.

The saved export contains 296 components, adding only R110 and R111.
All 294 prior component records and every prior pin-to-net assignment
are unchanged. Both resistor terminals are verified in the saved netlist.
ERC remains 100 errors and 11 warnings with identical finding records;
no exclusion, power flag or masking was introduced.

Main-rail inventory, sensor topology/conditional arithmetic, clock arithmetic
and SERVICE-005's 32 steady states and conditional DC screens pass.
The full 14-page PDF was refreshed; page 6 was visually reviewed and
the other 13 pages render identically to SERVICE-020. Fixture contacts,
full-rail thresholds, leakage, sequencing, recovery behavior and final
power budgets remain open. This is an integration checkpoint.

## SERVICE-022: discharge versus translator isolation review, 2026-10-04

Rechecked [TI SCES942A](https://www.ti.com/lit/ds/symlink/txu0202.pdf),
sections 7.5 and 9.3.4, and
[TI SCES416N](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf), section 6.5.
The TXU0202 supply-isolation condition is below 100 mV (or a disconnected
supply), with the complementary supply in its recommended range. SERVICE_VIO
is resistively grounded after fixture removal, so do not assume the floating
supply condition applies. The 60 uA allocation and 5100.5 ohm maximum
parallel resistance yield 0.30603 V: the conditional selector-low screen
does not establish supply isolation. A positive constant-injection model
requires less than 19.6059 uA total injection to settle below 100 mV.
That number is a design requirement, not a proved installed leakage bound.

With zero injection, 100 nF nominal C116 and 5100.5 ohm, the ideal decay
from 3.465 V to 0.100 V takes 1.808 ms. This is only an illustrative RC
calculation; capacitor tolerance, fixture storage, pin capacitance and
voltage-dependent leakage are excluded. With constant 60 uA injection,
the ideal model never reaches 100 mV. Do not specify a disconnect wait
from nominal capacitance alone.

The four selector input-leakage rows specify test inputs at GND or 5.5 V;
TXU0202 power-down rows likewise have explicit supply and pin conditions.
Those rows do not automatically bound every intermediate SERVICE_VIO state.
U31 should command OE low after service mode exits, providing a separate
isolation mechanism, but full-range thresholds and transition behavior
remain unqualified. Keep both processors held in reset during mode changes.
Closing this requires a justified leakage model and OE threshold proof,
or a revised discharge/control circuit, followed by physical recovery tests.
No schematic change or ERC waiver follows from this review.

## SERVICE-023: native J4 service contacts, 2026-10-04

J4 now exposes all five SERVICE-002 nets in the saved native schematic:
1 GND; 2 SERVICE_VIO; 3 SERVICE_TX to U27.5; 4 SERVICE_RX from U27.4;
5 SERVICE_C6_RESET_N to U29.3 and R109.2. SERVICE_VIO remains the
fixture-supplied translator A rail and selector input, with C116 bypass and
R110/R111 discharge. It does not merge with either board 3.3 V power rail.
Reset remains an open-drain fixture request through the existing selector
and supervisor. TP3 remains separate GPIO9 boot access.

The local five-pin passive symbol uses 150 mil pins, 100 mil rows, 50 mil
text and 10 mil body stroke. Reference and value are centered above its body.
It has no purchased connector MPN or populated-header claim. Its footprint
is deliberately blank pending deferred pad/mechanical qualification. The
Datasheet field identifies this project-relative service contract.

The saved netlist contains 302 components, adding only J4. All 301 prior
component records and every prior pin partition are unchanged after excluding
J4. Each J4 pin was checked against SERVICE-002 and the existing destinations.
ERC findings and configured ignored checks are identical to the previous
checkpoint: 99 errors and 11 warnings. The fixture supply remains an external
source requiring qualification; no power flag, exclusion or no-connect marker
was added to suppress it or any other unfinished circuit.

The full 14-page PDF was regenerated and rendered. J4 on page 6 was visually
reviewed; the other 13 pages are pixel-identical to the prior export. Clock,
main-rail inventory and LIS2DTW12 conditional arithmetic checks pass with their
existing limitations. SERVICE-005/006/022 qualification gates remain open,
including full rail-range thresholds, leakage, handover timing, physical
recovery trials, ESD and protected mechanical access. This checkpoint completes
the logical five-contact wiring, not qualification of the service subsystem.

## SERVICE-024: alternative selector screen (2026-10-04)

Research only; the installed TI gates remain unchanged. [Nexperia
74LVC1G157 Rev.12](https://assets.nexperia.com/documents/data-sheet/74LVC1G157.pdf),
Tables 3/4/6/7, offers 2.0 V high and 0.8 V low input limits over
2.7..3.6 V, but cannot be substituted blindly. Its select polarity is
opposite the present mux configuration: low selects pin 3, high pin 1.
It also specifies at most 10 ns/V input transition time in that rail range.
The slowly discharging SERVICE_VIO selector has no such edge bound.
Reject direct replacement pending a separately qualified select driver,
rewiring, output-load review and mode-transition proof. Schmitt-action
marketing does not waive the specified transition limit.

[Nexperia 74LVC1G97 Rev.8.1](https://assets.nexperia.com/documents/data-sheet/74LVC1G97.pdf)
matches the installed mux pin function, but Table 12 likewise gives discrete
supply threshold tests. It does not close the continuous-rail threshold gap
merely by changing manufacturer. No new symbol or BOM selection follows.

## SERVICE-025: stronger native fixture-rail discharge (2026-10-05)

R110/R111 are now 1k YAGEO RC0603FR-071KL, rather than the historical
10k parts in SERVICE-021. Wiring and all pin partitions are unchanged.
The older 306.03 mV failure screen remains evidence for the correction;
its resistor values no longer describe the installed circuit.

Using 1% initial tolerance and 100 ppm/K over a 100 K excursion gives
980.1..1020.1 ohms each and 490.05..510.05 ohms for the pair. At the
existing **assumed**, unqualified 60 uA adverse injection, the steady-state
SERVICE_VIO ceiling is 30.603 mV. With one resistor open it is 61.206 mV.
These are conditional screens against the TXU0202's below-100 mV
supply-isolation condition, not proof of actual aggregate injection or
single-fault safety. The respective 100 mV boundary currents are
196.059 uA and 98.030 uA; equality does not meet a below-100 mV condition.
Full leakage, temperature, rail-ramp and selector thresholds remain HOLD.

At 3.3 V +/-5%, pair current is at most 3.465/490.05 = 7.070707 mA,
and each resistor dissipates at most 12.25 mW. The part is rated 0.1 W
at 70 C; apply its thermal derating at the actual board temperature.
The fixture contract now requires at least 20 mA available, leaving
12.929293 mA after the discharge pair for translator, bias and transients.
No adapter is selected. This reserve is a requirement, not a qualified
complete static or dynamic budget; characterize startup/current limiting.

For a constant 60 uA injection and only nominal C116=100 nF,
Vinf=30.603 mV and tau=510.05*100 nF=51.005 us. Starting at 3.465 V,
to 100 mV takes tau*ln((3.465-Vinf)/(0.1-Vinf)), about 199 us.
With an illustrative 120 nF effective total, the screen is about 239 us.
Neither is a guaranteed off delay: actual storage, leakage and waveform
are unqualified. Keep both processors reset during mode changes, with
ground making first and breaking last. Default OE remains low.

Exact [manufacturer specification](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-071KL)
confirms 1k, 1%, 100 ppm/C and 0.1 W at 70 C. The October 5
[DigiKey quantity-one cut-tape offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-071KL/726843)
listed Active, 3,225,465 in stock, USD 0.10 and 22-week standard lead time.
Stock is unreserved; recheck before ordering. This consolidates an existing
BOM MPN. Native BOM fidelity passes for all 305 included references.

Saved-netlist comparison confirms all pin partitions and component inventory
unchanged; only R110/R111 values and their metadata differ. Audit coverage
remains 81 rows / 305 references. The 15-page native PDF was rendered and
reviewed; page 6 alone differs, and the other 14 pages are pixel-identical.
ERC remains 103 errors / 15 warnings with the same findings and four existing
ignored check categories. Clock, main-rail inventory and sensor conditional
checks pass with their stated limitations. Native Save All also regenerated
the audio child-file UUID; its symbols, nets and rendered page are unchanged.
No new ERC exclusion or source flag was introduced.
