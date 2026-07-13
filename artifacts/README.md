# Artifacts

Artifacts are model outputs, critiques, handoff documents, failure maps, and other generated records studied by Frontier Handoff. Their presence here does not endorse their claims.

## Preservation and evidence

A raw artifact is an immutable byte record. Keep explanation, metadata, corrections, and review outside `raw.md`. Do not add front matter, normalize whitespace, or silently fix a typo in a raw file. The adjacent metadata records a SHA-256 digest so later changes can be detected.

Three ideas are kept separate:

- **Preservation status** describes the record: for example, `raw`, `curated`, `superseded`, or `deprecated`.
- **Claim class** describes what the content is being offered as: a hypothesis, operational proposal, experimental result, reviewed recommendation, or verified finding.
- **Evidence dimensions** record human review, cross-model review, experimental testing, and independent reproduction separately.

`Reviewed` does not mean true. `Tested` does not mean improved. A failed or inconclusive test remains part of the record.

## Package layout

A raw artifact package normally contains:

- `raw.md`: preserved source bytes;
- `metadata.yaml`: identity, provenance, checksum, missing context, and evidence state;
- `review-notes.md`: review observations kept separate from source content.

Any edited or normalized derivative must be a new file or package with its own stable ID, checksum, editor, edit description, date, and parent-artifact reference. Never replace the raw record.

See the [provenance standard](../methodology/provenance-standard.md) before contributing an artifact.

## Included artifact

- [Fable 5: Standing Orders for Claude Opus 4.8](fable-5/001-standing-orders/) — preserved as an operational proposal. At initial import, it had no completed human review, protocol-complete cross-model review, experiment, or independent reproduction.

The source and target names for this first artifact are user-reported. They are not present in the raw document itself, and the exact model identifiers and generation environment are unknown.
