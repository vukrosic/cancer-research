# EXP-20260822-014 independent audit

## Final decision

**GO to preserve as FEASIBILITY_ONLY and non-confirmatory.** The independent
audit reproduced the final artifacts byte-for-byte and found no computational or
claim-boundary defect. It explicitly does not approve a two-source confirmatory
replication claim.

## Review history

### Methods review

The first design review returned NO-GO because KY had only nine matrix-defined
damaging STAG2 models and the original wording overstated confirmatory power.
The preregistration was amended before endpoint access to add exact context
rosters, a 10,000-simulation/100,000-null design-sensitivity label, a sealed
endpoint-completeness gate, precise percentile bootstrap behavior,
matrix-defined status language, same-release source corroboration wording, and
primary-only confirmatory status. The final methods review returned GO.

### Code review

The first implementation audit returned NO-GO because expected context and
endpoint-completeness stops were emitted as generic integrity errors. Commit
`0507f5b` added explicit `T0_CONTEXT_ADEQUACY` and
`T0_ENDPOINT_COMPLETENESS` receipts with an `endpoint_opened` boundary; 77 tests
passed and the final code audit returned GO.

The first live attempt then stopped before endpoint access with a generic input
receipt because the loader required a nonblank lineage on every Model.csv row.
`ACH-003132` was an ineligible non-cancerous model with blank lineage, not a
duplicate. Commit `849d456` narrowed the requirement to eligible models only;
the eligible lineage join remains strict.

### Final result audit

The final independent rerun verified:

- 1,292 eligible screens and 1,290 source-model units;
- exact Avana/KY counts 975/315 and frozen damaging-status counts;
- 2,580/2,580 finite source-model-pair endpoint values;
- primary design sensitivity 0.5070 Avana and 0.2406 KY, correctly forcing
  `FEASIBILITY_ONLY`;
- STAG2 → STAG1 Avana delta `-0.470899`, p `0.0000800`, CI
  `[-0.615112,-0.305556]`, failing only the Liver lineage-consistency gate;
- STAG2 → STAG1 KY delta `-0.641256`, p `0.0013500`, CI
  `[-0.766816,-0.479821]`, passing nominal gates;
- descriptive-only secondary behavior and no secondary rescue;
- all input hashes and four CSV artifact hashes.

The result directory, result card, and this audit remain to be committed as one
tracked release. The normalized summary self-digest is intentional and is
documented separately from the raw `summary.json` SHA-256.

## Claim boundary

The audit approves only preservation of the source-specific feasibility result.
It does not approve a confirmed genetic interaction, biological independence,
causal mechanism, drug target, patient benefit, or clinical interpretation.
