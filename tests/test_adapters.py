from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.adapters import (
    InvalidArtifactPayloadError,
    LocalJsonlAdapter,
    LocalMarkdownAdapter,
    LocalTextAdapter,
    LocalTranscriptJsonAdapter,
    UnknownAdapterError,
    build_default_registry,
)
from imprint.cli import app
from imprint.schemas import ArtifactStorageMode, ArtifactType


FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def test_local_text_adapter_normalizes_fixture_file() -> None:
    artifacts = LocalTextAdapter().ingest(FIXTURES / "local_text" / "synthetic-note.txt")

    assert len(artifacts) == 1
    artifact = artifacts[0]
    assert artifact.reference.source_type == "local_text"
    assert artifact.reference.artifact_type == ArtifactType.DOCUMENT
    assert artifact.storage_policy.mode == ArtifactStorageMode.METADATA_ONLY
    assert artifact.reference.raw_content_available is False


def test_local_markdown_adapter_strips_frontmatter_before_hashing() -> None:
    adapter = LocalMarkdownAdapter()
    envelopes = adapter.discover_artifacts(FIXTURES / "local_markdown" / "synthetic-brief.md")

    assert len(envelopes) == 1
    assert "title: Synthetic Brief" not in envelopes[0].content
    artifact = adapter.normalize(envelopes[0])
    assert artifact.reference.source_type == "local_markdown"


def test_local_jsonl_adapter_normalizes_multiple_records() -> None:
    artifacts = LocalJsonlAdapter().ingest(FIXTURES / "local_jsonl" / "synthetic-records.jsonl")

    assert len(artifacts) == 2
    assert artifacts[0].reference.source_type == "local_jsonl"
    assert artifacts[0].reference.timestamp is not None
    assert artifacts[1].reference.artifact_type == ArtifactType.TECHNICAL_NOTE


def test_local_jsonl_adapter_fails_closed_on_invalid_payload() -> None:
    with pytest.raises(InvalidArtifactPayloadError, match="missing text content"):
        LocalJsonlAdapter().ingest(FIXTURES / "local_jsonl" / "invalid-records.jsonl")


def test_local_transcript_json_adapter_maps_segments_to_artifacts() -> None:
    artifacts = LocalTranscriptJsonAdapter().ingest(
        FIXTURES / "local_transcript_json" / "synthetic-transcript.json"
    )

    assert len(artifacts) == 2
    assert all(artifact.reference.artifact_type == ArtifactType.TRANSCRIPT_SEGMENT for artifact in artifacts)
    assert artifacts[0].classification.authorship_origin == "human_origin"
    assert artifacts[1].classification.authorship_origin == "unknown_speaker"


def test_adapter_registry_dispatches_and_summarizes() -> None:
    registry = build_default_registry()
    artifact_registry = registry.ingest(
        "local_text",
        FIXTURES / "local_text",
    )

    assert artifact_registry.summary() == {
        "total": 1,
        "included": 1,
        "excluded": 0,
        "quarantined": 0,
    }


def test_unknown_adapter_raises_clear_error() -> None:
    registry = build_default_registry()

    with pytest.raises(UnknownAdapterError, match="unknown source adapter"):
        registry.get("nexus_db")


def test_cli_ingest_reports_compact_summary() -> None:
    result = RUNNER.invoke(
        app,
        [
            "ingest",
            "--source-type",
            "local_markdown",
            "--path",
            str(FIXTURES / "local_markdown"),
        ],
    )

    assert result.exit_code == 0
    assert "source_type=local_markdown" in result.stdout
    assert "artifacts=1" in result.stdout
