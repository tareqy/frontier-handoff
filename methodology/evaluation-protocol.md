# Evaluation protocol

> **Document role:** Experimental protocol
> **Claim class:** Operational proposal
> **Status:** Initial protocol; no repository experiment is implied by this document

## Purpose

Evaluation tests whether a transferred instruction changes downstream model performance under stated conditions. The primary comparison is the same successor model without and with the instruction. An originating model may be an optional reference condition, but it is not ground truth and does not establish that the instruction captures its capability.

An experiment can support, fail to support, or complicate a scoped claim. “Experimentally tested” never means “improved.”

## Unit of evaluation

- A **test case** is a versioned task, input, expected behavior or evidence, and scoring guidance.
- A **condition** is one intervention configuration.
- A **run** is one execution of one case in one condition.
- A **trial** is a repeated run used to observe stochastic variation.
- An **experiment** is the registered collection of cases, conditions, runs, criteria, and analysis.

Store run-level outputs and conditions. An aggregate report without inspectable runs is insufficient for reproduction.

## 1. Register the question before running treatment outputs

Create an experiment record using the repository template. State:

1. the exact artifact and version being tested;
2. the primary hypothesis;
3. the tasks and models to which the claim is limited;
4. the primary outcome dimensions and decision criteria;
5. expected benefits;
6. plausible harms and tradeoffs;
7. cases, conditions, trial count, and stopping rule;
8. exclusion and error-handling rules;
9. scoring and adjudication procedure;
10. planned analysis and known confounds.

Distinguish exploratory from confirmatory work. Exploratory findings are useful for generating hypotheses but must not be described as if their criteria were fixed in advance.

Commit or otherwise timestamp the design before inspecting treatment results when practical. If registration occurs later, label it retrospective.

## 2. Define conditions

The minimum two-arm comparison is:

- **Baseline:** the target model receives the task under the documented normal configuration, without the transferred instructions.
- **Treatment:** the same target model and configuration receive the same task with the transferred instructions.

Optional conditions include:

- the reported originating model as a reference arm;
- Light, Standard, and Strict instruction variants;
- a length-matched neutral or generic instruction control;
- a targeted subset of the handoff to test which component matters.

Each added condition needs a stated purpose. Do not add arms solely to create a favorable comparison.

The originating model is a reference, not an oracle. Its output is scored with the same rubric and may perform worse than either successor condition.

## 3. Match conditions and disclose differences

Hold constant, as far as the product permits:

- exact target-model identifier and snapshot;
- provider, interface, account features, and region;
- system and developer instructions other than the intervention;
- user task and conversation state;
- tools available, permissions, and tool results;
- attachments, retrieval, and external context;
- model mode, reasoning effort, sampling settings, and seed;
- maximum output and context limits;
- run period, especially for changing external facts.

Record every known difference. If exact parity is impossible, narrow the claim.

Transferred instructions consume context and may change latency and cost. That overhead is part of real-world treatment performance and must be reported. A separate mechanism study may use a length-matched control, but neutral padding is itself an intervention and does not erase the limitation.

Never compare product configurations with different tool access and attribute the entire difference to model capability.

## 4. Build test cases

Use the [test-case template](../templates/test-case.md) and the repository's test-case specification. Cases should represent the intended use rather than quote or paraphrase examples from the handoff.

Include, where relevant:

- routine cases where extra procedure may be wasteful;
- difficult cases where the proposed safeguards should matter;
- ambiguous requests with and without a need for clarification;
- false-premise cases;
- tasks containing exact numbers, dates, claims, or executable content;
- tasks where live verification is available and unavailable;
- creative, casual, or interpersonal tasks;
- tasks with several independently critical points;
- tasks where concise delivery matters;
- safety-sensitive tasks that can be evaluated without performing harmful actions.

For each case, define what can be checked objectively, what requires judgment, which ambiguity is intentional, and which answers may all be acceptable. Use external sources or executable checks for correctness when appropriate. Do not treat a model-generated reference answer as unquestionable ground truth.

Keep a held-out set when iterating on instructions. Public cases can become prompt-contaminated or overfit; document when a model may have seen them.

## 5. Score multiple dimensions

Use the [evaluation rubric](../evaluations/rubric.md) and retain dimension-level judgments. At minimum assess:

- correctness;
- completeness;
- unsupported claims;
- calibration;
- instruction following;
- task-specific usefulness;
- excessive rigidity;
- needless verbosity;
- verification quality;
- handling of ambiguity;
- recovery from false premises;
- operational safety.

Define anchors and failure examples before scoring. Prefer direct checks for calculations, code, dates, citations, and factual claims. Subjective dimensions remain judgments even when represented by numbers.

Do not collapse all dimensions into one score unless weights and tradeoffs were declared in advance. Always publish the underlying dimensions. A gain in correctness accompanied by substantial rigidity, refusal, latency, or verbosity is a mixed result unless the registered use case accepts that cost.

## 6. Use repeated and randomized trials

Model outputs vary. Run repeated trials per case and condition unless the interface is deterministic and that fact is established. There is no universal minimum trial count; choose one based on expected variation, cost, and the strength of claim, then report it.

Randomize or counterbalance:

- condition order;
- case order;
- trial order;
- assignment to evaluators.

Avoid running all baselines first and all treatments later, because time, model drift, rate limits, and evaluator learning can become condition effects. Preserve failed requests, timeouts, refusals, and tool errors as outcomes unless a predeclared infrastructure rule excludes them.

## 7. Blind evaluation where feasible

