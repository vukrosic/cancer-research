# EXP-20260822-025 result — CDKN2A proxy status to PELO dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `PELO (53918)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: CDKN2A matrix value `1` or `2`, labeled `damaging`;
- reference: CDKN2A matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and the 2025 Nature
report of PELO dependency in biallelic 9p21.3-deleted or MSI-H cancers:
[Chan et al., Nature](https://www.nature.com/articles/s41586-024-08509-3).
That study identifies FOCAD loss and the 9p21.3 copy-number context; a
CDKN2A damaging mutation is only a proxy and is not equivalent to that state.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.15800121383775034 | 4943 | 0.012569874301256988 | [-0.28100343920695936, -0.03014363746712523] | 10 | +0.5238095238095238 | FAIL |
| KY | -0.057692307692307696 | 832 | 0.3168068319316807 | [-0.25721153846153844, 0.13942307692307693] | 6 | +0.21428571428571427 | FAIL |

Avana was directionally negative, permutation-significant, and bootstrap
negative, but missed the frozen effect-size threshold (`delta <= -0.20`) and
failed lineage consistency. Positive lineage deltas included Breast
`+0.5238095238095238`, Bone `+0.42857142857142855`, Bowel
`+0.4090909090909091`, and Pancreas `+0.3037037037037037`.

KY was weakly negative but failed the effect-size, permutation, bootstrap, and
lineage-consistency gates. Its largest positive lineage delta was Ovary/
Fallopian Tube `+0.21428571428571427`.

Avana planning power was `0.8958`, but KY planning power was `0.5265`; the
paired experiment is permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, a
damaging-matrix CDKN2A proxy showed a heterogeneous negative association with
source-specific PELO knockout dependency in Avana and a weak, uncertain
negative association in KY; neither source passed the complete preregistered
gate contract.

This does not establish 9p21.3 deletion, FOCAD loss, MSI-H biology, a causal
CDKN2A–PELO interaction, PELO inhibitor sensitivity, treatment benefit, patient
selection, or clinical utility. It does not invalidate the Nature report,
which used copy-number, MSI, and functional perturbation evidence rather than
this CDKN2A mutation proxy. No source pooling, post hoc lineage exclusion,
threshold change, or endpoint-derived rescue was used.

## Artifact receipts

- `context_ledger.csv`: `1c6b1df176468f25de48585b97d456b7e83c3d2fa63352a31a527b4f3263e725`
- `design_sensitivity.csv`: `4d1a2acf900d7033702c5fcc3018c40d55c69accad71e546de4642e9926325bc`
- `endpoint_scores.csv`: `ae85894b710b0eea0f0d2a6bf3f9cd7ca00a2193071815895be76a89df538ff1`
- `inference.csv`: `2da3a19fcb761c63a321f0db3bc3c14822a3a09110512eecd3d922028891cac3`
- normalized `summary.json` digest: `8c25695dc89556510b20286b0082c94066f7b7eca552641a84c826ad1016fc73`
- pre-endpoint receipt: `d472cdb83390cdd4c35f8f4895360442c4f81901ce31e20ff5ad4845fa29b538`
