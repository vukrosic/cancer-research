# EXP038 execution log

## Frozen boundary

- selection checkpoint: `472eb28`;
- implementation commit: `e7cef51`;
- manifest binding commit: `102b0d2`;
- endpoint target column: `ICMT (23463)`;
- status column: `PTEN (5728)`;
- runner: `env PYTHONPATH=src .venv/bin/python -m candrel.pten_icmt_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `20.26` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before ICMT scores were parsed. It reports
`1,292` eligible screens, `1,290` source/model values, and
`sealed_before_endpoint: true`.

This runner was executed exactly once. The results directory did not exist
before execution; no prior result files or endpoint values were present.

## Result receipts

- context ledger: `48bf8b95574dc6b79acdb31acbb08cbc9166ffd4c04de600142df9c03baaa11b`;
- design sensitivity: `5a97a287c00c662c5a4297154d0d66640fbcbc19a6cb42b1659e9d31178dba1e`;
- endpoint scores: `a6f3cc20f9608296b18d6fd8e244f3615e94bdc9e1f61640639c5d2e32f4bd6f`;
- inference: `5d94acd69c367ab5ab6dda90439670fa85a5dc86c236a6c2e69baa72fbd31365`;
- normalized `summary.json`: `758cbd2c271d1f5e63efe3ec4b138866350ca36c48bf7c972421a1333180ef42`;
- pre-endpoint receipt: `9193e3e0fddd2409455bcc6ffcb7881e5ecd1a0a8a6b64f9ef1a22473e7f90d2`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the result ledgers and
frozen engine. The heartbeat remains deleted by user request.
