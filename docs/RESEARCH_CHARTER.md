# Research charter

## Objective

Build a public, reproducible evidence base for deciding which cancer genetic
vulnerability claims deserve costly orthogonal validation.

## Primary question

Which lineage-, biomarker-, or paralog-loss-associated dependencies retain their
direction, practical effect size, and uncertainty threshold when the screen family
is held out?

## Success criteria

- A frozen, versioned benchmark spanning independent Broad and Sanger screens.
- Positive controls recovered before novel candidates are evaluated.
- Candidate claims include effect sizes, confidence intervals, sensitivity tests,
  artifact flags, and explicit falsification outcomes.
- At least one useful output even if no candidate replicates: a negative catalogue
  and a tested protocol showing where discovery claims fail.
- One-command reproduction on a 16 GB Apple Silicon Mac.

## Hard boundaries

- Public, non-identifiable data only.
- Maximum 12 GB project storage; processed matrices, not raw sequencing reads.
- No clinical recommendations.
- No mechanistic or actionability claim without orthogonal experimental evidence.
- No novelty claim until the exact candidate passes a targeted prior-art audit.

## Research phases

1. Engineering/positive-control gate using source-tagged paired screens.
2. Freeze candidate contexts and independent evaluation thresholds.
3. Reproduce known biomarker dependencies, starting with MSI–WRN in colorectal models.
4. Test predeclared paralog-loss and rare-subgroup candidates.
5. Validate release stability and artifact sensitivity.
6. Produce a target-hypothesis ledger suitable for wet-lab handoff.
