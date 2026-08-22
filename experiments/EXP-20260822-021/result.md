# EXP-20260822-021 result — NF1 damaging status to PTPN11 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `PTPN11 (5781)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: NF1 matrix value `1` or `2`, labeled `damaging`;
- reference: NF1 matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `8c3229c5925e533688a9efb8979700d1f2d379a760d0672544a61073a8bfc375`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.24936294139060794 | 2747 | 0.0033399666003339967 | [-0.3797051328722242, -0.11321441572624681] | 6 | +1.0 | FAIL |
| KY | +0.046153846153846156 | 520 | 0.6307336926630733 | [-0.16153846153846155, 0.26153846153846155] | 3 | +1.0 | FAIL |

Avana passed the directional effect, permutation, and bootstrap gates, but it
failed the no-positive-lineage gate: Bladder/Urinary Tract was `+1.0` and
Esophagus/Stomach was `+0.5256410256410257`. The aggregate signal is therefore
not lineage-consistent under the frozen contract.

KY failed the directional, effect-size, permutation, bootstrap, negative-
lineage-count, and no-positive-lineage gates. It is not a replication of the
Avana direction.

## Interpretation boundary

The result does not establish that NF1-mutant, NF1-null, or functionally
deficient cancers depend on PTPN11. The damaging matrix is a proxy and does
not establish allele state, functional loss, protein state, RAS-pathway
activity, or causal mechanism. The result also does not establish SHP2/PTPN11
inhibitor sensitivity, a therapeutic window, treatment benefit, patient
selection, or clinical utility.

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix NF1 proxy had discordant source-specific,
lineage-stratified associations with PTPN11 knockout dependency and failed the
complete preregistered gate contract in both source families.

## Artifact receipts

- `context_ledger.csv`: `5523b2105d6313d82aa15db66f5ed784b0356bb67f8b3d64beb175614a2ae5f5`
- `design_sensitivity.csv`: `194e137c72c2b8190c37e552dcc05f5b190d1bac78e47d7b74ff518878ba1759`
- `endpoint_scores.csv`: `991c062f799e4c37d37dd4d9557583ff95dfafdae2965173605279fce1012c93`
- `inference.csv`: `eb19e60df392dcbff37992a176014a9f50a61649c35e06694c87f22ace26c408`
- normalized `summary.json` digest: `b71b85bff9fec326e005f0f0885a0c648a780bce0f4a6e0409bd48df6c290f96`
- pre-endpoint receipt: `7e15546d92bf6e20f52890e1c393053220a0a91821b8469cbef11687234bdaac`
