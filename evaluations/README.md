# Evaluations

This directory defines how Frontier Handoff tests a handoff artifact as an intervention.

The default comparison is:

- **Baseline:** a successor model receives the task without the transferred instructions.
- **Treatment:** the same successor model receives the same task plus the transferred instructions.
- **Optional reference:** the reported originating model receives the same task under documented conditions.

The reference arm cannot establish ground truth merely by being the source model. Model versions, product interfaces, system instructions, tools, context limits, and inference settings must be matched or recorded as confounds.

Start with the [evaluation protocol](../methodology/evaluation-protocol.md), [rubric](rubric.md), and [test-case specification](test-case-schema.md). Use the [test-case](../templates/test-case.md) and [experiment-report](../templates/experiment-report.md) templates.

Every submitted test case, experiment design, run, report, comparison, and reproduction is a governed artifact. Give each a stable ID and adjacent `metadata.yaml` using the [artifact metadata template](../templates/artifact-metadata.yaml). The inline identity section in a Markdown template does not replace its metadata sidecar.

## Evidence rules

- Fix cases, outcomes, weights, exclusions, and stopping rules before viewing treatment results.
- Preserve run-level outputs; do not publish only selected examples or aggregate scores.
- Use repeated trials and randomized order.
- Blind evaluators to condition and artifact authorship where feasible.
- Record treatment token, latency, refusal, and rigidity costs when available.
- Publish negative, mixed, failed, and inconclusive runs.
- Separate the fact that a test ran from its outcome.
- Scope every conclusion to the models, dates, tools, cases, and settings observed.

`results/` currently contains only its [submission guide](results/README.md). No experiment result is included in the initial repository.
