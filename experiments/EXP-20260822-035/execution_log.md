# EXP035 execution log

## Frozen boundary

- selection seal commit: `3cffc90`;
- implementation commit: `f9324f1`;
- manifest binding commit: `6a99e6d`;
- endpoint target column: `ENDOD1 (23052)`;
- status column: `TP53 (7157)`;
- runner: `.venv/bin/python -m candrel.tp53_endod1_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `23` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. The pre-endpoint
receipt was written before ENDOD1 scores were parsed. It reports `1,292`
eligible screens, `1,290` source/model values, and
`sealed_before_endpoint: true`.

This runner was executed exactly once. The initially created empty results
directory was removed before execution; no prior result files or endpoint
values existed.

## Result receipts

- context ledger: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`;
- design sensitivity: `bbb2bbd5e4078f49631838d266f286e78a6a5bc0b61371d661e15ed33d915f7d`;
- endpoint scores: `fc8c08f615ddc87f23ba0262e9637b6a45f399e3178f79162b7d69394b8daa88`;
- inference: `a048c0d2ec211f45520ae6656fadd24e0e719efa6f3ea879ca3046851daba4f6`;
- normalized `summary.json`: `cacbfb8e5df5032e7ab20aeb5e4310d66458ad20f7ce03da2da2acaa5f901c73`;
- pre-endpoint receipt: `f2d72b93b6cfce9fb9ddce14d22d570286070b33507c5840a4567dae6deeb16b`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the committed data and
frozen engine.
