# Experiment report: [descriptive title]

> **Template:** Replace every bracketed field. Delete guidance text only after the required information is supplied.
> **Claim class:** Experimental result
> **Testing status:** [completed / failed before completion]
> **Validation status:** [supported / not-supported / mixed / inconclusive]
> **Observed effect:** [beneficial / harmful / mixed / no-detectable-effect / inconclusive]

The existence of this report means an experiment was attempted; it does not imply that the treatment improved performance. `Validation status` addresses the preregistered claim; `observed effect` describes direction and may differ across dimensions.

Store this report beside a completed `metadata.yaml` based on [the artifact metadata template](artifact-metadata.yaml). Give submitted run records their own governed metadata and link them as parents.

## Identity

- Experiment ID: `[lower-case stable ID]`
- Report version: `[version]`
- Authors and roles: `[people and model assistance]`
- Run dates and timezone: `[ISO timestamps or unknown]`
- Relevant commit: `[full commit hash]`
- Parent artifact IDs and checksums: `[IDs and SHA-256 values]`
- Test-case IDs and versions: `[cases]`
- Rubric version or commit: `[reference]`
- Preregistration location and timestamp: `[path/commit or none, with reason]`
- License: `[identifier or unknown with explanation]`

## Question and hypotheses

State the exact intervention question. Separate the primary hypothesis, secondary hypotheses, and expected treatment costs. Identify what outcome would count against the handoff.

## Conditions

| Code | Model and exact identifier | Handoff treatment | Trials | Notes |
| --- | --- | --- | ---: | --- |
| B | [successor] | None | [n] | Baseline |
| T | [same successor] | [artifact ID, checksum, placement] | [n] | Treatment |
| R | [optional origin model] | [state instructions] | [n] | Optional reference; not ground truth |

Explain any mismatch in interface, mode, tools, context, settings, dates, or system instructions.

## Environment and controls

Record for each condition:

- provider, product/interface, model display name, and exact identifier;
- reasoning mode or effort;
- system and developer instructions when publishable, otherwise `withheld` and why;
- available and used tools, permissions, attachments, retrieval sources, and network access;
- context window or observed context use, output limit, sampling settings, and seed when exposed;
- task order, condition order, fresh-context policy, and carryover controls;
- treatment token count, placement, and any competing context removed to fit it;
- evaluator identities or pseudonyms, blinding, randomization, and conflicts;
- planned trial count, stopping rule, exclusions, and failure handling.

Use `unknown` rather than reconstructing unavailable settings.

## Procedure

Give commands or steps sufficient for another contributor to rerun the experiment. Identify any proprietary or unavailable component and the closest valid reproduction path. State whether the procedure was followed before summarizing results.

## Deviations and failures

List every departure from the preregistered plan, infrastructure failure, excluded run, retry, manual intervention, and post-hoc analysis. Include condition and run IDs. Write `None observed` only after checking run records.

## Run-level records

Link all inputs, outputs, tool transcripts or publishable summaries, checksums, score records, errors, exclusions, token counts, and latency records. Do not include only selected examples.

| Run ID | Case | Condition | Output path | Excluded | Error | Score-record path |
| --- | --- | --- | --- | --- | --- | --- |
| [run] | [case] | [code] | [path] | [yes/no] | [value] | [path] |

## Results

Report the preregistered primary outcome first, with trial counts and uncertainty appropriate to the design. Then report every rubric dimension, critical-failure count, unsupported-claim count, refusal rate, and available cost measure. Preserve evaluator-level disagreement.

Distinguish:

- observations directly computed from run records;
- judgments produced by evaluators;
- exploratory analyses added after results were visible.

## Interpretation

State the narrowest conclusion the data support. Name plausible alternative explanations, confounds, sensitivity to exclusions or weights, and evidence that would reverse the conclusion. Do not generalize beyond tested tasks, versions, interfaces, tools, and dates.

## Negative and inconclusive findings

Record regressions, null dimensions, failed cases, unsafe behavior, increased rigidity, verbosity, latency, and unanswered questions. This section is required even when the primary outcome is positive.

## Reproduction guidance

Identify the minimum files and commands needed to reproduce the study, expected nondeterminism, unavailable settings, and which finding should be reproduced first. A future reproduction must receive its own experiment ID and report deviations.

## Disclosure checklist

- [ ] All planned conditions and trials are accounted for.
- [ ] Raw outputs and score records are linked and checksummed.
- [ ] Model, interface, mode, tools, date, and treatment placement are recorded or marked unknown.
- [ ] Exclusions and stopping decisions were fixed in advance or disclosed as post-hoc.
- [ ] Evaluator blinding, bias, order effects, and prompt leakage are discussed.
- [ ] Version drift, context differences, tool differences, and stochastic variation are discussed.
- [ ] Negative and inconclusive results are included.
- [ ] Testing status is not presented as proof of improvement.
- [ ] No private, personal, confidential, or proprietary material is exposed.
