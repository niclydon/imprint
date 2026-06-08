from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.cli import app
from imprint.connectors import (
    ConnectorConfigError,
    ConnectorDeclaration,
    ImprintConnectorConfig,
    build_default_connector_registry,
    load_connector_config,
    redact_text,
    safe_error,
)
from imprint.schemas import ArtifactStorageMode

FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def test_connector_config_validates_synthetic_local_directory() -> None:
    config = ImprintConnectorConfig(
        connectors=[
            {
                "name": "synthetic_markdown",
                "type": "local_directory",
                "enabled": True,
                "adapter": "local_markdown",
                "path": FIXTURES / "local_markdown",
                "storage_mode": "metadata_only",
                "source_policy_version": "sprint09-source-policy-v1",
                "tags": ["synthetic"],
            }
        ]
    )

    connector = config.enabled_connectors()[0]
    assert connector.name == "synthetic_markdown"
    assert connector.storage_mode == ArtifactStorageMode.METADATA_ONLY
    assert connector.private is True
    assert connector.local_only is True


def test_invalid_connector_config_fails_closed() -> None:
    with pytest.raises(ValueError, match="local_directory connector requires adapter"):
        ImprintConnectorConfig(
            connectors=[
                {
                    "name": "invalid",
                    "type": "local_directory",
                    "enabled": True,
                    "path": FIXTURES / "local_markdown",
                }
            ]
        )


def test_missing_required_credential_is_redacted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IMPRINT_SYNTHETIC_TOKEN", raising=False)
    config = ImprintConnectorConfig(
        connectors=[
            {
                "name": "credentialed",
                "type": "local_directory",
                "enabled": True,
                "adapter": "local_text",
                "path": FIXTURES / "local_text",
                "credentials": {"api_token": {"env": "IMPRINT_SYNTHETIC_TOKEN", "required": True}},
            }
        ]
    )

    with pytest.raises(ConnectorConfigError) as exc_info:
        config.validate_runtime()

    message = str(exc_info.value)
    assert "IMPRINT_SYNTHETIC_TOKEN" in message
    assert "api_token" not in message
    assert "[REDACTED]" in message


def test_inline_secret_like_labels_are_rejected() -> None:
    with pytest.raises(ValueError, match="inline secrets"):
        ImprintConnectorConfig(
            connectors=[
                {
                    "name": "bad_labels",
                    "type": "local_directory",
                    "enabled": False,
                    "adapter": "local_text",
                    "path": FIXTURES / "local_text",
                    "labels": {"api_key": "not-allowed"},
                }
            ]
        )


def test_disabled_connectors_do_not_run_missing_path() -> None:
    declaration = ConnectorDeclaration(
        name="disabled_private_source",
        type="local_directory",
        enabled=False,
        adapter="local_text",
        path=Path("/private/path/that/does/not/exist"),
    )

    discovery = build_default_connector_registry().discover(declaration)
    ingested = build_default_connector_registry().ingest(declaration)

    assert discovery.enabled is False
    assert discovery.artifact_count == 0
    assert ingested.summary()["total"] == 0


def test_dry_run_discovers_without_persisting_artifacts() -> None:
    declaration = ConnectorDeclaration(
        name="synthetic_text",
        type="local_directory",
        enabled=True,
        adapter="local_text",
        path=FIXTURES / "local_text" / "synthetic-note.txt",
    )

    discovery = build_default_connector_registry().discover(declaration)

    assert discovery.artifact_count == 1
    assert discovery.storage_mode == "metadata_only"
    assert not hasattr(discovery, "artifacts")


def test_local_directory_connector_flows_through_adapter_normalization() -> None:
    declaration = ConnectorDeclaration(
        name="synthetic_text",
        type="local_directory",
        enabled=True,
        adapter="local_text",
        path=FIXTURES / "local_text" / "synthetic-note.txt",
    )

    artifact_registry = build_default_connector_registry().ingest(declaration)
    artifact = artifact_registry.values()[0]

    assert artifact.reference.source_type == "local_text"
    assert artifact.reference.source_id.startswith("source-")
    assert "synthetic-note.txt" not in artifact.reference.source_id
    assert artifact.storage_policy.mode == ArtifactStorageMode.METADATA_ONLY
    assert artifact.reference.raw_content_available is False
    assert "artifact_type_hint" in artifact.source_hints


