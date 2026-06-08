from __future__ import annotations

import json
from pathlib import Path

from imprint.adapters.normalization import parse_timestamp
from imprint.adapters.protocol import ArtifactEnvelope, InvalidArtifactPayloadError, SourceAdapter
from imprint.schemas import ArtifactType, AuthorshipOrigin


class LocalTranscriptJsonAdapter(SourceAdapter):
    source_type = "local_transcript_json"
    suffixes = {".json"}

    def supports(self, path: Path) -> bool:
        return path.is_dir() or path.suffix.lower() in self.suffixes

    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        artifacts: list[ArtifactEnvelope] = []
        for file_path in self._iter_paths(path):
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise InvalidArtifactPayloadError(f"transcript payload in {file_path} must be an object")
            segments = payload.get("segments")
            if not isinstance(segments, list):
                raise InvalidArtifactPayloadError(f"transcript payload in {file_path} must define segments")
            for index, segment in enumerate(segments, start=1):
                if not isinstance(segment, dict):
                    raise InvalidArtifactPayloadError(
                        f"transcript segment {index} in {file_path} must be an object"
                    )
                artifacts.append(self._envelope_from_segment(file_path, index, segment))
        return artifacts

    def _iter_paths(self, path: Path) -> list[Path]:
        if path.is_file():
            return [path]
        return sorted(candidate for candidate in path.rglob("*") if candidate.suffix.lower() in self.suffixes)

    def _envelope_from_segment(
        self,
        file_path: Path,
        index: int,
        segment: dict[str, object],
    ) -> ArtifactEnvelope:
        text = segment.get("text")
        if not isinstance(text, str) or not text.strip():
            raise InvalidArtifactPayloadError(
                f"transcript segment {index} in {file_path} is missing text"
            )
        speaker = segment.get("speaker")
        speaker_role = segment.get("speaker_role")
        if speaker is None:
            authorship_origin = AuthorshipOrigin.UNKNOWN_SPEAKER
        elif not isinstance(speaker, str):
            raise InvalidArtifactPayloadError(
                f"transcript segment {index} in {file_path} has invalid speaker"
            )
        elif speaker_role not in {"subject", "other", "unknown"}:
            authorship_origin = AuthorshipOrigin.PARSER_UNCERTAIN
        else:
            authorship_origin = (
                AuthorshipOrigin.HUMAN_ORIGIN
                if speaker_role == "subject"
                else AuthorshipOrigin.UNKNOWN_SPEAKER
            )

        timestamp = parse_timestamp(segment.get("timestamp")) if segment.get("timestamp") is not None else None
        source_id = f"{file_path.as_posix()}#segment:{index}"
        return ArtifactEnvelope(
            source_type=self.source_type,
            source_id=source_id,
            content=text.strip(),
            artifact_type=ArtifactType.TRANSCRIPT_SEGMENT,
            timestamp=timestamp,
            artifact_id_hint=str(segment["artifact_id"]) if isinstance(segment.get("artifact_id"), str) else None,
            authorship_origin=authorship_origin,
            authorship_confidence=0.75 if authorship_origin == AuthorshipOrigin.HUMAN_ORIGIN else 0.4,
            metadata={
                "artifact_type_hint": ArtifactType.TRANSCRIPT_SEGMENT.value,
                "speaker_present": isinstance(speaker, str),
                "speaker_role": speaker_role if isinstance(speaker_role, str) else "unknown",
            },
        )
