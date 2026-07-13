# Evaluation results

This directory is reserved for completed, run-level evaluation records. It contains no result in the initial repository.

A result submission must include:

- an experiment report using [the repository template](../../templates/experiment-report.md);
- adjacent governed metadata for the report and each submitted run, using [the metadata template](../../templates/artifact-metadata.yaml);
- immutable case and treatment versions or commit references;
- all publishable run-level inputs and outputs, not selected examples only;
- checksums and exact model/environment provenance where available;
- preregistered exclusions, scoring records, evaluator disagreement, and treatment costs;
- harmful, mixed, no-detectable-effect, failed, and inconclusive trials;
- a clear separation between observed results and interpretation.

Use one directory per experiment ID. A reproduction receives a distinct ID and links its parent experiment; it must not overwrite the original report.
