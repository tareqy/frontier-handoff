# Review protocol

> **Document role:** Review protocol
> **Claim class:** Operational proposal
> **Status:** Initial protocol; not experimentally validated

## Purpose

Review identifies provenance gaps, reasoning weaknesses, applicability limits, risks, and testable questions. It does not convert model-generated content into fact. Human review and cross-model review are independent dimensions, and neither substitutes for an experiment.

A review may be preliminary, scoped, or comprehensive. Its title and metadata must say which. “Reviewed” means only that a qualifying review record exists.

## Review types

**Provenance review** checks acquisition, attribution, paths, checksums, modification history, and missing environment data.

**Content review** examines claims, internal consistency, actionability, assumptions, and likely failure cases.

**Safety and privacy review** examines operational hazards, sensitive content, unauthorized material, and misuse risks.

**Cross-model review** uses a separately documented model to critique an artifact. It remains model-generated evidence.

**Evaluation review** examines an experiment's design, data, analysis, and interpretation. Use the [evaluation protocol](evaluation-protocol.md) in addition to this document.

A single review can cover several types if its scope is explicit.

## Reviewer record

Each review should record:

- review artifact ID and date;
- artifact IDs and versions reviewed;
- reviewer name, pseudonym, or **unknown**, as appropriate;
- reviewer type: human, model, or mixed;
- for a model reviewer: display name, exact identifier, provider, interface, mode, tools, prompt, and context when known;
- review scope and protocol version;
- whether the reviewer saw provenance, treatment labels, prior reviews, expected results, or owner conclusions;
- relevant expertise or limitations when voluntarily disclosed;
- conflicts of interest or contributor relationship;
- edits made to the review output.

Do not require personal data, private credentials, proprietary system prompts, or identity disclosure beyond what is necessary and safe.

## Prerequisites

Before substantive review:

1. Open the exact content path in metadata.
2. Recompute the content SHA-256 and compare it with metadata.
3. Open the linked prompt and parent artifacts.
4. Note missing or inaccessible records.
5. Confirm whether the reviewed file is raw or curated.
6. State whether the review is blind to source identity or evaluation condition.

If the checksum fails, stop the content review until the mismatch is explained. Record the mismatch; do not silently update the checksum.

## Review procedure

### 1. Inventory the claims

Separate:

- factual claims that can be externally checked;
- model self-reports;
- operational rules and recommendations;
- examples;
- implied universal claims;
- stated assumptions and unknowns.

Assign or confirm the artifact claim class. Do not treat an example as evidence merely because it illustrates the proposed rule.

### 2. Audit provenance

Check that:

- model display name is not presented as an exact identifier;
- user-reported attribution is labeled;
- dates, provider, interface, mode, tools, context, and attachments are either supported, **unknown**, or legitimately omitted;
- the prompt-output relationship has an identified basis;
- edits, redactions, normalization, and continuation boundaries are disclosed;
- the license and publication authority are not overstated.

List material gaps and explain how each limits interpretation.

### 3. Test internal coherence

Look for conflicting rules, undefined terms, impossible prerequisites, circular checks, and procedures whose completion cannot be observed. Confirm that triggers and actions can be distinguished. Check whether examples actually demonstrate the claimed prevention rather than merely restating it.

For numerical, legal, medical, security, or executable claims, require an appropriate source or test. A review must not manufacture verification from plausibility.

### 4. Challenge scope and assumptions

For each material proposal, ask:

1. Which task types should benefit?
2. Which task types could degrade?
3. What tool, context, latency, or user-interaction assumptions does it require?
4. Does it confuse stable knowledge with facts that must be verified in the current session?
5. Is the rule universal, or should it be conditional?
6. What is the smallest counterexample?
7. What result would cause the reviewer to withdraw the recommendation?

Pay particular attention to high-stakes analytical rules applied to casual, creative, interpersonal, or latency-sensitive tasks.

