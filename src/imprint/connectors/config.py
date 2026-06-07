from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from imprint.schemas import ArtifactStorageMode
from imprint.connectors.redaction import SECRET_KEY_PATTERN, SECRET_VALUE_PATTERN, safe_error

ConnectorType = Literal["local_directory", "manifest"]


class ConnectorConfigError(ValueError):
    pass


class ConnectorCredential(BaseModel):
    model_config = ConfigDict(extra="forbid")

    env: str = Field(min_length=1)
    required: bool = True

    @field_validator("env")
    @classmethod
    def env_name_is_safe(cls, value: str) -> str:
        if not value.startswith("IMPRINT_"):
            raise ValueError("connector credential env vars must use the IMPRINT_ prefix")
        return value


class ConnectorDeclaration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, pattern=r"^[A-Za-z0-9_.-]+$")
    type: ConnectorType
    enabled: bool = False
    adapter: str | None = None
    path: Path | None = None
    manifest_path: Path | None = None
    storage_mode: ArtifactStorageMode = ArtifactStorageMode.METADATA_ONLY
    source_policy_version: str = "sprint09-source-policy-v1"
    credentials: dict[str, ConnectorCredential] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    labels: dict[str, str] = Field(default_factory=dict)
    local_only: bool = True
    private: bool = True

    @model_validator(mode="after")
    def connector_shape_is_valid(self) -> ConnectorDeclaration:
        if self.type == "local_directory":
            if self.adapter is None:
                raise ValueError("local_directory connector requires adapter")
            if self.path is None:
                raise ValueError("local_directory connector requires path")
            if self.manifest_path is not None:
                raise ValueError("local_directory connector cannot set manifest_path")
        if self.type == "manifest":
            if self.manifest_path is None:
                raise ValueError("manifest connector requires manifest_path")
            if self.path is not None:
                raise ValueError("manifest connector cannot set path")
        if not self.local_only:
            raise ValueError("Sprint 09 connectors must be local_only")
        for key, value in self.labels.items():
            if SECRET_KEY_PATTERN.search(key) or SECRET_VALUE_PATTERN.search(value):
                raise ValueError("connector labels cannot include inline secrets")
        return self

    def validate_runtime(self) -> None:
        for name, credential in self.credentials.items():
            if credential.required and not os.environ.get(credential.env):
                raise ConnectorConfigError(
                    safe_error(
                        "required connector credential is not set",
                        {"connector": self.name, "credential": name, "env": credential.env},
                    )
                )
        if not self.enabled:
            return
        if self.path is not None and not self.path.exists():
            raise ConnectorConfigError(
                safe_error("connector path does not exist", {"connector": self.name, "path": str(self.path)})
            )
        if self.manifest_path is not None and not self.manifest_path.exists():
            raise ConnectorConfigError(
                safe_error(
                    "connector manifest does not exist",
                    {"connector": self.name, "manifest_path": str(self.manifest_path)},
                )
            )


class ImprintConnectorConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connectors: list[ConnectorDeclaration] = Field(default_factory=list)

    @model_validator(mode="after")
    def connector_names_are_unique(self) -> ImprintConnectorConfig:
        names = [connector.name for connector in self.connectors]
        if len(names) != len(set(names)):
            raise ValueError("connector names must be unique")
        return self

    def enabled_connectors(self) -> list[ConnectorDeclaration]:
        return [connector for connector in self.connectors if connector.enabled]

    def validate_runtime(self) -> None:
        for connector in self.connectors:
            connector.validate_runtime()


class ManifestEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, pattern=r"^[A-Za-z0-9_.-]+$")
    adapter: str = Field(min_length=1)
    path: Path
    tags: list[str] = Field(default_factory=list)
    labels: dict[str, str] = Field(default_factory=dict)


class ConnectorManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    entries: list[ManifestEntry] = Field(default_factory=list)


def load_connector_config(path: Path) -> ImprintConnectorConfig:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise ConnectorConfigError(safe_error("could not read connector config", {"path": str(path)})) from exc
    if not isinstance(raw, dict):
        raise ConnectorConfigError("connector config must be a mapping")
    connector_section = {"connectors": raw.get("connectors", [])}
    try:
        config = ImprintConnectorConfig.model_validate(connector_section)
        config.validate_runtime()
        return config
    except ValueError as exc:
        raise ConnectorConfigError(safe_error(str(exc))) from exc


def load_connector_manifest(path: Path) -> ConnectorManifest:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise ConnectorConfigError(safe_error("could not read connector manifest", {"path": str(path)})) from exc
    if not isinstance(raw, dict):
        raise ConnectorConfigError("connector manifest must be a mapping")
    try:
        return ConnectorManifest.model_validate(raw)
    except ValueError as exc:
        raise ConnectorConfigError(safe_error(str(exc))) from exc
