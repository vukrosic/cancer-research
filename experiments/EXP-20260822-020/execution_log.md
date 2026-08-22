# EXP-20260822-020 execution log

## Frozen boundary

- selection seal commit: `0e195ed66248082180d4e2791b8dbea506dfb110`;
- protocol commit: `cc8a055434b54f31d5125ec27412ab1867751536`;
- final implementation commit: `af37220f5000bfb71d60a39232185511275ae02d`;
- final manifest commit: `08ba3c1debdf9f933ba532dafe9b4569d7d7ec21`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `WEE1 (7465)`;
- runner: `.venv/bin/python -m candrel.tp53_wee1_replication`.

## Attempt 001

The runner returned `1` with `ERROR_RESULTS_DIRECTORY_EXISTS` because the
empty result directory had been created before invocation. No endpoint values
were parsed and no results were written. The typed preservation record is
`attempt-001_error_receipt.json`.

## Attempt 002 — provisional pre-project-hash-fix run

The runner completed in approximately `22.877` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. Its complete
bundle is preserved under `results_attempt-002_pre_project_hash_fix/`, but it
is not the release bundle because the project-file hash boundary was corrected
after this run.

## Attempt 003 — canonical release run

After restoring the historical `pyproject.toml` hash and rebinding the manifest
to implementation commit `af37220f5000bfb71d60a39232185511275ae02d`, the final
runner completed in approximately `22.134` seconds and returned exit code `2`.
The pre-endpoint receipt was written before the WEE1 column was parsed. The
scientific artifacts are byte-for-byte identical to Attempt 002; the summary
receipt differs only because the final implementation commit is recorded.

The endpoint receipt reports `1,292` eligible screens seen and `1,290` median-
collapsed source/model values. The final source-specific results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`;
- design sensitivity: `8bb85d0f76c925f7357c0fce4039647fba070b14a94d6b92d7fdc3961da007c3`;
- endpoint scores: `a4accd2588cc40b0f5a0b4c9b657953de7fbe91c1dc751f4a10b0884e018c6a7`;
- inference: `84cee4bd3b30cc01811b47ac4a8271c1c7eddd8d4862769630b4d56f7e5fc2b8`;
- normalized summary: `f4dd574713f3ae0b450896b53e71c3b144cc36151bf37be3ce69bd3253f93572`;
- pre-endpoint receipt: `4cd616be9dc7742f020598e5e9b4cfdbf2ab3e24fa5538ade88cbd07e08be656`.
