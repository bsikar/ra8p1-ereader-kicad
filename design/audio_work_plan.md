# Portable and desktop audio work plan

2026-10-05. Work resumed by the owner after expanded audio requirements.

**Current priority: resolve the [external architecture review](audio_external_review_2026-10-05.md).**
The BUF634A bank is now a research comparator, not the preferred production
implementation. Reopen transport, amplifier and power selection in the
EXT-A through EXT-G order before further power-bank CAD. The owner adopted
PCM768/DSD512, premium Bluetooth and the higher desktop ratings as required. RA8P1 remains system master.

The owner requested an active goal for the complete electrical schematic.
Current EXT-B work is captured in [RADIO-024](radio_sdio_migration.md): exact
SDHI0_C/WROOM pin allocation, USB alternate-function coexistence, reusable
bilateral-isolator candidate, source evidence and native migration gates.
RADIO-025 adds R114/R115 reset-edge straps, but identifies a zero-margin
host-to-C6 DC screen that must be resolved before passive-bus wiring. Fresh
stock evidence initially put the shared 10k resistor MPN on procurement hold.
RADIO-026 refreshed all 47 native instances with an indexed Mouser MOQ1
offer; purchase-time rechecking remains required. RADIO-027 rules out a
1.8 V host-bank workaround with the present 32-bit SDRAM and records the
passive translator's pull-up/current tradeoff.
The saved radio circuit remains SPI until the migration is verified; a
completed study or a clean local checkpoint does not complete the goal.


The audio study is part of the existing RA8P1 e-reader schematic objective;
display, touch, warm/cool front light, two cameras and illumination, speakers,
five buttons, sensors, storage, battery, USB-C and wet-port protection remain
required. Hardware is this task's scope. Streaming is from the owner's server;
firmware implementation and commercial streaming-service DRM are excluded.

Owner clarification: one USB-C cable to a host computer must carry USB DAC
audio and the host's available power. Negotiate PD where offered, power
playback first, and charge from remaining capacity. Stop charging a full
battery; avoid repeated maintenance cycling. Desktop capability depends on
the negotiated host budget, not the mere presence of USB. Portable demanding
headphones consume more battery energy and remain within pack/thermal limits.
An auxiliary PD inlet/dock is a fallback for weak hosts, not a prerequisite
for ordinary one-cable USB DAC use.

The owner delegated battery/runtime and packaging budgets to the designer,
wants broad conventional headphone coverage, and authorized computer control
and native KiCad work. Audio component design follows architecture selection;
GUI authorization does not bypass the requested study stages.

| Stage | Status | Concrete deliverable / completion gate |
| --- | --- | --- |
| 1. Validate requirements | Initial study committed in 998aa03; further limits may change with evidence | [Feasibility](audio_stage1_requirements.md), checked load/rail/heat math; independent review resolved intermediate-load power-cap finding. Original 2 W floor/4 W stretch/16 Vrms superseded by the owner-adopted external-review envelope; qualify continuous versus burst ratings. IEM at 8-9 ohms; no unlimited compatibility claim. |
| 2. Compare >=3 architectures | Research checkpoint reviewed; qualification gates remain | [Four conversion architectures](audio_architecture_candidates.md), complete DAC/I-V/filter/volume/line/IEM comparisons, ESS/AKM/Cirrus/TI/ADI/ladder coverage, source and procurement evidence. |
| 3. Headphone amplifier | Reopened after external review; old bank demoted | [Amplifier study](audio_amplifier_study.md), real difficult loads, integrated/composite/discrete/current-mode alternatives, low-level noise/gain, BTL/SE, SOA/heat, hardware protection and explicit continuous envelope. |
| 4. Digital platform | Reopened: SDIO, high-rate XU316 candidate and DSP return path | [Platform study](audio_platform_study.md), RA8P1+C6 vs alternatives, memory/radio/USB/DSP/I2S clock budgets, 192 kHz timing, interfaces and benchmark contracts. No firmware changes. |
| 5. Power architecture | Reopened: rail-dependent loss and source sizing | [Power tree and modes](audio_power_study.md), 20-30 Wh energy screen, 10h local/8h streaming allocations, host-powered one-cable USB DAC, PD offer-dependent output, playback-first surplus charging/full-battery charge stop, battery-isolation modes, dual rails, noise, thermal/wet-port and weak-source fallback. Exact cell topology remains open. |
| 6. Select architecture | Previous recommendation superseded in transport/power-bank portions | [Primary and runner-up](audio_architecture_selection.md): ESS differential I-V and separate quiet path retained; power stage reopened; AK4497S voltage-output runner-up. Native RA8 versus XU316 transport now compared against the proposed format targets. Host-powered PD with surplus charge/full-charge stop remains required. Current-sharing, hot swing, radio speed and sealed-enclosure thermal limits remain open. |
| 7. Component/native schematic | Bounded investigation resumed | Exact orderable parts, datasheet pin verification, corner/math checks, hardware fault handling, native GUI implementation, readable sheets and BOM. Save/export/full PDF visual review/ERC and push each coherent checkpoint. Final bank/charger wiring remains behind circuit-specific review. |
| Whole-device electrical integration | Pending subsystem completion | Reconcile pinmux, voltage domains, sequencing, power budgets and audio/digital/RF return paths with all e-reader circuits. Do not claim a manufacturing-ready board from proposal math. |

