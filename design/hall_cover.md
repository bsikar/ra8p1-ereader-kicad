# Magnetic cover sensor

## HALL-001: native integration checkpoint, 2026-10-04

U33 is **DRV5032FADBZR**, the FA 20 Hz omnipolar **push-pull** variant.
It detects either magnet polarity and asserts a low output when the field
exceeds its operate threshold. This implements the magnetic cover GPIO
circuit; enclosure, firmware, power sequencing and package qualification
remain open. U26 remains LIS2DTW12TR.

Manufacturer authority: [TI SLVSDC7H Rev H](https://www.ti.com/lit/ds/symlink/drv5032.pdf),
Tables 4-1 and 5-1, sections 6.3-6.6 and 8.4. The DBZ ordering code matters:
the TO-92 and X2SON versions have different pin maps.

| Contact | Saved connection | Native type |
| --- | --- | --- |
| U33.1 VCC | +3V3_MCU | Power input |
| U33.2 OUT | COVER_INT_N, U1.M12 P412 | Output |
| U33.3 GND | GND | Power input |
| C125.1 / C125.2 | +3V3_MCU / GND | Passive |

C125 is YAGEO CC0603KRX7R9BB224, 220 nF, 10%, 50 V X7R, 0603.
Place it directly beside U33 VCC1/GND3 with a short return loop. TI calls
for at least 100 nF ceramic bypass. The effective capacitance requirement
is not closed by a nominal value or a typical DC-bias curve.
[YAGEO exact-part sheet](https://yageogroup.com/download/specsheet/CC0603KRX7R9BB224)
identifies this candidate; footprint assignments remain blank pending
manufacturer package and pad review.

P412 is ball M12 in the selected BGA289 device. It supplies IRQ20-DS through
ISEL, per [RA8P1 HUM Rev 1.30](https://www.renesas.com/en/document/mah/ra8p1-group-users-manual-hardware),
Table 21.11, page 871. Configure PDR=0, PMR=0, ISEL=1 and PCR=0; keep the
input high impedance and its pull-up disabled. Do not configure an output
against the Hall push-pull driver. IRQ polarity/filtering, DSELR/ICU wake
configuration, startup masking and reading an already-closed cover state
require firmware implementation and review. This checkpoint makes no
firmware changes. P412 was unconnected before this integration.

## Conditional electrical screen

The device permits 1.65-5.5 V and -40 to +85 C. The existing conditional
MCU rail envelope is 3.151819680-3.393012496 V. TI specifies VOH >= VCC-0.35 V
at -1 mA and VOL <= 0.3 V at +1 mA. RA8P1 datasheet Rev 1.30 Table 2.5,
pages 48-49, places P412 among the VCC-powered 5 V tolerant ports with
VIH=0.8*VCC and VIL=0.2*VCC. Using independent rail extremes conservatively:

- High margin: 3.151819680 - 0.35 - 0.8*3.393012496 = 0.087409683 V.
- Low margin: 0.2*3.151819680 - 0.3 = 0.330363936 V.

These are conditional static margins, not acceptance of noise, leakage,
ground offsets or supply transients. Establish aggregate output loading
below the specified test currents across temperature and every power state.
U33 and the receiving MCU VCC domain must remain valid together. Review
power-off injection and startup/shutdown before relying on this interface.

For C125, nominal capacitance after -10% tolerance and -15% X7R temperature
change is 168.3 nF, before DC bias and aging. Combined further retention
must be at least 100/168.3 = 59.4177%. This is a loss budget, not a guaranteed
property of this part. Obtain effective-capacitance evidence at the actual
voltage, temperature and lifetime or choose a qualified alternative.

FA sampling is specified at 13.3-37 Hz (27-75 ms period). The active interval
has a 100 us maximum; first valid output after a supply ramp needs explicit
review and measurement. Do not equate active time with guaranteed startup
latency. Keep the interrupt masked until the rail and sensor state are valid.
The 3.5 uA maximum average-current entry is at VCC=3 V; it does not guarantee
the same ceiling at the 3.3 V rail corners. The 2.7 mA maximum peak entry
also needs inclusion in the rail/transient screen.

Retain +3V3_MCU during sleep for cover wake. This circuit cannot wake a
fully powered-off device with that rail removed; the existing power-button
path remains the power-off wake path. Close the sleep current budget and
actual deep-standby supply behavior before promising cover wake.

## Mechanical and water-resistant enclosure constraints

The FA absolute operate threshold spans 1.5-4.8 mT and release threshold
0.5-3 mT. Require closed-cover field magnitude above 4.8 mT and open-cover
field magnitude below 0.5 mT at the die across magnet, gap, alignment,
temperature and assembly tolerances. Include speaker and other magnets.
Hysteresis is not a substitute for those worst-case field checks.

Mount the sensor inside the sealed enclosure; no exposed contacts or
penetrations are required for magnetic detection. Determine sensor axis,
magnet position and cover gap with the actual enclosure. Water resistance,
seal materials, coating effects, condensation and environmental testing
remain enclosure/system work. This circuit does not qualify USB moisture
detection or the rest of the device for water exposure.

## Dated sourcing evidence

Unreserved distributor snapshots on 2026-10-04; recheck before purchasing:

| Part | Distributor / CT code | Listed stock | MOQ | USD qty 1 / 100 | Standard lead time |
| --- | --- | --- | --- | --- | --- |
| DRV5032FADBZR | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/DRV5032FADBZR/7400094), 296-47765-1-ND | 120185 | 1 | 0.33000 / 0.22870 | 20 weeks |
| CC0603KRX7R9BB224 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/CC0603KRX7R9BB224/5883804), 311-3374-1-ND | 111728 | 1 | 1.23 / 0.55000 | 17 weeks |

Both listings identify active parts and cut tape rather than a full-reel
minimum. Prices exclude tax and shipping. These are availability evidence,
not purchase reservations or manufacturer electrical qualification.

## Saved-design validation

Export the complete native XML netlist, then run:

```sh
python scripts/check_hall_cover.py --netlist /path/to/netlist.xml
```

Optional `--baseline` checks the 299-component pre-Hall checkpoint. It
requires all existing component records and electrical net partitions to
remain unchanged except for connecting U1.M12; new parts are U33 and C125.
The checker verifies exact part identities, pin map, cover net membership,
supply/bypass connectivity and the conditional arithmetic above. It does
not establish electrical or mechanical qualification.

Saved checkpoint results: 301 netlisted components, with all 299 baseline
component records preserved and only U1.M12 added to the new cover signal.
The native BOM has 123 groups and 298 included references (the existing
three copper test-pad references remain excluded). Native ERC is 99 errors
and 11 warnings, compared with 100 errors and 11 warnings before this work.
The sole removed finding is U1.M12 unconnected; there are no added findings.
The full 14-page PDF was rendered and visually reviewed; the other twelve
pages are pixel-identical to the preceding export. Hall, orientation,
ambient-bus, sensor clock and oscillator calculation checks pass their
stated conditional scopes. The remaining ERC findings and qualification
items prevent treating this checkpoint as a finished electrical design.
