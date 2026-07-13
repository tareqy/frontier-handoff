# GPT-5.6-SOL initial assessment

> **Document class:** Model opinion
> **Author label:** GPT-5.6-SOL, as designated by the repository-initialization task
> **Claim class:** Hypothesis
> **Evidence status:** Not experimentally validated
> **Independence:** Not a statement from OpenAI
> **Context limitation:** Dependent on the prompt, artifact, repository request, and files available in this session on 2026-07-13

## Bottom line

“Knowledge transfer” is a defensible shorthand only if the project means transferring explicit text artifacts and testing their behavioral effects. It is misleading if it implies that prose can transfer model weights, latent skills, private reasoning, world knowledge, or underlying capability. For experiments, I would use the narrower phrase **instruction transfer** or **operational-policy transfer** and reserve “knowledge transfer” for the project-level research question.

The first artifact is worth preserving because it makes concrete, falsifiable proposals about model behavior. It should not be installed as universal successor instructions merely because its reported source was considered unusually capable. The artifact is an intervention candidate. Its value depends on comparative results.

## What can realistically transfer through text

Text can carry explicit, inspectable material such as:

- task-decomposition procedures;
- checklists and stopping conditions;
- tool-use and verification policies;
- known failure patterns and proposed countermeasures;
- user preferences and delivery conventions;
- domain terminology and documented constraints;
- worked examples, counterexamples, and test cases;
- prompts that elicit a particular workflow;
- records of past failures, including negative results.

Transfer is more plausible when the successor already has the capability to execute the instruction, the instruction is compatible with its hierarchy and tools, and the task supplies enough context. Text may redirect attention or make a latent behavior more reliable. That is still a behavioral effect to measure, not evidence that capability moved from one model to another.

## What text cannot reliably transfer

A handoff document cannot copy:

- learned weights or latent representations;
- the originating model's actual internal computation;
- private chain-of-thought or a faithful causal account of how an answer was produced;
- unavailable training data or current-world knowledge;
- context-window capacity, reasoning budget, latency profile, or sampling behavior;
- product scaffolding, memory, permissions, browsing, code execution, or other tools;
- reliable self-knowledge about either model's strengths and weaknesses;
- tacit skill that the successor cannot implement from instructions.

Even a detailed procedure can fail because the successor interprets it differently, follows it inconsistently, or spends limited context and attention on the checklist rather than the task.

## The central category error

Generated instructions can sound like compressed expertise while being generic, internally inconsistent, or optimized for persuasiveness. A model's ability to describe a good workflow is not the same as its ability to follow that workflow, and the successor's compliance is not the same as improved task performance.

The prestige attached to a model name makes this error more likely. Attribution can establish who reportedly produced a proposal; it cannot validate the proposal. The first artifact's source and target names are user-reported, and its raw bytes do not name either model. No exact identifiers, run log, provider, interface, reasoning mode, or tool configuration are available.

## Can successor instructions improve performance?

Yes, plausibly and conditionally. A successor may benefit when instructions:

- direct attention to a failure it otherwise makes often;
- require a check that is cheap, available, and diagnostic;
- prevent dropped constraints on multipart tasks;
- encourage source use for volatile or consequential facts;
- give a useful response structure without fighting the requested format;
- provide domain-specific examples that transfer to the tested cases.

The likely mechanism is scaffolding: the text changes what the model attends to or which available behavior it selects. The repository has not yet measured such an effect.

## How instructions can degrade performance

The same intervention can hurt by:

- consuming context and computation with universal ceremony;
- increasing latency, tokens, refusals, caveats, and visible uncertainty markers;
- causing instruction interference with task-specific formats or higher-priority policies;
- replacing adaptive judgment with brittle thresholds;
- making a model over-check easy details while losing the task's main thread;
- suppressing exploration, creativity, voice, and conversational naturalness;
- encouraging performative verification without an independent source;
- prompting unsafe tool execution when a rule says to run code but omits consent and side-effect checks;
- reducing useful answers when tools are unavailable;
- overfitting to benchmark patterns exposed by the instructions.

An intervention can improve unsupported-claim counts while making answers less useful. A single aggregate score would conceal that tradeoff.

## What the first artifact appears to optimize for

The artifact attributed to Fable 5 appears designed to reduce:

