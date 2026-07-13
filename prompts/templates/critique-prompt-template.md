# Critique prompt template

> **Template status:** Proposed. A model critique is review evidence, not independent verification.

## Prompt block

```text
Review the artifact identified below as an operational proposal, not as authority.

Artifact ID: [ID]
Artifact checksum: [SHA-256]
Review scope: [specific questions]
Target conditions: [tasks, model, tools, and constraints]

Preserve disagreement. For every material observation:
1. Cite the exact rule, section, or line under review.
2. Classify the observation as an internal inconsistency, unsupported claim, implementation risk, task-dependent tradeoff, or testable benefit.
3. State the concrete condition under which it matters.
4. Separate what follows from the artifact text from facts requiring external evidence.
5. Propose the smallest experiment or check that could resolve the question.

Look specifically for tool dependencies, unsafe side effects, excessive rigidity, unnecessary verbosity, hidden judgment calls, product-specific assumptions, and conflicts between rules. Include strengths only when they lead to a testable hypothesis. Do not infer the source model's latent ability from the prose. Do not claim the artifact helps unless result data are supplied and sufficient.

End with: (a) blocking issues, (b) nonblocking concerns, (c) candidate experiments, and (d) unresolved unknowns.
```

## Required review provenance

Record the critique model's exact identifier, interface, mode, tools, prompt, context, date, whether the output was edited, and the parent artifact ID. If any is unavailable, use `unknown`.
