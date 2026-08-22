# EXP029: composite BRCA1/2 proxy to POLQ dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are
not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a composite damaging proxy defined by
BRCA1 or BRCA2 matrix damage associated with more negative source-specific POLQ
dependency than models intact for both BRCA1 and BRCA2, within lineages that
contain both statuses?

This is a reliability and transportability audit. It tests a matrix-defined
proxy against genetic POLQ knockout dependency. The proxy is not equivalent to
biallelic deletion, homologous-recombination deficiency, a genomic scar,
functional BRCA status, or a clinical biomarker.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to
  `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `BRCA1 (672)` or `BRCA2 (675)` in
  `OmicsSomaticMutationsMatrixDamaging.csv` has value `1` or `2`.
- Reference: both BRCA1 and BRCA2 matrix values are `0`.
- Target header: `POLQ (10721)` in `ScreenNaiveGeneScore.csv`; POLQ is DNA
  polymerase theta.
- Endpoint scores will be median-collapsed across eligible screens for each
  `(source, ModelID)`.

No POLQ score value was opened during selection. Selection is sealed in
`candidate_census.json`, `design_census_receipt.json`, and
`selection_seal.json` before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based Vargha-Delaney-style signed delta
for composite damaging versus matrix-intact models, then pool lineage
numerators and denominators within source. More negative means lower POLQ
dependency scores in the composite damaging group.

The nominal gates are:

1. pooled delta <= -0.20;
2. lineage-stratified sign-permutation p <= 0.05;
3. percentile bootstrap 95% upper bound < 0;
4. at least five lineages with negative lineage delta;
5. no lineage delta > +0.20.

The result is permanently labeled `FEASIBILITY_ONLY`; Avana planning power is
`0.6464` and KY planning power is `0.4469`, both below the `0.80` confirmatory
threshold.

## Repeats and seeds

- Null permutations: 100,000.
- Bootstrap replicates: 10,000.
- Planning seeds: Avana `20262900`; KY `20263000`.
- Inference seeds: Avana `20272900`; KY `20273000`.
- Score distributions and ordering are frozen by the implementation manifest.

## Claim boundary

The strongest permitted conclusion is a source-specific association between the
composite damaging matrix proxy and POLQ dependency in frozen 23Q4 cell-line
screens. The analysis cannot claim biallelic BRCA1/2 loss, HRD, functional BRCA
status, a causal synthetic-lethal interaction, pharmacologic POLQ inhibition,
inhibitor response, treatment benefit, or clinical utility.

## Sources

- Haider et al., *Nature Genetics* (2025): https://www.nature.com/articles/s41588-025-02108-2
- Arnoldus et al., *Nature Genetics* (2025): https://www.nature.com/articles/s41588-025-02221-2
- FOCAD/HBS1L comparator: https://www.sciencedirect.com/science/article/pii/S0167488925001752