Remove condition names, model names, run order, and irrelevant metadata before scoring. Assign neutral output IDs. Do not tell evaluators which condition the project expects to win.

Blinding may be incomplete because the transferred instructions can produce recognizable wording or structure. Record that risk. Do not rewrite outputs to improve blinding; editing would change the behavior being scored.

For subjective dimensions:

- use more than one evaluator when feasible;
- collect independent scores before discussion;
- record evaluator type and relevant provenance;
- report disagreement rather than averaging it away;
- use a documented adjudicator for material conflicts.

Model-based evaluators can assist with scale but introduce their own preferences, prompt sensitivity, and model drift. Preserve their prompts and outputs, and do not treat their scores as objective measurements.

## 8. Control leakage and false feedback

Do not expose:

- expected answers when the task would not normally include them;
- condition labels;
- owner conclusions;
- private rubric notes that reveal the desired behavior;
- prior outputs from another condition;
- test-case solutions inside the transferred instruction.

If leakage is intentional, such as testing whether a checklist can use supplied reference material, describe that as part of the intervention.

Separate instruction development cases from confirmatory cases. Repeatedly editing the handoff after seeing the same test set turns that set into training material for the project.

## 9. Preserve run evidence

Each run record should include:

- experiment, case, condition, and trial IDs;
- exact task and intervention version;
- model and environment metadata;
- start date and time when available;
- full output and tool trace when permitted;
- completion, truncation, refusal, timeout, and error state;
- token, latency, and cost information when exposed;
- content checksum;
- any redaction or transformation;
- evaluator records and scores linked separately.

Raw run outputs remain unchanged. Cleaned views, score sheets, and aggregate analyses are derivatives with their own provenance.

## 10. Analyze without hiding variation

Report:

- all registered cases and trials;
- missing, failed, and excluded runs with reasons;
- results by case, condition, and rubric dimension;
- paired differences where the same case was run under both conditions;
- distribution or range across trials, not only the best output;
- evaluator agreement and adjudications;
- instruction overhead and operational tradeoffs;
- deviations from the registered plan.

Use uncertainty appropriate to the sample and design. A small collection of subjective scores does not become objective because it has decimal places. Avoid claims of statistical significance without a justified analysis and enough independent observations.

Do not choose only the dimensions or cases on which treatment wins. Preserve negative, mixed, and inconclusive outcomes.

## 11. Assign an outcome conservatively

Use:

- **not-tested** when no qualifying experiment is linked;
- **inconclusive** when the design or evidence cannot distinguish the claim;
- **mixed** when important prespecified outcomes move in different directions;
- **not-supported** when the claim misses its declared criterion;
- **supported** when it meets the declared criterion under recorded conditions.

State the exact scope beside the outcome: artifact version, model identifier, product, tools, task set, date range, and criteria. A single supporting experiment normally produces an **experimental-result** artifact, not a **verified-finding** claim.

Unexpected positive findings are exploratory until tested under a newly fixed plan. A failed reproduction is evidence against generality and must not be hidden by retaining an older “supported” summary without qualification.

## 12. Reproduce independently

A reproduction should:

1. use the published cases, instructions, conditions, and scoring rules;
2. identify a separate reproducer and any relationship to the original work;
3. document model drift and every unavailable setting;
4. preserve new run-level evidence;
5. apply criteria without consulting unpublished original state;
6. report **reproduced**, **not reproduced**, **mixed**, or **inconclusive**;
7. avoid rewriting the original experiment report.

Exact replication may be impossible for hosted models whose snapshots change. In that case the result is a documented conceptual reproduction, and claims must be narrowed accordingly.

## Threats to validity that every report must discuss

- **Evaluator bias:** preferences or expectations affect subjective scores.
- **Order effects:** earlier conditions influence later runs or judgments.
- **Prompt leakage:** treatment, answer, or rubric information reaches a run or evaluator.
- **Model-version drift:** a hosted alias changes during or after the experiment.
- **Tool-access differences:** tools or results differ between conditions.
- **Context-window differences:** the intervention displaces other context or changes truncation.
- **Product scaffolding:** hidden instructions, retrieval, memory, and post-processing differ.
- **Stochastic variation:** one run is not representative.
- **Case selection:** cases favor the handoff or omit likely harms.
- **Public-test contamination:** models or prompt authors may have seen the benchmark.
- **Treatment visibility:** output style reveals the condition to evaluators.
- **Repeated tuning:** the test set influenced instruction revisions.

Naming a threat does not resolve it. State the mitigation used and the remaining effect on interpretation.

## Safety

Do not execute irreversible, dangerous, invasive, or unauthorized actions merely to test an instruction. Use sandboxes, synthetic data, dry runs, fixtures, and expert review. Medical, legal, financial, security, and other high-stakes cases need domain-appropriate sources and safeguards.

An artifact that improves rubric scores while causing unsafe action, disclosure, or unjustified confidence fails the operational-safety dimension.

## Completion checklist

- The design and criteria were fixed or labeled retrospective.
- Baseline and treatment differ only as documented.
- Model, product, tools, context, and version are recorded.
- Cases test intended benefits and plausible degradation.
- Trials are repeated and order is randomized or counterbalanced.
- Scoring is blind where feasible and evaluator bias is disclosed.
- Every run, failure, exclusion, and protocol deviation is retained.
- Dimension-level outcomes and treatment overhead are reported.
- Negative, mixed, and inconclusive results are visible.
- The conclusion is scoped and does not equate testing with improvement.
- Reproduction materials are sufficient for an outside evaluator to attempt the study.

Completing this checklist makes an experiment inspectable. It does not guarantee that its conclusion will generalize.
