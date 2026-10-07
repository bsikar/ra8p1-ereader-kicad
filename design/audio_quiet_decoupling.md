# Quiet headphone rail bulk: C128/C129

2026-10-05, Stage 7, [YouTrack RA8HW-4](https://youtrack.locked.cv/issue/RA8HW-4).
**WIP/HOLD: regulators, startup and assembled-board qualification remain open.**

Added native `Device:C_Polarized` capacitors through KiCad GUI: C128 positive
to AUDIO_VPOS, negative to GND; C129 positive to GND, negative to AUDIO_VNEG.
They supplement C126/C127 at U34. Native XML confirms polarity and preserves
every prior component field and pin-to-net membership. Footprints are blank.

This is the provisional quiet **+/-5V** OPA1622 supply, not the desktop bank.
Stage 6's +/-3V alternative remains open. These caps do not select the final
quiet rail or establish output capability.
[TI OPA1622 SBOS727B](https://www.ti.com/lit/ds/symlink/opa1622.pdf), Rev B,
section 10 p26, requires local 100nF ceramic bypasses from each supply to
ground. Additional 10uF is our allocation, not a TI mandated bulk value.
C126/C127 now use **TDK C1608X7R1H104K080AA**, 100nF +/-10%, 50V
X7R, -55..125C, manufacturer Production. The
[TDK part record](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H104K080AA)
and the pinned September 5 nominal DC-bias CSV give **98.5033nF at 5V**;
this is not a guaranteed minimum. Initial tolerance alone gives 90nF;
temperature, bias, aging and placement remain separate qualification gates.
The ceramic is nonpolar; each rail connects to GND, as required by TI.

[Mouser 810-C1608X7R1H104K](https://www.mouser.com/en/ProductDetail/TDK/C1608X7R1H104K080AA?qs=NRhsANhppD8dEJli2CDBHA%3D%3D)
web snapshot observed 2026-10-05: cut tape MOQ1/multiple1, $0.11 qty1 / $0.042 qty10,
620,194 stock, 24-week lead time, unreserved. This reuses an existing project
MLCC rather than introducing a second equivalent value. Higher-voltage/smaller
ceramics or C0G are alternatives, but need their own effective capacitance/
area/impedance evidence; no audible brand benefit is assumed. Native fields
record MPN, authority, local pin function and sourcing. Final rail/PDN and
local placement qualification remain HOLD; footprints remain deferred.

The all-parts audit preserves distinct indexed distributor quantities and
source ages; these are not live checkout reservations. Recheck the exact
cut-tape offer before buying the full high-count bypass bank. See
[component audit](component_audit_2026-10-05.md).

## Exact candidate

**KEMET T521B106M016ATE100**: 10uF +/-20%, 16V polymer tantalum, 100mohm
maximum ESR at 100kHz/25C, -55 to 125C. Authority:
[KEMET T2076_T52X-530](https://yageogroup.com/content/datasheet/asset/file/KEM_T2076_T52X-530),
2026-09-09, ordering row p25; voltage/ripple/reverse constraints pp33/34/36.
B case 3.5 x 2.8 x 2.0mm, MSL3; land pattern deferred. Leakage up to 16uA
after five minutes at rated voltage/25C is not a hot standby guarantee.

Category 5 recommends at most 90% rated DC through 105C (14.4V), reducing
to 60% at 125C (**9.6V**). +/-5V leaves voltage margin; this part is **not
selected for a +/-14V bank**. Rated ripple 1.410Arms at 45C/100kHz has
temperature multipliers 1.00 through 85C, 0.70 at 105C and 0.25 at 125C.
The corresponding 125C screen is 0.3525Arms at 100kHz; actual spectrum and
heating require analysis.

[DigiKey 399-16631-1-ND](https://www.digikey.com/en/products/detail/kemet/T521B106M016ATE100/8042258)
snapshot 2026-10-05: cut tape MOQ1, $1.72 each / $1.145 at ten, 17,479
available, 36-week standard lead, distributor Active. Unreserved, not a
purchase or continuing supply guarantee. Pair approximately $3.44 at qty1.
Similar T520 row is manufacturer NRND in the current datasheet despite
distributor Active listings; it was not used.

Alternatives are bias/temperature-qualified MLCC bulk (lower ESR but
effective capacitance, microphonics and regulator stability need proof), or
other suitable polymer/aluminum capacitors. The candidate provides documented
C/ESR and single-unit sourcing; no audible brand/price advantage is claimed.
Final choice requires the regulator's capacitance/ESR limits.

## Reservoir calculations and release gates

An illustrative 100mA, 10us pulse without upstream replenishment gives
`deltaV = I*dt/C + I*ESR`: initial minimum 8uF/100mohm gives **0.135V**.
Endurance allows -20% C change and twice initial ESR under the specified
test (p5); combining with initial tolerance gives an illustrative
6.4uF/200mohm screen, **0.17625V**. This is sensitivity arithmetic, not a
lifetime or rail-transient guarantee. A 1ms/100mA demand would consume
12.5V from 8uF alone: bulk capacitance cannot replace regulation.

At 5V nominal energy is 125uJ each, 250uJ per pair. A 1ms linear ramp with
maximum initial 12uF requires 60mA per rail from capacitance alone. Inrush
is converter/impedance dependent. 100mA ripple through 100mohm gives 1mW;
the actual spectrum/hot ESR must set the thermal budget.

Continuous reverse DC is prohibited. P36's limited transient allowance
shrinks to 1% rated at 125C (0.16V); normal operation must not reverse-charge
the negative-rail capacitor. Before release, prove:

- Sequencing, shutdown/discharge and reverse voltage during USB removal,
  full/dead battery, rail failure and stored-energy discharge.
- Regulator stability over effective C/ESR/temperature/tolerance, startup,
  load transients and residual rail noise/PSRR.
- Ripple spectrum, heating/endurance and exact land pattern.
- Pin-2/pin-4 local bypass placement and pin-11 exposed pad at V-, followed
  by loaded noise/pop/DC/fault measurements.

Native `Selection_Basis` records exact MPN, source/date, limits and HOLD.
This checkpoint does not finish charger, rail converter, jack or fault latch.
Sealed-enclosure temperature and moisture protection remain open.
