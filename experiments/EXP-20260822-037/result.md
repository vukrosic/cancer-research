# EXP-20260822-037 result — CDKN2A proxy status to MAT2A dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate screen families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `MAT2A (4144)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: CDKN2A damaging proxy when the matrix value is `1` or `2`;
- reference: CDKN2A matrix value `0`;
- status counts: Avana `110/865`, KY `37/278` damaging/matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The outcome-free planning powers were Avana `0.8906` and KY `0.5361`; the
paired-source contract therefore permanently limits this experiment to
`FEASIBILITY_ONLY`.

The biological motivation is the reported MAT2A vulnerability in homozygous
MTAP-deleted cancers and the use of CDKN2A deletion as an imperfect clinical
surrogate for MTAP loss ([primary phase I report](https://www.nature.com/articles/s41467-024-55316-5)). This experiment uses only a damaging CDKN2A mutation matrix proxy, which is not equivalent to CDKN2A deletion, MTAP deletion, or drug response.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `+0.1094477038` | 4943 | `0.9423905761` | `[-0.0196338256, +0.2336637669]` | 8 | `+1.0000` | FAIL |
| KY | `-0.2139423077` | 832 | `0.0351396486` | `[-0.4158653846, -0.0120192308]` | 8 | `+0.8333` | FAIL |

Avana is positive in the preregistered dependency direction and fails the
effect, permutation, bootstrap, and no-positive-lineage gates. KY passes the
direction, effect, permutation, and bootstrap gates, but fails the
no-positive-lineage gate; its positive Bone lineage is `+0.8333`. No source
pooling, post hoc lineage exclusion, threshold change, or proxy rescue was
used.

## Interpretation boundary

The strongest allowed statement is: in these frozen DepMap 23Q4 cohorts, the
CDKN2A damaging-matrix proxy did not show a robust source-consistent
association with MAT2A genetic dependency. The KY result is directionally
interesting but heterogeneous and is not a robust transport replication.

This does not refute MAT2A/MTAP biology. The mutation proxy, CDKN2A deletion,
MTAP deletion, cell-line composition, genetic MAT2A knockout, and MAT2A drug
inhibition are not equivalent. The result does not establish mechanism,
pharmacologic response, treatment benefit, patient selection, clinical
utility, or a confirmatory claim.

## Artifact receipts

- `context_ledger.csv`: `1c6b1df176468f25de48585b97d456b7e83c3d2fa63352a31a527b4f3263e725`
- `design_sensitivity.csv`: `d79398107dea3d888ca9c10be3855eef242cb16aa88d9ed477398fdf59730260`
- `endpoint_scores.csv`: `41ed3ccd4d7679247fc9bdfac663e34f524412c73bd078d947a6fbe6ce2ae5d6`
- `inference.csv`: `3fc988c9ce1d20c008a5866853536f5fd788b10ff52303a30e7a5fc27a0b49ad`
- normalized `summary.json` digest: `99f3330dc3f17949aaf8ed5c691206d01c61f639edb5cf243922ef45a6d6562c`
- `pre_endpoint_receipt.json`: `6a977c2df3823d22b92fa4f0027f15dd00f22850fade46a3f6b75ea22e22105e`
