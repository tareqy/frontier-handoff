# Extraction prompt template

> **Template status:** Proposed; using this template does not imply that the resulting artifact is useful or accurate.

Use the fields outside the prompt block to document intent. Preserve the actual executed prompt verbatim in the artifact-specific prompt file.

## Intended extraction

- Operational domain:
- Target successor or environment:
- Decisions the output should support:
- Known source-model context:
- Behaviors that require experimental testing:
- Excluded private or proprietary context:

## Prompt block

```text
You are producing an operational proposal for a successor model or workflow.

Scope: [tasks and conditions]
Target: [model, user, or environment; use “unknown” when not established]

Externalize only procedures that can be stated and tested through text. Do not claim to transfer hidden reasoning, model weights, latent capability, or tool access. Treat descriptions of your own abilities and of other models as hypotheses.

For each proposed procedure:
1. Name the triggering condition.
2. Give observable steps.
3. Name the failure it is intended to reduce.
4. State required tools, information, or permissions.
5. Give one case where the procedure could harm performance or should not apply.
6. Propose a test comparing a baseline without the procedure to a condition with it.

Separate stable instructions from product-specific behavior. Mark facts you cannot establish as unknown. Do not invent benchmark results, citations, model identifiers, or comparative claims. End with the three claims most in need of experimental validation.
```

## Before execution

- Replace every bracketed field.
- Decide whether the task calls for a universal policy or a scoped module; prefer a scoped module unless universality is itself being tested.
- Record model, interface, mode, tools, date, system context when shareable, attachments, and sampling settings.
- Define how the output will be preserved byte-for-byte.
