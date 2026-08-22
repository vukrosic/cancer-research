# EXP030 pre-endpoint selection correction

The first single execution stopped at `T0_CONTEXT_ADEQUACY` before endpoint
access. It detected that the planning receipt had reused EXP029's simulated
power values (`0.6464` for Avana and `0.4469` for KY) while EXP030 had already
sealed new planning seeds (`20263000` and `20263100`). The endpoint header was
verified during selection, but no CIP2A score value was opened; the original
`error_receipt.json` records `endpoint_opened: false`.

The outcome-free planning simulation was recomputed with the sealed EXP030
seeds. The corrected values are `0.6686` for Avana and `0.4355` for KY. The
critical deltas and all cohort counts are unchanged. Both powers remain below
the frozen `0.80` confirmatory threshold, so the experiment remains permanently
`FEASIBILITY_ONLY`.

This correction changes only pre-endpoint planning metadata and its dependent
hash receipts. It does not inspect, select on, or modify any CIP2A endpoint
score. The initial T0 error receipt is preserved as an audit trail.