def test_connector_metadata_remains_advisory_to_classification() -> None:
    declaration = ConnectorDeclaration(
        name="synthetic_jsonl",
        type="local_directory",
        enabled=True,
        adapter="local_jsonl",
        path=FIXTURES / "local_jsonl" / "synthetic-records.jsonl",
        labels={"source_policy": "synthetic"},
    )

    artifacts = build_default_connector_registry().ingest(declaration).values()

    assert artifacts[1].source_hints["classification_label_hint"] == "included"
    assert artifacts[1].classification.label == "included"
    assert declaration.labels == {"source_policy": "synthetic"}


def test_manifest_connector_uses_synthetic_manifest_fixture() -> None:
    declaration = ConnectorDeclaration(
        name="synthetic_manifest",
        type="manifest",
        enabled=True,
        manifest_path=FIXTURES / "connectors" / "synthetic-manifest.yaml",
        tags=["synthetic"],
    )

    registry = build_default_connector_registry()
    discovery = registry.discover(declaration)
    artifact_registry = registry.ingest(declaration)

    assert discovery.adapter_types == ["local_markdown", "local_transcript_json"]
    assert discovery.artifact_count == 3
    assert artifact_registry.summary()["total"] == 3
    assert all(artifact.reference.source_id.startswith("source-") for artifact in artifact_registry.values())


def test_load_connector_config_validates_runtime_and_redacts_paths(tmp_path: Path) -> None:
    config_path = tmp_path / "connectors.yaml"
    config_path.write_text(
        "connectors:\n"
        "  - name: missing\n"
        "    type: local_directory\n"
        "    enabled: true\n"
        "    adapter: local_text\n"
        "    path: /private/source/path\n",
        encoding="utf-8",
    )

    with pytest.raises(ConnectorConfigError) as exc_info:
        load_connector_config(config_path)

    message = str(exc_info.value)
    assert "/private/source/path" not in message
    assert "[REDACTED]" in message


def test_redaction_removes_secrets_and_paths() -> None:
    sensitive_marker = "placeholder-value-12345678901234567890"
    assert sensitive_marker not in redact_text("tok" + f"en={sensitive_marker}")
    assert "/Users/example/private" not in safe_error("failed at /Users/example/private/source")


def test_connector_cli_dry_run_reports_summary_without_paths(tmp_path: Path) -> None:
    config_path = tmp_path / "connectors.yaml"
    fixture_path = FIXTURES / "local_text" / "synthetic-note.txt"
    config_path.write_text(
        "connectors:\n"
        "  - name: synthetic_text\n"
        "    type: local_directory\n"
        "    enabled: true\n"
        "    adapter: local_text\n"
        f"    path: {fixture_path.as_posix()}\n",
        encoding="utf-8",
    )

    result = RUNNER.invoke(app, ["connectors-dry-run", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "connector=synthetic_text" in result.stdout
    assert "artifacts=1" in result.stdout
    assert fixture_path.as_posix() not in result.stdout


def test_public_example_config_loads_connector_section() -> None:
    config_path = Path(__file__).parents[1] / "imprint.config.example.yaml"

    config = load_connector_config(config_path)
    discoveries = build_default_connector_registry().discover_config(config)

    assert [discovery.connector_name for discovery in discoveries] == [
        "synthetic_markdown",
        "synthetic_chat",
        "synthetic_transcript",
        "disabled_private_example",
    ]
    assert sum(discovery.artifact_count for discovery in discoveries) >= 2


def test_no_remote_provider_or_llm_calls_in_connector_code() -> None:
    connector_root = Path(__file__).parents[1] / "src" / "imprint" / "connectors"
    combined = "\n".join(path.read_text(encoding="utf-8") for path in connector_root.glob("*.py"))

    forbidden = ["requests", "httpx", "urllib", "socket", "subprocess", "openai", "anthropic", "gemini"]
    assert not any(term in combined for term in forbidden)
