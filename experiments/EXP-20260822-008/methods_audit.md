# Outcome-blind methods audit — EXP-20260822-008

## Verdict

**GO to preregister with the exact constraints in `preregistration.md`.**

The independent critic did not inspect EXP-005 WRN-gap values, EXP-006 outcomes, or
any control-exposure/WRN-gap association.

## Required design constraints

The critic required:

- source×tissue ranks rather than raw Avana/KY score comparison;
- full 25/30/22/26 denominators before paired-model restriction;
- separate common-essential primary and nonessential corroborative panels;
- complete 103-screen gene eligibility and fixed 80% panel-retention gates;
- one median model-level exposure per panel, with genes explicitly not treated as
  independent observations;
- at least 10 distinct exposure values within each tissue;
- equal-tissue Spearman means, tissue-preserving permutation, and fixed-rank paired
  bootstrap without reranking duplicates;
- an interpretation hierarchy in which nonessential results cannot rescue the
  primary panel; and
- observational, non-causal, non-clinical claims only.

All constraints are incorporated verbatim in the frozen protocol.
