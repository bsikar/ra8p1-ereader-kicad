# KiCad library standards

## Project structure

Each board is an independent KiCad project. Components are shared by function,
not by the board that first used them. Do not install these parts into global
user libraries.

```
ra8p1_kicad/
  libs/
    symbols/<Category>.kicad_sym
    footprints/<Category>.pretty/<Footprint>.kicad_mod
    3dmodels/<Category>.3dshapes/<Model>.step
  ereader/
    ereader_rev1.kicad_pro
    ereader_rev1.kicad_sch
    ereader_rev1.kicad_pcb
    sym-lib-table
    fp-lib-table
  resources/                 Manufacturer references and source packages
  design/                    Electrical requirements and design rationale
```

Both `.step` and `.stp` model suffixes are accepted. Preserve manufacturer
filenames, especially where a model is shared between device families.

The categories are `Processors`, `Wireless`, `Memory`, `Power_Devices`,
`Connectors`, `Protection`, `Timing`, and `Sensors`. Add a category only when
the first actual part requires it. A future Gaggia project belongs in its own
board directory and can register these same libraries; do not duplicate parts.

## Portable references

Register symbols and footprints in each board's project-local tables:

```
Symbol library: ${KIPRJMOD}/../libs/symbols/Processors.kicad_sym
Footprint library: ${KIPRJMOD}/../libs/footprints/Processors.pretty
Model: ${KIPRJMOD}/../libs/3dmodels/Processors.3dshapes/<filename>.stp
```

Symbol footprint properties use `Category:Footprint`, for example
`Processors:BGA289C65P17X17_1200X1200X138`. Every reference must resolve from
the board directory. Do not retain old library aliases after moving parts.

## Schematic appearance

