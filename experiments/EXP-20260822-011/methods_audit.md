# EXP-20260822-011 pre-execution methods audit

## Decision

**GO after amendments.** The independent critic accepted a separate, narrow
pipeline-semantics child while emphasizing that the sole candidate was motivated by
EXP-010's observed failure and is not outcome-independent confirmation.

## Amendments frozen

- EXP-010 parent revision and three parent artifacts are hash-bound and immutable.
- Exact join key is `(ScreenID, ModelID, Library/source)` for sequence and QC rows.
- Blank, duplicate, contradictory, or noncanonical boolean values are rejected.
- Sole candidate retains sequence-level `PassesQC=True` and
  `ExcludeFromCRISPRCombined=False`, with count equal to `nPassingSequences`.
- Screen-level QC `PassesQC` is not an additional filter.
- All prior guide, LFC, identity, finite-value, formula, and `1e-8` zero-rtol guards
  remain.
- The execution path cannot load the EXP-005 gap file or perform ranking, omission,
  or robustness analysis.
- A complete 103-row ledger and aggregate resolved/persistent/new mismatch comparison
  are mandatory.
- No second candidate or fallback is allowed.

No passing-sequence reconstruction score was computed during this review.
