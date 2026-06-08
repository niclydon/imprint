from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.cli import app
from imprint.service import (
    ServiceAuthError,
    ServiceError,
    ServiceExportError,
    ServiceConfig,
    compare_batch_service_payloads,
    create_app,
    dry_run_job_payload,
    health_payload,
    latest_json_export,
    latest_markdown_export,
    latest_profile_payload,
    latest_warnings_payload,
    status_payload,
    version_payload,
)

RUNNER = CliRunner()


def _generate_exports(tmp_path: Path) -> Path:
    output_dir = tmp_path / "exports"
    result = RUNNER.invoke(app, ["example", "--output-dir", str(output_dir)])
    assert result.exit_code == 0
    return output_dir


def test_service_health_version_and_status_are_public_safe(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    assert health_payload(config)["status"] == "ok"
    assert version_payload()["version"] == "0.1.0"

    status = status_payload(config)

    assert status["status"] == "ready"
    assert status["latest_export"] == "profile.imprint.json"
    assert status["latest_markdown_export"] == "profile.md"
    assert status["validation_status"] == "PASS"
    assert str(export_dir) not in json.dumps(status)


def test_disabled_service_mode_blocks_data_endpoints(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=False)

    assert health_payload(config)["status"] == "disabled"

    blocked_calls = [
        lambda: version_payload(config),
        lambda: status_payload(config),
        lambda: latest_profile_payload(config),
        lambda: latest_json_export(config),
        lambda: latest_markdown_export(config),
        lambda: latest_warnings_payload(config),
        lambda: dry_run_job_payload(config, "Bearer synthetic-service-token"),
    ]
    for call in blocked_calls:
        with pytest.raises(ServiceError, match="service mode is disabled"):
            call()


def test_service_returns_latest_public_safe_profile_without_paths_or_raw_text(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    latest = latest_profile_payload(config)
    serialized = json.dumps(latest, sort_keys=True)

    assert latest == latest_json_export(config)
    assert latest["export_type"] == "canonical_json"
    assert "synthetic-demo.json" not in serialized
    assert str(export_dir) not in serialized
    assert "The Queue Underneath" not in serialized
    assert "IMPRINT_PRIVATE_SOURCE_TOKEN" not in serialized


def test_service_returns_markdown_from_generated_export_only(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    markdown = latest_markdown_export(config)

    assert "Observed Expression Patterns" in markdown
    assert "synthetic-demo.json" not in markdown
    assert str(export_dir) not in markdown


def test_service_rejects_markdown_that_is_not_generated_profile_export(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    (export_dir / "profile.md").write_text(
        "# Notes\n\nThis is ordinary prose that should not be served as profile export.\n",
        encoding="utf-8",
    )
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    with pytest.raises(ServiceExportError, match="generated profile shape"):
        latest_markdown_export(config)


def test_service_rejects_markdown_with_raw_private_markers(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    profile_md = export_dir / "profile.md"
    profile_md.write_text(
        profile_md.read_text(encoding="utf-8") + "\nraw_text: copied private message\n",
        encoding="utf-8",
    )
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    with pytest.raises(ServiceExportError, match="raw/private field markers"):
        latest_markdown_export(config)


def test_service_warnings_payload_uses_public_safe_export_metadata(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    warnings = latest_warnings_payload(config)

    assert warnings["status"] == "ok"
    assert warnings["warning_count"] == len(warnings["warnings"])
    assert any("public-safe export excludes raw artifact text" in item for item in warnings["limitations"])


def test_service_dry_run_requires_bearer_auth_and_does_not_rebuild(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(
        export_dir=export_dir,
        enabled=True,
        jobs_enabled=True,
        job_auth_token="synthetic-service-token",
    )

    with pytest.raises(ServiceAuthError, match="missing bearer token"):
        dry_run_job_payload(config, None)
    with pytest.raises(ServiceAuthError, match="invalid bearer token"):
        dry_run_job_payload(config, "Bearer wrong-token")

    result = dry_run_job_payload(config, "Bearer synthetic-service-token")

    assert result["job"] == "dry_run"
    assert result["would_rebuild"] is False
    assert result["status_report"]["validation_status"] == "PASS"


def test_service_jobs_fail_closed_when_not_enabled(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)

    with pytest.raises(ServiceAuthError, match="job endpoints are disabled"):
        dry_run_job_payload(config, "Bearer synthetic-service-token")


def test_service_rejects_non_localhost_bind_without_external_guard(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="localhost"):
        ServiceConfig(export_dir=tmp_path, bind_host="0.0.0.0")


def test_service_allows_external_bind_only_with_explicit_protection_and_auth(tmp_path: Path) -> None:
    with pytest.raises(ServiceAuthError, match="requires an auth token"):
        ServiceConfig(export_dir=tmp_path, bind_host="0.0.0.0", external_protection=True)

    config = ServiceConfig(
        export_dir=tmp_path,
        bind_host="0.0.0.0",
        external_protection=True,
        job_auth_token="synthetic-service-token",
    )

    assert config.external_protection is True


def test_batch_service_payloads_match_cli_generated_export(tmp_path: Path) -> None:
    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=True)
    batch_payload = json.loads((export_dir / "profile.imprint.json").read_text(encoding="utf-8"))

    report = compare_batch_service_payloads(batch_payload, latest_json_export(config))

    assert report["status"] == "PASS"
    assert report["canonical_json_equal"] is True
    assert report["build_manifest_equal"] is True


def test_fastapi_app_returns_bounded_service_error_when_available(tmp_path: Path) -> None:
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    export_dir = _generate_exports(tmp_path)
    config = ServiceConfig(export_dir=export_dir, enabled=False)

    response = TestClient(create_app(config)).get("/status")

    assert response.status_code == 400
    assert response.json() == {
        "service": "imprint",
        "status": "error",
        "error": "ServiceError",
        "message": "service mode is disabled",
    }
