from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.cli import app
from imprint.connectors import (
    ConnectorAuditLog,
    ConnectorConfigError,
    ConnectorDeclaration,
    ConnectorReplayManifest,
    ImprintConnectorConfig,
    build_default_connector_registry,
    connector_config_hash,
    load_connector_config,
    redact_text,
    replay_manifests_compatible,
    safe_error,
    scan_fixture_path,
    scan_fixture_tree,
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


def test_redaction_covers_real_world_credential_shapes() -> None:
    jwt_value = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJzdWJqZWN0IiwiaWF0IjoxNzAwMDAwMDAwfQ."
        "c2lnbmF0dXJl"
    )
    aws_key = "A" "KIA" + "ABCDEFGHIJKLMNOP"
    dsn = "postgres://subject:synthetic-password@example.com:5432/imprint"
    url_key = "https://example.com/callback?api_key=" + "syntheticapikeyvalue123"
    azure = (
        "DefaultEndpointsProtocol=https;AccountName=synthetic;"
        "AccountKey=syntheticaccountkeyvalue123;EndpointSuffix=core.windows.net"
    )
    refresh = "refresh_token=" + "syntheticrefreshtokenvalue123"
    basic = "Basic " + "c3ludGhldGljOnNlY3JldA=="
    bearer = "Bearer " + "syntheticbearertokenvalue123"

    sensitive_values = [jwt_value, aws_key, dsn, url_key, azure, refresh, basic, bearer]
    redacted = redact_text(" ".join(sensitive_values))

    for value in sensitive_values:
        assert value not in redacted
    assert redacted.count("[REDACTED]") >= len(sensitive_values)


def test_safe_error_redacts_nested_env_values_but_preserves_env_var_names() -> None:
    message = safe_error(
        "credential failure",
        {
            "env": "IMPRINT_SYNTHETIC_TOKEN",
            "nested": {"env": {"API_TOKEN": "syntheticapikeyvalue123"}},
        },
    )

    assert "IMPRINT_SYNTHETIC_TOKEN" in message
    assert "syntheticapikeyvalue123" not in message
    assert "API_TOKEN" not in message


def test_connector_replay_manifest_detects_version_incompatibility() -> None:
    baseline = ConnectorReplayManifest(
        connector_name="synthetic_gmail",
        connector_type="gmail",
        connector_version="sprint13.5-connector-v1",
        adapter_version="synthetic-adapter-v1",
        parser_version="parser-v1",
        source_policy_version="source-policy-v1",
        storage_mode=ArtifactStorageMode.METADATA_ONLY,
        config_hash=connector_config_hash({"mode": "sent-only"}),
        synthetic_fixture=True,
    )
    candidate = ConnectorReplayManifest(
        connector_name="synthetic_gmail",
        connector_type="gmail",
        connector_version="sprint13.5-connector-v1",
        adapter_version="synthetic-adapter-v1",
        parser_version="parser-v2",
        source_policy_version="source-policy-v1",
        storage_mode=ArtifactStorageMode.METADATA_ONLY,
        config_hash=connector_config_hash({"mode": "sent-only"}),
        synthetic_fixture=True,
    )

    assert baseline.replay_id.startswith("replay-")
    assert replay_manifests_compatible(baseline, baseline) is True
    assert replay_manifests_compatible(baseline, candidate) is False


def test_connector_replay_manifest_detects_manifest_version_drift() -> None:
    baseline = ConnectorReplayManifest(
        connector_name="synthetic_gmail",
        connector_type="gmail",
        connector_version="sprint13.5-connector-v1",
        adapter_version="synthetic-adapter-v1",
        parser_version="parser-v1",
        source_policy_version="source-policy-v1",
        storage_mode=ArtifactStorageMode.METADATA_ONLY,
        config_hash=connector_config_hash({"mode": "sent-only"}),
        synthetic_fixture=True,
    )
    candidate = ConnectorReplayManifest(
        connector_name="synthetic_gmail",
        connector_type="gmail",
        connector_version="sprint13.5-connector-v1",
        adapter_version="synthetic-adapter-v1",
        parser_version="parser-v1",
        source_policy_version="source-policy-v1",
        storage_mode=ArtifactStorageMode.METADATA_ONLY,
        config_hash=connector_config_hash({"mode": "sent-only"}),
        synthetic_fixture=True,
        manifest_version="future-replay-manifest-v2",
    )

    assert replay_manifests_compatible(baseline, candidate) is False


def test_connector_config_hash_redacts_secret_values_before_hashing() -> None:
    plain = connector_config_hash({"credential": "[REDACTED]", "path": "[REDACTED]"})
    sensitive = connector_config_hash(
        {
            "credential": "syntheticapikeyvalue123",
            "path": "/Users/example/private/source",
        }
    )

    assert sensitive == plain


