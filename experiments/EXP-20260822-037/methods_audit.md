# EXP-20260822-037 methods audit

## Pre-implementation review

The frozen direction is damaging-matrix `CDKN2A (1029)` status to `MAT2A
(4144)` dependency. Selection is outcome-free: the MAT2A endpoint header was
checked, but no MAT2A score row or endpoint value was opened when the census,
design receipt, and preregistration were written.

The primary clinical source supports MAT2A inhibition in the context of
homozygous MTAP deletion and documents that CDKN2A deletion is an imperfect
surrogate for MTAP loss. The present matrix exposure is a damaging-mutation
proxy and therefore cannot support an MTAP-deletion, CDKN2A-deletion,
mechanistic, drug-response, treatment, or clinical claim.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP037 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact MAT2A header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage
  gates, artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Frozen decision

`GO_TO_IMPLEMENTATION_AND_SINGLE_EXECUTION`.

The KY planning power is below the confirmatory threshold, so the experiment
cannot be upgraded after seeing endpoint values. The result, whether null,
positive, discordant, or a T0 stop, must be preserved as a feasibility-only
record.
