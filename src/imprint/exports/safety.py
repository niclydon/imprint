from __future__ import annotations

import re
from typing import Any

from imprint.schemas import ClaimLevel, ExpressionProfile, Signal, SignalSupport

FORBIDDEN_EXPORT_KEYS = {
    "prompt",
    "system_prompt",
    "instruction",
    "temperature",
    "decoding",
    "model_hint",
    "provider",
    "top_p",
    "frequency_penalty",
    "presence_penalty",
}

PATH_PATTERN = re.compile(r"(?:^/|^[A-Za-z]:[\\/]|\.\.|[/\\][^\s]+[/\\])")
SOURCE_ID_PATTERN = re.compile(r"^source-[A-Za-z0-9_-]+$")


class ExportSafetyError(ValueError):
    pass


def validate_public_export_profile(
    profile: ExpressionProfile,
    *,
    allow_bounded_interpretations: bool = False,
) -> None:
    _validate_no_prohibited_or_ungated_bounded(profile, allow_bounded_interpretations)
    _validate_signal_support(profile.signals)
    _validate_context_filters(profile)
    _validate_no_forbidden_keys(profile.model_dump(mode="json"))


def assert_public_safe_payload(payload: Any) -> None:
    _validate_no_forbidden_keys(payload)
    _validate_no_path_strings(payload)


def opaque_source_ids(support: SignalSupport) -> list[str]:
    source_ids = sorted(
        {evidence.artifact_ref.source_id for evidence in support.evidence_refs}
    )
    for source_id in source_ids:
        validate_opaque_source_id(source_id)
    return source_ids


def validate_opaque_source_id(source_id: str) -> None:
    if not SOURCE_ID_PATTERN.match(source_id):
        raise ExportSafetyError(f"source ID is not public-safe opaque metadata: {source_id}")
    if PATH_PATTERN.search(source_id):
        raise ExportSafetyError(f"source ID contains path-like data: {source_id}")


def _validate_no_prohibited_or_ungated_bounded(
    profile: ExpressionProfile,
    allow_bounded_interpretations: bool,
) -> None:
    claims = [*profile.claims, *(signal.claim for signal in profile.signals)]
    for claim in claims:
        if claim.level == ClaimLevel.PROHIBITED:
            raise ExportSafetyError(f"prohibited claim cannot export: {claim.claim_id}")
        if claim.level == ClaimLevel.QUARANTINED:
            raise ExportSafetyError(f"quarantined claim cannot export: {claim.claim_id}")
        if claim.level == ClaimLevel.BOUNDED_INTERPRETATION and not allow_bounded_interpretations:
            raise ExportSafetyError(
                f"bounded interpretation is not export-enabled: {claim.claim_id}"
            )


def _validate_signal_support(signals: list[Signal]) -> None:
    for signal in signals:
        support = signal.support
        if support.quarantined_count or support.excluded_count:
            raise ExportSafetyError(
                f"non-durable support cannot export as durable evidence: {signal.signal_id}"
            )
        if len(set(support.signal_model_versions)) > 1:
            raise ExportSafetyError(
                f"mixed signal model versions cannot export: {signal.signal_id}"
            )
        for source_id in opaque_source_ids(support):
            validate_opaque_source_id(source_id)


def _validate_context_filters(profile: ExpressionProfile) -> None:
    for context in profile.context_profiles:
        _validate_no_path_strings(context.source_filters)
        _validate_no_forbidden_keys(context.source_filters)


def _validate_no_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        forbidden = FORBIDDEN_EXPORT_KEYS.intersection(value)
        if forbidden:
            raise ExportSafetyError(
                f"export contains generation-control fields: {sorted(forbidden)}"
            )
        for item in value.values():
            _validate_no_forbidden_keys(item)
    elif isinstance(value, list):
        for item in value:
            _validate_no_forbidden_keys(item)


def _validate_no_path_strings(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _validate_no_path_strings(item)
    elif isinstance(value, list):
        for item in value:
            _validate_no_path_strings(item)
    elif isinstance(value, str) and PATH_PATTERN.search(value):
        raise ExportSafetyError(f"export contains path-like data: {value}")
