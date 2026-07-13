# Provenance standard

> **Document role:** Human-readable metadata specification
> **Claim class:** Operational proposal
> **Schema version:** 0.1
> **Status:** Initial standard

## Purpose

Provenance lets a reader distinguish stored bytes, contributor reports, inferences, and unknowns. It supports prompts, model outputs, curated handoffs, critiques, protocols, test cases, experiment runs, reports, and reproductions.

Metadata is evidence about a record, not authentication of every claim in its history. A checksum proves byte consistency after acquisition; it does not prove model identity, authorship, creation date, prompt causality, or factual correctness.

The reusable file is [templates/artifact-metadata.yaml](../templates/artifact-metadata.yaml). This document is authoritative when a template comment is ambiguous.

## General rules

1. Use one globally unique, stable artifact ID for each substantive record.
2. Use repository-root-relative paths with forward slashes and no leading slash or parent traversal.
3. Record exact values only when they were observed or supplied by an identified provenance source.
4. Use the literal scalar **unknown** for a material unavailable fact.
5. Use an empty collection only when “none recorded” is accurate; do not use it to conceal uncertainty.
6. Keep raw content free of front matter. Store metadata beside it.
7. Treat every content normalization, redaction, annotation, or correction as a modification.
8. Give derivatives new IDs and checksums; link their parents.
9. Use ISO 8601 dates or timestamps. Do not invent precision or timezone.
10. Do not include secrets, personal data, unauthorized proprietary material, or private system instructions.

## Required core fields

These fields are required for substantive artifacts in schema version 0.1.

| Field | Type | Requirement |
|---|---|---|
| **schema_version** | string | Use **0.1** for this version. |
| **artifact_id** | string | Repository-unique lowercase identifier using letters, digits, and hyphens. Never reuse it for different content. |
| **title** | string | Neutral descriptive title; do not embed an evidence claim. |
| **description** | string | State what the record contains without endorsing it. |
| **artifact_type** | string | Use a type from the controlled list below or document a necessary extension. |
| **claim_class** | string | One of the five claim classes below. |
| **status** | string | Preservation/editorial state only: raw, curated, superseded, or deprecated. |
| **created_at** | ISO 8601 or unknown | Original creation time. Use unknown when the source does not establish it. |
| **imported_at** | ISO 8601 | Date or timestamp the record entered this repository. |
| **content** | mapping | Repository path, media type, SHA-256, and required byte count. |
| **provenance** | mapping | Acquisition source, modification state, and chain-of-custody facts. |
| **modifications** | mapping | Content-change records keyed by stable modification ID; an unmodified record uses an empty mapping. |
| **review** | mapping | Independent review and reproduction summary fields. |
| **validation_status** | string | not-tested, inconclusive, mixed, not-supported, or supported. |
| **license** | string or unknown | License for this artifact, not merely the repository default. |

Repository policy documents and empty contributor templates do not need their own YAML sidecars. Once a prompt, critique, test case, or result is submitted as evidence, it should receive metadata under this standard.

## Artifact types

Use the narrowest applicable value:

- **extraction-prompt**
- **critique-prompt**
- **evaluation-prompt**
- **raw-model-output**
- **successor-standing-instructions**
- **curated-handoff**
- **human-review**
- **model-critique**
- **model-routing-protocol**
- **failure-map**
- **evaluation-rubric**
- **test-case**
- **experiment-design**
- **experiment-run**
- **experiment-report**
- **reproduction-report**
- **model-comparison**

An extension is acceptable when none fits. Define it in [terminology](../docs/terminology.md) before relying on it across several artifacts. Artifact type does not imply quality or evidence strength.

## Claim class

Every substantive generated artifact uses exactly one:

- **hypothesis**
- **operational-proposal**
- **experimental-result**
- **reviewed-recommendation**
- **verified-finding**

Use **operational-proposal** for an untested prompt, instruction set, rubric, or protocol. Use **experimental-result** for any documented experimental outcome, including negative and inconclusive results. Reserve **verified-finding** for a scoped synthesis with traceable supporting and reproduction evidence.