Initial portable runtime screens assume front light off and normal listening;
lighting/display activity, cameras, speaker output and high-power headphones
receive separate budgets. Mechanical heat spreading is part of feasibility
even though detailed enclosure/PCB/footprint/fabrication work remains deferred.

The Stage 6 recommendation permits bounded component investigation, with
explicit circuit-specific hold points. Current U34/K1 and the
unplaced transistor candidate stay explicitly WIP. Do not silently retain the
earlier INA1620/OPA1622 power proposal as an approved desktop architecture.
Preserve useful verified symbol assets; requalify them only if adopted.

Review artifacts are the full project PDF and native BOM. Current baseline:
15 PDF pages, 310 included physical references plus 4 BOM-excluded references,
102 ERC errors / 15 warnings after relay checkpoint 1eae855. These counts describe an unfinished design and
are not acceptance. Document-only phases need no invented native BOM changes.

Commit/push each bounded study or verified circuit phase, keep YouTrack
[RA8HW-4 audio](https://youtrack.locked.cv/issue/RA8HW-4/ereader-hw-design-high-fidelity-headphone-audio-and-music-playback-interfaces)
and [RA8HW-18 power](https://youtrack.locked.cv/issue/RA8HW-18/ereader-hw-design-USB-C-battery-charging-fuel-gauge-and-system-power-tree)
evidence current, and distinguish implemented wiring, engineering candidates
and pending measurements. Final output power, hiss, EMC, startup/stability
and physical thermal ratings require bench qualification.

Research checkpoint verification: independent read-only review reproduced
the amplifier/power scripts and found no remaining arithmetic blocker. Its
main-host PD routing finding and Cirrus mode/performance comparison were
corrected. Qualification gates remain open. Native GUI Save regenerated the
audio child sheet's internal file UUID only; symbols, instance paths, values,
wires and notes did not change. All 15 regenerated PDF pages match the prior
committed PDF pixel for pixel; fresh ERC remains 103 errors / 15 warnings.

2026-10-05 tracking change: the owner closed the GitHub issues and migrated
them to YouTrack. Use the existing RA8P1 E-reader Hardware board for ongoing
status, dependencies and acceptance evidence. Do not reopen or comment on
the closed GitHub issues. GitHub remains the code/commit remote. The overall
hardware epic is RA8HW-1; native integration/ERC is RA8HW-9 and radio transport
is RA8HW-17. Historical GitHub issue links remain provenance only.

Stage 6 checkpoint verification: the native headphone sheet now records the
one-cable host-power, surplus-charge/full-charge-off and fault-transition
requirements. No component or wire was added in this checkpoint. All 15 PDF
pages were rendered and visually reviewed; only page 15 changed, and pages
1–14 remain pixel-identical. The native 19-column BOM is byte-identical with
303 included references. Fresh ERC remains 103 errors / 15 warnings; those
are the unfinished-design baseline, not a passed electrical release. Stage 1,
amplifier, revised power and clock calculation checks pass.

Stage 7 buffer checkpoint: the native, unplaced BUF634AIDRBR candidate has
all nine package pads modeled, with the exposed pad at V-. No bank wiring,
footprint or output rating is accepted. The new
[sharing investigation](audio_buffer_qualification.md) and reproducible
`check_audio_buffer_sharing.py` replace the unsupported 25% sharing allowance
with explicit offset/ballast sensitivity screens. Typical DC output resistance
does not prove hot current sharing. Separate composite branches and the
discrete AB fallback need comparison before power-bank wiring. Final symbol
rendering was inspected; all existing library symbols are preserved.
The regenerated 15-page PDF is pixel-identical to the preceding checkpoint,
and the native BOM is unchanged. Fresh ERC remains 103 errors / 15 warnings;
clock, Stage 1, amplifier, power and sharing arithmetic checks pass. These
checks establish a recoverable investigation checkpoint, not electrical release.

Stage 7 sharing follow-up: the common-controller bank is rejected as the
wiring basis. Independently controlled gain-2 branches with an illustrative
Vishay array fail several aged 4W static-current screens. The next prototype
direction is four own-output unity composite branches per leg with upstream
gain. The script now enumerates DC/gain/ballast corners, gain-divider current,
all seven load points and an open-branch fault; the low-load unity corner is
about 200mA, conditional on an unqualified 3mV residual DC allocation.
One branch open raises that screen above 250mA, requiring hardware disconnect.
The revised 16 BUF/20 core power allocation gives 5.992W high-rail idle and
36.10/33.81/33.61W ideal input screens at 4W into 16/32/50 ohms with charge
and margin. Quiet playback keeps the bank off. Exact gain/count, hot drive,
coupled-loop stability and hardware protection are next; no native component
or wire is added in this documentation/calculation checkpoint. The existing
15-page PDF and native BOM therefore remain the current schematic artifacts.
Checkpoint verification: saved native hierarchy, exported/rendered all fifteen
pages and compared every page to the prior reviewed PDF; all pixels match.
Fresh ERC remains 103 errors / 15 warnings with four existing ignored checks.
No native schematic/library or BOM content changed. Clock, Stage 1, amplifier
envelope, power and expanded sharing calculations pass; `git diff --check`
passes. Static arithmetic is not hot-device or bench qualification.

Stage 7 compensation checkpoint: native OPA1656IDR candidate imported,
flattened, eight-pin map checked and all three units rendered. It remains
unplaced/HOLD with no footprint; the schematic wiring and BOM are unchanged.
The bounded nominal AC investigation is reproducible through
`scripts/investigate_audio_composite_ac.py`, with numerical evidence in
`audio_composite_ac_results.json`. The direct unity cell shows severe 1nF
peaking/negative apparent phase margin and inconsistent injected-loop DC
operating points. This is a compensation/model-validation HOLD, not a
certified oscillation frequency or accepted loaded amplifier. No proprietary
model files/binaries are committed. Next compare local high-frequency
feedback compensation, reconcile model operating points, then test coupled
loops and hardware fault response before native bank wiring. Hot SOA, final
noise and sealed-enclosure thermal/PD limits remain open. YouTrack RA8HW-4
owns this investigation; RA8HW-18 retains the power dependency.
Checkpoint verification: saved native hierarchy and refreshed all 15 PDF
pages. Every rendered page matches the prior reviewed PDF pixel for pixel;
native schematic files and existing library symbols are preserved, so no
physical reference/BOM content changes. Fresh ERC remains 103 errors / 15
warnings with four existing ignored checks. Clock, Stage 1, amplifier,
power and sharing arithmetic checks pass. Twelve isolated AC cases completed
at two gmin values; their status remains INVESTIGATION ONLY / HARDWARE HOLD.

Stage 7 coupled compensation checkpoint: corrected the investigation harness
to retain the actual AC bias (`.options keepopinfo`) instead of recording a
separate `.op` solution. The original checkpoint's DC values are superseded;
the regenerated twelve-case direct-feedback comparison retains severe 1nF
peaking and unreliable bias roots. Added 35 explicit compensated-cell/bank
runs and five four-port return-ratio groups, including +/-1% resistor /
+/-5% capacitor mismatch and a second gmin check. Matrix arithmetic was
cross-checked against independent analytic common/difference modes and
rejects inconsistent bias roots; individual injection columns are not
published as scalar loop margins. Numerical results and generated netlists
are committed without proprietary TI models or runtime binaries.

A 100-ohm/1nF network shows a roughly 44.723-degree weak coupled mode despite
a 61.760-degree conditional single-loop result. The next prototype candidate
is 1kohm/47pF, with 71.461 degrees weakest apparent margin at 4nF in this
nominal screen. Its MHz response still peaks and no full BTL, hot-device,
large-signal, DC-allocation or independent protection acceptance is inferred.
Corrected BUF634A table interpretation: 100/150mA headroom is 2.0/2.2V
typical and 2.2/2.5V maximum under the specified 25 C conditions, not hot
guarantees. Component-level transient/fault design is next; bank wiring
remains HOLD. See the current [qualification record](audio_buffer_qualification.md).

Checkpoint verification: native hierarchy saved; all fifteen exported PDF
pages rendered and pixel-identical to the prior reviewed checkpoint. No
native schematic/library or physical BOM change. Fresh ERC remains 103
errors / 15 warnings with four existing ignored checks. Clock, Stage 1,
amplifier, power and sharing math checks and `git diff --check` pass.

Stage 7 transient/quiet-decoupling checkpoint: archived all fourteen nominal
pulse cases, including eight complete, five timed out and one aborted. Small
10ns-edge commands show 33.6–42.3% overshoot; slower +/-5.696V pulses look
better but clipping/recovery is UNKNOWN. See the
[transient record](audio_composite_transient.md). Full bank wiring stays HOLD.
Next investigate input bandwidth/compensation and clipping/startup, then
full BTL, hot/device/fault corners and independent output disconnect.

Added native C128/C129, 10u/16V KEMET T521B106M016ATE100 bulk to provisional
quiet +/-5V rails. Negative-rail capacitor positive is at GND. Manufacturer
temperature/voltage/reverse/ripple constraints and single-unit sourcing are
in [quiet decoupling](audio_quiet_decoupling.md). Regulator/stability/startup/
footprint qualification stays HOLD. C126/C127 ceramics, DAC/I-V/line/volume,
quiet gain/rails and hardware output protection remain unfinished. This adds
no final DAC or bank and does not complete the power tree.

Verification: prior physical component fields and pin-to-net memberships
preserved. BOM now has 305 included references plus four native exclusions.
All 15 PDF pages rendered; pages 1–14 match the prior PDF pixel for pixel,
and caps/note on page 15 visually checked. ERC unchanged at 103 errors / 15
warnings, four existing ignored checks. AC/Gear regressions reproduce prior
results; known abort remains rejected. Analytic transient-metric, clock,
Stage 1, amplifier, power, sharing and BOM fidelity checks pass. Simulations/
arithmetic remain distinct from bench acceptance.

2026-10-05 sourcing and common-mode checkpoint: C126/C127 now have native
TDK 100 nF X7R source fields; their effective capacitance and placement
remain open. Portable composite-bank rails are revised from +/-5 V to an
investigation of +/-6 V for OPA1656 input common-mode; quiet +/-5 V is
unchanged. Full-bank idle/thermal/runtime penalties are explicitly screened
in [audio_composite_rails.md](audio_composite_rails.md). Historical +15 V
overstress recovery evidence is invalid; corrected +/-11 V bounded cases
timed out and remain UNKNOWN. No final bank wiring or hot rating is claimed.

The owner-requested all-parts review is in the
[component audit](component_audit_2026-10-05.md): 305 physical references,
79 selected codes, two unresolved references and 26 separately classified
unplaced/archived symbols. Native U14/R33/C95/C125 sourcing corrections
preserve connectivity. U14 released-specification/longevity, U1 transition,
U4 thin stock, high-count passive sourcing refresh, main-rail continuous
load/thermal closure and MIPI LDO value comparison are next acceptance
gates. This audit does not finish PD, battery, display, lighting, connectors
or independent headphone protection. Retain hardware work in YouTrack.

External-review checkpoint: firmware was checked at the updated 6196bf4
submodule revision. Current peripheral audio identifies UAC1 and host audio
retains the 192 kHz class limit. New calculations reproduce the proposed
high-rate packet sizes and load points, and reject the blanket 55% Class-AB
efficiency assumption for fixed high rails. Exact XU package voltage, USB
VBUS/host ownership, RA DSP return routing, Bluetooth codec roles and
benchmark distortion conditions are now explicit gates. No native component
or wire was changed. The owner explicitly accepted all three new requirement
groups after the initial review; exact parts and ratings remain unqualified. See the linked disposition and work-order record.

RADIO-026: refreshed native procurement metadata for all 47 instances of
RC0603FR-0710KL using an explicitly dated/indexed Mouser MOQ1 cut-tape offer.
This resolves the stale September snapshot without changing the resistor
type or connectivity. The DigiKey offer is out of stock. The full native BOM
and 15-page PDF were refreshed and checked; ERC identities are unchanged.
See [radio sourcing evidence](radio_sdio_migration.md#radio-026-sourcing-refresh).
Continue the SDIO electrical-interface gate and the larger audio/power,
display/camera and whole-system integration backlog; the full goal is active.

## Whole-system pin ownership checkpoint (2026-10-05)

[Saved MCU connection audit](mcu_connection_audit.md) now reports every
one of the 199 GPIO balls from the current native netlist. All 289 cached
package pins are distinct; the 199 GPIO names/balls agree with the
checked-in Renesas-derived BGA289 reference. This is a reference comparison,
not independent datasheet or alternate-function qualification.

There are 109 GPIOs with electrical peers, 79 open GPIOs and 11 named
singletons. The 11 singleton camera signals already reserve their ports;
the six planned radio SDHI0_C contacts and three historical SSI1_B audio
contacts remain physically open. Open is not permission to repurpose them.
The report explicitly carries those reservations plus the USB candidates.

Before choosing AUX enable/status or DAC controls, reconcile remaining
clock/source arbitration and all subsystem control allocations. The report
is regenerated by scripts/report_mcu_connections.py from a readonly XML
export and detects cached GPIO-map drift. No native CAD, BOM or PDF changed
in this audit. YouTrack update is pending: the exposed browser inventory
has no open YouTrack tab, and no YouTrack connector is available.

### 2026-10-05 auxiliary power-good checkpoint

Implemented R118 PG pull-up and local status labels in native KiCad;
receiver-referenced logic supply and controller integration remain open.
Verified old pin partitions unchanged, native BOM fidelity, clock arithmetic,
MCU map, and refreshed native review PDF. ERC remains at 118 findings.
Next: reconcile controller pin ownership and power-off sequencing, then
implement bounded auxiliary input and independent relay protection.
YouTrack update remains pending because no tracker tab/connector is available.

### 2026-10-05 controller ownership and shutdown gate

Reserved P107/N5 AUX request and P904/A16 polled PG status after checking
saved open-net state, recorded ownership and Renesas package/domain tables.
Rejected input-only P200 for output use. Corrected stale P106-free statements:
it is implemented microSD power request. MCU audit now carries these audio
reservations and historical optional MMC expansion contacts.
Conditional PG static margins pass; absent-VIN PG is not guaranteed valid.
Next native step is hardware main-power/request enable gating and receiver
wiring, with no unbudgeted AON/held-domain load and no MCU-only relay safety.
See audio_auxiliary_5v.md for numerical margins and sequencing conditions.
No CAD or PDF change in this ownership checkpoint; full goal remains active.

### 2026-10-05 native PG pull-up supply integration

Connected R118.1 to +3V3_MCU through an upward native power symbol and
updated its native Selection_Basis field and BOM. Readonly relay030 confirms
the only changed pin partition is R118.1 joining the MCU supply; PG still
contains U36.2/R118.2, with P904/A16 receiver wiring pending.
BOM fidelity, clock arithmetic and MCU map pass. ERC is 117 findings,
one isolated label removed and none added. The refreshed 15-page PDF has
pages 1-14 pixel-identical; page 15 and the separated C126-C129 banks
were rendered and inspected. Keep grounds below the banks and wires clear
of symbols/text in all future placements. Next: hierarchical PG receiver
connection and hardware enable/fault gating. Full implementation remains open.

### 2026-10-05 native hierarchical PG receiver connection

Implemented AUDIO_AUX_PG through the hierarchy to P904/A16. Netlist
comparison confirms only the intended receiver merge. BOM fidelity, MCU
map and clock arithmetic pass; ERC is 116 outstanding findings with no
new suppression. The refreshed 15-page PDF changed only pages 1, 2 and
15; those pages and the clean separated bypass banks were visually checked.
Next: update R118's historical receiver metadata, implement hardware
main-power/request enable gating, then bounded source and independent
headphone fault protection. Full goal remains active; no qualified working
audio supply or completed protection is claimed.

### 2026-10-05 auxiliary hardware permission and leakage review

Verified the permission takeoff must be downstream of R68, on Q3's
RUN_U13 clamp net. Upstream U16 output bypasses the independent clamp.
Compared three primary-datasheet logic candidates and recalculated loading.
An additional adverse 5 uA leakage can raise the conditional zero-raw EN
screen to 0.554934 V, above U13's 0.4 V low limit. Powered loading alone
therefore does not qualify a new gate. Resolve isolation, slow-edge behavior,
continuous control-rail thresholds and supply sequencing before native
placement. See audio_auxiliary_5v.md for equations and candidate limitations.
No new component or CAD/PDF change in this review; implementation remains
active, including R118 metadata, request hierarchy and hardware protection.

### 2026-10-05 staged permission isolation and receiver metadata

Placed Q5 DMN2056U-7 with source grounded; gate/drain remain intentionally
unfinished, visible as three new ERC errors (119 total, no suppression).
R118 metadata now reflects its implemented P904/A16 receiver. Existing
pin partitions remain unchanged. BOM fidelity and clock arithmetic pass;
PDF pages 1-14 are pixel-identical and page 15 was visually inspected,
including the cleaned bypass banks. Clarified the conditional normal main
rail bound as 3.151819680019..3.393012496197 V. Next: complete and qualify
Q5 gate network, drain pull-up, slow-edge request/permission logic and
hierarchy, then bounded source and independent headphone protection.
This is a WIP checkpoint; the complete electrical goal remains active.

### 2026-10-05 Q5 local gate pulldown

Implemented R119 1M from Q5 gate to GND. Verified saved netlist and
preservation of previous pin partitions. BOM fidelity (328 refs) and clock
arithmetic pass; ERC is 117 outstanding findings without suppression.
PDF page 15 refreshed and visually checked; pages 1-14 unchanged.
Conditional loading calculations for the planned series feed are recorded
in audio_auxiliary_5v.md. Next: series feed and permission hierarchy,
drain pull-up/request logic, bounded source and independent protection.
The full design goal remains active.

### 2026-10-05 native permission series input

Placed and wired R120 1k to Q5 gate/R119 and added MAIN_RUN_PERMIT
hierarchical input. Source export and parent/root connection remain open;
no main shutdown loading has yet changed. Prior pin partitions preserved.
BOM fidelity (329 refs) and clock arithmetic pass. ERC is 119 outstanding
findings without new suppression. PDF page 15 refreshed and visually
checked; pages 1-14 unchanged. Next: complete source hierarchy, then
permission drain pull-up/request logic and independent fault disconnect.
The complete design goal remains active.

- 2026-10-05 permission source export: MAIN_RUN_PERMIT output label now joins
  the clamped RUN_U13 net and has a parent main-supply sheet output pin.
  relay035 proves every component-pin partition unchanged. Audio input parent
  pin/root wiring and root audio block enlargement remain unfinished; R120.1
  is still isolated. ERC 121 (104 errors, 17 warnings); PDF refreshed and viewed.

### 2026-10-05 root permission connection checkpoint

Implemented the audio MAIN_RUN_PERMIT parent input and root wire from the
main-supply output through the open gutter. Saved relay038 netlist proves
the only component-pin partition change is R120.1 joining Q3.3, R68.2,
R69.2 and U13.A1. The upstream U16 output is not bypassing the Q3 clamp.
Component references were preserved after undoing a replacement-sheet
attempt that triggered automatic reannotation. ERC now reports 118 findings;
no unfinished circuit was suppressed. Clock arithmetic checks pass.
The full 15-page PDF was refreshed; root and audio pages visually inspected.
The root audio sheet box remains too small and its text crowded: corner drag
did not take effect through the current computer-control interface. This
layout item remains open. Q5 drain pull-up, request qualification, bounded
power source and independent headphone protection remain unfinished.
The full electrical implementation goal remains active.

### 2026-10-05 readable root hierarchy and drain pull-up checkpoint

The root audio sheet box is enlarged to 53.34 x 26.67 mm; the saved
aligned power-good port and root wires were verified to preserve every
component-pin partition. The earlier crowded-box layout item is resolved.

R121 10k is now wired from +3V3_MCU to Q5 drain. Saved relay041 verifies
the connection and preservation of all previous pin partitions. Native BOM
fidelity passes for 330 included references and four exclusions; clock
arithmetic passes. ERC remains WIP with 117 outstanding findings and no
new suppression. The refreshed full 15-page PDF was visually checked on
the root and audio pages. Next: supply-valid startup/brownout inhibition,
request logic and output-low qualification, then bounded source connection
and independent headphone fault protection. The full goal remains active.
