# EXP-20260822-014 result

## Decision

**FEASIBILITY_ONLY; no confirmatory replication claim.** The frozen primary
STAG2-status → STAG1-dependency analysis shows a strong negative direction in
both source-specific cohorts, but the pre-outcome design-sensitivity receipt is
below the required 80% power in both sources. Independently, Avana fails the
frozen lineage-consistency gate. The result is therefore not a successful
two-source replication.

This is a replication audit of a known paralog interaction, not a novel cancer
discovery or treatment result.

## Execution and context

The final run used `uv run candrel-paralog-replication` at code commit
`849d4567f1ca85e70a959739cb98a797941d7b91`, after the preregistration and
methods GO at commit `3d088442fe86d14c8258f54e58a01a81a995f940`.

The context gate passed before endpoint access:

- 1,292 eligible screens collapsed to 1,290 source-model units;
- Avana: 975 source-model units; KY: 315;
- 1,098 unique ModelIDs across both source cohorts;
- STAG2 matrix-defined damaging status: 31 Avana and 9 KY models;
- PDS5B matrix-defined damaging status: 23 Avana and 12 KY models;
- target endpoint completeness: 2,580/2,580 source-model-pair values;
- source-specific scores were never compared in raw units.

The exposure is matrix-defined damaging mutation status (`damaging matrix value
>=1`), not a claim of functional or biallelic loss. Avana and KY are
source-specific corroboration cohorts from the same public release, not
independent biological cohorts.

## Pre-outcome design sensitivity

The frozen sensitivity model used 10,000 alternative simulations at an expected
direction statistic of `delta=-0.20`, with a 100,000-permutation null critical
distribution and the exact observed lineage group sizes.

| Pair | Source | Simulated power | Confirmatory threshold |
|---|---|---:|---:|
| STAG2 → STAG1 | Avana | 0.5070 | ≥ 0.80 |
| STAG2 → STAG1 | KY | 0.2406 | ≥ 0.80 |

Both primary sources were therefore labeled underpowered before target-score
access. This label cannot be rescued by the observed effect.

## Primary STAG2 → STAG1 result

| Source | Delta | One-sided p | Bootstrap 95% interval | Frozen gate status |
|---|---:|---:|---:|---|
| Avana | -0.470899 | 0.0000800 | [-0.615112, -0.305556] | Fail: Liver lineage delta +0.913043 > +0.20 |
| KY | -0.641256 | 0.0013500 | [-0.766816, -0.479821] | Passes all six nominal gates |

Avana’s overall direction, effect threshold, permutation p-value, bootstrap
interval, and negative-lineage-count gates pass. Its lineage-consistency gate
fails because the Liver lineage-specific delta is `+0.913043`. KY has six
contributing lineages and passes all six nominal gates.

Because the design-sensitivity requirement fails for both sources and Avana
fails a primary gate, `overall_pass` is false and no confirmatory STAG2 claim is
made.

## Secondary PDS5B → PDS5A result

The secondary pair was descriptive only and could not rescue the primary.
Avana’s nominal gates pass with delta `-0.600000`, p `0.0000100`, and bootstrap
interval `[-0.737349, -0.445783]`. KY fails its nominal permutation and
lineage-consistency gates with delta `-0.203252`, p `0.161538`, and bootstrap
interval `[-0.398374, -0.008130]`; its CNS/Brain lineage delta is `+1.0`.
No multiplicity-adjusted or confirmatory secondary claim is made.

## Claim boundary

The frozen data provide feasibility/robustness evidence that the direction of the
known STAG2-status/STAG1-dependency relationship appears strongly negative in
these source-specific score summaries, while its confirmatory status is not
established under the preregistered power and lineage gates.

This does not establish novelty, causal tumor biology, functional or biallelic
loss, a druggable STAG1 inhibitor, therapeutic selectivity, patient benefit, or
clinical utility. It does not validate the secondary PDS5B/PDS5A pair as a
replicated interaction.

## Input and artifact receipts

| Receipt | SHA-256 |
|---|---|
| `ScreenNaiveGeneScore.csv` | `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721` |
| `AchillesScreenQCReport.csv` | `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407` |
| `CRISPRScreenMap.csv` | `1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad` |
| `Model.csv` | `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341` |
| damaging mutation matrix | `aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3` |

| Tracked artifact | SHA-256 |
|---|---|
| `context_ledger.csv` | `d2a55264d567515a822e4f918cdb0f5b47ab9bf6b675d37ac2c30bb24279cfdb` |
| `design_sensitivity.csv` | `9ec28f32fa795b77349a64449adab02985800e1503932ecf09c618369ed3d144` |
| `endpoint_scores.csv` | `7ee86b031ff3d915214321f2bd3430b9b546c794cdab7226ba770fb8f32c2ec9` |
| `inference.csv` | `7d46a5e37f5e8fd85ef14ac21a71f42bf6e244c96ce7dc56267331315ec39dc1` |
| `summary.json` raw file | `c9e05a708d1d527d4b8b5064fbc9505e5889010113c0b0c0949eca51eda52445` |
| `summary.json` normalized self-digest | `e6916bdef82ee01fea3df34e5d5f80357b48aac09ca43fbdfc9e59e98a6c9125` |

The machine-readable receipt is [`summary.json`](results/summary.json); its
normalized self-digest is intentionally distinct from the literal file hash.
The full protocol is [`preregistration.md`](preregistration.md), and the
independent review is [`audit.md`](audit.md).
