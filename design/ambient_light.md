# Ambient-light integration

## ALS-001: native symbol checkpoint, 2026-10-04

Created `Sensors:OPT4001DTSR` through the native Symbol Editor. This initial
symbol-only checkpoint preceded the native circuit integration below.
The existing LIS2DTW12TR orientation circuit is unchanged.
Authority: [TI SBOS993A Rev A, Table 6-2](https://www.ti.com/lit/ds/symlink/opt4001.pdf).

| DTS pin | Name | Electrical type |
| --- | --- | --- |
| 1 | VDD | Power input |
| 2 | ADDR | Input |
| 3 | NC | Unconnected |
| 4 | GND | Power input |
| 5 | SCL | Input |
| 6 | NC | Unconnected |
| 7 | INT | Bidirectional |
| 8 | SDA | Bidirectional |

The eight-pin DTS ordering code is distinct from the four-pin YMN variant.
Pin 7 supports open-drain output and hardware-trigger input. Proposed polling
keeps INT_DIR=1 and a 10k pullup, without allocating another MCU interrupt.
Proposed ADDR-to-ground selects 0x44; local bypass is 100nF.
These are integration decisions pending native wiring and validation.

[DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/OPT4001DTSR/17748298)
showed 346 available in cut tape, USD1.68 at quantity one, unreserved.
Native hidden fields record the exact manufacturer and supplier codes.

Next: connect the common +3V3_MCU rail and IIC0_A bus; reuse the existing
4.7k pullups only after revising the bus inventory. The prior 60pF allocation
is not permission to add sensor capacitance. Bound leakage, edge timing,
startup and shutdown backfeed before acceptance. A 100uA supply planning
allowance is a design reserve, not a guaranteed datasheet maximum.

Use a sealed optical window and isolate the sensor optically from the
frontlight and both camera lights. Window transmission, angular response,
condensation and calibration remain enclosure-dependent qualification work.
No footprint, model, PCB or production acceptance is included.

## ALS-002/003: native integration checkpoint, 2026-10-04

Placed and wired U32 through KiCad. VDD pin 1 uses +3V3_MCU; ADDR pin 2
and GND pin 4 use GND. SCL pin 5 and SDA pin 8 join /SENS_SCL and /SENS_SDA,
respectively, retaining host balls K13 and R16 and the existing R102/R103
4.7k pullups. NC pins 3 and 6 remain unconnected per the device pin map.
No second bus pullup pair was added.

R112 is a 10k YAGEO RC0603FR-0710KL pullup from INT pin 7 to +3V3_MCU.
It follows Table 6-2; polling requires INT_DIR=1, including after register
configuration. No MCU interrupt is allocated. C124 is the 100nF local
VDD-to-GND bypass recommended in section 9.4, with sourced candidate
Murata GRM188R72A104KA35D. Passive source snapshots are inherited dated,
unreserved evidence; recheck before ordering. Effective capacitance,
leakage, temperature, aging and physical placement remain unqualified.

Read-only KiCad XML audit found 299 components. All 296 previous complete
component records and their pin-to-net memberships were preserved against
the service-discharge checkpoint. The three additions are U32, C124 and
R112. Native ERC remains 100 errors and 11 warnings; this is a WIP result,
not electrical acceptance or a clean ERC claim.

### Expanded shared-bus allocation fails the existing Fast-mode screen

`scripts/check_ambient_light.py` audits the exported topology and reproduces
the following conditional arithmetic. These are engineering allocations,
not measured or guaranteed installed limits:

- Existing 60pF ceiling plus provisional 10pF sensor/route reserve = 70pF.
  TI's 3pF typical pin capacitance is not a guaranteed maximum.
- Existing 15uA leakage allocation plus provisional 2uA reserve = 17uA.
  This is not a full-temperature OPT4001 leakage guarantee.
- Existing R102/R103 envelope: 4376.147..5034.194 ohm, including allocated
  tolerance, temperature and service drift; rail 3.151819680..3.393012496V.
- Worst allocated rise: 318.072781ns, failing the 300ns ceiling. At 17uA,
  the corresponding capacitance ceiling is 66.022625pF.
- With 1.3us low, 0.6us high and 300ns allocated fall, 400kHz period slack
  is -18.072781ns. Bus divider/filter settings are not accepted.
- Conditional static high floor is 3.066238391V and sink ceiling is
  0.792343mA. R112's hypothetical INT-low draw is 0.346190mA and resistor
  dissipation is 1.174628mW using 1% tolerance plus 1% temperature reserve.

Next: revise the complete bus capacitance/leakage inventory and pullup/timing
choice, then qualify host and both sensor thresholds, edges, startup,
shutdown/backfeed and power-cycle behavior together. The added device does
not inherit the prior 60pF approval. The 100uA ALS supply planning reserve
also does not establish maximum supply current or aggregate rail capacity.

## ALS-004: complete saved-bus inventory and pullup comparison, 2026-10-04

The read-only exported netlist contains exactly four contacts on each line:
SCL = R102.2, U1.K13, U26.1 and U32.5; SDA = R103.2, U1.R16,
U26.4 and U32.8. Both pullups return to +3V3_MCU. U26 is the approved
LIS2DTW12TR. The audit now asserts these complete contact sets, the retained
4.7k values and the replacement part number. Adding another bus load will
require revising this inventory and the conditional allocation.

Compared lower nominal pullups using the same 1% initial, 1% temperature
and 5% service-drift allocations. Slow edges use 70pF, 17uA leakage sinking
and the minimum rail; fast edges use 25pF, 17uA injection and the maximum
rail. These allocations remain unqualified. The timing screen follows
[RA8P1 Rev.1.30 Table 2.66](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet)
and [OPT4001 SBOS993A](https://www.ti.com/lit/ds/symlink/opt4001.pdf).

| Uninstalled nominal pullup | Conditional rise range | Sink ceiling | 400kHz period slack |
| --- | --- | --- | --- |
| 3.9k | 73.904..261.023ns | 0.951387mA | 38.977ns |
| 3.3k | 62.912..219.056ns | 1.121276mA | 80.944ns |
| 2.7k | 51.788..177.773ns | 1.366670mA | 122.227ns |
| 2.2k | 42.413..143.880ns | 1.673414mA | 156.120ns |

3.3k is the next candidate for sourcing and native installation: it provides
more conditional margin than 3.9k while retaining lower sink current than
2.7k or 2.2k. No pullup was changed in this checkpoint. The table is a
lumped planning comparison, not permission to operate the current circuit
at 400kHz. Divider/filter settings, fall time, full-temperature device limits,
actual board capacitance, supply sequencing and future bus loads still need
qualification. Preserve the failed installed 4.7k screen until native
replacement and its saved-netlist verification are complete.

## ALS-005: native 3.3k shared-bus pullups, 2026-10-04

Changed R102/R103 in native KiCad to YAGEO RC0603FR-073K3L, 3.3k,
1%, +/-100ppm/C, 0603, 0.1W at 70C, -55..155C. The
[manufacturer ordering-code sheet](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-073K3L)
confirms these ratings. Native fields include the exact MPN, manufacturer
document, supplier code/URL, selection basis and dated availability snapshot.
[DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0603FR-073K3L/730073)
showed Active status, 622,536 unreserved in stock, cut-tape code
311-3.30KHRCT-ND, USD0.10 qty1 / 0.01220 qty100 and a 22-week
manufacturer lead time. Recheck before ordering. Footprints remain deferred.

Under the ALS-004 allocations, the installed pair has a resistance envelope
of 3072.6135..3534.6465 ohm. Conditional rise is 62.912..219.056ns,
sink ceiling 1.121276mA, and the minimum-pulse 400kHz period screen has
80.944ns slack. This closes the failed *planning calculation* for the
previous 4.7k pair; it does not qualify operation at 400kHz. The script
retains that historical 318.072781ns failure separately.

The complete saved bus inventory remains the exact ALS-004 contact sets.
Read-only comparison against the 299-component ALS checkpoint permits
only R102/R103 value and source-metadata changes, preserving their other
identity fields, all 297 other complete component records and every contact
membership. The native circuit and both notes now show the installed values.
No new components or wires were added by this pullup checkpoint.

Remaining acceptance work: bound installed capacitance and leakage across
temperature and service conditions; verify RA8P1 IIC clock/divider/filter
timing and both sensors' edge/threshold limits; evaluate startup, supply
collapse, backfeed and recovery. OPT4001 optical-window transmission,
frontlight/camera-light isolation, condensation and calibration remain open.
The resistor environmental rating does not qualify enclosure water resistance.

Verification: both sensor calculation/topology scripts pass against the saved
XML; the native ERC findings are identical to ALS-003 (100 errors, 11 warnings).
The full 14-page PDF was refreshed: pages 1-13 are pixel-identical to the
preceding reviewed export, and page 14 was rendered and inspected for the
new values and notes. Native CLI BOM export retains the project-configured
19 columns and has 121 groups / 296 included references; TP1-TP3 remain
explicitly excluded copper testpoints. All included values, manufacturer
names/MPNs and DigiKey codes match the saved XML. Clock calculation checks
and `git diff --check` pass. This remains a WIP electrical design.

## ALS-006: host divider and recovery screen, 2026-10-04

Reviewed [RA8P1 HUM R01UH1064EJ0130 Rev1.30](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware),
chapter 40. Pages 2384 and 2386 define IICphi = PCLKB / 2^CKS and
NF=01 as two filter stages. Page 2402 equation (5) applies with SCLE=1,
NFE=1 and nonzero CKS. BRH/BRL must each be at least nf+1; reserved
register bits 7:5 must be written as ones. Keep FMPE=0 for Fast-mode.

`scripts/check_sensor_iic_clock.py` screens a provisional PCLKB=50MHz
+/-1% allocation with CKS=001, NF=01, BRH=23 and BRL=31 (register
writes 0xF7 and 0xFF). These are candidate settings, not firmware changes
or an approved system clock configuration. The current crystal circuit
does not establish this PCLKB range. The script computes high/low pulse
minima and maximum rate with zero fall time as a conservative rate bound;
zero fall time is not an accepted electrical edge. It also demonstrates
why the manual's illustrative 400kbps tuple is not a corner-qualified
setting for this bus. Stretching can further reduce the transfer rate.

Recovery must respect sections 40.12.2-40.12.3, pages 2448-2449. CLO
outputs one extra SCL cycle per request and must clear before another
request. Use it only for lost synchronization, monitor SDAI, and issue
STOP after the slave releases SDA. CLO cannot recover a slave holding
SCL low. Both module reset forms release the MCU outputs; neither proves
that a sensor has reset or released its own output. Clear IICRST afterward.
The whole-bus power-cycle/discharge path remains an electrical dependency.

Still open: derive PCLKB and its tolerance from the complete PLL/clock
plan, verify sensor and host setup/hold plus START/STOP and bus-free timing,
select SDA delay from guaranteed limits, bound physical edges/leakage,
and qualify interrupted-transfer recovery. Do not mark ALS or U26 fully
qualified from this divider screen. No schematic, BOM or firmware changed
in ALS-006; the existing full PDF remains the current circuit view.