Do not promote a raw artifact's class in place. New evidence normally creates a linked result or synthesis.

## Status and evidence are separate

**status** answers how content is preserved or editorially treated:

- **raw**
- **curated**
- **superseded**
- **deprecated**

It does not answer whether content was reviewed, tested, supported, or reproduced. Those facts belong under **review**, **validation_status**, linked evidence, and lifecycle events. See the [artifact lifecycle](../docs/artifact-lifecycle.md).

## Model and environment fields

The following top-level fields are conditionally required: include them for model-facing prompts, model outputs, model critiques, and model-run evidence. For those artifact types, an unavailable value is recorded as **unknown** rather than omitted. This preserves the distinction between “not applicable” and “applicable but unavailable.”

| Field | Meaning |
|---|---|
| **source_model** | Reported model display name. This is not an exact identifier. |
| **target_model** | Intended recipient model display name, or unknown when there is no established target. |
| **provider** | Provider actually observed or reported; do not infer it from an alias. |
| **model_identifier** | Exact model, snapshot, or deployment identifier exposed by the provider. |
| **model_mode** | Exposed reasoning effort, inference mode, or similar setting. |
| **interface** | Product, application, API, or command-line surface used. |
| **tools_available** | Tools available to the model, including none, a documented list, or unknown. |
| **attachments_or_context_used** | Non-prompt material supplied to the run, with safe paths or descriptions. |
| **system_instructions** | Shareable system-instruction text or path, unknown, or a concise withheld-with-reason statement. |

When an artifact compares several models or runs, store per-run environment data in the experiment records rather than flattening incompatible values into one field.

**system_instructions** is optional when it is genuinely unrelated and conditionally expected for model-run evidence. Use **unknown** when availability cannot be established. If the instructions are known but cannot be published, use a scalar such as **withheld: private product instructions not authorized for publication** and record the resulting limitation. Private disclosure is never required.

## Content block

The **content** mapping contains:

| Subfield | Requirement |
|---|---|
| **path** | Required repository-root-relative path to the content file. |
| **media_type** | Required media type, such as text/markdown or application/yaml. |
| **sha256** | Required 64-character lowercase SHA-256 digest of exact stored bytes. |
| **byte_count** | Required non-negative exact byte count of the stored content. |

For raw imports, compute the digest after copying into the repository and compare it with the available source digest in the same session when practical. On macOS or Linux:

    shasum -a 256 path/to/file

Do not normalize line endings, trim trailing whitespace, add front matter, or re-encode a raw file before hashing. A checksum mismatch is a provenance incident to investigate, not a value to update automatically.

Content metadata does not create a circular hash because metadata lives outside the content file.

## Relationships

The following fields are optional for unrelated repository records and conditionally required when the relationship exists. A generated model output should normally identify its prompt; a derivative must identify its parents.

| Field | Requirement |
|---|---|
| **prompt_path** | Repository-root-relative exact prompt path, or unknown when no prompt is established. |
| **parent_artifacts** | List of artifact IDs on which this record depends or from which it derives. Empty only when no parent is established. |

A path records a claimed relationship; it does not prove causation. Put the basis for a prompt-output relationship in **provenance.prompt_output_relationship**, such as **directly-observed**, **user-reported**, or **unknown**.

Critiques identify the artifact reviewed as a parent. Experiment runs identify the design, case, condition, and intervention artifacts. Aggregate reports identify all run collections or manifests used.

## Provenance block

The **provenance** mapping must include:

| Subfield | Requirement |
|---|---|
| **source** | How the repository acquired the record: user-provided, direct-generation, repository-import, or a documented alternative. |
| **content_modified** | Boolean. False only when no intentional content transformation occurred after acquisition. |
| **chain_of_custody** | Concise account of what was observed, what was reported, and what remains unauthenticated. |

Include when applicable:

