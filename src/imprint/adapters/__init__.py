from imprint.adapters.local_jsonl import LocalJsonlAdapter
from imprint.adapters.local_markdown import LocalMarkdownAdapter
from imprint.adapters.local_text import LocalTextAdapter
from imprint.adapters.local_transcript_json import LocalTranscriptJsonAdapter
from imprint.adapters.protocol import (
    AdapterError,
    ArtifactEnvelope,
    InvalidArtifactPayloadError,
    SourceAdapter,
    SourceNotSupportedError,
    UnknownAdapterError,
)
from imprint.adapters.registry import AdapterRegistry, ArtifactRegistry


def build_default_registry() -> AdapterRegistry:
    return AdapterRegistry(
        adapters=[
            LocalTextAdapter(),
            LocalMarkdownAdapter(),
            LocalJsonlAdapter(),
            LocalTranscriptJsonAdapter(),
        ]
    )


__all__ = [
    "AdapterError",
    "AdapterRegistry",
    "ArtifactEnvelope",
    "ArtifactRegistry",
    "InvalidArtifactPayloadError",
    "LocalJsonlAdapter",
    "LocalMarkdownAdapter",
    "LocalTextAdapter",
    "LocalTranscriptJsonAdapter",
    "SourceAdapter",
    "SourceNotSupportedError",
    "UnknownAdapterError",
    "build_default_registry",
]