- fluent answers to false or misread premises;
- unverified numbers, dates, names, and current-state claims;
- confidence flattening between evidence and assumption;
- first-idea lock-in;
- omitted parts of multipart requests;
- invented specifics and untested executable content;
- recommendations buried beneath generic reasoning.

Its strongest design choice is operational specificity. Rules have identifiers, triggers, actions, examples, and named failures. That makes them easier to turn into benchmark hypotheses than ordinary advice such as “be careful.”

## What it may overconstrain

The artifact treats one protocol as appropriate for every task. I disagree with that design choice.

The `Doing:` preamble, exact uncertainty vocabulary, bare-declarative restriction, one-question A/B rule, single-primary-critical-point rule, fixed delivery order, 25-word sentence cap, mandatory hostile objection, and recursive final gate are not obviously universal. Several numerical thresholds are asserted without evidence. The rule that noncritical content receives only a single pass is especially hard to defend if a later pass reveals a real error.

The verification policy also needs a safety boundary. Having an execution tool does not authorize running destructive code, contacting third parties, exposing data, or changing external state. Tool availability, permission, isolation, and reversibility are separate questions.

The confidence scheme blurs **certainty** with **checked once this session**. Tools and sources can fail. Stable background knowledge and volatile session-verified facts also need distinct treatment. Otherwise, the rules risk alternating between unearned certainty and unusable caution.

## How to test the difference

The core comparison should use the same successor-model identifier under matched conditions:

1. no transferred instructions beyond the experiment's common harness;
2. the unchanged standing-orders artifact;
3. any revised or tiered variant as a separately identified treatment.

The originating model can be an optional reference arm, not ground truth. Task text, context, tools, interface, settings, and scoring criteria should be fixed before outputs are judged. Randomize condition order, blind evaluators where feasible, repeat stochastic trials, and retain run-level outputs. Report model-version drift, tool failures, exclusions, and prompt leakage.

Measure dimensions separately: correctness, completeness, unsupported claims, calibration, instruction following, usefulness, rigidity, verbosity, verification quality, ambiguity handling, false-premise recovery, safety, latency, and token cost. Subjective ratings should include evaluator instructions and disagreement rather than being presented as objective measurements.

## The next three experiments

### 1. Full-treatment crossover across task classes

Compare no handoff with the unchanged artifact on factual analysis, coding, ambiguous requests, high-stakes simulations, casual conversation, and creative work. Use matched tools, randomized order, blind review, and repeated trials. This establishes whether benefits exist and whether they reverse by task class.

### 2. Rule-family ablation

Test verification, uncertainty labeling, self-attack, completeness, delivery, and the final gate separately and in combinations. Record quality, latency, tokens, refusals, and evaluator preference. This can distinguish useful mechanisms from ceremonial overhead and identify harmful interactions.

### 3. Proportional Light/Standard/Strict routing

Compare the universal artifact with a documented router that selects Light, Standard, or Strict checks based on stakes, reversibility, factual volatility, and tool availability. Include deliberately wrong routing cases. This tests both the proposed tiers and whether routing error erases their benefit.

## What I would do differently

If I owned the project, I would treat each instruction set as an experimental treatment, not a constitution for successor models. I would:

- preserve the raw artifact exactly, while refusing to equate preservation with endorsement;
- decompose the monolith into independently testable rule families;
- add explicit activation conditions, safety gates, and conflict priority to derivatives;
- design benchmark cases before reading treatment outputs where possible;
- run the successor baseline first and publish negative or mixed findings;
- emphasize within-model comparisons over prestige comparisons between model names;
- keep integrity, review, testing, outcome, and reproduction as separate metadata dimensions;
- postpone leaderboards and universal scores until the repository has enough real runs to justify them.

My strongest criticism is that the project will become low-value if it collects eloquent handoff documents faster than it falsifies them. The scarce resource is not generated advice. It is well-controlled evidence about when that advice helps, when it hurts, and what it costs.

## Related records

- [Preserved raw artifact](../artifacts/fable-5/001-standing-orders/raw.md)
- [Initial review notes](../artifacts/fable-5/001-standing-orders/review-notes.md)
- [User-provided originating prompt](../prompts/fable-5/001-standing-orders/prompt.md)
