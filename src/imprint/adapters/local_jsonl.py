from __future__ import annotations

import json
from pathlib import Path

from imprint.adapters.normalization import parse_timestamp
from imprint.adapters.protocol import ArtifactEnvelope, InvalidArtifactPayloadError, SourceAdapter
from imprint.schemas import (
    ArtifactClassificationLabel,
    ArtifactType,
    AuthorshipOrigin,
)


TEXT_KEYS = ("text", "content", "body")


class LocalJsonlAdapter(SourceAdapter):
    source_type = "local_jsonl"
    suffixes = {".jsonl"}

    def supports(self, path: Path) -> bool:
        return path.is_dir() or path.suffix.lower() in self.suffixes

    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        artifacts: list[ArtifactEnvelope] = []
        for file_path in self._iter_paths(path):
            for line_number, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
                if not raw_line.strip():
                    continue
                try:
                    payload = json.loads(raw_line)
                except json.JSONDecodeError as exc:
                    raise InvalidArtifactPayloadError(
                        f"invalid jsonl in {file_path} line {line_number}: {exc.msg}"
                    ) from exc
                if not isinstance(payload, dict):
                    raise InvalidArtifactPayloadError(
                        f"jsonl payload in {file_path} line {line_number} must be an object"
                    )
                artifacts.append(self._envelope_from_payload(file_path, line_number, payload))
        return artifacts

    def _iter_paths(self, path: Path) -> list[Path]:
        if path.is_file():
            return [path]
        return sorted(candidate for candidate in path.rglob("*") if candidate.suffix.lower() in self.suffixes)

    def _envelope_from_payload(
        self,
        file_path: Path,
        line_number: int,
        payload: dict[str, object],
    ) -> ArtifactEnvelope:
        content = next((payload[key] for key in TEXT_KEYS if payload.get(key)), None)
        if not isinstance(content, str) or not content.strip():
            raise InvalidArtifactPayloadError(
                f"jsonl payload in {file_path} line {line_number} is missing text content"
            )

        timestamp = parse_timestamp(payload.get("timestamp")) if payload.get("timestamp") is not None else None

        source_id = str(payload.get("source_id") or f"{file_path.as_posix()}#line:{line_number}")
        artifact_id_hint = (
            str(payload["artifact_id"]) if isinstance(payload.get("artifact_id"), str) else None
        )
        authorship_confidence = payload.get("authorship_confidence", 0.6)
        if not isinstance(authorship_confidence, (int, float)):
            raise InvalidArtifactPayloadError(
                f"jsonl payload in {file_path} line {line_number} has invalid authorship_confidence"
            )

        return ArtifactEnvelope(
            source_type=self.source_type,
            source_id=source_id,
            content=content.strip(),
            artifact_type=ArtifactType.DOCUMENT,
            timestamp=timestamp,
            artifact_id_hint=artifact_id_hint,
            classification_label=ArtifactClassificationLabel.INCLUDED,
            authorship_origin=AuthorshipOrigin.MISSING_METADATA,
            authorship_confidence=0.5,
            metadata=self._hint_metadata(payload, float(authorship_confidence)),
        )

    def _artifact_type(self, value: object) -> ArtifactType:
        if value is None:
            return ArtifactType.DOCUMENT
        try:
            return ArtifactType(str(value))
        except ValueError as exc:
            raise InvalidArtifactPayloadError(f"unsupported artifact_type: {value}") from exc

    def _authorship_origin(self, value: object) -> AuthorshipOrigin:
        if value is None:
            return AuthorshipOrigin.MISSING_METADATA
        try:
            return AuthorshipOrigin(str(value))
        except ValueError as exc:
            raise InvalidArtifactPayloadError(f"unsupported authorship_origin: {value}") from exc

    def _classification_label(self, value: object) -> ArtifactClassificationLabel:
        if value is None:
            return ArtifactClassificationLabel.INCLUDED
        try:
            return ArtifactClassificationLabel(str(value))
        except ValueError as exc:
            raise InvalidArtifactPayloadError(f"unsupported classification_label: {value}") from exc

    def _hint_metadata(
        self,
        payload: dict[str, object],
        authorship_confidence: float,
    ) -> dict[str, object]:
        metadata: dict[str, object] = {}
        if payload.get("artifact_type") is not None:
            metadata["artifact_type_hint"] = self._artifact_type(payload.get("artifact_type")).value
        if payload.get("authorship_origin") is not None:
            metadata["authorship_origin_hint"] = self._authorship_origin(payload.get("authorship_origin")).value
            metadata["authorship_confidence_hint"] = authorship_confidence
        if payload.get("classification_label") is not None:
            metadata["classification_label_hint"] = self._classification_label(
                payload.get("classification_label")
            ).value
        return metadata
