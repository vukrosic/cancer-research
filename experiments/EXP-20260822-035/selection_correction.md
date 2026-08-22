# EXP035 selection metadata correction

Before the single endpoint execution, boundary validation found that the
`CRISPRScreenMap.csv` SHA-256 had been transcribed incorrectly in the
outcome-free candidate census and selection seal: the committed selection
draft omitted the `71` segment in the digest. The census, selection seal, and
manifest were corrected to the frozen input hash
`1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad`.

This was a metadata-only correction. No ENDOD1 score row or endpoint value was
opened while it was made, and the runner executed only after the corrected
selection artifacts passed the implementation-boundary check. The corrected
files are included in the EXP035 release commit; the original preregistration
commit `3cffc90` is retained in Git history for auditability.
