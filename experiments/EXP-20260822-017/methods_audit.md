# EXP-20260822-017 methods audit

## Independent pre-implementation review target

The frozen direction is matrix-intact `TP53 (7157)` status to `MDM2 (4193)`
dependency. The selection is outcome-free: no MDM2 score row or endpoint value
was opened when the candidate census and preregistration were written.

The candidate is important because a primary CRISPR study identified and
validated MDM2 dependency in TP53-wild-type Ewing sarcoma models. The present
experiment asks whether a deliberately weaker, matrix-defined proxy reproduces
as a source-specific association across Avana and KY. It is a reliability audit,
not a new treatment or novelty claim.

## Required audit checks

- Verify exact hashes and headers for the four metadata inputs and endpoint file.
- Verify exact ScreenID-to-ModelID identity, eligible source/model counts, and
  nonblank lineages before endpoint access.
- Verify TP53 domain `{0,1,2}`, exact exposed/reference counts, and mixed-lineage
  adequacy against the frozen manifest.
- Verify the sealed candidate census and deterministic planning powers before
  endpoint access.
- Verify the implementation boundary includes the EXP017 wrapper and every
  imported local analysis module that affects inference, plus `uv.lock`.
- Verify the endpoint hash immediately before parsing and enforce exact MDM2
  header identity and complete source/model coverage.
- Recompute delta, permutation p-values, bootstrap intervals, lineage gates,
  artifact hashes, and the normalized summary digest independently.
- Require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false` regardless of nominal
  gate outcomes.

## Review status

This document is a pre-implementation audit checklist. It must be amended only
with implementation-boundary and execution receipts after the runner is bound;
the frozen question, candidate census, thresholds, and claim boundary must not be
rewritten after endpoint access.
