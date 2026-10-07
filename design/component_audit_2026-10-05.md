# Component audit - 2026-10-05

The saved schematic contains **305 included physical references, 79 selected ordering codes, and two unresolved references (C9 and J1)**. All are enumerated below. Four native copper contacts, J4 and TP1-TP3, are excluded from purchases. The 26 unplaced library symbols are separately classified so historical parts cannot silently return to the BOM.

**This is not a purchase-ready or manufacturing-approved BOM.** Four sourcing/value corrections have been applied in native KiCad. Lifecycle transitions, released specifications, weak stock evidence and circuit qualification remain open where stated. Manufacturer Active/Production status means currently offered; it does not promise that a part will remain available for years. An explicit published longevity commitment is reported only where found. Newer release dates alone do not make a part better.

Research prioritizes manufacturer documents and exact order-code status, then distributor quantity-one offers. The observation date is October 5, 2026; the source-age column preserves older indexed evidence. Cached quantities are not live checkout confirmation. Prices are USD at one piece unless otherwise stated, excluding taxes, freight, tariffs and custom-reel charges. **TR in an MPN or a factory pack of 2000/10000 does not itself establish a minimum order:** distributor cut tape, tube and tray can be sold one piece at a time. Choose cut tape rather than paying a reeling fee for a prototype.

The machine-readable [audit](component_audit_2026-10-05.json) retains source links, manufacturer/distributor status, price, packaging, source age and electrical/value rationale for every row. [Native BOM](../exports/ereader_rev1_bom.csv) retains the complete selection basis for each individual reference. Existing historical sourcing fields remain historical; the audit is the newer sourcing evidence except where replacement fields were updated.

## Applied native replacements

| Reference | Previous ordering code | Current candidate | Reason and remaining gate |
| --- | --- | --- | --- |
| U14 | IS42S32160F-7TLI | AS4C16M32SC-7TIN | Old exact code has distributor Discontinued/owner-reported Mouser NRND. Alliance offers the same 64 MiB x32, industrial TSOP-86 interface, quantity-one tray. All 86 package pins and every existing net membership were preserved. Public September 2018 Rev 1.0 is **PRELIMINARY**: released specifications/manufacturer confirmation, startup, timing, SI, refresh, power and footprint remain HOLD. This replacement removes reliance on the old source but is not yet a fully qualified production choice. |
| R33 | RT0603BRD07100KL | TNPW0603100KBEEA | Old selected distributor stock unavailable. Preserves 100 kohm, 0.1%, 25 ppm/K, 0603 source-supervisor divider; $0.26 quantity-one CT, 65,460 listed. Existing 3.263705831..3.476597632 V source-trip calculation is unchanged. |
| C95 | C1608C0G1H103J080AA | GRM1885C1H103JA01D | TDK still has production evidence but distributor stock was unavailable. Murata keeps 10 nF, 5%, C0G, 50 V, 0603 reset timing; $0.13 CT, 395,362 listed. Exact approval sheet, leakage, placement and startup qualification remain open. The linked manufacturer typical-spec summary is not a final approved specification. |
| C125 | CC0603KRX7R9BB224 | C1608X7R1H224K080AB | Hall bypass keeps 220 nF, 10%, X7R, 50 V, 0603 and consolidates with 12 existing references. Quantity-one price falls from $1.23 to $0.17. Effective capacitance must still exceed the Hall sensor's 100 nF requirement under bias, temperature and aging. |

Replacement source links are in the individual entries below. No wiring or value changes were necessary for these four substitutions. Old library assets remain archived for provenance; they are not approved alternatives.

## Additional native electrical correction