| Subfield | Meaning |
|---|---|
| **original_filename** | Contributor-reported or source-established original name. |
| **observed_import_filename** | Filename actually observed during import. |
| **source_model_attribution** | Basis such as user-reported, interface-observed, provider-log, or unknown. |
| **target_model_attribution** | Basis for the intended target claim. |
| **prompt_output_relationship** | Basis for linking output to prompt. |
| **copy_integrity_verified** | True only when source and stored bytes were compared during import. |
| **source_path_note** | A non-sensitive explanation of source-location discrepancies. |

Do not publish a local path if it exposes personal information or a secret location. A contributor account can establish what was reported while still leaving authorship unauthenticated.

### Provenance basis vocabulary

- **observed** — directly visible in the acquisition environment;
- **user-reported** — supplied by a contributor but not independently verified;
- **provider-log** — supported by a retained provider record;
- **derived** — computed from identified inputs;
- **unknown** — unavailable or not established.

Use a more precise term when needed and define it in the chain-of-custody text.

## Modifications

**modifications** is a required mapping keyed by a stable modification ID. Use an empty mapping, **{}**, for unmodified raw content. Do not use a list: stable keys let later records refer to a particular change without relying on list position.

Each modification record requires:

| Subfield | Requirement |
|---|---|
| **occurred_at** | ISO 8601 date or timestamp; use unknown only for a historical change whose date cannot be established. |
| **actor** | Human, model, or process identifier; use unknown when unavailable or unsafe to disclose. |
| **modification_type** | Short stable type such as normalization, redaction, correction, annotation, reorganization, or other. |
| **description** | Exact account of what content changed. |
| **reason** | Why the change was made. |
| **source** | Parent artifact ID or repository-relative source path. |
| **meaning_changed** | Boolean stating whether the change may alter meaning. |

An illustrative shape is:

    modifications:
      mod-20260713-001:
        occurred_at: "2026-07-13"
        actor: contributor-id
        modification_type: redaction
        description: Removed one credential from the copied context.
        reason: Prevent secret exposure.
        source: source-artifact-id
        meaning_changed: false

Formatting normalization counts as a modification. A new checksum without a modification explanation is not an edit record. A curated or redacted artifact must have at least one modification record, while raw content requires **provenance.content_modified: false** and **modifications: {}**.

Metadata-only corrections are not content modifications. Record them as lifecycle events, as defined below, and retain the correction basis in Git history. They never require rewriting raw content.

## Lifecycle events

**lifecycle_events** is an optional mapping keyed by a stable event ID. Omit it when no event history is recorded, or use an empty mapping. Each event record requires:

| Subfield | Requirement |
|---|---|
| **occurred_at** | ISO 8601 date or timestamp, or unknown for an unavailable historical date. |
| **actor** | Human, model, process, or unknown. |
| **event_type** | Event vocabulary from the [artifact lifecycle](../docs/artifact-lifecycle.md). |
| **description** | Concise, auditable account of the event. |

Append new event IDs rather than reusing or renumbering old ones. A metadata correction uses **event_type: metadata-corrected**. Its description must name the corrected field, old value, new value, and evidence basis. For example: “Field provider changed from unknown to Example Provider; basis: provider run log at linked record.”

## Review block

The **review** mapping requires:

| Subfield | Type | Meaning |
|---|---|---|
| **human_reviewed** | boolean | True only when a qualifying linked human review exists. |
| **reviewers** | list | Reviewer IDs, labels, or review-record paths; empty when none is recorded. |
| **human_review_paths** | list | Repository-relative paths to qualifying human-review metadata records. |
| **cross_model_reviewed** | boolean | True only when a preserved model critique and provenance exist. |
| **review_models** | list | Model-review records or identifiers; empty when none is recorded. |
| **cross_model_review_paths** | list | Repository-relative paths to qualifying model-critique metadata records. |
| **experimentally_validated** | boolean | True only when a scoped claim met declared validation criteria. |
| **evaluation_paths** | list | Repository-relative paths to qualifying experiment-report metadata records. |
| **independently_reproduced** | boolean | True only when a qualifying independent reproduction is linked. |
| **reproduction_paths** | list | Repository-relative paths to qualifying reproduction-report metadata records. |

