# Orientation sensor alternative review

## SENS-022: native LIS2DTW12TR replacement, 2026-10-04

U26 now uses the exact project-local `Sensors:LIS2DTW12TR` symbol. This
supersedes the LIS2DW12TR procurement selection and the candidate-only
status recorded below. The following dated reviews are preserved as history;
their DW-specific startup and power-cycle claims do not qualify DTW.

Authority is [ST DS12825 Rev4, Table1 and section4](https://www.st.com/resource/en/datasheet/dm00560052.pdf).
All twelve pin functions match the previous circuit. The native Symbol
Editor created the replacement in the Sensors library, with exact Value,
manufacturer ordering code, description and datasheet fields. KiCad migrated
U26 without resetting alternate pin selections or field positions. Its SA0
input selection, existing unused-pin markers and every wire are preserved.

The refreshed [DigiKey primary listing](https://www.digikey.com/en/products/detail/stmicroelectronics/LIS2DTW12TR/9997333),
retrieved 2026-10-04 and marked crawled today, reports 503 units in stock,
Active status, cut tape 497-19047-1-ND, USD2.10 at quantity one and a
24-week standard lead time. This supersedes the earlier cached 10,544-unit
snapshot. Stock is unreserved; check checkout availability before purchase.
U26's native sourcing fields now identify this part and dated snapshot.

The saved XML contains 285 components; only U26's component record changed.
Complete net partitions match the preceding radio-input-bias checkpoint.
The new symbol's complete pin types, alternates, coordinates, lengths and
graphics match the old symbol after normalizing its identifier. The candidate
Python topology and conditional interface screen pass on the saved DTW
netlist. ERC finding identities are unchanged: 100 errors and 11 warnings.
No ERC suppressions, new no-connect markers or power flags were introduced.

The sheet annotation cites the DTW datasheet and ST's 20ms example followed
by reset polling. That example is not a guaranteed maximum boot time; exact
startup/recovery qualification remains open. Full configured bus timing,
corner leakage, effective passive values, current budget and footprint
qualification also remain open. Existing passive Selection_Basis fields
retain their dated DW review history; they do not establish DTW acceptance.

## Historical procurement hold: U26, 2026-10-04

The owner raised a low-volume availability concern after the LIS2DW12TR
integration checkpoint. At this review checkpoint, procurement selection
was placed on hold pending an alternative review. SENS-022 above records
the subsequent replacement; older stock snapshots must not approve it.

The [DigiKey exact LIS2DW12TR listing](https://www.digikey.com/en/products/detail/stmicroelectronics/LIS2DW12TR/7348326),
retrieved 2026-10-04, reports only 2 units in stock, 24-week standard
manufacturer lead time, and USD1.79 at quantity one. It identifies
497-17718-1-ND as cut tape and lists quantity-one pricing; 10,000 is the
full tape-and-reel price break, not evidence of a cut-tape minimum order.
This public listing does not establish checkout availability or reserve
stock. Two remaining units are insufficient evidence of robust supply.

The [DigiKey AIS2DW12TR listing](https://www.digikey.com/en/products/detail/stmicroelectronics/AIS2DW12TR/10231571),
retrieved on the same date (page marked crawled yesterday), reports
4,234 units, cut tape 497-19477-1-ND, USD3.00 at quantity one and
24-week manufacturer lead time. This is a sourcing lead only. No electrical
equivalence, pin compatibility, tap capability, timing or firmware
compatibility is established by these distributor attributes. Review the
manufacturer datasheet and application requirements before selection.

The schematic has not been changed by this procurement review. Replacement
must preserve required orientation and motion sensing, shared-rail logic
compatibility, interrupt wake behavior and bounded recovery. Reconcile the
existing sensor-dependent shutdown calculations and firmware contract with
the chosen part before accepting its circuit. Native BOM sourcing fields
and the PDF will need updating with the eventual CAD checkpoint.

## AIS2DW12 alternative screen, 2026-10-04

Primary authority: [ST DocID031240 Rev4](https://www.st.com/resource/en/datasheet/ais2dw12.pdf),
Tables 2/4/5 and register map. Its twelve package contacts have the same
functions as the present U26 worksheet. Supply range is 1.62..3.6V;
VDDIO must not exceed VDD+0.1V. Shared supply and existing bypass topology
are plausible starting points. This is not circuit acceptance.

It provides 6D/4D orientation and motion functions, +/-2g or +/-4g ranges
and rates up to 100Hz. Registers 0x31..0x33 and 0x39 are reserved;
no hardware single/double-tap function is documented. Do not reuse a
LIS2DW12 tap configuration. The long-term zero-g offset bounds are
plus/minus700mg; sensitivity at +/-2g outside Mode1 spans
0.207..0.281mg/digit. Calibration and rotation thresholds need evaluation.

PARTS-CHECKLIST.md includes hardware tap in the candidate inventory, while
design/sensors.md explicitly requires auto-rotation. Preserve tap capability
while reviewing further candidates rather than silently dropping it.
AIS2DW12 is not selected for U26 by this review. Manufacturer-specific
startup/recovery behavior and configured bus timing remain unchecked.

## LIS2DTW12 preferred replacement candidate, 2026-10-04

[ST's product page](https://www.st.com/en/mems-and-sensors/lis2dtw12.html)
documents portrait/landscape, motion wake and single/double-tap recognition.
This preserves the intended feature set better than the AIS candidate.

[DS12825 Rev4](https://www.st.com/resource/en/datasheet/lis2dtw12.pdf),
Table1, lists the same twelve pin functions as the current U26 worksheet.
Its supply range is 1.62..3.6V; VDDIO maximum is VDD+0.1V. Electrical
output levels are VDDIO-0.2V high and 0.2V low at 4mA. Table conditions
are 1.8V/25C unless otherwise stated; full-corner behavior remains open.

Python screening with the present rail envelope gives IRQ high margin
3.151819680-0.2-0.8*3.393012496 = 0.237409683V and low margin
0.2*3.151819680-0.2 = 0.430363936V. These are conditional DC calculations,
not measured compatibility. Existing sensor arithmetic passes but remains
LIS2DW12-specific; it does not qualify this replacement's startup or timing.

[DigiKey listing](https://www.digikey.com/en/products/detail/stmicroelectronics/LIS2DTW12TR/9997333)
identifies cut tape 497-19047-1-ND and USD2.10 at quantity one. Retrieved
2026-10-04, its cached page reports 10,544 units and 24-week lead time;
the search snapshot reports 4,200. Neither is a live checkout confirmation.
Use a fresh availability check before procurement selection.

Preferred candidate only: verify startup/off-time, bypass, I2C timing and
address, interrupt modes, current budget and register differences before
native replacement. Create an exact project-local symbol and verify every
pin; retaining wires alone cannot establish acceptance. Full PDF/ERC and
BOM refresh belong with the CAD change. Footprint qualification is deferred.

### Interface and startup evidence, 2026-10-04

Run `python scripts/check_lis2dtw12_candidate.py` for the candidate's
conditional logic and bus screen. It uses the existing rail, 25..60pF,
15uA leakage and resistor-drift allocations; none is a measured guarantee.

The accessible [ST DS12825 Rev4 document](https://www.st.com/resource/en/datasheet/dm00560052.pdf)
Table7 specifies fast-mode low/high minima 1.3/0.6us, setup100ns,
hold10..900ns and bus-free1.3us. Section4 requests local 100nF ceramic
and 10uF aluminum near VDD9. These support retaining the proposed topology.

[ST's polling example](https://raw.githubusercontent.com/STMicroelectronics/STMems_Standard_C_drivers/master/lis2dtw12_STdC/examples/lis2dtw12_read_data_polling.c)
waits20ms before reading identity, then resets and polls completion.
This example is not a worst-case startup specification. Production firmware
must bound polling, handle transaction failures and avoid an infinite loop.
The [ST driver header](https://raw.githubusercontent.com/STMicroelectronics/lis2dtw12-pid/master/lis2dtw12_reg.h)
defines high-address read byte0x33 (seven-bit0x19) and identity0x44.
Identity alone does not distinguish this device from LIS2DW12.

No replacement-specific power-off duration was established by this review.
The old LIS2DW12 <100mV/10ms condition must not be claimed as a verified
LIS2DTW12 requirement. Retain conservative hardware discharge while obtaining
exact recovery evidence. Native replacement and its PDF remain pending.

### Saved connection audit, 2026-10-04

The fresh native XML export still identifies U26 as LIS2DW12TR. Run
`python scripts/check_lis2dtw12_candidate.py --netlist <export.xml>` to
check the topology that the proposed replacement must preserve. It checks
pins 2/3/9/10 on +3V3_MCU, pins 6/7/8 grounded, clock/data/INT1 at host
K13/R16/D11, and the existing bypass and pullup values and endpoints.
Pins 5 and 11 must remain separate unused nets; native no-connect markers
and pin electrical types require separate schematic/ERC review.

This audit passed the current saved export. Deliberately removing the
reserved-pin ground connection and changing a pullup value each caused a
failure. It verifies the existing connection contract, not a new sensor
installation, full pin-map acceptance or startup/recovery qualification.

## SENS-010: system power cost and LIS2DW12, 2026-09-27

Status: **native replacement in progress**, not a qualified circuit. SENS-013
below records the current saved U26 LIS2DW12TR implementation. SENS-001..009
describe the previous ADXL367 branch and are historical design analysis;
their pin numbers and VREG network do not apply to the replacement.

The owner requires orientation/state sensing, not an ADXL ordering code.
PARTS-CHECKLIST.md describes a candidate inventory. SENS-007's passive
4.7kohm branch consumes up to 0.775342mA before switch, translator and sensor
loads. That cost undermines the purpose of choosing a nanopower sensor.
Evaluate the complete circuit's energy, not just the MEMS typical current.

ST LIS2DW12TR is a useful alternative because it preserves orientation,
motion wake and single/double tap. Its FIFO holds 32 levels; it does not
preserve the ADXL367's 512-sample FIFO capability, which is not an owner
requirement. ST reports the part active and in volume production on its
[product page](https://www.st.com/en/mems-and-sensors/lis2dw12.html).

The proposed connection shares +3V3_MCU for VDD, VDDIO and host pullups.
This avoids a separately ramped sensor voltage and its signal translation.
It permits motion wake only while that rail remains powered; it does not
add motion-triggered cold power-on. Preserve the existing physical power
button and firmware-independent shutdown/recovery contract.

## Manufacturer requirements to carry into implementation

[DS11811 Rev.9](https://www.st.com/resource/en/datasheet/lis2dw12.pdf),
Tables 1/4 and section 4: supply range 1.62..3.6V; tie CS high for I2C.
VDDIO must respect VDD+0.1V. Use the recommended local supply bypass,
including 100nF ceramic and 10uF aluminum at VDD. Output limits are
VDDIO-0.2V high and 0.2V low at the stated 4mA drive condition. Table 4
is conditioned at 1.8V/25C unless otherwise noted: do not silently promote
every tabulated number into a full-temperature guarantee.

Native symbol pin-map worksheet (entered and checked in SENS-012 below):

| Pin | Name | Base electrical type |
| --- | --- | --- |
| 1 | SCL/SPC | Input |
| 2 | CS | Input |
| 3 | SDO/SA0 | Bidirectional |
| 4 | SDA/SDI/SDO | Bidirectional |
| 5 | NC | Not connected |
| 6 | GND | Power input |
| 7 | RES | Passive, must ground |
| 8 | GND | Power input |
| 9 | VDD | Power input |
| 10 | VDDIO | Power input |
| 11 | INT2 | Bidirectional (alternate external trigger) |
| 12 | INT1 | Output |

[AN5038 Rev.6](https://www.st.com/resource/en/application_note/an5038-lis2dw12-alwayson-3d-accelerometer-stmicroelectronics.pdf),
sections 1/3/5.9: SA0's internal pullup cannot be disabled; use a high strap
for low-power operation. Keep host signals floating or low until VDDIO is
present. Boot takes at most 20ms; proper power-off requires VDD below
100mV for at least 10ms. Reset and boot must run serially, not together.
Polling reset completion and then waiting the boot interval belongs in the
firmware contract. Neither operation substitutes for hardware power cycling
when the bus is stuck.

## Integration calculations and unresolved shutdown condition

Run `python scripts/check_sensor_alternative.py`.

Using the existing conditional 3.15182..3.39301V host-rail envelope,
the independent-corner IRQ screen has 0.237412V high and 0.430364V low
margin. This supports reviewing a direct interrupt connection; it does
not qualify unallocated GPIO routing, transients or temperature behavior.

The existing SYS-007 reservoir screen holds control above 2.7V for
46.589403ms. With its 1mF main-rail capacitance ceiling and 11.4211ohm
discharge path, reaching 90mV plus 10ms source-stop allowance and 10ms
below-threshold hold requires 62.131061ms even without positive injection.
Therefore **the existing SYS-007 allocation is insufficient for this
candidate**. The 200ms rearm lockout does not extend reservoir hold-up.

The initial six-capacitor screen incorrectly reserved only 100uA for two
additional 100uF parts. The installed T491D107K010AT bank uses 125uA per
part after the temperature/endurance leakage screen; two more require
250uA. The corrected hold is **62.141848ms**. With an unproven 1mA
other-backfeed ceiling alone, discharge equilibrium is 11.4211mV and the
required time is 63.644687ms. Thus six parts also fail this screen.
The former 66.706626ms and positive 3.061939ms margin are withdrawn.
PWR-006 also retains 1.5mA for key-filter charge return. Preserve that
separately: the combined 2.5mA screen has a 28.552750mV equilibrium and
requires 66.398757ms. The new 1mA allowance must not replace that existing
key-return allocation.

### Revised reservoir draft implemented, 2026-09-27

Four **T491D227K010AT, 220uF/10V, +/-10%** parts now replace C63-C66
in the native power-button sheet. This is a conditional electrical draft,
not acceptance of the shutdown or sensor subsystem.
The [exact KEMET specification](https://search.kemet.com/download/specsheet/T491D227K010AT)
gives 22uA leakage after five minutes at 25C. The
[T491 family specification, 2026-07-08, pages 2-3](https://content.kemet.com/datasheets/KEM_T2005_T491.pdf)
provides the temperature and endurance factors. Retain the existing
conservative stacked model through 85C; this is not a 125C or unlimited-life
claim. Capacitor leakage before five minutes remains a startup qualification
dependency and is not bounded by the steady-state part specification.

```text
Cmin = 4*220u*0.9^3 = 641.520uF
Cmax_model = 4*220u*1.1^3 = 1171.280uF
Bank leakage screen = 4*22uA*10*1.25 = 1.100mA
Other existing control allocation = 1.125mA - 0.500mA = 0.625mA
New control allocation = 0.625 + 1.100 + 0.100 reserve = 1.825mA
Vinitial = 3.263705831 - max(0.250, 1.825mA*102.24) = 3.013705831V
Hold = [Cmin*(Vinitial-2.7) - 1uC] / (1.825mA+0.817mA)
     = 75.794309ms; margin over 66.398757ms = 9.395552ms
Recharge steady model = 3.70 - 0.250 - 102.24*1.825mA = 3.263412V
Recharge from zero to 3.25V = 102.24*Cmax*ln(Vsteady/(Vsteady-3.25))
                          = 0.657961s
```

The recharge screen fits the existing one-second settling allocation but
has only 13.412mV static headroom at the 3.70V recovery boundary. It does
not prove startup leakage, switch behavior, incomplete recharge during
rapid cycling, or successful operation below that recovery contract.
The full source-qualification interval remains additional to settling.
The native capacitor sourcing fields and nearby held-supply note were
updated through KiCad. Review the remaining dependent SYS-007/PWR-006
notes, control-current budgets and recovery assumptions before signoff.
The combined 2.5mA
return/injection bound, 1mF ceiling, FET resistance and charge-loss allocations
remain qualification conditions; a larger reservoir does not prove them.

Sourcing snapshot retrieved 2026-09-27: the
[DigiKey T491D227K010AT listing](https://www.digikey.com/en/products/detail/kemet/T491D227K010AT/2336333)
identifies cut tape **399-8379-1-ND**, Active, 3,958 in stock, USD2.24/1.521/
1.14770 at quantities 1/10/100, and 20-week standard lead time. Stock is
unreserved and must be rechecked before purchase. Native BOM fields now
identify these exact parts. Footprint qualification remains deferred.

Verification of the saved native revision: exported XML confirms all net
memberships unchanged, the same component inventory, and only C63-C66's
component records changed against the preceding sensor-capacitor checkpoint.
All four values are 220u with the exact MPN and supplier code above.
ERC finding identities are unchanged: 119 errors and 55 warnings. This
is not a passing whole-design ERC gate. The calculation script passes its
conditional screens. Dependent native notes and the selection-basis fields
for U10, R31, R39/R40 and C63-C66 were subsequently reconciled through KiCad.
R31's resistor-only drop at 1.825mA is 0.18616825V. The saved export
`C:\work\sensor-hold220-notes.xml` preserves every net membership and the
277-component inventory against `sensor-hold220.xml`; exactly those eight
component records changed. Full PDF/BOM export and all-page visual review
remain outstanding before a phase commit.

## Sourcing and next implementation step

[DigiKey exact part](https://www.digikey.com/en/products/detail/stmicroelectronics/LIS2DW12TR/7348326)
identifies 497-17718-1-ND cut tape; the retrieved listing showed active,
6,070 stocked, USD1.79 at one and USD1.29590 at 100, 24-week standard lead
time. This is a dated, unreserved indication, not a purchase approval.
Mouser's exact-part page could not be retrieved through its region redirect;
do not mistake nearby LIS2DS12TR or LIS2DWTR EOL listings for this device.

Before replacing U26: resolve the shared-rail shutdown budget, verify IIC0
timing/pullups and an interrupt GPIO, create and check the local symbol
through native KiCad, then rewire the sensor page. Preserve all required
features and re-export connectivity/ERC/BOM. A pin-compatible replacement
is not assumed. The older ADXL analysis remains available for comparison.

## SENS-011: shared-rail bus and interrupt reservation

Reserve **P306/D11, IRQ28-DS** for sensor INT1, with latched active-high
interrupt operation and a rising-edge wake configuration. The 289-ball
column in [Renesas Rev.1.30 Table 1.17](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet)
identifies this deep-standby-capable input. The saved netlist confirms D11,
IIC0 SCL P410/K13 and SDA P409/R16 are all presently unconnected. This is a
pin reservation; native hierarchy wiring and firmware wake configuration
remain to be implemented. Keep this IRQ distinct from the button IRQs.

Candidate bus: one 4.7kohm pullup per line to the common +3V3_MCU supply,
with sensor VDD/VDDIO on that same rail. No isolation switch or parallel
pullup on a second domain is proposed. SA0 high selects address **0x19**;
CS also straps high. Do not confuse that address with WHO_AM_I=0x44.

The calculation script screens 1% initial tolerance, 100ppm/K over 100K
and an additional 5% service-drift allocation. It assumes 25..60pF total
capacitance per line and 15uA total adverse leakage per line. These are
design acceptance allocations, not a sourced leakage inventory or a
measurement of the future PCB. The current exact 4.7kohm resistor candidate
is YAGEO RC0603FR-074K7L from SENS-007; sourcing fields remain to be entered
for the eventual pullups.

Computed bounds: 4376.1465..5034.1935ohm, 92.697489..255.927683ns
30%-70% rise, 0.790342mA maximum sink allocation and 3.076307V high
floor. Both lines continuously low draw up to 1.550684mA through their
pullups alone; include duty cycle and fault behavior in the energy budget.
The rise figures here used zero leakage and are superseded by SENS-020;
the DC bounds are retained.
The script passes these conditional DC/rise checks and the revised
reservoir checks. These checks do not inspect native connectivity.

Renesas Table 2.66 fast-mode rise limits are 20..300ns with FMPE=0;
the dedicated _A pins do not require the _B pin drive-strength setting.
ST DS11811 Table 7 permits 400kHz, with low/high minima of 1.3/0.6us,
100ns data setup, 10ns..0.9us data hold and 1.3us bus-free time.
Peripheral divider/filter settings, falling-edge timing and clock tolerance
must still be checked against both devices before firmware acceptance.
Do not carry the ADXL-specific 120ns rise limit into this LIS interface.

The RC check covers only rising edges and DC levels. It does not prove
fall time, configured timing, startup, hot leakage or bus recovery. Host
internal pulls must not introduce another supply domain. Keep the bus
undriven before the shared supply is valid, wait the boot interval, and
clear latched interrupt sources before arming/rearming wake. A stuck bus
must have a bounded recovery path through full main-rail power cycling.
Motion wake remains limited to modes that retain +3V3_MCU; cold start uses
the physical power button. Symbol creation is recorded in SENS-012 and
the in-progress native circuit replacement in SENS-013.

## SENS-012: native LIS2DW12 symbol, 2026-09-27

Created `Sensors:LIS2DW12TR` through the native KiCad Symbol Editor using
the existing twelve-pin symbol's drawing style as a starting point. Every
package number was remapped to DS11811 Rev.9 Table 1; INT1 is Output,
INT2 retains Bidirectional for its alternate trigger-input function, RES
is Passive and must be grounded, and NC is Unconnected. Ground names
`GND_1` and `GND_2` distinguish pads 6 and 8 without merging them.

The native pin table reports twelve pins and no duplicate numbers. A
read-only check of the saved library independently compares every pin
number, name and electrical type to the worksheet above (allowing the
two ground suffixes and the active-low CS overbar). All twelve match.
Native rendering was inspected: reference/value above the body, readable
pin names and numbers, 150mil pins and 100mil row spacing retained.

Value and manufacturer fields now identify STMicroelectronics LIS2DW12TR.
The Datasheet field points to ST's PDF. Inherited ADXL description,
supplier references, height and footprint assignment were replaced or
cleared; a read-only search of the new symbol finds no ADXL367 text.
The footprint remains blank under the deferred physical qualification
scope. Distributor and qualification fields will be completed during
placement. The older ADXL symbol and U26 circuit remain available;
this library addition has not changed schematic connectivity.

Next: replace the unfinished U26 branch through native KiCad, retaining
the page's readable layout. Connect the shared supply, required bypass,
CS/SA0 high straps, RES/ground treatment, IIC0 hierarchy and INT1 wake
path; remove the obsolete ADXL-only VREG and bleeder circuit. Verify
actual exported pin memberships, component inventory, ERC differences
and the updated BOM before treating the sensor integration as complete.

## SENS-013: native U26 migration checkpoint, 2026-09-27

Replaced U26 through KiCad's Change Symbols dialog with
`Sensors:LIS2DW12TR`, preserving its reference and position. Updated the
value, manufacturer, datasheet and description from the new library symbol;
cleared the inherited ADXL footprint and supplier metadata. Procurement
fields for the replacement remain to be populated.

Removed the inherited SCL-to-ground wire and its ground marker, removed
the SA0 low strap, and disconnected the obsolete C115/C116 VREG branch
from RES. RES now has a direct ground wire. The saved netlist independently
confirms U26 pads 6/7/8 on GND and pads 9/10 on the shared, still undriven
supply. INT2 pad 11 and NC pad 5 retain their no-connect treatment. Pads
1/2/3/4/12 are explicitly unfinished; no markers hide those connections.

The native sheet note now identifies the LIS part and the remaining work.
C115/C116 and their isolated wiring still need removal. R102 is still a
bleeder and must be repurposed or removed. Complete the supply/bulk bypass,
CS/SA0 high straps, pullups and hierarchical SCL/SDA/INT1 host connections.
Then finish sourcing, timing and power qualification, and inspect the PDF
and BOM before considering this subsystem complete.

Read-only validation compared `C:/work/sensor-lis-migration.xml` with
`C:/work/sensor-hold220-notes.xml`: all net memberships excluding U26 are
unchanged and all 277 components remain. The new ERC checkpoint is
122 errors / 55 warnings (177 total), versus the preceding 119 / 55.
The sensor page still reports unfinished power and signal connections;
this increase is not an accepted final ERC result. `git diff --check`
passes, with Git's existing CRLF-normalization warnings only. No commit
or push was made at this partial migration checkpoint.

## SENS-014: supply, pullups and sheet interfaces, 2026-09-27

Continued the native KiCad migration. Removed C115/C116 and their obsolete
isolated VREG wiring. Repurposed R102 as the 4.7k SCL pullup and added R103
as the separate 4.7k SDA pullup. Connected VDD/VDDIO, CS, SA0 and both
pullup tops to +3V3_MCU. C117/C118 retain their visible common supply and
ground wires. Added hierarchical SENS_SCL (Input), SENS_SDA
(Bidirectional) and SENS_INT1 (Output), with INT1 wired to pad 12.
Updated the native WIP note to describe the remaining work.

Saved netlist `C:/work/sensor-lis-interfaces.xml` confirms U26 pads
2/3/9/10 on +3V3_MCU, pads 6/7/8 on GND, pad 1 with R102 bottom on
SENS_SCL, pad 4 with R103 bottom on SENS_SDA, and pad 12 on SENS_INT1.
INT2 and NC retain their explicit no-connect treatment. The crossed
signal/supply wires are separate nets. Comparing net memberships while
excluding the seven changed sensor references confirms connectivity
outside this branch is unchanged. Inventory is 276 components: C115 and
C116 removed, R103 added, all other references retained.

ERC is 117 errors / 57 warnings (174 total). The sensor page reports
three missing parent sheet pins and one bidirectional-to-power-output
conflict from the multifunction SA0/SDO supply strap; review the native
symbol's I2C-mode electrical modeling rather than suppressing that rule.
Parent hierarchy and MCU connections remain unfinished. Complete those
connections, the manufacturer-recommended bulk bypass, exact passive and
procurement metadata, and remaining timing/power qualification. This is
an intermediate electrical checkpoint, not subsystem acceptance. No
commit or push was made, and the complete release PDF/BOM review remains
pending.

## SENS-015: sensor host hierarchy connected, 2026-09-27

Completed the native root and MCU sheet interfaces for the sensor. SENS_SCL
reaches U1 K13/P410, SENS_SDA reaches U1 R16/P409, and SENS_INT1 reaches
U1 D11/P306. Imported the matching parent pins and added labeled wire stubs
in the existing open space without relocating the surrounding circuits.
The MCU pins still use their base GPIO symbol names/types; peripheral-mode
electrical modeling remains to be reviewed.

Saved netlist `C:/work/sensor-host-final.xml` verifies exact memberships:
SCL = U26.1, R102.2, U1.K13; SDA = U26.4, R103.2, U1.R16;
INT1 = U26.12, U1.D11. Comparing with SENS-014 while excluding only those
three newly connected MCU pads confirms all other connectivity is unchanged.
The inventory remains 276 components. Final label placement at wire ends
removes three new dangling-stub warnings without changing connectivity.

ERC is 111 errors / 56 warnings (167 total). The three missing sensor parent
pins and three unconnected MCU pins are resolved. The sensor SA0/SDO
bidirectional-to-power-output warning remains for mode-specific symbol
review. Bulk bypass, sourcing/passive metadata, timing and power qualification,
and the full PDF/BOM review remain open. No commit or push at this checkpoint.

## SENS-016: aluminum bulk bypass, 2026-09-27

Added a new Device:C_Polarized through KiCad, which assigned the now-free
C115 reference. This is a new 10uF VDD bypass, not the removed ADXL VREG
capacitor. Positive pad 1 connects to +3V3_MCU; negative pad 2 connects to
the visible C117/C118 common ground return. The native note identifies
placement near U26 VDD pad 9 and records the completed host wiring.

ST DS11811 Rev 9 section 4 specifies a 100nF ceramic and 10uF aluminum near
VDD. The selected electrical draft part is Panasonic EEE-FN1C100R (catalog
spelling EEEFN1C100R), 16V. Its MPN, description and manufacturer datasheet
are in C115; dedicated manufacturer/distributor fields remain to complete.
Footprint qualification is deferred. Source:
https://industrial.panasonic.com/cdbs/www-data/pdf/RDE0000/RDE0000C1259.pdf
(FN catalog, 01-Sep-25). Ratings include +/-20% at 120Hz/20C, -55..105C,
2000h endurance at 105C, 1.35ohm ESR at 100kHz/20C, and 90mArms at
100kHz/105C. The 4mm diameter part has 5.8mm nominal / 6.1mm maximum
height; mechanical fit remains open. The device must remain dry inside
the sealed enclosure; it is not itself a water-resistant component.

The Python screen now accounts for this part within the existing 1mF
main-rail capacitance limit. Initial, soldering and endurance factors give
a conditional 20C allocation of 5.04..17.16uF, leaving 982.84uF for all
other main-rail capacitance. These factors do not establish combined
temperature/service limits or guarantee 10uF effective capacitance.
Catalog leakage is 3uA at 20C after two minutes at rated voltage; startup
and temperature leakage remain unqualified. Do not add this capacitor
outside the 1mF recovery budget or treat nominal bypass guidance as a
proven transient-response bound.

Distributor snapshot (unreserved, 2026-09-27): DigiKey
10-EEE-FN1C100RCT-ND, active, 9,706 listed, $0.42 each / $0.16610 at 100,
31-week manufacturer lead time:
https://www.digikey.com/en/products/detail/panasonic-industry/EEE-FN1C100R/11656952

Saved netlist C:/work/sensor-bulk.xml confirms capacitor polarity and
unchanged connectivity after excluding only new C115. Inventory is 277.
ERC remains 111 errors / 56 warnings. Passive service qualification,
mode-specific pin types, IIC timing and remaining sourcing fields are open;
this is not subsystem acceptance. No commit/push or full PDF/BOM review yet.

## SENS-017: native sourcing metadata, 2026-09-27

Completed the canonical manufacturer, ordering-code, distributor, procurement
status, selection-basis and dated sourcing fields for R102/R103, C115 and U26
through KiCad's native Symbol Fields Table. C115 now has
Manufacturer_Part_Number in addition to its original MPN field. Updated the
C117/C118 selection basis to identify LIS2DW12 VDD/VDDIO bypass and removed
the obsolete ADXL regulator-stability wording. Their existing Murata sourcing
records are retained; effective capacitance remains unqualified.

R102/R103 are YAGEO RC0603FR-074K7L, DigiKey 311-4.70KHRCT-ND.
The manufacturer specification confirms 4.7k, 1%, +/-100ppm/C, 0.1W at
70C and 0603 size. These match the tolerance and TCR inputs in
check_sensor_alternative.py. The 5% service-drift allowance and 25..60pF
bus-capacitance envelope remain design allocations, not qualified limits.
Sources:
https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-074K7L
and https://www.digikey.com/en/products/detail/yageo/RC0603FR-074K7L/727212 .
The retrieved manufacturer sheet is generated 2026-09-28 UTC. The local
2026-09-27 America/Chicago sourcing snapshot lists Active, 4,483,261 stock,
USD 0.10 at one / 0.01220 at 100, and 22-week lead time, unreserved.

C115's refreshed DigiKey listing supersedes the earlier SENS-016 snapshot:
Active, 9,260 stock, cut-tape USD 0.50 at one / 0.20240 at 100, 37-week
lead time, unreserved. Its native fields retain the conditional capacitance
allocation within the total 1mF main-rail budget and the unresolved
startup/temperature leakage, service-life and enclosure-fit qualifications.
Source: https://www.digikey.com/en/products/detail/panasonic-industry/EEE-FN1C100R/11656952 .

U26's primary DigiKey page timed out on this refresh. The indexed DigiKey
mirror, reported as a six-day-old crawl, listed Active, 1,091 stock, USD
1.90 at one / 1.37370 at 100 and 24-week lead time. Its native snapshot
explicitly says this is indicative, unreserved and not live-verified.
Recheck the primary listing before procurement. Indexed source:
https://sc-b.digikeyassets.com/en/products/detail/stmicroelectronics/LIS2DW12TR/7348326 .

Saved netlist C:/work/sensor-metadata-final.xml confirms all six sensor
components have the seven canonical sourcing fields populated. The complete
277-component inventory and every net membership are unchanged from
C:/work/sensor-bulk.xml. ERC C:/work/sensor-metadata-erc.json remains
111 errors / 56 warnings. No circuit geometry or wiring was edited.
I2C-mode pin modeling, complete bus timing, passive/power-cycle service
qualification and the full PDF/BOM release review remain open. No commit
or push was made at this checkpoint.

## SENS-018: native I2C address pin mode, 2026-09-27

Added SA0 (Input) and SDO (Output) alternate functions to pin 3 of the
project-local LIS2DW12TR symbol through the native Symbol Editor. The base
SDO/SA0 bidirectional definition and all twelve base pin objects remain
unchanged. Updated U26 from the library without resetting fields, geometry,
or alternate selections, then selected SA0 in the schematic. Authority:
ST DS11811 Rev 9 Tables 1 and 12, at
https://www.st.com/resource/en/datasheet/lis2dw12.pdf .

Saved netlist C:/work/sensor-mode-final.xml has 277 components and identical
net memberships to SENS-017. Pin 3 remains on +3V3_MCU; KiCad exports its
selected function as SA0_3 and electrical type input. All six sensor parts'
sourcing fields survived the library update. Corrected C115/C117/C118
Selection_Basis citations and this document from section 5 to section 4,
Figure 6, page 19 for the decoupling recommendation. Values are unchanged.

ERC C:/work/sensor-sa0-erc.json reports 111 errors / 55 warnings. The only
removed finding is the bidirectional-to-power-output warning on the address
strap; no new finding was introduced. Rules and exclusions were not changed.
Remaining MCU peripheral pin selections, complete IIC timing, passive service
qualification, total main-rail capacitance and power-cycle/backfeed checks
remain open. This checkpoint is not subsystem acceptance or a release;
full PDF/BOM review and commit/push remain outstanding.

## SENS-019: MCU peripheral alternatives, 2026-09-27

Added and selected three native alternatives in the project-local BGA289
processor symbol: P306/D11 IRQ28-DS (Input), P410/K13 SCL0_A
(Bidirectional), and P409/R16 SDA0_A (Bidirectional). The library diff
contains exactly those three alternate-definition additions; base GPIO
names, numbers, electrical types, geometry and existing alternatives remain
unchanged. Native Update Symbols from Library was restricted to U1 with
field resets and alternate-function resets disabled. Both IIC pins retain
bidirectional modeling for their bus input/output roles; this does not model
open-drain transistor characteristics or prove the firmware configuration.

Authority: Renesas RA8P1 Datasheet R01DS0439EJ0130 Rev.1.30, Feb 27 2026,
Table 1.17 BGA289 column, and IIC timing Tables 2.66 onward:
https://www.renesas.com/en/document/dst/ra8p1-group-datasheet .
The alternatives fit within the existing symbol bodies without overlapping
opposing names. No schematic wires or label positions were changed.

Saved export C:/work/sensor-host-modes.xml verifies the three chosen
functions, unchanged net memberships across the complete project, all 277
components, and unchanged component fields. The interrupt net is U26.12
to U1.D11; clock is U26.1/U1.K13/R102.2; data is
U26.4/U1.R16/R103.2. ERC C:/work/sensor-host-modes-erc.json has the same
111 errors / 55 warnings and the same finding categories/descriptions as
SENS-018. git diff --check passes (line-ending notices only).

Complete IIC clock/filter timing, passive service and power-cycle/backfeed
qualification remain open. Selecting an alternate in KiCad is not firmware
pin-mux programming. No full PDF/BOM release review or commit/push at this
checkpoint.

## SENS-020: leakage-aware rise and receiver timing, 2026-09-27

The earlier rise calculation used ln(7/3)*R*C, although the DC screen
included 15uA adverse leakage. That expression assumes the final voltage
equals the pullup rail. With constant signed leakage I (positive sinking),
Vinf = Vrail - I*R and the 30%-70% crossing interval is
R*C*ln((Vinf - 0.3*Vrail)/(Vinf - 0.7*Vrail)). This is a lumped model;
the +/-15uA bound must hold throughout the transition, not just at DC.
The common supply is assumed equal at the two devices, without rail drop
or ground shift. Those physical bounds remain to be qualified.

Updated check_sensor_alternative.py uses -15uA injection for the fastest
corner and +15uA sinking for the slowest, at the minimum rail. With the
existing resistor envelope and 25..60pF allocation, the revised rise range
is 88.561996..270.548613ns. It remains inside the RA8 fast-mode 20..300ns
window, but the calculated capacitance ceiling is only 66.531481pF.
This is not permission to add another bus device without a new inventory.
No resistor or capacitor value was changed.

Receiver requirements for the current fast-mode candidate (FMPE=0):

| Quantity | Required envelope / condition |
| --- | --- |
| Actual SCL frequency | <=400kHz at the fastest clock corner |
| SCL low / high at pin thresholds | >=1.3us / >=0.6us |
| START hold / repeated START setup / STOP setup | >=0.6us each |
| STOP-to-START bus-free time | >=1.3us |
| Data setup into LIS2DW12 | >=100ns |
| Data hold at LIS2DW12 interface | 10..900ns per ST Table 7 |
| Rise at both receiving pins | 20..300ns; conditional model above |
| Fall at both receiving pins | >=20ns*(Vpullup/5.5V), <=300ns; 12.338218ns lower bound covers the whole allocated rail range |
| Host data setup requirement | tIICcyc + 50ns; check sensor-driven data separately |
| Host filter / reference clock | Use actual Table 2.66 coefficients for configured NF/NFE |

ST authority: DS11811 Rev9 Table 7 and Figure 4, page 10,
https://www.st.com/resource/en/datasheet/lis2dw12.pdf . Its timing table
is based on protocol requirements and is not production tested. Renesas
authority: R01DS0439EJ0130 Rev1.30 Table 2.66, page 180,
https://www.renesas.com/en/document/dst/ra8p1-group-datasheet .
Renesas specifies input timing; it does not establish generated output
pulse widths from an unspecified divider setting.

A 400kHz period is 2.5us. Minimum low/high times plus the modeled slowest
rise and the allowed 300ns fall consume 2.470548613us, leaving only
29.451387ns for additional pulse width, quantization and clock margin in
that corner. A simple 50%-duty 400kHz waveform cannot meet the 1.3us low
minimum even before accounting for edges. Clock frequency alone therefore
cannot qualify this bus. Do not infer register settings from a nominal
400kHz request to a driver.

For the longest-filter coefficients (NF=11, NFE=1), the host high-time
minimum is 6*tIICcyc+300ns. Keeping it <=600ns and host data setup
tIICcyc+50ns <=100ns requires tIICcyc<=50ns, or IICphi>=20MHz.
This is a derived constraint if using the sensor's minimum timing values,
not a selected or verified RA8 clock configuration. Longer pulses/setup
can permit other reference clocks. IIC bus wakeup is assumed disabled;
orientation wake uses the separate IRQ28-DS line. Check the extra PCLKB
terms if bus wakeup is enabled.

The repository has no established PCLKB/IICphi divider/filter plan to
validate here. The RA8P1 hardware-manual web fetch timed out; no register
formula was borrowed from another MCU. Remaining work is to establish the
clock range including clock changes, calculate ICBRL/ICBRH/CKS and SDA delay
against the exact manual, validate both data directions and ACK timing,
and bound actual falling edges. These calculations leave the circuit
conditional; they do not establish complete 400kHz operation.

## SENS-021: whole-main-rail inventory link, 2026-09-27

[PWR-CAP-001](main_rail_capacitance.md) now inventories the saved native
capacitors against the assumed 1mF shutdown ceiling. Direct main storage
is 512.21uF nominal; C43 through FB1 adds 10uF. The new read-only netlist
script separates switched rails, regulator outputs, button filters and
held/source reservoirs. It identifies Pcam module capacitance as missing
from the native sum. This is an inventory step, not proof of the effective
upper bound or the 2.5mA injection allocation used by the shutdown model.
