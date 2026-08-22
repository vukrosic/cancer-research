# EXP-20260822-015 pre-execution methods audit

## Status

Independent review requested. The outcome-free census and planning power receipt
used only eligibility metadata and the damaging-status matrix. The ARID1B target
score column has not been parsed by the experiment implementation.

## Frozen safeguards

- The primary is a published ARID1A-status/ARID1B-dependency replication, not a
  novelty claim.
- Avana and KY are source-specific corroboration cohorts from one release; no
  biological independence or raw cross-source score comparison is claimed.
- The damaging matrix and eligible screen/model context are loaded and recorded
  before the ARID1B endpoint column is opened.
- Lineage-stratified damaging-status-versus-intact comparisons prevent pooled
  lineage composition from defining the primary result.
- Exact context counts, a pre-outcome 10,000-simulation design sensitivity, and
  a sealed endpoint-completeness gate are required before inference.
- The lower-tail permutation, ModelID bootstrap, six gates, feasibility label,
  and conservative claim boundary are frozen in the preregistration.

No ARID1B score, dependency contrast, p-value, interval, or result has been
computed before this protocol freeze.

## Critic round 1 — 2026-08-22

Independent Terra methods critic: `01a029b7-b3cd-78a2-8b70-9db3d608bae9`.

Initial verdict: **NO-GO until protocol amendments**. The critic confirmed the
biological identifiers, conservative literature framing, source-specific and
lineage-stratified design, endpoint completeness gate, estimator direction, and
claim boundary. Required amendments were:

- make the KY power of 0.5636 permanently feasibility-only in the title and
  final Boolean, rather than allowing observed gates to imply confirmation;
- specify the Normal shift, PCG64 seeds, empirical quantile and equality rule;
- freeze exact QC-to-screen-map-to-Model-to-matrix-to-endpoint join and
  missing-lineage behavior;
- bind the implementation commit/module digest before endpoint access; and
- hash the context ledger and design-sensitivity receipt before opening the
  endpoint.

The preregistration was amended with these requirements before execution.

## Critic round 2 — implementation audit

Independent Terra implementation critic: `01a029be-ea4b-7f51-a62a-b5963e1e1e5f`.

Initial verdict: **NO-GO** for three release blockers: the implementation was
not yet bound by commit/module digest, `inference.csv` still labeled nominal
source rows `primary_confirmatory=True`, and a T0 stop would delete the staged
context/design artifacts and in-memory pre-endpoint receipt. The critic also
requested deeper artifact-schema tests.

The runner was amended to bind final implementation commit
`2135a60d89d10e9147c149c838543ebe7493e392`
and module SHA-256 `99a77c47e53a0989c5b6928884839b64a4f9440dfb33513ff954bbaba90ff699`,
write `pre_endpoint_receipt.json` before endpoint loading, preserve staged
context/design files under `t0_provenance` on an endpoint T0 stop, force all
nominal CSV flags to `False`, and validate these invariants. The focused suite
now has 82 passing tests.
