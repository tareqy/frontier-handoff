#!/usr/bin/env python3
"""Validate Frontier Handoff metadata, references, checksums, and local links.

The Python standard library does not include a YAML parser. To keep validation
dependency-free and deterministic, repository metadata uses a deliberately
small YAML profile implemented here. The profile accepts:

* two-space-indented mappings with simple keys;
* scalar sequences;
* quoted or conservative plain scalars;
* ``[]`` and ``{}`` for empty collections; and
* ``|``, ``|-``, ``>``, and ``>-`` block strings.

It deliberately rejects YAML features that make review harder or parsing less
predictable: tabs, duplicate keys, aliases, anchors, tags, merge keys, flow
collections other than empty ones, and sequences of mappings. This script does
not claim to validate arbitrary YAML such as GitHub workflow files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import unquote, urlsplit


SUPPORTED_SCHEMA_VERSIONS = {"0.1"}
CLAIM_CLASSES = {
    "hypothesis",
    "operational-proposal",
    "experimental-result",
    "reviewed-recommendation",
    "verified-finding",
}
CONTENT_STATUSES = {"raw", "curated", "superseded", "deprecated"}
VALIDATION_STATUSES = {
    "not-tested",
    "inconclusive",
    "mixed",
    "not-supported",
    "supported",
}
MODEL_FACING_TYPES = {
    "extraction-prompt",
    "critique-prompt",
    "evaluation-prompt",
    "raw-model-output",
    "successor-standing-instructions",
    "curated-handoff",
    "model-critique",
    "model-routing-protocol",
    "failure-map",
    "experiment-run",
}
EVIDENCE_RECORD_TYPES = {
    "experiment-run",
    "experiment-report",
    "reproduction-report",
}
LIFECYCLE_EVENT_TYPES = {
    "proposed",
    "generated",
    "imported-raw",
    "human-reviewed",
    "cross-model-reviewed",
    "experiment-designed",
    "experimentally-tested",
    "independently-reproduced",
    "revised",
    "superseded",
    "deprecated",
    "metadata-corrected",
}
EFFECT_DIRECTIONS = {
    "beneficial",
    "harmful",
    "mixed",
    "no-detectable-effect",
    "inconclusive",
}

_KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")
_KEBAB_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_INTEGER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)")
_NUMERIC_LIKE_RE = re.compile(
    r"[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?"
)
_BLOCK_RE = re.compile(
    r"(?P<key>[A-Za-z_][A-Za-z0-9_-]*): (?P<marker>[>|](?:[-+]?)?)"
)
_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?P<target><[^>\n]+>|(?:\\.|[^)\s])+)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?\s*\)"
)
_REFERENCE_LINK_RE = re.compile(
    r"^ {0,3}\[[^\]\n]+\]:\s*(?P<target><[^>\n]+>|\S+)"
)


class MetadataProfileError(ValueError):
    """Raised when a file is outside the supported metadata YAML profile."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int | None
    code: str
    message: str

    def format(self, root: Path) -> str:
        try:
            display_path = self.path.resolve().relative_to(root.resolve()).as_posix()
        except (OSError, ValueError):
            display_path = self.path.as_posix()
        location = display_path
        if self.line is not None:
            location += f":{self.line}"
        return f"{location}: {self.code} {self.message}"


@dataclass(frozen=True)
class ParsedMetadata:
    data: dict[str, Any]
    lines: dict[tuple[str, ...], int]


@dataclass(frozen=True)
class MetadataRecord:
    path: Path
    parsed: ParsedMetadata


@dataclass(frozen=True)
class _ProfileLine:
    number: int
    indent: int
    content: str
    block_value: str | None = None


def _render_block(lines: list[str], marker: str) -> str:
    style = marker[0]
    chomping = marker[1:] or "clip"
    if style == "|":
        value = "\n".join(lines)
    else:
        paragraphs: list[str] = []
        current: list[str] = []
        for line in lines:
            if line == "":
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
                paragraphs.append("")
            else:
                current.append(line)
        if current:
            paragraphs.append(" ".join(current))
        value = "\n".join(paragraphs)

    if chomping == "-":
        return value.rstrip("\n")
    # Exact keep-chomping behavior is unnecessary for schema fields, but both
    # accepted forms retain at least the final newline required by YAML.
    return value + "\n"


def _tokenize_profile(text: str) -> list[_ProfileLine]:
    raw_lines = text.splitlines()
    tokens: list[_ProfileLine] = []
    index = 0

    while index < len(raw_lines):
        raw = raw_lines[index]
        line_number = index + 1
        if "\t" in raw:
            raise MetadataProfileError(line_number, "tabs are not allowed")
        if not raw.strip() or raw.lstrip(" ").startswith("#"):
            index += 1
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise MetadataProfileError(
                line_number, "indentation must use multiples of two spaces"
            )
        content = raw[indent:].rstrip()
        if content in {"---", "..."}:
            raise MetadataProfileError(
                line_number, "YAML document markers are outside the metadata profile"
            )

        block_match = _BLOCK_RE.fullmatch(content)
        if block_match:
            marker = block_match.group("marker")
            block_lines: list[str] = []
            next_index = index + 1
            while next_index < len(raw_lines):
                candidate = raw_lines[next_index]
                if "\t" in candidate:
                    raise MetadataProfileError(next_index + 1, "tabs are not allowed")
                if not candidate.strip():
                    block_lines.append("")
                    next_index += 1
                    continue
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if candidate_indent <= indent:
                    break
                if candidate_indent < indent + 2 or candidate_indent % 2:
                    raise MetadataProfileError(
                        next_index + 1,
                        "block content must be indented by at least two spaces",
                    )
                block_lines.append(candidate[indent + 2 :].rstrip())
                next_index += 1
            tokens.append(
                _ProfileLine(
                    number=line_number,
                    indent=indent,
                    content=f"{block_match.group('key')}:",
                    block_value=_render_block(block_lines, marker),
                )
            )
            index = next_index
            continue

        if re.search(r":\s*[>|][0-9+-]*\s*$", content):
            raise MetadataProfileError(
                line_number,
                "only |, |-, |+, >, >-, and >+ block markers are supported",
            )
        tokens.append(_ProfileLine(line_number, indent, content))
        index += 1

    return tokens


