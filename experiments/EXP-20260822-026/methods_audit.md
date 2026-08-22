# EXP-20260822-026 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `PTEN (5728)` status to `PAPSS1
(9061)` dependency. Selection is outcome-free: no PAPSS1 score row or endpoint
value was opened when the candidate census, design receipt, and
preregistration were written.

The primary Nature Cancer study supports PAPSS1/PAPSS2 collateral lethality in
patient-translational models and describes collateral PAPSS2 loss near PTEN,
while reporting that the interaction is not detectable in ordinary DepMap cell
lines. PTEN mutation is only a proxy in this experiment and is not equivalent
to PTEN deletion or PAPSS2 co-deletion. No claim about patient translation,
mechanistic causality, drug response, treatment benefit, or clinical utility is
permitted.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP026 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact PAPSS1 header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.
