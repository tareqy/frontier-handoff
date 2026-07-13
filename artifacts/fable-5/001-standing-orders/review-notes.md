# Initial review: standing orders

> **Document class:** Initial model critique and opinion
> **Claim class:** Hypothesis
> **Reviewer label:** GPT-5.6-SOL, as designated by the repository-initialization task
> **Review date:** 2026-07-13
> **Evidence status:** Not experimentally validated; not human reviewed; not a protocol-complete cross-model review
> **Scope:** The preserved raw artifact, the user-provided prompt, and the context available during repository initialization

## Initial judgment

The artifact is a concrete operational proposal for reducing fluent factual errors, dropped requirements, and unexamined recommendations. Its named triggers, countermeasures, examples, and final gate make several ideas testable. That is a useful starting property, not evidence that the complete instruction set improves another model.

The largest concern is scope. The artifact applies a strict analytical protocol to every task. Several rules are costly, internally tense, dependent on tools, or likely to interfere with casual and creative work. The raw document should remain unchanged; any scoped or tiered alternative should be a new derivative and tested against both the raw version and a no-handoff baseline.

## Clear strengths

- It turns generic cautions into observable actions: verify a premise, enumerate asks, re-run calculations, expose unknowns, and test executable content.
- It identifies recognizable failure modes such as premise echo, invented specifics, unit errors, stale facts, coverage theater, and untested code.
- It asks for uncertainty markers beside the affected claim rather than in a distant caveat.
- It emphasizes source reopening, independent derivation, and live verification for changeable facts.
- It treats completeness as something that can be checked against the original request.
- It requires an objection to name a concrete failure case rather than perform vague “both sides” theater.
- Its examples can seed benchmark cases, provided the cases are rewritten and scored independently rather than treated as proof.

## Possible rigidity

Several absolute rules may create brittle behavior:

- The required `Doing:` line may be useful as a correction point but can be intrusive when the intended deliverable is already clear or when the requested format forbids it.
- The one-question rule assumes an A/B ambiguity. Real requests can have more than two plausible readings or need clarification because the stakes are high, even when a wrong draft would be editable.
- Requiring exactly one primary critical point conflicts with the tie exception and does not fit tasks with several independent catastrophic risks.
- Reserving bare declarative sentences for claims labeled `CERTAIN` may make ordinary prose cluttered and can imply stronger certainty than a single source or tool result supports.
- Fixed answer/reasoning/risks ordering and a hard 25-word sentence limit are stylistic constraints, not demonstrated reliability mechanisms.
- “Three assumptions,” “9-to-1,” and an output of roughly 300 words are unvalidated thresholds.
- Weakest-input confidence inheritance ignores sensitivity. Some conclusions remain stable throughout a broad uncertain input range.

The request that every rule require “zero judgment calls” is not achievable. Terms used by the artifact—including vague, likely, surprising, critical, cheap to catch, and strongest objection—still require contextual judgment.

## Universal rules that may be too expensive

The following operations may be worthwhile in high-stakes work but excessive on every response:

- verify every factual premise before answering;
- independently re-derive each number and date;
- run a fixed multi-question self-attack on every conclusion;
- account mechanically for every constraint;
- apply inline confidence wording to every unverified claim;
- sweep ten fake-competence patterns and then run a ten-item final gate;
- restart the gate from item one after any repair, without a latency or stopping condition.

The cost is not just tokens or time. A long compliance routine can consume attention and context that the task itself needs. This tradeoff requires measurement.

## Risks for casual and creative tasks

For brainstorming, fiction, informal conversation, stylistic editing, or deliberately speculative work, the protocol may:

- turn useful exploration into repeated assumptions and refusals;
- add visible labels and sections the user did not request;
- force a verdict where ambiguity is the point;
- favor adversarial checking over originality or voice;
- over-compress sentences and damage rhythm;
- produce a `Doing:` preamble, reasoning, and risk section when the deliverable alone would be better.

These are hypotheses about interference, not observed failures from a completed experiment.

## Verification and tool access

Some requirements depend on capabilities that are not established in this artifact's provenance. Live current-state checks require browsing or another authoritative source. Code execution requires a compatible runtime and dependencies. Source reopening requires the source to remain in context. Independent verification can require a genuinely independent source rather than a second pass through the same model.

The instruction to run code whenever execution exists lacks a safety gate. Existence of a tool is not permission to execute a destructive command, contact an external service, expose private data, or mutate user state. A derivative should require consent and a safe test environment, and prefer static analysis, dry runs, or isolated tests when execution has side effects.

## Stable knowledge versus session-verified facts

The artifact does not settle how to treat stable background knowledge remembered by a model. One rule demotes unverified current-world claims to `Likely`; another treats source-less specifics as guesses requiring `Unknown`. Applied broadly, the latter can make routine stable facts unusable. Applied narrowly, it needs a stated boundary.

`CERTAIN` is also too strong a name for “checked this session.” Computations can encode a wrong assumption, sources can be mistaken, and tools can return stale data. A more defensible label for a derivative would describe the evidence action—for example, “verified this session against [source]”—without claiming certainty.

## Is one critical point sufficient?

Not always. A deployment command can contain an unsafe deletion, a wrong environment, and a bad rollback instruction; any one may be independently severe. A legal or medical answer can have several actionable facts that a reader cannot cheaply verify. Selecting one focus may improve effort allocation, but imposing a single focus can hide other high-consequence elements.

A better proposal is to identify a small set of critical points, rank them by impact and detectability, and verify all points above a declared risk threshold. Whether that outperforms the original rule remains an experimental question.

The statement that everything outside the critical point receives “single-pass quality” is especially questionable. Once an error is noticed, a policy should not forbid correcting it merely because it is outside the chosen focus.

## Should the final gate have variants?

Yes, as a hypothesis to test rather than a silent rewrite:

- **Light:** confirm intent, coverage, and obvious unsupported specifics; designed for casual, creative, and reversible work.
- **Standard:** add premise checks, calibrated uncertainty, selective verification, and a proportional counterargument for substantive analysis.
- **Strict:** independently verify critical claims, record provenance, test executable content safely, and run adversarial review for high-stakes or irreversible actions.

Activation criteria must include stakes, reversibility, factual volatility, tool availability, and the user's requested mode. The tier itself should be recorded in an experiment.

## Questions requiring experimental validation

1. Does the unchanged artifact improve correctness and completeness over a no-handoff baseline on the same successor model?
2. Does it reduce unsupported specifics, and at what cost in useful answers, latency, tokens, refusals, and verbosity?
3. Which individual rules cause gains or regressions when ablated?
4. Does the one-question policy reduce rebuilds or merely increase confident guessing on multi-way ambiguities?
5. Does single-critical-point allocation outperform a small risk-ranked set?
6. Do confidence labels improve evaluator calibration, or only create the appearance of calibration?
7. How does performance change when browsing, code execution, or source access is unavailable?
8. Does the protocol improve high-stakes analytical work while degrading casual, creative, or exploratory work?
9. Are Light, Standard, and Strict variants better than one universal gate?
10. Do benefits survive model-version drift and repeated stochastic trials?

## Review disposition

Preserve the artifact as a raw operational proposal. Do not promote it to a reviewed recommendation or claim that it transfers capability. The next step should be an experiment design with matched conditions, blind scoring where feasible, repeated trials, and dimension-level results—including negative and inconclusive outcomes.
