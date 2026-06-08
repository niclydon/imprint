from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from imprint.connectors.redaction import redact_value
from imprint.connectors.replay import ConnectorReplayManifest

CONNECTOR_AUDIT_LOG_VERSION = "sprint13.5-connector-audit-log-v1"


@dataclass(frozen=True)
class ConnectorAuditLog:
    connector_run_id: str
    connector_name: str
    connector_type: str
    source_policy_version: str
    discovered_count: int
    included_count: int
    excluded_count: int
    quarantined_count: int
    storage_mode: str
    replay_manifest: ConnectorReplayManifest | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    log_version: str = CONNECTOR_AUDIT_LOG_VERSION

    def to_public_safe_dict(self) -> dict[str, Any]:
        payload = {
            "log_version": self.log_version,
            "connector_run_id": self.connector_run_id,
            "connector_name": self.connector_name,
            "connector_type": self.connector_type,
            "source_policy_version": self.source_policy_version,
            "counts": {
                "discovered": self.discovered_count,
                "included": self.included_count,
                "excluded": self.excluded_count,
                "quarantined": self.quarantined_count,
            },
            "storage_mode": self.storage_mode,
            "replay_manifest_ref": (
                self.replay_manifest.replay_id if self.replay_manifest is not None else None
            ),
            "warnings": [f"warning-{index + 1}" for index, _warning in enumerate(self.warnings)],
            "errors": [f"error-{index + 1}" for index, _error in enumerate(self.errors)],
            "metadata": {
                key: value
                for key, value in self.metadata.items()
                if key
                in {
                    "connector_version",
                    "parser_version",
                    "adapter_version",
                    "synthetic_fixture",
                    "private_fixture",
                    "replay_limitations",
                }
            },
        }
        return redact_value(payload)
