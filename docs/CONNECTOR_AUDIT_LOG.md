# Connector Audit Log

Status: Sprint 13.5 enforcement contract

## Purpose

The connector audit log defines a standardized, redacted local record of connector discovery and
ingestion behavior. It gives future private connector implementations a common audit shape before
any Gmail, iMessage, transcript, database, cloud, or live API connector exists.

Implementation lives in `src/imprint/connectors/audit.py`.

## Log Version

Current version: `sprint13.5-connector-audit-log-v1`

## Required Fields

An audit log includes:

- connector run ID
- connector name and type
- source policy version
- discovered, included, excluded, and quarantined counts
- storage mode
- replay manifest reference
- warnings
- redacted errors
- redacted metadata

## Redaction Rule

Audit logs must never expose:

- raw artifact text
- credentials
- OAuth refresh/access material
- database DSNs
- API keys in URLs
- JWTs
- AWS keys
- Azure connection strings
- bearer/basic auth values
- private local paths
- unredacted connector config

`ConnectorAuditLog.to_public_safe_dict()` applies connector redaction to warnings, errors, and
metadata before returning a serializable payload.

## Local vs Public Use

Connector audit logs are local-private by default. Public-safe summaries may include only counts,
non-secret connector identifiers, storage mode, source policy version, and replay manifest refs.

## Regression Coverage

Sprint 13.5 tests prove audit logs redact DSNs, API-key metadata, and local paths while preserving
counts and replay references.
