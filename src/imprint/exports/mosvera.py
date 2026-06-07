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
            "source_references": "opaque_metadata_only",
            "generation_controls_included": False,
        },
        "expression_summaries": expression_summaries,
        "avoid_patterns": avoid_patterns,
        "boundary": (
            "Imprint compiles expression; Mosvera owns aesthetic intent and runtime behavior."
        ),
    }
    assert_public_safe_payload(overlay)
    return overlay
