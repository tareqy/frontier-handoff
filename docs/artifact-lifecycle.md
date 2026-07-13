# Artifact lifecycle

> **Document role:** Repository policy
> **Claim class:** Operational proposal
> **Status:** Initial policy; not experimentally validated

Artifact maturity is not a single ladder. Preservation state, review evidence, experimental evidence, reproduction, and editorial disposition can change independently. A linear label such as “mature” would conceal important differences: a carefully preserved raw output may be untested, while a tested proposal may have an inconclusive result.

This repository therefore records a small handling status, independent evidence fields, linked governed records, and append-only events.

## The dimensions

### Handling status

The top-level **status** field describes preservation or editorial handling only:

- **raw** — stored as received, with no intentional content edits;
- **curated** — a derivative whose edits are disclosed and whose parent is retained;
- **superseded** — retained for history but replaced by a named later artifact;
- **deprecated** — retained but discouraged because of evidence, safety, relevance, or maintenance concerns.

An artifact proposal is a contribution-stage record, normally an issue or draft, rather than a raw artifact status. Once generated or imported, the committed record receives the appropriate handling status.

Raw does not mean authentic, accurate, safe, reviewed, or endorsed. Curated does not mean validated. Superseded and deprecated artifacts retain their earlier evidence records.

### Claim class

Every substantive generated artifact receives one of the following classes:

- **hypothesis** — a falsifiable claim or question awaiting evidence;
- **operational-proposal** — instructions, a prompt, protocol, rubric, or recommended procedure offered for testing;
- **experimental-result** — observations from a documented evaluation, regardless of outcome;
- **reviewed-recommendation** — a recommendation that incorporates identified review evidence but is not necessarily experimentally supported;
- **verified-finding** — a narrowly scoped synthesis supported by adequate traceable evidence and explicit criteria.

These classes describe what a record claims to be. They are not prestige levels. A raw operational proposal does not become a verified finding merely because an experiment supported part of it. The experiment is a separate result artifact; any later synthesis must state its scope and link both records.

### Review evidence

Human and cross-model reviews are recorded separately. The required **review.human_review_paths** and **review.cross_model_review_paths** lists point to governed **metadata.yaml** records, not directly to prose content. A human-review path qualifies only when its target has **artifact_type: human-review**; a cross-model path qualifies only for **artifact_type: model-critique**.

**human_reviewed: true** and **cross_model_reviewed: true** each require at least one qualifying path. A false value keeps the corresponding list empty and means there is no recorded qualifying review. It does not mean a reviewer rejected the artifact.

Cross-model review is critique evidence, not independent experimental confirmation. A review produced by another model remains a model-generated artifact with its own provenance.

The validator checks target artifact type and path structure. It cannot establish reviewer competence, independence, honesty, or correctness.

### Experimental evidence

The **validation_status** field summarizes the current outcome for the artifact's scoped claims:

- **not-tested** — no qualifying experiment is linked;
- **inconclusive** — evidence does not distinguish the conditions sufficiently;
- **mixed** — prespecified dimensions or cases move in materially different directions;
- **not-supported** — the tested claim missed its declared criterion under the recorded conditions;
- **supported** — the tested claim met its declared criterion under the recorded conditions.

“Experimentally tested” is an event, not an outcome. A negative result is still a completed test. **Supported** never means universally true, and it must link to run-level evidence.

The required **review.evaluation_paths** list points only to governed metadata with **artifact_type: experiment-report**. A lone **experiment-run** and an arbitrary record labeled **claim_class: experimental-result** do not qualify. For ordinary artifacts, **not-tested** requires an empty list and every other validation status requires at least one qualifying experiment-report path.

All qualifying human-review, model-critique, experiment-report, and
reproduction-report records must name the artifact they assess in their own
**parent_artifacts**. The assessed artifact points to the evidence metadata in
its review block. Validation requires both directions so an unrelated report
cannot be attached as evidence merely because its type matches.

A narrow recursion exemption applies to governed **experiment-run**, **experiment-report**, and **reproduction-report** records. They may state the outcome of their own completed evidence without linking another experiment report in **evaluation_paths**. Their content and parents are the evidence consumed by a later report or artifact. Other artifact types cannot use this exemption.

The compatibility field **review.experimentally_validated** is conservative: set it to true only when a scoped claim met declared validation criteria, **validation_status** is **supported**, and a qualifying evaluation path is present. It must not be used to mean merely “an experiment ran.” A false value can coexist with qualifying evaluation paths for **inconclusive**, **mixed**, or **not-supported** results.

Reports may separately record observed **effect_direction** as **beneficial**, **harmful**, **mixed**, **no-detectable-effect**, or **inconclusive**. Validation status asks whether a declared claim was supported; effect direction asks how the intervention moved outcomes. A supported claim can describe a harmful effect.

