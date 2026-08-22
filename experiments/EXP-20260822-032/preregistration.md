# EXP032: SMAD4 damaging proxy to AURKA dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined SMAD4 damaging proxy
associated with more negative source-specific AURKA dependency than SMAD4-matrix
intact models, within lineages containing both statuses?

This tests transportability of a reported SMAD4-loss/AURKA synthetic-lethal
mechanism. A damaging matrix value is not equivalent to biallelic loss,
functional SMAD4 loss, pathway activation, or pharmacologic AURKA inhibition.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `SMAD4 (4089)` matrix value `1` or `2`.
- Reference: `SMAD4 (4089)` matrix value `0`.
- Target header: `AURKA (6790)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No AURKA score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and `selection_seal.json`
before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based signed delta for SMAD4 damaging
versus matrix-intact models, then pool lineage numerators and denominators
within source. More negative means lower AURKA dependency score in the damaging
group.

The nominal gates are pooled delta <= -0.20, lineage-stratified permutation
p <= 0.05, bootstrap upper bound < 0, at least five negative lineages, and no
lineage delta > +0.20. The result is permanently `FEASIBILITY_ONLY`; planning
power is `0.6502` for Avana and `0.4713` for KY.

## Repeats and claim boundary

Use 100,000 null permutations, 10,000 bootstrap replicates, planning seeds
20263200/20263300, and inference seeds 20273200/20273300. No source pooling,
raw cross-source score comparison, functional SMAD4 claim, AURKA-drug claim,
spindle-checkpoint mechanism claim, pharmacologic claim, treatment claim,
clinical claim, or confirmatory claim is permitted.

## Source

Shi et al., *Oncogene* (2022): https://www.nature.com/articles/s41388-022-02293-y
