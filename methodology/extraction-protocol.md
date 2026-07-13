# Extraction protocol

> **Document role:** Collection protocol
> **Claim class:** Operational proposal
> **Status:** Initial protocol; not experimentally validated

## Purpose

Extraction is the collection of explicit procedures, heuristics, critiques, and testable claims from a model-access context. It does not extract model weights, latent representations, private reasoning, training data, or intrinsic capability. The output is an operational proposal or hypothesis until later evidence supports a different, scoped record.

This protocol applies both to planned generations and to historical outputs imported after the original session. Historical imports may have incomplete provenance; they must disclose the gaps rather than reconstruct them.

## Roles

- The **collector** controls or documents the model session.
- The **source model** is the model reported to produce the output.
- The **target model** is the intended recipient, if one exists.
- The **contributor** submits the records. The collector and contributor may be the same person.

Model names and roles are reported provenance. They do not by themselves establish identity, relative capability, or lineage.

## 1. Define the extraction before prompting

Write a short collection plan that answers:

1. What operational question should the artifact address?
2. Who or what is the intended user or target model?
3. Which tasks and environments are in scope?
4. Which outputs will be retained: every run, a fixed count, or a declared stopping rule?
5. Which later observation could show that the extracted proposal is unhelpful or harmful?
6. Which information must not enter the model context or public repository?

Choose the initial claim class before generation:

- use **hypothesis** for a falsifiable descriptive claim or research question;
- use **operational-proposal** for prompts, instructions, procedures, rubrics, and routing rules.

Do not classify a newly generated instruction as an experimental result, reviewed recommendation, or verified finding.

## 2. Preserve the exact model-facing input

Save the prompt exactly as submitted, including unusual whitespace and punctuation when available. Keep descriptive front matter outside a clearly marked prompt block. Record whether the submitted prompt was copied from another source, edited during the session, or reconstructed later.

The prompt should make the intended deliverable inspectable. When designing a new extraction prompt:

- request concrete triggers, actions, boundaries, dependencies, and failure conditions;
- ask which rules require tools, current information, or privileged context;
- ask for counterexamples and cases where the advice should not apply;
- ask for costly tradeoffs such as latency, token use, verbosity, rigidity, or unnecessary refusal;
- request testable examples without treating the model's examples as validation;
- avoid using claimed model superiority as evidence that the response is correct;
- avoid prompting the model to invent hidden architectural, training, or successor-model facts;
- separate requested self-analysis from externally checkable claims.

A historical prompt may violate these recommendations. Preserve it rather than improving it retroactively, and discuss limitations in a separate review.

## 3. Capture the environment

Record the following before or immediately after the run when the interface exposes them:

- date and time, including timezone;
- model display name and exact model identifier;
- provider;
- interface or product;
- model mode or reasoning-effort setting;
- sampling settings, seed, and other exposed inference parameters;
- tools available and tools actually used;
- attachments, retrieved sources, conversation history, and other context;
- system or developer instructions when legally and practically shareable;
- context-window or output-limit information, if known;
- account, preview, regional, or feature flags that could affect behavior, if safely shareable.

Use **unknown** for a material but unavailable value. Do not infer an exact model identifier from a marketing name. Do not require or publish private system prompts, credentials, personal information, proprietary context, or secrets.

If context must be redacted, record that a redaction occurred, who performed it when shareable, and how the omission could affect interpretation. A redacted transcript is a derivative, not a byte-identical raw record.

## 4. Run the extraction

For a planned collection:

1. Start from the session state named in the collection plan.
2. Submit the preserved prompt without silent edits.
3. Save the complete output immediately, including refusal text, truncation, tool messages, and visible errors.
4. Record whether the output completed normally, hit a limit, was interrupted, or required a continuation.
5. Preserve continuation prompts and segments in order. Do not concatenate them without recording the boundary.
6. Repeat only according to the declared run count or stopping rule.
7. Keep failed, weak, and duplicate-looking runs. Exclusion belongs in later analysis with a reason.

When a product does not expose an export, a manual copy can be the available source. Record the copy method and its limitations. Do not describe manually copied bytes as a provider-authenticated transcript.

If the model uses tools, preserve the tool requests, results, and errors when permitted. A final answer alone may not show which claims were externally grounded.

## 5. Import the records

Prompts and outputs live in separate collections but share stable references. For each raw output:

1. Copy the available source bytes without normalization.
2. Store raw content without repository front matter.
3. Compute SHA-256 over the stored bytes.
4. Record the repository-relative content path and checksum in metadata.
5. Record the prompt path and any parent artifacts.
6. Distinguish observed facts from user-reported attribution.
7. Set **status: raw** and choose the appropriate claim class.
8. Set review and validation summaries conservatively.
9. List known provenance and content limitations.
10. Check that the raw source and metadata do not expose prohibited material.

The detailed field rules are in the [provenance standard](provenance-standard.md). A checksum verifies later byte consistency only. It does not verify the prompt-output relationship, model identity, creation date, or truth of the content.

## 6. Create derivatives without rewriting the source

Normalization, redaction, annotation, correction, consolidation, and adaptation all create derivative artifacts. A derivative must have:

- a new artifact ID;
- its own content path and checksum;
- **status: curated**;
- the raw source in **parent_artifacts**;
- a modification record stating what changed and why;
- an editor or process identifier when shareable;
- a license statement;
- links to relevant review or evaluation records.

Do not copy a curated version over a raw file. A metadata correction may update the sidecar record, but its basis and date must remain visible in Git history.

## 7. Prepare for evaluation

Extraction and evaluation should be separable. Before calling an artifact useful:

- translate its important rules into testable claims;
- identify tasks where each rule should help;
- identify tasks where it could add cost or cause harm;
- separate requirements dependent on tools from requirements a model can execute unaided;
- define a baseline that omits the transferred artifact;
- preserve enough run and environment detail for repeated trials.

Do not design only examples already solved in the extracted text. That measures recall or prompt leakage, not general transfer.

## Historical import procedure

When only a file and contributor account are available:

1. Preserve the available file bytes.
2. Record the observed filename, size, format, and checksum.
3. Record contributor-reported original filename, prompt, model, target, and dates as reported facts.
4. Set unavailable environment and creation fields to **unknown**.
5. State that the prompt-output pairing and model attribution were not independently verified unless direct evidence exists.
6. Do not backfill plausible provider, mode, tool, or interface values.
7. Write an initial review separately from the source.

Incomplete but candid provenance is more useful than a complete fictional history.

## Extraction completion checklist

- The exact prompt or the limits of its reconstruction are recorded.
- Raw output bytes are separate from metadata and commentary.
- Model and environment fields distinguish observed, reported, and unknown values.
- The run count and exclusions do not conceal unfavorable outputs.
- Tool use, context, attachments, continuation, and truncation are disclosed when known.
- SHA-256 matches the stored content.
- No secrets, private prompts, personal data, confidential context, or unauthorized material are present.
- Every edit or redaction creates a disclosed derivative.
- The artifact is labeled as a hypothesis or operational proposal unless separate evidence justifies another record.

Passing this checklist means the extraction is documented. It does not mean the extracted content is correct or effective.
