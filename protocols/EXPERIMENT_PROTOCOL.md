# Experiment protocol

Each experiment has a permanent ID and directory. Before evaluation, record:

- hypothesis and null;
- discovery/test boundary and biological split unit;
- inclusion/exclusion rules;
- primary and secondary endpoints;
- minimum practical effect;
- statistical test and multiplicity correction;
- negative controls and artifact checks;
- seed and compute budget;
- stopping and pivot rules.

At launch, freeze a machine-readable manifest containing input URLs and hashes, code
commit/dirty state, environment, entrypoint, seed, expected outputs, and parent ID.
Any post-result change becomes a child experiment. Never replace a metric, exclusion,
or cohort in place.

Every completed or failed run receives `result.md` with claim tier, exact command,
status, effect sizes, uncertainty, gate outcomes, limitations, and next decision.
