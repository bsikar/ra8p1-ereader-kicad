# C9 core-regulator bulk capacitor

CORE-C9-001, 2026-09-27. C9 remains 47uF on MCU_VCORE with
Procurement_Status HOLD. A candidate is now recorded in its native KiCad
Selection_Basis and Sourcing_Snapshot fields. It is not yet promoted to
the canonical manufacturer part number or purchase BOM.

Candidate: **Murata GRM32ER71A476KE15K**. The manufacturer's
[GRM32ER71A476KE15-04CA reference sheet, January 10, 2025](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71A476KE15-04CA.pdf)
specifies 47uF +/-10%, 10V, X7R, -55..125C and 1210 size.
Body dimensions are 3.2 +/-0.3 by 2.5 +/-0.2 by 2.5 +/-0.2mm.
K is the 4000-piece reel packaging code; L is the 1000-piece reel code
for this same manufacturer control code. This does not establish electrical
equivalence to the older 6.3V E20 reference component.

[DigiKey candidate page](https://www.digikey.com/en/products/detail/murata-electronics/GRM32ER71A476KE15K/16034240),
observed 2026-09-27: Active, 1595 unreserved, 17-week standard lead time,
USD0.98 at quantity 1 and USD0.43690 at quantity 100. Cut-tape ordering
code is 490-GRM32ER71A476KE15KCT-ND. An earlier search result showed
13123; the opened page's 1595 supersedes that indexed count. Stock and
price are observations, not reservation or manufacturer lifecycle guarantees.

Historical hold: on 2026-09-05 the native field recorded Mouser stock7034
and an End of Life flag for GRM32ER70J476KE20L, conflicting with DigiKey's
indexed Active/zero-stock result. Do not erase this history by presenting
the E15 candidate as a renamed E20 part.

Initial-tolerance arithmetic is 47*(1-0.10)=42.3uF and
47*(1+0.10)=51.7uF. These are measurement-condition endpoints, not
guaranteed effective capacitance at the core voltage. The X7R temperature
classification alone does not establish a combined DC-bias, aging and
temperature bound.

Before final selection, compare manufacturer DC-bias/impedance data against
the actual RA8P1 core-voltage range and the allowed output network in the
Renesas hardware manual. Verify L1, the twelve 220nF local bypasses and C9
as one regulator output network, including startup and transients. A higher
voltage rating by itself is not proof of loop compatibility. Obtain the
applicable manufacturer approval specification before procurement.

This pass changes hidden metadata only; value, connectivity, drawing and
the existing purchase hold remain unchanged. The main-rail inventory must
continue to identify C9's canonical MPN as unspecified until selection is
approved electrically.
