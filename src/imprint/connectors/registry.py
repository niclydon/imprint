from __future__ import annotations

from dataclasses import dataclass, field

from imprint.adapters import ArtifactRegistry
from imprint.connectors.config import ConnectorDeclaration, ImprintConnectorConfig
from imprint.connectors.local_directory import LocalDirectoryConnector
from imprint.connectors.manifest import ManifestConnector
from imprint.connectors.protocol import ConnectorDiscovery, SourceConnector


class UnknownConnectorError(ValueError):
    pass


@dataclass
class ConnectorRegistry:
    connectors: dict[str, SourceConnector] = field(default_factory=dict)

    def register(self, connector: SourceConnector) -> None:
        self.connectors[connector.connector_type] = connector

    def get(self, connector_type: str) -> SourceConnector:
        if connector_type not in self.connectors:
            raise UnknownConnectorError(f"unknown connector type: {connector_type}")
        return self.connectors[connector_type]

    def discover(self, declaration: ConnectorDeclaration) -> ConnectorDiscovery:
        return self.get(declaration.type).discover(declaration)

    def ingest(self, declaration: ConnectorDeclaration) -> ArtifactRegistry:
        return self.get(declaration.type).ingest(declaration)

    def discover_config(self, config: ImprintConnectorConfig) -> list[ConnectorDiscovery]:
        return [self.discover(declaration) for declaration in config.connectors]

    def ingest_config(self, config: ImprintConnectorConfig) -> ArtifactRegistry:
        registry = ArtifactRegistry()
        for declaration in config.connectors:
            registry.extend(self.ingest(declaration).values())
        return registry


def build_default_connector_registry() -> ConnectorRegistry:
    registry = ConnectorRegistry()
    registry.register(LocalDirectoryConnector())
    registry.register(ManifestConnector())
    return registry
