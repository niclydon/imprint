from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from imprint.consumers import validate_consumer_payload
from imprint.exports import EXPORT_SCHEMA_VERSION
from imprint.exports.safety import (
    ExportSafetyError,
    assert_public_safe_payload,
    validate_public_safe_string,
    validate_opaque_source_id,
)
from imprint.schemas import (
    ArtifactStoragePolicy,
    BuildManifest,
    ComparabilityResult,
    DriftKind,
    SourcePolicy,
)

VALIDATION_REPORT_VERSION = "sprint12-validation-report-v1"
COMPARISON_REPORT_VERSION = "sprint12-comparison-report-v1"

RAW_CONTENT_KEYS = {
    "raw_text",
    "raw_content",
    "content",
    "body",
    "source_path",
    "filesystem_path",
    "private_locator",
    "original_source_id",
}
CANONICAL_EXPORT_TYPES = {"canonical_json"}
CONSUMER_CONTRACTS = {
    "mosvera_consumer_contract",
    "broadside_consumer_contract",
    "agent_consumer_contract",
    "human_cli_consumer_contract",
}
OVERLAY_CONTRACTS = {"mosvera_expression_overlay"}


class QualityGateError(ValueError):
    pass


def validate_export_file(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    report = _base_validation_report(path)
    checks: list[dict[str, Any]] = []

    _record(checks, "json_parse", True)
    _validate_payload_privacy(payload, checks)
    _validate_export_shape(payload, checks)

    failed = [check for check in checks if check["status"] == "FAIL"]
    warnings = [check["message"] for check in checks if check["status"] == "WARN"]
    reason_codes = sorted({check["reason_code"] for check in failed})
    report.update(
        {
            "status": "FAIL" if failed else "PASS",
            "checks": checks,
            "warnings": warnings,
            "release_gate": {
                "status": "FAIL" if failed else "PASS",
                "blocking_failures": [check["name"] for check in failed],
                "required_reviews": [],
                "reason_codes": reason_codes,
            },
        }
    )
    return report


def compare_export_files(baseline_path: Path, candidate_path: Path) -> dict[str, Any]:
    baseline = _canonical_payload(_load_json(baseline_path), baseline_path)
    candidate = _canonical_payload(_load_json(candidate_path), candidate_path)

    baseline_manifest = BuildManifest.model_validate(baseline["profile"]["build_manifest"])
    candidate_manifest = BuildManifest.model_validate(candidate["profile"]["build_manifest"])
    compatible_corpus = _corpus_fingerprint(baseline) == _corpus_fingerprint(candidate)
    comparability = ComparabilityResult.from_manifests(
        baseline_manifest,
        candidate_manifest,
        compatible_corpus=compatible_corpus,
    )
    changes = _profile_changes(baseline, candidate)
    drift_kinds = _drift_kinds(
        baseline_manifest,
        candidate_manifest,
        compatible_corpus=compatible_corpus,
        has_signal_changes=bool(changes["signals"]["changed_signal_ids"]),
        comparability_label=str(comparability.label),
    )
    warnings = _comparison_warnings(comparability, drift_kinds)
    version_metadata = _comparison_version_metadata(baseline, candidate)
    required_reviews = _required_comparison_reviews(comparability, version_metadata)
    release_status = "PASS" if not required_reviews else "WARN"

    return {
        "report_version": COMPARISON_REPORT_VERSION,
        "status": "PASS",
        "baseline": {
            "path": baseline_path.name,
            "export_id": baseline["export_id"],
            "profile_id": baseline["profile"]["profile_id"],
        },
        "candidate": {
            "path": candidate_path.name,
            "export_id": candidate["export_id"],
            "profile_id": candidate["profile"]["profile_id"],
        },
        "comparability": {
            **comparability.model_dump(mode="json"),
            "state": str(comparability.label).upper(),
            "version_metadata": version_metadata,
        },
        "drift": {
            "kinds": [str(kind) for kind in drift_kinds],
            "expression_drift_reported": DriftKind.EXPRESSION_DRIFT in drift_kinds,
            "implementation_drift_reported_as_expression": False,
        },
        "changes": changes,
        "warnings": warnings,
        "release_gate": {
            "status": release_status,
            "required_reviews": required_reviews,
            "reason_codes": required_reviews,
            "blocking_failures": [],
            "summary": (
                "comparison is release-reviewable"
                if release_status == "PASS"
                else "comparison requires release review before drift claims"
            ),
        },
    }


def _base_validation_report(path: Path) -> dict[str, Any]:
    return {
        "report_version": VALIDATION_REPORT_VERSION,
        "file": path.name,
        "status": "FAIL",
        "checks": [],
        "warnings": [],
        "release_gate": {"status": "FAIL", "blocking_failures": []},
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualityGateError(f"could not read JSON export: {exc}") from exc
    if not isinstance(payload, dict):
        raise QualityGateError("export payload must be a JSON object")
    return payload


def _canonical_payload(payload: dict[str, Any], path: Path) -> dict[str, Any]:
    if payload.get("export_type") != "canonical_json":
        raise QualityGateError(f"{path.name} is not a canonical JSON profile export")
    report = validate_export_file(path)
    if report["status"] != "PASS":
        raise QualityGateError(f"{path.name} failed validation")
    return payload


def _validate_payload_privacy(payload: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    try:
        assert_public_safe_payload(payload)
        _walk_privacy(payload)
    except (ExportSafetyError, QualityGateError) as exc:
        _record(checks, "privacy", False, str(exc))
        return
    _record(checks, "privacy", True)


def _validate_export_shape(payload: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    export_type = payload.get("export_type")
    contract = payload.get("contract")
    if export_type in CANONICAL_EXPORT_TYPES:
        _validate_canonical_export(payload, checks)
        return
    if contract in CONSUMER_CONTRACTS:
        _validate_consumer_contract(payload, checks)
        return
    if contract in OVERLAY_CONTRACTS:
        _validate_overlay_contract(payload, checks)
        return
    _record(checks, "schema", False, "unsupported export or consumer contract shape")


def _validate_canonical_export(payload: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    required = {"export_id", "export_type", "schema_version", "mode", "profile", "source_summary", "expression_patterns", "compatibility", "limitations"}
    missing = sorted(required - set(payload))
    if missing:
        _record(checks, "schema", False, f"missing canonical fields: {missing}")
        return
    try:
        BuildManifest.model_validate(payload["profile"]["build_manifest"])
        ArtifactStoragePolicy.model_validate(payload["profile"]["artifact_storage"])
        SourcePolicy.model_validate(payload["profile"]["source_policy"])
    except (KeyError, TypeError, ValidationError) as exc:
        _record(checks, "schema", False, f"profile metadata failed schema validation: {exc}")
        return
    _record(checks, "schema", True)

    if payload["schema_version"] != EXPORT_SCHEMA_VERSION:
        _record(
            checks,
            "export_version",
            False,
            f"expected {EXPORT_SCHEMA_VERSION}, got {payload['schema_version']}",
        )
    else:
        _record(checks, "export_version", True)
    _validate_compatibility(payload.get("compatibility"), checks, require_warnings=False)
    _validate_expression_patterns(payload["expression_patterns"], checks)


def _validate_consumer_contract(payload: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    try:
        validate_consumer_payload(payload)
    except (ExportSafetyError, ValueError) as exc:
        _record(checks, "consumer_contract", False, str(exc))
        return
    _record(checks, "consumer_contract", True)
    _validate_evidence_policy(payload.get("evidence_policy"), checks)
    _validate_compatibility(payload.get("compatibility"), checks, require_warnings=True)


def _validate_overlay_contract(payload: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    required = {"overlay_version", "export_schema_version", "source_profile", "evidence_policy", "compatibility"}
    missing = sorted(required - set(payload))
    if missing:
        _record(checks, "overlay_contract", False, f"missing overlay fields: {missing}")
        return
    _record(checks, "overlay_contract", True)
    _validate_evidence_policy(payload.get("evidence_policy"), checks)
    _validate_compatibility(payload.get("compatibility"), checks, require_warnings=True)


def _validate_expression_patterns(patterns: Any, checks: list[dict[str, Any]]) -> None:
    if not isinstance(patterns, list):
        _record(checks, "source_ids", False, "expression_patterns must be a list")
        return
    try:
        for pattern in patterns:
            if pattern.get("claim", {}).get("level") in {"prohibited", "quarantined"}:
                raise QualityGateError("prohibited or quarantined claim appeared in export")
            for source_id in pattern.get("support", {}).get("source_ids", []):
                validate_opaque_source_id(source_id)
    except (AttributeError, ExportSafetyError, QualityGateError) as exc:
        _record(checks, "source_ids", False, str(exc))
        return
    _record(checks, "source_ids", True)


def _validate_evidence_policy(policy: Any, checks: list[dict[str, Any]]) -> None:
    if not isinstance(policy, dict):
        _record(checks, "evidence_policy", False, "missing evidence policy")
        return
    failures = []
    if policy.get("raw_text_included") is not False:
        failures.append("raw_text_included must be false")
    if policy.get("path_references_included") is not False:
        failures.append("path_references_included must be false")
    if policy.get("private_locators_included") is not False:
        failures.append("private_locators_included must be false")
    if policy.get("generation_controls_included") is not False:
        failures.append("generation_controls_included must be false")
    if failures:
        _record(checks, "evidence_policy", False, "; ".join(failures))
    else:
        _record(checks, "evidence_policy", True)


def _validate_compatibility(
    compatibility: Any,
    checks: list[dict[str, Any]],
    *,
    require_warnings: bool,
) -> None:
    if not isinstance(compatibility, dict):
        _record(checks, "compatibility", False, "missing compatibility metadata")
        return
    required = {"compiler_version", "classifier_versions", "signal_model_versions", "schema_version", "export_schema_version", "warnings"}
    missing = sorted(required - set(compatibility))
    if missing:
        _record(checks, "compatibility", False, f"missing compatibility fields: {missing}")
        return
    if require_warnings and not compatibility.get("warnings"):
        _record(checks, "compatibility", False, "mandatory compatibility warnings are missing")
        return
    if compatibility.get("export_schema_version") != EXPORT_SCHEMA_VERSION:
        _record(checks, "compatibility", False, "compatibility export schema version mismatch")
        return
    _record(checks, "compatibility", True)


def _walk_privacy(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in RAW_CONTENT_KEYS:
                raise QualityGateError(f"raw/private content field is not allowed: {path}.{key}")
            _walk_privacy(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _walk_privacy(item, f"{path}[{index}]")
    elif isinstance(value, str):
        try:
            validate_public_safe_string(value, path=path)
        except ExportSafetyError as exc:
            raise QualityGateError(str(exc)) from exc


def _profile_changes(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    baseline_patterns = _pattern_map(baseline)
    candidate_patterns = _pattern_map(candidate)
    baseline_ids = set(baseline_patterns)
    candidate_ids = set(candidate_patterns)
    common_ids = baseline_ids & candidate_ids
    changed_ids = sorted(
        signal_id
        for signal_id in common_ids
        if baseline_patterns[signal_id] != candidate_patterns[signal_id]
    )
    return {
        "metadata": {
            "compiler_version_changed": baseline["compatibility"]["compiler_version"] != candidate["compatibility"]["compiler_version"],
            "classifier_versions_changed": baseline["compatibility"]["classifier_versions"] != candidate["compatibility"]["classifier_versions"],
            "signal_model_versions_changed": baseline["compatibility"]["signal_model_versions"] != candidate["compatibility"]["signal_model_versions"],
            "schema_version_changed": baseline["compatibility"]["schema_version"] != candidate["compatibility"]["schema_version"],
            "export_schema_version_changed": baseline["compatibility"]["export_schema_version"] != candidate["compatibility"]["export_schema_version"],
        },
        "support": {
            "included_support_count_delta": candidate["source_summary"]["included_support_count"] - baseline["source_summary"]["included_support_count"],
            "profile_signal_count_delta": candidate["source_summary"]["profile_signal_count"] - baseline["source_summary"]["profile_signal_count"],
        },
        "signals": {
            "added_signal_ids": sorted(candidate_ids - baseline_ids),
            "removed_signal_ids": sorted(baseline_ids - candidate_ids),
            "changed_signal_ids": changed_ids,
        },
        "compatibility_warnings": {
            "baseline": baseline["compatibility"].get("warnings", []),
            "candidate": candidate["compatibility"].get("warnings", []),
        },
    }


def _pattern_map(payload: dict[str, Any]) -> dict[str, str]:
    patterns = {}
    for pattern in payload.get("expression_patterns", []):
        material = {
            "family": pattern.get("family"),
            "name": pattern.get("name"),
            "claim": pattern.get("claim"),
            "confidence": pattern.get("confidence"),
            "support": pattern.get("support"),
        }
        patterns[pattern["signal_id"]] = sha256(
            json.dumps(material, sort_keys=True).encode("utf-8")
        ).hexdigest()
    return patterns


def _corpus_fingerprint(payload: dict[str, Any]) -> str:
    manifest = payload["profile"]["build_manifest"]
    source_summary = payload["source_summary"].get("source_types", {})
    material = {
        "config_hash": manifest.get("config_hash"),
        "artifact_store_mode": manifest.get("artifact_store_mode"),
        "source_summary": source_summary,
    }
    return sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def _drift_kinds(
    baseline: BuildManifest,
    candidate: BuildManifest,
    *,
    compatible_corpus: bool,
    has_signal_changes: bool,
    comparability_label: str,
) -> list[DriftKind]:
    kinds: list[DriftKind] = []
    if (
        baseline.schema_family != candidate.schema_family
        or baseline.schema_version != candidate.schema_version
        or baseline.export_schema_version != candidate.export_schema_version
    ):
        kinds.append(DriftKind.SCHEMA_DRIFT)
    if (
        baseline.compiler_version != candidate.compiler_version
        or baseline.classifier_version != candidate.classifier_version
        or baseline.extractor_family != candidate.extractor_family
        or baseline.extractor_major_version != candidate.extractor_major_version
        or baseline.extractor_minor_version != candidate.extractor_minor_version
        or baseline.extractor_code_version != candidate.extractor_code_version
        or baseline.extractor_prompt_version != candidate.extractor_prompt_version
    ):
        kinds.append(DriftKind.COMPILER_DRIFT)
    if not compatible_corpus or baseline.source_policy_version != candidate.source_policy_version:
        kinds.append(DriftKind.CORPUS_DRIFT)
    if has_signal_changes and comparability_label != "not_comparable":
        kinds.append(DriftKind.EXPRESSION_DRIFT)
    return list(dict.fromkeys(kinds))


def _comparison_version_metadata(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    baseline_classifier_versions = _version_list(
        baseline["compatibility"].get("classifier_versions", [])
    )
    candidate_classifier_versions = _version_list(
        candidate["compatibility"].get("classifier_versions", [])
    )
    baseline_signal_versions = _version_list(
        baseline["compatibility"].get("signal_model_versions", [])
    )
    candidate_signal_versions = _version_list(
        candidate["compatibility"].get("signal_model_versions", [])
    )
    return {
        "baseline_classifier_versions": baseline_classifier_versions,
        "candidate_classifier_versions": candidate_classifier_versions,
        "baseline_signal_model_versions": baseline_signal_versions,
        "candidate_signal_model_versions": candidate_signal_versions,
        "mixed_classifier_versions": (
            len(baseline_classifier_versions) > 1 or len(candidate_classifier_versions) > 1
        ),
        "mixed_signal_model_versions": (
            len(baseline_signal_versions) > 1 or len(candidate_signal_versions) > 1
        ),
    }


def _required_comparison_reviews(
    comparability: ComparabilityResult,
    version_metadata: dict[str, Any],
) -> list[str]:
    reviews: list[str] = []
    if str(comparability.label) == "not_comparable":
        reviews.append("not_comparable")
    elif str(comparability.label) == "partially_comparable":
        reviews.append("partially_comparable")
    if version_metadata["mixed_classifier_versions"]:
        reviews.append("mixed_classifier_versions")
    if version_metadata["mixed_signal_model_versions"]:
        reviews.append("mixed_signal_model_versions")
    return list(dict.fromkeys(reviews))


def _version_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return sorted({str(item) for item in value if str(item)})
    if isinstance(value, str) and value:
        return sorted({item.strip() for item in value.split(",") if item.strip()})
    return []


def _comparison_warnings(
    comparability: ComparabilityResult,
    drift_kinds: list[DriftKind],
) -> list[str]:
    warnings = []
    if str(comparability.label) == "not_comparable":
        warnings.append("not-comparable profiles must not be presented as expression drift")
    if DriftKind.COMPILER_DRIFT in drift_kinds:
        warnings.append("compiler/classifier/signal-version drift is implementation drift")
    if DriftKind.CORPUS_DRIFT in drift_kinds:
        warnings.append("corpus drift changes evidence basis")
    if DriftKind.SCHEMA_DRIFT in drift_kinds:
        warnings.append("schema/export drift changes representation")
    return warnings


def _record(
    checks: list[dict[str, Any]],
    name: str,
    passed: bool,
    message: str | None = None,
    reason_code: str | None = None,
) -> None:
    checks.append(
        {
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "message": message or ("ok" if passed else "failed"),
            "reason_code": reason_code or name,
        }
    )
