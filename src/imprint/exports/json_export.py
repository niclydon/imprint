from __future__ import annotations

import json
from hashlib import sha256
from typing import Any

from imprint.exports.safety import (
    assert_public_safe_payload,
    opaque_source_ids,
    validate_public_export_profile,
)
from imprint.schemas import ExportMode, ExpressionProfile, Signal

EXPORT_SCHEMA_VERSION = "sprint07-export-v1"


def canonical_profile_export(
    profile: ExpressionProfile,
    *,
    mode: ExportMode = ExportMode.PUBLIC_SAFE,
    allow_bounded_interpretations: bool = False,
) -> dict[str, Any]:
    validate_public_export_profile(
        profile,
        allow_bounded_interpretations=allow_bounded_interpretations,
    )
    patterns = [_pattern_summary(signal) for signal in profile.signals]
    payload: dict[str, Any] = {
        "export_id": _export_id(profile, "canonical-json"),
        "export_type": "canonical_json",
        "schema_version": EXPORT_SCHEMA_VERSION,
        "mode": mode.value if hasattr(mode, "value") else str(mode),
        "profile": {
            "profile_id": profile.profile_id,
            "subject_id": profile.subject_id,
            "build_manifest": profile.build_manifest.model_dump(mode="json"),
            "artifact_storage": profile.artifact_storage.model_dump(mode="json"),
            "source_policy": profile.source_policy.model_dump(mode="json"),
        },
        "source_summary": _source_summary(profile),
        "expression_patterns": patterns,
        "context_profiles": [_context_summary(context) for context in profile.context_profiles],
        "compatibility": _compatibility_summary(profile),
        "limitations": _limitations(profile),
    }
    assert_public_safe_payload(payload)
    return payload


def canonical_profile_json(profile: ExpressionProfile) -> str:
    return json.dumps(canonical_profile_export(profile), indent=2, sort_keys=True) + "\n"


def _pattern_summary(signal: Signal) -> dict[str, Any]:
    support = signal.support
    return {
        "signal_id": signal.signal_id,
        "family": signal.family,
        "name": signal.name,
        "claim": {
            "claim_id": signal.claim.claim_id,
            "level": signal.claim.level,
            "text": signal.claim.text,
            "validation": signal.claim.validation.model_dump(mode="json"),
        },
        "confidence": signal.claim.confidence.model_dump(mode="json"),
        "support": {
            "artifact_count": support.artifact_count,
            "included_count": support.included_count,
            "excluded_count": support.excluded_count,
            "quarantined_count": support.quarantined_count,
            "source_types": sorted(support.source_types),
            "source_ids": opaque_source_ids(support),
            "classification_model_versions": sorted(support.classification_model_versions),
            "signal_model_versions": sorted(support.signal_model_versions),
            "rule_ids": sorted(support.rule_ids),
            "audit_limitations": sorted(str(item) for item in support.audit_limitations),
            "limitations": sorted(support.limitations),
            "raw_content_available": support.raw_content_available,
        },
    }


def _source_summary(profile: ExpressionProfile) -> dict[str, Any]:
    source_types: dict[str, dict[str, int]] = {}
    for context in profile.context_profiles:
        source_type = context.source_filters.get("source_type", context.context_label)
        source_types[str(source_type)] = {
            "included_count": context.included_count,
            "excluded_count": context.excluded_count,
            "quarantined_count": context.quarantined_count,
        }
    included = sum(signal.support.included_count for signal in profile.signals)
    return {
        "profile_signal_count": len(profile.signals),
        "claim_count": len(profile.claims),
        "included_support_count": included,
        "source_types": dict(sorted(source_types.items())),
    }


def _context_summary(context: Any) -> dict[str, Any]:
    return {
        "profile_id": context.profile_id,
        "baseline_profile_id": context.baseline_profile_id,
        "context_label": context.context_label,
        "source_filters": context.source_filters,
        "artifact_type_filters": context.artifact_type_filters,
        "included_count": context.included_count,
        "excluded_count": context.excluded_count,
        "quarantined_count": context.quarantined_count,
        "compilation_strategy": context.compilation_strategy,
        "divergence_count": len(context.divergences),
    }


def _compatibility_summary(profile: ExpressionProfile) -> dict[str, Any]:
    classifier_versions = sorted(
        {
            version
            for signal in profile.signals
            for version in signal.support.classification_model_versions
        }
    )
    signal_versions = sorted(
        {
            version
            for signal in profile.signals
            for version in signal.support.signal_model_versions
        }
    )
    warnings: list[str] = []
    if len(classifier_versions) > 1:
        warnings.append("multiple classifier versions are represented in support metadata")
    return {
        "compiler_version": profile.build_manifest.compiler_version,
        "classifier_versions": classifier_versions,
        "signal_model_versions": signal_versions,
        "schema_version": profile.build_manifest.schema_version,
        "export_schema_version": EXPORT_SCHEMA_VERSION,
        "warnings": warnings,
    }


def _limitations(profile: ExpressionProfile) -> list[str]:
    limitations = {
        "public-safe export excludes raw artifact text and filesystem paths",
        "confidence summarizes support strength, not truth about a person",
    }
    for signal in profile.signals:
        limitations.update(signal.support.limitations)
        limitations.update(str(item) for item in signal.support.audit_limitations)
    return sorted(limitations)


def _export_id(profile: ExpressionProfile, export_type: str) -> str:
    export_material = f"{profile.profile_id}:{export_type}:{EXPORT_SCHEMA_VERSION}"
    digest = sha256(export_material.encode()).hexdigest()
    return f"export-{export_type}-{digest[:12]}"
