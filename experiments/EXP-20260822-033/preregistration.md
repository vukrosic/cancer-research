# EXP033: ARID1A damaging proxy to ATR dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined ARID1A damaging proxy
associated with more negative source-specific ATR dependency than ARID1A-matrix
intact models, within lineages containing both statuses?

This tests transportability of a reported ARID1A-defect/ATR-inhibitor
synthetic-lethal mechanism. A damaging matrix value is not equivalent to
biallelic loss, functional ARID1A loss, replication-stress state, or
pharmacologic ATR inhibition.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `ARID1A (8289)` matrix value `1` or `2`.
- Reference: `ARID1A (8289)` matrix value `0`.
- Target header: `ATR (545)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No ATR score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and `selection_seal.json`
before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based signed delta for ARID1A damaging
versus matrix-intact models, then pool lineage numerators and denominators
within source. More negative means lower ATR dependency score in the damaging
group.

The nominal gates are pooled delta <= -0.20, lineage-stratified permutation
p <= 0.05, bootstrap upper bound < 0, at least five negative lineages, and no
lineage delta > +0.20. The result is permanently `FEASIBILITY_ONLY`; planning
power is `0.8666` for Avana and `0.5810` for KY.

## Repeats and claim boundary

Use 100,000 null permutations, 10,000 bootstrap replicates, planning seeds
20263300/20263400, and inference seeds 20273300/20273400. No source pooling,
raw cross-source score comparison, functional ARID1A claim, ATR-drug claim,
DNA-damage or replication-stress mechanism claim, pharmacologic claim,
treatment claim, clinical claim, or confirmatory claim is permitted.

## Source

Williamson et al., *Nature Communications* (2016):
https://www.nature.com/articles/ncomms13837
