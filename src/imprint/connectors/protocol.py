from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from imprint.adapters.registry import ArtifactRegistry
from imprint.connectors.config import ConnectorDeclaration


class ConnectorError(ValueError):
    pass


@dataclass(frozen=True)
class ConnectorCapability:
    connector_type: str
    adapter_types: list[str]
    supports_dry_run: bool = True
    persists_artifacts: bool = False
    requires_network: bool = False
    invokes_models: bool = False
    description: str = ""


@dataclass(frozen=True)
class ConnectorDiscovery:
    connector_name: str
    connector_type: str
    enabled: bool
    adapter_types: list[str]
    artifact_count: int
    storage_mode: str
    source_policy_version: str
    tags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class SourceConnector(Protocol):
    connector_type: str

    def capability(self) -> ConnectorCapability:
        raise NotImplementedError

    def discover(self, config: ConnectorDeclaration) -> ConnectorDiscovery:
        raise NotImplementedError

    def ingest(self, config: ConnectorDeclaration) -> ArtifactRegistry:
        raise NotImplementedError
