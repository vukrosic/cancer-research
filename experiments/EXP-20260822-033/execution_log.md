# EXP033 execution log

## Frozen boundary

- selection seal commit: `c274c91`;
- implementation commit: `693a71c`;
- manifest binding commit: `017b7a5`;
- endpoint target column: `ATR (545)`;
- status column: `ARID1A (8289)`;
- runner: `.venv/bin/python -m candrel.arid1a_atr_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `20` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. The pre-endpoint
receipt was written before ATR scores were parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

## Result receipts

- context ledger: `d808bd50211f644697a2606504e94e8a0cf588c212c8f4e651114821f36b2aad`;
- design sensitivity: `e3d31f068ddeecb4a6aafa182800c50b3ac938c9fddb157a7fb1263dcac3d271`;
- endpoint scores: `866ff59581feb9c8a8da54482a492c7647a54a65e449c4024b1999b993f28052`;
- inference: `dd10f50542d67f98f45d368d905b6ce2de195fbc0671c817aa29e417d9b52502`;
- normalized `summary.json`: `ce2347a2ce01e2135fc93c353d352353a71bbb07c889a9a39d0d9ea6d4ffb8f7`;
- pre-endpoint receipt: `3eb99863b1e5d07deef863b336758529bb0cf3e4c9c758373b705ee4284c3170`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the committed data and
frozen engine.
