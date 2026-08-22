# EXP034: TP53 damaging proxy to TDG dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined TP53 damaging proxy
associated with more negative source-specific TDG dependency than TP53-matrix
intact models, within lineages containing both statuses?

This tests transportability of a recent p53-deficient-cancer/TDG synthetic-lethal
mechanism. A damaging matrix value is not equivalent to biallelic loss,
functional TP53 loss, p53 pathway state, or pharmacologic TDG inhibition.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `TP53 (7157)` matrix value `1` or `2`.
- Reference: `TP53 (7157)` matrix value `0`.
- Target header: `TDG (6996)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No TDG score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and `selection_seal.json`
before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based signed delta for TP53 damaging
versus matrix-intact models, then pool lineage numerators and denominators
within source. More negative means lower TDG dependency score in the damaging
group.

The nominal gates are pooled delta <= -0.20, lineage-stratified permutation
p <= 0.05, bootstrap upper bound < 0, at least five negative lineages, and no
lineage delta > +0.20. The result is permanently `FEASIBILITY_ONLY`; planning
power is `0.9951` for Avana and `0.7617` for KY.

## Repeats and claim boundary

Use 100,000 null permutations, 10,000 bootstrap replicates, planning seeds
20263400/20263500, and inference seeds 20273400/20273500. No source pooling,
raw cross-source score comparison, functional TP53 claim, TDG-drug claim,
DNA-repair mechanism claim, pharmacologic claim, treatment claim, clinical
claim, or confirmatory claim is permitted.

## Source

Zhou et al., *Nature Chemical Biology* (2026):
https://www.nature.com/articles/s41589-025-02100-1
