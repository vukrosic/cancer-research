# EXP035: TP53 damaging proxy to ENDOD1 dependency transport audit

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `ENDOD1 (23052)` / endonuclease domain containing 1 from the frozen
  DepMap 23Q4 naive CRISPR screen;
- exposure: TP53 damaging proxy when the matrix value is `1` or `2`;
- reference: TP53 matrix value `0`;
- canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from a primary study reporting an
ENDOD1/TP53 synthetic-lethal interaction
([Nature Communications study](https://www.nature.com/articles/s41467-022-30311-w)).
EXP035 tests only a TP53 damaging-matrix proxy against genetic ENDOD1 knockout
dependency; it is not a pharmacology experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `+0.0120830321` | 9683 | 0.6002039980 | `[-0.0814830115, +0.1066818135]` | 9 | `+1.0` | FAIL |
| KY | `+0.0376266281` | 1382 | 0.6679833202 | `[-0.1287988423, +0.2040520984]` | 7 | `+1.0` | FAIL |

Both sources were positive rather than negative in the preregistered direction,
missed the effect-size, permutation, bootstrap, and no-positive-lineage gates,
and showed substantial lineage heterogeneity. Avana had positive lineage
deltas in Ampulla of Vater `+0.5`, Eye `+0.5714285714`, Prostate `+0.6666666667`,
and Thyroid `+1.0`. KY had positive deltas in Breast `+0.8333333333`, Myeloid
`+1.0`, Prostate `+1.0`, and Uterus `+0.8333333333`.

The outcome-free planning powers were Avana `0.9950` and KY `0.7417`; the KY
power prevents any confirmatory two-source claim.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
TP53 damaging-matrix proxy did not show a robust source-consistent association
with genetic ENDOD1 dependency. This does not refute the reported TP53/ENDOD1
biology; the proxy, endpoint, cell-line composition, and genetic-versus-drug
mechanism are not equivalent.

This does not establish functional TP53 loss, TP53 hotspot mutation status,
ENDOD1-inhibitor efficacy, DNA-repair mechanism, causal synthetic lethality,
treatment benefit, patient selection, clinical utility, or a confirmatory claim.
No source pooling, post hoc lineage exclusion, threshold change, or proxy rescue
was used.

## Artifact receipts

- `context_ledger.csv`: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`
- `design_sensitivity.csv`: `bbb2bbd5e4078f49631838d266f286e78a6a5bc0b61371d661e15ed33d915f7d`
- `endpoint_scores.csv`: `fc8c08f615ddc87f23ba0262e9637b6a45f399e3178f79162b7d69394b8daa88`
- `inference.csv`: `a048c0d2ec211f45520ae6656fadd24e0e719efa6f3ea879ca3046851daba4f6`
- normalized `summary.json` digest: `cacbfb8e5df5032e7ab20aeb5e4310d66458ad20f7ce03da2da2acaa5f901c73`
- pre-endpoint receipt: `f2d72b93b6cfce9fb9ddce14d22d570286070b33507c5840a4567dae6deeb16b`
