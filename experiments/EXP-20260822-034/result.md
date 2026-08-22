# EXP034 result — TP53 damaging proxy to TDG dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `TDG (6996)` / thymine DNA glycosylase from the frozen DepMap 23Q4
  naive CRISPR screen;
- exposure: TP53 damaging proxy when the matrix value is `1` or `2`;
- reference: TP53 matrix value `0`;
- canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from a recent study reporting TDG
synthetic lethality in p53-deficient cancers
([Nature Chemical Biology study](https://www.nature.com/articles/s41589-025-02100-1)).
EXP034 tests only a TP53 damaging-matrix proxy against genetic TDG knockout
dependency; it is not a pharmacology experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `-0.0953216978` | 9683 | 0.0236297637 | `[-0.1862026232, -0.0027832283]` | 16 | `+1.0` | FAIL |
| KY | `+0.1780028944` | 1382 | 0.9805501945 | `[0.0231548480, 0.3299927641]` | 5 | `+1.0` | FAIL |

Avana passed the direction, permutation, bootstrap, and minimum-negative-lineage
gates, but missed the effect-size gate and failed no-positive-lineage
consistency. Positive lineages included Ampulla of Vater `+1.0`, Cervix
`+0.9285714286`, and Thyroid `+1.0`.

KY was positive rather than negative and failed direction, effect, permutation,
bootstrap, and no-positive-lineage gates. Kidney and Prostate were both
`+1.0`; Bowel, Breast, Lung, and Peripheral Nervous System were also positive.

The outcome-free planning powers were Avana `0.9951` and KY `0.7617`; the KY
power prevents any confirmatory two-source claim.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
TP53 damaging-matrix proxy did not show a robust source-consistent association
with genetic TDG dependency. This does not refute p53-deficient-cancer/TDG
biology; the proxy, endpoint, cell-line composition, and genetic-versus-drug
mechanism are not equivalent.

This does not establish functional TP53 loss, TDG-inhibitor efficacy,
DNA-repair mechanism, causal synthetic lethality, treatment benefit, patient
selection, clinical utility, or a confirmatory claim. No source pooling,
post hoc lineage exclusion, threshold change, or proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`
- `design_sensitivity.csv`: `27bd90078c4818c9aa73fe7b9e8ac5a450eb68e47e771510a304e11684e397f9`
- `endpoint_scores.csv`: `edafcd0ca1e447ce853283bb6f3497b4dd961a421061cd3ceb9092f713806da1`
- `inference.csv`: `62e88924779766e3933400cd3a323e1c0797c3d184a2303efc6f0aee279e0dca`
- normalized `summary.json` digest: `69fdc4222e745c80245bc752b181259d731bf03669190201769d36677644d20c`
- pre-endpoint receipt: `d15ac4493f852ea5113acfad4970ace2f4111c37a52ba9e98ec98f354e0f6be7`
