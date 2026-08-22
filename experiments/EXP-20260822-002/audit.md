# Independent audit — EXP-20260822-002

## Verdict

**GO — commit and push the negative result.**

The independent auditor inspected the preregistration, manifest, receipt enforcement,
implementation, tests, smoke and full outputs, result card, provenance audit, state,
and git diff. It independently recomputed all eight gene-level correlations and the
aggregate from the hash-locked inputs.

Verified evidence:

- median `rho(fc_clean_qn) - rho(bf_scaled)` = -0.0031225654;
- 4/8 genes had a positive difference;
- all eight genes had 177 identical paired models;
- 9/9 tests passed;
- the full command exits 2 as documented because the scientific gate failed;
- parent receipt, smoke output, and full output hashes match the result card;
- no post-hoc threshold change or cohort mismatch was found.

The auditor found no repository artifact indicating an MSI-conditioned WRN
calculation. EXP-002 code does not load MSI labels, so the MSI–WRN contrast remains
sealed in the recorded evidence.

## Claim review

Approved only in this form: within the fixed historical eight-gene panel,
`fc_clean_qn` did not show materially higher Broad/Sanger rank agreement than
source-labelled `bf_scaled`. The result does not prove source independence and does
not support a biological or clinical conclusion.

## Non-blocking recommendations

- Add an explicit CLI test for scientific `FAIL` mapping to exit code 2.
- Add a deterministic-bootstrap fixture regression test.
- Give future experiments an experiment-local receipt even when inputs are inherited.

These are recorded for the next implementation cycle and do not block this result.
