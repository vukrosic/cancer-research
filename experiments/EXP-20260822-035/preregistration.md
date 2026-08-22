# EXP035: TP53 damaging proxy to ENDOD1 dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not authorized until the selection commit is recorded in the implementation
boundary.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined TP53 damaging proxy
associated with more negative source-specific ENDOD1 dependency than TP53-matrix
intact models, within lineages containing both statuses?

This tests transportability of the TP53/ENDOD1 synthetic-lethal mechanism
reported by Tang et al. A damaging matrix value is not equivalent to a
biallelic loss, functional TP53 loss, TP53 hotspot mutation, or pharmacologic
ENDOD1 inhibition.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `TP53 (7157)` matrix value `1` or `2`.
- Reference: `TP53 (7157)` matrix value `0`.
- Target header: `ENDOD1 (23052)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No ENDOD1 score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and `selection_seal.json`
before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based signed delta for TP53 damaging
versus matrix-intact models, then pool lineage numerators and denominators
within source. More negative means lower ENDOD1 dependency score in the
damaging group.

The nominal gates are pooled delta <= -0.20, lineage-stratified permutation
p <= 0.05, bootstrap upper bound < 0, at least five negative lineages, and no
lineage delta > +0.20. The result is permanently `FEASIBILITY_ONLY`; planning
power is `0.9950` for Avana and `0.7417` for KY.

## Repeats and claim boundary

Use 100,000 null permutations, 10,000 bootstrap replicates, planning seeds
20263500/20263600, and inference seeds 20273500/20273600. No source pooling,
raw cross-source score comparison, functional TP53 claim, TP53-mutation claim,
ENDOD1-drug claim, DNA-repair mechanism claim, pharmacologic claim, treatment
claim, clinical claim, causal claim, or confirmatory claim is permitted.

## Source

Tang et al., *Nature Communications* (2022):
https://www.nature.com/articles/s41467-022-30311-w