def _parse_single_quoted(value: str, line: int) -> str:
    if len(value) < 2 or not value.endswith("'"):
        raise MetadataProfileError(line, "unterminated single-quoted scalar")
    inner = value[1:-1]
    result: list[str] = []
    index = 0
    while index < len(inner):
        if inner[index] != "'":
            result.append(inner[index])
            index += 1
            continue
        if index + 1 >= len(inner) or inner[index + 1] != "'":
            raise MetadataProfileError(
                line, "single quotes inside a scalar must be doubled"
            )
        result.append("'")
        index += 2
    return "".join(result)


def _parse_scalar(value: str, line: int) -> Any:
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise MetadataProfileError(
                line, f"invalid double-quoted scalar: {error.msg}"
            ) from error
        if not isinstance(parsed, str):
            raise MetadataProfileError(line, "quoted metadata scalars must be strings")
        return parsed
    if value.startswith("'"):
        return _parse_single_quoted(value, line)

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    if _INTEGER_RE.fullmatch(value):
        return int(value)

    if lowered in {"~", "yes", "no", "on", "off", "y", "n"}:
        raise MetadataProfileError(
            line, f"ambiguous plain scalar {value!r}; quote it explicitly"
        )
    if _NUMERIC_LIKE_RE.fullmatch(value):
        raise MetadataProfileError(
            line, f"non-integer numeric scalar {value!r} must be quoted"
        )
    if value.startswith(("!", "&", "*", "`", "@", "[", "{", "]", "}")):
        raise MetadataProfileError(
            line, "tags, anchors, aliases, and flow collections are not supported"
        )
    if value.startswith(("|", ">")):
        raise MetadataProfileError(line, "block markers must follow a mapping key")
    if " #" in value or value.startswith("#"):
        raise MetadataProfileError(
            line, "inline comments are not supported; use a full comment line"
        )
    if ": " in value or value.endswith(":"):
        raise MetadataProfileError(
            line, "plain strings containing ': ' must be quoted or use a block scalar"
        )
    return value


def parse_restricted_yaml(text: str) -> ParsedMetadata:
    """Parse a metadata document using the repository's YAML profile."""

    tokens = _tokenize_profile(text)
    if not tokens:
        raise MetadataProfileError(1, "metadata document is empty")
    if tokens[0].indent != 0:
        raise MetadataProfileError(tokens[0].number, "top-level keys must be unindented")
    if tokens[0].content.startswith("-"):
        raise MetadataProfileError(tokens[0].number, "top level must be a mapping")

    source_lines: dict[tuple[str, ...], int] = {}

    def parse_block(
        start: int, indent: int, prefix: tuple[str, ...]
    ) -> tuple[Any, int]:
        if start >= len(tokens) or tokens[start].indent != indent:
            line = tokens[start].number if start < len(tokens) else tokens[-1].number
            raise MetadataProfileError(line, "invalid indentation")

        is_sequence = tokens[start].content.startswith("- ")
        if is_sequence:
            values: list[Any] = []
            index = start
            while index < len(tokens) and tokens[index].indent == indent:
                token = tokens[index]
                if not token.content.startswith("- "):
                    raise MetadataProfileError(
                        token.number, "mappings and sequence items cannot share a block"
                    )
                item = token.content[2:].strip()
                if not item:
                    raise MetadataProfileError(
                        token.number, "empty or nested sequence items are not supported"
                    )
                if re.match(r"[A-Za-z_][A-Za-z0-9_-]*:\s", item):
                    raise MetadataProfileError(
                        token.number, "sequences of mappings are outside the metadata profile"
                    )
                values.append(_parse_scalar(item, token.number))
                index += 1
                if index < len(tokens) and tokens[index].indent > indent:
                    raise MetadataProfileError(
                        tokens[index].number,
                        "nested content below a scalar sequence item is not supported",
                    )
            return values, index

        result: dict[str, Any] = {}
        index = start
        while index < len(tokens) and tokens[index].indent == indent:
            token = tokens[index]
            if token.content.startswith("-"):
                raise MetadataProfileError(
                    token.number, "mappings and sequence items cannot share a block"
                )
            match = re.fullmatch(
                r"([A-Za-z_][A-Za-z0-9_-]*):(.*)", token.content
            )
            if not match:
                raise MetadataProfileError(
                    token.number, "expected a simple mapping key followed by ':'"
                )
            key, remainder = match.groups()
            if not _KEY_RE.fullmatch(key):
                raise MetadataProfileError(token.number, f"invalid key {key!r}")
            if key in result:
                raise MetadataProfileError(token.number, f"duplicate key {key!r}")
            field_path = prefix + (key,)
            source_lines[field_path] = token.number

            if token.block_value is not None:
                result[key] = token.block_value
                index += 1
                continue

            if remainder:
                if not remainder.startswith(" "):
                    raise MetadataProfileError(
                        token.number, "a mapping value must follow ': '"
                    )
                result[key] = _parse_scalar(remainder.strip(), token.number)
                index += 1
                continue

            index += 1
            if index >= len(tokens) or tokens[index].indent <= indent:
                raise MetadataProfileError(
                    token.number, "empty values are not allowed; use null, [], or {}"
                )
            if tokens[index].indent != indent + 2:
                raise MetadataProfileError(
                    tokens[index].number, "nested blocks must indent exactly two spaces"
                )
            result[key], index = parse_block(index, indent + 2, field_path)

        if index < len(tokens) and tokens[index].indent > indent:
            raise MetadataProfileError(tokens[index].number, "unexpected indentation")
        return result, index

    data, final_index = parse_block(0, 0, ())
    if final_index != len(tokens):
        raise MetadataProfileError(tokens[final_index].number, "could not parse document")
    if not isinstance(data, dict):
        raise MetadataProfileError(tokens[0].number, "top level must be a mapping")
    return ParsedMetadata(data=data, lines=source_lines)


