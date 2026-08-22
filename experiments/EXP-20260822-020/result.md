# EXP-20260822-020 result — TP53 damaging status to WEE1 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families; no pooled
estimate is reported.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `WEE1 (7465)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: TP53 matrix value `1` or `2`, labeled `damaging`;
- reference: TP53 matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.03852111948776206 | 9683 | 0.21191788082119178 | [-0.12796653929567284, 0.05381080243726111] | 14 | +0.5 | FAIL |
| KY | -0.3096960926193922 | 1382 | 0.0001799982000179998 | [-0.470369030390738, -0.14616497829232997] | 12 | +1.0 | FAIL |

Avana passed only the directional delta and negative-lineage-count gates. It
failed the `-0.20` effect gate, permutation gate, bootstrap upper-bound gate,
and no-positive-lineage gate. Its aggregate association is near zero and its
lineage effects are heterogeneous.

KY passed the directional effect, permutation, and bootstrap gates and had a
negative aggregate delta, but failed the no-positive-lineage gate because
Peripheral Nervous System was `+0.43333333333333335` and Prostate was `+1.0`.
KY therefore also fails the frozen all-gates contract. These lineages are
preserved; they are not excluded or rescued.

## Interpretation boundary

The result does not establish that TP53-mutant, TP53-null, or functionally
deficient cancers depend on WEE1. The damaging matrix is a proxy and does not
establish allele state, functional loss, protein state, KRAS co-mutation,
replication stress, or causal mechanism. The result also does not establish
WEE1 inhibitor sensitivity, a therapeutic window, treatment benefit, patient
selection, or clinical utility.

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix TP53 proxy had source-specific, lineage-stratified associations
with WEE1 knockout dependency that were discordant in aggregate and failed the
complete preregistered gate contract in both source families.

## Artifact receipts

- `context_ledger.csv`: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`
- `design_sensitivity.csv`: `8bb85d0f76c925f7357c0fce4039647fba070b14a94d6b92d7fdc3961da007c3`
- `endpoint_scores.csv`: `a4accd2588cc40b0f5a0b4c9b657953de7fbe91c1dc751f4a10b0884e018c6a7`
- `inference.csv`: `84cee4bd3b30cc01811b47ac4a8271c1c7eddd8d4862769630b4d56f7e5fc2b8`
- normalized `summary.json` digest: `f4dd574713f3ae0b450896b53e71c3b144cc36151bf37be3ce69bd3253f93572`
- pre-endpoint receipt: `4cd616be9dc7742f020598e5e9b4cfdbf2ab3e24fa5538ade88cbd07e08be656`
