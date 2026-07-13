# Codex architecture opinion

> **Document class:** Model opinion and architectural proposal
> **Author label:** GPT-5.6-SOL, as designated by the repository initialization task
> **Claim class:** Operational proposal
> **Evidence status:** Not experimentally validated; not a statement from OpenAI

## Bottom line

Frontier Handoff is worth building if it behaves like an evidence repository, not a shrine to model output. Temporary access to a model can produce useful explicit procedures, prompts, critiques, and test ideas. Text cannot preserve a model's weights, latent capability, private reasoning, product environment, or tool access. The phrase “knowledge transfer” is therefore a research framing to test, not a mechanism this repository should claim to have established.

The strongest version of this project preserves source records, makes provenance gaps conspicuous, and tests whether an instruction changes successor-model behavior under controlled conditions. The weakest version accumulates eloquent prompts and outputs, calls them wisdom, and never measures whether they help.

## What is strong about the concept

- Time-limited access creates a practical reason to collect explicit operational policies while collection is possible.
- Prompt/output pairs can expose concrete hypotheses about failure modes and mitigations.
- Cross-model disagreement can generate useful test cases rather than being edited into false consensus.
- A public record can improve reproducibility by retaining exact inputs, outputs, model settings, tools, and negative results.
- Successor instructions are interventions that can be compared with a baseline. That makes at least part of the idea empirically tractable.

## What could make it misleading or low-value

The main risk is authority laundering: a claim gains status because a model described itself as unusually capable, not because the claim survived review or experiment. Model self-reports are generated testimony. They may be insightful, post-hoc, generic, product-conditioned, or wrong.

Other failure modes are predictable: unverifiable model aliases; edited “raw” outputs; missing system or tool context; selective publication of positive runs; public benchmarks tuned after seeing results; evaluator knowledge of the treatment; model-version drift; and comparisons that confound instructions with tool access, context length, latency budget, or product scaffolding. A checksum detects later byte changes. It does not authenticate the model, prompt, date, or causal history.

This project also risks mistaking ceremony for improvement. Long universal checklists can increase refusals, latency, verbosity, and rigidity while appearing more careful. A persuasive artifact is not evidence that the artifact improves task performance.

## Prompts and outputs should be separate, but linked

Prompts and outputs should live in separate top-level collections. They have different reuse, review, and versioning patterns: one prompt can generate several outputs, and one output can receive several critiques or evaluations. Co-locating them as if they were one document encourages silent rewriting and weakens chain-of-custody reasoning.

Separation must not make the relationship hard to follow. Stable IDs, relative paths, parent references, and adjacent metadata should link each raw output to its reported prompt. Matching numeric slugs make browsing easy without pretending that directory proximity proves causation.

## Raw and curated outputs are different records

A raw output is an immutable byte record. It receives no front matter, corrections, normalized whitespace, or silent typo fixes. Descriptive metadata and review notes sit beside it. Repository attributes disable text normalization for raw files, and a SHA-256 digest detects drift.

A curated output is a new artifact with its own ID, checksum, editor, date, parent IDs, and modification description. It may correct, annotate, reorganize, or scope a raw output, but it never replaces the raw record. A diff should be easy to produce. “Reviewed” describes scrutiny; it does not mean “true.”

## Model self-reports and claim labels

Statements about a model's strengths, weaknesses, reasoning, or successor should be labeled as hypotheses unless independent evidence supports a narrower classification. Generated operational instructions are normally **operational proposals**. A critique can support a **reviewed recommendation**, but only when its review scope and reviewer provenance are recorded. An **experimental result** reports observations under stated conditions. A **verified finding** should be rare, scoped to explicit evidence, and never imply universal validity.

The first Fable 5 artifact should therefore remain `raw` with claim class `operational-proposal`. Its attribution to Fable 5 and target relationship to Claude Opus 4.8 are user-reported provenance; those facts do not appear in the artifact bytes.

## Provenance should record facts and their source

Each record should identify what is observed, what is reported, and what is unknown. Useful fields include stable ID, artifact type, claim class, content path, prompt path, parents, source and target model display names, exact identifiers, provider, interface, mode, tools, attachments/context, dates, edit history, review records, evidence state, license, relevant commit, and a content checksum.

