# Independent audit and corrections

Audit date: 2026-08-22  
Initial verdict: **NO-GO for publication**  
Auditor: independent Codex agent, read-only

## What the auditor reproduced

- Every saved numerical field from the cached full API payloads.
- All 16 raw input hashes.
- 8 eligible genes, 177 paired models per gene, median rho 0.4222, all rho positive.
- The retry changed API projection only; scientific inputs and gates were invariant.
- No bug in Spearman, bootstrap, permutation, aggregation, or gate calculations.

## Blocking findings and resolution

1. No Git commit or executable input lock: resolved by adding a tracked acquisition
   receipt and hash enforcement. A changed API response now stops with `Input drift`.
2. Retry exceeded the literal network-only rule: retained as a protocol deviation;
   neither the failed output nor original wording was erased.
3. “Context-selective signal” was not tested: removed from current README and result
   interpretation. The original preregistration is preserved and corrected here.
4. “Dependency sign agreement” was misleading: future output uses threshold-class
   agreement and reports the full 2x2 contingency counts. The original output key is
   preserved as historical evidence and explicitly deprecated.
5. Tests were too narrow: added receipt-drift tests, exact aggregate-gate testing, and
   an offline fixture-backed end-to-end run.

## Publication gate

Do not publish until the repository is committed, the manifest points to a real code
commit, the corrected verification run passes, and the independent auditor rechecks
the changes.
