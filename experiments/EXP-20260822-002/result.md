# EXP-20260822-002 result

## Status

**FAIL — preregistered processing-inflation hypothesis falsified on the frozen panel.**

The data-integrity gate passed for all eight genes, but neither practical-effect gate
passed.

## Exact execution

Correctness gate:

```bash
uv run pytest
uv run candrel-processing-sensitivity --repeats 50 \
  --output experiments/EXP-20260822-002/results/smoke_gate.json
```

Frozen evaluation:

```bash
uv run candrel-processing-sensitivity
```

The expected process exit code is 2 because the scientific hypothesis failed. Nine
tests passed before evaluation.

## Primary results

- All 8/8 genes had exactly 177 paired, QC-eligible Broad/Sanger models under both
  primary fields.
- Median gene-wise Spearman correlation:
  - `fc_clean_qn`: 0.4222399
  - `bf_scaled`: 0.4541519
- Median paired correlation difference
  `fc_clean_qn - bf_scaled`: **-0.0031226** (gate: at least +0.10).
- 4/8 genes had a positive difference (gate: at least 6/8).

| Gene | rho `fc_clean_qn` | rho `bf_scaled` | Difference | Bootstrap 95% interval |
| --- | ---: | ---: | ---: | ---: |
| WRN | 0.2076 | 0.2550 | -0.0474 | [-0.1016, 0.0021] |
| BRAF | 0.1475 | 0.1243 | 0.0232 | [-0.0302, 0.0754] |
| KRAS | 0.5526 | 0.5470 | 0.0055 | [-0.0272, 0.0371] |
| NRAS | 0.2476 | 0.2593 | -0.0118 | [-0.0676, 0.0436] |
| EGFR | 0.5799 | 0.5579 | 0.0220 | [-0.0394, 0.0781] |
| PIK3CA | 0.6345 | 0.6287 | 0.0058 | [-0.0388, 0.0506] |
| CTNNB1 | 0.4736 | 0.5063 | -0.0327 | [-0.0940, 0.0241] |
| MDM2 | 0.3708 | 0.4020 | -0.0312 | [-0.0813, 0.0205] |

The descriptive unscaled-`bf` median correlation was 0.4558558. No gene's bootstrap
interval excluded zero in favor of higher `fc_clean_qn` agreement.

## Interpretation

The broad claim that `fc_clean_qn` materially inflates cross-source rank agreement is
not supported in this fixed panel. Source-labelled scaled Bayesian factors produce
similar, and slightly higher median, Broad/Sanger concordance. This negative result is
useful: agreement in EXP-001 cannot be dismissed as a simple artifact of choosing
`fc_clean_qn`.

This does **not** prove `fc_clean_qn` is suitable for independent replication. The
official processing documentation still describes overlap-informed cross-source batch
correction for combined products, and the API field's exact lineage remains
insufficiently explicit. Similar correlations can coexist with leakage or altered
model-level values.

## Claim boundary

This is a T0/T1 processing-sensitivity result on eight preselected genes in a
historical API snapshot. It is not a genome-wide estimate, does not test MSI-selective
WRN dependency, and makes no mechanistic, druggability, treatment, patient-benefit, or
clinical claim. The MSI–WRN group contrast remains uncomputed.

## Artifacts

- `results/summary.json`, SHA-256
  `7f2349d77c86c74113c7738bd4e6a8cf83a0534247175143b4d116f29f65ab57`
- `results/smoke_gate.json`, SHA-256
  `e4950e7ccd212ac3aacaf6d4af28da17e0840fc2322ee1d4ab1b256dd2272bce3`

## Next decision

Send the code, receipt enforcement, cohort identity, numerical outputs, and claim
language to an independent adversarial audit. If approved, push the negative result.
Then preregister a current-release availability experiment without using the failed
historical cohort or relaxing its adequacy threshold.