SERVICE-025 changes R110/R111 from 10k to 1k, using an existing active
quantity-one USD 0.10 BOM MPN. The parallel discharge improves the conditional
60 uA off-state screen from 306.03 mV to 30.603 mV; fixture loading rises
to 7.071 mA maximum. See [service review](service_interface.md#service-025-stronger-native-fixture-rail-discharge-2026-10-05).
Actual leakage, storage and sequencing remain HOLD. The fixture contract
now requires at least 20 mA; no adapter has been qualified.

## Priority findings and engineering decisions

### Supplier refresh in this continuation

Thirty-seven source rows were refreshed after the initial audit: 36 direct
supplier retrievals dated October 5 and one last-month T521 page, whose age
remains explicit. Original quantities/prices are retained in each JSON row's
`source_history`. Native sourcing snapshots and per-reference selection
calculations remain historical; no electrical or BOM change was made during
this refresh.

- **C43/C46/C47/C73/C88/C92/C102:** DigiKey now lists 55,220 of
  C3216X7R1V106K160AC, $0.68 quantity-one cut tape. That covers the seven
  installed uses; the prior zero-stock source hold is resolved at the listing
  level. Mouser's freshly retrieved page instead lists zero, so the older
  indexed Mouser stock must not guide this purchase.
- **R42:** DigiKey now lists zero RG2012L-102-L-T05, $3.45 on backorder.
  Mouser's indexed yesterday offer lists 1,560, $3.66 quantity-one cut tape;
  direct retrieval failed. This is an explicit source hold until that exact
  offer is refreshed. Do not relax 0.01%/2 ppm/K to fix availability without
  recomputing the main rail's upper limit.
- **C115 and L1:** fresh DigiKey counts are 250 and 144, respectively, lower
  than the earlier 9,260 and 1,149. Both still cover a prototype; these counts
  do not establish reliable replenishment.
- **U1/U4 and the 74 common 100 nF capacitors:** the weak primary sources
  remain unchanged: one discontinued-at-DigiKey MCU, four radio switches,
  and four capacitors. Indexed Mouser stock for the capacitors is insufficient
  evidence of live availability for all 74 positions. Failed retrieval is
  recorded as uncertainty, not converted into zero stock or a passed check.

Alliance's [published longevity policy](https://www.alliancememory.com/about/)
states 7-10 years **from launch for many products**. It does not identify
AS4C16M32SC-7TIN's inclusion or commitment end date. Its September 2018
preliminary datasheet date is not proof of launch date, and the policy cannot
be read as another 7-10 years from today. U14's remaining-life and released
specification gates stay open.

Direct listing references are in the individual rows below. The
[Mouser R42 offer](https://www.mouser.com/en/c/passive-components/resistors/film-resistors/?resistance=1+kOhms&temperature+coefficient=2+PPM+%2F+C&tolerance=0.01+%25)
remains indexed evidence only.

### Retained engineering decisions

1. **U1 ordering-code transition:** Renesas lists both R7KA8P1KFLCAC#UC0 and #UC1 Active and recommends #UC1 as replacement. DigiKey labels #UC0 Discontinued with one piece/no backorders; older Mouser and manufacturer-aggregator quantities are not refreshed checkout stock. The #UC1 manufacturer offer found has MOQ 189, not one. Retain native #UC0 until the PCN, packing/die revision, balls, errata and distributor quantity-one #UC1 availability are established. Do not silently substitute the archived 224-ball processor. [UC0](https://www.renesas.com/en/products/ra8p1/part-details/r7ka8p1kflcac-uc0), [UC1](https://www.renesas.com/en/products/ra8p1/part-details/r7ka8p1kflcac-uc1).
2. **U14 longevity/specification and price:** Alliance's current product page and reviewed SDRAM EOL list contain no retirement of this selected SC code, but neither guarantees remaining lifetime. Its manufacturer-linked ShopMemory page shows $19.20 at qty 1..107, with stock not established; DigiKey lists $43.60 and 175. Older Mouser evidence was $32.99/29 pieces and could not be refreshed. Confirm the authorized primary offer before paying the premium. A newer AS4C16M32SB-6BCN alternative changes to commercial BGA-90 and documents much higher self-refresh current (60 mA versus SC 5 mA), so it is not an automatic improvement for this portable device. [Alliance product](https://www.alliancememory.com/as4c16m32sc/), [EOL list](https://www.alliancememory.com/product/eol-sdram/), [manufacturer-linked store](https://www.shopmemory.com/product/as4c16m32sc-7tin/).
3. **U13 continuous-load and thermal HOLD:** The placed part is TPS63806YFFR, not archived TPS63802. TI's 2.5 A output headline is transient; its typical 5.5 A switch limit is not a continuous output rating. The incomplete 2.095 A main-rail allocation, at 3.393012496197 V, 3.2 V input and assumed 75% efficiency, requires 2.961817158 A input and dissipates 2.369453727 W in conversion. Close low-battery, hot enclosure, switch/inductor limits and the expanded camera/display/audio budget before retaining or changing the regulator. Input maximum is 5.5 V: negotiated 15/20 V PD cannot feed it directly. The earlier LTC3119 replacement was driven by the tight rail upper-voltage requirement; returning to the $24.07 part without closing that conflict is not justified. [TI TPS63806](https://www.ti.com/product/TPS63806), [current circuit study](main_regulator_tps63806.md).
4. **U23 price review:** ADI recommends LT3042 for new designs; its exact IMSE options are Production. A distributor stopping replenishment is not manufacturer EOL. The ~$9.12 MIPI LDO has no demonstrated requirement yet for its ultra-low noise. TPS7A2018PDBVR (300 mA; indexed 45,221, $0.37 qty-one CT) or TPS7A0218PYCHR (200 mA, much lower idle current, tiny DSBGA) merit evaluation. Neither is qualified for this rail's noise, sequencing, reverse behavior, enable/defaults or package. Preserve the present conservative **13 mA full-load IQ allocation**; the 2 mA nominal IQ does not justify reducing a worst-case budget. [ADI](https://www.analog.com/en/products/lt3042.html), [TI alternative](https://www.ti.com/product/TPS7A20), [quantity-one offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A2018PDBVR/13566855).
5. **U4 fragile stock:** Only four TPS22964CYZPT were listed. Cut tape avoids the reel minimum but this is a weak replenishment position. Same-family YZPR had zero immediate stock in the reviewed offer. TPS22964C2 and FPF1048BUCX are comparison candidates, not substitutes: review shutdown reverse blocking, discharge, control thresholds, sequencing and package first. Reverse blocking on the present part occurs when disabled; it is not an always-on battery power-path controller.
6. **High-count passives:** DigiKey's four C1608X7R1H104K080AA cannot cover the 74 placed uses; its quantity-one price does not fix that. Mouser indexed quantity-one stock exists but needs live refresh. The seven C3216X7R1V106K160AC now have a refreshed DigiKey stock listing of 55,220, quantity-one CT at $0.68; their primary source hold is resolved at listing level. Their electrical qualification is unchanged. The quantity-one source table preserves both offers and their ages.
7. **Precision resistors:** R41/R42 cost ~$2.18/$3.66 because the present SDRAM rail upper limit depends on their small tolerance/drift. R12/R67 with R13/R74 set a 3.019..3.113 V supervisor corner. Replacing these with generic 1% resistors purely on price would invalidate those budgets. The 0.1% 30-ohm RT parts cost the same ~$0.10 as ordinary RC parts; simplification can follow SI review without a claimed large saving. Ordinary pulls/series resistors do not require boutique parts.
8. **Audio candidate limitations:** The OPA1656 controller is not rail-to-rail input. The portable bank study now investigates +/-6 V instead of +/-5 V; full-bank typical idle is 2.568 W and a stated optimistic 32-ohm portable screen yields only ~2.01 hours from an assumed 17.76 Wh usable pack. This is a serious portable heat/runtime concern, not evidence that more expensive op-amps solve it. Keep the quiet path separate and the bank off during quiet listening. Composite stability, hot SOA, sharing, protection and sealed-enclosure continuous power remain HOLD. [Rail correction](audio_composite_rails.md).
9. **Environmental constraints:** EVQP7 buttons are -20..70 C and unsealed, the Pcam FFC/socket is not an ingress barrier, and ordinary USB/SD/audio connectors need enclosure/seal integration. ESD441 is not moisture sensing and its 5.5 V standoff cannot protect a 15/20 V PD power line. Wet-port inhibition and independent headphone DC/fault disconnect remain unfinished hardware.

## Electrical and value review by reference

Every selected ordering code below has a sourcing, lifecycle and fit/value entry. Grouped rows cover all listed references; their individual native Selection_Basis remains authoritative for differing uses of the same resistor or capacitor. The reviews screen suitability but do not claim completed tests.

- X7R MLCCs: nominal capacitance alone is insufficient. Preserve voltage, temperature, tolerance, DC-bias/aging, effective capacitance, inrush, ESR/loop stability and package-height requirements. C0G crystal/timer/SET capacitors are not interchangeable with X7R based on nominal value.
- R76: the 2.21 kohm microSD limiter study produces conditional 0.38/0.50/0.62 A limits; verify inrush, card load and switch fault SOA. R82 is the 330-ohm card discharge. R83-R88 are 33-ohm SD series values pending SI; R43 zero-ohm CLK is a tuning placeholder, not a terminated bus.
- R102/R103: 3.3 kohm I2C pulls produce conditional 62.9..219 ns rise times and ~1.12 mA sink demand. Bus capacitance, pins, partial-power leakage and clock settings remain gates. Other pulls retain their per-reference rise/fall/leakage and truth-table budgets.
- R31/R39/R40: 2512 nominal 1 W is not a hot-enclosure pulse/fault rating. R95 18 kohm 0.1%/25 ppm sets the MIPI rail screen at 1.754..1.846 V. Main-rail divider R41/R42/R66 remains nominal 3.272 V with maximum 3.393 V under the stated tolerances.
- L1: 2.2 uH, 37/40.7 milliohm typical/maximum DCR at 25 C; typical 7 A at 30% inductance drop and 4.6 A at 40 C rise are different limits, not guaranteed hot operation. L2: 0.47 uH, 3.7/4.3 milliohm typical/maximum DCR; 6.4 A at 10% drop is not the 15.7 A 30% drop rating. Verify hot ripple/saturation/copper loss and loop behavior.
- T491 reservoir capacitors retain the existing conditional 641.52 uF minimum bank budget; MnO2 surge/short behavior, leakage, ESR and charge limits need closure before considering polymer substitutes. Quiet T521 capacitors require correct negative-rail polarity, reverse-voltage limits, ripple and regulator stability; the listed 43-week factory lead time is a replenishment risk despite distributor stock.
- ESP32-C6 is retained as radio, not the USB audio/player processor. It lacks Classic Bluetooth A2DP and its native USB serial interface is not a high-speed UAC2 engine. LIS2DTW12 is an orientation accelerometer plus temperature, not a six-axis gyro IMU. These are role limitations, not reasons to discard working requirements blindly.

## Complete placed-part source screen

CT means cut tape; qty-one tray/tube is also acceptable. All circuit and footprint release gates remain open unless a particular completed check is named. Source ages below refer to the page evidence, not an inventory reservation.


### 1. UNSELECTED - C9

Manufacturer lifecycle evidence: UNSELECTED.

Sourcing: **DigiKey; listed stock UNVERIFIED; UNVERIFIED/1; UNVERIFIED; UNVERIFIED.** Source age: UNVERIFIED.

Role and existing limits: Candidate: Murata GRM32ER71A476KE15K, 47uF +/-10%, 10V X7R 1210. Murata GRM32ER71A476KE15-04CA (2025-01-10). HOLD pending DC-bias/aging and RA8P1 core-loop qualification; see design/core_bulk_c9.md.

Fit/qualification screen: Core47uFcandidate MurataGRM32ER71A476KE15K not selected; effectiveC/bias/aging/loop HOLD. Price/alternative review: No selected price; not purchasable.



### 2. 1-1734248-5 - J3

Manufacturer lifecycle evidence: TE drawing; distributor Active, manufacturer horizon unconfirmed.

Sourcing: **DigiKey; listed stock 22,650; $1.49/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: CMS-014: matches Digilent Zybo Z7 D.1 J2 and Pcam 5C pinout. Wurth 686715100001 cable maps host n to module n; 15 contacts, 1mm pitch, 0.30mm flex. Footprint qualification deferred. See ../design/camera_storage_interfaces.md.

Fit/qualification screen: Pcam cable/pinout15x1mm0.30mm matches; -20..85C SI/mating HOLD. Price/alternative review: $1.49 reasonable; alternate must match contact side.

Sources: [Manufacturer evidence](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=1734248&DocType=Customer+Drawing&PartCntxt=1-1734248-5), [DigiKey offer](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/1-1734248-5/2272380).



### 3. 74LVC1G14GW,125 - U12

Manufacturer lifecycle evidence: Nexperia current product; DigiKey Active.

Sourcing: **DigiKey; listed stock 265,269; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SYS-007 / PWR-004: 2.7..4.6V held-domain inverter; 1uA input leakage. Four 1k/1M gate branches include future USB clear: peak <=18.773595mA, steady <=22.773595uA, VGS>=2.596278V. Local100n bypass; shared10ms settling and500uA non-rail-input current allocation require qualification. See ../design/main_regulator_ltc3119.md.

Fit/qualification screen: Schmitt held-domain inverter; sub1.65V/ramp/leak HOLD. Price/alternative review: $0.10; no price issue.

Sources: [Manufacturer evidence](https://www.nexperia.com/product/74LVC1G14GW), [DigiKey offer](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74LVC1G14GW-125/946729), [Specification reference](https://assets.nexperia.com/documents/data-sheet/74LVC1G14.pdf).



### 4. 74LVC1G17GW,125 - U16

Manufacturer lifecycle evidence: Nexperia current product; DigiKey Active.

Sourcing: **DigiKey; listed stock 28,878; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: PWR-006: SYS_AON raw-powered EN buffer with partial-power-down Ioff. Separate held-domain Q3 clamp covers undefined sub-1.65V supply behavior. Full EN calculations: design/main_regulator_tps63806.md.

Fit/qualification screen: Ioff ENbuffer; held Q3 handles raw sub1.65V undefined behavior. Price/alternative review: $0.10; no price issue.

Sources: [Manufacturer evidence](https://www.nexperia.com/product/74LVC1G17GW), [DigiKey offer](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74LVC1G17GW-125/1965408), [Specification reference](https://assets.nexperia.com/documents/data-sheet/74LVC1G17.pdf).



### 5. ABS07-LR-32.768KHZ-6-1-T - Y2

Manufacturer lifecycle evidence: Abracon current datasheet; DigiKey Active; exact horizon unconfirmed.

Sourcing: **DigiKey; listed stock 8,268; $1.48/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: CL6pF +/-10ppm; ESR50kohm max at25C; drive0.5uW max; CLK-002

Fit/qualification screen: 6pF50kohm0.5uW RTC; boardstartup/stray HOLD. Price/alternative review: $1.48 justified lowESR10ppm;12.5pFarchive not substitute.

Sources: [Manufacturer evidence](https://abracon.com/Resonators/ABS07-LR.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/abracon-llc/ABS07-LR-32-768KHZ-6-1-T/5231514).



### 6. BLM18PG121SN1D - FB1

Manufacturer lifecycle evidence: Murata family specification; DigiKey Active; exact mfr lifecycle unconfirmed.

Sourcing: **DigiKey; listed stock 523,412; $0.14/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: USB-004: 120 ohm +/-25% at 100MHz; DCR max 0.05 ohm initial/0.10 after testing; rated 2A at 85C, 1A at 125C.

Fit/qualification screen: USBlocal filter2A85C/1A125C; bias/resonance/drop HOLD; notPDwholeinput. Price/alternative review: $0.14 reasonable.

Sources: [Manufacturer evidence](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA0003_PDF_FERRITEBEADINDUCTORTYPEFILTER), [DigiKey offer](https://www.digikey.com/en/products/detail/murata-electronics/BLM18PG121SN1D/584248).



### 7. C1005NP01H040C050BA - C37 C38

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 7,245; $0.11/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: 4pF +/-0.25pF NP0 50V; RTC initial matching; CLK-002; stray unmeasured

Fit/qualification screen: StableC0G/NP0timing/filter/crystal;leak/tolerance/stray/startup HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1005NP01H040C050BA), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C1005NP01H040C050BA/3955443).



### 8. C1005NP01H080D050BA - C35 C36

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 73,246; $0.11/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: 8pF +/-0.5pF, 50V NP0, 0402. Initial load network per RA8P1 Group10; 8pF/2 + estimated 2pF stray = 6pF. Board matching required.

Fit/qualification screen: StableC0G/NP0timing/filter/crystal;leak/tolerance/stray/startup HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1005NP01H080D050BA), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C1005NP01H080D050BA/3951017).



### 9. GRM1885C1H103JA01D - C95

Manufacturer lifecycle evidence: Murata base InProduction SimSurfing; exactDpacking distributorActive; no future guarantee.

Sourcing: **DigiKey; listed stock 395,362; $0.13/1; Qty1 cut tape; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: RST-002 value/tolerance/TC unchanged; oldTDKproduction butzeroDK/Mouserstock.

Fit/qualification screen: 10nF5%C0G30ppm/C50V0603 keeps reset timercorners; CTleakage/startup and exactapprovalsheet/footprint HOLD. Linked2015Murata typicalspecsummary is not finalapprovedspec. Price/alternative review: $0.13 practicalreplacementzero-stockTDK;stableC0Grequired notcheapX7R.

Sources: [Manufacturer evidence](https://ds.murata.co.jp/simsurfing/mlcc.html?partnumbers=%5B%22GRM1885C1H103JA01%22%5D), [DigiKey offer](https://www.digikey.com/en/products/detail/murata-electronics/GRM1885C1H103JA01D/4421555), [Specification reference](https://www.farnell.com/datasheets/2048016.pdf).



### 10. C1608NP01H102J080AA - C52 C68

Manufacturer lifecycle evidence: TDK Meister 2025.12 primary indexed exact code Production; live page unavailable.

Sourcing: **DigiKey; listed stock 26,851; $0.22/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: RADIO-012: U6 CT-to-GND, 1nF NP0 50V +/-5%, +/-30ppm/C. Nominal delay = C*1.23V/1.15uA + 25us. Charge-time corner screen includes capacitor tolerance, 100C excursion and allocated 10nA leakage; full sequencing remains open.

Fit/qualification screen: StableC0G/NP0timing/filter/crystal;leak/tolerance/stray/startup HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608NP01H102J080AA), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C1608NP01H102J080AA/3955721).



### 11. C1608X7R1H103K080AA - C41

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 615,640; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: Renesas QDG Table 1 p.6: 10 nF ceramic at U1.H15. 50 V X7R +/-10%; initial 9..11 nF. USB-003.

Fit/qualification screen: X7Rbypass; effectiveCunderbias/temp/aging,ESR/startup/inrush/loop HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H103K080AA), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C1608X7R1H103K080AA/567691).



