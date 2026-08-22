# EXP-20260822-022 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `EP300 (2033)` status to `CREBBP
(1387)` dependency. Selection is outcome-free: no CREBBP score row or endpoint
value was opened when the candidate census, design receipt, and
preregistration were written.

The biological source supports a CRISPR-observed EP300/CREBBP paralog
interaction. It does not turn the mutation matrix into functional EP300 loss
and does not justify claims about paralog causality, inhibitor response, or
clinical benefit. Lineage, co-mutation, protein state, and assay differences
remain alternative explanations.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP022 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact CREBBP header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Execution receipt

The bound runner completed in approximately `21.006` seconds with the required
feasibility-only exit code `2`. Pre-endpoint boundary verification returned GO;
the exact `CREBBP (1387)` header was verified before endpoint values were
parsed. The terminal result is `FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`, with
`confirmatory_claim: false` and `overall_pass: false`.

Independent recomputation matched both source-specific deltas, pair counts,
permutation p-values, bootstrap intervals, and lineage deltas. Both sources
failed the no-positive-lineage gate. The full repository suite passed `116`
tests. Preserve this heterogeneous feasibility-only outcome without post hoc
rescue.
