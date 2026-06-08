from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ConsentClass(StrEnum):
    OWNER_AUTHORED = "owner_authored"
    THIRD_PARTY_AUTHORED = "third_party_authored"
    MIXED = "mixed"
    UNKNOWN = "unknown"
    SYSTEM_GENERATED = "system_generated"


class ConsentAction(StrEnum):
    ALLOW = "allow"
    EXCLUDE = "exclude"
    QUARANTINE = "quarantine"


@dataclass(frozen=True)
class ConsentBoundaryResult:
    consent_class: ConsentClass
    action: ConsentAction
    reason_codes: list[str] = field(default_factory=list)
    explanation: str = ""

    @property
    def allows_durable_support(self) -> bool:
        return self.action == ConsentAction.ALLOW


@dataclass(frozen=True)
class ConsentBoundary:
    source_family: str
    allow_classes: frozenset[ConsentClass] = frozenset({ConsentClass.OWNER_AUTHORED})
    exclude_classes: frozenset[ConsentClass] = frozenset(
        {ConsentClass.THIRD_PARTY_AUTHORED, ConsentClass.SYSTEM_GENERATED}
    )

    def evaluate(self, hints: dict[str, Any]) -> ConsentBoundaryResult:
        consent_class = consent_class_from_hints(hints)
        if consent_class in self.allow_classes:
            return ConsentBoundaryResult(
                consent_class=consent_class,
                action=ConsentAction.ALLOW,
                reason_codes=["consent_owner_authored"],
                explanation="Source hints identify subject-authored content.",
            )
        if consent_class in self.exclude_classes:
            return ConsentBoundaryResult(
                consent_class=consent_class,
                action=ConsentAction.EXCLUDE,
                reason_codes=[f"consent_{consent_class.value}"],
                explanation="Source hints identify non-subject or generated content.",
            )
        return ConsentBoundaryResult(
            consent_class=consent_class,
            action=ConsentAction.QUARANTINE,
            reason_codes=[f"consent_{consent_class.value}"],
            explanation="Source hints do not prove subject-authored content.",
        )


SOURCE_CONSENT_BOUNDARIES = {
    "gmail": ConsentBoundary(source_family="gmail"),
    "sent_mail": ConsentBoundary(source_family="gmail"),
    "imessage": ConsentBoundary(source_family="imessage"),
    "chat": ConsentBoundary(source_family="imessage"),
    "transcript": ConsentBoundary(source_family="transcript"),
    "database": ConsentBoundary(source_family="database"),
}
PRIVATE_SOURCE_FAMILY_MARKERS = frozenset(SOURCE_CONSENT_BOUNDARIES)

CONSENT_HINT_KEYS = {
    "consent_class",
    "source_family",
    "source_role",
    "participant_role",
    "speaker_role",
    "system_generated",
    "message_role",
    "group_chat",
    "mixed_speakers",
}


def consent_class_from_hints(hints: dict[str, Any]) -> ConsentClass:
    explicit = hints.get("consent_class")
    if isinstance(explicit, ConsentClass):
        return explicit
    if isinstance(explicit, str):
        try:
            return ConsentClass(explicit)
        except ValueError:
            return ConsentClass.UNKNOWN

    if hints.get("system_generated") is True or hints.get("message_role") == "system":
        return ConsentClass.SYSTEM_GENERATED
    if hints.get("source_role") in {"received", "third_party", "other_participant"}:
        return ConsentClass.THIRD_PARTY_AUTHORED
    if hints.get("participant_role") in {"other", "group_other", "third_party"}:
        return ConsentClass.THIRD_PARTY_AUTHORED
    if hints.get("speaker_role") in {"other", "third_party"}:
        return ConsentClass.THIRD_PARTY_AUTHORED
    if hints.get("contains_quote_marker") or hints.get("contains_forward_marker"):
        return ConsentClass.MIXED
    if hints.get("group_chat") is True or hints.get("mixed_speakers") is True:
        return ConsentClass.MIXED
    if hints.get("source_role") in {"sent", "subject", "owner"}:
        return ConsentClass.OWNER_AUTHORED
    if hints.get("participant_role") in {"subject", "owner"}:
        return ConsentClass.OWNER_AUTHORED
    if hints.get("speaker_role") in {"subject", "owner"}:
        return ConsentClass.OWNER_AUTHORED
    return ConsentClass.UNKNOWN


def consent_boundary_for_hints(source_type: str, hints: dict[str, Any]) -> ConsentBoundary:
    source_family = hints.get("source_family")
    if isinstance(source_family, str) and source_family in SOURCE_CONSENT_BOUNDARIES:
        return SOURCE_CONSENT_BOUNDARIES[source_family]
    for marker, boundary in SOURCE_CONSENT_BOUNDARIES.items():
        if marker in source_type:
            return boundary
    return ConsentBoundary(source_family=source_type)


def evaluate_consent_boundary(source_type: str, hints: dict[str, Any]) -> ConsentBoundaryResult:
    if not CONSENT_HINT_KEYS.intersection(hints):
        if any(marker in source_type for marker in PRIVATE_SOURCE_FAMILY_MARKERS):
            return ConsentBoundaryResult(
                consent_class=ConsentClass.UNKNOWN,
                action=ConsentAction.QUARANTINE,
                reason_codes=["consent_missing_private_source_hints"],
                explanation="Private-source connector did not provide consent boundary hints.",
            )
        return ConsentBoundaryResult(
            consent_class=ConsentClass.OWNER_AUTHORED,
            action=ConsentAction.ALLOW,
            reason_codes=["consent_not_declared_legacy_local_source"],
            explanation="Legacy local adapter source has no private connector consent boundary.",
        )
    return consent_boundary_for_hints(source_type, hints).evaluate(hints)