Fields that cannot realistically be known must be optional or accept `unknown`. A display name is not an exact model identifier. Repository metadata should identify who supplied an attribution. System instructions should be recorded only when legally and practically shareable; secrets and proprietary prompts are not the price of contribution.

The initialization request names `/mnt/data/standing-instructions(1).md`, which is absent in this environment, and separately directs import from `~/Downloads/standing-instructions.md`. The available Downloads file will be used. Metadata should retain the user-reported original filename and separately record the observed import filename and this discrepancy.

## Evaluation should compare an intervention, not reputations

The primary comparison is the same successor model under matched conditions without and with the transferred instructions. The originating model is an optional reference arm, not a ground truth oracle. Cases and scoring criteria should be fixed before judging outputs. Runs should preserve exact task text, condition, model identifier, interface, settings, tools, context, output, timing or token data when available, and exclusions.

Evaluation should use randomized condition order, blind scoring where feasible, repeated trials, and run-level results. It must discuss subjective judgment, evaluator bias, prompt leakage, order effects, version drift, stochastic variation, context-window and tool differences, and treatment overhead. Correctness and safety matter, but so do rigidity, verbosity, unnecessary refusal, and task usefulness. Negative and inconclusive results belong in the record.

No scalar score should erase dimension-level results. “Experimentally tested” should not imply “improved,” and “independently reproduced” should describe a separate replication under documented conditions.

## Status is multidimensional

I disagree with a single linear lifecycle from proposed to reproduced. These are partly events and partly independent evidence dimensions. The repository should track:

- content state: proposed, raw, curated, superseded, or deprecated;
- review evidence: human and cross-model review records;
- evaluation evidence: not tested or tested, with outcome kept separately;
- reproduction evidence: not attempted, reproduced, not reproduced, mixed, or inconclusive;
- append-only events: generated, imported, reviewed, tested, revised, superseded, and deprecated.

This prevents a human review from being misread as experimental confirmation and prevents a failed reproduction from being hidden behind a mature-looking status.

## What should be postponed

Do not build a web application, database, package, automated model runner, leaderboard, universal aggregate score, ontology service, or elaborate schema migration system yet. Do not add a curated derivative of the first artifact before a review purpose and edit policy exist. Do not pre-populate benchmark results or model comparisons.

A human-readable standard, reusable templates, one narrow validator, and tests are enough for the first version. A formal schema or results database becomes worthwhile only after several real contributions reveal stable requirements.

## Structure chosen

The repository keeps the requested top-level structure because it maps to real responsibilities:

```text
docs/          project concepts, lifecycle, terminology, and explicit opinions
methodology/   protocols for extraction, review, evaluation, provenance, limits
prompts/       source prompts and prompt-specific templates
artifacts/     immutable raw outputs, metadata, and clearly separate reviews
evaluations/   rubric, case specification, and future run-level results
templates/     reusable metadata, experiment, comparison, and case records
scripts/       repository-owned validation
tests/         validator regression tests
.github/       contribution forms and continuous validation
```

`prompts/templates/` is reserved for model-facing prompt patterns. Top-level `templates/` is reserved for contributor-facing records. Future curated outputs should use a clearly named derivative path under the corresponding artifact directory rather than altering `raw.md`.

I am adding only `scripts/` and `tests/` beyond the proposal. They materially reduce provenance errors and keep validation reproducible. I am not adding a formal schema directory now because a prose standard plus an executable validator is less likely to drift during the repository's first real cases.

## Licensing decision

MIT is appropriate for project-authored code and documentation because the repository is small and intended for broad reuse. The repository license must not silently assert rights over imported model outputs or third-party material. Every artifact therefore carries its own license field; `unknown` is the honest value when distribution rights or provider terms have not been established in the available provenance.

## Post-implementation addendum: validator cost

The dependency-free metadata validator became the repository's largest maintenance surface because it implements a conservative YAML subset, evidence-state rules, governed cross-record links, checksums, and Markdown path checks. This is the one initial component I consider potentially overbuilt for two governed records. Its tests and the risk of evidence-label laundering justify retaining it now, but contributors should not expand the custom parser casually. After several real submissions, compare its maintenance cost with a mature YAML parser plus a formal schema, or with a simpler JSON-compatible metadata profile. Keep whichever design makes provenance failures easiest to detect and schema evolution easiest to review.
