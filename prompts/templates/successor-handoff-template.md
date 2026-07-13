# Successor handoff prompt template

> **Template status:** Proposed. This template produces an instruction candidate, not a verified capability transfer.

## Prompt block

```text
Write a scoped operating procedure for [successor model or workflow] performing [task class]. Address the procedure to the successor in executable language.

For each rule, provide:
- Trigger: an observable condition.
- Action: a sequence the successor can perform with the stated tools and permissions.
- Check: an observable completion or failure test.
- Boundary: when the rule should be skipped, weakened, or escalated.
- Cost: expected latency, tokens, tool use, or loss of flexibility.
- Failure prevented: the named behavior the rule targets.

Organize rules into three optional levels:
- Light: low-cost checks for casual or reversible tasks.
- Standard: default checks for consequential analytical or production work.
- Strict: high-cost checks for high-stakes, irreversible, or externally executed work.

Do not state that the procedure reproduces another model's reasoning or capability. Do not invent facts about the successor. Mark model comparisons as hypotheses and identify required tool access. Resolve conflicting rules explicitly. End with tests that could show the handoff degrades performance as well as tests that could show improvement.
```

## Scoping record

- Intended task classes:
- Excluded task classes:
- Assumed tools and permissions:
- Treatment placement:
- Maximum acceptable overhead:
- Planned baseline and evaluation cases:
