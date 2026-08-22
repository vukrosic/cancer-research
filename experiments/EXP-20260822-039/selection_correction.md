# EXP039 pre-endpoint correction

## Attempt 001

The first bound invocation stopped at `T0_INPUT_HASH` before loading any
endpoint value. The error receipt reported a screen-map SHA-256 mismatch. The
failure was caused by a two-character transcription error in the EXP039
implementation and manifest (`...c65806657c3f8...` instead of the actual
frozen digest `...c65806657f3c8...`).

The five current input files were independently rehashed. The endpoint,
screen-QC, screen-map, model, and damaging-matrix files all match the corrected
frozen digests. No endpoint row or PARP1 value was opened during the failed
attempt.

## Remediation

The corrected digest was applied to the implementation, manifest, and sealed
selection contract before endpoint access. The candidate identity,
PBRM1-or-ARID2 composite rule, canonical roster, planning powers, seeds, gates,
and claim boundary are unchanged. The failed receipt is preserved in
`attempt_001_t0_error_receipt.json`. Only a corrected bound invocation may
proceed.
