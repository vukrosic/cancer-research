# EXP-20260822-027 execution log

## Frozen boundary

- selection seal commit: `756a928`;
- implementation commit: `45a6bdd`;
- manifest binding commit: `6fb646b`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `EZH2 (2146)`;
- runner: `.venv/bin/python -m candrel.arid1a_ezh2_replication`.

The first local metadata helper printed a different planning-power pair because
it used a different status-label convention. The frozen executable engine was
rerun before implementation, producing the bound planning values Avana `0.8621`
and KY `0.5760`; the correction is documented in the selection seal and methods
audit.

## Execution

The bound runner completed in approximately `20.17` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the EZH2 column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `d808bd50211f644697a2606504e94e8a0cf588c212c8f4e651114821f36b2aad`;
- design sensitivity: `c47db1bf4e19ee9af4978bad1ddc4c4f3c1de49bf0f84dafb32c8ce2dd9c6993`;
- endpoint scores: `7925b76cd2606684633532c74107cb6305643d51dcb6012946312063778ae59c`;
- inference: `1534c8682958c01ac77f248350e9d36c77aaf824e18895b233ad02be5a50ab97`;
- normalized summary: `dcf59dc6fc31ade64fa631258f0a30ba43e0eb1cb3e4fa293cb5f220a3765053`;
- pre-endpoint receipt: `c5d8fd516a70641842e65fa1b98ab20a1f9eb72234a9a20e8769d6e8105e6b8e`.
