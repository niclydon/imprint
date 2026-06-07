from __future__ import annotations

from typing import Any, Literal

from imprint.exports.json_export import EXPORT_SCHEMA_VERSION, canonical_profile_export
from imprint.exports.safety import assert_public_safe_payload
from imprint.schemas import ExpressionProfile

CONSUMER_CONTRACT_SCHEMA_VERSION = "sprint08-consumer-contract-v1"
ConsumerName = Literal["mosvera", "broadside", "agent", "human_cli"]


def consumer_contract(profile: ExpressionProfile, consumer: ConsumerName) -> dict[str, Any]:
    payload = canonical_profile_export(profile)
    if consumer == "mosvera":
        contract = mosvera_consumer_contract_from_canonical(payload)
    elif consumer == "broadside":
        contract = broadside_consumer_contract_from_canonical(payload)
    elif consumer == "agent":
        contract = agent_consumer_contract_from_canonical(payload)
    elif consumer == "human_cli":
        contract = human_cli_consumer_contract_from_canonical(payload)
    else:
        raise ValueError(f"unsupported consumer contract: {consumer}")
    validate_consumer_payload(contract)
    return contract


def validate_consumer_payload(payload: dict[str, Any]) -> None:
    assert_public_safe_payload(payload)
    _reject_generation_control_values(payload)


def compatibility_policy(canonical_payload: dict[str, Any]) -> dict[str, Any]:
    compatibility = canonical_payload["compatibility"]
    warnings = list(compatibility.get("warnings", []))
    if _has_metadata_only_audit_limitation(canonical_payload):
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
        "consumer_contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
        "warnings": sorted(set(warnings)),
    }


def mosvera_consumer_contract(profile: ExpressionProfile) -> dict[str, Any]:
    return consumer_contract(profile, "mosvera")


def broadside_consumer_contract(profile: ExpressionProfile) -> dict[str, Any]:
    return consumer_contract(profile, "broadside")


def agent_consumer_contract(profile: ExpressionProfile) -> dict[str, Any]:
    return consumer_contract(profile, "agent")


def human_cli_consumer_contract(profile: ExpressionProfile) -> dict[str, Any]:
    return consumer_contract(profile, "human_cli")


def mosvera_consumer_contract_from_canonical(payload: dict[str, Any]) -> dict[str, Any]:
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
    return {
        "contract": "mosvera_consumer_contract",
        "contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
        "source_profile": _source_profile(payload),
        "evidence_policy": _evidence_policy(),
        "compatibility": compatibility_policy(payload),
        "expression_summaries": expression_summaries,
        "avoid_patterns": avoid_patterns,
        "boundary": "Imprint compiles expression; Mosvera owns aesthetic intent and runtime behavior.",
    }


def broadside_consumer_contract_from_canonical(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract": "broadside_consumer_contract",
        "contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
        "source_profile": _source_profile(payload),
        "evidence_policy": _evidence_policy(),
        "compatibility": compatibility_policy(payload),
        "profile_summary": {
            "profile_signal_count": payload["source_summary"]["profile_signal_count"],
            "included_support_count": payload["source_summary"]["included_support_count"],
            "source_types": payload["source_summary"]["source_types"],
        },
        "observed_expression_patterns": [_constraint_summary(pattern) for pattern in payload["expression_patterns"]],
        "limitations": payload["limitations"],
        "boundary": "Imprint supplies supported expression constraints; Broadside owns publication decisions.",
    }


def agent_consumer_contract_from_canonical(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract": "agent_consumer_contract",
        "contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
        "source_profile": _source_profile(payload),
        "evidence_policy": _evidence_policy(),
        "compatibility": compatibility_policy(payload),
        "safe_pattern_lookup": {
            pattern["signal_id"]: _constraint_summary(pattern)
            for pattern in payload["expression_patterns"]
        },
        "usage_rules": [
            "validate canonical JSON before using this projection",
            "surface compatibility warnings before applying profile constraints",
            "do not treat confidence as truth",
            "do not treat bounded interpretations as facts",
            "do not use non-durable or quarantined support as durable evidence",
        ],
    }


def human_cli_consumer_contract_from_canonical(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract": "human_cli_consumer_contract",
        "contract_schema_version": CONSUMER_CONTRACT_SCHEMA_VERSION,
        "source_profile": _source_profile(payload),
        "evidence_policy": _evidence_policy(),
        "compatibility": compatibility_policy(payload),
        "display_sections": [
            "profile summary",
            "observed expression patterns",
            "limitations",
            "compatibility warnings",
        ],
        "limitations": payload["limitations"],
    }


def _source_profile(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "profile_id": payload["profile"]["profile_id"],
        "subject_id": payload["profile"]["subject_id"],
        "canonical_export_id": payload["export_id"],
        "canonical_export_schema_version": EXPORT_SCHEMA_VERSION,
    }


def _evidence_policy() -> dict[str, Any]:
    return {
        "raw_text_included": False,
        "source_references": "opaque_source_ids_only",
        "path_references_included": False,
        "private_locators_included": False,
        "generation_controls_included": False,
    }


def _constraint_summary(pattern: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": pattern["signal_id"],
        "family": pattern["family"],
        "name": pattern["name"],
        "observed_expression_pattern": pattern["claim"]["text"],
        "claim_level": pattern["claim"]["level"],
        "confidence": pattern["confidence"]["display"],
        "support": {
            "included_count": pattern["support"]["included_count"],
            "source_types": pattern["support"]["source_types"],
            "source_ids": pattern["support"]["source_ids"],
            "audit_limitations": pattern["support"]["audit_limitations"],
            "limitations": pattern["support"]["limitations"],
        },
    }


def _has_metadata_only_audit_limitation(payload: dict[str, Any]) -> bool:
    limitations = payload.get("limitations", [])
    if any("raw_content_unavailable" in limitation for limitation in limitations):
        return True
    storage = payload["profile"].get("artifact_storage", {})
    return storage.get("mode") == "metadata_only"


def _reject_generation_control_values(value: Any) -> None:
    forbidden_terms = (
        "system prompt",
        "provider-specific prompt",
        "image generation instruction",
        "publishing workflow",
        "editorial workflow",
        "temperature",
        "model hint",
    )
    if isinstance(value, dict):
        for item in value.values():
            _reject_generation_control_values(item)
    elif isinstance(value, list):
        for item in value:
            _reject_generation_control_values(item)
    elif isinstance(value, str):
        lowered = value.lower()
        if any(term in lowered for term in forbidden_terms):
            raise ValueError(f"consumer payload contains downstream control language: {value}")