All four path lists are required. Every item points to the governed artifact's **metadata.yaml**, not its content file. Paths are repository-root-relative, and self-reference is invalid. Qualification is structural:

- **human_review_paths** targets an artifact with **artifact_type: human-review**;
- **cross_model_review_paths** targets an artifact with **artifact_type: model-critique**;
- **evaluation_paths** targets a governed artifact with **artifact_type: experiment-report**;
- **reproduction_paths** targets an artifact with **artifact_type: reproduction-report**.

Every qualifying evidence record must also list the artifact it reviews,
evaluates, or reproduces in its own **parent_artifacts**. The subject record
points to the evidence metadata through the appropriate review path, and the
evidence record points back to the subject as a parent. This bidirectional link
is required by repository validation; a correctly typed but unrelated record
does not qualify as evidence for the subject.

A positive boolean requires at least one qualifying path in its corresponding list. **human_reviewed: false** requires an empty **human_review_paths** list, and **cross_model_reviewed: false** requires an empty **cross_model_review_paths** list.

For an ordinary artifact, **validation_status: not-tested** requires an empty **evaluation_paths** list, and every other validation status requires at least one qualifying experiment-report path. A record does not qualify merely because it has **claim_class: experimental-result**, and an individual **experiment-run** is not an evaluation report.

There is one narrow recursion exemption. Governed records with **artifact_type: experiment-run**, **experiment-report**, or **reproduction-report** may state their own completed **validation_status** without linking another experiment report in **evaluation_paths**. Their own content and parent records are the evidence later consumers evaluate. The exemption prevents an infinite chain of reports citing reports; it does not let other artifact types bypass a qualifying experiment report.

**experimentally_validated: true** additionally requires **validation_status: supported**; false can coexist with evaluation paths for inconclusive, mixed, or not-supported results.

**independently_reproduced: true** requires at least one qualifying reproduction path. False can coexist with reproduction paths so failed, mixed, or inconclusive reproduction evidence remains linked rather than hidden.

A false boolean means positive evidence is not recorded. It does not by itself prove rejection, a failed attempt, or no attempt. Read the linked governed records and lifecycle history for the outcome.

An initial model opinion may be mentioned in nonqualifying descriptive metadata without setting **cross_model_reviewed** true or populating **cross_model_review_paths** when the critique prompt, reviewer environment, or protocol is incomplete. Do not place experimental status under a reviewer prediction.

## Validation status

Use one:

- **not-tested**
- **inconclusive**
- **mixed**
- **not-supported**
- **supported**

The value summarizes the artifact's current scoped experimental evidence, not whether someone executed a run. **supported** requires linked criteria and results. **not-supported** is not the same as unsafe or useless outside the tested scope. A changed result should preserve earlier reports and explain the new evidence.

**effect_direction** is an optional report-level field, not a substitute for **validation_status**. When present, use exactly:

- **beneficial**
- **harmful**
- **mixed**
- **no-detectable-effect**
- **inconclusive**

Validation status describes support for a preregistered claim; effect direction describes the observed operational direction. A supported harm hypothesis can therefore have **validation_status: supported** and **effect_direction: harmful**. Multi-metric reports should record direction at the claim or metric level when one top-level direction would conceal tradeoffs.

## Reviewer and review-model provenance

Detailed reviews should be artifacts of their own. Their metadata records:

- reviewer type and identifier when safe;
- date and scope;
- reviewed artifact IDs;
- review protocol version;
- conflicts or relationship to the contributor;
- whether source identity, condition labels, prior reviews, or expected conclusions were visible;
- for a model reviewer, all available model and environment fields;
- exact critique prompt and raw output paths;
- modifications and limitations.

Do not force a human reviewer to publish personal data. A stable pseudonym plus conflict disclosure can be sufficient.

