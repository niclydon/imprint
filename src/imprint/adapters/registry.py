from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from imprint.adapters.protocol import SourceAdapter, UnknownAdapterError
from imprint.schemas import Artifact, ArtifactClassificationLabel, ArtifactStoragePolicy


@dataclass
class ArtifactRegistry:
    artifacts: dict[str, Artifact] = field(default_factory=dict)

    def add(self, artifact: Artifact) -> None:
        self.artifacts[artifact.artifact_id] = artifact

    def extend(self, artifacts: list[Artifact]) -> None:
        for artifact in artifacts:
            self.add(artifact)

    def values(self) -> list[Artifact]:
        return list(self.artifacts.values())

    def summary(self) -> dict[str, int]:
        counts = {
            "total": len(self.artifacts),
            "included": 0,
            "excluded": 0,
            "quarantined": 0,
        }
        for artifact in self.artifacts.values():
            label = ArtifactClassificationLabel(artifact.classification.label)
            counts[label.value] += 1
        return counts


class AdapterRegistry:
    def __init__(self, adapters: list[SourceAdapter] | None = None):
        self._adapters: dict[str, SourceAdapter] = {}
        for adapter in adapters or []:
            self.register(adapter)

    def register(self, adapter: SourceAdapter) -> None:
        self._adapters[adapter.source_type] = adapter

    def get(self, source_type: str) -> SourceAdapter:
        if source_type not in self._adapters:
            raise UnknownAdapterError(f"unknown source adapter: {source_type}")
        return self._adapters[source_type]

    def source_types(self) -> list[str]:
        return sorted(self._adapters)

    def ingest(
        self,
        source_type: str,
        path: Path,
        *,
        storage_policy: ArtifactStoragePolicy | None = None,
    ) -> ArtifactRegistry:
        adapter = self.get(source_type)
        registry = ArtifactRegistry()
        registry.extend(adapter.ingest(path, storage_policy=storage_policy))
        return registry
