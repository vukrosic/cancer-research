# EXP-20260822-023 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `APC (324)` status to `TDO2 (6999)`
dependency. Selection is outcome-free: no TDO2 score row or endpoint value was
opened when the candidate census, design receipt, and preregistration were
written.

The primary study supports APC-deficient TDO2 synthetic essentiality in
genetic, organoid, and pharmacological models. It does not turn the mutation
matrix into functional APC loss and does not justify claims about WNT
causality, inhibitor response, or clinical benefit. Lineage, co-mutation,
protein state, and assay differences remain alternative explanations.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP023 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact TDO2 header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Execution receipt

The bound runner completed in approximately `18.031` seconds with the required
feasibility-only exit code `2`. Pre-endpoint boundary verification returned GO;
the exact `TDO2 (6999)` header was verified before endpoint values were parsed.
The terminal result is `FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`, with
`confirmatory_claim: false` and `overall_pass: false`.

Independent recomputation matched both source-specific deltas, pair counts,
permutation p-values, bootstrap intervals, and lineage deltas. Avana was weakly
negative and KY strongly positive, so the sources disagree in direction. The
full repository suite passed `121` tests. Preserve this discordant
feasibility-only outcome without post hoc rescue.
