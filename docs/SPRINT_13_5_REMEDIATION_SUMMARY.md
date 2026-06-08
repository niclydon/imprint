# Sprint 13.5 Remediation Summary: Private Adapter Enforcement Foundation

**Date:** 2026-06-08
**Status:** Implemented
**Scope:** Sprint 13 adversarial enforcement gaps before real private adapters

## Summary

Sprint 13.5 turns Sprint 13 strategy into enforceable public-core contracts and tests without adding
real private adapters. The implementation adds consent-boundary evaluation, stronger connector
redaction, replay manifest metadata, redacted audit log payloads, fixture leakage scanning, and
adapter-authority boundary tests.

## Gaps Fixed

### Consent enforcement

- Added `ConsentClass`, `ConsentAction`, `ConsentBoundary`, and `ConsentBoundaryResult` in
  `src/imprint/connectors/consent.py`.
- Integrated consent evaluation into `RuleBasedArtifactClassifier`.
- Added tests for received mail, group chat participant content, third-party transcript speakers, and
  owner-authored source hints.

### Redaction hardening

- Expanded connector redaction for OAuth-style refresh/access tokens, JWTs, database DSNs, API keys
  in URL query parameters, AWS access keys, Azure connection strings, and bearer/basic auth values.
- Added tests for all required credential shapes.

### Replay and rebuild versioning

- Added `ConnectorReplayManifest`, replay IDs, config hashing, and compatibility checks in
  `src/imprint/connectors/replay.py`.
- Documented replay metadata and drift semantics in `docs/CONNECTOR_REPLAY_MANIFEST.md`.

### Connector audit log contract

- Added `ConnectorAuditLog` in `src/imprint/connectors/audit.py`.
- Audit payloads include run IDs, connector metadata, counts, storage mode, replay refs, warnings,
  errors, and metadata after redaction.
- Documented the contract in `docs/CONNECTOR_AUDIT_LOG.md`.

### Public/private leakage detection

- Added fixture leakage scanner in `src/imprint/connectors/leakage.py`.
- Scanner detects unsafe fixture naming, real-looking emails, phone numbers, private URLs, local home
  paths, account IDs, DSNs, and credential/token shapes.
- Added tests for unsafe synthetic-private fixture content and current public fixture trees.

### Adapter authority boundaries

- Expanded connector tests to prove connector code does not import pipeline authority such as
  classifiers, signal extractors, compilers, exporters, LLM/provider packages, or network clients.

## Documentation Updated

- `docs/CONSENT_BOUNDARY_MODEL.md`
- `docs/CONNECTOR_REPLAY_MANIFEST.md`
- `docs/CONNECTOR_AUDIT_LOG.md`
- `docs/CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONNECTOR_IMPLEMENTATION_STANDARD.md`

## Non-Goals Preserved

Sprint 13.5 does not implement Gmail, iMessage, Plaud, Looki, transcript, database, cloud, OAuth,
live API, service/API, UI review, or raw corpus storage behavior.

## Verification

Sprint 13.5 verification includes targeted consent/connector tests, full test suite, compile checks,
connector dry-run, synthetic example generation, validation, and profile diff smoke tests.

## Adversarial Fan-Out Fixes

Focused adversarial subagents initially returned NO-GO findings. Sprint 13.5 resolved them before
final review:

- private-source consent aliases now fail closed when consent hints are missing
- transcript segments require explicit `speaker_role` before durable subject-authored inclusion
- nested `env` mappings no longer leak secret values or secret-like nested keys
- fixture leakage scanning detects base64/base64url-encoded credentials and local paths
- public narrative docs were sanitized for private file-share handoff details
- replay compatibility includes manifest version
- config hashes are computed over redacted config shape
- audit logs emit allowlisted summaries instead of arbitrary warning/error/raw metadata text
- connector authority scans recurse through connector subpackages