### 12. C1608X7R1H104K080AA - C6 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C30 C31 C32 C33 C34 C39 C40 C44 C45 C48 C49 C50 C51 C53 C54 C55 C56 C58 C59 C60 C61 C62 C67 C72 C76 C77 C78 C79 C80 C81 C82 C83 C84 C85 C86 C87 C89 C90 C91 C93 C97 C98 C101 C104 C105 C106 C107 C111 C112 C113 C114 C116 C119 C120 C121 C122 C123 C126 C127

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 4; $0.11/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: 100 nF +/-10%, 50 V X7R. +3V3_MCU bypass. TDK nominal DC-bias curve: interpolated 99.45 nF at 3.3 V; reference data, not guaranteed minimum. See PWR-001 design/power_decoupling.md.

Fit/qualification screen: X7Rbypass; effectiveCunderbias/temp/aging,ESR/startup/inrush/loop HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H104K080AA), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk-corporation/C1608X7R1H104K080AA/513811).

Alternate sourcing evidence: [Mouser](https://www.mouser.com/en/ProductDetail/TDK/C1608X7R1H104K080AA?qs=NRhsANhppD8dEJli2CDBHA%3D%3D), 1,189,609 listed, $0.11/1, MOQ 1 cut tape; factory reel 4000 is not MOQ; indexed 4 weeks ago; live checkout unverified. **Live source refresh remains HOLD.**



### 13. C1608X7R1H224K080AB - C1 C2 C4 C5 C7 C8 C10 C11 C12 C13 C14 C15 C125

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 1,334; $0.17/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-005: 220nF at each VCL/VSS pair per Renesas QDG Rev1.10 section1.2; TDK 50V X7R +/-10% production part. Nominal bias curve only; PDN qualification remains open. C125 consolidation replacesYAGEO220n50V10%X7R;Hallrequires>=100nFeffective;bias/aging/temp qualificationopen; $1.23->$0.17.

Fit/qualification screen: X7Rbypass; effectiveCunderbias/temp/aging,ESR/startup/inrush/loop HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H224K080AB), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk-corporation/C1608X7R1H224K080AB/2732843).



### 14. C2012X7R1E105K125AB - C57

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 209,557; $0.23/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: BTN-004: t_force_nom = 65ms + C[uF]/1.56e-4 = 6475.256ms. C tolerance/temp-only 0.765..1.265uF -> 4.969..8.174s with nominal IC equation; excludes IC spread, DC bias, aging and leakage. Full Python-checked math: ../design/single_button_power.md.

Fit/qualification screen: X7Rbypass; effectiveCunderbias/temp/aging,ESR/startup/inrush/loop HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1E105K125AB), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C2012X7R1E105K125AB/513887).



### 15. C3216X7R1V106K160AC - C43 C46 C47 C73 C88 C92 C102

Manufacturer lifecycle evidence: TDKexact code Production direct/indexedprimary; future production horizon unconfirmed.

Sourcing: **DigiKey; listed stock 55,220; $0.68/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: USB-004: QDG Table 2 10uF analog bypass; 35V X7R +/-10%; exact nominal bias curve 9.644uF at 3.3V, not guaranteed minimum.

Fit/qualification screen: X7Rbypass; effectiveCunderbias/temp/aging,ESR/startup/inrush/loop HOLD. Price/alternative review: StandardMLCCprice; dielectric/effectiveC/package must matchalternates.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1V106K160AC), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/C3216X7R1V106K160AC/3956465).

