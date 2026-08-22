# EXP-20260822-016 independent artifact audit

## Audit status

Initial independent artifact verdict: **NO-GO as a finalized preregistered
receipt; numerically reproducible as a protocol-deviation artifact**.

Auditor: independent Terra agent `01a029e3-403c-7321-9208-d2640dc852c8`.

The audit verified the implementation boundary, all five raw-input hashes,
1,290 source/model units, 1,292 unique eligible screens, duplicate-screen
median collapse, CSV/summary agreement, exact deltas, permutation p-values,
bootstrap intervals, lineage deltas, gate flags, pre-endpoint receipt links,
and normalized summary self-digest.

## Blocking deviation

The frozen candidate census recorded planning powers Avana `0.8622` and KY
`0.5699`, while the executable canonical-roster design receipt recorded
`0.8652` and `0.5875`. The preregistration required exact reproduction of the
planning draw. The working tree also contained an attempted post-completion
relabeling; that relabeling was reverted, and the frozen preregistration is
preserved unchanged. The discrepancy is now documented as a protocol
deviation, with no confirmatory or clinical claim.

## Release gate

This audit must remain **NO-GO for a clean preregistered claim**. A final
artifact re-audit may return GO only for release as an explicitly labeled
`PROTOCOL_DEVIATION_NONCONFIRMATORY` record after the command log and all result
files are tracked in Git.

## Final re-audit — GO for deviation release only

After the complete command log, pre-endpoint receipt, result ledgers, summary,
result card, and audit were staged, the independent auditor returned
**GO-for-deviation-release only** as `PROTOCOL_DEVIATION_NONCONFIRMATORY`.
The staged-bundle check was clean: artifact hashes, normalized summary digest,
implementation boundary, endpoint coverage, deterministic inference, and
terminal `confirmatory_claim: false` labels all verified. The frozen
preregistration and candidate census remain unchanged. This release does not
support a clean preregistered claim, a confirmatory replication claim, a pooled
two-source claim, or any clinical inference.
