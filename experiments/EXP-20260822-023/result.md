# EXP-20260822-023 result — APC damaging status to TDO2 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `TDO2 (6999)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: APC matrix value `1` or `2`, labeled `damaging`;
- reference: APC matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `64d3f95cf8bac59c1b7293b464c8cbe9133441a94c9e44897529540c9c58fb8d`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and a primary study
supporting APC-deficient TDO2 synthetic essentiality:
[PMC9262860](https://pmc.ncbi.nlm.nih.gov/articles/PMC9262860/). That study
does not convert the damaging matrix into functional APC loss.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.12317880794701987 | 1510 | 0.15482845171548285 | [-0.28480132450331125, 0.033112582781456956] | 6 | +0.34615384615384615 | FAIL |
| KY | +0.49216300940438873 | 319 | 0.996510034899651 | [0.2476489028213166, 0.7053291536050157] | 2 | +0.8333333333333334 | FAIL |

Avana was directionally negative but failed the effect-size, permutation,
bootstrap, and no-positive-lineage gates. Its strongest positive lineage was
Head and Neck `+0.34615384615384615`; Skin was `+0.34328358208955223`.

KY was positive rather than negative and failed every substantive gate except
the minimum negative-lineage count. Positive lineage deltas included Lung
`+0.8333333333333334`, Esophagus/Stomach `+0.7837837837837838`, and Bowel
`+0.3888888888888889`.

The two source families therefore disagree in direction. Both source planning
powers were below `0.80` before endpoint access (Avana `0.5184`, KY `0.2861`),
so the experiment is permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix APC proxy did not reproduce a source-consistent association
with TDO2 knockout dependency; Avana was weakly negative and KY was strongly
positive under the preregistered lineage-stratified analysis.

This does not refute the published APC/TDO2 findings in their own models, and
it does not establish functional APC loss, WNT causality, TDO2 inhibitor
sensitivity, treatment benefit, patient selection, or clinical utility. No
source pooling, post hoc lineage exclusion, threshold change, or endpoint-
derived rescue was used.

## Artifact receipts

- `context_ledger.csv`: `9123ac9b0ec93d7c772cd37a2e3e7ab83666ffdbaed9fc4edfb5abe95dc36e18`
- `design_sensitivity.csv`: `be87ae6b7e265948d789a0fdf02950ff6d9ea21a342f742f9579f975c3314ced`
- `endpoint_scores.csv`: `05104dfe6becd13c908524748dac7061958fb87096cc35050caf09a653785425`
- `inference.csv`: `61d29592337f2a9f1d01c5fe4e3101f688428d6470f2e6ceab42e5c339c326aa`
- normalized `summary.json` digest: `4ee2d29210ab51c4223ff81e57c0390d8b70dbf37f78c2960af139331f78e027`
- pre-endpoint receipt: `3d97124d177407b9940a0833ca14aa560790057de2ac9e2eb6a527f56caa21c2`
