# Outcome-blind methods audit — EXP-20260822-006

## Initial verdict

**NO-GO as initially phrased; repaired before outcome association.**

The critic required proof that screen-level QC was not pseudoreplicated across models,
that the metrics did not directly contain WRN, that the composite was not presented
as validated, that “association” replaced causal “explanation,” and that rank,
permutation, bootstrap, and point-versus-CI gates were explicit.

## Provenance/availability remediation

- 103/103 full-denominator model-source records map to 103 unique ScreenIDs.
- The 34 paired models map to 68 unique source screens.
- All five metrics are complete in every denominator.
- NNMD, ROCAUC, essential median, and nonessential median are unique for every model
  in every source×tissue stratum; FPR has 14–24 unique values in the full strata and
  ties are handled by average midranks.
- Official control-list hashes match the release; WRN is absent from both lists.

## Final verdict

**GO to preregister with the exact frozen details in `preregistration.md`.**

The critic did not inspect or compute any WRN-gap/QC association and did not edit
files.

