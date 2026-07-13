# Project principles

> **Document role:** Repository policy
> **Claim class:** Operational proposal
> **Status:** Initial policy; not an experimental result

Frontier Handoff exists to collect and test explicit instructions, procedures, and other operational artifacts produced during temporary model access. It does not assume that a model is authoritative about itself or that text can transfer latent capability. These principles govern repository content, contribution review, and interpretation.

## 1. Preserve raw outputs

A raw artifact is a byte record, not an editable draft. Store it without front matter, corrections, whitespace normalization, or silent typo fixes. Record a SHA-256 checksum over the stored bytes. Put explanations and warnings in adjacent metadata or review files.

If the available source has already been transformed by an interface, export, copy operation, or redaction, disclose that fact. Do not call a reconstruction byte-identical to an unavailable original.

## 2. Separate source material from interpretation

Prompts, raw outputs, curated derivatives, critiques, and experiment reports are separate records. Link them with stable IDs and repository-relative paths. Never insert editorial conclusions into a raw file or present a review as part of the source output.

## 3. Record provenance at the level actually known

Record the model display name, exact identifier, provider, product or interface, reasoning mode, tools, date, attachments, context, and relevant system instructions when they are known and may lawfully be shared. Distinguish an observed value from a contributor-reported value. A display name is not evidence of an exact model build.

A checksum establishes that repository bytes have not changed since the checksum was recorded. It does not establish who produced them, which prompt caused them, or whether a model attribution is authentic.

## 4. Use unknown instead of completing the story

Use **unknown** when a material fact cannot be established. Omit a field only when the provenance standard marks it optional and its absence is not misleading. Never infer a provider, timestamp, model version, setting, or license from a plausible naming convention.

## 5. Treat model self-reports as hypotheses

A model's account of its strengths, weaknesses, reasoning, training, or relationship to another model is generated testimony. Label it as a hypothesis unless independent evidence supports a narrower claim. Eloquence, specificity, and confidence do not increase its evidentiary status.

## 6. Prefer reproducible tests over persuasive prose

An operational proposal earns support by changing measured performance under documented conditions, not by sounding sophisticated. Preserve the task, conditions, model configuration, tools, outputs, scoring criteria, exclusions, and repeated trials needed to inspect the result.

## 7. Preserve disagreement

Keep materially different human and model critiques visible. Do not edit several reviews into artificial consensus. A synthesis may explain the disagreement, but it must link the underlying records and identify which conclusions remain unresolved.

## 8. Separate model capability from product scaffolding

Do not attribute an observed difference to a model when the comparison also changes tools, system instructions, retrieval, context window, product features, latency budget, or other interface behavior. Document those differences and narrow the conclusion accordingly.

## 9. Avoid benchmark theater

Do not optimize for an impressive aggregate score while hiding weak cases, subjective judgments, treatment overhead, or changed conditions. Predeclare cases and criteria when practical. Report dimension-level and run-level results, including failures. A leaderboard is not a substitute for causal evidence.

## 10. Publish negative and inconclusive results

A transferred instruction may help, do nothing, or make performance worse. Report all three outcomes with the same provenance standard. Do not classify “tested” as “supported,” and do not remove a failed trial because it complicates the narrative.

## 11. Never silently rewrite history

Corrections to metadata must be dated and described. Changes to substantive content create a new derivative artifact with its own ID, checksum, editor, parent reference, and modification record. A superseded or deprecated record remains available unless removal is necessary for security, privacy, or legal reasons.

## 12. Publish criteria before judgment

Define the task, scoring dimensions, acceptable evidence, failure conditions, and adjudication process before inspecting treatment outputs whenever feasible. Post-hoc criteria must be labeled as such. A reviewer who knows the condition should disclose that limitation.

## 13. Scope every evidence claim

“Supported,” “reproduced,” and “verified” apply only to the model versions, conditions, tasks, dates, and criteria actually examined. Do not generalize from one artifact, model, or benchmark to frontier models as a class. A verified finding is a scoped synthesis, not a permanent universal fact.

## 14. Keep evidence dimensions independent

Raw preservation, human review, cross-model review, experimental testing, reproduction, and editorial deprecation answer different questions. Track them separately. A reviewed artifact is not thereby correct; a tested artifact is not thereby helpful; a reproduced effect is not thereby universal.

## 15. Make intervention costs visible

Measure or disclose instruction length, context consumption, latency, token use, refusal rate, rigidity, and verbosity where they matter. An instruction that improves correctness while making ordinary tasks unusable has a tradeoff, not an unqualified win.

## 16. Minimize collection and protect contributors

Collect only the context needed to understand or reproduce an artifact. Never require private system prompts, secrets, personal data, confidential conversations, proprietary code, or material the contributor lacks permission to publish. Redactions must be visible and described.

## 17. Prefer simple, inspectable infrastructure

Use readable Markdown and YAML, repository-owned validation, and ordinary Git history while the collection is small. Add databases, runners, formal schemas, or leaderboards only when real contributions demonstrate a need that outweighs maintenance and migration cost.

## 18. Make correction and dispute first-class

Allow contributors to challenge attribution, interpretation, scoring, and conclusions without rewriting the historical record. Link corrections and counterevidence to the artifact they address. The goal is an auditable disagreement, not a single institutional voice.

## Applying the principles

The [artifact lifecycle](artifact-lifecycle.md) defines independent evidence dimensions. The [provenance standard](../methodology/provenance-standard.md) defines the metadata needed to apply these principles, and the [evaluation protocol](../methodology/evaluation-protocol.md) defines how claims of improvement should be tested.
