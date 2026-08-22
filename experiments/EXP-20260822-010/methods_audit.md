# EXP-20260822-010 pre-perturbation methods audit

## Decision

**GO after amendments.** The independent critic judged the direct WRN guide-level
robustness audit valuable and nonredundant, but returned an initial NO-GO because the
reconstruction joins, no-drift gate, perturbation unit, reporting configurations,
and parity limitation needed exact definitions.

## Amendments frozen before any omission result

- Guide means use only exact frozen-screen, source-matched, nonexcluded sequence
  columns with complete finite LFCs.
- All 103 reconstructed baseline scores must match official naïve WRN scores within
  absolute tolerance `1e-8` and zero relative tolerance before any omission.
- Each denominator model-source record must retain its one exact frozen ScreenID.
- Omissions are global and library-specific: four Avana-only plus five KY-only
  configurations, never screen-specific or simultaneous two-library omissions.
- Every configuration retains all 103 identities and at least three/four Avana/KY
  guides.
- Percentiles are recomputed only in the frozen full source-by-tissue denominators
  with average midranks and the exact `>=0.25` flag threshold.
- Full robustness means 9/9 omissions; primary pass requires at least 8/10 locked
  baseline-flagged models fully robust.
- Baseline-plus-nine gap summaries, source-specific robustness, theta range, and
  unflagged transitions are descriptive and cannot rescue a primary failure.
- No p-values or intervals treat the dependent perturbations as independent tests.
- The four-to-three versus five-to-four median parity difference is explicit and
  forbids source-comparative guide-influence or causal language.

No leave-one-guide-out score, percentile, gap, transition, or robustness result was
computed during this review.
