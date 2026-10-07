# BQ25798 PD charger candidate qualification

2026-10-05. **HOLD: unplaced library candidate, not a selected charger circuit.**
This follows the owner's lifecycle, quantity-one, suitability and price audit.
It supersedes using the historical BQ25616 circuit directly on negotiated PD.
The complete source architecture remains in [Stage 5](audio_power_study.md).

## Sourcing and value

[TI's exact BQ25798RQMR listing](https://www.ti.com/product/BQ25798/part-details/BQ25798RQMR)
is Active. TI's store is out of stock; that is not an EOL declaration.
[DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/BQ25798RQMR/15666783)
lists 7,394, $5.90 at quantity one, cut tape code 296-BQ25798RQMRCT-ND.
The factory reel contains 3,000; the prototype does not require buying it.
Avoid the optional $7 reeling fee. These are unreserved October 5 snapshots,
excluding freight/taxes/tariffs, and must be rechecked before purchase.
No published remaining-life guarantee was established.

Integrated buck-boost conversion, input sensing and a supported TI PD charger
family justify studying this $5.90 device. MPPT and backup features are not
requirements and do not justify its selection by themselves. Compare total
inductor, capacitor, protection, isolation and configuration BOM, efficiency
and fault behavior before choosing it. A charger does not improve sound by
brand or price; its noise, power loss and system behavior matter.

## Electrical limits and native pin review

Authority is [TI SLUSDV2C Rev C, June 2026](https://www.ti.com/lit/ds/symlink/bq25798.pdf),
especially sections 5, 6.3-6.5, 7.3.2, 7.3.8, 7.3.12 and the register tables.
The reviewed package is 29-pin RQM, 4 x 4 mm. Input operation is 3.6-24 V;
30 V is an absolute maximum, not an operating target. Recommended limits
include 3.3 A input, 5 A switch/charge current and 6 A continuous BAT discharge
(10 A for at most one second). None grants USB input permission or approves
that current for the battery, inductor, PCB or sealed enclosure.
The 44.2 C/W datasheet junction-to-ambient figure is a test-board result.

The native project symbol was copied from KiCad's Battery_Management:BQ25798,
then edited through the native pin table and symbol properties. All physical
pins 1-29 are visible exactly once; there is no invented pad 30. All legs are
150 mil, text 50 mil, body outline 10 mil, endpoints/rows 100 mil grid.
Footprint is blank. Upstream license and exception are retained in
`libs/symbols/KICAD_LIBRARY_LICENSE.md`.

| Pin(s) | Name | Circuit constraints for later integration |
| --- | --- | --- |
| 1 | STAT | Open-drain charge/fault indication; qualified pull-up domain required. |
| 2, 3 | VBUS | Both contacts on the same protected charger input; local bypass. |
| 4, 19 | BTST1, BTST2 | Bootstrap capacitors to SW1/SW2 respectively; reference uses 47 nF, at least 10 V. |
| 5 | REGN | Internal bias supply, local 4.7 uF; not the product always-on rail. |
| 6, 7 | D+, D- | Charger source detection, not USB audio data. Keep separate from RA8P1 data and disable automatic detection in a qualified configuration. |
| 8, 9 | VAC2, VAC1 | Input detection; tie to VBUS where the respective external input FET pair is absent, per TI. |
| 10, 11 | ACDRV2, ACDRV1 | Input FET gate drive; ground when the respective FET pair is absent. |
| 12 | QON | Active-low wake/reset input; internal pull-up can exceed 3.3 V. Do not directly join the existing key/control domain without checking limits. |
| 13 | CE | Active-low charge enable; never floating. Hardware defaults must inhibit unqualified charging. |
| 14, 15 | SCL, SDA | Configuration bus; resolve independent startup controller, voltage and reset ownership. |
| 16 | TS | REGN-referenced pack-temperature network, tolerance/open/short analysis required. |
| 17 | ILIM_HIZ | Analog current limit/HIZ, lower of analog and register limits; never tie to REGN merely to get maximum current. |
| 18 | BATP | Pack-positive sense through TI's recommended 100 ohm path; isolation must preserve valid sensing. |
| 20 | PROG | Resistor-defined cell count and frequency at POR. |
| 21 | INT | Open-drain interrupt; independent fault response cannot depend solely on the application. |
| 22, 23 | BAT | Both contacts on the same bidirectional battery power node. |
| 24 | SDRV | Ship-FET control; cannot provide sustained attached-adapter battery isolation. Rev C requires 1 nF/50 V to ground without SFET; do not reuse the removed BAT-tie option. |
| 25 | SYS | NVDC system output; do not assume a fixed 3.3 V supply. |
| 26, 28 | SW2, SW1 | Switching nodes; passive symbol abstraction, external loop/inductor/layout qualification required. |
| 27 | GND | Ground contact. |
| 29 | PMID | Power node, not a grounded exposed pad. |

VBUS 2 is modeled power input and 3 passive; BAT 22 power output and 23
passive, preserving separate visible contacts without duplicate power-driver
conflicts. BAT is physically bidirectional, including discharge. These types
are ERC abstractions, not proof of reverse isolation, startup or power flow.
No arbitrary power flags should be introduced for the switched nodes.
Rev C minimum effective capacitances are VBUS 2 uF, SYS 6 uF, BAT 3 uF and
PMID 4 uF without backup (70 uF with backup). Reference nominal capacitor
banks are not DC-bias/temperature/aging qualification.

## Reset, pack and temperature gates

The retained [Jauch LP906090JH pack specification](https://www.jauch.com/downloadfile/677e3f68c583d30f0e3fd6874fe248710/matd_246525_lp906090jh.pdf)
is Rev 1.1, August 2024: protected 1S, 3.7 V/6 Ah, 4.2 V charging,
1.2 A standard/3 A maximum charge, 6 A discharge, 0-45 C charging.
Its protection thresholds are fault backups, not operating setpoints or a
6 A load limiter. The pack has no supplied NTC; an insulated surface sensor
and attachment/thermal-lag analysis are required without modifying the pack.

For 1S, PROG uses 3.0 kohm at 1.5 MHz or 4.7 kohm at 750 kHz, with TI's
resistance tolerance. Defaults are 1 A charge, 3.5 V VSYSMIN and 4.2 V VREG.
Changing CELL resets cell-dependent parameters. Incorrect cell configuration
can overvoltage the existing 5.5 V maximum U13 input. The hardware must
bound that low-voltage bus independently of a software register assumption.

At TI's specified 4.2 V test point, the 1S regulation upper error is +0.95%
over the cited temperature range: 4.2399 V. The pack's permissible normal
charge-voltage tolerance has not been established, so the default cannot
be accepted merely because both documents print 4.2 V. The intended reduced
4.10 V target needs a guaranteed error limit at that setting. Applying the
same percentage gives 4.13895 V as arithmetic only, not a guaranteed limit.

Rev C section 7.3.2 says watchdog/reset returns VREG to the cell default,
whereas the VREG register table lists REG_RST reset only. Treat this conflict
conservatively pending manufacturer clarification and reset tests. EN_CHG
defaults enabled, AUTO_INDET_EN defaults enabled and watchdog defaults 40 s.
Do not assume a programmed lower charge voltage or disabled data-pin detector
survives every reset. A normally inhibited CE gate needs independent valid
configuration/temperature permission; disabling watchdog alone is insufficient.

[TI's TPS25751 support response](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1486218/usb-pd-chg-evm-01-usb-pd-chg-evm-01-battery-charger-register-values)
states that the PD controller does not configure charger NTC register 18h.
Its autonomous charger feature is not a general register initialization engine.
Qualify TS limits/tolerances and open/short faults for the pack's 0-45 C window.
Configuration and charging must remain safe with the main processor off,
depleted/absent pack, corrupt configuration, I2C loss and independent resets.

## Full-battery desktop isolation: negative result

Disabling charge does not disconnect BAT from SYS. During source overload,
NVDC intentionally lets the battery supplement SYS. Rev C SDRV modes do not
solve the owner's attached-host isolation requirement: shutdown is ignored
with an adapter present, ship requires no adapter and adapter insertion wakes
it, and system reset disconnects only temporarily before returning to idle.
Do not describe CE or the ship FET as a sustained desktop battery disconnect.

P1 therefore requires a separately qualified reverse-blocking battery branch
and external digital preregulator/source mux, alongside external analog power.
The charger can remain on a distinct controlled charge branch. This is an
architecture requirement, not permission to open BAT/BATP arbitrarily: examine
sensing, termination, reverse currents, dead-pack start and source transfer.
If this topology cannot provide safe independent charge/isolation behavior,
reject BQ25798 and compare a separate charger/system-power architecture.

Port current must cover every parallel branch. Charger IINDPM alone cannot
limit analog converters bypassing it. Enforce the aggregate source contract,
shed charging first, then reduce amplifier capability. Full-battery external
playback must demonstrate no repeated net battery cycling. Weak hosts are
allowed reduced output; no hidden battery boost to preserve a desktop rating.

## Alternatives and closure sequence

- [BQ25672](https://www.ti.com/lit/ds/symlink/bq25672.pdf): integrated 3 A
  buck charger, 3.6-24 V/1-4S. Less 5 V input margin and still NVDC; not an
  isolation solution. Exact stock/cost and controller integration unverified.
- [BQ25756](https://www.ti.com/product/BQ25756): Active external-FET charger,
  4.2-70 V/1-14S, resistor/autonomous plus I2C controls. Worth comparing if
  BQ25798 default behavior fails. More area/FET/BOM/thermal work; exact
  quantity-one sourcing and complete startup behavior not yet qualified.
- Historical BQ25616 has useful resistor-set lower-voltage charging work,
  but cannot accept raw 15/20 V PD. A preregulated implementation needs a
  new complete system cost/efficiency/isolation comparison.

Next: resolve released reset semantics and guaranteed pack voltage tolerance;
define independent configuration/CE/temperature interlocks; qualify digital
source mux and charge branch; calculate total power/current/thermal corners;
select inductor/capacitors and exact PD/wet-path parts; only then place and
wire the circuit. [TIDA-050047](https://www.ti.com/lit/ug/tiduey1/tiduey1.pdf)
is useful integration evidence but its 2-4S reference does not qualify this
1S pack or wet-port startup. No component purchase or schematic release is
approved by this candidate checkpoint.
