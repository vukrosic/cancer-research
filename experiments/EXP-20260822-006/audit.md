# Independent audit — EXP-20260822-006

## Initial result audit

**GO.** The independent auditor made no file edits and found no validity blocker.

The auditor independently verified:

- all five frozen input SHA-256 receipts;
- all source×tissue denominators, 103/103 unique ScreenIDs, and exact agreement
  between the QC screens and screens underlying the frozen EXP-003 scores;
- all five quality transforms, average-midrank percentiles, FPR ties, equal-weight
  composite values, and all 34 exported model rows;
- Large Intestine rho -0.25490, Ovary rho 0.12255, and equal-tissue theta -0.06618;
- within-tissue frozen-rank permutation and paired fixed-rank bootstrap logic;
- correct failure of all four gates; and
- the observational, post-unsealing evidence label and non-causal claim boundary.

A separately seeded/ordered Monte Carlo stream produced a nearby p-value of about
0.650 rather than 0.645. This is expected Monte Carlo variation and is immaterial to
the frozen 0.05 gate.

## Non-blocking hardening and re-audit

The auditor recommended enforcing, in code, the already-verified identity between
each selected QC ScreenID and the `screen_ids` value in the hash-frozen EXP-003
model-score table. The implementation now freezes those upstream identities,
rejects any mismatch before percentile construction, and includes a regression test.

**Re-audit verdict: GO for commit and push.** The auditor verified that the guard is
wired into the real execution path, all 32 tests pass, and every scientific value is
unchanged. A subsequent packaging-only normalization changed generated model-table
line endings from CRLF to LF; the JSON artifacts and all model-table values remained
unchanged, while the final CSV hash was updated in `result.md`.
