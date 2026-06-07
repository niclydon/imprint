from __future__ import annotations

from datetime import UTC, datetime
import hashlib

from imprint.adapters.protocol import ArtifactEnvelope
from imprint.schemas import Artifact, ArtifactClassification, ArtifactReference, ArtifactStoragePolicy


def sha256_text(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def stable_identifier(prefix: str, *parts: str) -> str:
    token = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{token}"


def utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def parse_timestamp(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return utc_datetime(value)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=UTC)
    if isinstance(value, str):
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        return utc_datetime(datetime.fromisoformat(normalized))
    raise ValueError(f"unsupported timestamp type: {type(value).__name__}")


def envelope_to_artifact(
    envelope: ArtifactEnvelope,
    *,
    storage_policy: ArtifactStoragePolicy,
) -> Artifact:
    content_hash = sha256_text(envelope.content)
    artifact_id = envelope.artifact_id_hint or stable_identifier(
        "artifact",
        envelope.source_type,
        envelope.source_id,
        content_hash,
    )
    classification_id = stable_identifier("classification", artifact_id, envelope.source_id)
    timestamp = utc_datetime(envelope.timestamp) if envelope.timestamp else None

    reference = ArtifactReference(
        artifact_id=artifact_id,
        source_id=envelope.source_id,
        artifact_type=envelope.artifact_type,
        source_type=envelope.source_type,
        content_hash=content_hash,
        timestamp=timestamp,
        time_bucket=envelope.time_bucket,
        raw_content_available=storage_policy.raw_content_available,
    )
    classification = ArtifactClassification(
        classification_id=classification_id,
        label=envelope.classification_label,
        authorship_origin=envelope.authorship_origin,
        authorship_confidence=envelope.authorship_confidence,
        reason_categories=[envelope.authorship_origin],
    )
    return Artifact(
        artifact_id=artifact_id,
        reference=reference,
        storage_policy=storage_policy,
        classification=classification,
    )
