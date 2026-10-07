# CMS-013 MIPI regulator value review

2026-10-05 decision: retain installed U23 `LT3042IMSE#PBF` for this
checkpoint. Its $9.12 qty-one audit price merits optimization, but a cheaper
part must preserve supply accuracy, startup/restart and reverse-fault behavior.
This is the follow-up to the [complete component audit](component_audit_2026-10-05.md).
Neither the existing circuit nor any alternative is a manufacturing release.

## Requirements and candidates

The [existing CMS-013 circuit](camera_storage_interfaces.md#cms-013---mipi-host-18v-supply-implementation-in-progress)
powers only host VCC18_MIPI. Camera-module power is separate. RA8P1
R01DS0439EJ0130 Tables 2.2/2.39/2.44 require 1.65..1.95 V and at least
8.4 us/V rise gradient; the 4.1 mA CSI operating condition is not a startup
or all-mode limit. C109 has 22 uF nominal storage and R94 a permanent 1k
load. A sudden input collapse can leave the output charged.

| Exact alternative | Lifecycle / qty-one evidence | Electrical/value disposition |
| --- | --- | --- |
| TPS7A2018PDBVR | TI exact Active; DigiKey 44,860/$0.37 CT snapshot | Reject as a direct substitution: retained output can violate its input-relative absolute maximum and cause damaging reverse current. Extra protection needs its own fault analysis. |
| TPS73118DBVR | TI exact Active; DigiKey 2,647/$1.38 CT, retrieved Oct 5 | Reject as a direct substitution: EN must go low before input removal for reverse blocking. Tying EN to IN can also cause startup overshoot with slow ramps. Its broad accuracy row starts at 10 mA, above this branch's normal load. |
| TPS70918DBVR | TI Active family; indexed two-month DigiKey offer 2,933/$1.51 CT, not refreshed | Reject for this direct replacement: reverse blocking is conditional on output above 1.8 V. Do not infer coverage throughout collapse of a nominal 1.8 V rail. |
| LT3008EDC-1.8#TRMPBF | ADI recommended for new designs; DigiKey 2,563/$4.75 CT, retrieved Oct 5 | Backup study: autonomous reverse protection, but 20 mA capacity and no programmable reference soft-start. Four cents saved versus LT3060 does not justify losing load margin and timing control. |
| LT3060EDC-1.8#TRMPBF | ADI recommended for new designs; DigiKey 813/$4.79 CT, retrieved Oct 5 | Preferred next candidate; $4.33 lower IC price, fixed 1.8 V, 100 mA, programmable reference bypass/startup and reverse protection independent of SHDN. Not installed or purchase-approved. |
| LT3060IDC-1.8#TRMPBF | Exact code in ADI datasheet; indexed four-month DigiKey stock 50 is TR MOQ500, Mouser nonstocked | Do not substitute an assumed qty-one industrial offer. The E-grade CT offer above is distinct; E-grade limits are assured by design/characterization over -40..125 C, while I-grade has full-range guarantee. Refresh if I-grade is required. |

Stock is an unreserved web snapshot, excluding freight/tax. Reel suffixes
alone do not determine MOQ; the offered distributor packaging does.
Active/recommended status does not guarantee a future production horizon.

## LT3060 bounded screen and remaining integration work

ADI Rev D specifies 1.764..1.836 V for the E/I fixed 1.8 V DFN under its
line/load conditions, including load above 1 mA. Keep R94: its lower screen
is 1.617488482 mA even at the MCU's 1.65 V lower limit. Input 3.151819680 V
exceeds the 2.35 V accuracy condition by 0.801819680 V. The conditional
C109 minimum remains 8.976 uF versus the 2.2 uF requirement, with ESR <=3 ohm;
the assumed bias/aging retention still needs evidence.

DFN pin map for a future native asset: 1 REF/BYP, 2 ADJ, 3/4 OUT,
5/6 IN, 7 SHDN, 8 GND, exposed pad 9 GND. SHDN can follow IN.
Fixed-version ADJ can be left open when feedforward filtering is unused;
it is not an output-sense pin. Remove R95's SET function only with the
actual circuit migration; do not reuse the LT3042 pin numbers.

Reference soft-start is approximately 6 ms with 10 nF. Reusing C110's
100 nF gives approximately 60 ms; 4.7 nF gives approximately 2.82 ms.
These are typical proportional screens, not minimum/maximum output ramp
or settling guarantees. The [U2 reset calculation](reset_coordination_tps3890.md)
has an 8.148276 ms charge-only minimum, so the existing 100 nF cannot
inherit the previous startup argument. Input-ramp offset, warm restart,
reference reset, output overshoot, MCU domain sequencing and reset release
must be resolved together. A longer main reset delay alone does not prove
MIPI rise gradient or safe power collapse.

The 30 uVrms headline is measured at 0.6 V under particular conditions,
not a guaranteed 1.8 V result. Reference noise scales with output gain
without feedforward filtering. The 120 Hz PSRR row does not establish
rejection of U13's switching spectrum. No required PHY ripple spectrum or
board PDN acceptance is established by the MCU's DC voltage range.

Keep the existing 20 mA input allocation. The script reports a conservative
10.192593 mA alternative planning screen using the 4 mA ground-current
maximum row at 100 mA plus explicit auxiliary allowances; it does not
interpolate a guaranteed maximum at this branch's smaller load or changed
input voltage. Thermal screens similarly use this allocation and ADI's
test-board thermal values, not sealed-enclosure qualification. No guaranteed
battery-life gain is inferred from no-load IQ or conservative allocations.

Next integration gate: establish startup/restart and PHY ripple limits,
choose and source REF/BYP/feedforward parts, create/verify the nine-pad native
asset, then migrate U23/C110/R95 connections and verify the full netlist/BOM,
ERC and every PDF page. C108/C109/R94/C111 and unrelated nets must be
preserved unless an explicit electrical change is justified. If reliable
timing needs another monitor, compare its total cost/power with retaining
LT3042 before claiming a saving.

## Sources and reproduction

- [TI TPS7A20 SBVS338H](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), absolute maxima and reverse-current section; [exact status](https://www.ti.com/product/TPS7A20/part-details/TPS7A2018PDBVR), [offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A2018PDBVR/13566855).
- [TI TPS731 SBVS034P, April 2026](https://www.ti.com/lit/ds/symlink/tps731.pdf), sections 5.5/6.3.3/6.3.4; [exact status](https://www.ti.com/product/TPS731/part-details/TPS73118DBVR), [offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS73118DBVR/1672846). New/legacy silicon distinctions are retained.
- [TI TPS709 SBVS186H](https://www.ti.com/lit/ds/symlink/tps709.pdf), reverse protection conditions; [product](https://www.ti.com/product/TPS709), [indexed offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS70918DBVR/3903337).
- [ADI LT3008 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/3008fc.pdf), [status](https://www.analog.com/en/products/lt3008.html), [offer](https://www.digikey.com/en/products/detail/analog-devices-inc/LT3008EDC-1-8-TRMPBF/2074406).
- [ADI LT3060 Rev D](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3060.pdf), pages 2/4-6/15-21; [status](https://www.analog.com/en/products/lt3060.html), [E-grade CT offer](https://www.digikey.com/en/products/detail/analog-devices-inc/LT3060EDC-1-8-TRMPBF/2355153), [historical I-grade TR offer](https://www.digikey.co.uk/en/products/detail/analog-devices-inc/LT3060IDC-1-8-TRMPBF/2355773), [Mouser nonstocked I-grade](https://au.mouser.com/ProductDetail/Analog-Devices/LT3060IDC-18TRMPBF?qs=hVkxg5c3xu%252BECJviPobcNQ%3D%3D).
- [Renesas RA8P1 datasheet](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet), Rev 1.30, used from the owner firmware reference checkout.

Run `python scripts/check_mipi_ldo_selection.py <fresh-kicadxml-export>`.
It binds the screen to the installed parts and connections and performs
arithmetic only. It explicitly retains startup, noise, retention and thermal
HOLD. The script is not a simulation, a hardware test or purchasing approval.

Checkpoint verification: the native editor adds only the visible review note
on supply page 4; save also regenerates the audio document UUID. Complete
pin-to-net partitions and all 305 included references/19 BOM fields are
unchanged. All fifteen PDF pages were rendered and inspected; fourteen match
the prior checkpoint pixel for pixel. Poppler independently renders the
changed page. Fresh ERC retains 103 errors/15 warnings and the four existing
ignored checks, with no new suppression. Clock, camera and this inventory/
arithmetic screen pass. The schematic remains WIP.