def _nested(data: Mapping[str, Any], *path: str) -> Any:
    value: Any = data
    for key in path:
        if not isinstance(value, Mapping) or key not in value:
            return None
        value = value[key]
    return value


def _line(record: MetadataRecord, *path: str) -> int | None:
    return record.parsed.lines.get(tuple(path))


def _add(
    issues: list[Issue],
    record: MetadataRecord,
    code: str,
    message: str,
    *path: str,
) -> None:
    issues.append(Issue(record.path, _line(record, *path), code, message))


def _require_string(
    issues: list[Issue], record: MetadataRecord, *path: str
) -> str | None:
    value = _nested(record.parsed.data, *path)
    dotted = ".".join(path)
    if value is None:
        _add(issues, record, "SCHEMA001", f"missing required field {dotted}", *path)
        return None
    if not isinstance(value, str) or not value.strip():
        _add(
            issues,
            record,
            "SCHEMA002",
            f"{dotted} must be a non-empty string",
            *path,
        )
        return None
    return value


def _require_bool(
    issues: list[Issue], record: MetadataRecord, *path: str
) -> bool | None:
    value = _nested(record.parsed.data, *path)
    dotted = ".".join(path)
    if value is None:
        _add(issues, record, "SCHEMA001", f"missing required field {dotted}", *path)
        return None
    if type(value) is not bool:
        _add(issues, record, "SCHEMA002", f"{dotted} must be a boolean", *path)
        return None
    return value


def _require_list(
    issues: list[Issue], record: MetadataRecord, *path: str
) -> list[Any] | None:
    value = _nested(record.parsed.data, *path)
    dotted = ".".join(path)
    if value is None:
        _add(issues, record, "SCHEMA001", f"missing required field {dotted}", *path)
        return None
    if not isinstance(value, list):
        _add(issues, record, "SCHEMA002", f"{dotted} must be a list", *path)
        return None
    return value


def _require_mapping(
    issues: list[Issue], record: MetadataRecord, *path: str
) -> Mapping[str, Any] | None:
    value = _nested(record.parsed.data, *path)
    dotted = ".".join(path)
    if value is None:
        _add(issues, record, "SCHEMA001", f"missing required field {dotted}", *path)
        return None
    if not isinstance(value, Mapping):
        _add(issues, record, "SCHEMA002", f"{dotted} must be a mapping", *path)
        return None
    return value


def _validate_unknown_or_string_list(
    issues: list[Issue], record: MetadataRecord, *path: str
) -> None:
    value = _nested(record.parsed.data, *path)
    dotted = ".".join(path)
    if value is None:
        _add(issues, record, "SCHEMA001", f"missing required field {dotted}", *path)
        return
    valid = value == "unknown" or (
        isinstance(value, list)
        and all(isinstance(item, str) and item.strip() for item in value)
    )
    if not valid:
        _add(
            issues,
            record,
            "SCHEMA002",
            f"{dotted} must be 'unknown' or a list of non-empty strings",
            *path,
        )


