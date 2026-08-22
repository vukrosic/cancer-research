# EXP-20260822-006 result

## Status

**FAIL — the frozen five-metric QC-rank-asymmetry composite was not positively
associated with source-specific WRN rank discordance.**

Evidence label: preregistered derived observational analysis after EXP-005 endpoint
unsealing. This is not blinded confirmation and the result is not a causal test.

## Exact execution

The preregistration and outcome-blind methods audit were committed and pushed as
`4c167d1` before any WRN-gap/QC association was computed.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-wrn-qc-asymmetry --smoke \
  --output experiments/EXP-20260822-006/results/smoke_summary.json \
  --model-output experiments/EXP-20260822-006/results/smoke_model_qc_asymmetry.csv
uv run candrel-wrn-qc-asymmetry \
  --output experiments/EXP-20260822-006/results/summary.json \
  --model-output experiments/EXP-20260822-006/results/model_qc_asymmetry.csv
```

Thirty-one tests passed at initial execution. After independent audit, an exact
upstream-score/QC ScreenID drift guard and its regression test were added; the final
suite has 32 passing tests. The change did not alter any analysis value. CSV line
endings were subsequently normalized from CRLF to LF for clean Git diffs; this
changed only the model-table byte hashes. The expected scientific-failure exit code
was 2 for both the smoke and full runs. The full run used 100,000 tissue-preserving
permutations and 10,000 within-tissue paired bootstraps.

## Integrity and adequacy

- All five input SHA-256 receipts matched the frozen manifest.
- The full QC denominators contained 103 model-source records and 103 unique
  ScreenIDs: Avana 25 / KY 30 Large Intestine and Avana 22 / KY 26 Ovary.
- The association population was exactly the 34 EXP-005 paired ModelIDs, 17 per
  tissue.
- All five QC metrics and the primary composite were finite and nonconstant.
- WRN was absent from the hash-verified 1,247-gene common-essential and 781-gene
  nonessential control lists used by the screen QC metrics.
- Source-specific QC percentiles used the full source-by-tissue denominators; only
  the 34 paired models entered the association.

## Primary result

| Estimand | Result | Frozen gate | Pass? |
|---|---:|---:|:---:|
| Equal-tissue mean Spearman `theta` | **-0.0662** | >= 0.40 | No |
| One-sided tissue-preserving permutation p | **0.6452** | <= 0.05 | No |
| Fixed-rank paired-bootstrap 95% CI | **[-0.3922, 0.2780]** | lower > 0.10 | No |
| Lowest tissue rho | **-0.2549** | >= -0.20 | No |

All four frozen outcome gates failed. The two tissue estimates pointed in different
directions:

| Tissue | Paired models | Spearman rho |
|---|---:|---:|
| Large Intestine | 17 | **-0.2549** |
| Ovary | 17 | **0.1225** |

The smoke run already showed a near-zero aggregate, but the frozen full run was
completed because smoke was a correctness and adequacy gate rather than an outcome
selection rule.

## Descriptive secondary results

No individual metric was inferentially tested. Their preregistered descriptive
equal-tissue mean correlations with the absolute WRN percentile gap were:

| QC-rank asymmetry | Equal-tissue mean rho |
|---|---:|
| Essential-depletion median | 0.1360 |
| FPR | 0.1250 |
| NNMD | -0.0858 |
| ROCAUC | -0.0895 |
| Nonessential-depletion median | -0.1348 |

The 10 EXP-005 gap-flagged models had median composite QC asymmetry 0.2576, versus
0.2289 among the 24 unflagged models. This small descriptive difference cannot
rescue the failed primary rank-based analysis.

## Interpretation

This experiment falsifies the specific proposed explanation that a simple
equal-weight composite of source-specific screen-QC rank differences tracks the
observed WRN ranking gaps in these 34 models. The data are compatible with no useful
positive association, and the tissue directions are heterogeneous.

The failure does not show that technical factors are irrelevant. Screen-level
control separation and depletion are broad assay-quality summaries; guide-level
WRN design, assay timing, cell-line state, source-specific biology, or measurement
noise could still matter. Those are new hypotheses requiring separately frozen
tests, not post hoc rescues of EXP-006.

## Claim boundary

Maximum supported claim: in the frozen Large Intestine and Ovary overlap set, the
preregistered five-metric source-QC-rank-asymmetry composite did not positively
track source-specific WRN dependency-rank gaps.

This null/negative observational result does not establish absence of all technical
confounding, a biological mechanism, a treatment target, patient benefit, or
clinical relevance.

## Artifacts

- `results/summary.json`: SHA-256
  `19d66441da20ef940284423911ea5e17ab45d2a1e34cfc63d5058d26544dcc45`.
- `results/model_qc_asymmetry.csv`: SHA-256
  `6326b383e4e9b40b218339663d59214e8ac5fcc954c8fd95668b627c2d1c3824`.
- `results/smoke_summary.json`: SHA-256
  `170684a4ed4d4aab9e9cd44fc695c770ca009404a65fccfad0f05e5aa1c75311`.
- Smoke and full model tables are byte-identical because smoke changes inference
  repeats only.

Independent audit reproduced all inputs, screen identities, QC transforms,
percentiles, composites, model rows, point estimates, inference logic, failed gates,
and claim boundaries. It returned GO. A non-blocking ScreenID drift guard was added;
targeted re-audit verified the guard, 32 tests, and unchanged scientific values, and
returned GO for commit and push. The later line-ending-only normalization is recorded
above and was separately checked before commit.
