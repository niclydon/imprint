from __future__ import annotations

import base64
import re
from typing import Any
from urllib.parse import unquote

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

MAX_DECODED_STRING_BYTES = 4096
MIN_ENCODED_STRING_LENGTH = 16

CREDENTIAL_PATTERN = re.compile(
    r"(?:"
    r"sk-[A-Za-z0-9]{20,}|"
    r"ghp_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"BEGIN (?:RSA|OPENSSH|EC|PRIVATE) KEY|"
    r"[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s:@]+@"
    r")"
)
JWT_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"([A-Za-z0-9_-]{10,})\.([A-Za-z0-9_-]{10,})\.([A-Za-z0-9_-]{8,})"
    r"(?![A-Za-z0-9_-])"
)
PATH_PATTERN = re.compile(r"(?:^/|^[A-Za-z]:[\\/]|(?:^|[\\/])\.\.(?:[\\/]|$)|[/\\][^\s]+[/\\])")
ENCODED_PATH_SEPARATOR_PATTERN = re.compile(r"%(?:2[fF]|5[cC])")
BASE64_CANDIDATE_PATTERN = re.compile(r"[A-Za-z0-9+/_=-]+")
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
    _validate_no_private_metadata_keys(payload)
    _validate_no_forbidden_keys(payload)
    _validate_no_unsafe_strings(payload)


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
    validate_public_safe_string(source_id, path="$source_id")


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
        _validate_no_unsafe_strings(context.source_filters)
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


def _validate_no_private_metadata_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_path = f"{path}.{key}"
            if key.startswith("_"):
                raise ExportSafetyError(f"export contains private metadata field: {key_path}")
            _validate_no_private_metadata_keys(item, key_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_no_private_metadata_keys(item, f"{path}[{index}]")


def _validate_no_unsafe_strings(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _validate_no_unsafe_strings(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_no_unsafe_strings(item, f"{path}[{index}]")
    elif isinstance(value, str):
        validate_public_safe_string(value, path=path)


def validate_public_safe_string(value: str, *, path: str = "$") -> None:
    if CREDENTIAL_PATTERN.search(value) or _contains_jwt(value):
        raise ExportSafetyError(f"credential-like value is not allowed at {path}")
    if _contains_path(value):
        raise ExportSafetyError(f"path-like value is not allowed at {path}")
    for decoded in _bounded_decoded_strings(value):
        if CREDENTIAL_PATTERN.search(decoded) or _contains_jwt(decoded):
            raise ExportSafetyError(f"encoded credential-like value is not allowed at {path}")
        if _contains_path(decoded):
            raise ExportSafetyError(f"encoded path-like value is not allowed at {path}")


def _contains_path(value: str) -> bool:
    if PATH_PATTERN.search(value) or ENCODED_PATH_SEPARATOR_PATTERN.search(value):
        return True
    if "%" in value:
        decoded = unquote(value)
        return decoded != value and PATH_PATTERN.search(decoded) is not None
    return False


def _contains_jwt(value: str) -> bool:
    for match in JWT_PATTERN.finditer(value):
        header, payload, _signature = match.groups()
        if _base64url_json_object(header) and _base64url_json_object(payload):
            return True
    return False


def _base64url_json_object(value: str) -> bool:
    try:
        decoded = _decode_base64(value, urlsafe=True)
    except ValueError:
        return False
    stripped = decoded.strip()
    return stripped.startswith("{") and stripped.endswith("}")


def _bounded_decoded_strings(value: str) -> list[str]:
    if len(value) < MIN_ENCODED_STRING_LENGTH or len(value) > MAX_DECODED_STRING_BYTES:
        return []
    if not BASE64_CANDIDATE_PATTERN.fullmatch(value):
        return []
    decoded: list[str] = []
    for urlsafe in (False, True):
        try:
            candidate = _decode_base64(value, urlsafe=urlsafe)
        except ValueError:
            continue
        if candidate != value and _is_printable_text(candidate):
            decoded.append(candidate)
    return list(dict.fromkeys(decoded))


def _decode_base64(value: str, *, urlsafe: bool) -> str:
    padding = "=" * (-len(value) % 4)
    candidate = value + padding
    decoder = base64.urlsafe_b64decode if urlsafe else base64.b64decode
    try:
        decoded = decoder(candidate)
    except Exception as exc:
        raise ValueError("invalid base64") from exc
    if len(decoded) > MAX_DECODED_STRING_BYTES:
        raise ValueError("decoded string too large")
    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("decoded string is not utf-8") from exc


def _is_printable_text(value: str) -> bool:
    if not value:
        return False
    printable = sum(character.isprintable() or character in "\r\n\t" for character in value)
    return printable / len(value) >= 0.9
