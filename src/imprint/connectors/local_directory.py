from __future__ import annotations

from imprint.adapters import AdapterRegistry, ArtifactRegistry, build_default_registry
from imprint.connectors.config import ConnectorDeclaration
from imprint.connectors.protocol import ConnectorCapability, ConnectorDiscovery
from imprint.connectors.redaction import safe_error
from imprint.schemas import ArtifactStoragePolicy


class LocalDirectoryConnector:
    connector_type = "local_directory"

    def __init__(self, adapter_registry: AdapterRegistry | None = None):
        self.adapter_registry = adapter_registry or build_default_registry()

    def capability(self) -> ConnectorCapability:
        return ConnectorCapability(
            connector_type=self.connector_type,
            adapter_types=self.adapter_registry.source_types(),
            description="Uses an allowlisted local adapter over a configured local file or directory.",
        )

    def discover(self, config: ConnectorDeclaration) -> ConnectorDiscovery:
        if not config.enabled:
            return _disabled_discovery(config)
        adapter = self._adapter(config)
        try:
            envelopes = adapter.discover_artifacts(config.path)  # type: ignore[arg-type]
        except Exception as exc:
            raise ValueError(safe_error(str(exc), {"connector": config.name})) from exc
        return ConnectorDiscovery(
            connector_name=config.name,
            connector_type=self.connector_type,
            enabled=True,
            adapter_types=[adapter.source_type],
            artifact_count=len(envelopes),
            storage_mode=config.storage_mode.value,
            source_policy_version=config.source_policy_version,
            tags=list(config.tags),
        )

    def ingest(self, config: ConnectorDeclaration) -> ArtifactRegistry:
        if not config.enabled:
            return ArtifactRegistry()
        adapter = self._adapter(config)
        registry = ArtifactRegistry()
        storage_policy = ArtifactStoragePolicy(mode=config.storage_mode)
        try:
            registry.extend(adapter.ingest(config.path, storage_policy=storage_policy))  # type: ignore[arg-type]
        except Exception as exc:
            raise ValueError(safe_error(str(exc), {"connector": config.name})) from exc
        return registry

    def _adapter(self, config: ConnectorDeclaration):
        if config.adapter is None:
            raise ValueError("local_directory connector requires adapter")
        return self.adapter_registry.get(config.adapter)


def _disabled_discovery(config: ConnectorDeclaration) -> ConnectorDiscovery:
    return ConnectorDiscovery(
        connector_name=config.name,
        connector_type=config.type,
        enabled=False,
        adapter_types=[config.adapter] if config.adapter else [],
        artifact_count=0,
        storage_mode=config.storage_mode.value,
        source_policy_version=config.source_policy_version,
        tags=list(config.tags),
        warnings=["connector disabled"],
    )
