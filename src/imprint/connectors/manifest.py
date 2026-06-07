from __future__ import annotations

from pathlib import Path

from imprint.adapters import AdapterRegistry, ArtifactRegistry, build_default_registry
from imprint.connectors.config import ConnectorDeclaration, load_connector_manifest
from imprint.connectors.protocol import ConnectorCapability, ConnectorDiscovery
from imprint.connectors.redaction import safe_error
from imprint.schemas import ArtifactStoragePolicy


class ManifestConnector:
    connector_type = "manifest"

    def __init__(self, adapter_registry: AdapterRegistry | None = None):
        self.adapter_registry = adapter_registry or build_default_registry()

    def capability(self) -> ConnectorCapability:
        return ConnectorCapability(
            connector_type=self.connector_type,
            adapter_types=self.adapter_registry.source_types(),
            description="Reads a synthetic manifest of allowlisted local adapter inputs.",
        )

    def discover(self, config: ConnectorDeclaration) -> ConnectorDiscovery:
        if not config.enabled:
            return ConnectorDiscovery(
                connector_name=config.name,
                connector_type=self.connector_type,
                enabled=False,
                adapter_types=[],
                artifact_count=0,
                storage_mode=config.storage_mode.value,
                source_policy_version=config.source_policy_version,
                tags=list(config.tags),
                warnings=["connector disabled"],
            )
        manifest = load_connector_manifest(config.manifest_path)  # type: ignore[arg-type]
        artifact_count = 0
        adapter_types: set[str] = set()
        for entry in manifest.entries:
            adapter = self.adapter_registry.get(entry.adapter)
            entry_path = self._resolve_entry_path(config.manifest_path, entry.path)  # type: ignore[arg-type]
            try:
                artifact_count += len(adapter.discover_artifacts(entry_path))
            except Exception as exc:
                raise ValueError(safe_error(str(exc), {"connector": config.name, "entry": entry.name})) from exc
            adapter_types.add(adapter.source_type)
        return ConnectorDiscovery(
            connector_name=config.name,
            connector_type=self.connector_type,
            enabled=True,
            adapter_types=sorted(adapter_types),
            artifact_count=artifact_count,
            storage_mode=config.storage_mode.value,
            source_policy_version=config.source_policy_version,
            tags=list(config.tags),
        )

    def ingest(self, config: ConnectorDeclaration) -> ArtifactRegistry:
        if not config.enabled:
            return ArtifactRegistry()
        manifest = load_connector_manifest(config.manifest_path)  # type: ignore[arg-type]
        registry = ArtifactRegistry()
        storage_policy = ArtifactStoragePolicy(mode=config.storage_mode)
        for entry in manifest.entries:
            adapter = self.adapter_registry.get(entry.adapter)
            entry_path = self._resolve_entry_path(config.manifest_path, entry.path)  # type: ignore[arg-type]
            try:
                registry.extend(adapter.ingest(entry_path, storage_policy=storage_policy))
            except Exception as exc:
                raise ValueError(safe_error(str(exc), {"connector": config.name, "entry": entry.name})) from exc
        return registry

    def _resolve_entry_path(self, manifest_path: Path, entry_path: Path) -> Path:
        if entry_path.is_absolute():
            return entry_path
        return manifest_path.parent / entry_path