def _valid_iso_date(value: str) -> bool:
    try:
        if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            date.fromisoformat(value)
        else:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _validate_metadata_schema(record: MetadataRecord) -> list[Issue]:
    issues: list[Issue] = []
    data = record.parsed.data

    schema_version = _require_string(issues, record, "schema_version")
    if schema_version and schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        _add(
            issues,
            record,
            "SCHEMA003",
            f"unsupported schema_version {schema_version!r}",
            "schema_version",
        )

    artifact_id = _require_string(issues, record, "artifact_id")
    if artifact_id and not _KEBAB_RE.fullmatch(artifact_id):
        _add(
            issues,
            record,
            "SCHEMA003",
            "artifact_id must use lowercase kebab-case",
            "artifact_id",
        )
    _require_string(issues, record, "title")
    _require_string(issues, record, "description")
    artifact_type = _require_string(issues, record, "artifact_type")
    if artifact_type and not _KEBAB_RE.fullmatch(artifact_type):
        _add(
            issues,
            record,
            "SCHEMA003",
            "artifact_type must use lowercase kebab-case",
            "artifact_type",
        )

    claim_class = _require_string(issues, record, "claim_class")
    if claim_class and claim_class not in CLAIM_CLASSES:
        _add(
            issues,
            record,
            "SCHEMA003",
            f"claim_class must be one of {', '.join(sorted(CLAIM_CLASSES))}",
            "claim_class",
        )
    status = _require_string(issues, record, "status")
    if status and status not in CONTENT_STATUSES:
        _add(
            issues,
            record,
            "SCHEMA003",
            f"status must be one of {', '.join(sorted(CONTENT_STATUSES))}",
            "status",
        )

    created_at = _require_string(issues, record, "created_at")
    if created_at and created_at != "unknown" and not _valid_iso_date(created_at):
        _add(
            issues,
            record,
            "SCHEMA003",
            "created_at must be 'unknown' or an ISO 8601 date/time",
            "created_at",
        )
    imported_at = _require_string(issues, record, "imported_at")
    if imported_at and (imported_at == "unknown" or not _valid_iso_date(imported_at)):
        _add(
            issues,
            record,
            "SCHEMA003",
            "imported_at must be a known ISO 8601 date/time",
            "imported_at",
        )

    content = data.get("content")
    if not isinstance(content, Mapping):
        _add(issues, record, "SCHEMA001", "content must be a mapping", "content")
    content_path = _require_string(issues, record, "content", "path")
    media_type = _require_string(issues, record, "content", "media_type")
    if media_type and not re.fullmatch(r"[a-z0-9.+-]+/[a-z0-9.+-]+", media_type):
        _add(
            issues,
            record,
            "SCHEMA003",
            "content.media_type must be a lowercase media type",
            "content",
            "media_type",
        )
    checksum = _require_string(issues, record, "content", "sha256")
    if checksum and not _SHA256_RE.fullmatch(checksum):
        _add(
            issues,
            record,
            "SCHEMA003",
            "content.sha256 must be 64 lowercase hexadecimal characters",
            "content",
            "sha256",
        )
    byte_count = _nested(data, "content", "byte_count")
    if byte_count is None:
        _add(
            issues,
            record,
            "SCHEMA001",
            "missing required field content.byte_count",
            "content",
            "byte_count",
        )
    elif type(byte_count) is not int or byte_count < 0:
        _add(
            issues,
            record,
            "SCHEMA002",
            "content.byte_count must be a non-negative integer",
            "content",
            "byte_count",
        )

    provenance = data.get("provenance")
    if not isinstance(provenance, Mapping):
        _add(
            issues,
            record,
            "SCHEMA001",
            "provenance must be a mapping",
            "provenance",
        )
    source = _require_string(issues, record, "provenance", "source")
    content_modified = _require_bool(
        issues, record, "provenance", "content_modified"
    )
    _require_string(issues, record, "provenance", "chain_of_custody")
    if source == "user-provided" and status == "raw":
        _require_string(issues, record, "provenance", "original_filename")

    modifications = _require_mapping(issues, record, "modifications")
    if modifications is not None:
        for modification_id, modification in modifications.items():
            modification_path = ("modifications", modification_id)
            if not _KEBAB_RE.fullmatch(modification_id):
                _add(
                    issues,
                    record,
                    "SCHEMA003",
                    "modification IDs must use lowercase kebab-case",
                    *modification_path,
                )
            if not isinstance(modification, Mapping):
                _add(
                    issues,
                    record,
                    "SCHEMA002",
                    f"modifications.{modification_id} must be a mapping",
                    *modification_path,
                )
                continue
            occurred_at = _require_string(
                issues, record, *modification_path, "occurred_at"
            )
            if (
                occurred_at
                and occurred_at != "unknown"
                and not _valid_iso_date(occurred_at)
            ):
                _add(
                    issues,
                    record,
                    "SCHEMA003",
                    f"modifications.{modification_id}.occurred_at must be "
                    "'unknown' or an ISO 8601 date/time",
                    *modification_path,
                    "occurred_at",
                )
            for field in (
                "actor",
                "modification_type",
                "description",
                "reason",
                "source",
            ):
                value = _require_string(issues, record, *modification_path, field)
                if (
                    field == "modification_type"
                    and value
                    and not _KEBAB_RE.fullmatch(value)
                ):
                    _add(
                        issues,
                        record,
                        "SCHEMA003",
                        "modification_type must use lowercase kebab-case",
                        *modification_path,
                        field,
                    )
            _require_bool(issues, record, *modification_path, "meaning_changed")
    if status == "raw" and content_modified is True:
        _add(
            issues,
            record,
            "STATE001",
            "raw content cannot have provenance.content_modified set to true",
            "provenance",
            "content_modified",
        )
    if content_modified is False and modifications:
        _add(
            issues,
            record,
            "STATE001",
            "unmodified content must have an empty modifications mapping",
            "modifications",
        )
    if content_modified is True and modifications == {}:
        _add(
            issues,
            record,
            "STATE001",
            "modified content must describe at least one modification",
            "modifications",
        )
    if status == "curated" and not (
        content_modified is True and modifications is not None and bool(modifications)
    ):
        _add(
            issues,
            record,
            "STATE001",
            "curated content requires content_modified: true and at least one "
            "modification record",
            "status",
        )

    review = data.get("review")
    if not isinstance(review, Mapping):
        _add(issues, record, "SCHEMA001", "review must be a mapping", "review")
    human_reviewed = _require_bool(issues, record, "review", "human_reviewed")
    reviewers = _require_list(issues, record, "review", "reviewers")
    cross_model_reviewed = _require_bool(
        issues, record, "review", "cross_model_reviewed"
    )
    review_models = _require_list(issues, record, "review", "review_models")
    human_review_paths = _require_list(
        issues, record, "review", "human_review_paths"
    )
    cross_model_review_paths = _require_list(
        issues, record, "review", "cross_model_review_paths"
    )
    experimentally_validated = _require_bool(
        issues, record, "review", "experimentally_validated"
    )
    evaluation_paths = _require_list(issues, record, "review", "evaluation_paths")
    independently_reproduced = _require_bool(
        issues, record, "review", "independently_reproduced"
    )
    reproduction_paths = _require_list(
        issues, record, "review", "reproduction_paths"
    )

    for values, field in (
        (reviewers, "reviewers"),
        (human_review_paths, "human_review_paths"),
        (review_models, "review_models"),
        (cross_model_review_paths, "cross_model_review_paths"),
        (evaluation_paths, "evaluation_paths"),
        (reproduction_paths, "reproduction_paths"),
    ):
        if values is not None and not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            _add(
                issues,
                record,
                "SCHEMA002",
                f"review.{field} must contain only non-empty strings",
                "review",
                field,
            )
        if values is not None and len(values) != len(set(values)):
            _add(
                issues,
                record,
                "SCHEMA003",
                f"review.{field} must not contain duplicate entries",
                "review",
                field,
            )
    if human_reviewed is True and not reviewers:
        _add(
            issues,
            record,
            "STATE001",
            "human_reviewed requires at least one reviewer",
            "review",
            "reviewers",
        )
    if human_reviewed is True and not human_review_paths:
        _add(
            issues,
            record,
            "STATE001",
            "human_reviewed requires at least one qualifying human_review_path",
            "review",
            "human_review_paths",
        )
    if human_reviewed is False and reviewers:
        _add(
            issues,
            record,
            "STATE001",
            "reviewers must be empty while human_reviewed is false",
            "review",
            "reviewers",
        )
    if human_reviewed is False and human_review_paths:
        _add(
            issues,
            record,
            "STATE001",
            "human_review_paths must be empty while human_reviewed is false",
            "review",
            "human_review_paths",
        )
    if cross_model_reviewed is True and not review_models:
        _add(
            issues,
            record,
            "STATE001",
            "cross_model_reviewed requires at least one review model",
            "review",
            "review_models",
        )
    if cross_model_reviewed is True and not cross_model_review_paths:
        _add(
            issues,
            record,
            "STATE001",
            "cross_model_reviewed requires at least one qualifying "
            "cross_model_review_path",
            "review",
            "cross_model_review_paths",
        )
    if cross_model_reviewed is False and review_models:
        _add(
            issues,
            record,
            "STATE001",
            "review_models must be empty while cross_model_reviewed is false",
            "review",
            "review_models",
        )
    if cross_model_reviewed is False and cross_model_review_paths:
        _add(
            issues,
            record,
            "STATE001",
            "cross_model_review_paths must be empty while "
            "cross_model_reviewed is false",
            "review",
            "cross_model_review_paths",
        )

    validation_status = _require_string(issues, record, "validation_status")
    if validation_status and validation_status not in VALIDATION_STATUSES:
        _add(
            issues,
            record,
            "SCHEMA003",
            "validation_status must be one of "
            + ", ".join(sorted(VALIDATION_STATUSES)),
            "validation_status",
        )
    if validation_status == "not-tested" and (
        experimentally_validated is True or independently_reproduced is True
    ):
        _add(
            issues,
            record,
            "STATE001",
            "not-tested conflicts with validation or reproduction claims",
            "validation_status",
        )
    if validation_status == "not-tested" and evaluation_paths:
        _add(
            issues,
            record,
            "STATE001",
            "evaluation_paths must be empty while validation_status is not-tested",
            "review",
            "evaluation_paths",
        )
    if (
        validation_status in VALIDATION_STATUSES - {"not-tested"}
        and not evaluation_paths
        and artifact_type not in EVIDENCE_RECORD_TYPES
    ):
        _add(
            issues,
            record,
            "STATE001",
            "a completed validation_status requires at least one evaluation_path",
            "review",
            "evaluation_paths",
        )
    if experimentally_validated is True and validation_status != "supported":
        _add(
            issues,
            record,
            "STATE001",
            "experimentally_validated requires validation_status: supported",
            "review",
            "experimentally_validated",
        )
    if (
        experimentally_validated is True
        and not evaluation_paths
        and artifact_type not in EVIDENCE_RECORD_TYPES
    ):
        _add(
            issues,
            record,
            "STATE001",
            "experimentally_validated requires at least one evaluation_path",
            "review",
            "evaluation_paths",
        )
    if (
        independently_reproduced is True
        and not reproduction_paths
    ):
        _add(
            issues,
            record,
            "STATE001",
            "independently_reproduced requires at least one reproduction_path",
            "review",
            "reproduction_paths",
        )
    if claim_class == "experimental-result" and validation_status == "not-tested":
        _add(
            issues,
            record,
            "STATE001",
            "experimental-result requires a completed test outcome",
            "claim_class",
        )
    if claim_class == "reviewed-recommendation" and not (
        human_reviewed is True or cross_model_reviewed is True
    ):
        _add(
            issues,
            record,
            "STATE001",
            "reviewed-recommendation requires human or cross-model review",
            "claim_class",
        )
    if claim_class == "verified-finding":
        required_state = (
            human_reviewed is True
            and experimentally_validated is True
            and independently_reproduced is True
            and validation_status == "supported"
        )
        if not required_state:
            _add(
                issues,
                record,
                "STATE001",
                "verified-finding requires human review, supported experimental "
                "validation, and independent reproduction",
                "claim_class",
            )

    _require_string(issues, record, "license")
    limitations = data.get("known_limitations")
    if limitations is not None and (
        not isinstance(limitations, list)
        or not all(isinstance(item, str) and item.strip() for item in limitations)
    ):
        _add(
            issues,
            record,
            "SCHEMA002",
            "known_limitations must be a list of non-empty strings",
            "known_limitations",
        )
    parent_artifacts = data.get("parent_artifacts")
    if parent_artifacts is not None and (
        not isinstance(parent_artifacts, list)
        or not all(
            isinstance(item, str) and _KEBAB_RE.fullmatch(item)
            for item in parent_artifacts
        )
    ):
        _add(
            issues,
            record,
            "SCHEMA002",
            "parent_artifacts must be a list of artifact IDs",
            "parent_artifacts",
        )

    if artifact_type in MODEL_FACING_TYPES:
        for field in (
            "source_model",
            "target_model",
            "provider",
            "model_identifier",
            "model_mode",
            "interface",
        ):
            _require_string(issues, record, field)
        _validate_unknown_or_string_list(issues, record, "tools_available")
        _validate_unknown_or_string_list(
            issues, record, "attachments_or_context_used"
        )
        system_instructions = data.get("system_instructions")
        if system_instructions is not None and (
            not isinstance(system_instructions, str) or not system_instructions.strip()
        ):
            _add(
                issues,
                record,
                "SCHEMA002",
                "system_instructions must be a non-empty string when present",
                "system_instructions",
            )

    if artifact_type == "successor-standing-instructions":
        _require_string(issues, record, "prompt_path")

    lifecycle_events = data.get("lifecycle_events")
    if lifecycle_events is not None:
        if not isinstance(lifecycle_events, Mapping):
            _add(
                issues,
                record,
                "SCHEMA002",
                "lifecycle_events must be a mapping keyed by stable event ID",
                "lifecycle_events",
            )
        else:
            for event_id, event in lifecycle_events.items():
                event_path = ("lifecycle_events", event_id)
                if not _KEBAB_RE.fullmatch(event_id):
                    _add(
                        issues,
                        record,
                        "SCHEMA003",
                        "lifecycle event IDs must use lowercase kebab-case",
                        *event_path,
                    )
                if not isinstance(event, Mapping):
                    _add(
                        issues,
                        record,
                        "SCHEMA002",
                        f"lifecycle_events.{event_id} must be a mapping",
                        *event_path,
                    )
                    continue
                occurred_at = _require_string(
                    issues, record, *event_path, "occurred_at"
                )
                if (
                    occurred_at
                    and occurred_at != "unknown"
                    and not _valid_iso_date(occurred_at)
                ):
                    _add(
                        issues,
                        record,
                        "SCHEMA003",
                        f"lifecycle_events.{event_id}.occurred_at must be "
                        "'unknown' or an ISO 8601 date/time",
                        *event_path,
                        "occurred_at",
                    )
                _require_string(issues, record, *event_path, "actor")
                event_type = _require_string(
                    issues, record, *event_path, "event_type"
                )
                if event_type and event_type not in LIFECYCLE_EVENT_TYPES:
                    _add(
                        issues,
                        record,
                        "SCHEMA003",
                        "event_type must be one of "
                        + ", ".join(sorted(LIFECYCLE_EVENT_TYPES)),
                        *event_path,
                        "event_type",
                    )
                _require_string(issues, record, *event_path, "description")

    effect_direction = data.get("effect_direction")
    if effect_direction is not None and effect_direction not in EFFECT_DIRECTIONS:
        _add(
            issues,
            record,
            "SCHEMA003",
            "effect_direction must be one of "
            + ", ".join(sorted(EFFECT_DIRECTIONS)),
            "effect_direction",
        )

    relevant_commit = data.get("relevant_commit")
    if relevant_commit is not None and not (
        relevant_commit == "unknown"
        or (
            isinstance(relevant_commit, str)
            and re.fullmatch(r"[0-9a-f]{7,40}", relevant_commit)
        )
    ):
        _add(
            issues,
            record,
            "SCHEMA003",
            "relevant_commit must be 'unknown' or a 7-40 character Git hash",
            "relevant_commit",
        )

    # Suppress unused local warnings while retaining descriptive variable names
    # for schema checks above.
    _ = content_path
    return issues


