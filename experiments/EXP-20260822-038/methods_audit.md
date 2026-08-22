# EXP-20260822-038 methods audit

## Pre-implementation review

The frozen direction is damaging-matrix `PTEN (5728)` status to `ICMT
(23463)` dependency. Selection is outcome-free: the ICMT endpoint header was
checked, but no ICMT score row or endpoint value was opened when the census,
design receipt, and preregistration were written.

The primary source reports a PTEN-mutant/ICMT synthetic-essential relationship
in triple-negative breast cancer. The present experiment uses a damaging
mutation matrix proxy across all eligible lineages and a genetic knockout
endpoint, so it cannot claim PTEN protein loss, triple-negative specificity,
pharmacologic ICMT inhibition, or clinical response.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP038 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact ICMT header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage
  gates, artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Frozen decision

`GO_TO_IMPLEMENTATION_AND_SINGLE_EXECUTION`.

KY planning power is below the confirmatory threshold, so the experiment
cannot be upgraded after endpoint values are seen. The result, whether null,
positive, discordant, or a T0 stop, must be preserved as a feasibility-only
record.