def test_connector_audit_log_redacts_errors_and_references_replay_manifest() -> None:
    manifest = ConnectorReplayManifest(
        connector_name="synthetic_database",
        connector_type="database",
        connector_version="sprint13.5-connector-v1",
        adapter_version="synthetic-adapter-v1",
        parser_version="parser-v1",
        source_policy_version="source-policy-v1",
        storage_mode=ArtifactStorageMode.METADATA_ONLY,
        config_hash=connector_config_hash({"query": "synthetic_subject_rows"}),
        synthetic_fixture=True,
    )
    log = ConnectorAuditLog(
        connector_run_id="run-synthetic-database",
        connector_name="synthetic_database",
        connector_type="database",
        source_policy_version="source-policy-v1",
        discovered_count=4,
        included_count=1,
        excluded_count=2,
        quarantined_count=1,
        storage_mode="metadata_only",
        replay_manifest=manifest,
        warnings=["synthetic warning"],
        errors=["failed with postgres://subject:synthetic-password@example.com:5432/imprint"],
        metadata={"api_key": "syntheticapikeyvalue123", "path": "/Users/example/private/source"},
    )

    payload = log.to_public_safe_dict()
    serialized = str(payload)

    assert payload["replay_manifest_ref"] == manifest.replay_id
    assert payload["counts"] == {"discovered": 4, "included": 1, "excluded": 2, "quarantined": 1}
    assert payload["warnings"] == ["warning-1"]
    assert payload["errors"] == ["error-1"]
    assert "synthetic-password" not in serialized
    assert "syntheticapikeyvalue123" not in serialized
    assert "/Users/example/private/source" not in serialized


def test_connector_audit_log_does_not_emit_ordinary_raw_text_metadata() -> None:
    log = ConnectorAuditLog(
        connector_run_id="run-synthetic",
        connector_name="synthetic",
        connector_type="gmail",
        source_policy_version="source-policy-v1",
        discovered_count=1,
        included_count=0,
        excluded_count=1,
        quarantined_count=0,
        storage_mode="metadata_only",
        warnings=["ordinary raw message sentence should not appear"],
        errors=["ordinary raw error text should not appear"],
        metadata={"raw_text": "ordinary raw body should not appear", "connector_version": "v1"},
    )

    payload = log.to_public_safe_dict()
    serialized = str(payload)

    assert "ordinary raw" not in serialized
    assert payload["metadata"] == {"connector_version": "v1"}


def test_fixture_leakage_scanner_flags_private_fixture_content(tmp_path: Path) -> None:
    unsafe = tmp_path / "mail-export.jsonl"
    unsafe.write_text(
        "email=person@private-company.test phone=415-555-1212 "
        "dsn=postgres://subject:synthetic-password@example.com:5432/imprint",
        encoding="utf-8",
    )

    reasons = {finding.reason_code for finding in scan_fixture_path(unsafe)}

    assert "fixture_name_not_synthetic" in reasons
    assert "real_email" in reasons
    assert "phone_number" in reasons
    assert "dsn" in reasons


def test_fixture_leakage_scanner_flags_encoded_private_content(tmp_path: Path) -> None:
    import base64

    unsafe = tmp_path / "synthetic-private-fixture.json"
    key_name = "api" + "_key"
    encoded_secret = base64.b64encode(f"{key_name}=syntheticapikeyvalue123".encode()).decode()
    encoded_path = base64.b64encode(b"/Users/example/private/source").decode()
    unsafe.write_text(f"{encoded_secret}\n{encoded_path}\n", encoding="utf-8")

    reasons = {finding.reason_code for finding in scan_fixture_path(unsafe)}

    assert "encoded_credential_or_token" in reasons
    assert "encoded_local_home_path" in reasons


def test_current_public_fixture_content_has_no_private_leakage_patterns() -> None:
    findings = []
    for root in (FIXTURES, Path(__file__).parents[1] / "examples" / "synthetic_corpus"):
        findings.extend(scan_fixture_tree(root, require_synthetic_name=False))

    assert findings == []


def test_public_narratives_do_not_expose_private_handoff_paths() -> None:
    narrative_root = Path(__file__).parents[1] / "docs" / "narrative"
    combined = "\n".join(path.read_text(encoding="utf-8") for path in narrative_root.glob("*.md"))

    forbidden = [
        "/Users/niclydon",
        "smb://",
        "10.10.0.1",
        "projects/nexus",
        "Netflix export",
        "Anvil",
    ]
    assert not any(term in combined for term in forbidden)


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
    combined = "\n".join(path.read_text(encoding="utf-8") for path in connector_root.rglob("*.py"))

    forbidden = ["requests", "httpx", "urllib", "socket", "subprocess", "openai", "anthropic", "gemini"]
    assert not any(term in combined for term in forbidden)


def test_connector_code_does_not_import_pipeline_authority() -> None:
    connector_root = Path(__file__).parents[1] / "src" / "imprint" / "connectors"
    combined = "\n".join(path.read_text(encoding="utf-8") for path in connector_root.rglob("*.py"))

    forbidden = [
        "from imprint.classification",
        "import imprint.classification",
        "from imprint.signals",
        "import imprint.signals",
        "from imprint.compiler",
        "import imprint.compiler",
        "from imprint.exports",
        "import imprint.exports",
        "canonical_profile",
        "ProfileCompiler",
        "RuleBasedArtifactClassifier",
        "RuleBasedSignalExtractor",
    ]
    assert not any(term in combined for term in forbidden)
