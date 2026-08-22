# EXP-20260822-012 independent audit

## Decision

**GO.** The generated EXP012 result is internally consistent with the committed
implementation and its preregistration. Preserve the primary failure and its narrow
claim.

## Reproduced provenance and gates

- EXP012 preregistration is frozen at `cc0329c`; implementation is frozen at
  `8098f4e`.
- All small-input hashes, both large-LFC MD5/SHA-256 receipts, all EXP011 parent
  artifact hashes, all five EXP012 CSV hashes, and the normalized EXP012 summary
  self-digest match.
- Baseline reconstruction is 103/103 with maximum discrepancy
  `5.551115123125783e-17`.
- EXP-011's 103-row reconstruction ledger matches with zero maximum score drift.
- EXP-005's 34 scores, percentiles, gaps, and locked ten flags reproduce within the
  frozen tolerance; maximum percentile and gap drift are zero.

## Reproduced robustness outputs

- Exactly four Avana and five KY global omissions ran.
- Full ledger: 1,030 rows; paired gap ledger: 340 rows; robustness table: 34 rows;
  guide means: 103 rows; configuration table: 10 rows.
- Every unaffected source's score and percentile is invariant across all global
  omissions.
- Five of ten locked flagged models are fully robust; six are robust to all Avana
  omissions and six to all KY omissions. The primary `>=8/10` gate therefore fails.
- Equal-tissue theta is `0.5790913398452961` at baseline and `[0.45316986228026923,
  0.6356495181766879]` across omissions.
- There are 26 unflagged-to-flagged transitions across 216 possible events and 10
  unique transition models.

The read-only audit did not overwrite the published result directory; the runner's
stale-directory refusal is functioning as designed.

## Non-computation and claim boundary

No p-value, confidence interval, multiplicity correction, guide ranking, subgroup
rescue, causal guide-quality analysis, or multi-guide perturbation was computed.
The result supports only the narrow same-assay passing-sequence robustness claim in
the EXP012 result card. EXP-010 remains unchanged and failed at its own T0 gate.
