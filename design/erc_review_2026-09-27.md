# ERC review, 2026-09-27

Saved project: 277 components, 14 sheets. This is an unfinished electrical
design; the review does not approve manufacturing or the remaining circuits.

## Standard capacitor cache refresh

The first fresh CLI ERC reported 111 errors and 55 warnings. Forty-four
warnings were Device:C_Small cache mismatches. Read-only comparison against
the bundled KiCad 10 Device library found identical pin objects and two
differences: hidden Description position (0,-10.16 instead of 0,0), and the
lower plate stroke (0.3048 instead of 0.3302mm).

A recoverable schematic copy was made before the native KiCad operation.
Tools / Update Symbols from Library was restricted to Device:C_Small;
all instance-field updates and optional resets were disabled. No global
library was modified. Cached definitions changed on the MCU interfaces,
supplies, clocks/debug, radio, power-button, user-controls and microSD sheets.

After native save, full schematic-object comparison confirmed every
instance, component UUID, field, position, wire and other drawing object
unchanged. The orientation sheet's top-level document UUID was regenerated
by KiCad; its instances and parent-sheet hierarchy were unchanged. Fresh
XML exports before and after had byte-identical components and nets
sections. Cached pin objects also remained identical.

## Remaining findings

Fresh ERC now reports **111 errors and 11 warnings**:

| Finding | Count | Disposition |
| --- | ---: | --- |
| Unconnected pins | 107 | Unfinished root CEU integration (11), MCU allocation (82), and radio (14); resolve against subsystem and recovery requirements |
| Undriven signal inputs | 2 | MCU allocation remains unfinished; retain errors |
| Undriven power inputs | 2 | Core-sheet ground and power-control source findings remain; source implementation must justify any eventual power flags |
| Isolated hierarchical labels | 11 | CEU front-camera signals currently have only one connected pin; front-camera implementation required |
| Library mismatch | 0 | Resolved by native cache refresh |

The complete multiset of non-library violations (severity, type,
description and affected-item descriptions) is unchanged from the first
fresh run. No ERC exclusions or rules changed. A lower warning count is
not electrical completion.

Radio's open pins include UART0 RX/TX contacts 24/25 and USB contacts 13/14.
Resolve recovery access before deciding unused-pin treatment. The eleven
CEU root errors require the second camera circuit; no-connect markers
would conceal the missing implementation.

Reproduce ERC with:

```sh
kicad-cli sch erc --format json -o erc-current.json ereader/ereader_rev1.kicad_sch
```

## Published WIP checkpoint validation

The complete 14-page PDF was regenerated with the repository export script
and every rendered page visually reviewed. The native BOM export was refreshed
after clearing a temporary C11 search filter: 19 columns, 109 groups, and
274 unique included references. Every exported value and canonical MPN matches
the fresh XML netlist. TP1-TP3 are intentionally excluded; the netlist contains
277 components. Saving the BOM settings preserved all component and net records.

Fresh CLI ERC reproduced 111 errors and 11 warnings. Clock, camera bandwidth,
sensor-alternative, historical sensor-bus, and main-rail capacitance scripts ran
successfully. Their reported rejected historical candidates and conditional
results remain design findings, not test failures or electrical signoff.
Whitespace validation passed. Independent read-only review found no electrical
regression blocking this WIP checkpoint; its stale-status and BOM-filter findings
were corrected before commit. Temporary Python bytecode is excluded.

This checkpoint includes the LIS2DW12 sensor circuit and host integration,
revised held-supply/discharge draft, camera timing screen, capacitor inventory,
C9 candidate procurement record, and capacitor library-cache repair. Front-camera
hardware, recovery, power-source/USB, display/touch/lighting, audio, and final
electrical qualification remain open under epic #21.
