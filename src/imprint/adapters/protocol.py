from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from imprint.schemas import (
    Artifact,
    ArtifactClassificationLabel,
    ArtifactStoragePolicy,
    ArtifactType,
    AuthorshipOrigin,
)


@dataclass(frozen=True)
class ArtifactEnvelope:
    """Adapter-local artifact payload before normalization.

    Fields such as authorship/classification/type may reflect upstream source hints.
    Downstream classification must re-assess them before durable profile use.
    """

    source_type: str
    source_id: str
    content: str
    artifact_type: ArtifactType = ArtifactType.DOCUMENT
    timestamp: datetime | None = None
    time_bucket: str | None = None
    artifact_id_hint: str | None = None
    classification_label: ArtifactClassificationLabel = ArtifactClassificationLabel.INCLUDED
    authorship_origin: AuthorshipOrigin = AuthorshipOrigin.MISSING_METADATA
    authorship_confidence: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)


class AdapterError(ValueError):
    """Base class for local adapter errors."""


class UnknownAdapterError(AdapterError):
    """Raised when a source type is not registered."""


class SourceNotSupportedError(AdapterError):
    """Raised when an adapter cannot handle a provided path."""


class InvalidArtifactPayloadError(AdapterError):
    """Raised when a local artifact payload is malformed."""


class SourceAdapter(ABC):
    source_type: str

    @abstractmethod
    def supports(self, path: Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        raise NotImplementedError

    def normalize(
        self,
        envelope: ArtifactEnvelope,
        *,
        storage_policy: ArtifactStoragePolicy | None = None,
    ) -> Artifact:
        from imprint.adapters.normalization import envelope_to_artifact

        return envelope_to_artifact(
            envelope,
            storage_policy=storage_policy or ArtifactStoragePolicy(),
        )

    def ingest(
        self,
        path: Path,
        *,
        storage_policy: ArtifactStoragePolicy | None = None,
    ) -> list[Artifact]:
        if not self.supports(path):
            raise SourceNotSupportedError(
                f"adapter {self.source_type} does not support path: {path}"
            )
        return [
            self.normalize(envelope, storage_policy=storage_policy)
            for envelope in self.discover_artifacts(path)
        ]
