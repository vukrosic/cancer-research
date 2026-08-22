# EXP-20260822-016 pre-execution methods audit

## Status

Independent review requested. The candidate census used eligibility metadata,
the damaging-status matrix, literature, and endpoint header identity only. No
KEAP1 endpoint value has been parsed.

## Safeguards

- The selected direction is a recent primary CRISPR-reported ARID1A/KEAP1
  relationship, not a novelty, causality, druggability, or clinical claim.
- Avana and KY remain source-specific cohorts from one release; no biological
  independence or raw cross-source comparison is assumed.
- The context ledger and design receipt must be written and hashed before the
  KEAP1 endpoint is opened.
- KY's below-threshold design power permanently disables confirmation.
- All T0 stops preserve the exact boundary and never use subgroup or threshold
  rescue.

## Critic round 1 — 2026-08-22

Independent Terra methods/implementation critic:
`01a029d3-3513-79d0-8cdd-0347dc1ab854` and
`01a029da-25e6-79f3-ae2f-cdc1eb590ec8`.

Initial verdicts were **NO-GO** for an unbound implementation receipt, an
incorrect shared-function call contract, incomplete frozen-threshold checks,
and a positive test that could bind an unrelated module. The candidate census,
target identifiers, permanent feasibility label, and scientific claim boundary
were approved.

Amendments made before implementation binding:

- require the exact EXP016 module path and compare its SHA-256 both in the
  working tree and at the declared Git implementation commit;
- verify all frozen input hashes, status/eligibility/adequacy gates, primary
  pair and analysis type, design label/threshold/seeds, inference repeats,
  seeds, and thresholds;
- add the pre-endpoint endpoint-input hash stop and exact shared-call contract;
- add valid-boundary, threshold-drift, endpoint-hash, T0 classification, and
  source-specific-unit tests.

No KEAP1 endpoint value has been accessed.

The implementation is now bound to commit
`58bc6dea37dd06eaabcacb145ba2cadaf310789d` and module SHA-256
`c5c70e6149e4a5cfd7dc9e0b26a43fb6cc315e8251632fde27ccf631a3193d10` in the
manifest. The binding commit itself will be recorded before endpoint access.
