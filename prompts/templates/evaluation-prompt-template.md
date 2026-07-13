# Evaluation prompt template

> **Template status:** Proposed. Use only with a frozen case and rubric version.

## Blind evaluator prompt block

```text
Evaluate the candidate output against the supplied test case and rubric. Do not infer or reward the model, condition, or artifact author. Ignore polish unless a rubric dimension requires it.

Test case ID and version: [ID/version]
Rubric version or commit: [reference]
Applicable dimensions: [list]
Critical failures: [predeclared list]

For each applicable dimension:
1. Cite output evidence.
2. Apply the case-specific anchor before the general rubric.
3. Assign 0–4 or the preregistered N/A.
4. State the main uncertainty in the score.

Then list every critical failure, unsupported outcome-relevant claim, and unmet task requirement. Do not add new criteria after reading the output. Do not treat caution, length, confidence, or a stated verification step as evidence that verification occurred. If identifying information reveals a likely condition, record the suspected leakage but continue scoring the content.

Return the fixed score record first and a short rationale second. Do not provide an aggregate unless the experiment preregistered its weights.
```

## Evaluator record

- Evaluator identity or stable pseudonym:
- Human or model:
- Expertise relevant to case:
- Conflicts or artifact authorship:
- Condition guessed, if any:
- Output order:
- Adjudication used:
