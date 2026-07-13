# Test-case specification

> **Status:** Initial human-readable schema; fields may evolve after real studies.

A test case freezes the task and its judgment criteria before treatment outputs are inspected. The reusable form is [templates/test-case.md](../templates/test-case.md).

## Identity and provenance

| Field | Required | Description |
| --- | --- | --- |
| `test_case_id` | Yes | Globally unique lower-case identifier. |
| `title` | Yes | Short descriptive title without an expected-outcome claim. |
| `version` | Yes | Case revision identifier. A task or scoring change creates a new version. |
| `case_status` | Yes | Case workflow state: `draft`, `preregistered`, `active`, `retired`, or `compromised`. This is separate from the governed sidecar's artifact `status`. |
| `authors` | Yes | People or model-assisted authorship with provenance. |
| `created_at` | Yes | ISO date, or `unknown` for imported historical cases. |
| `relevant_commit` | At run time | Commit that fixed the case used in the experiment. |
| `license` | Yes | Rights for task text and fixtures; use `unknown` only with an explanation. |

## Task definition

Each case must preserve exact user-visible task text and identify the intended audience, domain, response format, attachments, allowed context, tools, external access, time limit, and any side effects. Hidden fixtures or reference answers may be stored separately to support blinded runs, but their path and checksum must be recorded.

State whether the case is designed to test ambiguity, a false premise, current information, executable output, high-stakes advice, creative work, or another named behavior. Do not retroactively add a challenge label after seeing model behavior.

## Expected behavior and checks

Before running a condition, record:

- required elements and material constraints;
- acceptable answer families, when more than one is valid;
- disallowed outcomes and critical failures;
- machine checks, reference sources, calculations, or expert checks;
- the rubric dimensions that apply and case-specific 0/2/4 anchors;
- the primary outcome, weights if any, and tie handling;
- acceptable ambiguity handling and clarification behavior;
- operational-safety boundaries;
- what evidence would falsify the expected judgment.

Reference material can be wrong. Identify its source, access date, checksum where practical, and uncertainty. Avoid a single hidden answer for genuinely open-ended tasks.

## Experimental controls

Specify conditions without model-specific praise:

- baseline instruction content and placement;
- treatment artifact ID, content checksum, and placement;
- optional originating-model reference condition;
- model identifier, interface, mode, tools, context, and sampling settings held constant;
- trials per condition and stopping rule;
- task and condition randomization;
- fresh-context or carryover policy;
- blinding and de-identification process;
- evaluator assignment and adjudication;
- prompt-leakage controls;
- preregistered exclusions and failure handling.

## Run record

Every completion needs a stable run ID, condition code, timestamp, exact model and environment data, input checksum, output path and checksum, tool transcript or summary when publishable, token/latency data when available, execution errors, exclusion status, and evaluator records. Use `unknown` instead of reconstructing missing values.

## Revision rule

After preregistration, changes to task text, fixtures, expected behavior, scoring, or exclusions create a new case version. Typographical metadata corrections may be appended with a dated reason when they cannot change a score. Never overwrite the case definition used by an existing result.
