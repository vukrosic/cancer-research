# EXP-20260822-028: TP53-proxy to TIPARP dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined damaging TP53 status associated with more negative source-specific TIPARP (PARP7) knockout dependency than matrix-intact TP53 models, within lineages that contain both statuses?

This is a reliability and transportability audit. The primary SCHEMATIC study reports a multilineage PARP7 interaction network that includes TP53 and related genome-integrity factors, while its strongest drug-biomarker validation focused on KDM5C/KDM6A alterations. This experiment tests a narrower TP53 matrix proxy and does not recreate the paper's combinatorial CRISPR interaction score.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `TP53 (7157)` in `OmicsSomaticMutationsMatrixDamaging.csv` is damaging when the frozen matrix value is 1 or 2.
- Reference: the same matrix value is 0.
- Target header: `TIPARP (25976)` in `ScreenNaiveGeneScore.csv`; TIPARP is PARP7.
- Endpoint scores will be median-collapsed across eligible screens for each `(source, ModelID)`.

No TIPARP score value was opened during selection. Selection was sealed in
`candidate_census.json`, `design_census_receipt.json`, and
`selection_seal.json` before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based Vargha-Delaney-style signed delta for damaging versus matrix-intact models, then pool lineage numerators and denominators within source. More negative means lower TIPARP dependency scores in the damaging group.

The nominal gates are:

1. pooled delta <= -0.20;
2. two-sided sign-permutation p <= 0.05 under lineage-stratified relabeling;
3. percentile bootstrap 95% upper bound < 0;
4. at least five lineages with negative lineage delta;
5. no lineage delta > +0.20.

The result is permanently labeled `FEASIBILITY_ONLY`; no confirmatory claim is enabled because KY planning power is below 0.80.

## Repeats and seeds

- Null permutations: 100,000.
- Bootstrap replicates: 10,000.
- Planning seeds: Avana 20262800; KY 20262900.
- Inference seeds: Avana 20272800; KY 20272900.
- Score distributions and ordering are frozen by the implementation manifest.

## Claim boundary

The strongest permitted conclusion is a source-specific association between the frozen matrix proxy and TIPARP dependency in frozen 23Q4 cell-line screens. The analysis cannot claim functional TP53 loss, the SCHEMATIC combinatorial interaction, pharmacologic PARP7 inhibition, inhibitor response, treatment benefit, or clinical utility.

## Sources

- Fong et al., *Nature Genetics* (2025): https://www.nature.com/articles/s41588-024-01971-9
- Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC12266356/
- Related 3D-model KRAS/SCD candidate excluded for exposure constancy: https://doi.org/10.1038/s41586-026-10843-7