## Known limitations

**known_limitations** is optional only when no material limitation is known. When used, it is a list of concrete gaps affecting authenticity, interpretation, comparison, or reuse. Examples include unknown exact model identifier, missing generation log, user-reported attribution, redacted context, unavailable tool trace, incomplete review, or model drift.

Do not put generic disclaimers here to make the list look complete. Record artifact-specific limitations.

## License

**license** records the license or rights status of the individual artifact. The repository's MIT license does not silently establish rights over imported model outputs, third-party text, attachments, or provider exports.

Use **unknown** when rights were not established in the available provenance. Contributors must still have permission to submit the material; **unknown** is not permission to publish copyrighted, confidential, or proprietary content.

## Relevant commit

**relevant_commit** is optional. It identifies a Git commit that establishes or materially updates the record. It may be **unknown** during initialization. Updating it creates a later commit, so it should be treated as a traceability pointer, not a self-authenticating seal.

## Prompt-specific records

A submitted prompt should preserve exact model-facing wording in a marked block or raw content file. Record:

- prompt artifact ID and type;
- intended source and target roles;
- version and parents;
- environment assumptions;
- attachments or context;
- whether it was actually run;
- outputs linked as child artifacts.

A prompt that has never run is an operational proposal, not an experimental result.

## Critiques and evaluations

A critique is a separate artifact whose parents include the reviewed record. It records the reviewer and, for model critiques, the exact prompt, model environment, raw output, and edits.

An experiment design links intervention and test-case artifacts. A run records the exact condition and output. An experiment report links all included runs, exclusions, scoring records, deviations, and analysis. A reproduction report links the original experiment, its own run records, and the new environment and deviations.

Experiment and reproduction reports should identify their run artifacts in **parent_artifacts**. Schema version 0.1 validates direct structural references but does not prove that a report includes every run it claims to summarize or that every transitive parent is complete. Transitive run completeness is a review-level check in this version.

Do not summarize several runs into a model-comparison artifact without retaining the run-level evidence.

## Validation

Repository validation should check at least:

- YAML syntax;
- required fields and allowed enumerations;
- unique artifact IDs;
- repository-relative referenced paths;
- content file existence;
- SHA-256 consistency;
- required **content.byte_count** and **provenance.chain_of_custody**;
- raw **content_modified: false** and **modifications: {}**;
- required review evidence lists and qualifying governed-artifact links;
- positive review booleans and non-**not-tested** validation states against those structural links;
- modification and lifecycle-event record shape;
- allowed validation-status and effect-direction vocabulary.

Automated validation checks structural links, not the truth of a review, independence of a reviewer or reproducer, authorship, publication rights, or experimental quality. A qualifying path proves that a structurally compatible governed record exists; it does not prove that its claims are sound.

### Governed metadata YAML profile

The repository-owned validator intentionally accepts a conservative YAML subset for governed **metadata.yaml** files:

- two-space indentation;
- simple-key mappings;
- scalar lists;
- conservative scalar values;
- empty collections;
- literal or folded block strings.

It rejects tabs, duplicate keys, anchors, aliases, tags, merge keys, nonempty flow collections, and sequences of mappings. Use nested mappings keyed by stable IDs for structured modification and lifecycle records.

This profile does not apply to arbitrary YAML in GitHub configuration, workflows, issue forms, or other external formats. Those files follow the syntax required by their platform.

## Minimum import checklist

- Required core fields are present.
- Artifact type, claim class, and status are not being used as praise.
- Unknown model and environment facts remain unknown.
- Attribution basis and prompt-output relationship are explicit.
- Content path, byte count, and SHA-256 match the stored file.
- Chain of custody states what is observed, reported, and unauthenticated.
- Raw content has no repository front matter or undisclosed edits.
- Parent and prompt paths resolve.
- Review and validation summaries have the required empty or qualifying governed-artifact path lists.
- Known limitations name the material gaps.
- License and publication authority are not overstated.
- Sensitive or unauthorized material is absent.
