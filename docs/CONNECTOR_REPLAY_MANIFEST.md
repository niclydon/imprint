# Connector Replay Manifest

Status: Sprint 13.5 enforcement contract

## Purpose

The connector replay manifest defines the metadata required to compare or rebuild connector-driven
profile runs without confusing connector/parser/source-policy drift with expression drift.

Implementation lives in `src/imprint/connectors/replay.py`.

## Manifest Version

Current version: `sprint13.5-connector-replay-manifest-v1`

## Required Fields

A replay manifest records:

- `connector_name`
- `connector_type`
- `connector_version`
- `adapter_version`
- `parser_version`
- `source_policy_version`
- `storage_mode`
- `config_hash`
- `synthetic_fixture`
- `private_fixture`
- `replay_limitations`

The manifest also exposes a stable `replay_id` derived from the manifest content.

## Compatibility Rule

Connector-driven comparisons must not claim clean expression drift when any of these fields differ:

- connector type
- connector version
- adapter version
- parser version
- source policy version
- storage mode
- config hash
- synthetic/private fixture indicators

Sprint 13.5 adds `replay_manifests_compatible` as the public helper for this decision. Future profile
comparison work should lift replay manifest metadata into build manifests before private connectors
ship.

## Config Hash

`config_hash` must be computed from redacted, non-secret config shape. It must not include credential
values, private paths, provider cursors, local account identifiers, or raw source text.

## Replay Limitations

Replay limitations must disclose when exact rebuilds are impossible, such as:

- mutable live source state
- metadata-only storage without source snapshot
- skipped attachments or audio
- provider cursor expiry
- parser version changes

## Regression Coverage

Sprint 13.5 tests prove replay IDs are stable and parser-version drift makes manifests incompatible.