### Reproduction evidence

Independent reproduction asks whether a separate evaluator can obtain a compatible result from documented materials. Record the reproducer, environment, deviations, trial data, and outcome. The required **review.reproduction_paths** list points to governed records with **artifact_type: reproduction-report**.

**review.independently_reproduced: true** requires at least one qualifying reproduction path. A false value means only that positive independent reproduction is not recorded. The list may still contain failed, mixed, or inconclusive reproduction records so negative evidence remains visible. The recursion exemption does not broaden **reproduction_paths**: its entries still target governed **reproduction-report** metadata.

Experiment and reproduction reports should list their run artifacts as parents. In schema version 0.1, validation checks direct structural links but does not establish that every summarized run is transitively present. Transitive run completeness remains a review-level judgment.

## Lifecycle events

Events preserve chronology without pretending that all artifacts follow the same path. The optional **lifecycle_events** field is a mapping keyed by stable event ID; it is not a positional list. Each event requires:

- **occurred_at** — ISO 8601 date or timestamp, or **unknown** for an unavailable historical date;
- **actor** — human, model, process, or **unknown**;
- **event_type** — one of the event types below;
- **description** — a concise, auditable account.

Append a new stable event ID rather than rewriting or renumbering an existing event.

The core event types are:

1. **proposed** — a contributor defines the intended artifact, scope, and collection plan;
2. **generated** — a model or process produces content;
3. **imported-raw** — source bytes enter the repository and receive a checksum;
4. **human-reviewed** — a human review record is linked;
5. **cross-model-reviewed** — a model critique record is linked;
6. **experiment-designed** — cases, hypotheses, criteria, and analysis plan are fixed;
7. **experimentally-tested** — documented runs are completed, including negative or inconclusive outcomes;
8. **independently-reproduced** — an independent report records its reproduction outcome;
9. **revised** — a derivative artifact is created; the source remains unchanged;
10. **superseded** — a named replacement becomes preferred;
11. **deprecated** — use is discouraged with a recorded reason;
12. **metadata-corrected** — a sidecar fact changes without changing artifact content.

Do not create an event merely to make a record look complete. If the generation date or actor is unavailable, preserve **unknown** rather than reconstructing a plausible history.

For **metadata-corrected**, the description must state the field name, old value, new value, and evidence basis. The event records the correction; it must not be used to hide a raw content change.

## Common paths

The following examples are illustrative, not mandatory workflows:

- A historical output may enter at **imported-raw**, receive human and model reviews, and never be experimentally tested.
- A new extraction prompt may be **proposed**, **generated**, imported with several outputs, then tested. Some outputs may remain raw while a separate curated handoff is created.
- A tested instruction may receive **not-supported** or **mixed** validation status and later be deprecated.
- A result may be independently reproduced while its source proposal remains raw.

## Revisions, corrections, and removal

Never revise a raw artifact in place. Create a new artifact with:

- a new artifact ID and content checksum;
- the source artifact in **parent_artifacts**;
- **status: curated**;
- a **modifications** mapping keyed by stable modification ID;
- a link from the earlier record when it is superseded.

Each modification record requires **occurred_at**, **actor**, **modification_type**, **description**, **reason**, **source**, and **meaning_changed**. An unmodified raw artifact uses **modifications: {}** and **provenance.content_modified: false**.

Correcting metadata does not require changing raw content, but the correction should be visible in Git history and described as a **metadata-corrected** lifecycle event. Its description states field, old value, new value, and basis. Changing an attribution from one unverified claim to another must identify the source of the correction.

Removal is exceptional. Security, privacy, legal, or consent concerns may require deleting exposed material from the current tree and possibly Git history. Record a non-sensitive tombstone or security note when doing so would not repeat the exposure.

## Minimum evidence for public labels

| Label | Minimum record |
|---|---|
| Raw | Stored bytes, byte count, SHA-256 checksum, chain of custody, **modifications: {}** |
| Human reviewed | **human_reviewed: true** plus a qualifying human-review metadata path |
| Cross-model reviewed | **cross_model_reviewed: true** plus a qualifying model-critique metadata path |
| Experimentally tested | Non-**not-tested** status plus a qualifying evaluation metadata path |
| Independently reproduced | **independently_reproduced: true** plus a qualifying reproduction-report metadata path |
| Superseded | Named replacement and reason |
| Deprecated | Reason, date, and safer or current alternative when one exists |

See the [provenance standard](../methodology/provenance-standard.md) for field requirements and the [review protocol](../methodology/review-protocol.md) for what counts as a review.

Repository validation confirms field shape, path existence, and compatible linked artifact types or claim classes. It does not verify the truth of linked content, the independence of a reviewer or reproducer, or the quality of an experiment.