### 5. Assess operating costs and failure modes

Inspect for:

- excessive rigidity or refusal;
- needless verbosity or forced labeling;
- repeated work with little error reduction;
- context-window consumption;
- latency and tool-call cost;
- inability to comply when live tools are unavailable;
- instructions that conflict with a user's higher-priority request;
- false confidence created by procedural ceremony;
- a final checklist too strict or long for routine use;
- a single “critical point” rule that ignores several tied risks.

When appropriate, propose scoped variants such as Light, Standard, and Strict. Treat the variants as new operational proposals requiring comparison, not as fixes proven by review.

### 6. Attack the strongest conclusion

Write the most consequential conclusion in one sentence. Identify a concrete input, task, or environment that would make it false. Then choose one disposition:

- **unsupported** — evidence or reasoning does not justify the conclusion;
- **conditional** — retain it only within a named boundary;
- **plausible but unverified** — retain it as a hypothesis or operational proposal;
- **supported by cited review evidence** — retain it as a reviewed recommendation, with scope;
- **requires experiment** — identify the comparison that could resolve it.

Do not use “no concerns” without describing what was checked.

### 7. Record findings

Each material finding should contain:

- a short name;
- the exact section or claim addressed;
- the observation;
- supporting source or reasoning;
- severity: critical, major, minor, or question;
- confidence and what could change it;
- proposed action;
- evidence needed for resolution.

Severity describes consequence, not certainty. A high-confidence minor typo is not a critical finding; a potentially severe but uncertain safety issue should state both facts.

### 8. Separate review from experiment design

End with questions that require empirical validation. For each question, suggest:

- a baseline and treatment;
- task classes likely to expose the effect;
- intended outcome and likely tradeoff measures;
- a failure or harm criterion.

Do not claim the proposed experiment has run. Register it separately before collecting treatment outputs.

## Cross-model review requirements

Preserve the exact critique prompt and raw model output. Record whether the reviewer model saw:

- the source model name;
- claims that the source was “stronger” or temporary;
- prior human conclusions;
- expected weaknesses;
- the evaluation rubric or condition labels.

These details can anchor the critique. When practical, request independent issue identification before revealing prior review notes, then compare overlap and disagreement.

A cross-model critique of a model self-report is not independent evidence about either model's capability. It is a source of hypotheses, missed cases, and proposed tests.

## Disagreement, correction, and appeal

Do not resolve disagreement by overwriting an earlier review. Add a response or counter-review that links the contested record and identifies:

- the exact disputed statement;
- whether the dispute concerns fact, interpretation, scope, or value judgment;
- new evidence, if any;
- the requested metadata correction or conclusion change.

Correct objective metadata through an auditable commit without changing raw content. A disputed attribution remains user-reported until better evidence is recorded. If reviewers reach different conclusions, preserve both and summarize the conditions that drive the difference.

## Updating evidence fields

- Set **human_reviewed** to true only when a linked human review meets this protocol's minimum reviewer, scope, and findings requirements.
- Set **cross_model_reviewed** to true only when the critique prompt, output, and reviewer-model provenance are retained.
- Do not change **validation_status** based on review alone.
- Do not set **experimentally_validated** or **independently_reproduced** based on a reviewer's prediction.
- A raw artifact remains **status: raw** after review.

## Minimum review checklist

- Content and checksum match the metadata.
- Review scope, reviewer type, date, and access to prior conclusions are disclosed.
- Factual claims, model self-reports, proposals, and examples are separated.
- Provenance gaps and modification history are assessed.
- At least one concrete counterexample or boundary is considered.
- Tool dependence, cost, rigidity, and task degradation are considered.
- Findings distinguish consequence from confidence.
- Disagreement and unknowns remain visible.
- Empirical questions are labeled as unrun proposals.
- The raw artifact was not edited.

Completing this checklist records scrutiny. It does not establish correctness, effectiveness, or safety.
