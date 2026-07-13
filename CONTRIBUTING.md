# Contributing to Frontier Handoff

Frontier Handoff accepts source artifacts, critiques, evaluation materials, reproductions, and corrections. The standard is traceability, not agreement with a preferred model or conclusion.

Read the [project principles](docs/project-principles.md), [provenance standard](methodology/provenance-standard.md), and [security policy](SECURITY.md) before contributing. For experiments, also read the [evaluation protocol](methodology/evaluation-protocol.md).

## Before submitting any model material

Confirm that you have permission to publish every included prompt, output, attachment, excerpt, and configuration detail. Remove material you cannot lawfully or safely disclose. Do not submit:

- API keys, access tokens, cookies, credentials, or private keys;
- private system prompts you lack permission to publish;
- customer data, confidential conversations, or private repository content;
- personal information not necessary and consented to;
- proprietary source code, documents, or datasets without permission.

Redaction changes content. If a source needs redaction, retain the original privately only when lawful, publish a clearly labeled derivative, describe every redaction, and do not call the public file raw.

## Required disclosure

For every generated output or experiment, report the following when available and use `unknown` when it is not:

- model display name and exact model identifier;
- provider;
- product or interface;
- model mode or reasoning effort;
- generation date and timezone;
- tools available and whether each was used;
- attachments or context supplied;
- sampling settings, seed, context limit, and output limit;
- relevant system instructions when legally and practically shareable;
- whether the output was edited, by whom, and a complete edit description;
- test conditions, treatment placement, trial count, and exclusions;
- content license or the reason rights are unknown;
- who supplied each attribution when it was not independently observed.

Disclosure of secrets, personal data, proprietary information, or nonpublishable system prompts is never required. Record the field as `withheld` with a general reason when even naming the detail would create risk.

## Contribution paths

### Propose an extraction prompt

1. Open an artifact proposal issue and state the operational knowledge the prompt is intended to elicit.
2. Explain likely failure modes and how the resulting output could be tested.
3. Add the prompt under `prompts/` only after it has a stable ID and metadata.
4. Preserve verbatim prompt text in a clearly marked block. Put commentary outside that block.
5. Do not claim the prompt works until a documented comparison supports that claim.

### Add a raw artifact

1. Create a globally unique ID using lower-case letters, digits, and hyphens.
2. Preserve the original bytes as `raw.<extension>` without front matter or normalization.
3. Store all labels in adjacent `metadata.yaml`; record the SHA-256 digest and byte count.
4. Link the exact prompt when known. If the pairing or model attribution is contributor-reported, say so.
5. Add review notes separately. Never insert review comments into the raw file.
6. State the artifact-level license. `unknown` is preferable to an unsupported rights claim.

If an output was edited before you received it, it is not raw from the model. It may still be submitted as a source record if the edit history is explicit.

### Add a model critique

Create a separate artifact with its own ID, adjacent `metadata.yaml`, prompt, raw output, model provenance, and parent IDs. State the critique question and review scope. A cross-model critique is generated evidence, not independent verification merely because another model produced it.

### Add an evaluation

Fix the case and scoring criteria before judging treatment outputs. Compare a no-handoff baseline with the handoff condition using the same successor model and matched settings. Preserve run-level data, repeated trials, all preregistered dimensions, exclusions, and negative or inconclusive results. Give every submitted test case, experiment design, run, and report its own stable ID, checksum, adjacent `metadata.yaml`, and parent links. Use the [experiment report](templates/experiment-report.md), [test-case template](templates/test-case.md), and [metadata template](templates/artifact-metadata.yaml).

### Report a reproduction

Identify the original experiment and commit, distinguish exact from conceptual reproduction, and list every setup difference. Create a governed reproduction-report artifact with adjacent `metadata.yaml`, parent links, and run-level evidence. Report finding-level outcomes as reproduced, not reproduced, mixed, or inconclusive. Do not turn a partial match into a universal confirmation.

### Dispute a conclusion

Disagreement is a contribution. Link the exact claim, identify the evidence or assumption in dispute, state what observation would change your view, and add a critique or counter-result when possible. Do not rewrite the disputed historical record.

### Correct metadata

Correct factual metadata in a focused pull request. Append a `metadata-corrected` entry under `lifecycle_events` with the date, contributor, affected field, old value, new value, evidence basis, and reason in its description. A checksum correction requires rechecking the raw bytes and explaining why the previous value was wrong. Content corrections require a new derivative or superseding artifact, never a changed raw file.

## Pull request expectations

- Keep one logical contribution per pull request when practical.
- Link parent artifacts, prompts, cases, and results with repository-relative paths.
- Label unknown facts as `unknown`; do not infer exact model IDs from display names.
- Separate observed facts, contributor reports, model claims, reviews, and experimental observations.
- Confirm that raw files are unchanged and checksums match.
- Run:

  ```sh
  python3 -m unittest discover -s tests -v
  python3 scripts/validate_repository.py
  ```

- Complete the pull request checklist, including privacy and licensing review.

Maintainers may request narrower claims, additional provenance, or a reproducible case. Rejection of unsupported claims is not rejection of the underlying artifact; raw records can remain useful when their limitations are clear.
