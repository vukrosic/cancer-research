# Independent audit — EXP-20260822-003

## Initial verdict

**NO-GO for the strict unseen-held-out claim; numerical result verified.**

The auditor independently reconstructed all 147 model-score rows from the frozen raw
inputs with zero discrepancy and recomputed:

- Avana: delta -0.7431906615, 95% CI [-0.9377431907, -0.5019455253],
  permutation p 1/100,001;
- KY: delta -0.9306666667, 95% CI [-1.0000000000, -0.8133333333],
  permutation p 1/100,001.

All tissue deltas, cohort counts, completeness values, hashes, statistical tails,
and six gates matched. Sixteen tests passed at the initial audit point.

The blocker was implementation/protocol alignment: the first implementation parsed
KY WRN values and created KY model-score objects before the Avana effect gate, even
though it delayed the KY contrast calculation. It also did not operationally verify
the manifest-listed sequence-map receipt.

## Remediation

- Recorded the protocol deviation in `result.md`.
- Withdrew claims that KY endpoint values were unseen.
- Refactored extraction so only Avana screen values are parsed before discovery.
- Added a sequential evaluation function whose confirmation loader is never called
  on discovery failure.
- Added SHA-256 verification for `ScreenSequenceMap.csv`.
- Added tests for discovery-failure sealing and complete input-hash coverage.
- Final suite: 19 tests, including a full `run()` discovery-failure test.

## Re-audit

**GO — remediation is technically and scientifically sufficient for commit/push.**

The same independent auditor verified that:

- result, README, and audit language preserve the deviation and do not call KY
  values unseen;
- direct discovery-failure execution performs one Avana extraction, no KY
  extraction, and returns `confirmation = null`;
- all five frozen input hashes are enforced and match;
- independent recomputation of Avana and KY aggregate and tissue effects remains
  exact;
- the final repository suite passes 19 tests.

No scientific or publication blocker remains under the narrowed claim.
