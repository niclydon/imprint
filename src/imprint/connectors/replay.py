from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any

from imprint.connectors.redaction import redact_value
from imprint.schemas import ArtifactStorageMode

CONNECTOR_REPLAY_MANIFEST_VERSION = "sprint13.5-connector-replay-manifest-v1"


@dataclass(frozen=True)
class ConnectorReplayManifest:
    connector_name: str
    connector_type: str
    connector_version: str
    adapter_version: str
    parser_version: str
    source_policy_version: str
    storage_mode: ArtifactStorageMode | str
    config_hash: str
    synthetic_fixture: bool
    private_fixture: bool = False
    manifest_version: str = CONNECTOR_REPLAY_MANIFEST_VERSION
    replay_limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        storage_mode = (
            self.storage_mode.value
            if hasattr(self.storage_mode, "value")
            else str(self.storage_mode)
        )
        return {
            "manifest_version": self.manifest_version,
            "connector_name": self.connector_name,
            "connector_type": self.connector_type,
            "connector_version": self.connector_version,
            "adapter_version": self.adapter_version,
            "parser_version": self.parser_version,
            "source_policy_version": self.source_policy_version,
            "storage_mode": storage_mode,
            "config_hash": self.config_hash,
            "synthetic_fixture": self.synthetic_fixture,
            "private_fixture": self.private_fixture,
            "replay_limitations": list(self.replay_limitations),
        }

    @property
    def replay_id(self) -> str:
        material = json.dumps(self.to_dict(), sort_keys=True)
        return "replay-" + sha256(material.encode("utf-8")).hexdigest()[:16]


def connector_config_hash(config: dict[str, Any]) -> str:
    sanitized = json.dumps(redact_value(config), sort_keys=True, default=str)
    return sha256(sanitized.encode("utf-8")).hexdigest()


def replay_manifests_compatible(
    baseline: ConnectorReplayManifest,
    candidate: ConnectorReplayManifest,
) -> bool:
    compared_fields = (
        "manifest_version",
        "connector_type",
        "connector_version",
        "adapter_version",
        "parser_version",
        "source_policy_version",
        "storage_mode",
        "config_hash",
        "synthetic_fixture",
        "private_fixture",
    )
    return all(baseline.to_dict()[field] == candidate.to_dict()[field] for field in compared_fields)
