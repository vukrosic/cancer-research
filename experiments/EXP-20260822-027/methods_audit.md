# EXP027 methods audit

## Selection gate

Selection used only frozen input hashes, metadata joins, the ARID1A damaging matrix column, the EZH2 endpoint header identity, literature metadata, and seeded synthetic planning simulations. The target score column was not parsed beyond confirming that `EZH2 (2146)` exists exactly once in the endpoint header. The selection artifacts are therefore outcome-free.

## Context construction

Eligible screens are filtered by the frozen QC flags and library names. Screen IDs are joined exactly to Model IDs, and lineage is taken from `Model.csv`. Multiple eligible screens for a source/model are retained as sorted screen IDs and later median-collapsed only after the pre-endpoint receipt. The canonical roster contains 1,290 source/model rows: 975 Avana and 315 KY.

## Design sensitivity

Planning uses the same lineage-stratified rank-delta estimator as the execution analysis. Null scores are independent `Normal(0,1)` draws and the alternative gives damaging models a mean shift of `-0.358286909243`, with separate PCG64 streams per source. The frozen rejection quantile is NumPy's linear 0.05 quantile of 100,000 null draws. Simulated power is 0.8643 for Avana and 0.5716 for KY; the paired record is feasibility-only.

## Audit constraints

- No source pooling is permitted.
- No target-specific threshold, lineage exclusion, or post hoc exposure redefinition is permitted.
- No negative or positive result can upgrade the feasibility-only label.
- No raw score comparison across Avana and KY is permitted.
- Any input, schema, identity, coverage, canonical-roster, or manifest drift is a non-evaluable stop, not a result.

## Reproducibility

The implementation must bind the selection seal, canonical roster digest, design receipt, frozen input hashes, `pyproject.toml`, `uv.lock`, and its transitive engine module before endpoint values are read. An independent audit must recompute context, design, endpoint, inference, artifact, and terminal-claim receipts from the committed repository.