def _discover_metadata(root: Path) -> list[Path]:
    paths: list[Path] = []
    for top_level in ("artifacts", "prompts", "evaluations"):
        base = root / top_level
        if not base.is_dir():
            continue
        for path in base.rglob("metadata.yaml"):
            relative = path.relative_to(root)
            if "templates" in relative.parts:
                continue
            paths.append(path)
    return sorted(paths)


def _safe_repo_file(
    root: Path, reference: str
) -> tuple[Path | None, str | None]:
    if not reference or reference == "unknown":
        return None, "reference must name a repository file"
    if "\\" in reference:
        return None, "repository paths must use forward slashes"
    pure = PurePosixPath(reference)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None, "repository path must be normalized, relative, and remain in the repository"
    candidate = root.joinpath(*pure.parts)
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except FileNotFoundError:
        return None, "referenced file does not exist"
    except (OSError, ValueError):
        return None, "referenced path escapes the repository"
    if not resolved.is_file():
        return None, "reference must point to a file"
    return resolved, None


def _metadata_path_fields(record: MetadataRecord) -> Iterable[tuple[tuple[str, ...], str]]:
    candidates = [
        ("content", "path"),
        ("prompt_path",),
        ("review", "preliminary_review", "path"),
    ]
    for path in candidates:
        value = _nested(record.parsed.data, *path)
        if isinstance(value, str) and value != "unknown":
            yield path, value

    for list_field in ("attachment_paths", "evaluation_paths", "test_case_paths"):
        values = record.parsed.data.get(list_field)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str) and value != "unknown":
                    yield (list_field,), value

    for list_field in (
        "human_review_paths",
        "cross_model_review_paths",
        "evaluation_paths",
        "reproduction_paths",
    ):
        values = _nested(record.parsed.data, "review", list_field)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str) and value != "unknown":
                    yield ("review", list_field), value


