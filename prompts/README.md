# Prompts

This directory preserves prompts used to elicit, critique, transform, or evaluate Frontier Handoff artifacts. Prompt records are evidence about an intervention; they are not evidence that the intervention works.

Prompts and outputs live in separate top-level directories because they have different histories. A prompt may produce multiple outputs, and an output may later receive multiple critiques or evaluations. Repository-root-relative paths and stable IDs connect the records.

## What a prompt package should contain

Each prompt package should include:

- `prompt.md`: the exact prompt text inside an unmistakable verbatim block, with any explanation outside that block;
- `README.md`: purpose, provenance, known gaps, and links to reported outputs;
- `metadata.yaml`: a stable prompt ID, content checksum, modification record for any surrounding documentation, model/environment fields, and evidence state.

Do not silently repair spelling, whitespace, punctuation, or line wrapping inside a source prompt. If a normalized or revised prompt is useful, add it as a separate version and describe every change.

Model names, target relationships, generation dates, product interfaces, modes, tools, and prompt-to-output relationships must be labeled as observed, contributor-reported, or `unknown`. Possessing both a prompt and an output does not independently prove that one generated the other.

## Included prompt

- [Fable 5 standing-orders prompt](fable-5/001-standing-orders/README.md) — prompt artifact `fable-5-001-standing-orders-prompt`, reported as the origin of output artifact `fable-5-001-standing-orders`.

Reusable prompt patterns belong in [`prompts/templates/`](templates/). They are templates, not records of completed model runs.