Alternate sourcing evidence: [Mouser Europe](https://eu.mouser.com/en/ProductDetail/TDK/C3216X7R1V106K160AC?qs=JQOhpTY17vfqHp09rhelgw%3D%3D), 545 listed, EUR 0.568/1, MOQ 1 cut tape; factory reel 2000 is not MOQ; indexed 3 weeks ago; regional price, not US checkout quote. **Live source refresh remains HOLD.**



### 16. CL32B226MOJNNNE - C74 C75 C94 C96 C103 C108 C109

Manufacturer lifecycle evidence: SamsungbaseMassProduction;DigiKey exact packing Active.

Sourcing: **DigiKey; listed stock 152,098; $0.52/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-006: 22uF 20% 16V X7R 1210. C74/C75/C94 output; C96 input. Effective C/bias/aging qualification in design/main_regulator_tps63806.md.

Fit/qualification screen: X7Rbulk/bypass;effectiveC/bias/aging/temp/loop/inrush HOLD. Price/alternative review: OrdinaryMLCCpricing;cheapnominalsameC mayfailbias minimum.

Sources: [Manufacturer evidence](https://product.samsungsem.com/mlcc/CL32B226MOJNNN.do), [DigiKey offer](https://www.digikey.com/en/products/detail/samsung-electro-mechanics/CL32B226MOJNNNE/3891481).



### 17. DM3AT-SF-PEJM5 - J2

Manufacturer lifecycle evidence: Hirose exactdrawing; DigiKey Active; no horizon.

Sourcing: **DigiKey; listed stock 81,818; $3.55/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-003: Hirose EDC-325165-00-00;1 DAT2,2 DAT3,3 CMD,4 VDD,5 CLK,6 VSS,7 DAT0,8 DAT1;MP2/MP4 separate normally-open card detect;MP1/3/5/6 shield. Exact socket pin contract only; incomplete card power and bus circuitry. See ../design/camera_storage_interfaces.md.

Fit/qualification screen: microSDpush-pushdetect; inrush/isolation/SI/ingress HOLD. Price/alternative review: $3.55 reasonable; frictionconnector changesuse.

Sources: [Manufacturer evidence](https://www.hirose.com/product/download/?distributor=chip1&lang=en&num=DM3AT-SF-PEJM5&type=2d), [DigiKey offer](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/DM3AT-SF-PEJM5/2533566).



### 18. DMN2056U-7 - Q1 Q2 Q3

Manufacturer lifecycle evidence: Diodes currentdatasheet/PCN; DigiKey Active.

Sourcing: **DigiKey; listed stock 46,058; $0.39/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SYS-007: KILL clamp or main-rail discharge NMOS, G1/S2/D3; VGS 2.596V minimum screen with 1k gate resistor and 1M pulldown. Qualify <=0.2 ohm installed on-resistance, <=1uA gate/board leakage, full action within shared 10ms response. See ../design/system_power_design.md SYS-007.

Fit/qualification screen: LowVGSclamp;hotIDSS/ramp/boardleak HOLD; threshold notRDS guarantee. Price/alternative review: $0.39; generic2N7002 not qualified.

Sources: [Manufacturer evidence](https://www.diodes.com/datasheet/download/DMN2056U.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/diodes-incorporated/DMN2056U-7/7352909).



### 19. DRV5032FADBZR - U33

Manufacturer lifecycle evidence: TI family ACTIVE; DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 119,590; $0.33/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: HALL-001: TI SLVSDC7H Table 5-1 FA DBZ pin map 1 VCC, 2 push-pull OUT, 3 GND; 20Hz omnipolar. Cover wake circuit qualification pending; see design/hall_cover.md.

Fit/qualification screen: Lowduty Hall FA variant;magnet/orientation/threshold/enclosure HOLD. Price/alternative review: $0.33 inexpensive.

Sources: [Manufacturer evidence](https://www.ti.com/product/DRV5032FA), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/DRV5032FADBZR/7400094), [Specification reference](https://www.ti.com/lit/ds/symlink/drv5032.pdf).



### 20. EEE-FN1C100R - C115

Manufacturer lifecycle evidence: Panasonic2025FNcatalog; DigiKey Active.

Sourcing: **DigiKey; listed stock 250; $0.50/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: SENS-016/017/018: ST DS11811 Rev9 section 4, Figure 6, page 19 calls for 10uF aluminum near VDD9 with C117. Panasonic FN 16V +/-20%; conditional 20C 5.04..17.16uF allocation is included in 1mF total main-rail limit. Startup/temperature leakage, service life and mechanical fit remain open; see design/sensor_alternative.md.

Fit/qualification screen: 10uF16Valuminum;leak/coldESR/endurance/startup HOLD. Price/alternative review: $0.50; ceramic changesESR/C.

Sources: [Manufacturer evidence](https://industrial.panasonic.com/cdbs/www-data/pdf/RDE0000/RDE0000C1259.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/panasonic-industry/EEE-FN1C100R/11656952).



### 21. EEE-FP0J470AR - C42

Manufacturer lifecycle evidence: Panasonic exactcurrentproduct; DigiKey Active.

Sourcing: **DigiKey; listed stock 11,262; $0.65/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: USB-003; Renesas QDG Table 1 p.6: 47 uF electrolytic VCC_USBHS bypass. 6.3 V +/-20%, 0.36 ohm max ESR at 100 kHz/20 C; 240 mArms at 100 kHz/105 C.

Fit/qualification screen: 47uF6.3Vbulk;loop/leak/ESR/cold/endurance HOLD. Price/alternative review: $0.65reasonable.

Sources: [Manufacturer evidence](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEEFP0J470AR), [DigiKey offer](https://www.digikey.com/en/products/detail/panasonic-industry/EEE-FP0J470AR/1701010).



### 22. EEF-JX0J151RF - C99 C100

Manufacturer lifecycle evidence: Panasonic currentJXcatalog; DigiKey Active.

Sourcing: **DigiKey; listed stock 9,329; $3.96/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: PWR-004: one of two 150uF output bulk capacitors; 94.5uA initial leakage allowance each; 3000h/125C endurance; capacitance condition limits and ripple derating included in engineering record; not an installed guarantee.

Fit/qualification screen: 150uF6.3Vpolymerpair; effectiveC/ESR/ripple/inrush/loop HOLD. Price/alternative review: $3.96costly; cheaperpolymer must preserve minima.

Sources: [Manufacturer evidence](https://industrial.panasonic.com/cdbs/www-data/pdf/ABE0000/ast-ind-199072.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/panasonic-electronic-components/EEF-JX0J151RF/16718126).



### 23. ERA-6ARW333V - R12 R67

Manufacturer lifecycle evidence: Panasonic exactcurrentproduct; DigiKey Active.

Sourcing: **DigiKey; listed stock 3,943; $0.57/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: RST-002: 33k upper SENSE with 20k lower; 0.05%, 10ppm/C. Conditional rising 3.019118825..3.113278988V. See design/reset_coordination_tps3890.md; fast-fault qualification separate.

Fit/qualification screen: 33k0.05%10ppmdivider with20kRG gives3.019..3.113V;leak HOLD. Price/alternative review: $0.57 accuracy justified vs1%RC.

Sources: [Manufacturer evidence](https://industrial.panasonic.com/jp/products/pt/high-precision-chip-resistors/models/ERA6ARW333V), [DigiKey offer](https://www.digikey.com/en/products/detail/panasonic-industry/ERA-6ARW333V/3073417).



### 24. ESD441DPYR - D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12

Manufacturer lifecycle evidence: TI exact ordering code ACTIVE / Production; no remaining-life guarantee.

Sourcing: **DigiKey; listed stock 10,339; $0.34/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: BTN-010: DPY IO1/GND2, leakage <100nA over +/-5.5V and operating temperature; fits 12uA PB allocation. TI RevB pp1/3/6. Typical DPY +8.2V/-3.8V at16A TLP; board residual transient and R19 pulse qualification required. No generic diode model.

Fit/qualification screen: Single-channel unidirectional ESD protection, 5.5 V standoff, 1 pF typical. Clamp voltage versus protected-pin absolute limits, layout, leakage and connector ESD require qualification. Not a moisture detector or protection for 15/20 V PD VBUS.. Price/alternative review: $0.34 each is reasonable for individual data-line clamps; array alternatives must preserve capacitance, clamp behavior and routing..

Sources: [Manufacturer evidence](https://www.ti.com/product/ESD441/part-details/ESD441DPYR), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/ESD441DPYR/28715599), [Specification reference](https://www.ti.com/lit/ds/symlink/esd441.pdf).



### 25. ESP32-C6-WROOM-1-N8 - U3

Manufacturer lifecycle evidence: Espressif currentmodule; C6chipfamily12yrfromJan2023, not exact module guarantee.

Sourcing: **DigiKey; listed stock 992; $5.55/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: Radioonly;noClassicA2DP/USB UAC;link/RF/current HOLD

Fit/qualification screen: Radioonly;noClassicA2DP/USB UAC;link/RF/current HOLD. Price/alternative review: $5.55certifiedmodule defensible.

Sources: [Manufacturer evidence](https://www.espressif.com/en/products/longevity-commitment1), [DigiKey offer](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-C6-WROOM-1-N8/17728866), [Specification reference](https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf).



### 26. EVQP7A01P - SW1 SW2 SW3 SW4 SW5

Manufacturer lifecycle evidence: Panasonic EVQ-P7family; DigiKey Active.

Sourcing: **DigiKey; listed stock 118,902; $0.28/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: BTN-003/010: min load 10uA at 2V, max 50mA at 12V, initial contact <=0.5 ohm, bounce <=10ms; -20..70C product limit. R18/R19 guarantee contact-current and PB threshold DC screens; ESD and lifetime qualification required.

Fit/qualification screen: -20..70C buttons; mechanical/lifetime/ingress HOLD; unsealed. Price/alternative review: $0.28;sealedalternative if housing cannot isolate.

Sources: [Manufacturer evidence](https://industrial.panasonic.com/cdbs/www-data/pdf/ATK0000/ATK0000C378.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/panasonic-industry/EVQ-P7A01P/4429447).



### 27. G6K-2F-Y DC3 - K1

Manufacturer lifecycle evidence: CurrentG6Kdatasheet; DigiKey ActiveAratas(formerOmron); transfer notEOL.

Sourcing: **DigiKey; listed stock 15,746; $4.62/1; Tube; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: AUD-011 candidate/HOLD: nonlatching DPDT 3V coil, 91 ohm +/-10% at 23C; coil 1+/8-, COM 3/6, NC 2/7, NO 4/5 per Omron G6K 2025-11-18 p6. SE COM/NO wiring only; coil supply/driver/clamp/DC and rail-fault gating unimplemented. Qualify temperature pickup, release timing, lifetime contact resistance; no waterproof claim. Footprint deferred.

Fit/qualification screen: 1Aquiet signal relay, notbank; driver/fault/contactlife HOLD. Price/alternative review: $4.62 isolation justified vsanalogswitchfaultlimits.

Sources: [Manufacturer evidence](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8145/Omron_11-18-2025_P6K_Datasheet_EN.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/G6K-2F-Y-DC3/369205).



### 28. GRM188R72A104KA35D - C117 C118 C124

Manufacturer lifecycle evidence: Murata current exact/base specification;DigiKey Active;manufacturer exactlifecycle unconfirmed.

Sourcing: **DigiKey; listed stock 535,359; $0.16/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SENS-017/018: LIS2DW12 local VDD9/VDDIO10 bypass, 100nF 10% X7R 100V 0603; C117 with C115 near VDD9. ST DS11811 Rev9 section 4, Figure 6, page 19. Effective capacitance over bias/temperature/aging and placement qualification pending; see design/sensor_alternative.md.

Fit/qualification screen: X7Rbulk/bypass;effectiveC/bias/aging/temp/loop/inrush HOLD. Price/alternative review: OrdinaryMLCCpricing;cheapnominalsameC mayfailbias minimum.

Sources: [Manufacturer evidence](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R72A104KA35-01A.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/murata-electronics/GRM188R72A104KA35D/702549).



### 29. GRM31C5C1H104JA01K - C69 C70 C71 C110

Manufacturer lifecycle evidence: Murata current exact/base specification;DigiKey Active;manufacturer exactlifecycle unconfirmed.

Sourcing: **DigiKey; listed stock 22,231; $0.52/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SYS-007: three parallel 100nF C0G CT-to-GND; C initial/temperature envelope 284.145..316.827nF (Murata cold Table A +0.58%). TI nominal delay 300/175+0.0005=1.714786s. Proportional IC model minimum 0.974511s is not a guaranteed limit; require qualified hold >=0.90s. No X7R substitution.

Fit/qualification screen: C0G100n stabletiming/SET;leak/startup HOLD. Price/alternative review: $0.52stabletiming premium justified vsX7R.

Sources: [Manufacturer evidence](https://www.mouser.com/datasheet/2/281/1/GRM31C5C1H104JA01_01A-1987788.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/murata-electronics/GRM31C5C1H104JA01K/2548138).



### 30. GRM31CR70J226KE19L - C3

Manufacturer lifecycle evidence: Murata current exact/base specification;DigiKey Active;manufacturer exactlifecycle unconfirmed.

Sourcing: **DigiKey; listed stock 104,226; $1.00/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Renesas Quick Design Guide Table3 recommended family; 22uF +/-10% 6.3V X7R; effective capacitance and lifecycle approval pending

Fit/qualification screen: X7Rbulk/bypass;effectiveC/bias/aging/temp/loop/inrush HOLD. Price/alternative review: OrdinaryMLCCpricing;cheapnominalsameC mayfailbias minimum.

Sources: [Manufacturer evidence](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM31CR70J226KE19-01CA.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/murata-electronics/GRM31CR70J226KE19L/3845712).



### 31. AS4C16M32SC-7TIN - U14

Manufacturer lifecycle evidence: Current manufacturer product; absent from reviewed SDRAM EOL list; no exact remaining-life guarantee. Public Sep2018Rev1.0 PRELIMINARY -> HOLD.

Sourcing: **DigiKey; listed stock 175; $43.60/1; Qty1 tray; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: CMS-010 replacement matches 86pins; underlying full net memberships preserved. ShopMemory/Mouser comparison is not current purchase authorization.

Fit/qualification screen: Native86pin/fourunit map matches;64MiB16Mx32,3.0..3.6V,-40..85C,CL3/133MHz; startup/refresh/SI/timing/power/footprint and released specifications HOLD. Price/alternative review: $43.60DKqty1 vs$32.99Mouser indexedlastmonth29stock (directrefreshfailed), linkedShopMemory$19.20qty1..107 butstocknotverified. Do notpayDKpremium before confirmingauthorizedprimarysource..

Sources: [Manufacturer evidence](https://www.alliancememory.com/as4c16m32sc/), [DigiKey offer](https://www.digikey.com/en/products/detail/alliance-memory-inc/AS4C16M32SC-7TIN/9681183), [Specification reference](https://www.alliancememory.com/wp-content/uploads/AllianceMemory_512M-SDRAM_Cdie_AS4C16M32SC-AS4C32M16SC-AS4C64M8SC-7TIN_Sept2018_rev1.0.pdf).



### 32. LIS2DTW12TR - U26

Manufacturer lifecycle evidence: STexactActive/volumeproduction.

Sourcing: **DigiKey; listed stock 503; $2.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: LIS2DTW12TR replaces low-stock LIS2DW12TR; DS12825 Rev4 Table1/section4. Shared +3V3_MCU VDD9/VDDIO10, I2C 0x19, P410/K13 SCL, P409/R16 SDA, P306/D11 INT1. ST example waits 20ms then polls reset; exact startup/recovery qualification pending. See design/sensor_alternative.md.

Fit/qualification screen: Orientationaccelerometer+temp, not6axisgyroIMU;bus/power HOLD. Price/alternative review: $2.10MOQ1; rejectedLIS2DW12 notfitted.

Sources: [Manufacturer evidence](https://www.st.com/en/mems-and-sensors/lis2dtw12.html), [DigiKey offer](https://www.digikey.com/en/products/detail/stmicroelectronics/LIS2DTW12TR/9997333), [Specification reference](https://www.st.com/resource/en/datasheet/dm00560052.pdf).



### 33. LM66100DCKR - U10

Manufacturer lifecycle evidence: TI family ACTIVE; DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 67,423; $0.36/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SENS-010 / SYS-007 revision: VIN1=raw SYS_AON, VOUT6 via R31=100R to AON_HOLD, CE3=AON_HOLD downstream of R31. GND2 and unused ST5 to GND; NC4 internally unconnected. Do not move R31 before VIN or sense immediate VOUT: limited reverse current can fail to trip. Budget0.817mA pre-trip reverse plus1.825mA control and combined1uC transition/initial-undershoot reserve. Qualify VIN=0..4.6V leakage and slow/floating-source collapse. Topology: ../design/system_power_design.md SYS-007; revised reservoir budget: ../design/sensor_alternative.md SENS-010.

Fit/qualification screen: Idealdiode hold-up; reverse/drop/fault HOLD, notbatteryPDpowerpath. Price/alternative review: $3.36 autonomous function justified.

Sources: [Manufacturer evidence](https://www.ti.com/product/LM66100), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/LM66100DCKR/10273183), [Specification reference](https://www.ti.com/lit/ds/symlink/lm66100.pdf).



### 34. LT3042IMSE#PBF - U23

Manufacturer lifecycle evidence: ADIrecommendednewdesigns; exactIMSE#PBF/#TRPBF PRODUCTION.

Sourcing: **Mouser; listed stock 7,701; $9.12/1; Qty-one offer; confirm carrier choice at purchase; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-013: adjustable MIPI 1.8V supply; 200mA I-grade MSOP. ADI Rev C pin map and reverse-output protection. SET ramp model, effective capacitance and rail sequencing require qualification.

Fit/qualification screen: MIPI200mAultraquietLDO; IQ2mAnominal;13mAbudgetconservative;startup/reverse/noise HOLD. Price/alternative review: $9.12 costreview vsTPS7A20/02; no blind swap.

Sources: [Manufacturer evidence](https://www.analog.com/en/products/lt3042.html), [Mouser offer](https://www.mouser.com/en/ProductDetail/Analog-Devices/LT3042IMSEPBF?qs=oahfZPh6IAKNLbWsEo0jgA%3D%3D), [Specification reference](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3042.pdf).



### 35. LTC2954ITS8-1#TRPBF - U9

Manufacturer lifecycle evidence: ADIrecommendednewdesigns; exact ordering option present.

Sourcing: **DigiKey; listed stock 4,637; $7.83/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: BTN-001..008: initial-off hardware latch, debounced held-button interrupt, independent forced-off timer, 2.7-26.4V. Full math: ../design/single_button_power.md

Fit/qualification screen: Autonomousbutton/forcedoff6uAtyp;reservoir/ramp/fault HOLD. Price/alternative review: $7.83 hardwareoff independentMCU justified.

Sources: [Manufacturer evidence](https://www.analog.com/en/products/ltc2954.html), [DigiKey offer](https://www.digikey.com/en/products/detail/analog-devices-inc/LTC2954ITS8-1-TRPBF/1621452), [Specification reference](https://www.analog.com/media/en/technical-documentation/data-sheets/2954fb.pdf).



### 36. OPA1622IDRCR - U34

Manufacturer lifecycle evidence: TI family ACTIVE; DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 4,264; $7.43/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: AUD-010 WIP: TI SBOS727B Rev B pin map; dual unity-gain SE buffer; EP11 tied to V-4; bypass, default-off, rail and independent output disconnect design remain open.

Fit/qualification screen: Quietheadphonecandidate;gain/rails/IEMnoise/pop/DCfault/stability HOLD;notbank. Price/alternative review: $7.43 noise/drive justified;INA1620/OPA1688 alternatives require analysis.

Sources: [Manufacturer evidence](https://www.ti.com/product/OPA1622), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/OPA1622IDRCR/5804204), [Specification reference](https://www.ti.com/lit/ds/symlink/opa1622.pdf).



### 37. OPT4001DTSR - U32

Manufacturer lifecycle evidence: TI family ACTIVE; DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 346; $1.68/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: TI SBOS993A Rev A Table 6-2; 8-pin DTS only; circuit qualification pending

Fit/qualification screen: Ambientlight;opticalwindow/bus/crosstalkcalibration HOLD. Price/alternative review: $1.68reasonable;OPT300x ifresolutionpermits.

Sources: [Manufacturer evidence](https://www.ti.com/product/OPT4001), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/OPT4001DTSR/17748298), [Specification reference](https://www.ti.com/lit/ds/symlink/opt4001.pdf).



### 38. R7KA8P1KFLCAC#UC0 - U1

Manufacturer lifecycle evidence: RenesasexactUC0/UC1Active;UC0replacementUC1; transitionPCNunknown.

Sourcing: **DigiKey; listed stock 1; $29.47/1; Qty-one tray offer; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: TRANSITIONHOLD PCN/die/balls/errata/qty1UC1stock;retainnativeUC0

Fit/qualification screen: TRANSITIONHOLD PCN/die/balls/errata/qty1UC1stock;retainnativeUC0. Price/alternative review: HistoricalMouser317/$29.47MOQ1;DK1discontinued;UC1MOQ189 notqty1.

Sources: [Manufacturer evidence](https://www.renesas.com/en/products/ra8p1/part-details/r7ka8p1kflcac-uc0), [DigiKey offer](https://www.digikey.com/en/products/detail/renesas-electronics-corporation/R7KA8P1KFLCAC-UC0/26738126), [Specification reference](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet).



### 39. RC0603FR-07100KL - R22

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 596,757; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: BTN-001/007: 100k KILL-to-GND with 10k pull-up to switched +3V3_MCU. At 3.0..3.6V including resistor tolerance/TC and leakage: high >=2.606319V; MCU sink <=0.379310mA. R22 keeps KILL low when the switched rail is absent. See ../design/single_button_power.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-07100KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07100KL/729836).



### 40. RC0603FR-0710KL - R1 R2 R3 R4 R5 R8 R9 R10 R11 R14 R15 R16 R17 R18 R20 R21 R27 R28 R29 R30 R44 R45 R46 R47 R48 R49 R50 R51 R52 R53 R64 R72 R75 R77 R78 R79 R80 R81 R96 R97 R107 R108 R109 R112 R113

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 4,884; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: 10k 1%, 100mW at 70C, 0603; 3.6V/9.9k=0.364mA and 1.31mW worst nominal-tolerance load. MCU pull-up reference: HUM 21.4 and reset/MD guidance. PCB footprint deferred.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0710KL/729827).



### 41. RC0603FR-0710RL - R66

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 119,702; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: PWR-006: 10R lower feedback trim in series with R42 1k; 1%, 200ppm/C. See design/main_regulator_tps63806.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0710RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0710RL/726879).



### 42. RC0603FR-07110KL - R34

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 180,003; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: PWR-004: 110k AON_HOLD-to-MAIN_PWR_EN pull-up; 1% initial plus 100ppm/C over 100C. With 3.8uA adverse load, POR current <=14.003041uA and held 2.7V input >=2.273598V. See ../design/main_regulator_ltc3119.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-07110KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07110KL/726905).



### 43. RC0603FR-071K5L - R98 R99

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 460,674; $0.11/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: Camera SCCB host pull-up: 1.5k, 1%, 100ppm/C per Pcam host guidance. Conditional combined host/module sink screen is 3.013mA at 0.4V; require dedicated RA IIC FMPE=1. Host 300ns RC screen permits 231.39pF; module sink, translator drop and complete bus timing require qualification. See ../design/camera_storage_interfaces.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-071K5L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-071K5L/726864).



### 44. RC0603FR-071KL - R19 R23 R24 R25 R26 R35 R36 R68 R70 R73 R94 R110 R111

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 3,225,465; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: BTN-003: 1k series resistor with 10k PB pullup and C56=100nF. Worst resistor screen 980.1..1020.1 ohm. Threshold KCL and peak contact discharge math in ../design/single_button_power.md; exposed-node ESD protection required.

R110/R111 additionally implement SERVICE-025 parallel discharge; aggregate leakage, storage and fixture qualification remain open.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-071KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-071KL/726843).



### 45. RC0603FR-071ML - R37 R38 R71

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 2,221,237; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SYS-007: 1M gate-source pulldown minimizes held-reservoir load. Rmin=980100R including 1% and 100ppm/C over 100C; branch <=5.693399uA including 1uA qualified gate/board leakage. See ../design/system_power_design.md SYS-007.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-071ML), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-071ML/726844).



### 46. RC0603FR-072K21L - R76

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 1,825; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-072K21L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-072K21L/727018).



### 47. RC0603FR-072K2L - R6

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 139,931; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Renesas RA8x2 Quick Design Guide revision 1.10 Table 2 p.7: 2.2 kohm +/-1% USBHS reference resistor. See design/usb_interface.md USB-001.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-072K2L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-072K2L/729963).



### 48. RC0603FR-07330RL - R82

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 219,407; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-07330RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07330RL/730109).



### 49. RC0603FR-0733RL - R83 R84 R85 R86 R87 R88

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 386,443; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0733RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0733RL/727158).



### 50. RC0603FR-073K3L - R102 R103

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 622,536; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: ALS-005: shared LIS2DTW12TR/OPT4001 IIC0_A pullup; 3.3k 1%, +/-100ppm/C, 0.1W at 70C, 0603. Conditional 25..70pF / +/-17uA screen: 62.912..219.056ns rise, 1.121276mA sink. 5% drift, installed capacitance/leakage and host timing require qualification; see design/ambient_light.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-073K3L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-073K3L/730073).



### 51. RC0603FR-0747KL - R65 R89 R90 R91 R92 R93 R100 R101 R104 R105 R106

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 1,523,498; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-011; INT 47k pull-up to switched +3V3_MCU; explicit departure from vendor 5-10k to fit 100uA VOL test; ILOW <=80.150949uA, VHIGH >=3.050265V; RC timing qualification pending

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-0747KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0747KL/730200).



### 52. RC0603FR-074K7L - R7

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 4,356,337; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: RADIO-019: R7 4.7k / R8 10k, 1% x 100 ppm/C x 100 C and adverse 12uA ON allocation; low <=0.383594 V, high >=1.639635 V for valid host domain. See ../design/radio_interface.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-074K7L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-074K7L/727212).



### 53. RC0603FR-0768KL - R69

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 264,136; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-004: 68k RUN_U13-to-GND. Raw zero screen with 2uA buffer Ioff and 1uA RUN leakage allocation gives <=0.2081V. RUN leakage is an engineering allocation, not a guaranteed hot limit. Held clamp additionally required. See ../design/main_regulator_ltc3119.md.

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-0768KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0768KL/727352).



### 54. RC0603JR-070RL - R43

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 9,345,144; $0.10/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: CMS-010; populated source-side SDCLK tuning link; 0R is not validated damping or timing closure

Fit/qualification screen: Ordinarypull/series 1% resistor; per-reference budget below; power/leak/RC/SI HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://www.yageogroup.com/component-documentation/download/specsheet/RC0603JR-070RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC0603JR-070RL/726675).



### 55. RC2512FK-07100RL - R31

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 226; $0.34/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SENS-010 / SYS-007 revision: 100R between U10 VOUT and AON_HOLD; CE senses downstream reservoir. Rmin/max=98.01/102.01ohm with tolerance and100C TCR allocation. At1.825mA control load, resistor drop<=0.18616825V. Pre-trip reverse<=80mV/98.01ohm<0.817mA. Short screen:4.6^2/98.01<0.216W, below1W nominal rating; temperature/pulse cycling qualification required. Topology: ../design/system_power_design.md SYS-007; revised reservoir: ../design/sensor_alternative.md SENS-010.

Fit/qualification screen: 2512 nominal1W discharge/fault; pulse/hot/boardtemperature HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC2512FK-07100RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC2512FK-07100RL/5921799).



### 56. RC2512FK-0722RL - R39 R40

Manufacturer lifecycle evidence: YAGEO current RC family; distributor exact Active; exact mfr future horizon unconfirmed.

Sourcing: **DigiKey; listed stock 14,447; $0.32/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: SENS-010 / SYS-007 revision: two22R1W in parallel; Rpath_max=11.4211ohm including allocated0.2ohm FET. At Cmain<=1mF and2.5mA total return/injection (1.5mA key filters +1mA other), Vinf=28.552750mV. 10ms response +46.398757ms from3.6V to90mV +10ms low hold =66.398757ms TOTAL; held75.794309ms conditional margin9.395552ms. Each22R worst initial power0.601052W. Derate and qualify FET resistance, backfeed and repeated/continuous fault energy. Full equation: ../design/sensor_alternative.md SENS-010.

Fit/qualification screen: 2512 nominal1W discharge/fault; pulse/hot/boardtemperature HOLD. Price/alternative review: Commodity price reasonable; preserve value/tolerance/TC/power on substitutions.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RC2512FK-0722RL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RC2512FK-0722RL/5922011).



### 57. RG1608N-203-W-T1 - R13 R74

Manufacturer lifecycle evidence: Susumu current RG specs; exactDigiKey Active; no sunset commitment.

Sourcing: **DigiKey; listed stock 77,982; $0.61/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: RST-002: 20k lower SENSE with 33k upper; 0.05%, 10ppm/C. Conditional rising 3.019118825..3.113278988V. See design/reset_coordination_tps3890.md; fast-fault qualification separate.

Fit/qualification screen: 20k0.05%10ppm supervisor ratio/TC;3.019..3.113Vcorner;leak HOLD. Price/alternative review: $0.61 accuracy premium justified.

Sources: [Manufacturer evidence](https://www.susumu.co.jp/common/pdf/n_catalog_partition01_en.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/susumu/RG1608N-203-W-T1/600628).



### 58. RG2012L-102-L-T05 - R42

Manufacturer lifecycle evidence: Susumu current RG specs; exactDigiKey Active; no sunset commitment.

Sourcing: **DigiKey; listed stock 0; $3.45/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-006: 1k lower feedback in series with R66 10R; 0.01%, 2ppm/C. See design/main_regulator_tps63806.md.

Fit/qualification screen: 1k0.01%2ppm lowerTPS63806divider plusR66;3.272Vnom/3.393max;leak/loop HOLD. Price/alternative review: $2.18/$3.66 costly but quantified accuracy; network/accurateregulator futurecoststudy;1%not equivalent.

Sources: [Manufacturer evidence](https://www.susumu.co.jp/common/pdf/n_catalog_partition01_en.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/susumu/RG2012L-102-L-T05/3737817), [Specification reference](https://www.susumu.co.jp/common/pdf/RG_LL_Data_Sheet.pdf).



### 59. RG2012V-562-P-T1 - R41

Manufacturer lifecycle evidence: Susumu current RG specs; exactDigiKey Active; no sunset commitment.

Sourcing: **DigiKey; listed stock 493; $2.18/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-006: 5k6 upper feedback; 0.02%, 5ppm/C; installed tolerance model in design/main_regulator_tps63806.md.

Fit/qualification screen: 5.6k0.02%5ppm upperTPS63806divider;3.393Vmaximumneeded for SDRAM;leak/loop HOLD. Price/alternative review: $2.18/$3.66 costly but quantified accuracy; network/accurateregulator futurecoststudy;1%not equivalent.

Sources: [Manufacturer evidence](https://www.susumu.co.jp/common/pdf/n_catalog_partition01_en.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/susumu/RG2012V-562-P-T1/1248344).



### 60. TNPW0603100KBEEA - R33

Manufacturer lifecycle evidence: Vishay currentApr2026TNPWspecification; DigiKey exact code Active; no exact sunset guarantee.

Sourcing: **DigiKey; listed stock 65,460; $0.26/1; Qty1 cut tape; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SYS-007 replacement retains R32/R33 ratio, tolerance and TC; unavailable oldYAGEO replaced.

Fit/qualification screen: 100k0.1%25ppm0603,P70general0.11W,100V; preserves source-trip3.263705831..3.476597632V; leakage/circuit/footprint HOLD. Price/alternative review: $0.26vsunavailable$0.10YAGEO; BournsCRT0603-BY-1003ELF3788stock/$0.10 alternative notqualified;16cpremiumacceptableprototype.

Sources: [Manufacturer evidence](https://www.vishay.com/docs/28758/tnpw_e3.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603100KBEEA/1857055).



### 61. RT0603BRD0718KL - R95

Manufacturer lifecycle evidence: YAGEO current RT family; distributor Active where stocked; mfr exact horizon unconfirmed.

Sourcing: **DigiKey; listed stock 43,794; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-013: 18k SET resistor; 0.1% and 25ppm/C over 100C model, 98..102uA SET current, +/-2mV offset and +/-100nA leakage allocation give 1.75404..1.84624V. DC limits require 2<VIN<20V and load >=1mA; startup unqualified. See design/camera_storage_interfaces.md.

Fit/qualification screen: Precision0.1%25ppm divider/SET/series duty; perref corners below; hot/leak/power HOLD. Price/alternative review: Precisioncost justified threshold/SET corners;1%drop-in invalidates calculation.

Sources: [Manufacturer evidence](https://yageogroup.com/component-documentation/download/specsheet/RT0603BRD0718KL), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RT0603BRD0718KL/1072301).



### 62. RT0603BRD0730RL - R54 R55 R56 R57 R58 R59 R60 R61 R62 R63

Manufacturer lifecycle evidence: YAGEO current RT family; distributor Active where stocked; mfr exact horizon unconfirmed.

Sourcing: **DigiKey; listed stock 5,046; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-011; external JESD251 30R series on DQ0-7, CK and DS; 0.1%, 25ppm/C, 100C screen 29.895075..30.105075 ohm; MCU-side placement starting point, SI qualification open

Fit/qualification screen: Precision0.1%25ppm divider/SET/series duty; perref corners below; hot/leak/power HOLD. Price/alternative review: $0.10sameprice as1%RC;30ohmprecision carriesnoqty1premium.

Sources: [Manufacturer evidence](https://yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RT0603BRD0730RL/1072456).



### 63. RT0805BRD07732KL - R32

Manufacturer lifecycle evidence: YAGEO current RT family; distributor Active where stocked; mfr exact horizon unconfirmed.

Sourcing: **DigiKey; listed stock 15,646; $0.10/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: SYS-007: 732k top from raw SYS_AON to U11 SENSE; lower 100k. Each +/-0.1%, 25ppm/C, 100C excursion; U11 0.405V +/-2% and +/-25nA. Nominal trip 3.3696V, corners 3.263705831..3.476597632V. Exact thin-film part; no 1% thick-film substitution.

Fit/qualification screen: Precision0.1%25ppm divider/SET/series duty; perref corners below; hot/leak/power HOLD. Price/alternative review: Precisioncost justified threshold/SET corners;1%drop-in invalidates calculation.

Sources: [Manufacturer evidence](https://yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L), [DigiKey offer](https://www.digikey.com/en/products/detail/yageo/RT0805BRD07732KL/6617094).



### 64. S28HL01GTFPBHI030 - U15

Manufacturer lifecycle evidence: InfineonexactActivepreferred;plannedatleast2037.

Sourcing: **DigiKey; listed stock 2,553; $32.06/1; Qty-one tray offer; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: CMS-011; 128MiB 3V Octal NOR; Infineon 002-18216 revision AB Fig1/Table7; 125MHz DDR target pending timing, power and SI qualification

Fit/qualification screen: 128MiBoctal2.7..3.6Vindustrial;boot/ECC/DQS/SI/reset HOLD. Price/alternative review: $22.21capacity/octalspeeddefensible;smallerquadnotdrop-in.

Sources: [Manufacturer evidence](https://www.infineon.com/part/S28HL01GTFPBHI030), [DigiKey offer](https://www.digikey.com/en/products/detail/infineon-technologies/S28HL01GTFPBHI030/15903885), [Specification reference](https://www.mouser.com/datasheet/3/70/1/8HS01GT_S28HL512T_S28HL01GT_512MB_1GB_SEMPER_TM_FLASH_OCTAL_INTERFACE_1_8V_3-DataSheet-v68_00-EN.pdf).



### 65. SN74LVC1G97DBVR - U7 U8 U19 U20 U24 U28 U29 U30 U31

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 25,305; $0.23/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: RADIO-015: Schmitt-input AND configuration, IN1 grounded. Gate reset request with MCU reset. Partial-power-down Ioff specified; analog ramp and full sequencing qualification remain open.

Fit/qualification screen: Faultsequence logic perref truth-table/ramp/Ioff/hot HOLD. Price/alternative review: $0.23reasonable;AUPchanges voltage/drive/timing.

Sources: [Manufacturer evidence](https://www.ti.com/product/SN74LVC1G97), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G97DBVR/571196), [Specification reference](https://www.ti.com/lit/ds/symlink/sn74lvc1g97.pdf).



### 66. SPM5020T-2R2M-LR - L1

Manufacturer lifecycle evidence: TDKexact code Production.

Sourcing: **DigiKey; listed stock 144; $1.27/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Renesas R01AN7883EU0110 Table 3; 2.2uH +/-20%, DCR max 40.7mOhm, rated current 4.6A typical (40C rise), 7A typical (30% inductance loss).

Fit/qualification screen: 2.2uHcore37typ40.7maxmohm25C;7A30%drop/4.6A40Crise typ;hotloop HOLD. Price/alternative review: Referencechoice defensible;cheaper changesloss/saturation.

Sources: [Manufacturer evidence](https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=SPM5020T-2R2M-LR), [DigiKey offer](https://www.digikey.com/en/products/detail/tdk/SPM5020T-2R2M-LR/5962361).



### 67. T491D227K010AT - C63 C64 C65 C66

Manufacturer lifecycle evidence: KEMETcurrentT491catalog;DigiKey Active.

Sourcing: **DigiKey; listed stock 3,738; $2.24/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: SENS-010 / SYS-007 revision: four parallel 220uF/10V. Cmin=880uF*0.9^3=641.52uF; control<=1.825mA plus 0.817mA reverse allocation; Vinitial=3.013705831V; 1uC transition reserve gives 75.794309ms to 2.7V. At Cmain<=1mF and return/injection<=2.5mA: 10ms response +46.398757ms discharge to90mV +10ms low hold =66.398757ms TOTAL. Conditional margin9.395552ms. See ../design/sensor_alternative.md; startup/leakage/backfeed qualification pending.

Fit/qualification screen: MnO2reservoirmin641.52uF;surge/leak/ESR/short/charge/hot HOLD. Price/alternative review: $2.24each;polymerchangesleak/hold-up.

Sources: [Manufacturer evidence](https://content.kemet.com/datasheets/KEM_T2005_T491.pdf), [DigiKey offer](https://www.digikey.com/en/products/detail/kemet/T491D227K010AT/2336333).



### 68. T521B106M016ATE100 - C128 C129

Manufacturer lifecycle evidence: KEMETcurrentT52xcatalog;DigiKey Active;43wkfactory risk.

Sourcing: **DigiKey; listed stock 17,524; $1.72/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: supplier page crawled last month; retrieved 2026-10-05; not a live checkout.

Role and existing limits: WIP quiet +/-5V rail bulk. KEMET T2076_T52X-530 2026-09-09 pp25,33,34,36: 10uF +/-20%,16V,100mohm,125C category 5. DigiKey399-16631-1-ND CT MOQ1 $1.72 17479 available 2026-10-05 unreserved. HOLD startup/reverse/ripple/regulator stability and footprint; see design/audio_quiet_decoupling.md. Not selected for high-voltage power bank.

Fit/qualification screen: Quiet10uF16Vpolymer;negativepolarity/reverse/ripple/temp/loop HOLD. Price/alternative review: $1.72 lowESRdefensible;MLCCbias/microphonictrade.

Sources: [Manufacturer evidence](https://yageogroup.com/content/datasheet/asset/file/KEM_T2076_T52X-530), [DigiKey offer](https://www.digikey.com/en/products/detail/kemet/T521B106M016ATE100/8042243).



### 69. TMUX1511RSVR - U21 U22

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 82,239; $0.77/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Two devices isolate six 3.3 V SDHI1_B lines; SEL high closes each channel. Main-powered VDD, SD_READY-qualified control. See ../design/microsd_power_interface.md.

Fit/qualification screen: Poweredoffbusisolation;enabledefaults/bandwidth/cardSI HOLD. Price/alternative review: $0.68;cheapmuxwithoutpoweredoffprotection wrong.

Sources: [Manufacturer evidence](https://www.ti.com/product/TMUX1511), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TMUX1511RSVR/9954161), [Specification reference](https://www.ti.com/lit/ds/symlink/tmux1511.pdf).



### 70. TPS22950CDDCR - U17

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 14,713; $0.98/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: Supervised VDD_SD island; ILIM 2.21k gives table 0.38/0.50/0.62 A min/typ/max under stated conditions. Keep external 330R discharge and G30 undervoltage monitor. See ../design/microsd_power_interface.md.

Fit/qualification screen: microSDlimitR76.38/.50/.62Aconditional;inrush/fault/SOA HOLD. Price/alternative review: $1.83currentlimitfunction;22917not equivalent.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS22950), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS22950CDDCR/18187757), [Specification reference](https://www.ti.com/lit/ds/symlink/tps22950.pdf).



### 71. TPS22964CYZPT - U4

Manufacturer lifecycle evidence: TI exact code ACTIVE;DigiKey exact code Activebut4stock.

Sourcing: **DigiKey; listed stock 4; $1.77/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: FRAGILESTOCK;reverseblockdisabledonly;railfault/startup HOLD;YZPR0stock

Fit/qualification screen: FRAGILE STOCK;reverseblockdisabledonly;railfault/startup HOLD;YZPR0stock. Price/alternative review: $1.56;compare22964C2/FPF1048pinout/functionfirst.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS22964), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS22964CYZPT/4457704), [Specification reference](https://www.ti.com/lit/ds/symlink/tps22963c.pdf).



### 72. TPS3808G01DBVR - U11

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 59,060; $1.96/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: SYS-007: adjustable 0.405V +/-2%, SENSE +/-25nA; 732k/100k precision divider gives 3.3696V nominal, 3.263705831..3.476597632V corners. RESET open-drain shares MAIN_PWR_EN; VDD and MR on AON_HOLD; CT 3x100n C0G, nominal 1.714786s; require qualified reset hold >=0.90s. No fixed-G33 substitution.

Fit/qualification screen: 732k/100kprecision supervisor3.2637..3.4766V;reset/ramp/leak HOLD. Price/alternative review: $1.96justified;TPS3899/3840changefunction.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS3808), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G01DBVR/666712), [Specification reference](https://www.ti.com/lit/ds/symlink/tps3808.pdf).



### 73. TPS3808G30DBVR - U18

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 11,092; $1.84/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: SD power contract: 2.79 V nominal threshold, CT open 12..28 ms; main-powered VDD and card-side SENSE, MR on SD_PWR_ON. See ../design/microsd_power_interface.md.

Fit/qualification screen: Fixedrailthreshold/propagation/rampsequencing HOLD. Price/alternative review: $1.84reasonable.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS3808), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G30DBVR/666724), [Specification reference](https://www.ti.com/lit/ds/symlink/tps3808.pdf).



### 74. TPS389001DSET - U2 U6

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 2,090; $2.22/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: RST-002: adjustable 1.15V falling/1.157V rising supervisor, open-drain reset. R67/R74 33k/20k; C95 10n and R75 10k. Conditional main-rail DC/startup coordination; fast-collapse qualification remains open. See design/reset_coordination_tps3890.md.

Fit/qualification screen: SeparateSENSE/delayreset;C95C0Gpreservescorner;leak/startup/fastfault HOLD. Price/alternative review: $2.22featuresjustify;3899differentdelay/pins.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS3890), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS389001DSET/6110554), [Specification reference](https://www.ti.com/lit/ds/symlink/tps3890.pdf).



### 75. TPS63806YFFR - U13

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 4,223; $3.66/1; Qty-one cut tape; optional full reel and reeling fees excluded; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-006: 3.272277V nominal forced-PWM buck-boost, MODE tied VIN. Divider 5k6/(1k+10R), 470nH and qualified effective bypass requirements in design/main_regulator_tps63806.md. Reset coordination and source protection remain open.

Fit/qualification screen: 2.095Acontinuousallocationunqualified;2.5Atransient/5.5Aswitchnotguarantee;5.5Vmaxinput;thermal HOLD. Price/alternative review: $3.23defensible;historicalLTC3119$24.07notdefaultredesign.

Sources: [Manufacturer evidence](https://www.ti.com/product/TPS63806), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS63806YFFR/10715517), [Specification reference](https://www.ti.com/lit/ds/symlink/tps63806.pdf).



### 76. TXU0102DCUR - U25

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 27,420; $1.08/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: Fixed2out/Ioff;OE/supply/timing HOLD

Fit/qualification screen: Fixed2out/Ioff;OE/supply/timing HOLD. Price/alternative review: $1.08reasonable;autoTXS/TXBnot equivalent.

Sources: [Manufacturer evidence](https://www.ti.com/product/TXU0102), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TXU0102DCUR/16341507), [Specification reference](https://www.ti.com/lit/ds/symlink/txu0102.pdf).



### 77. TXU0202DCUR - U27

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 18,216; $1.08/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: UARTonedirectioneach;supplies/bypass/OE/pullspresent;fixture/ramp/timing HOLD

Fit/qualification screen: UARTonedirectioneach;supplies/bypass/OE/pullspresent;fixture/ramp/timing HOLD. Price/alternative review: $1.08domainisolationjustified.

Sources: [Manufacturer evidence](https://www.ti.com/product/TXU0202), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TXU0202DCUR/16677096), [Specification reference](https://www.ti.com/lit/ds/symlink/txu0202.pdf).



### 78. TXU0304PWR - U5

Manufacturer lifecycle evidence: TI family ACTIVE;DigiKey exact code Active.

Sourcing: **DigiKey; listed stock 13,297; $1.05/1; CT / optional reel; MOQ 1 offer observed; refresh before purchase.** Source age: today.

Role and existing limits: RADIO-009: 3 outbound + 1 inbound SPI channels; dual supply with Ioff; OE sequencing and timing closure pending

Fit/qualification screen: SPI3out1in/Ioff;OEtiming/partialpower HOLD. Price/alternative review: $1.05reasonable;autoTXS/TXBnot equivalent.

Sources: [Manufacturer evidence](https://www.ti.com/product/TXU0304), [DigiKey offer](https://www.digikey.com/en/products/detail/texas-instruments/TXU0304PWR/14641423), [Specification reference](https://www.ti.com/lit/ds/symlink/txu0304.pdf).



### 79. XGL5020-471MEC - L2

Manufacturer lifecycle evidence: Coilcraftexactcurrentproduct;DigiKey Marketplace Active.

Sourcing: **DigiKey Marketplace / Coilcraft; listed stock 722; $3.83/1; Qty-one strip; delivery/extra shipping not yet confirmed; Quantity-one price observed; stock must cover board quantity; recheck before buying.** Source age: today; direct supplier retrieval 2026-10-05.

Role and existing limits: PWR-006: 0.47uH 20%; incoming screen 0.412..0.518uH plus allocated +/-10% operating change gives 0.3708..0.5698uH. Qualification required; design/main_regulator_tps63806.md.

Fit/qualification screen: 0.47uHscreen/window/hotloss HOLD;6.4A10%dropvs15.7A30%droptyp. Price/alternative review: DirectMOQ1CT$2.55stockdynamicunconfirmed;DKmarket785$3.833wkshipaged3wk.

Sources: [Manufacturer evidence](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xgl/xgl5020/xgl5020-471/), [DigiKey offer](https://www.digikey.com/en/products/detail/coilcraft/XGL5020-471MEC/16634589).



### 80. XRCGB24M000F3M19R0 - Y1

Manufacturer lifecycle evidence: MuratafactorytransferPCN notEOL; currentspecification.

Sourcing: **Mouser; listed stock 5,705; $0.32/1; qty-one offer; confirm packaging; MOQ 1 offer observed; refresh before purchase.** Source age: 5 days ago.

Role and existing limits: Murata JGC49-3003B: 24MHz, CL6pF, ESR<=100 ohm, drive<=300uW; RA8P1 Group10 reference ESR ceiling210 ohm, not board validation. Terminals1/3; linked spare pads2/4 NC.

Fit/qualification screen: 24MHz6pFESR100ohm300uW;negativeR/stray/startup HOLD. Price/alternative review: MouserMOQ1$0.32/5705indexed5daysgoodvalue;FL2400022not equivalent.

Sources: [Manufacturer evidence](https://www.ttieurope.com/content/dam/tti-europe/products/PCN/Murata/Murata-D09089-A-D7300.pdf), [Mouser offer](https://www.mouser.com/c/passive-components/frequency-control-timing-devices/crystals/?q=XRCGB24M000F3M19R0), [Specification reference](https://pim.murata.com/asset/pim4/ceramicResonatorCrystalUnit/SPEC_XRCGB24M000F3M19R0_PDF_CERAMICRESONATORCRYSTALUNIT).



### 81. UNSELECTED - J1

Manufacturer lifecycle evidence: UNSELECTED.

Sourcing: **DigiKey; listed stock UNVERIFIED; UNVERIFIED/1; UNVERIFIED; UNVERIFIED.** Source age: UNVERIFIED.

Role and existing limits: Physical SWD connector unresolved; existing generic symbol is not a purchasable MPN

Fit/qualification screen: Select matingdebugconnector and pinout; no exactMPN/stockprice. Price/alternative review: Unknown.



## Unplaced library inventory - all 26 symbols

Archived symbols are excluded from the current buy list. A lifecycle/stock refresh is required if reconsidered; neither their existence in the library nor historical availability approves purchase. Candidates remain unplaced and unqualified.

| Exact library symbol / order code | Disposition, sourcing evidence and fit/value decision |
| --- | --- |
| Audio_Devices:BUF634AIDRBR | Current bank-study candidate; TI family Active; indexed DigiKey 779 last week, $4.45 qty-one CT (older evidence differed). Hot swing/SOA, current sharing, compensation, noise and thermal cost remain HOLD. Do not buy 16 units merely because the model runs. [TI](https://www.ti.com/product/BUF634A). |
| Audio_Devices:OPA1656IDR | Current controller candidate; TI family Active; indexed DigiKey 9,079 five days ago, $2.99 qty-one CT. Positive common-mode ceiling V+ minus 2.25 V is a material limitation; revised rails and recovery guard are documented. No audible premium claim. [TI](https://www.ti.com/product/OPA1656). |
| Connectors:12401610E4#2A | Archived unsealed USB-C candidate. Reconsider only after PD data/power/current, shield, temperature and moisture/seal requirements; no current lifecycle/qty-one/price approval. |
| Memory:IME5132SDBETG-6I | Archived alternative SDRAM. Different part/package/limits require full pin, timing, power and sourcing review if revived; not a qualified U14 substitute. |
| Memory:IS25LP01GJ-RHLE | Archived serial-memory option; current selected U15 octal NOR meets the present direction. Boot/interface/ECC/capacity and stock would need fresh review before paying for another memory architecture. |
| Memory:IS42S32160F-7TLI | Retired U14 exact code: distributor Discontinued, owner-reported Mouser NRND. Remaining stock is not a new-design justification. Not approved for new purchases. |
| Memory:MX35LF1G24AD-Z4I-T | Archived NAND option; controller/ECC/bad-block and capacity benefit over selected octal NOR/microSD not established. No current buy approval. |
| Power_Devices:BQ25188YBGR | TI exact code Active, but legacy 1 A linear charger does not cover the expanded PD/audio thermal and charging envelope. Archived pending complete power-path decision; not primary charger selection. [TI](https://www.ti.com/product/BQ25188/part-details/BQ25188YBGR). |
| Power_Devices:BQ25798RQMR | Unplaced native charger candidate, all 29 physical pins reviewed. TI exact Active; October 5 DigiKey 7,394, $5.90 quantity-one cut tape, not a 3,000-piece purchase. Integrated PD-range buck-boost merits comparison on total BOM/efficiency. Charge/reset/NTC/pack and independent desktop isolation remain HOLD: CE stops charge, SDRV cannot maintain adapter-attached isolation. Blank footprint. [Detailed review](charger_pd_bq25798.md). |
| Power_Devices:BQ27427YZFR | Unplaced gauge option; TI exact Active; DigiKey detailed indexed last-month offer 21,167/$1.97 qty-one CT (newer category snapshot differed: recheck). Integrated 7 milliohm shunt, pack capacity/chemistry/current/SOA and 50 uA typical versus 9 uA sleep need comparison. Gauge is not pack protection. [TI](https://www.ti.com/product/BQ27427/part-details/BQ27427YZFR), [offer](https://www.digikey.com/en/products/detail/texas-instruments/BQ27427YZFR/18153923). |
| Power_Devices:FDN337N | Unplaced relay-driver candidate; exact onsemi manufacturer lifecycle not confirmed, DigiKey Active. Indexed four-day offer 227,189/$0.90 qty-one CT. Do not use a cheaper UMW device with the same printed part number without qualification. Package pin map, hot gate drive, leakage, flyback and fault response remain HOLD. [onsemi offer](https://www.digikey.com/en/products/detail/FDN337N/FDN337NCT-ND/458950). |
| Power_Devices:LTC3119IUFD#PBF | ADI recommended for new designs; DigiKey reviewed 6,909/$24.07 qty-one tube. Archived main-regulator choice: voltage-upper-limit conflict and expanded thermal/current budget remain unresolved. Its 5 A headline is conditional on input/output conditions; no automatic improvement over U13. [ADI](https://www.analog.com/en/products/ltc3119.html). |
| Power_Devices:MAX17260SETD+T | Unplaced gauge alternative; ADI product present but exact manufacturer lifecycle not confirmed in this review; DigiKey Active indexed three-week offer 12,642/$4.55 qty-one CT. 5.1 uA low-power and scalable external shunt can justify higher cost for a higher-current pack; chemistry/current/noise/layout/thermal qualification required. [ADI](https://www.analog.com/en/products/max17260.html), [offer](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX17260SETD-T/9833457). |
| Power_Devices:SN74AVC8T245PWR | Front parallel-camera translator candidate; TI exact Active; indexed Oct 4 DigiKey 15,975/$1.63 qty-one CT. 1.4..3.6 V ports, VCCA-referenced controls and conditional speed do not establish CEU timing/skew/VOH acceptance. [TI](https://www.ti.com/product/SN74AVC8T245/part-details/SN74AVC8T245PWR), [offer](https://www.digikey.com/en/products/detail/texas-instruments/SN74AVC8T245PWR/864331). |
| Power_Devices:TPS22917DBVT | Legacy AON switch; historical Sept 5 8,127/$1.14 qty-one listing is not current approval. Reevaluate reverse/default/discharge requirements and current manufacturer/supplier status if revived. |
| Power_Devices:TPS22918TDBVRQ1 | Archived radio switch replaced by TPS22964C. Automotive qualification alone is not a benefit sufficient to revive a part lacking the required reverse behavior. Fresh lifecycle/stock/price review required if considered elsewhere. |
| Power_Devices:TPS3808G33DBVR | Archived supervisor threshold incompatible with present rail corner/sequence direction. Correct selected supervisors are in the placed inventory; fresh fit/source review required before any reuse. |
| Power_Devices:TPS63802DLA (default MPN TPS63802DLAR) | Archived 2 A regulator choice; not the placed U13. Do not use the shorter symbol name as a purchasable code or silently revive it for the expanded load allocation. |
| Power_Devices:TPS7A0218PYCHR | Unplaced front-camera/MIPI LDO comparison; TI exact Active; indexed two-week DigiKey 21,081/$0.83 qty-one CT. Fixed 1.8 V/200 mA, tiny four-ball DSBGA, 25 nA typical IQ under TI conditions; distributor's 60 nA field is not the same specification condition. Enable/reverse/PSRR/accuracy/hot current and package remain HOLD. [TI](https://www.ti.com/product/TPS7A02/part-details/TPS7A0218PYCHR), [offer](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A0218PYCHR/14004290). |
| Processors:R7KA8P1KFLCAB#UC0 | Archived 224-ball RA8P1; current design uses 289 balls and corresponding interfaces. Not a drop-in way to fix U1 sourcing. No buy approval. |
| Protection:RCLAMP0582N.TCT | Archived USB ESD choice; fresh clamp/capacitance/leakage/footprint/current sourcing review required if revived. ESD does not implement wet-port inhibit. |
| Protection:TPD6E004RSER | Archived ESD array; no approval to replace distributed clamps without protected-pin/SI/layout qualification and fresh source/price review. |
| Sensors:ADXL367BCCZ-RL7 | Archived orientation alternative; current selected LIS2DTW12 serves orientation/temperature. Cost/power/features and stock must be reevaluated for a defined benefit before switching again. |
| Sensors:LIS2DW12TR | Retired orientation selection after owner sourcing rejection; not the installed LIS2DTW12TR. No approval to return to the former code. |
| Timing:ABS07-32.768KHZ-1-T | Archived RTC crystal, not selected low-load ABS07-LR code. Load/ESR/startup/drive and source review required; not interchangeable by frequency alone. |
| Timing:FL2400022 | Archived main crystal replaced by selected Murata 24 MHz/6 pF option. No current lifecycle/qty-one/value approval to revive it. |

## Modules, owned hardware and not-yet-selected parts

The on-board audit does not establish a complete finished-device BOM. The following hardware must receive the same four-part acceptance review before installation/purchase:

| Item | Current state / next acceptance gate |
| --- | --- |
| Digilent 410-358 Pcam 5C / cable | Existing MIPI candidate; native connector mapping is documented. Module and exact cable stock, revision, long-term supply, power/SCCB and enclosure fit need refresh/qualification. Bare OV5640 status is not module availability. |
| Adafruit 5840 OV5640 autofocus breakout | Front CEU candidate; board-voltage translation, clock, address collision, module sourcing/revision and thermal/mechanical requirements remain open. [Interface study](camera_storage_interfaces.md). |
| Waveshare 6-inch 1448 x 1072 HD HAT / panel | Owner's prototype hardware; reuse does not prove the bare panel/controller procurement path. Production direction integrates IT8951 and support rails on-board; exact order code, released documentation, sourcing, touch, warm/cool frontlight and waveform/license support remain unresolved. [Requirements](ereader_requirements.md). |
| Battery, protection, charger and gauge | Existing protected Jauch 1S pack is a first candidate, not acceptance for high audio current/runtime. Exact pack/connector/NTC/capacity/current/aging and availability need closure. BQ25188 is not silently retained for the expanded load. |
| USB-PD/power path and wet-port hardware | TPS25751D remains a controller family to qualify; exact BQ25798RQMR is now an unplaced native charger candidate, not a selected circuit. Host power contract, weak hosts, safe defaults, charge termination, external system supply, independent full-battery isolation, pack temperature and PD/wet faults remain gates. [Charger review](charger_pd_bq25798.md). |
| DAC, I/V, volume, line output, audio clocks and output jacks | ES9039Q2M is an architecture recommendation, AK4497S the runner-up; final exact codes, quantities, prices, lifecycle, supply/clock/defaults and analog measurements are not approved by this audit. Hardware DC/fault disconnect and sealed jack selections are unfinished. |
| Bank converters, compensation parts and output protection | Exact regulators/resistors/C0G capacitors/contacts are not selected; hot continuous envelope and the common-mode/thermal correction must be closed first. |
| Flashlight, front-camera light and frontlight | Requirements retained; exact LEDs/drivers/current/thermal/optical/seal choices remain open. No unselected part can pass a stock or price check. |

## Closing the open acceptance gates

U23's detailed [MIPI LDO comparison](mipi_ldo_selection.md) rejects direct
TPS7A20/TPS731/TPS709 substitutions on reverse/startup conditions. The
preferred next candidate LT3060EDC-1.8 has a refreshed qty-one CT offer at
$4.79, but the existing 100 nF would imply about 60 ms typical startup;
timing, PHY noise and native integration remain open. U23 stays LT3042 in
this checkpoint, with the 20 mA planning allocation retained.

Before a purchase-ready BOM: obtain released U14 limits and a support horizon, close U1 transition/qty-one supply, refresh thin/stale source offers, finish the whole power budget and regulator proof, compare U23 alternatives on measured/required noise and sequencing, select C9/J1 and missing hardware, and qualify every package/footprint. Before production: loaded timing/SI/PDN, faults, sealed-case heat, ingress/condensation, battery charging and audio protection/measurements must pass. These are existing engineering dependencies, not resolved by distributor Active status.

## Checkpoint validation

Native replacements preserve complete pin-to-net membership. U14's four units contain exactly 86 unique package pins; the old/new pin numbers, names and electrical types match the reviewed manufacturer map. Per-reference native BOM fidelity is checked against a fresh saved XML netlist (305 rows, 19 columns, four native exclusions). All fifteen PDF pages are regenerated and inspected. Fresh ERC has 103 errors and 15 warnings with four existing ignored checks; those findings remain open and no suppression was added. Clock and relevant camera, power, sensor, audio-envelope/sharing/rail arithmetic checks accompany this checkpoint. Arithmetic and nominal-model results are not bench qualification.

Final verification results: complete native net partitions unchanged versus
the pre-replacement export; exact MPN coverage for all 305 included refs and
report coverage for all 25 unplaced library symbols pass. All fifteen pages
rendered; pages 1-9 and 11-15 match the prior PDF pixel for pixel, and page 10
was independently rendered with Poppler and visually inspected. Fresh saved
ERC evidence is `ereader/ERC-final.rpt`.

Passed checks: `check_clock_calculations`, `check_bom_export`,
`check_camera_budget`, `check_hall_cover`, `check_main_rail_capacitance`,
`check_lis2dtw12_candidate`, `check_sensor_bus_budget`,
`check_sensor_iic_clock`, `check_ambient_light`, `check_audio_stage1`,
`check_audio_amp_envelope`, `check_audio_power_study`,
`check_audio_buffer_sharing`, `check_audio_composite_rails` and
`check_audio_transient_metrics`. Hall inventory expectations were updated
for the actual C125 substitution; the capacitance inventory parser now
accepts the existing voltage-annotated `10u/16V` fields without treating the
voltage as capacitance. Existing historical sensor screens retain their
explicit rejected conditions; passing their arithmetic is not acceptance
of a rejected circuit. No unresolved ERC condition was waived.

Supplier-refresh checkpoint validation: fresh saved XML still covers all 305
included references and preserves the complete prior net partitions. Native
BOM fidelity passes all 19 columns; the report still covers all 25 unplaced
library symbols. All 15 PDF pages were re-exported, rendered and visually
inspected; each is pixel-identical to the prior reviewed PDF. Fresh ERC
remains 103 errors and 15 warnings with the same four ignored checks. Clock,
installed main-rail capacitance inventory and MIPI LDO inventory/arithmetic
checks pass. No circuit, native BOM selection or electrical acceptance gate
was changed by refreshing supplier evidence.

Charger-candidate checkpoint: the saved project now has 26 separately
classified unplaced symbols. BQ25798RQMR's 29 visible physical pins match
the reviewed native pin-table inventory; all older library symbols remain
unchanged. Its native SVG was rendered and inspected. Fresh XML preserves
every schematic net membership and all 305 included references/79 selected
MPNs; per-reference BOM fidelity passes all 19 columns. All 15 PDF pages
were freshly exported, rendered and inspected, and remain pixel-identical
to the prior reviewed schematic because the charger is not placed.
Fresh ERC remains 103 errors/15 warnings and the same four ignored checks.
Audio power arithmetic, installed main-rail capacitance and MIPI LDO
inventory/arithmetic checks pass; these are conditional screens, not bench
qualification. The charger review corrects the proposed source architecture:
CE/SDRV cannot deliver sustained attached-host battery isolation, and reset
charge voltage/NTC/default behavior remains HOLD.