The visual style follows the relevant [KiCad library conventions](https://klc.kicad.org/):

- Pin names, pin numbers, reference and value text: 50 mil (1.27 mm).
- Body stroke: 10 mil (0.254 mm), solid, with body-background fill for ICs.
- Pin length: 150 mil (3.81 mm) by default. Use 200 mil (5.08 mm) consistently
  throughout a symbol when its imported pin numbers exceed three characters.
- Connection endpoints on a 100 mil (2.54 mm) grid; rows spaced at 100 mil.
- Pin-name offset: 20 mil (0.508 mm).
- Reference above value, centered above the body; hidden metadata at the origin.
- Body width accommodates the longest opposing pin names plus a clear gap.
  Body height follows its pin rows. Consistent style does not mean identical
  rectangle dimensions regardless of function.
- IC units use a shared top datum so fields align between units of different
  heights. This is a project-specific placement convention, not a claim of
  complete upstream KLC compliance.
- Crystals retain conventional resonator graphics; never replace them with a
  generic IC rectangle merely to make all parts look identical.

Split large ICs into non-interchangeable functional units when that improves
readability. Use normal reference suffixes (`U1A`, `U1B`, etc.), an internal
functional heading, and exactly one occurrence of each package pin across all
units. Do not duplicate supply pins in every unit. Units remain one physical
component with one footprint and one BOM entry.

Use `U` for ICs, `J` for connectors, `D` for protection arrays, and `Y` for
crystals. Preserve part numbers and manufacturer descriptions. Before electrical
acceptance, Datasheet fields must identify manufacturer documents or valid
project-relative references. Inherited product-page and distributor links are
preserved by the appearance cleanup and remain unverified source metadata.

Use KiCad 10 native pin stacks for internally shared package connections when
this improves readability. Bracketed pin numbers such as `[3,4]` represent
both physical pads, not a new pad named `3,4`. Keep all stack numbers visible;
do not combine independent signals or unconnected package pins into a stack.
This follows [KLC S4.3](https://klc.kicad.org/symbol/s4/s4.3/) and requires
KiCad 10's [pin-stack support](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#pin-stacks).

## Electrical and mechanical acceptance

Use standard KiCad `Device` primitives for ordinary passives and `power`
symbols for global supplies and ground. Register the bundled libraries with
`${KICAD10_SYMBOL_DIR}` in the project table; do not modify the user's global
libraries or create substitute resistor/capacitor/inductor graphics. Cached
symbols in each schematic preserve its rendering when opened elsewhere.

Draw decoupling banks with visible common rail and return wires, junctions at
actual branches, and named pin-pair placement notes. Power arrows point up,
grounds point down, and signal paths normally flow left to right. Use local
labels for sheet-local signals and hierarchical pins for inter-sheet signals;
avoid replacing visible short connections with repeated labels.

`PWR_FLAG` is an ERC source declaration, not a supply name or a substitute for
a regulator. Place it only at a justified source or after a passive element
that separates the source's power-output pin from the powered net. State the
source beside any non-obvious flag. Do not flag an unimplemented supply just
to suppress an undriven-power error. Never hide unfinished wiring with
no-connect markers or globally weaken ERC rules.

Appearance cleanup is not electrical qualification. Untouched imported units
retain unverified names and passive/unspecified electrical types, including
unusual ESP32 ground sub-pad numbering. The selected 289-ball RA8P1 core,
DCDC, I/O-supply, and analog units have explicit power-pin names and types
checked against its pin list; this does not qualify the remaining units or
their footprints. The four DCDC VLO contacts are one shared output group and
must connect to the same inductor-input net. Keep A7 as the group's
`Power output` pin and model A8, B7, and B8 as `Passive`; this preserves every
visible package contact while avoiding three false power-output-to-power-output
ERC conflicts. This is a symbol-modeling choice only: it does not imply that
the four contacts may use separate nets. Check each remaining symbol against
its exact ordering-code
datasheet before wiring, and qualify footprints before PCB work. Do not infer
safety from an ERC result on all-passive imported symbols.

The 289-ball USB/MIPI unit now uses normalized manufacturer pin names,
power-input types for its nine supply/ground pins, and bidirectional types
for the four USB data pins. USBHS_RREF remains passive for its external
reference resistor. The six unused MIPI lanes currently have bidirectional types;
their explicit no-connect treatment is not qualification for active MIPI use.
CMS-013 now connects VCC18_MIPI R2 to +1V8_MIPI with local C111 bypass;
camera-lane types and connections still require active-interface review.
Authority: RA8P1 Datasheet Rev.1.30 Table 1.17; RA8x2 Quick Design Guide
Rev.1.10 Tables 1-2; RA8P1 HUM Rev.1.30 section 21.4 for unused MIPI.

The BGA289 unit H GPIOs PD01 (B16), PD02 (B17), PD03 (C15),
PD04 (C14), PD05 (C16), PD06 (C17), and PD07 (E15) use
`Bidirectional` electrical types rather than the imported `Passive` types.
Authority: `firmware/docs/reference/ra8p1-datasheet.pdf`, Rev.1.30,
Table 1.16 (Pmn general-purpose I/O; P200 is the input-only exception)
and Table 1.17 (BGA289 ball assignments). Pin numbers, names, geometry,
and alternate functions were not edited. U1 schematic instances were
updated through KiCad; native ERC remains 113 errors and 11 warnings.
This qualifies these seven base GPIO types, not the remaining imported
pins or all peripheral alternate functions.

The same datasheet checks establish `Bidirectional` base GPIO types for
unit G PB00 (E16), PB01 (D17), PB02 (E13), PB03 (D16), PB04 (D13),
PB05 (D15), PB06 (E14), PB07 (D14), and PA07 (G4). These nine imported
`Passive` types were corrected through the KiCad pin table and propagated
to U1 schematic instances. Native ERC remains 113 errors and 11 warnings.
Other unit G pins with peripheral-specific output types remain subject to
review against their intended use and selected alternate functions.

Units E and F have 42 further base GPIO types corrected from `Passive`
to `Bidirectional`, using the same Rev.1.30 Tables 1.16 and 1.17:

- Unit E: P600-P606 and P700-P715 (23 pins).
- Unit F: P805-P807, P809-P812, P902, P904-P908, and P910-P915 (19 pins).

Each ball assignment was checked against the BGA289 column before editing
the native KiCad pin table. The symbol retains 289 pins without duplicates.
U1 schematic instances were updated with alternate-function reset disabled;
ERC remains 113 errors and 11 warnings. Existing peripheral-specific input
and output types were not included in this pass and stilFinal GPIO pass and handoff (2026-09-25): all 13 units A-M were inspected
for this pin-type pass. Additional corrections, using the same datasheet:

- Unit B: P000-P015 and P106-P111, Passive to Bidirectional (22).
- Unit C: P206, P207, P304-P306, P308, P312 to Bidirectional (7);
  P200/C5 to Input, per the manufacturer input-only exception (1).
- Unit D: P400-P405, P407-P415, P500-P502, P511-P515 to
  Bidirectional (23).

Total GPIO changes against the starting revision: 110 Passive to
Bidirectional and one Passive to Input. P808/U5 was restored to its
existing Output type during final diff review. No pin names, numbers,
geometry, or alternate definitions changed in the library diff.
Final native ERC: 114 errors and 11 warnings; see ereader/ERC-final.rpt.
Typing P200 as Input exposes its unfinished undriven connection in
addition to its existing unconnected-pin finding. This is not suppressed.
The pass does not qualify every peripheral alternate, active MIPI use,
unused-pin treatment, or unfinished circuits. Existing CEU integration,
USB wiring, power-source and other schematic issues remain open.
Work stops here at the owner request; no PCB design was performed.

l require review.

New design net labels use `COPI`, `CIPO` and `CS` instead of legacy SPI terms.
Review imported pin-name aliases against manufacturer documentation before
renaming them; visual normalization must not silently change their identity.

The project-local `Power_Devices:LTC3119IUFD#PBF` uses 21 visible pin objects
representing all 29 QFN pads exactly once. Its PVIN, PVOUT, SW1, SW2 and PGND
stacks follow the internal connections in ADI's
[3119fb Rev B, pages 2 and 11-13](https://www.analog.com/media/en/technical-documentation/data-sheets/3119fb.pdf).
The exposed pad is PGND pad 29. VCC is a separate internal-bias output, not
PVOUT; SVCC is a power input that must connect to VCC. PGOOD is open collector.
SW1/SW2 and BST1/BST2 are passive electrical abstractions for switched analog
nodes, not missing supply drivers that need arbitrary power flags. NC pads
24, 26 and 27 remain separate visible passive pins because ADI permits either
leaving them open or grounding them. Use explicit no-connect markers when
leaving them open in a circuit. Uniform 200 mil legs accommodate the stacked
numbers. Sourcing fields identify the exact I-grade QFN ordering code and a
dated, unreserved distributor snapshot. The library pin-map check does not
qualify the external loop, shutdown, source protection, thermal design or
footprint; circuit integration is tracked separately in
[#825](https://github.com/bsikar/ra8-firmware/issues/825).

Footprints and 3D models describe physical dimensions, not schematic styling.
Preserve pad numbers, pad sizes, pitch, mask/paste settings, courtyard,
silkscreen, keepouts and model transforms during a library move. Validate
those separately against manufacturer drawings before PCB layout.

## Change checks

1. Preserve a recoverable copy before bulk conversion.
2. Compare complete pin inventories before and after, including pin number,
   name, electrical type, graphic type, visibility and alternate functions.
3. Confirm all symbol-to-footprint and footprint-to-model paths resolve.
4. Compare footprint geometry and model bytes against the source.
5. Export every unit with KiCad and inspect the rendered graphics.
6. Update schematic library IDs and cached symbols together. Existing wired
   sheets require a connectivity-preserving migration, not blind replacement.
7. Remove superseded libraries only after the replacements and references pass.

Version the hardware project, local libraries, references, and complete
schematic PDF together. Exclude machine-local KiCad state and editor history.
Use Git LFS for reference archives exceeding GitHub's regular file-size limit.
Keep project and library files directly editable after a normal clone.
