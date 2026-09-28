# Main-rail capacitance inventory

PWR-CAP-001, 2026-09-27. Saved native project exported to
C:/work/main-cap-audit.xml; 277 component records. This inventory supersedes
the nominal totals in the earlier TPS63806 migration record for the current
schematic. It does not replace the 1mF effective-capacitance acceptance limit.

Reproduce from a fresh export:

```sh
kicad-cli sch export netlist --format kicadxml -o main-cap-audit.xml ereader/ereader_rev1.kicad_sch
python scripts/check_main_rail_capacitance.py main-cap-audit.xml
```

The script reads saved connectivity and capacitor values, groups exact
ordering codes, and verifies the known FB1 and key-filter connections. It
does not read unsaved GUI state, infer capacitor tolerance from a nominal
value, or write CAD. Counts include exported components regardless of DNP;
an assembly-variant audit is separate. Capacitors must have two exported
pads and recognized values or the script fails rather than silently omitting
them. This check does not discover arbitrary reverse paths through ICs.

## Current direct inventory

| Parts | Nominal per part | Count | Nominal total |
| --- | ---: | ---: | ---: |
| TDK C1608X7R1H104K080AA | 0.1uF | 50 | 5uF |
| Murata GRM188R72A104KA35D, C117/C118 | 0.1uF | 2 | 0.2uF |
| TDK C1608X7R1H103K080AA, C41 | 0.01uF | 1 | 0.01uF |
| TDK C3216X7R1V106K160AC, C47/C88/C92/C102 | 10uF | 4 | 40uF |
| Panasonic EEE-FN1C100R, C115 | 10uF | 1 | 10uF |
| Samsung CL32B226MOJNNNE, C74/C75/C94/C108 | 22uF | 4 | 88uF |
| Murata GRM31CR70J226KE19L, C3 | 22uF | 1 | 22uF |
| Panasonic EEE-FP0J470AR, C42 | 47uF | 1 | 47uF |
| Panasonic EEF-JX0J151RF, C99/C100 | 150uF | 2 | 300uF |
| **Direct +3V3_MCU total** | | **66** | **512.21uF** |

C43 adds 10uF through FB1 on +3V3_USBHS_A: direct plus ferrite branch
is 522.21uF nominal. The previous 469.21uF direct migration inventory
is 43uF below the current saved inventory. Use the exported reference list
when reconciling later additions; do not carry the older total forward.

## Storage on other paths

| Net or path | Nominal storage | Treatment |
| --- | ---: | --- |
| Four button RC filters behind R27-R30 | 0.40uF | Separate resistor-limited discharge tails; already associated with a return-current allocation |
| +3V3_RADIO | 10.30uF | Through U4; verify switch state, reverse current and module-internal storage |
| VDD_SD | 22.10uF | Through U17; card-internal storage is additional and unspecified |
| +1V8_MIPI | 22.10uF | U23 regulator output; assess reverse path rather than treating as direct 3.3V capacitance |
| MCU_VCORE | 49.64uF | MCU internal regulator output; C9 has no canonical manufacturer ordering code in this export |
| AON_HOLD | 880.30uF | Separate control hold-up reservoir; not direct main-rail storage |
| SYS_AON | 32.30uF | Upstream source storage; not direct main-rail storage |

The sums above cover explicitly drawn capacitors only. J3.15 feeds the
external Pcam module directly from +3V3_MCU; its capacitance and discharge
behavior are absent from the native component sum. J1.1 is debugger VTref;
external debugger backfeed must also be bounded. The future display, audio,
front camera, illumination and additional sensors can consume both the
capacitance and injection budgets and must be added before system acceptance.

## Consequences for power-cycle qualification

The nominal 522.21uF subtotal neither proves nor contradicts a 1mF maximum
effective total. Do not use 477.79uF as qualified remaining headroom:
tolerance, reflow, temperature, aging, service variation and external loads
are not bounded by this inventory. C115's separate conditional upper screen
of 17.16uF is already part of the total limit, not an allowance outside it.

For the existing shutdown calculation to apply, establish maximum charge
released into the main node by all connected storage and source paths.
Keep the key-filter return budget separate to avoid counting its same
stored charge both as direct capacitance and as injected current. Regulator
outputs and switched loads need state-dependent analysis throughout rail
collapse, not just powered-off leakage at zero volts. The 880.3uF nominal
held reservoir supports shutdown control and is intentionally modeled on
its own rail; treating it as another direct load would be incorrect.

Next acceptance work: per-family effective upper bounds; Pcam and other
external-load storage; U4/U17/U23/MCU reverse-path review; source-stop delay;
and validation of the 2.5mA aggregate return/injection ceiling. Existing
sensor hold-time arithmetic remains conditional until these are established.
No native wiring or capacitor value changed during this audit.

