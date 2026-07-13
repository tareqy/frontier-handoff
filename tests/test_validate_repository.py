from __future__ import annotations

import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import (
    MetadataProfileError,
    parse_restricted_yaml,
    validate_repository,
)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _yaml_list(name: str, values: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    if not values:
        return f"{prefix}{name}: []"
    items = "\n".join(f"{prefix}  - {value}" for value in values)
    return f"{prefix}{name}:\n{items}"


def _metadata_text(
    *,
    artifact_id: str,
    content_path: str,
    content: bytes,
    artifact_type: str = "test-record",
    status: str = "raw",
    parent_artifacts: list[str] | None = None,
    claim_class: str = "operational-proposal",
    validation_status: str = "not-tested",
    content_modified: bool = False,
    modifications: list[str] | None = None,
    human_reviewed: bool = False,
    reviewers: list[str] | None = None,
    human_review_paths: list[str] | None = None,
    cross_model_reviewed: bool = False,
    review_models: list[str] | None = None,
    cross_model_review_paths: list[str] | None = None,
    experimentally_validated: bool = False,
    evaluation_paths: list[str] | None = None,
    independently_reproduced: bool = False,
    reproduction_paths: list[str] | None = None,
) -> str:
    parents = _yaml_list("parent_artifacts", parent_artifacts or [])
    if modifications:
        modification_entries = []
        for index, description in enumerate(modifications, 1):
            modification_entries.append(
                f"""\
  test-change-{index}:
    occurred_at: "2026-07-13"
    actor: Test fixture
    modification_type: test-change
    description: {json.dumps(description)}
    reason: Exercise modification validation.
    source: Test fixture source
    meaning_changed: false"""
            )
        edits = "modifications:\n" + "\n".join(modification_entries)
    else:
        edits = "modifications: {}"
    human_reviewers = _yaml_list("reviewers", reviewers or [], indent=2)
    human_paths = _yaml_list(
        "human_review_paths", human_review_paths or [], indent=2
    )
    models = _yaml_list("review_models", review_models or [], indent=2)
    model_paths = _yaml_list(
        "cross_model_review_paths", cross_model_review_paths or [], indent=2
    )
    evaluations = _yaml_list("evaluation_paths", evaluation_paths or [], indent=2)
    reproductions = _yaml_list(
        "reproduction_paths", reproduction_paths or [], indent=2
    )
    return f"""\
schema_version: "0.1"
artifact_id: {artifact_id}
title: Test artifact
description: A test record.
artifact_type: {artifact_type}
claim_class: {claim_class}
status: {status}
source_model: unknown
target_model: unknown
provider: unknown
model_identifier: unknown
model_mode: unknown
interface: unknown
system_instructions: unknown
tools_available: unknown
attachments_or_context_used: unknown
created_at: unknown
imported_at: "2026-07-13"
{parents}
content:
  path: {content_path}
  media_type: text/markdown
  sha256: "{_sha256(content)}"
  byte_count: {len(content)}
provenance:
  source: direct-generation
  content_modified: {str(content_modified).lower()}
  chain_of_custody: Created by the validator test fixture.
{edits}
review:
  human_reviewed: {str(human_reviewed).lower()}
{human_reviewers}
{human_paths}
  cross_model_reviewed: {str(cross_model_reviewed).lower()}
{models}
{model_paths}
  experimentally_validated: {str(experimentally_validated).lower()}
{evaluations}
  independently_reproduced: {str(independently_reproduced).lower()}
{reproductions}
validation_status: {validation_status}
lifecycle_events: {{}}
license: unknown
"""


class TemporaryRepository:
    def __init__(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.base = Path(self._temporary.name)
        self.root = self.base / "repository"
        self.root.mkdir()

    def close(self) -> None:
        self._temporary.cleanup()

    def write_artifact(
        self,
        artifact_id: str = "test-one",
        *,
        directory: str = "artifacts/test-one",
        content: bytes = b"source bytes\n",
        content_path: str | None = None,
        create_content: bool = True,
        metadata: str | None = None,
        **metadata_options: object,
    ) -> Path:
        artifact_directory = self.root / directory
        artifact_directory.mkdir(parents=True, exist_ok=True)
        repository_content_path = content_path or f"{directory}/raw.md"
        if create_content:
            target = self.root.joinpath(*Path(repository_content_path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        metadata_path = artifact_directory / "metadata.yaml"
        metadata_path.write_text(
            metadata
            or _metadata_text(
                artifact_id=artifact_id,
                content_path=repository_content_path,
                content=content,
                **metadata_options,
            ),
            encoding="utf-8",
        )
        return metadata_path


class MetadataProfileTests(unittest.TestCase):
    def test_parses_nested_mappings_sequences_and_folded_text(self) -> None:
        parsed = parse_restricted_yaml(
            """\
schema_version: "0.1"
description: >-
  First line
  continues here.
review:
  complete: false
  reviewers:
    - Alice
    - Model B
empty: []
"""
        )

        self.assertEqual(parsed.data["schema_version"], "0.1")
        self.assertEqual(parsed.data["description"], "First line continues here.")
        self.assertEqual(parsed.data["review"]["reviewers"], ["Alice", "Model B"])
        self.assertFalse(parsed.data["review"]["complete"])
        self.assertEqual(parsed.lines[("review", "reviewers")], 7)

    def test_rejects_duplicate_keys_at_any_depth(self) -> None:
        for text in (
            "artifact_id: one\nartifact_id: two\n",
            "review:\n  complete: false\n  complete: true\n",
        ):
            with self.subTest(text=text), self.assertRaises(MetadataProfileError):
                parse_restricted_yaml(text)

    def test_rejects_tabs_odd_indentation_and_inline_comments(self) -> None:
        invalid_documents = (
            "artifact_id:\tvalue\n",
            "artifact_id: one\n   title: bad\n",
            "artifact_id: one # ambiguous\n",
        )
        for text in invalid_documents:
            with self.subTest(text=text), self.assertRaises(MetadataProfileError):
                parse_restricted_yaml(text)

    def test_rejects_anchors_aliases_flow_values_and_sequences_of_mappings(self) -> None:
        invalid_documents = (
            "artifact_id: &id one\n",
            "artifact_id: *id\n",
            "data: [one, two]\n",
            "items:\n  - name: one\n",
        )
        for text in invalid_documents:
            with self.subTest(text=text), self.assertRaises(MetadataProfileError):
                parse_restricted_yaml(text)

    def test_requires_quotes_for_ambiguous_scalars(self) -> None:
        for scalar in ("yes", "NO", "on", "1.5"):
            with self.subTest(scalar=scalar), self.assertRaises(MetadataProfileError):
                parse_restricted_yaml(f"value: {scalar}\n")


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TemporaryRepository()

    def tearDown(self) -> None:
        self.repository.close()

    def issues(self) -> list:
        return validate_repository(self.repository.root)

    def codes(self) -> list[str]:
        return [issue.code for issue in self.issues()]

    def test_minimal_valid_repository_passes(self) -> None:
        self.repository.write_artifact()
        self.assertEqual(self.issues(), [])

    def test_byte_count_is_required(self) -> None:
        path = self.repository.write_artifact()
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^  byte_count: [0-9]+\n", "", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")

        issues = self.issues()
        self.assertTrue(
            any(
                issue.code == "SCHEMA001" and "content.byte_count" in issue.message
                for issue in issues
            )
        )

    def test_missing_required_field_is_reported(self) -> None:
        path = self.repository.write_artifact()
        text = path.read_text(encoding="utf-8").replace("title: Test artifact\n", "")
        path.write_text(text, encoding="utf-8")

        issues = self.issues()
        self.assertIn("SCHEMA001", [issue.code for issue in issues])
        self.assertTrue(any("title" in issue.message for issue in issues))

    def test_governed_metadata_must_use_the_profile(self) -> None:
        path = self.repository.write_artifact()
        path.write_text("artifact_id: &shared one\n", encoding="utf-8")

        issues = self.issues()
        self.assertEqual([issue.code for issue in issues], ["YAML001"])

    def test_template_metadata_is_not_validated_as_a_record(self) -> None:
        self.repository.write_artifact()
        template = self.repository.root / "templates" / "metadata.yaml"
        template.parent.mkdir(parents=True)
        template.write_text("not: [in, profile]\n", encoding="utf-8")

        self.assertEqual(self.issues(), [])

    def test_no_metadata_records_is_an_error(self) -> None:
        issues = self.issues()
        self.assertEqual([issue.code for issue in issues], ["META001"])

    def test_duplicate_artifact_ids_are_reported(self) -> None:
        self.repository.write_artifact(directory="artifacts/one")
        self.repository.write_artifact(directory="artifacts/two")

        issues = self.issues()
        duplicates = [issue for issue in issues if issue.code == "ID001"]
        self.assertEqual(len(duplicates), 1)
        self.assertIn("artifacts/one/metadata.yaml", duplicates[0].message)

    def test_missing_and_self_parent_references_are_reported(self) -> None:
        self.repository.write_artifact(
            parent_artifacts=["not-present", "test-one"]
        )

        issues = self.issues()
        reference_issues = [issue for issue in issues if issue.code.startswith("REF")]
        self.assertEqual({issue.code for issue in reference_issues}, {"REF001", "REF002"})

    def test_existing_parent_reference_passes(self) -> None:
        self.repository.write_artifact("parent-one", directory="artifacts/parent")
        self.repository.write_artifact(
            "child-one",
            directory="artifacts/child",
            parent_artifacts=["parent-one"],
        )

        self.assertEqual(self.issues(), [])

    def test_missing_prompt_and_content_files_are_reported(self) -> None:
        path = self.repository.write_artifact(create_content=False)
        text = path.read_text(encoding="utf-8").replace(
            "parent_artifacts: []\n",
            "prompt_path: prompts/missing.md\nparent_artifacts: []\n",
        )
        path.write_text(text, encoding="utf-8")

        missing = [issue for issue in self.issues() if issue.code == "REF001"]
        self.assertEqual(len(missing), 2)
        self.assertTrue(any("content.path" in issue.message for issue in missing))
        self.assertTrue(any("prompt_path" in issue.message for issue in missing))

    def test_repository_path_traversal_is_rejected(self) -> None:
        outside = self.repository.base / "outside.md"
        outside.write_bytes(b"outside\n")
        self.repository.write_artifact(
            content=b"outside\n",
            content_path="../outside.md",
            create_content=False,
        )

        issues = self.issues()
        self.assertTrue(
            any(issue.code == "REF001" and "remain in" in issue.message for issue in issues)
        )

    def test_symlink_escape_is_rejected(self) -> None:
        outside = self.repository.base / "outside.md"
        content = b"outside\n"
        outside.write_bytes(content)
        link = self.repository.root / "artifacts" / "test-one" / "raw.md"
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(outside)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlinks unavailable: {error}")
        self.repository.write_artifact(content=content, create_content=False)

        self.assertTrue(any(issue.code == "REF001" for issue in self.issues()))

    def test_checksum_and_byte_count_are_checked_over_raw_bytes(self) -> None:
        content = b"line one\r\nline two\n"
        path = self.repository.write_artifact(content=content)
        text = path.read_text(encoding="utf-8")
        text = text.replace(_sha256(content), "0" * 64)
        text = text.replace(f"byte_count: {len(content)}", "byte_count: 2")
        path.write_text(text, encoding="utf-8")

        codes = [issue.code for issue in self.issues()]
        self.assertIn("CHECKSUM001", codes)
        self.assertIn("CHECKSUM002", codes)

    def test_raw_status_cannot_claim_modified_content(self) -> None:
        self.repository.write_artifact(
            content_modified=True, modifications=["Normalized whitespace."]
        )

        self.assertTrue(any(issue.code == "STATE001" for issue in self.issues()))

    def test_curated_status_requires_a_modification_record(self) -> None:
        self.repository.write_artifact(status="curated")

        self.assertTrue(
            any(
                issue.code == "STATE001" and "curated content" in issue.message
                for issue in self.issues()
            )
        )

    def test_structured_modification_record_is_validated(self) -> None:
        path = self.repository.write_artifact(
            status="curated",
            content_modified=True,
            modifications=["Wrapped the source in documentation markers."],
        )
        self.assertEqual(self.issues(), [])

        text = path.read_text(encoding="utf-8").replace(
            "    source: Test fixture source\n", ""
        )
        path.write_text(text, encoding="utf-8")
        self.assertTrue(
            any(
                issue.code == "SCHEMA001" and ".source" in issue.message
                for issue in self.issues()
            )
        )

    def test_model_facing_artifacts_require_environment_fields(self) -> None:
        path = self.repository.write_artifact(artifact_type="extraction-prompt")
        text = path.read_text(encoding="utf-8").replace("provider: unknown\n", "")
        path.write_text(text, encoding="utf-8")

        self.assertTrue(
            any(
                issue.code == "SCHEMA001" and "provider" in issue.message
                for issue in self.issues()
            )
        )

    def test_lifecycle_events_use_structured_allowed_values(self) -> None:
        path = self.repository.write_artifact()
        text = path.read_text(encoding="utf-8").replace(
            "lifecycle_events: {}\n",
            """\
lifecycle_events:
  correction-2026-07-13:
    occurred_at: "2026-07-13"
    actor: Test fixture
    event_type: metadata-corrected
    description: Corrected a derived byte count.
""",
        )
        path.write_text(text, encoding="utf-8")
        self.assertEqual(self.issues(), [])

        text = text.replace("event_type: metadata-corrected", "event_type: invented")
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any(issue.code == "SCHEMA003" for issue in self.issues()))

    def test_review_flags_require_attribution(self) -> None:
        self.repository.write_artifact(human_reviewed=True)

        issues = self.issues()
        self.assertTrue(any("at least one reviewer" in issue.message for issue in issues))

    def test_evidence_path_must_point_to_governed_metadata(self) -> None:
        ungoverned = self.repository.root / "artifacts" / "ungoverned" / "review.md"
        ungoverned.parent.mkdir(parents=True)
        ungoverned.write_text("Review text.\n", encoding="utf-8")
        self.repository.write_artifact(
            human_reviewed=True,
            reviewers=["Reviewer One"],
            human_review_paths=["artifacts/ungoverned/review.md"],
        )

        self.assertTrue(any(issue.code == "EVIDENCE001" for issue in self.issues()))

    def test_evidence_path_must_have_the_qualifying_artifact_type(self) -> None:
        self.repository.write_artifact(
            "wrong-review-type",
            directory="artifacts/wrong-review",
            artifact_type="test-record",
            parent_artifacts=["test-one"],
        )
        self.repository.write_artifact(
            human_reviewed=True,
            reviewers=["Reviewer One"],
            human_review_paths=["artifacts/wrong-review/metadata.yaml"],
        )

        self.assertTrue(any(issue.code == "EVIDENCE002" for issue in self.issues()))

    def test_evidence_record_must_name_the_subject_as_parent(self) -> None:
        self.repository.write_artifact(
            "unrelated-human-review",
            directory="artifacts/unrelated-review",
            artifact_type="human-review",
        )
        self.repository.write_artifact(
            human_reviewed=True,
            reviewers=["Reviewer One"],
            human_review_paths=["artifacts/unrelated-review/metadata.yaml"],
        )

        self.assertTrue(any(issue.code == "EVIDENCE003" for issue in self.issues()))

    def test_artifact_cannot_use_itself_as_qualifying_evidence(self) -> None:
        self.repository.write_artifact(
            artifact_type="human-review",
            human_reviewed=True,
            reviewers=["Reviewer One"],
            human_review_paths=["artifacts/test-one/metadata.yaml"],
        )

        issues = self.issues()
        self.assertTrue(
            any(
                issue.code == "EVIDENCE001" and "itself" in issue.message
                for issue in issues
            )
        )

    def test_negative_evaluation_and_failed_reproduction_remain_linkable(self) -> None:
        subject_id = "test-one"
        self.repository.write_artifact(
            "mixed-experiment-report",
            directory="artifacts/mixed-report",
            artifact_type="experiment-report",
            claim_class="experimental-result",
            validation_status="mixed",
            parent_artifacts=[subject_id],
        )
        self.repository.write_artifact(
            "inconclusive-reproduction-report",
            directory="artifacts/inconclusive-reproduction",
            artifact_type="reproduction-report",
            claim_class="experimental-result",
            validation_status="inconclusive",
            parent_artifacts=[subject_id],
        )
        self.repository.write_artifact(
            subject_id,
            validation_status="mixed",
            experimentally_validated=False,
            evaluation_paths=["artifacts/mixed-report/metadata.yaml"],
            independently_reproduced=False,
            reproduction_paths=[
                "artifacts/inconclusive-reproduction/metadata.yaml"
            ],
        )

        self.assertEqual(self.issues(), [])

    def test_every_independent_reproduction_claim_requires_another_report(self) -> None:
        for artifact_type in ("experiment-report", "reproduction-report"):
            with self.subTest(artifact_type=artifact_type):
                repository = TemporaryRepository()
                try:
                    repository.write_artifact(
                        artifact_type=artifact_type,
                        claim_class="experimental-result",
                        validation_status="supported",
                        independently_reproduced=True,
                    )
                    issues = validate_repository(repository.root)
                    self.assertTrue(
                        any(
                            issue.code == "STATE001"
                            and "reproduction_path" in issue.message
                            for issue in issues
                        )
                    )
                finally:
                    repository.close()

    def test_claim_class_cannot_overstate_evidence(self) -> None:
        cases = (
            ("experimental-result", "completed test outcome"),
            ("reviewed-recommendation", "requires human or cross-model review"),
            ("verified-finding", "independent reproduction"),
        )
        for index, (claim_class, expected) in enumerate(cases):
            with self.subTest(claim_class=claim_class):
                repository = TemporaryRepository()
                try:
                    repository.write_artifact(
                        artifact_id=f"test-{index}", claim_class=claim_class
                    )
                    issues = validate_repository(repository.root)
                    self.assertTrue(any(expected in issue.message for issue in issues))
                finally:
                    repository.close()

    def test_verified_finding_with_required_evidence_state_passes(self) -> None:
        subject_id = "test-one"
        human_path = "artifacts/human-review/metadata.yaml"
        evaluation_path = "artifacts/evaluation/metadata.yaml"
        reproduction_path = "artifacts/reproduction/metadata.yaml"
        self.repository.write_artifact(
            "human-review-one",
            directory="artifacts/human-review",
            artifact_type="human-review",
            parent_artifacts=[subject_id],
        )
        self.repository.write_artifact(
            "experiment-report-one",
            directory="artifacts/evaluation",
            artifact_type="experiment-report",
            claim_class="experimental-result",
            validation_status="supported",
            parent_artifacts=[subject_id],
        )
        self.repository.write_artifact(
            "reproduction-report-one",
            directory="artifacts/reproduction",
            artifact_type="reproduction-report",
            claim_class="experimental-result",
            validation_status="supported",
            parent_artifacts=[subject_id],
        )
        self.repository.write_artifact(
            subject_id,
            claim_class="verified-finding",
            validation_status="supported",
            human_reviewed=True,
            reviewers=["Reviewer One"],
            human_review_paths=[human_path],
            experimentally_validated=True,
            evaluation_paths=[evaluation_path],
            independently_reproduced=True,
            reproduction_paths=[reproduction_path],
        )

        self.assertEqual(self.issues(), [])

    def test_markdown_links_check_paths_but_skip_external_anchor_and_code(self) -> None:
        self.repository.write_artifact()
        docs = self.repository.root / "docs"
        docs.mkdir()
        (docs / "target.md").write_text("# Target\n", encoding="utf-8")
        (docs / "source.md").write_text(
            """\
[valid](target.md#heading)
[reference][target]
[target]: target.md
[external](https://example.com/missing)
[email](mailto:nobody@example.com)
[anchor](#local)
`[inline code](missing-inline.md)`
```
[fenced code](missing-fenced.md)
```
""",
            encoding="utf-8",
        )

        self.assertEqual(self.issues(), [])

    def test_missing_markdown_link_is_reported(self) -> None:
        self.repository.write_artifact()
        readme = self.repository.root / "README.md"
        readme.write_text("[missing](docs/not-there.md)\n", encoding="utf-8")

        issues = self.issues()
        self.assertTrue(any(issue.code == "LINK001" for issue in issues))

    def test_links_inside_immutable_raw_content_are_not_enforced(self) -> None:
        content = b"[historical broken link](not-in-repository.md)\n"
        self.repository.write_artifact(content=content)

        self.assertEqual(self.issues(), [])


if __name__ == "__main__":
    unittest.main()
