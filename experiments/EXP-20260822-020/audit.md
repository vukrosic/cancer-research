# EXP-20260822-020 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The exact metadata audit
recomputed `1,292` eligible screens, Avana `975` and KY `315` source/model
units, status counts `610/365` and `233/82`, mixed-lineage counts `25/16`, the
canonical roster SHA-256, and design powers `0.9948` and `0.7564`. The endpoint
file hash and exact `WEE1 (7465)` header identity were verified before values
were parsed.

The independent biological review returned conditional GO and confirmed that
EXP020 is target-specific and distinct from EXP017, while warning that it is
not an independent validation of a general TP53-status claim. A second
read-only code reviewer timed out before returning; it was closed without
editing files or accessing endpoint values. The local boundary audit was the
decisive pre-endpoint implementation check.

## Post-execution checks

**GO.** The following checks passed:

- result directory contains exactly the five frozen result artifacts;
- context and endpoint ledgers each contain `1,290` rows;
- design and inference files each contain two source rows;
- all non-summary artifact SHA-256 values match `summary.json`;
- normalized summary digest matches the recorded digest;
- the pre-endpoint receipt recomputes from its three-field payload;
- an independent pairwise recomputation from `endpoint_scores.csv` exactly
  matches both source deltas, pair counts, and every contributing-lineage
  delta in `summary.json`;
- the runner's own `validate_staged` check passes;
- the terminal label remains `FEASIBILITY_ONLY`, with
  `confirmatory_claim: false` and `overall_pass: false`.

The first local audit script contained a checker-only mistake: it compared the
actual `summary.json` file hash to the normalized self-digest. This was
corrected without changing any research artifact; the corrected audit treats
the summary self-digest separately and passes.

## Protocol incidents

Attempt 001 stopped before endpoint access because an empty `results/`
directory had been created during repository preparation, and the runner's
existence guard correctly returned `ERROR_RESULTS_DIRECTORY_EXISTS`. The
  receipt is preserved in `attempt-001_error_receipt.json`. The empty directory
  was removed; no result data were deleted. Attempt 002 produced a complete
  provisional bundle, which was retained under an explicit pre-project-hash-fix
  name. Attempt 003 is the canonical release run under the final manifest.

## Claim decision

No upgrade, pooling, post hoc lineage exclusion, threshold change, or rescue is
permitted. EXP020 is released only as a T1 descriptive feasibility result.
