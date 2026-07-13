# Test case: [title]

> **Template:** Complete and commit this record before reviewing treatment outputs.

Store a submitted case beside governed `metadata.yaml` based on [the artifact metadata template](artifact-metadata.yaml). The inline identity section below does not replace that sidecar.

## Identity

- Test-case ID: `[lower-case stable ID]`
- Version: `[version]`
- Case status: `[draft / preregistered / active / retired / compromised]`
- Authors, including model assistance: `[names or stable pseudonyms]`
- Created at: `[ISO date or unknown]`
- Relevant commit: `[full hash once fixed]`
- License: `[identifier or unknown with explanation]`

## Purpose

- Behavior under test:
- Intended audience and decision:
- Task class: [factual / coding / ambiguous / false-premise / casual / creative / high-stakes / other]
- Why this case can distinguish baseline from treatment:
- Evidence that would falsify the expected judgment:

## Exact task shown to every condition

```text
[verbatim task]
```

## Inputs and environment

- Attachment paths and checksums:
- Allowed context:
- Allowed tools and permissions:
- Network access:
- Time or token limits:
- Side effects permitted:
- Hidden fixtures or reference paths and checksums:

## Preregistered expected behavior

### Required elements

- [requirement]

### Acceptable answer families

- [valid approach or answer range]

### Disallowed outcomes and critical failures

- [failure]

### Ambiguity and clarification policy

[What assumption, branch, or question is acceptable?]

### Reference checks

| Check ID | Claim or behavior | Method/source | Access date | Expected result | Limitations |
| --- | --- | --- | --- | --- | --- |
| [check] | [value] | [value] | [date] | [value] | [value] |

## Rubric configuration

- Rubric version or commit:
- Primary outcome:
- Applicable dimensions:
- Dimensions preregistered as N/A and why:
- Weights, if any:
- Tie and critical-failure handling:

Define case-specific anchors for every applicable dimension:

| Dimension | 0 anchor | 2 anchor | 4 anchor |
| --- | --- | --- | --- |
| [dimension] | [failure] | [mixed] | [strong] |

## Experimental controls

- Baseline instruction content and placement:
- Treatment artifact ID, checksum, and placement:
- Optional reference condition:
- Matched model/environment settings:
- Trials per condition:
- Stopping rule:
- Condition and task randomization:
- Fresh-context or carryover policy:
- Blinding and de-identification:
- Evaluator assignment and adjudication:
- Prompt-leakage controls:
- Preregistered exclusions and error handling:

## Revision log

| Date | Version | Change | Reason | Author | Affects scoring? |
| --- | --- | --- | --- | --- | --- |
| [date] | [version] | Initial draft | [reason] | [author] | [yes/no] |
