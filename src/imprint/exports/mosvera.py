from __future__ import annotations

from typing import Any

from imprint.exports.json_export import EXPORT_SCHEMA_VERSION, canonical_profile_export
from imprint.exports.safety import assert_public_safe_payload
from imprint.schemas import ExpressionProfile

MOSVERA_OVERLAY_VERSION = "sprint07-mosvera-overlay-v1"


def mosvera_expression_overlay(profile: ExpressionProfile) -> dict[str, Any]:
    payload = canonical_profile_export(profile)
    expression_summaries = []
    avoid_patterns = []
    for pattern in payload["expression_patterns"]:
        summary = {
            "family": pattern["family"],
            "name": pattern["name"],
            "observed_expression_pattern": pattern["claim"]["text"],
            "confidence": pattern["confidence"]["display"],
            "support_artifact_count": pattern["support"]["included_count"],
            "source_types": pattern["support"]["source_types"],
            "source_ids": pattern["support"]["source_ids"],
        }
        if pattern["family"] == "anti_pattern":
            avoid_patterns.append(summary)
        else:
            expression_summaries.append(summary)
    overlay: dict[str, Any] = {
        "contract": "mosvera_expression_overlay",
        "overlay_version": MOSVERA_OVERLAY_VERSION,
        "export_schema_version": EXPORT_SCHEMA_VERSION,
        "source_profile": {
            "profile_id": payload["profile"]["profile_id"],
            "compiler_version": payload["compatibility"]["compiler_version"],
            "signal_model_versions": payload["compatibility"]["signal_model_versions"],
        },
        "evidence_policy": {
            "raw_text_included": False,
            "source_references": "opaque_source_ids_only",
            "path_references_included": False,
            "private_locators_included": False,
            "generation_controls_included": False,
        },
        "compatibility": _compatibility_policy(payload),
        "expression_summaries": expression_summaries,
        "avoid_patterns": avoid_patterns,
        "boundary": (
            "Imprint compiles expression; Mosvera owns aesthetic intent and runtime behavior."
        ),
    }
    assert_public_safe_payload(overlay)
    return overlay


def _compatibility_policy(payload: dict[str, Any]) -> dict[str, Any]:
    compatibility = payload["compatibility"]
    warnings = list(compatibility.get("warnings", []))
    if payload["profile"].get("artifact_storage", {}).get("mode") == "metadata_only":
        warnings.append("metadata-only audit limitations apply; raw artifact text is not included")
    warnings.append("bounded interpretations are policy-gated and must not be treated as facts")
    warnings.append("confidence summarizes support strength, not identity truth")
    if len(compatibility.get("signal_model_versions", [])) > 1:
        warnings.append("multiple signal model versions are represented across profile patterns")
    return {
        "mandatory_in_consumer_projection": True,
        "compiler_version": compatibility["compiler_version"],
        "classifier_versions": compatibility["classifier_versions"],
        "signal_model_versions": compatibility["signal_model_versions"],
        "schema_version": compatibility["schema_version"],
        "export_schema_version": compatibility["export_schema_version"],
        "warnings": sorted(set(warnings)),
    }