def _hash_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            byte_count += len(chunk)
    return digest.hexdigest(), byte_count


def _validate_metadata_relations(
    root: Path, records: Sequence[MetadataRecord]
) -> tuple[list[Issue], set[Path]]:
    issues: list[Issue] = []
    ids: dict[str, MetadataRecord] = {}
    raw_content_paths: set[Path] = set()
    records_by_metadata_path = {
        record.path.resolve(): record for record in records
    }

    for record in records:
        artifact_id = record.parsed.data.get("artifact_id")
        if not isinstance(artifact_id, str):
            continue
        if artifact_id in ids:
            first = ids[artifact_id]
            issues.append(
                Issue(
                    record.path,
                    _line(record, "artifact_id"),
                    "ID001",
                    f"duplicate artifact_id {artifact_id!r}; first declared in "
                    f"{first.path.relative_to(root).as_posix()}",
                )
            )
        else:
            ids[artifact_id] = record

    for record in records:
        data = record.parsed.data
        artifact_id = data.get("artifact_id")
        parents = data.get("parent_artifacts", [])
        if isinstance(parents, list):
            for parent in parents:
                if not isinstance(parent, str):
                    continue
                if parent == artifact_id:
                    _add(
                        issues,
                        record,
                        "REF002",
                        "an artifact cannot name itself as a parent",
                        "parent_artifacts",
                    )
                elif parent not in ids:
                    _add(
                        issues,
                        record,
                        "REF001",
                        f"parent artifact {parent!r} is not present in the repository",
                        "parent_artifacts",
                    )

        resolved_paths: list[tuple[tuple[str, ...], str, Path]] = []
        for field_path, reference in _metadata_path_fields(record):
            resolved, error = _safe_repo_file(root, reference)
            if error:
                _add(
                    issues,
                    record,
                    "REF001",
                    f"{'.'.join(field_path)}: {error}: {reference!r}",
                    *field_path,
                )
            elif resolved is not None:
                resolved_paths.append((field_path, reference, resolved))

        evidence_rules = {
            ("review", "human_review_paths"): (
                "human-review",
                None,
            ),
            ("review", "cross_model_review_paths"): (
                "model-critique",
                None,
            ),
            ("review", "evaluation_paths"): (
                "experiment-report",
                None,
            ),
            ("review", "reproduction_paths"): (
                "reproduction-report",
                None,
            ),
        }
        for field_path, reference, resolved in resolved_paths:
            if field_path not in evidence_rules:
                continue
            target_record = records_by_metadata_path.get(resolved)
            if target_record is None:
                _add(
                    issues,
                    record,
                    "EVIDENCE001",
                    f"{'.'.join(field_path)} must point to a governed metadata.yaml "
                    f"record: {reference!r}",
                    *field_path,
                )
                continue
            if target_record is record:
                _add(
                    issues,
                    record,
                    "EVIDENCE001",
                    f"{'.'.join(field_path)} cannot use the subject artifact itself",
                    *field_path,
                )
                continue

            required_type, allowed_claim_class = evidence_rules[field_path]
            target_data = target_record.parsed.data
            target_type = target_data.get("artifact_type")
            target_claim_class = target_data.get("claim_class")
            if not (
                target_type == required_type
                or (
                    allowed_claim_class is not None
                    and target_claim_class == allowed_claim_class
                )
            ):
                alternative = (
                    f" or claim_class {allowed_claim_class!r}"
                    if allowed_claim_class
                    else ""
                )
                _add(
                    issues,
                    record,
                    "EVIDENCE002",
                    f"{'.'.join(field_path)} target must have artifact_type "
                    f"{required_type!r}{alternative}; got {target_type!r}/"
                    f"{target_claim_class!r}",
                    *field_path,
                )

            target_parents = target_data.get("parent_artifacts")
            if not isinstance(artifact_id, str) or not isinstance(
                target_parents, list
            ) or artifact_id not in target_parents:
                _add(
                    issues,
                    record,
                    "EVIDENCE003",
                    f"evidence record {reference!r} must name {artifact_id!r} in "
                    "its parent_artifacts",
                    *field_path,
                )

        content_path = next(
            (
                resolved
                for field_path, _reference, resolved in resolved_paths
                if field_path == ("content", "path")
            ),
            None,
        )
        expected_checksum = _nested(data, "content", "sha256")
        expected_bytes = _nested(data, "content", "byte_count")
        if content_path is not None and isinstance(expected_checksum, str):
            actual_checksum, actual_bytes = _hash_file(content_path)
            if actual_checksum != expected_checksum:
                _add(
                    issues,
                    record,
                    "CHECKSUM001",
                    f"content checksum mismatch: expected {expected_checksum}, "
                    f"computed {actual_checksum}",
                    "content",
                    "sha256",
                )
            if type(expected_bytes) is int and actual_bytes != expected_bytes:
                _add(
                    issues,
                    record,
                    "CHECKSUM002",
                    f"content byte_count mismatch: expected {expected_bytes}, "
                    f"computed {actual_bytes}",
                    "content",
                    "byte_count",
                )
            if data.get("status") == "raw":
                raw_content_paths.add(content_path)

    return issues, raw_content_paths


