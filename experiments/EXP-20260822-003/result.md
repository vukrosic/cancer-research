# EXP-20260822-003 result

## Status

**PASS WITH RECORDED PROTOCOL DEVIATION — source-separated MSI–WRN positive control
recovered in discovery and sequentially gated confirmation.**

This is recovery of a known cell-line association under a reliability protocol, not
a novel WRN–MSI biological discovery.

## Exact execution

The preregistration and manifest were committed and pushed as `5470d9a` before the
endpoint archive was downloaded.

Correctness gate:

```bash
uv run pytest
uv run candrel-msi-wrn-replication --smoke \
  --output experiments/EXP-20260822-003/results/smoke_summary.json \
  --model-output experiments/EXP-20260822-003/results/smoke_model_scores.csv
```

Frozen evaluation:

```bash
uv run candrel-msi-wrn-replication
```

Nineteen tests passed. The final full analysis used 100,000 within-tissue label
permutations and 10,000 stratified bootstrap resamples and completed in 7.59 seconds
on the project Mac.

## Integrity and adequacy

- `ScreenNaiveGeneScore.csv` matched official MD5
  `265f8372e9cd0fad56c1a6b66b8a783d`.
- All three metadata files matched their frozen SHA-256 hashes.
- Endpoint completeness was 100%: 69/69 eligible Avana models and 78/78 eligible
  KY models.
- Every tissue/source stratum retained at least two MSI and two MSS models.
- The remediated program parses and evaluates KY only after Avana passes all
  discovery gates; a regression test proves the confirmation loader is not called on
  discovery failure.

## Primary results

| Source/library | Models | Stratified delta | Bootstrap 95% CI | One-sided permutation p | Negative tissues | Result |
|---|---:|---:|---:|---:|---:|---|
| Broad / Avana | 69 | **-0.7432** | [-0.9377, -0.5019] | 1 / 100,001 | 4 / 4 | PASS |
| Sanger / KY | 78 | **-0.9307** | [-1.0000, -0.8133] | 1 / 100,001 | 4 / 4 | PASS |

Negative delta means a randomly formed within-tissue MSI–MSS pair tends to have a
more negative WRN score in the MSI model.

Tissue-specific deltas:

| Tissue | Avana | KY |
|---|---:|---:|
| Endometrium | -0.8000 | -0.8667 |
| Large Intestine | -0.9048 | -0.9300 |
| Ovary | -0.4824 | -0.9167 |
| Stomach | -0.7778 | -1.0000 |

Median within-tissue MSI-minus-MSS pair difference was -0.884 for Avana and -3.448
for KY. Those raw shifts are not compared across sources because the naïve score
scales differ by library; the primary estimand is rank based within source.

## Interpretation

The reliability pipeline recovered a strong, directionally consistent known
biomarker–dependency association from Broad Avana screens and then from Sanger KY
screens using source-separated, per-library naïve scores. The result survived tissue
control because only MSI–MSS pairs from the same tissue entered the primary effect.

## Protocol deviation and remediation

The first full implementation read the complete WRN column, constructed both Avana
and KY model-score objects, and checked adequacy for both sources before evaluating
the Avana discovery contrast. It did not estimate or emit the KY MSI–MSS effect until
Avana passed, and no threshold, cohort, or statistic changed. Nevertheless, this
violated the preregistration sentence that KY WRN values would remain unevaluated if
Avana failed.

The independent audit returned NO-GO for a strict unseen-held-out claim. Remediation:

- the deviation is preserved here rather than erased;
- all “unseen held-out values” language is withdrawn;
- the final code extracts only Avana screen values first and calls the KY loader only
  after discovery passes;
- `ScreenSequenceMap.csv` is now verified as a provenance input;
- tests cover both the full `run()` discovery-failure path and the lower-level
  confirmation-loader seal, plus all five frozen input hashes.

Because KY values were parsed in the initial implementation, this result is described
as a **sequentially gated confirmation contrast**, not a pristine unseen held-out
evaluation. The independently generated Sanger screen family remains experimentally
source-separated from Broad.

The smallest discovery effect was in ovarian models (delta -0.482), but it remained
in the expected direction and above the frozen practical threshold. No tissue in
either source showed a materially opposite effect.

The CRC-only experiment remains unavailable under its frozen minimum because Broad
has 7 MSI colorectal models rather than 8. The four-tissue result is a separate
population and does not alter that negative checkpoint.

## Claim boundary

Maximum supported claim: in this frozen public four-tissue cell-model cohort,
source-separated naïve CRISPR scores recovered the known association of MSI status
with stronger WRN knockout loss of fitness in Broad Avana discovery and a
sequentially gated Sanger KY confirmation contrast under the preregistered
tissue-stratified rule.

This does not establish a new synthetic lethality, mechanism, universal MSI effect,
drug efficacy, therapeutic window, patient response, or clinical actionability.

## Artifacts

- `results/summary.json`: SHA-256
  `d7b8cefb86bbe9c435bd4931f7d11d419f9639b5d642aaa774c1c831482d41e8`.
- `results/model_scores.csv`: all 147 retained source-model rows; SHA-256
  `072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654`.
- `results/smoke_summary.json`: SHA-256
  `0f54f65e5c003248d1a20d7448e05f29b7ea171afeba972160f1246844033634`.
- `results/full_timing.txt`: SHA-256
  `ffebc09d3167e22743411f361280170f2a1b17c819c347d758a1d9994298ea43`.

The initial independent audit numerically reproduced every result but blocked the
strict held-out claim. Re-audit verified the remediation and narrowed claim and
returned GO for commit/push.
