# EXP-20260822-007 result

## Status

**FAIL T0 — source-specific WRN guide-site mutation exposure is constant zero in
the frozen 34-model cohort. No association analysis was computed.**

Evidence label: outcome-blind data-availability and exposure-adequacy audit. This is
not an inferential experiment and was not repository-preregistered before exposure
inspection.

## Exact execution

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-wrn-guide-mutation-adequacy
```

Thirty-five tests passed. The command returned expected adequacy-failure exit code 2.
It read only the dedicated hash-frozen `cohort.csv` containing ModelID and tissue;
the WRN percentile-gap values from EXP-005 were neither an input nor parsed.

## Provenance and identity

- All four official Figshare MD5 receipts and all five local SHA-256 receipts matched.
- The guide maps contained four eligible Avana and five eligible KY guides for
  `WRN (7486)`: all were used by Chronos, uniquely aligned, and had no drop reason.
- Both mutation matrices contained 1,750 model columns and all 34 frozen cohort
  ModelIDs.
- Every selected guide had exactly one mutation-matrix row and every cohort value was
  binary and complete.

The initial large downloads stalled after partial transfer; they were preserved and
completed with HTTP range resumption. Final official MD5 matches prove the resumed
files are complete and byte-correct.

## Adequacy result

| Tissue | Models | Any Avana WRN-guide mutation | Any KY WRN-guide mutation | Unique asymmetry values | Nonconstant? |
|---|---:|---:|---:|---:|:---:|
| Large Intestine | 17 | 0 | 0 | 1 | No |
| Ovary | 17 | 0 | 0 | 1 | No |

All 34 models have zero mutations at all four Avana and all five KY WRN guide
locations. Therefore each source-specific burden and every absolute source
difference equal zero.

The matrices are not globally empty at these guide rows: among all 1,750 matrix
models, two Avana WRN guide rows and two KY WRN guide rows each contain one annotated
mutation. The constant-zero cohort result is therefore a cohort fact, not a parser
that silently converted every value to zero.

## Stop decision

The prospective adequacy rule required a nonconstant guide-mutation-asymmetry
exposure in each tissue. Both tissues failed. Per protocol, no Spearman correlation,
permutation, bootstrap, outcome threshold, or alternative mutation aggregation was
computed. The cohort was not broadened and the exposure was not redefined.

## Interpretation and claim boundary

The official 23Q4 matrices provide no support for mutations directly overlapping
the selected WRN guide locations as an explanation for source-specific WRN ranking
gaps among these 34 models. This specific candidate cannot be statistically tested
because it has no exposure variation.

This does not establish that guide design is irrelevant. The binary matrices do not
test guide efficacy, exon/domain placement, mismatch position effects outside the
annotated interval, structural variation, uncalled variants, assay duration,
cell-line state, or library-specific processing. Those remain distinct hypotheses.

## Artifacts

- `results/summary.json`: SHA-256
  `fd6951175e935f4a03e70c07e79453ef485fad33956e640eed9a867464677cf8`.
- `results/model_exposure.csv`: SHA-256
  `a963cce774ad5308655a6e38faaf9769f77fc15f98df22a06eba854a2782eb1d`.

Independent audit verified official Figshare metadata and hashes, exact cohort
identity, guide selection, matrix coverage, binary values, constant-zero exposures,
35 tests, and the absence of any WRN-gap or association computation. It returned GO
for commit and push.
