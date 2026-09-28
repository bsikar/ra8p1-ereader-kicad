# E-Reader Sensor and Peripheral Specifications

This document outlines the required sensors, power management, and auxiliary peripherals for the `ereader_rev1` hardware design.

The native orientation circuit now uses LIS2DW12TR U26 on +3V3_MCU,
IIC0_A (P410/K13 clock, P409/R16 data), and P306/D11 IRQ28-DS.
See [sensor_alternative.md](sensor_alternative.md), SENS-011 through SENS-020,
for the current circuit, sourcing, native verification and remaining limits.
The SENS-001 through SENS-009 entries below are historical ADXL367 work;
their pin numbers, components, supply requirements and addresses do not
describe the replacement circuit. ALS, Hall, display temperature and the
other peripherals listed at the end remain requirements to implement.

## SENS-001: ADXL367 symbol qualification, 2026-09-27

The project-local `Sensors:ADXL367BCCZ-RL7` was corrected in the native
KiCad Symbol Editor against [ADI Rev.B, Table 9](https://www.analog.com/media/en/technical-documentation/data-sheets/adxl367.pdf).
It is now placed as U26 on the native `orientation_sensor.kicad_sch`
hierarchical sheet (page 14). This is an explicitly marked WIP placement;
its supply and signal connections remain unfinished.

| Pins | Native electrical type |
| --- | --- |
| 1 SCLK, 4 CS/SCL, 8 ADC_IN | Input |
| 2 MOSI/SDA, 3 MISO/ASEL, 5 INT1, 6 INT2 | Bidirectional |
| 7/11 GND, 10 VS, 12 VDDIO | Power input |
| 9 VREG_OUT | Power output |

Bidirectional base types preserve the shared-pin modes; select more specific
alternates when implementing I2C and interrupt-only operation. VREG_OUT is
for internal-supply decoupling, not an available external-load supply.

A read-only comparison confirms twelve unique pins with unchanged names,
coordinates, lengths and graphic styles. Native rendering was inspected.
KiCad reordered pin records and omitted the explicit default name offset;
the properties dialog confirms the retained 20mil offset. No footprint or
3D model changed. The newly placed symbol contains the corrected pin types.

## SENS-002: power sequencing before electrical acceptance

ADI Rev.B pp5-6 and 58-59 require discharge below 50mV after power loss,
with at least 300ms below that level before restart. Supply capability must
exceed 250uA during startup/reset; this is a minimum source-capability
requirement, not a maximum current suitable for the power budget.

The current Rev.B Table 1 lists the 0V-to-90%-VS rise time as 4ms in the
minimum column; footnote 14 also calls it a minimum. An older
[ADI employee reply dated 2022-04-06](https://ez.analog.com/mems/f/q-a/556831/adxl367-software-reset-timing)
instead says the rise time must be less than 4ms. The revision history
records Table 1 changes in Rev.B. Preserve this conflict until the current
requirement is resolved; do not turn the older reply into a current guarantee.
The manufacturer PDF was retrieved by the web reader, but its table has
not yet been visually verified locally because direct downloads failed.

A controlled-rise load switch is only a candidate. Its typical slew curve
does not establish a guaranteed timing bound across process, voltage,
temperature and external-component tolerance. The
[TI TPS22918 CT discussion](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1236075/tps22918-inquiry-about-ct-and-rise-time)
explicitly identifies the rise-time data as typical; no switch is accepted
for U26 by this placement.

Consequently, direct attachment to +3V3_MCU is not yet qualified. Next:
design a controlled, discharged sensor supply; bound off-state bus injection;
then allocate the I2C bus and interrupt, select bypass capacitors, and draw
the complete sensor branch. The existing main-rail discharge calculation
does not establish a 300ms minimum restart interval.

### Native wiring validation, 2026-09-27

The root hierarchy gained only the new sheet block; existing sheet content
has no semantic Git diff after native Save All (line endings were normalized
by KiCad). U26 is automatically annotated and has twelve physical pins.
U26 pins 7 and 11 are grounded. Pin 1 is grounded for I2C operation.
Unused ADC_IN pin 8 has an explicit no-connect, as permitted by Table 9;
this does not hide unfinished interface wiring. C115 and C116 are parallel
100nF capacitors from VREG_OUT pin 9 to ground, nominally 0.2uF. Their
exact ordering codes, tolerance and effective capacitance remain to be
qualified. An unrelated inherited footprint was cleared before duplication.

Fresh CLI netlist comparison preserves all 271 pre-existing component
records and all their net memberships. Only U26, C115 and C116 are added.
CLI ERC now reports 122 errors and 55 warnings, compared with the resumed
114-error/55-warning baseline. The eight additional errors are confined to
unfinished U26 wiring: five unconnected pins, one undriven input, and two
undriven power inputs. No ERC suppression or placeholder power flag was
added. Complete exports and BOM refresh remain pending.

Rev.B page 29 confirms the seven-bit I2C address is 0x1D with ASEL grounded
or 0x53 with ASEL high. ASEL pin 3 is now grounded, selecting 0x1D.
INT2 pin 6 is explicitly unused: use INT1 for interrupts and the internal
clock/sample timing. Firmware must leave EXT_SAMPLE disabled and must not
map interrupts to INT2. See Rev.B pp61-62. The fresh netlist confirms both
treatments; ERC removes only these two unconnected-pin findings with no
new finding. Do not confuse the I2C address with the MEMS device-ID value.

## SENS-003: control bus and isolation screening, 2026-09-27

**Review correction:** the dual-domain pullup proposal below is rejected.
Its rise-time and sink arithmetic passes, but its absolute-voltage behavior
does not. Do not implement it. The retained numbers explain the rejection;
SENS-004 records the revised direction. No such pullups or switch have
been placed, so no native circuit rollback is required.

Reserve IIC0_A for the sensor/control bus: SCL=P410/K13 and SDA=P409/R16
on the selected 289-ball MCU. Both pins are unconnected in the saved
netlist; these are reservations, not completed hierarchy connections.
[Renesas Rev.1.30 Table 1.17](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet)
identifies these dedicated IIC alternates (asterisked in the table), distinct
from SCI channels with similarly named SCL/SDA functions. Preserve camera
IIC1_A and the existing memory/radio/audio assignments. P407 remains SD_READY.
USB controller integration must not reuse P409/P410 for overcurrent signals.
Use external port-controller status on another GPIO when that circuit is drawn.

Candidate isolation: [TI TMUX1511, SCDS390B](https://www.ti.com/lit/ds/symlink/tmux1511.pdf),
three channels for SCL, SDA and INT1. Its 4.5ohm maximum on-resistance,
6pF maximum on-capacitance, 70uA maximum supply current and 2uA
full-temperature powered-off leakage are screening inputs. Do not use the
25C, <=3V 10nA leakage row for a 3.3V product. Control threshold is 1.2V
high/0.45V low; the internal 6Mohm pulldown is typical, not a guaranteed
default-state design. An external pull and a hardware valid-supply gate
remain required. This is not a selected or placed component. Its power-off
leakage bound applies at VDD=0; behavior throughout rail collapse needs review.
The 100nA off-leakage row has different terminal-voltage test conditions.

Run `python scripts/check_sensor_bus_budget.py` for a **candidate arithmetic
screen**, not circuit acceptance. The model assumes two 2.4kohm pullups per
line (one per domain), 1% initial tolerance, 100ppm/K over an assumed 100K
excursion, both domains within 3.15182..3.39301V, and 25..100pF aggregate
bus capacitance. These rail and capacitance bounds are design targets and
must be established by the eventual circuit; the switched rail is not yet
designed. The lumped RC approximation does not validate a distributed bus,
switch transition behavior, or timing over all operating conditions.

Calculated screening results:

- 2.559867mA sink load and 0.411519V remote low including switch resistance.
- 3.133329V high floor with the modeled 15.05uA aggregate leakage.
- 24.913099..104.100710ns 30%-70% rise for the assumed capacitance range.
- 20.069763..115.272989pF mathematical capacitance window for 20..120ns.
- Up to 51.268153uA cross-current between unequal live supply domains.

The rise target combines the MCU's 20ns minimum (Table 2.66) with the
sensor's 120ns maximum (Table 4). The latter table is specified at 25C,
VS=VDDIO=2V, so this arithmetic alone does not qualify 3.3V/full-temperature
operation. The MCU 3mA sink screening avoids assuming the stronger FMPE
mode; actual peripheral timing and filters still need configuration review.

An illustrative three-channel 6uA injection budget with a guaranteed
<=1kohm discharge path yields 6mV equilibrium. With <=1uF capacitance,
discharge from 3.39301V to 50mV takes 4.343513ms, after which the separate
300ms hold must elapse. **Neither the discharge path nor these leakage and
capacitance limits are implemented.** Include load-switch leakage, board
leakage and interrupt pulls before accepting a restart delay; count the
hold from crossing 50mV, not from issuing a shutdown command.

## SENS-004: supply/interface coupling review, 2026-09-27

ADI Rev.B Table 5 limits digital-pin voltage to VDDIO, without a +0.3V
allowance. Equal pullups to the two modeled rail extremes produce a
3.272415V bus while sensor VDDIO is 3.151820V, even at zero leakage.
The bus therefore violates that limit although both rails are individually
valid. A bilateral switch does not translate voltage. The script now
explicitly reports this rejected case rather than printing an overall pass.

The next candidate uses one 2.4kohm pullup on each line, both to sensor
VDDIO, and two TMUX1511 channels. Host internal pulls must remain disabled,
including during recovery; hardware isolation must cover reset/power loss.
The dedicated sensor segment cannot inherit other devices' host-rail pulls.
The assumed aggregate capacitance is reduced to 25..50pF, giving the
49.826198..103.910068ns lumped rise screen. Actual capacitance, leakage,
switch control and collapse behavior remain open. This is not wired yet.

For an external supply ramp, a 91ohm feed and a **guaranteed effective**
30..70uF capacitance allocation give a 6.121242ms minimum ideal charge
screen from a 50mV residual to 90% of 3.39301V. Assumptions are a monotonic
bounded source, no external backfeed, no positive load injection, and the
same resistor tolerance/TCR model as SENS-003. The feed would precede both
VS and VDDIO, avoiding a large resistor between the two supply pins.
This does not resolve the conflicting ADI rise-time guidance in SENS-002.

At the low input corner, two continuously low bus lines plus an **assumed**
1mA other-load allocation yield 2.835213V. This is not a guaranteed ADXL
maximum-current model. Its 0.9*VDDIO interrupt-high screen is 2.551691V,
below the host GPIO requirement 0.8*3.39301=2.714408V. Accordingly INT1
needs voltage translation (review the existing TXU0102 family) rather than
a third bilateral-switch channel. Use the separate GPIO thresholds in
Renesas Table 2.5, not its 0.7*VCC IIC row, for this interrupt check.

The [TPS22917 datasheet](https://www.ti.com/lit/ds/symlink/tps22917.pdf)
was downloaded and page 6 visually inspected: its 150ohm QOD figure is
in the **typical** column, not the maximum column. It cannot establish a
guaranteed discharge time. Its switching-time table is also typical.
An external bounded discharge path or measured-voltage restart interlock
is needed; do not apply the earlier illustrative 1kohm/1uF result to a
30..70uF ramp capacitor. None of these candidate supply parts is placed.

Possible ramp capacitor: KYOCERA AVX TAJB476K010RNJ, nominal 47uF,
10V, 10%. The [TAJ Rev.3 sheet](https://datasheets.kyocera-avx.com/TAJ.pdf)
lists this family row at 4.7uA initial DCL and 1ohm ESR (100kHz).
Its qualification table distinguishes temperature stability, endurance and
humidity tests; passing those individual tests does not automatically prove
the combined 30..70uF allocation. Confirm effective capacitance, leakage,
ESR over the ramp frequency range, surge/derating and lifecycle before
selection. Procurement and native fields remain pending.

---

## SENS-005: local supply bypass implementation, 2026-09-27

Placed and wired through native KiCad: C117 = 100nF from U26 VS pin 10
to GND, and C118 = 100nF from VDDIO pin 12 to GND. Both use the standard
Device:C_Small primitive with a visible common ground return. VS and
VDDIO remain distinct, undriven nets pending supply design. No power flags
were added. Exact capacitor ordering codes and footprints remain pending;
blank footprints avoid inheriting an unrelated imported part's footprint.
Authority: ADXL367 Rev.B, page 58, Power Supply Decoupling.

Read-only exported-netlist comparison against the preceding address-strap
checkpoint confirms every pre-existing net membership is unchanged after
excluding the two new capacitors. Each new capacitor's pin 1 connects only
to its intended U26 supply pin, and both pin 2 returns connect to GND.
ERC is now 120 errors / 55 warnings: two unconnected supply-pin findings
removed, no new findings. Undriven supply findings remain intentionally open.

Direct current-revision PDF downloads continued to time out. The reachable
Akizuki mirror is Rev.0 (64 pages), not Rev.B; it must not be used as visual
verification of the current table. Rev.B manufacturer text still explicitly
calls the rise-time requirement a minimum in Table 1 footnote 14. The older
support-answer conflict remains unresolved; no ramp circuit was accepted.

## SENS-006: synchronized supply domain, 2026-09-27

An [ADI employee clarification, 2025-12-22](https://ez.analog.com/mems/f/q-a/601740/power-supply-for-vddio-on-the-reset)
explicitly addresses ADXL367: do not reset VS to ground while retaining
VDDIO at 3.3V; both supplies should transition together. The employee points
to ADXL366 page 63 for this sequencing detail while a merged clarification
is being prepared. That related-part reference does not replace ADXL367's
other specifications. Read the employee reply, not the page's AI summary.

Accordingly U26 VS and VDDIO are now joined by a visible native wire,
with one common future switched/ramped supply. C117 and C118 remain
separate local bypass parts for their respective supply pins. This supersedes
SENS-005's separate-net state. Do not simplify the interface by keeping
VDDIO on the host supply while independently cycling VS. The common-domain
choice is consistent with the single-supply option in ADXL367 Rev.B page 58.
Supply source, isolation and restart control remain unfinished.

Read-only netlist comparison verifies exactly one change: the two two-node
supply nets merged into {U26.10, U26.12, C117.1, C118.1}. All other net
memberships and all component records are unchanged. Native ERC now has
119 errors and 55 warnings; merging the two undriven supply nets removes
one duplicate undriven-net finding, not the unresolved supply requirement.

Additional screening: CSD13380F3 is not yet accepted as an external
discharge switch. Its [SLPS593A electrical table](https://www.ti.com/lit/ds/symlink/csd13380f3.pdf)
specifies on-resistance at 25C unless stated otherwise; a room-temperature
maximum plus a typical temperature curve cannot establish the full-temperature
bound requested here. A passive bleeder or measured-voltage interlock remains
an available design route. No bleeder or discharge MOSFET has been placed.

## SENS-007: passive discharge branch, 2026-09-27

R102 = 4.7kohm is now wired across the common U26 supply and GND through
native KiCad. It provides a passive discharge path independent of control
logic or the load switch's typical-only QOD resistance. It is a WIP circuit
choice, not acceptance of the complete restart system. Its pin 1 is on the
sensor supply; pin 2 is grounded. Native netlist comparison preserves all
earlier connectivity after excluding R102. ERC remains 119 errors / 55 warnings.

Candidate exact part: YAGEO RC0603FR-074K7L, 0603, 4.7kohm, 1%,
100ppm/C, 0.1W at 70C. The native Datasheet field records the
[manufacturer specification](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-074K7L).
MPN/procurement fields and footprint assignment remain pending. The
[DigiKey listing](https://www.digikey.com/en/products/detail/yageo/RC0603FR-074K7L/727212)
identifies CT order code 311-4.70KHRCT-ND; the retrieved 2026-09-27 snapshot
showed active status and 3,346,683 available (unreserved).

The Python sensor-budget script now evaluates 1% initial tolerance, a
conservative 100K excursion at 100ppm/K, and an additional 5% lifetime
drift allocation. That last allocation requires qualification; it is not a
claim that individual manufacturer environmental tests prove all combined
service conditions. The resulting resistance envelope is 4376.147..5034.194ohm.
With <=70uF total rail capacitance and <=8uA total incoming off-state current,
the equilibrium is 40.274mV. Discharge from 3.39301V to 50mV takes at most
2.058924s in this lumped model; adding the 300ms hold gives 2.358924s.
A candidate minimum restart interval is 3s, measured from actual source
removal and valid isolation, including control/clock tolerance. It is not
yet a proven firmware delay or hardware interlock.

Cost while powered: at most 0.775342mA and 2.630743mW under that resistance
envelope. Include this in the product sleep budget; it dominates the bare
accelerometer's typical current. With the existing hypothetical 91ohm feed,
two low bus lines and 1mA other load, the additional bleeder leaves a
2.780545V supply and 2.743631V IIC high screen. Interrupt translation is
still required by the earlier GPIO threshold analysis.

The 8uA injection limit is an acceptance budget, not yet a sourced sum.
TMUX1511's VDD=0 specification does not qualify the entire collapsing rail;
TXU0102 also has supply-pin reverse current as well as I/O leakage. The
current TXU0102 SCES941A page 8 gives -1uA on an unpowered supply at
-40..85C under its stated test conditions. Account for that path, load-switch
leakage, control inputs, board leakage and retained charge before accepting
the delay. Do not call the discharge requirement closed solely because
the arithmetic assertions pass. The 4ms rise-time discrepancy remains open.

## SENS-008: loaded-rail ramp calculation correction, 2026-09-27

The earlier 6.121ms calculation targets 90% of the input voltage, not 90%
of the loaded sensor supply. It cannot establish the proposed minimum
rise time. The calculation script now labels that result historical.

For a conservative fastest-charge envelope, ignore all discharge loads,
use a source at most 3.39301V, initial voltage at most 50mV, and the minimum
feed resistance 89.1891ohm. Target 90% of the hypothetical loaded supply
floor, 0.9 * 2.780545V = 2.502490V. With no positive current injection,
the lower time bound is Rmin * Cmin * ln((Vmax - 0.05)/(Vmax - Vtarget)).
At 30uF it is only 3.539439ms. This is insufficient proof of a 4ms minimum,
not evidence that a physical corner necessarily fails. The calculated
minimum capacitance is 33.903681uF; a revised provisional effective
capacitance allocation of 40..70uF yields a 4.719252ms lower bound.

No ramp capacitor is qualified or placed. The supply floor still assumes
a hypothetical 1mA non-bus load; it is not a guaranteed ADXL367 startup
current bound. Positive injection, capacitor ESR, effective capacitance
over all conditions, and actual source behavior still require review.
The manufacturer's conflicting rise-time guidance remains unresolved.
The unchanged 70uF upper allocation preserves SENS-007's conditional
discharge arithmetic; neither calculation proves circuit acceptance.

The native schematic note now describes the implemented common supply,
local bypass capacitors and R102, with source/interfaces explicitly WIP.
After native save, exported component records and every net's pin membership
match the SENS-007 checkpoint. The note is visually readable without
overlapping the circuit. The calculation script and `git diff --check` pass.

## SENS-009: bypass-capacitor sourcing, 2026-09-27

C115-C118 candidate ordering code: Murata GRM188R72A104KA35D,
100nF +/-10%, X7R, 100V, 0603 (1608 metric). The
[manufacturer product page](https://www.murata.com/products/productdetail?partno=GRM188R72A104KA35%23)
identifies the D packaging suffix and -55..125C operating range. The
[2025 reference specification](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R72A104KA35-01A.pdf)
is the native Datasheet field source. Footprints remain unassigned under
the deferred physical-library qualification scope.

[DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/GRM188R72A104KA35D/702549)
lists active status, CT code 490-3285-1-ND, 735,979 in stock and USD0.16
at quantity one in the retrieved 2026-09-27 snapshot. Stock is unreserved;
recheck before purchasing. The older GRM188R71H104KA93D was not selected
because its listing is obsolete.

These are sourced candidates, not a claim that the complete sensor supply
is qualified. Two 100nF parts provide the nominal 0.2uF requested for
VREG_OUT by ADXL367 Table 9. Initial tolerance alone gives 0.18..0.22uF;
the X7R temperature characteristic, DC bias, aging and regulator stability
still require review. The 100V rating does not itself prove a capacitance
floor. C117/C118 retain their nominal 100nF supply-bypass roles. Do not
use these small bypass capacitors as the unplaced 40..70uF ramp capacitor.

Native KiCad bulk-field edits saved all four exact MPNs, manufacturer PDF
links, DigiKey codes/URLs, selection basis, procurement status and dated
sourcing snapshots. Read-only netlist comparison against SENS-008 confirms
that only C115-C118 component records changed and every net membership is
unchanged. `git diff --check` passes. No electrical wiring or value changed.

## 1. Sensors (Environmental & State Detection)

### Ambient Light Sensor (ALS)
* **Function**: Measures ambient room light intensity.
* **Purpose**: Automatically adjusts the screen front-light brightness and color temperature.
* **Interface**: I2C

### 3-Axis Accelerometer (G-Sensor)
* **Function**: Detects device orientation.
* **Purpose**: Triggers screen rotation (portrait/landscape).
* **Interface**: I2C + Interrupt GPIO

### Hall Effect Sensor
* **Function**: Detects magnetic fields.
* **Purpose**: Triggers automatic wake/sleep when a magnetic protective cover is opened or closed.
* **Interface**: GPIO (Active Low/High)

### Temperature Sensor
* **Function**: Measures temperature near the display panel.
* **Purpose**: Adjusts E-Ink drive waveforms to compensate for physical response differences in warm/cold environments.
* **Interface**: I2C or Thermistor (often integrated into the E-Ink panel or PMIC)

---

## 2. Core Peripherals & Support ICs

### E-Ink Power Management IC (EPDC PMIC)
* **Purpose**: Generates the high positive and negative voltages (+15V, -15V, +22V, -20V) required to physically manipulate the charged pigment particles in the E-Ink display.
* **Example**: Texas Instruments TPS65185 or equivalent.
* **Interface**: I2C (control) + Enable/Interrupt GPIOs

### Capacitive Touch Screen Controller
* **Purpose**: Decodes multi-touch gestures from the capacitive overlay on top of the E-Ink display.
* **Interface**: I2C + Reset + Interrupt GPIOs

### Battery Fuel Gauge
* **Purpose**: Monitors battery voltage, current, state of charge (percentage), and health.
* **Interface**: I2C

### Dual-Channel LED Front-Light Driver
* **Purpose**: Drives the LEDs for front-lighting. Supports two independent channels to blend warm (amber) and cool (white) LEDs for color temperature adjustment.
* **Interface**: PWM or I2C

### USB-C Charger & Protection Controller
* **Purpose**: Handles lithium-polymer battery charging, USB-C CC line detection (for power delivery compatibility), overvoltage protection, and thermal monitoring.
* **Interface**: I2C (or standalone status pins)

### Haptic Motor Driver (Optional)
* **Purpose**: Drives a linear resonant actuator (LRA) or eccentric rotating mass (ERM) motor to provide tactile page-turn feedback.
