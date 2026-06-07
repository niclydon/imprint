from __future__ import annotations

from pathlib import Path
import re

from imprint.adapters.protocol import ArtifactEnvelope, SourceAdapter
from imprint.schemas import ArtifactType, AuthorshipOrigin


FRONTMATTER_PATTERN = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


class LocalMarkdownAdapter(SourceAdapter):
    source_type = "local_markdown"
    suffixes = {".md", ".markdown"}

    def supports(self, path: Path) -> bool:
        return path.is_dir() or path.suffix.lower() in self.suffixes

    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        artifacts: list[ArtifactEnvelope] = []
        for file_path in self._iter_paths(path):
            raw = file_path.read_text(encoding="utf-8")
            artifacts.append(
                ArtifactEnvelope(
                    source_type=self.source_type,
                    source_id=file_path.as_posix(),
                    content=self._normalize_markdown(raw),
                    artifact_type=ArtifactType.DOCUMENT,
                    authorship_origin=AuthorshipOrigin.MISSING_METADATA,
                )
            )
        return artifacts

    def _iter_paths(self, path: Path) -> list[Path]:
        if path.is_file():
            return [path]
        return sorted(candidate for candidate in path.rglob("*") if candidate.suffix.lower() in self.suffixes)

    def _normalize_markdown(self, raw: str) -> str:
        without_frontmatter = FRONTMATTER_PATTERN.sub("", raw, count=1)
        return without_frontmatter.strip()
