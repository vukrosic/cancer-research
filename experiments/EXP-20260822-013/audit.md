# EXP-20260822-013 independent audit

## Final decision

**GO after paired-unit and release-tracking remediation.** The corrected
experiment is reproducible and the negative primary result is preserved. The
audit did not find a numerical, sequencing, or claim-boundary defect in the
final run.

## Review history

### Pre-execution implementation audit

The first independent code audit returned NO-GO because the frozen parameter
files are source-specific for 35 unpaired denominator records. Requiring both
source columns for all 103 records would have stopped before the parameter
ledger and outcome access. The exact coverage was measured: 103 finite
own-source values and both source values for all 34 paired models. The protocol
amendment was committed publicly at `07976d9`, and the runner was changed to
ignore expected opposite-source blanks for unpaired records.

### First execution audit

The first result audit reproduced all numerical outputs but found that the
outcome-blind adequacy receipt counted each paired model twice, once per source.
The implementation therefore reported 34 observations per tissue instead of
the required 17. This did not change the association result, but it made the
gate receipt non-equivalent to the preregistration. The unit fix was committed
at `51a2874`; the old output was moved to
`/tmp/cancer-research-exp013-pre-fix-results` and is not used as evidence.

### Corrected execution audit

The corrected run was independently checked for:

- 103 unique source-specific parameter-ledger records;
- 34 paired ModelIDs, exactly 17 in each tissue;
- 17 distinct efficacy and growth exposures per tissue, largest tie 1;
- all four frozen input SHA-256 values;
- byte-identical CSV outputs across independent temporary reruns;
- 100,000 permutations, 10,000 bootstraps, seed `20260830`;
- efficacy-only p-value, interval, and primary gates;
- growth theta/correlations with no growth p-value or confidence interval;
- the exact failed-gate interpretation and narrow noncausal claim boundary.

The corrected numerical receipt is:

- efficacy theta `0.2071078431`;
- one-sided permutation p `0.1220187798` with 12,201 extreme permutations;
- bootstrap 95% interval `[-0.1697118656, 0.5334215543]`;
- tissue rho `-0.0637254902` (Large Intestine) and `0.4779411765`
  (Ovary);
- growth descriptive theta `0.1139705882`.

The first corrected artifact review temporarily returned NO-GO only because the
result directory and result card were untracked and `audit.md` did not yet
exist. Release commit `da41e14` adds those exact artifacts. `git ls-files` now
shows every EXP013 result and documentation file, and the tracked files reproduce
the hashes in `result.md` and `summary.json`. This resolves the provenance issue.

## Audit claim boundary

The audit approves only the computational statement that the preregistered
positive efficacy-association gates failed in this frozen two-tissue,
same-assay, already-unsealed endpoint analysis. It does not approve a causal,
mechanistic, therapeutic, patient, or clinical interpretation.
