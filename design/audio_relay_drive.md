# Headphone relay drive qualification

2026-10-05. Draft implementation for AUD-011/AUD-012. Q4, R116 and D13
are now placed and wired in the native schematic. No qualified coil supply
or hardware fault controller is established yet. K1 remains on HOLD.

## Coil supply constraint

The main regulator's allocated complete envelope is
3.151819680019 to 3.393012496197 V; see
[main regulator calculations](main_regulator_tps63806.md). This includes a
combined 75 mV allowance and is not measured performance. K1 requires a
qualified rated-voltage drive; connecting its 3 V coil directly to this
rail is not accepted.

[TI TPS7A20 Rev. H, electrical table, pages 6-7](https://www.ti.com/lit/ds/symlink/tps7a20.pdf)
specifies +/-1.5% output tolerance for a 3 V DBV part with input at least
VOUT(NOM) + 0.3 V. Our lower rail endpoint misses that test condition by
148.180 mV. DBV dropout is 145 mV maximum at 300 mA, measured with output
at 95% of nominal. Neither a lower-current dropout estimate nor typical
curves extends the stated output-tolerance guarantee to our input envelope.
TPS7A2030PDBVR powered directly by the main rail is therefore **not accepted**
as a guaranteed 3 V coil supply from that rail. U35 is now placed as an
incomplete draft for a separate auxiliary supply, as recorded below.

A future supply choice must either provide sufficient guaranteed input
headroom, have explicit low-headroom regulation limits covering the actual
envelope, or use a qualified conversion/drive arrangement. Do not silently
raise the main rail or change its existing tolerance allocation.

### Higher-input supply contract, 2026-10-05

Correct the earlier shorthand ordering code: the exact 3 V SOT-23-5 device
is **TPS7A2030PDBVR**, not TPS7A2030DBVR.
[TI's exact product page](https://www.ti.com/product/TPS7A20/part-details/TPS7A2030PDBVR)
marks it Active. [DigiKey's exact listing](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A2030PDBVR/13566871)
showed 12,059 stock, cut-tape MOQ1, USD 0.35/1 and 0.245/10,
26-week standard lead time on October 5. TI's public ordering page showed
out of stock; distributor stock is an unreserved snapshot.

For the next supply implementation, investigate a regulated audio auxiliary
5 V bus with an allocated 4.75-5.25 V envelope at the LDO input. This is a
**new design contract**, not an existing implemented rail. It must work on
battery and authorized external power, remain separate from raw USB-PD,
and be available before disconnect closure. Do not substitute a headphone
signal rail or assume the charger SYS output provides this envelope.
The lower endpoint exceeds the LDO's 3.3 V accuracy-test input floor by
1.45 V. Its upper endpoint leaves 0.75 V to the 6 V recommended input
ceiling; upstream startup/overshoot must also satisfy that ceiling.

With the provisional 60 mA coil allocation, a conservative 2 mA LDO ground
current allocation gives 62 mA input and 325.5 mW at 5.25 V. Using the
2.955 V lower output endpoint gives 148.2 mW LDO loss. The DBV data-sheet
187.1 C/W reference-board thermal metric gives a 27.73 C rise screen;
it is not a sealed-enclosure or PCB thermal guarantee. One regulator may
serve the current single-ended relay only at this allocation. Do not add
balanced relays without revisiting aggregate load, dissipation and fault
sequencing. Startup capacitors/inrush are additional to this steady budget.

The candidate output envelope is 2.955-3.045 V before transient/wiring
allowances. Subtracting the provisional Q4 49.2 mV drop leaves 2.9058 V at
the coil before wiring loss. This exceeds the 23 C catalog pickup screen,
but does not establish hot pickup or release behavior. Omron's 150 percent
maximum coil voltage is explicitly instantaneous, so it does not justify
continuous direct connection to the main 3.3 V rail.
[G6K manufacturer ratings and notes](https://components.omron.com/us-en/system/files/2026-05/datasheet_pdf/K106-E1.pdf).

Implementation order: qualified auxiliary converter/source selection;
exact native LDO symbol and pin review; local capacitors and coil supply;
hardware rail-good/DC-fault gate with startup delay; then closure and
fault-energy validation. No new regulator is placed at this study checkpoint.

## Low-side switch screening

[Nexperia PMV20EN, July 2018, table 7](https://assets.nexperia.com/documents/data-sheet/PMV20EN.pdf)
specifies maximum on resistance at gate voltages 4.5 and 10 V. Its threshold
and logic-level description do not qualify resistance at our prospective
3.3 V control voltage. Reject this candidate for a direct 3.3 V gate drive.

[Nexperia PMV30UN2, April 2014, tables 2 and 7](https://assets.nexperia.com/documents/data-sheet/PMV30UN2.pdf)
maps gate/source/drain to pins 1/2/3. Maximum on resistance is 43 milliohm
at 2.5 V gate drive and 25 C, and 59 milliohm at 1.8 V and 25 C.
Its 150 C maximum is specified at 4.5 V, not 2.5 V. Thus its room-temperature
logic-drive screen is useful, but it is **not yet a qualified full-temperature
driver**. The 20 V drain rating also requires clamp tolerance and overshoot
margin. This candidate was not placed; the draft instead uses Q4 FDN337N.

## Remaining implementation gates

### FDN337N native library preparation (2026-10-04)

`Power_Devices:FDN337N` is a native KiCad library candidate, derived from
KiCad 10 `Transistor_FET:Q_NMOS_GSD`. It is now placed as Q4, with R116
10k from gate to source. The native BOM export includes both components.
Its inherited 1 G / 2 S / 3 D map still
requires visual comparison with the exact manufacturer package drawing.
Footprint is blank. Do not treat this preparation checkpoint as approval.

[onsemi FDN337N/D, November 2023 Rev. 5, pages 1-2](https://www.onsemi.com/pdf/datasheet/fdn337n-d.pdf)
specifies 30 V drain rating, +/-8 V gate rating and -55 to +150 C junction
range. Maximum on resistance is 82 milliohm at 2.5 V gate drive and 25 C;
the 125 C maximum of 110 milliohm is specified at 4.5 V gate drive. There
is no guaranteed hot 2.5 V maximum in that table. Threshold is not an
on-resistance guarantee. Hot drive, leakage, transient clamp margin and
release-time qualification remain open.

[DigiKey exact onsemi listing](https://www.digikey.com/en/products/detail/onsemi/FDN337N/458847)
showed active status, cut-tape quantity one availability and 227,024 units
on 2026-10-04: FDN337NCT-ND, USD 0.90 at one / 0.557 at ten, 17-week
manufacturer standard lead time. This is an unreserved snapshot; recheck
before procurement. A same-named device from another manufacturer is not
an approved substitution.

## Native regulator placement checkpoint (2026-10-05)

U35 is now `Power_Devices:TPS7A2030PDBVR`, copied and flattened through
KiCad's native symbol editor from `Regulator_Linear:TPS7A20xxxDBV`.
TI SBVS338H Rev H section 4 verifies DBV pins 1 IN, 2 GND, 3 EN,
4 N/C and 5 OUT. Pin 4 has no internal connection and retains the
upstream hidden no-connect electrical type. The schematic connects pin 2
to GND and ties EN to IN per section 6.3.2; relay switching and independent
fault inhibition must act on Q4's gate, not rely on LDO enable timing.

At this placement checkpoint U35 IN/EN had no source, OUT had no
load or capacitor, and K1 pin 1 remained open. The auxiliary converter,
local capacitors, output-to-coil wiring and hardware fault control were
still required. The footprint is blank. Exact ordering code and dated
DigiKey Active/MOQ1 sourcing snapshot are retained in the native description;
separate procurement fields still need completion.

Native BOM fidelity passes for 311 included references and 19 columns,
with four native exclusions. The full 15-page PDF was rendered and reviewed;
only page 15 differs from the preceding checkpoint. ERC is 104 errors and
15 warnings, two more errors from the explicitly unfinished U35 input
source and output connection. No ERC policy was changed. Saved-netlist
inspection confirms U35 pins 1/3 share a net and pin 2 reaches GND.

### Local capacitor draft checkpoint (2026-10-05)

C130 and C131 now provide nominal 10uF/35V local input and output
capacitance respectively. Both use Device:C with blank footprints and
the exact candidate Taiyo Yuden MCJCG31LBB7106KTPA01 in the native
description. C130 pin 1 reaches U35 IN/EN; C131 pin 1 reaches U35 OUT;
both pin 2 terminals reach GND. The auxiliary source and K1 positive
coil connection remain open. These capacitors do not qualify that source.

[Manufacturer specification sheet, July 25 2023](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5483/MCJCG31LBB7106KTPA01_SS.pdf)
identifies 10uF +/-10%, 35V X7R, 1206 soft termination, mass production
and preferred status. The higher rating/nominal capacitance supplies
DC-bias margin; soft termination is a mechanical reliability feature,
not an audio fidelity claim. Characteristic curves are typical reference
data, not guaranteed minima. Effective capacitance across bias,
temperature, initial tolerance and aging, and effective ESR in the
regulator stability band, still need qualification.

TI Rev H recommended conditions require at least 0.47uF effective local
input capacitance and 0.47-200uF effective output capacitance for stability,
with output ESR at most 100 milliohm. The nominal 10uF choice is a draft;
do not equate its printed value with effective capacitance. Converter
ripple, startup inrush, interconnect inductance and transients also remain
open. Keep the parts close to U35 during later PCB implementation.

[DigiKey exact listing](https://www.digikey.com/en/products/detail/taiyo-yuden/MCJCG31LBB7106KTPA01/22208966)
showed Active, 1,585 units, cut tape MOQ1, USD1.40/1 and 0.912/10 on
2026-10-05: 587-MCJCG31LBB7106KTPA01CT-ND. This is an unreserved
stock snapshot. Separate procurement fields and footprint qualification
remain open; the native description and datasheet record the candidate.

Saved-netlist inspection verifies all three capacitor nets above. The
native BOM passes fidelity for 313 included references, 19 columns and
four native exclusions. Full 15-page PDF rendering was reviewed; only
page 15 changes relative to cc0f8d0. ERC is 103 errors and 15 warnings,
one fewer error than the placement checkpoint because U35 OUT is now
connected to C131. No ERC policy changed; unfinished circuits remain
visible. Clock and documented arithmetic checks pass separately.

## Native clamp draft (2026-10-05)

### Coil output connection checkpoint (2026-10-05)

Native local labels now connect U35 OUT, C131 pin 1 and K1 positive coil
pin 1 on `AUDIO_SE_COIL_3V`. Saved netlist confirms exactly those members.
Q4 gate remains default-off through R116; no firmware or independent fault
drive is implemented. U35 input still lacks a qualified source. This
connection does not approve relay pickup, source transients or DC protection.

ERC now reports 102 errors and 15 warnings: K1 pin 1's unconnected finding
is removed. BOM fidelity remains 313 included references, 19 columns, four
exclusions. Full PDF export preserves pages 1-14; changed page 15 was
rendered and visually reviewed. No ERC policy was changed.

The [TI TPS63070 family datasheet Rev B](https://www.ti.com/lit/ds/symlink/tps63070.pdf)
is an upstream auxiliary-converter screening candidate, not placed or
selected. TPS630701 has fixed 5V output, a 2-16V input range, forced PWM
and open-drain power good. It cannot accept raw 20V PD. Investigate supply
from the bounded low-voltage system bus, with shutdown isolation and
sequencing. Its internal VAUX pin must not supply external circuitry.
Output tolerance/ripple/transient budget, aggregate load, effective
capacitors, inductor limits, source isolation, current/thermal behavior,
exact code/lifecycle/MOQ1 stock and competing converters remain required
before native implementation. Do not infer guaranteed full-temperature
operation from the advertised switch-current limit or typical efficiency.

D13 is a Littelfuse SMF12A candidate, represented by the standard
`Device:D_Zener` unidirectional avalanche primitive. Its cathode connects
to Q4 drain / K1 pin 8 (`AUDIO_SE_COIL_LOW`); its anode connects to Q4
source / GND. K1 pin 1 is still unpowered. Exact manufacturer, datasheet,
selection limits and dated quantity-one sourcing fields are recorded in
the native schematic and exported BOM.

[Littelfuse SMF datasheet, revised November 2, 2023](https://www.littelfuse.com/assetdocs/tvs-diode-smf-datasheet?assetguid=7eb8a5b6-bdd0-4561-8f19-0c3cc6f9b2af)
lists SMF12A with 12 V standoff, 13.3–14.7 V breakdown at 1 mA,
19.9 V maximum clamp at 10.1 A for the specified 10/1000 us pulse,
and 2.5 uA maximum leakage at standoff under table conditions.
Those conditions do not establish a full-temperature clamp limit for our
actual waveform. The nominal 30 V MOSFET rating leaves 10.1 V against
the listed clamp point; temperature shift and layout overshoot consume
that margin and must be bounded before acceptance.

[DigiKey F5747CT-ND](https://www.digikey.com/en/products/detail/littelfuse-inc/SMF12A/3429604)
showed Active, 73,684 stock, cut-tape MOQ1, USD 0.52/1 and 0.318/10 on
2026-10-05. This is an unreserved source snapshot, not a lifetime guarantee.

The drain-to-source clamp dissipates both stored coil energy and energy
delivered by the coil supply during decay. With constant clamp Vc above
supply Vs and ignoring winding resistance conservatively,
`t_decay = L*I0/(Vc-Vs)` and
`E_TVS = 0.5*L*I0^2*Vc/(Vc-Vs)`.
Coil inductance, temperature, actual clamp waveform and contact release
must be characterized; the catalog release time is not transferred to
this circuit. A plain diode would yield a lower reverse coil voltage and
slower electrical current decay. This TVS does not detect headphone DC
or replace independent hardware fault gating.

Use 60 mA as a provisional coil-current allocation, not a measured maximum.
A provisional Q4 resistance allocation of 0.82 ohm (ten times the listed
25 C / 2.5 V maximum) gives 49.2 mV drop and 2.952 mW dissipation.
This generous engineering allowance is not a manufacturer hot guarantee;
it enables draft integration while full-temperature verification remains open.

### Saved checkpoint verification

Native Save All, full 15-page PDF export and visual review completed on
2026-10-05. Pages 1-14 render identically to the prior committed PDF;
page 15 adds the driver/clamp draft and updates its implementation note.
The native BOM export matches the saved netlist for all 310 included
references and 19 columns, with four native exclusions. Netlist inspection
confirms D13 cathode / Q4 drain / K1 pin 8 share `AUDIO_SE_COIL_LOW`,
D13 anode / Q4 source / R116 pin 2 share GND, and R116 pin 1 reaches
Q4 gate. The gate has no active drive yet.

ERC is 102 errors and 15 warnings: the only removed finding is K1 pin 8
previously unconnected; no new finding identities appear relative to the
103-error / 15-warning baseline. No ERC policy was changed. Clock checks,
coil-supply headroom arithmetic and provisional switch-loss arithmetic pass;
these do not qualify the unfinished protection system.

- Establish guaranteed coil pickup across temperature, tolerance and
  self-heating; the relay's 23 C pickup limit is insufficient by itself.
- Budget worst-case cold coil current for the selected output group and
  fault cases. Include coil supply loss in the battery and thermal budgets.
- Select the switch, default-off bias, gate resistance and qualified control
  interface, including missing control power and powered-off leakage.
- Select the inductive clamp with a bounded peak drain voltage and pulse
  energy. Characterize release with that clamp; do not apply the catalog
  release time to an untested flyback arrangement.
- Implement independent DC/rail-fault gating with fault override of the MCU,
  startup delay and defined fault-energy/detection/opening limits. Ground
  remains continuous; balanced outputs require four switched conductors.
- Check exact purchasable ordering codes and small-quantity stock before
  importing parts; candidate electrical suitability is not procurement proof.

```python
from math import isclose
main_min_v = 3.1518196800191163
ldo_nom_v = 3.0
accuracy_test_min_v = ldo_nom_v + 0.3
headroom_shortfall_v = accuracy_test_min_v - main_min_v
assert main_min_v < accuracy_test_min_v
assert isclose(headroom_shortfall_v, 0.14818031998088355)
print('TPS7A20 accuracy-test input shortfall V:', headroom_shortfall_v)
print('Coil supply NOT qualified; no extrapolated accuracy guarantee.')
```
