# EXP-20260822-009 independent audit

## Decision

**GO.** The implementation and preserved negative result faithfully follow the
preregistration pushed at commit `8fa611e`. No post-preregistration method drift or
required statistical remediation was found.

## Independent checks

- Reproduced all four SHA-256 input receipts.
- Verified 103 exact unique ScreenIDs and frozen source-by-tissue denominators:
  Avana/KY 25/30 Large Intestine and 22/26 Ovary.
- Verified all count values are finite nonnegative integers and the paired cohort is
  exactly 17 models per tissue.
- Located exactly three differing records, all included greater than passing:
  `ACH-000663` Avana, `ACH-000680` Avana, and `ACH-000719` KY.
- Reproduced full-denominator average-tied percentiles. Primary and sensitivity
  exposures had six levels/largest tie seven in Large Intestine and five/seven in
  Ovary.
- Confirmed the execution path completes every exposure adequacy gate before hashing
  or opening the outcome file.
- Confirmed tied frozen ranks, tissue-preserving permutation, plus-one positive-tail
  p-values, and paired bootstraps without reranking or degenerate redraw.

## Reproduced estimates

Primary `nIncludedSequences` exposure:

- theta = 0.0667134;
- Large Intestine rho = -0.3679361;
- Ovary rho = 0.5013629;
- 35,416 of 100,000 permutation estimates at least observed, giving
  `(1 + 35,416) / 100,001 = 0.3541665`;
- bootstrap 95% CI [-0.2376696, 0.3390970].

Sensitivity `nPassingSequences` exposure:

- theta = 0.0710329;
- p = 0.3464965;
- bootstrap 95% CI [-0.2322252, 0.3448028].

All four primary gates fail. Sensitivity is correctly labeled non-independent and
non-rescuing.

## Software and artifacts

- 46 tests pass.
- CLI help exits 0; a hash-integrity failure exits 1; scientific failure exits 2.
- Smoke and full model tables are byte-identical with SHA-256
  `4e15632f37adf77e185465b484fdf52a0967ac59d63c736a8b79850c592491c3`.
- Result language is negative, noncausal, cohort-limited, and nonclinical.

The audited EXP-009 result is approved for commit and push.
