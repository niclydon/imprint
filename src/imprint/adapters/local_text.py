from __future__ import annotations

from pathlib import Path

from imprint.adapters.protocol import ArtifactEnvelope, SourceAdapter
from imprint.schemas import ArtifactType, AuthorshipOrigin


class LocalTextAdapter(SourceAdapter):
    source_type = "local_text"
    suffixes = {".txt"}

    def supports(self, path: Path) -> bool:
        return path.is_dir() or path.suffix.lower() in self.suffixes

    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        artifacts: list[ArtifactEnvelope] = []
        for file_path in self._iter_paths(path):
            artifacts.append(
                ArtifactEnvelope(
                    source_type=self.source_type,
                    source_id=file_path.as_posix(),
                    content=file_path.read_text(encoding="utf-8"),
                    artifact_type=ArtifactType.DOCUMENT,
                    authorship_origin=AuthorshipOrigin.MISSING_METADATA,
                    metadata={"artifact_type_hint": ArtifactType.DOCUMENT.value},
                )
            )
        return artifacts

    def _iter_paths(self, path: Path) -> list[Path]:
        if path.is_file():
            return [path]
        return sorted(candidate for candidate in path.rglob("*") if candidate.suffix.lower() in self.suffixes)
