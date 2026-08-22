# Independent audit — EXP-20260822-007

## Verdict

**GO. EXP-007 correctly stops at T0.**

The auditor made no file edits and independently verified:

- official DepMap Public 23Q4 Figshare v2 file IDs, sizes, and MD5 receipts;
- all local MD5 and SHA-256 receipts;
- exact `(model_id, tissue)` identity between the two-column outcome-free cohort and
  the frozen EXP-005 population: 17 Large Intestine and 17 Ovary models;
- that no WRN-gap field is present in the actual execution input;
- exact guide filters: `WRN (7486)`, `UsedByChronos=True`, one alignment, and blank
  drop reason, yielding four Avana and five KY guides;
- one mutation row per selected guide, complete binary values, and zero mutations for
  every selected guide across all 34 cohort models;
- constant-zero source-asymmetry exposure in both tissues; and
- no implemented or executed correlation, permutation, bootstrap, or outcome
  association.

Thirty-five tests passed. The narrow wording correctly excludes only variation in
the specific annotated guide-location mutation exposure, not all guide-related
mechanisms.
