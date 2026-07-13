# Terminology

> **Document role:** Normative glossary
> **Claim class:** Operational proposal
> **Status:** Initial terminology; revise through documented review

These definitions prevent evidentiary and product terms from being used as synonyms. They describe how Frontier Handoff uses the terms, not universal industry definitions.

## Records and relationships

**Artifact**
A versioned repository record with a stable ID, content, provenance, and a stated claim class. Prompts, raw outputs, critiques, curated handoffs, test cases, and experiment reports can all be artifacts.

**Artifact ID**
A repository-unique, stable identifier. Renaming a file does not change the ID. A materially revised content record receives a new ID and points to its parent.

**Source artifact**
An earlier record from which another record was produced or about which a claim is made. “Source” describes a relationship; it does not authenticate authorship.

**Parent artifact**
A source record explicitly linked from a derivative, critique, or result. Parent links form provenance, not endorsement.

**Prompt**
The exact model-facing input used or proposed for use. Surrounding system instructions, conversation history, attachments, and tool state are separate context and should be recorded when known and shareable.

**Raw output**
Content stored without intentional alteration after acquisition. Raw means byte-preserved from the available source; it does not mean original, authentic, correct, safe, or unedited before acquisition.

**Curated output**
A new derivative that may normalize, annotate, reorganize, correct, or scope source material. It has its own ID, checksum, edit description, and parent links. It never replaces its raw parent.

**Successor handoff**
Instructions or other explicit material intended to influence a target model after access to a source model ends or changes. It is an operational proposal until evidence supports narrower claims.

**Critique**
A structured assessment of an artifact's claims, omissions, risks, assumptions, or applicability. A critique is review evidence, not an experimental result.

**Failure map**
A structured proposal or evidence-backed record connecting task conditions, observable failure modes, detection signals, and possible mitigations. Each connection retains its own evidence scope.

**Model-routing protocol**
A proposed rule for choosing a model, mode, tool configuration, or escalation path for a task. Routing performance must be tested against alternatives under documented constraints.

## Models and environments

**Source model** or **originating model**
The model reported to have produced an artifact. The display name, exact model identifier, provider, and attribution basis are separate provenance facts.

**Target model** or **successor model**
The model intended to receive or be evaluated with a handoff artifact. “Successor” indicates the planned role, not lesser capability or a verified lineage.

**Model display name**
A human-facing label such as a product or family name. It may be user-reported and may not identify a reproducible build.

**Model identifier**
The most exact provider-issued model, snapshot, deployment, or version string available. Use **unknown** when the interface does not expose it.

**Provider**
The organization or service operating the model endpoint, when known. Do not infer it solely from an informal model alias.

**Interface or product**
The application, API, command-line client, or other product surface through which a run occurred. It can add hidden instructions, retrieval, memory, formatting, or safety behavior.

**Model mode or reasoning effort**
A user-visible setting affecting inference behavior or budget. Record the setting as exposed by the product; do not infer internal reasoning.

**Tools available**
The tools a model could call during a run, not merely the tools it actually called. Actual calls belong in the run record when available.

**Product scaffolding**
System instructions, tools, retrieval, memory, orchestration, post-processing, and interface behavior around a model. Observed product performance is not automatically evidence of the underlying model's isolated capability.

**Frontier model**
A contextual project label for a model believed by a contributor to be unusually capable or newly available. The label is not a verified rank, a stable category, or evidence of superiority.

## Transfer language

**Knowledge transfer**
The project's broad research framing: extracting explicit material from one access context and testing it with another. The phrase does not imply transfer of weights, latent representations, private reasoning, training data, or intrinsic capability.

**Instruction transfer** or **operational-policy transfer**
The more precise description when text carries procedures, heuristics, reminders, rubrics, or routing rules. These terms are preferred in methodological conclusions.

**Model self-report**
A model-generated statement about its own or another model's strengths, weaknesses, reasoning, training, or likely behavior. It is evidence to evaluate, not authority to accept.

## Claim classes

**Hypothesis**
A falsifiable claim or research question for which the artifact does not yet present adequate confirming evidence.

**Operational proposal**
A prompt, procedure, instruction set, rubric, protocol, or recommendation offered for use or testing. This is the default class for generated standing instructions.

**Experimental result**
A record of observations under stated conditions. The class includes positive, negative, mixed, and inconclusive outcomes.

**Reviewed recommendation**
A recommendation whose stated scope incorporates documented review. Review does not imply experimental support.

**Verified finding**
A narrow synthesis supported by traceable evidence, declared criteria, and an explicit scope. It is not a universal truth label and should be rare.

Claim class is not a maturity ladder. New evidence normally creates a linked result or synthesis rather than relabeling immutable raw content.

## Evidence and evaluation

**Review**
Structured inspection of provenance, reasoning, applicability, or risk. Human review and cross-model review are separate evidence dimensions.

**Cross-model review**
A critique produced by a model other than the reported source model, or by a materially different documented model configuration. It is not independent reproduction.

**Validation**
Comparison of a scoped claim against criteria fixed for an experiment. In this repository, **supported** means the claim met those criteria under recorded conditions; it does not mean universally correct.

**Test case**
A versioned task, inputs, expected behavior or reference evidence, scoring guidance, and known ambiguity used in evaluation.

**Condition**
One intervention configuration in an experiment. The usual baseline is the successor model without transferred instructions; the treatment is the same model with them.

**Run**
One execution of one test case in one condition with a recorded environment and output.

**Trial**
A repeated run used to observe stochastic variation. Projects should state when they use “trial” differently.

**Baseline**
The comparison condition without the transferred instruction. It is not assumed to be weak or inferior.

**Treatment**
The condition that adds the handoff artifact. Any other differences must be disclosed as confounds.

**Blind review**
Scoring performed without revealing the condition or other information likely to bias the evaluator. A review is not fully blind if output style or instruction wording reveals the condition; disclose partial blinding.

**Independent reproduction**
A separate evaluator reruns a documented experiment without relying on the original evaluator's unpublished state. Exact duplication may be impossible after model drift, so all deviations must be reported.

**Negative result**
A result that does not meet a prespecified improvement criterion or supports a prespecified null or harm condition. It remains useful evidence.

**Inconclusive result**
A result that cannot distinguish the relevant claims with the available design, data, or reliability. It is not a weak positive result.

**Benchmark theater**
Presentation that creates an appearance of rigor through scores, cases, or rankings while hiding selection, confounds, subjective criteria, failed runs, or weak reproducibility.

## Provenance terms

**Observed**
Directly established in the acquisition environment, such as a filename, byte count, displayed setting, or checksum.

**User-reported**
Supplied by a contributor but not independently established from the stored bytes or interface evidence.

**Inferred**
Derived from other facts. Inferences must be labeled and should not replace a value that is properly **unknown**.

**Unknown**
Material information is unavailable or cannot be established. It is an explicit provenance value, not an invitation to guess.

**Content checksum**
A digest of the stored file's exact bytes. Frontier Handoff uses SHA-256 for raw content. It detects byte changes; it does not prove semantic accuracy or authorship.

**Modification**
An intentional content change, normalization, redaction, annotation, or other transformation. Copying bytes without change is an import operation, not a content modification.

**Relevant commit**
A Git commit that establishes or materially changes a record. The field may be **unknown** during initial import and updated through an auditable metadata commit.

**Prompt leakage**
Exposure of treatment instructions, expected answers, labels, rubric details, or evaluation cases in a way that changes the behavior being measured or biases scoring.

For how these terms interact, see the [artifact lifecycle](artifact-lifecycle.md).
