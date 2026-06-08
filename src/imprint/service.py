from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from secrets import compare_digest
from typing import Any

from imprint import __version__
from imprint.consumers import CONSUMER_CONTRACT_SCHEMA_VERSION
from imprint.exports import EXPORT_SCHEMA_VERSION
from imprint.exports.safety import (
    ExportSafetyError,
    assert_public_safe_payload,
    validate_public_safe_string,
)
from imprint.quality import QualityGateError, validate_export_file

LATEST_JSON_EXPORT = "profile.imprint.json"
LATEST_MARKDOWN_EXPORT = "profile.md"


class ServiceError(ValueError):
    pass


class ServiceAuthError(ServiceError):
    pass


class ServiceExportError(ServiceError):
    pass


@dataclass(frozen=True)
class ServiceConfig:
    export_dir: Path
    enabled: bool = False
    bind_host: str = "127.0.0.1"
    external_protection: bool = False
    read_only: bool = True
    jobs_enabled: bool = False
    job_auth_token: str | None = None

    def __post_init__(self) -> None:
        local_hosts = {"127.0.0.1", "localhost", "::1"}
        if self.bind_host not in local_hosts and not self.external_protection:
            raise ServiceError("service bind host must be localhost unless protected externally")
        if self.external_protection and not self.job_auth_token:
            raise ServiceAuthError("externally protected service mode requires an auth token")
        if self.jobs_enabled and not self.job_auth_token:
            raise ServiceAuthError("job endpoints require an auth token when enabled")


def health_payload(config: ServiceConfig) -> dict[str, Any]:
    payload = {
        "service": "imprint",
        "status": "ok" if config.enabled else "disabled",
        "mode": "local_private",
        "read_only": config.read_only,
    }
    _assert_service_payload_safe(payload)
    return payload


def version_payload(config: ServiceConfig | None = None) -> dict[str, Any]:
    if config is not None:
        _require_enabled_for_data(config)
    payload = {
        "service": "imprint",
        "version": __version__,
        "export_schema_version": EXPORT_SCHEMA_VERSION,
        "consumer_contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
    }
    _assert_service_payload_safe(payload)
    return payload


def status_payload(config: ServiceConfig) -> dict[str, Any]:
    _require_enabled_for_data(config)
    export_path = _export_path(config, LATEST_JSON_EXPORT)
    markdown_path = _export_path(config, LATEST_MARKDOWN_EXPORT)
    validation_status = "MISSING"
    warning_count = 0
    profile_signal_count = 0
    included_support_count = 0
    if export_path.exists():
        try:
            report = validate_export_file(export_path)
            validation_status = report["status"]
            if report["status"] == "PASS":
                payload = _load_latest_json_payload(config)
                warnings = payload.get("compatibility", {}).get("warnings", [])
                warning_count = len(warnings)
                profile_signal_count = int(
                    payload.get("source_summary", {}).get("profile_signal_count", 0)
                )
                included_support_count = int(
                    payload.get("source_summary", {}).get("included_support_count", 0)
                )
        except (QualityGateError, ServiceExportError):
            validation_status = "FAIL"
    payload = {
        "service": "imprint",
        "status": "ready" if validation_status == "PASS" else "unavailable",
        "latest_export": LATEST_JSON_EXPORT if export_path.exists() else None,
        "latest_markdown_export": LATEST_MARKDOWN_EXPORT if markdown_path.exists() else None,
        "latest_export_mtime": _mtime(export_path) if export_path.exists() else None,
        "validation_status": validation_status,
        "warning_count": warning_count,
        "profile_signal_count": profile_signal_count,
        "included_support_count": included_support_count,
        "read_only": config.read_only,
        "jobs_enabled": config.jobs_enabled,
    }
    _assert_service_payload_safe(payload)
    return payload


def latest_profile_payload(config: ServiceConfig) -> dict[str, Any]:
    return latest_json_export(config)


def latest_json_export(config: ServiceConfig) -> dict[str, Any]:
    _require_enabled_for_data(config)
    payload = _load_latest_json_payload(config)
    report = validate_export_file(_export_path(config, LATEST_JSON_EXPORT))
    if report["status"] != "PASS":
        raise ServiceExportError("latest export failed validation")
    _assert_service_payload_safe(payload)
    return payload


def latest_markdown_export(config: ServiceConfig) -> str:
    _require_enabled_for_data(config)
    path = _export_path(config, LATEST_MARKDOWN_EXPORT)
    if not path.exists():
        raise ServiceExportError("latest Markdown export is missing")
    content = path.read_text(encoding="utf-8")
    _validate_markdown_export_shape(content)
    validate_public_safe_string(content, path="$markdown")
    return content


def latest_warnings_payload(config: ServiceConfig) -> dict[str, Any]:
    export = latest_json_export(config)
    warnings = list(export.get("compatibility", {}).get("warnings", []))
    limitations = list(export.get("limitations", []))
    payload = {
        "service": "imprint",
        "status": "ok",
        "warnings": warnings,
        "limitations": limitations,
        "warning_count": len(warnings),
    }
    _assert_service_payload_safe(payload)
    return payload


def dry_run_job_payload(config: ServiceConfig, authorization: str | None) -> dict[str, Any]:
    _require_enabled_for_data(config)
    _require_job_auth(config, authorization)
    payload = {
        "service": "imprint",
        "status": "ok",
        "job": "dry_run",
        "would_rebuild": False,
        "status_report": status_payload(config),
    }
    _assert_service_payload_safe(payload)
    return payload


