# Limitations

> **Document role:** Project limitation statement
> **Claim class:** Operational proposal
> **Review status:** Initial Codex-authored assessment; not human reviewed
> **Experimental status:** No experiment is claimed by this document

Frontier Handoff is an evidence-building project, not evidence that textual handoff works. Its usefulness depends on the quality of future artifacts, provenance, comparisons, and reproductions. The limitations below should constrain repository claims from the start.

## Text transfers explicit material, not model capability

Prompts can carry procedures, heuristics, examples, rubrics, vocabulary, and reminders. They cannot transfer weights, latent representations, private reasoning, training data, hidden system behavior, current knowledge, tool access, or the source model's reliability.

A successor may imitate the form of an instruction without reproducing the capability that made it useful. Conversely, a successor may already perform the procedure without needing the handoff. The project should measure changed behavior, not assume transferred knowledge.

## Model self-analysis is not privileged evidence

A model can produce plausible accounts of its own strengths, weaknesses, or reasoning without access to the facts needed to establish those claims. The same applies to descriptions of successor models. Specificity and confident language can make these reports more persuasive without making them more accurate.

Self-reports are useful for generating hypotheses and test cases. They are not independent capability measurements.

## “Frontier” and model identity may be unverifiable

Temporary or unusual access does not prove that a model is superior, novel, or representative of a stable version. Product display names may map to changing deployments, and interfaces often do not expose exact identifiers. Contributor-reported attributions can be preserved without being authenticated.

Repository language should describe the access context and attribution basis rather than converting an informal name into a verified model identity.

## Provenance can be incomplete

Historical artifacts may lack generation logs, system instructions, timestamps, tool traces, sampling settings, attachments, or exact model identifiers. Manual copying can preserve the available bytes but cannot recreate missing chain of custody.

SHA-256 detects later byte changes. It does not prove authorship, prompt-output causality, date, or truth. **Unknown** metadata is therefore an honest limit, not a defect to hide.

## Raw does not mean original or safe

A raw repository file may already have been reformatted, truncated, filtered, copied, or edited before acquisition. Raw means the repository did not intentionally change the available source bytes. It does not authenticate an upstream original.

Raw outputs may contain fabricated claims, insecure commands, unsafe guidance, bias, personal information, or unauthorized material. Preservation is not endorsement, and security or legal concerns can justify removal.

## Instructions can degrade performance

Long standing instructions can consume context, increase latency and cost, force verbosity, trigger unnecessary clarification or refusal, and make creative or casual work rigid. Universal verification requirements may be impossible without tools. Repeated self-checks can create ceremony without independent evidence.

An instruction can improve one dimension while harming another. Evaluations must measure usefulness, rigidity, verbosity, ambiguity handling, and safety alongside correctness.

## Comparisons have unavoidable confounds

Model performance depends on provider, exact version, product scaffolding, system instructions, tools, context, retrieval, account features, inference settings, rate limits, and time. Hosted aliases can drift during an experiment. Adding a handoff also changes context length and may displace other material.

Matched conditions and disclosure reduce these confounds but may not eliminate them. Results should be limited to the documented environment.

## Output variation requires repeated trials

One output can exaggerate both success and failure. Repeated runs reveal stochastic variation, but finite trials still leave uncertainty. Seeds may be unavailable or may not guarantee identical behavior on hosted systems.

The repository does not prescribe one universal sample size. Experiments must justify their trial count and avoid stronger claims than the data support.

## Evaluation contains judgment

Correctness can sometimes be checked directly, but completeness, usefulness, calibration, rigidity, and verbosity require judgment. Numeric rubrics do not make subjective decisions objective. Human and model evaluators bring preferences, expertise gaps, expectations, and fatigue.

Blind review, multiple evaluators, explicit anchors, and visible disagreement improve inspectability. They do not remove evaluator bias.

## Benchmark selection can manufacture improvement

Cases chosen after reading an artifact may mirror its examples and reward its vocabulary. Repeated tuning against a fixed public suite can overfit the handoff. Selective publication of favorable cases or dimensions can create benchmark theater.

Predeclared criteria, held-out cases, run-level results, and negative-result publication reduce this risk. Public cases may still be contaminated or recognized by future models.

## Reproduction may be approximate

An outside contributor may be unable to access the same model snapshot, interface, account feature, or tool environment. Exact replication can become impossible after a hosted model changes. A conceptual reproduction remains useful when deviations are explicit, but it cannot establish byte-for-byte or environment-identical repeatability.

“Independently reproduced” must identify what was reproduced, by whom, under which deviations, and with what outcome.

## Cross-model review is not independent validation

A second model may identify omissions or counterexamples, but it can share training patterns, evaluator biases, product scaffolding, or the same factual errors. Its review is another generated artifact. Without preserved prompt and environment provenance, even the degree of independence is unclear.

Model agreement is not ground truth, and model disagreement is not proof that either side is correct.

## Results may not generalize

Evidence from one model, language, domain, user population, or task distribution may not transfer to another. High-stakes work may need domain experts and authoritative sources. Creative, interpersonal, accessibility, and multilingual tasks can respond differently to the same standing instructions.

A verified finding must state its tested scope. It should not become a claim about all successor models or all tasks.

## Access and publication create selection bias

Contributors with temporary model access are not a representative sample of users or products. They may retain striking outputs and discard ordinary failures before repository collection begins. Provider availability and cost can determine which models receive more evaluation.

The repository can require disclosure of known selection, but it cannot recover outputs that were never saved.

## Legal, privacy, and security constraints limit transparency

Full reproducibility may conflict with privacy, confidentiality, provider terms, system-prompt restrictions, or intellectual-property rights. Contributors must not publish secrets, personal data, customer material, proprietary source code, private system prompts they lack permission to share, or confidential conversations.

Redaction can be necessary, but it changes the record and may limit interpretation. Artifact-level **license: unknown** does not grant publication permission or override third-party rights.

## Repository process is itself provisional

The metadata vocabulary, validator, rubric, and contribution process are an initial design. Real contributions may reveal missing fields or burdensome requirements. Changes should be versioned and should not invalidate historical raw checksums or silently reinterpret old statuses.

The project should postpone a leaderboard, database, automated model runner, and universal aggregate score until evidence shows they solve a real problem.

## Limitation of the first artifact

The first standing-orders artifact is attributed by the user to Fable 5 and targeted to Claude Opus 4.8. Those relationships are not embedded in the raw bytes. Exact identifiers, provider, interface, mode, tools, original creation date, and generation log are unavailable in the current provenance.

Its rules appear to prioritize verification, decomposition, calibration, adversarial checking, completeness, and direct delivery. That observation is an initial review, not an experimental finding. No completed experiment currently establishes that applying the full instruction set improves a successor model, and its universal requirements may impose substantial cost or rigidity.

## What these limitations require

- Use narrow, conditional language.
- Keep unknown facts unknown.
- Publish raw records and editorial interpretation separately.
- Compare the same successor model with and without the intervention.
- Record product and tool differences.
- Run repeated trials and retain negative or inconclusive outcomes.
- Treat review as critique evidence, not validation.
- Revisit conclusions after model drift or failed reproduction.
- Remove or restrict exposed sensitive material even when preservation would otherwise be desirable.

These practices make evidence easier to inspect. They do not eliminate the limitations.
