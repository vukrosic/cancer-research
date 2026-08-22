# Agent operating contract

Read `state/task_spec.md`, `state/progress.json`, and `state/STATE.json` before work.
Then read the current experiment preregistration and manifest.

## Non-negotiable rules

- This is computational hypothesis generation, not medical advice.
- Never claim a treatment, therapeutic window, patient benefit, or clinical utility.
- Never overwrite a completed experiment. Changes create a new child experiment.
- Freeze cohort, endpoints, exclusions, metrics, and stopping rules before evaluation.
- Split by biological and experimental unit; preserve source, site, library, and model IDs.
- Fit all preprocessing and selection on discovery data only.
- Preserve failures and null results with uncertainty intervals.
- Raw source data remain untracked unless redistribution terms explicitly permit it.
- Verify citations from primary papers or official resources before relying on them.
- “Novel” requires a narrow statement and a dated prior-art ledger; absence is not proof.
- No wet-lab, clinical, or external-service action is implied by repository work.

## Experiment lifecycle

1. Create `experiments/EXP-YYYYMMDD-NNN/preregistration.md`.
2. Create `manifest.json` with frozen inputs, hashes, code state, seed, and entrypoint.
3. Run the smallest data/correctness gate.
4. Save commands, stdout/stderr, metrics, plots, and failure traces.
5. Write `result.md` even when the run fails or the hypothesis is rejected.
6. Append findings and iteration state; do not rewrite history.
7. Run tests before committing.

## Claim tiers

- T0 engineering: a pipeline executes and reproduces.
- T1 descriptive: an association exists in named public data.
- T2 predictive: a frozen claim replicates in a held-out screen or dataset.
- T3 biological hypothesis: a mechanism is plausible and awaits orthogonal experiments.
- T4 clinical: out of scope without clinically appropriate validation.

## Stall handling

Zero new findings or a metric drop increments `stale_count`. At two stale iterations,
change a structural assumption rather than tuning parameters. At four, record a human
attention item. A work session is capped at 15 rounds or 30 minutes.
