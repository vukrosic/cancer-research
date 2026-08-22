# EXP030: composite BRCA1/2 proxy to CIP2A dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a composite damaging proxy defined by
BRCA1 or BRCA2 matrix damage associated with more negative source-specific CIP2A
dependency than models intact for both BRCA1 and BRCA2, within lineages that
contain both statuses?

This tests transportability of a reported BRCA–CIP2A/TOPBP1 synthetic-lethal
mechanism. The matrix proxy is not equivalent to biallelic deletion, HRD,
functional BRCA status, or a clinical biomarker.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `BRCA1 (672)` or `BRCA2 (675)` has damaging matrix value `1` or `2`.
- Reference: both BRCA1 and BRCA2 matrix values are `0`.
- Target header: `CIP2A (57650)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No CIP2A score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and
`selection_seal.json` before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based signed delta for composite damaging
versus matrix-intact models, then pool lineage numerators and denominators
within source. More negative means lower CIP2A dependency in the composite
damaging group.

The nominal gates are pooled delta <= -0.20, lineage-stratified permutation
p <= 0.05, bootstrap upper bound < 0, at least five negative lineages, and no
lineage delta > +0.20. The result is permanently `FEASIBILITY_ONLY`; planning
power is `0.6686` for Avana and `0.4355` for KY.

## Repeats and claim boundary

Use 100,000 null permutations, 10,000 bootstrap replicates, planning seeds
20263000/20263100, and inference seeds 20273000/20273100. No source pooling,
raw cross-source score comparison, functional BRCA claim, HRD claim, causal
synthetic-lethal claim, pharmacologic CIP2A claim, treatment claim, or clinical
claim is permitted.

## Source

Adam et al., *Nature Cancer* (2021): https://www.nature.com/articles/s43018-021-00266-w
