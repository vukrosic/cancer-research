# EXP-20260822-011 independent audit

## Decision

**GO.** EXP-011 is reproducible within its declared post-failure scope, and the
bounded reconstruction claim may be preserved.

## Reproduced provenance and sequencing

- Preregistration, manifest, and methods audit were committed at `dd3e920`, before
  implementation commit `3f6c73f` and before candidate execution.
- All three frozen EXP-010 parent-artifact hashes match, and the parent experiment is
  unchanged from its preserved `e18f8b1` failure revision.
- Both large LFC files and every small input match the frozen hash receipts.
- All 55 cache-disabled tests pass.

## Reproduced candidate and gate

The code exposes exactly one candidate: sequence-level `PassesQC=True` plus
`ExcludeFromCRISPRCombined=False`, with retained count equal to
`nPassingSequences`. It then computes mean LFC by guide and median LFC across the
four Avana or five KY frozen WRN guides.

Exact three-field joins, canonical booleans, finite values, guide identities,
denominator counts, and the absolute `1e-8` / relative-zero tolerance are enforced.

Independent ledger checks found:

- 103 unique frozen identities;
- the expected source and tissue counts;
- retained counts equal to passing counts for every screen;
- 103/103 passing comparisons;
- maximum absolute discrepancy `5.551115123125783e-17`;
- all three parent mismatch identities resolved; and
- zero new mismatches.

## Scope and non-computation

No executable gap, rank, percentile, guide-omission, or robustness path exists. The
only references to those analyses are explicit non-computation receipts and test
assertions. No fallback candidate exists.

The sole candidate was motivated by the observed EXP-010 failure. Therefore this is
a bounded pipeline-semantics audit, not independent confirmation, a biological
result, or a repair of EXP-010.

## Maximum approved claim

**This passing-sequence rule reconstructs WRN scores in the frozen 103-screen
subset.**
