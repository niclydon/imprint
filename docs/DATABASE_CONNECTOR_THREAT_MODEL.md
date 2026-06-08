# Database Connector Threat Model

Status: Sprint 13 strategy gate

## Scope

This document defines the conditions required before any SQL, warehouse, application database, cloud
data, or query-based connector can be implemented. Sprint 13 does not implement database drivers,
network access, query execution, schema introspection, or cloud credentials.

## Source Ownership and Consent

Databases can contain many people's records and operational secrets. A future connector must define:

- who owns or controls the database
- which tables, views, or exported files are permitted
- which rows belong to the profile subject
- whether records include other people, customers, employees, or third parties
- whether consent exists for each source class
- whether derived rows include generated or system-authored text

Default policy: only explicitly allowlisted synthetic or owner-authorized rows may be ingested.
Unbounded table scans are forbidden.

## Credential Handling

Database credentials and DSNs are high-risk. A future connector must:

- use least-privilege read-only credentials
- require query allowlists or named extracts
- store DSNs and passwords only through the credential storage policy
- never print DSNs, usernames, hostnames, database names, schema names, or table names from private deployments in public-safe output
- fail closed on inline DSNs, broad privileges, missing query allowlists, or unapproved network access
- require separate review for cloud IAM, service accounts, tunnels, and bastions

Public docs may use only fictional env var names and generic placeholder labels.

## Local Storage and Retention

Default storage must be `metadata_only`. Query results that contain text, identifiers, or row-level
metadata are protected data.

Retention metadata must record:

- query or extract identifier, not raw SQL when private
- connector version
- row count and excluded/quarantined count
- row-level subject filter policy
- storage mode
- whether raw row text or structured fields were retained locally

## Replay and Rebuild Behavior

Replay must be deterministic and bounded. A future connector must use one of:

- a checked-in synthetic fixture
- an ignored local export snapshot
- an allowlisted query with pinned parameters and row limits

Replay metadata must include query allowlist version, parameter shape, row-count limits, source policy
version, and extraction timestamp bucket. Live database state changes must be disclosed as a replay
limitation.

## Audit and Revocation

The connector must produce a local audit summary with:

- configured source class
- allowlisted query or extract name
- rows discovered, included, excluded, and quarantined
- subject-filter policy
- credential source env var names without values
- retention mode and replay limitation

Revocation disables credentials or source exports and marks local replay state stale unless the
operator explicitly retains a protected snapshot.

## Source-Specific Privacy Leaks

Database-specific leak vectors include:

- DSNs, usernames, hostnames, schema names, table names, and private query text
- row IDs, customer IDs, employee IDs, tenant IDs, and account IDs
- records about people other than the profile subject
- operational logs, support tickets, and generated system messages
- hidden joins that pull unauthorized columns
- row-level timestamps precise enough to identify private events
- cloud project, bucket, dataset, or warehouse identifiers

Public-safe exports must contain only opaque source IDs and aggregate support metadata.

## Adapter Hint Trust Boundaries

Database columns may hint at author, record type, ownership, and source status. These hints are
advisory. Classification must still decide authorship, inclusion, quarantine, AI/template risk, and
support eligibility.

The connector must not treat database row labels as truth about a person. It may only normalize
allowlisted rows into artifacts.

## Synthetic Fixture Requirements

Before implementation, synthetic database fixtures must cover:

- allowlisted rows authored by the subject
- rows about or by another person
- system-generated rows
- query denylist failures
- DSN redaction
- row-level subject filter behavior
- row limit and pagination boundaries
- schema drift or missing column failures
- replay from a synthetic export snapshot

Fixtures must use fictional schemas, fictional table names, fake row IDs, and synthetic row content.
No private schema names, SQL files, exports, or database dumps may be committed.

## Public Repository Safety Constraints

The public repository may contain connector standards, synthetic database-shaped fixtures, and tests
for allowlisting/redaction behavior. It must not contain database drivers wired to live systems,
private SQL, dumps, DSNs, cloud project identifiers, or table names from private deployments.

A database connector remains blocked until query allowlisting, credential handling, row-level privacy,
replay, audit, and synthetic fixture tests exist.