def compare_batch_service_payloads(
    batch_payload: dict[str, Any],
    service_payload: dict[str, Any],
) -> dict[str, Any]:
    batch_normalized = _canonical_json(batch_payload)
    service_normalized = _canonical_json(service_payload)
    matching = batch_normalized == service_normalized
    payload = {
        "service": "imprint",
        "status": "PASS" if matching else "FAIL",
        "canonical_json_equal": matching,
        "build_manifest_equal": batch_payload.get("profile", {}).get("build_manifest")
        == service_payload.get("profile", {}).get("build_manifest"),
        "export_schema_version_equal": batch_payload.get("schema_version")
        == service_payload.get("schema_version"),
        "warning_count_equal": len(batch_payload.get("compatibility", {}).get("warnings", []))
        == len(service_payload.get("compatibility", {}).get("warnings", [])),
    }
    _assert_service_payload_safe(payload)
    return payload


def create_app(config: ServiceConfig) -> Any:
    try:
        from fastapi import Depends, FastAPI, Header, HTTPException
        from fastapi.responses import JSONResponse
        from fastapi.responses import PlainTextResponse
    except ImportError as exc:
        raise ServiceError("FastAPI service requires installing imprint[api]") from exc

    app = FastAPI(title="Imprint Local Service", version=__version__)

    @app.exception_handler(ServiceError)
    def service_error_handler(_request: Any, exc: ServiceError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=_safe_error_payload(exc),
        )

    @app.exception_handler(QualityGateError)
    def quality_error_handler(_request: Any, exc: QualityGateError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=_safe_error_payload(exc),
        )

    def job_auth(authorization: str | None = Header(default=None)) -> None:
        try:
            _require_job_auth(config, authorization)
        except ServiceAuthError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc

    @app.get("/health")
    def health() -> dict[str, Any]:
        return health_payload(config)

    @app.get("/version")
    def version() -> dict[str, Any]:
        return version_payload(config)

    @app.get("/status")
    def status() -> dict[str, Any]:
        return status_payload(config)

    @app.get("/profiles/latest")
    def latest_profile() -> dict[str, Any]:
        return latest_profile_payload(config)

    @app.get("/exports/latest.json")
    def latest_json() -> dict[str, Any]:
        return latest_json_export(config)

    @app.get("/exports/latest.md", response_class=PlainTextResponse)
    def latest_markdown() -> str:
        return latest_markdown_export(config)

    @app.get("/warnings/latest")
    def latest_warnings() -> dict[str, Any]:
        return latest_warnings_payload(config)

    @app.post("/jobs/dry-run")
    def dry_run(_: None = Depends(job_auth)) -> dict[str, Any]:
        return dry_run_job_payload(config, authorization=f"Bearer {config.job_auth_token}")

    return app


def _require_enabled_for_data(config: ServiceConfig) -> None:
    if not config.enabled:
        raise ServiceError("service mode is disabled")


def _require_job_auth(config: ServiceConfig, authorization: str | None) -> None:
    if not config.jobs_enabled:
        raise ServiceAuthError("job endpoints are disabled")
    expected = config.job_auth_token
    if not expected:
        raise ServiceAuthError("job endpoints require auth")
    prefix = "Bearer "
    if not authorization or not authorization.startswith(prefix):
        raise ServiceAuthError("missing bearer token")
    supplied = authorization[len(prefix) :]
    if not compare_digest(supplied, expected):
        raise ServiceAuthError("invalid bearer token")


def _load_latest_json_payload(config: ServiceConfig) -> dict[str, Any]:
    path = _export_path(config, LATEST_JSON_EXPORT)
    if not path.exists():
        raise ServiceExportError("latest export is missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ServiceExportError("latest export is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ServiceExportError("latest export must be a JSON object")
    return payload


def _validate_markdown_export_shape(content: str) -> None:
    required_markers = [
        "# Imprint Profile Summary:",
        "## Basis",
        "## Observed Expression Patterns",
        "## Limitations and Privacy",
        "## Compatibility",
    ]
    missing = [marker for marker in required_markers if marker not in content]
    if missing:
        raise ServiceExportError("latest Markdown export does not match generated profile shape")
    forbidden_markers = {
        "raw_text:",
        "raw_content:",
        "source_path:",
        "filesystem_path:",
        "private_locator:",
        "original_source_id:",
        '"raw_text"',
        '"raw_content"',
        '"source_path"',
        '"filesystem_path"',
        '"private_locator"',
        '"original_source_id"',
    }
    lowered = content.lower()
    if any(marker in lowered for marker in forbidden_markers):
        raise ServiceExportError("latest Markdown export contains raw/private field markers")


def _export_path(config: ServiceConfig, filename: str) -> Path:
    if filename not in {LATEST_JSON_EXPORT, LATEST_MARKDOWN_EXPORT}:
        raise ServiceExportError("unsupported service export")
    base = config.export_dir.resolve()
    candidate = (base / filename).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ServiceExportError("export file escapes configured export directory") from exc
    return candidate


def _mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).isoformat()


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _assert_service_payload_safe(payload: Any) -> None:
    try:
        assert_public_safe_payload(payload)
    except ExportSafetyError as exc:
        raise ServiceExportError(str(exc)) from exc


def _safe_error_payload(exc: Exception) -> dict[str, str]:
    message = str(exc)
    try:
        validate_public_safe_string(message, path="$error.message")
    except ExportSafetyError:
        message = "request failed"
    payload = {
        "service": "imprint",
        "status": "error",
        "error": exc.__class__.__name__,
        "message": message,
    }
    _assert_service_payload_safe(payload)
    return payload
