# Model-condition comparison: [title]

> **Template:** A model name is not an experimental condition. Replace every bracketed field and report environment differences.

Store a submitted comparison beside governed `metadata.yaml` based on [the artifact metadata template](artifact-metadata.yaml), and retain the governed run/report parents it summarizes.

## Comparison question

- Decision this comparison supports: [question]
- Primary outcome fixed before review: [outcome]
- Cases and versions: [IDs]
- Rubric and commit: [reference]
- Comparison type: [same-model instruction intervention / cross-model reference / other]

## Condition matrix

| Condition | Provider | Exact model ID | Interface | Mode | Tools | Context | Instructions | Trials |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| [A] | [value] | [value] | [value] | [value] | [value] | [value] | [checksum/path] | [n] |
| [B] | [value] | [value] | [value] | [value] | [value] | [value] | [checksum/path] | [n] |

For unknown values, write `unknown`. For nonpublishable details, write `withheld` and a general reason. Do not infer exact identifiers from display names.

## Comparability assessment

List every matched factor and every known difference: dates, snapshots, system instructions, product scaffolding, context limits, treatment token use, sampling, tools, permissions, attachments, retrieval, latency budget, and evaluator exposure. Classify each difference as unlikely, plausible, or severe confounding and explain the criterion.

If conditions are not comparable enough for a causal claim, retain a descriptive comparison and say so.

## Results by dimension

| Dimension | A | B | Difference and uncertainty | Critical failures |
| --- | ---: | ---: | --- | --- |
| Correctness | [value] | [value] | [value] | [value] |
| Completeness | [value] | [value] | [value] | [value] |
| Unsupported claims | [value] | [value] | [value] | [value] |
| Calibration | [value] | [value] | [value] | [value] |
| Instruction following | [value] | [value] | [value] | [value] |
| Task-specific usefulness | [value] | [value] | [value] | [value] |
| Adaptability (absence of excessive rigidity) | [value] | [value] | [value] | [value] |
| Conciseness (absence of needless verbosity) | [value] | [value] | [value] | [value] |
| Verification quality | [value] | [value] | [value] | [value] |
| Handling of ambiguity | [value] | [value] | [value] | [value] |
| Recovery from false premises | [value] | [value] | [value] | [value] |
| Operational safety | [value] | [value] | [value] | [value] |

Link run-level data and evaluator records. Report output tokens, latency, tool calls, refusals, and evaluator agreement separately.

## Interpretation boundaries

- What the observations support:
- What they do not support:
- Negative, mixed, or inconclusive findings:
- Alternative explanations:
- Version and date scope:
- Highest-value reproduction:

Never convert “Condition A scored higher here” into an unqualified claim that its model is stronger.