## PWR-CAP-002: Pcam shutdown constraints

2026-09-27. The saved XML confirms J3.15 and U24.5 share +3V3_MCU;
J3.11, U24.4 and R97.1 share the module PWUP net, with R97.2 grounded.
PWUP therefore controls the module's enable input, not isolation of its
3.3V input. Neither a low PWUP nor an asserted host reset removes the
module input capacitors from the main rail.

The text of Digilent's [Pcam 5C schematic, 500-358 C.0, 2017-10-18,
sheet 1](https://digilent.com/reference/_media/reference/add-ons/pcam-5c/pcam_5c_sch.pdf)
identifies IC5 as LP5907MFX-1.8/NOPB and IC6 as LP5907MFX-2.8/NOPB.
Module reference designators in this section are not host-board references.
The extracted text is insufficient to verify every capacitor's connected
rail. The PDF screenshot tool returned no usable image and the direct
download was denied; retain the unquantified external-module entry above
until the actual wiring and populated assembly revision are inspected.
Do not add an inferred module subtotal to the script's native-only sum.

[TI LP5907 SNVS798Q, July 2025](https://www.ti.com/lit/ds/symlink/lp5907.pdf)
establishes these relevant limits:

- Section 5.1, note 2: absolute maximum OUT voltage is the lesser of
  IN + 0.3V and 6V. This is a stress limit, not a reverse-blocking guarantee.
- Section 5.5: automatic output discharge resistance is 230 ohm typical,
  with EN below VIL; no maximum resistance is supplied in that row.
- Section 6.4.2: there is no dedicated UVLO and internal circuitry is not
  fully functional until IN reaches 2.2V.
- Section 5.5: EN-low <=0.4V and EN-high >=1.2V apply at IN=2.2..5.5V.

Consequently, the shutdown proof cannot extend the enable thresholds or
typical discharge behavior down to the sensor's 90mV discharge target.
It also cannot treat these regulators as ideal reverse-blocking switches.
The following checks are required for this already-connected module:

1. Inventory the populated module's input, 1.8V, 2.8V and sensor-core
   capacitors separately, including their maximum effective charge.
2. Establish hardware PWUP-low timing for forced shutdown and brownout,
   including the interval where U24 loses its valid supply. Firmware
   shutdown alone does not cover a hung host.
3. Check both regulator OUT-IN waveforms throughout collapse against the
   0.3V stress limit; bound returned charge/current without assuming the
   typical output discharge remains active below 2.2V.
4. Include SCCB, MIPI and any connected auxiliary signal injection in the
   aggregate return budget. A regulator-only calculation does not cover
   signal-pin paths.

These are acceptance conditions, not observed failures of the module.
Keep the existing 1mF/2.5mA system screen conditional. No capacitor total,
native connection, or ERC disposition changes in PWR-CAP-002.

## PWR-CAP-003: switched radio and SD storage

2026-09-27. The netlist confirms U4 A2/B2 on +3V3_MCU and A1/B1
on +3V3_RADIO; U17 pin 2 on +3V3_MCU and pin 5 on VDD_SD. The
inventory script now checks these connections before reporting a combined
storage subtotal. This makes branch omission visible if the topology changes.

[TPS22964C SLVSBS6A, section 11.1.4](https://www.ti.com/lit/ds/symlink/tps22964c.pdf)
permits reverse conduction when enabled. Reverse protection requires the
switch disabled and either VIN or VOUT above 1V. This agrees with RADIO-019;
its output capacitors cannot be excluded solely on the part's protection
feature. ON-state collapse and the below-1V interval remain relevant.

[TPS22950x SLVSFJ2B, section 9.3.4](https://www.ti.com/lit/ds/symlink/tps22950.pdf)
includes TPS22950C in its reverse-blocking description. Enabled operation
allows reverse current before threshold detection and turn-off delay;
the narrative threshold is about 900mA. Pulling ON low enables continuous
reverse blocking. Do not equate this with zero transient return current
or use the typical response as a guaranteed charge bound.

The native nominal storage totals are now reported as:

| Included branches | Nominal capacitance |
| --- | ---: |
| Main rail and FB1 | 522.21uF |
| Radio output | 10.30uF |
| SD output | 22.10uF |
| Combined stored-capacitance subtotal | **554.61uF** |

This is an inventory of separately stored charge, not an equivalent single
RC network. Radio-module and card-internal storage are still additional.
No maximum effective-capacitance claim follows from nominal values. For
the forced-off analysis, either establish each branch's isolation timing
and bounded returned charge or include its maximum stored charge in a
time-dependent discharge model. Counting a branch as both added capacitance
and an independent full-charge injection would double count it.

The selected 1mF effective limit and 2.5mA return allocation are unchanged;
the new subtotal does not qualify them. No native CAD changed in this pass.