def _strip_inline_code(line: str) -> str:
    return re.sub(r"(`+)(?:(?!\1).)*\1", "", line)


def _markdown_targets(path: Path) -> Iterable[tuple[int, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return

    fence_character: str | None = None
    fence_length = 0
    for number, line in enumerate(lines, 1):
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            continue
        if fence_character is not None:
            continue

        visible = _strip_inline_code(line)
        reference_match = _REFERENCE_LINK_RE.match(visible)
        if reference_match:
            yield number, reference_match.group("target")
        for match in _INLINE_LINK_RE.finditer(visible):
            yield number, match.group("target")


def _validate_markdown_links(root: Path, raw_content_paths: set[Path]) -> list[Issue]:
    issues: list[Issue] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts:
            continue
        try:
            resolved_path = path.resolve(strict=True)
        except OSError:
            continue
        if resolved_path in raw_content_paths:
            # Historical raw content is immutable. Its links are evidence, not
            # repository-authored navigation that the project can silently fix.
            continue
        for line, raw_target in _markdown_targets(path):
            target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
            target = target.replace("\\)", ")").replace("\\(", "(")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//") or not parsed.path:
                continue
            decoded_path = unquote(parsed.path)
            if any(token in decoded_path for token in ("{{", "}}", "<", ">")):
                continue
            pure = PurePosixPath(decoded_path)
            if pure.is_absolute() or "\\" in decoded_path:
                issues.append(
                    Issue(
                        path,
                        line,
                        "LINK001",
                        f"internal Markdown link must be relative: {target!r}",
                    )
                )
                continue
            candidate = path.parent.joinpath(*pure.parts)
            try:
                resolved = candidate.resolve(strict=True)
                resolved.relative_to(root.resolve())
            except FileNotFoundError:
                issues.append(
                    Issue(
                        path,
                        line,
                        "LINK001",
                        f"internal Markdown link target does not exist: {target!r}",
                    )
                )
            except (OSError, ValueError):
                issues.append(
                    Issue(
                        path,
                        line,
                        "LINK001",
                        f"internal Markdown link escapes the repository: {target!r}",
                    )
                )
    return issues


def validate_repository(root: Path) -> list[Issue]:
    """Return every deterministic validation issue found below ``root``."""

    root = root.resolve()
    issues: list[Issue] = []
    records: list[MetadataRecord] = []
    metadata_paths = _discover_metadata(root)
    if not metadata_paths:
        issues.append(
            Issue(root, None, "META001", "no governed metadata.yaml files were found")
        )

    for path in metadata_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(
                Issue(path, None, "YAML001", "metadata must be valid UTF-8")
            )
            continue
        try:
            parsed = parse_restricted_yaml(text)
        except MetadataProfileError as error:
            issues.append(Issue(path, error.line, "YAML001", str(error)))
            continue
        record = MetadataRecord(path=path, parsed=parsed)
        records.append(record)
        issues.extend(_validate_metadata_schema(record))

    relation_issues, raw_content_paths = _validate_metadata_relations(root, records)
    issues.extend(relation_issues)
    issues.extend(_validate_markdown_links(root, raw_content_paths))
    return sorted(
        issues,
        key=lambda issue: (
            issue.path.as_posix(),
            issue.line if issue.line is not None else 0,
            issue.code,
            issue.message,
        ),
    )


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    issues = validate_repository(root)
    if issues:
        for issue in issues:
            print(issue.format(root))
        print(f"Validation failed with {len(issues)} issue(s).")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
