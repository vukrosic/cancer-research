# EXP-20260822-027: ARID1A-proxy to EZH2 dependency transport audit

Status: outcome-free selection sealed; implementation and endpoint execution are not yet authorized by this receipt alone.

## Question

In the frozen DepMap 23Q4 cohort, is a matrix-defined damaging ARID1A status associated with more negative source-specific EZH2 knockout dependency than matrix-intact ARID1A models, within lineages that contain both statuses?

This is a reliability and transportability audit. The literature direction is an ARID1A-mutant/EZH2-inhibition interaction in ovarian cancer models, not proof that the frozen DepMap proxy or CRISPR endpoint represents the same biological state.

## Frozen data and exposure

- Sources: Avana and KY only.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact `ScreenID` to `ModelID` join, and nonblank `OncotreeLineage`.
- Exposure: `ARID1A (8289)` in `OmicsSomaticMutationsMatrixDamaging.csv` is damaging when the frozen matrix value is 1 or 2.
- Reference: the same matrix value is 0.
- Target header: `EZH2 (2146)` in `ScreenNaiveGeneScore.csv`.
- Endpoint scores will be median-collapsed across eligible screens for each `(source, ModelID)`.

No EZH2 score value was opened during selection. Selection was sealed in `candidate_census.json`, `design_census_receipt.json`, and `selection_seal.json` before implementation.

## Primary estimand and gates

Within each lineage, compute the rank-based Vargha-Delaney-style signed delta for damaging versus matrix-intact models, then pool lineage numerators and denominators within source. More negative means lower EZH2 dependency scores in the damaging group.

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
- Planning seeds: Avana 20262700; KY 20262800.
- Inference seeds: Avana 20272700; KY 20272800.
- Score distributions and ordering are frozen by the implementation manifest.

## Claim boundary

The strongest permitted conclusion is a source-specific association between the frozen matrix proxy and EZH2 dependency in frozen 23Q4 cell-line screens. The analysis cannot claim functional ARID1A loss, ovarian-specific biology, pharmacologic EZH2 inhibition, causal synthetic lethality, inhibitor response, treatment benefit, or clinical utility.

## Sources

- Bitler et al., *Nature Medicine* (2015): https://www.nature.com/articles/nm.3799
- Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC4352133/
