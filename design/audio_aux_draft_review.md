# Isolated AUX electrical draft

Status: NATIVE_DRAFT_PROGRESS. All source acceptance, integration, production, physical, disposition coverage and full-goal flags remain false.

This pinless root review island contains the exact sealed source union: 259 components, 289 source pin rows, every passive endpoint and 17 UNFULFILLED provider obligations. AD_RETURN has no connection to system GND. AUX5V and the IV/QUIET/LINE 5V input boundaries remain distinct. New footprints are blank; all prior components, libraries, project settings, physical fields and old pin partitions are frozen.

The original catalog-style layout was held during visual review. The four circuit pages were replaced with local switching/rectifier paths, shared capacitor rails, feedback dividers, regulator decoupling and complete Form B discharge resistor chains. Upright 50mil fields and moved long boundary aliases corrected subsequent readability findings. The source ledger and net partition did not change.

Native baseline: 356 components, 378 nets, 16 sheets, 352 BOM rows, 95 errors and 16 warnings. Final hierarchy: 615 components, 577 nets, 21 sheets and 611 BOM rows. The standalone draft has 43 errors and 162 warnings: 26 representative open parent-port reports, source-open RT/SS, 15 undriven supply/return representatives, and 54 external LED nets with three isolated-label diagnostics each. All 72 non-return parent ports are independently verified physically open. The failing release ERC exit code is retained; no PWR_FLAG, provider driver, exclusion, suppression or no-connect mark is added.

Exact draft diagnostic tuples were frozen while detached before the final whole-hierarchy export. Existing RUN_U13/MAIN_RUN_PERMIT produces one old multiple-name warning whose representative can vary among three frozen RUN_U13 labels. The gate witnesses only those UUIDs at their exact old positions and the unchanged old endpoint partition; every other tuple remains exact. Negative cases reject an outside UUID, changed name/position or additional warning.

Independent entry point: scripts/check_audio_aux_draft.py. With an evidence directory containing the fresh baseline and source directory, --native regenerates XML/ERC/BOM/PDF and verifies source hashes, exact endpoints and frozen old fields; --self-test exercises semantic rejections; --visual renders all21 pages and proves every old circuit body pixel-identical with explicit titleblock/root-review masks; --privacy scans all reachable Git objects, staged/working files, PDFs and recursive archive entries against configured private values without exposing them. Source arithmetic and12 primary PDF hashes are replayed read-only. The checked-in source snapshot contains only public source URLs.

Evidence remains outside Git in the owning worker artifact directory. No provider or full-system acceptance is inferred from this draft. Main merge and publication belong to the root integration gate.
