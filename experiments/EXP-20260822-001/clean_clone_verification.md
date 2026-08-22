# Clean-clone verification

Verified: 2026-08-22T10:28:13+02:00  
Source commit: `573cf94`

A fresh local clone with no raw cache successfully:

1. installed the locked environment with `uv sync --extra dev`;
2. passed all six tests;
3. fetched all 16 API inputs;
4. matched every tracked expected SHA-256 hash;
5. reproduced 8 eligible genes, median Spearman 0.4222399196689809,
   positive-rho fraction 1.0, and final status PASS.

The rerun receipt reported input-receipt SHA-256
`2086b1f686c28aa87fe2e82228792f98533ca82c14ba3b6a7a07b901d829b2e9`.
The temporary clone was moved to the macOS Trash after verification and is recoverable
until the Trash is emptied.
