# Connector Implementation Standard

Status: Sprint 13 strategy gate

## Purpose

This standard defines the minimum requirements for implementing any future private connector. It
prevents adapter authority creep and keeps public core generic, synthetic-testable, and privacy-first.

Sprint 13 does not implement new private connectors. This document is a gate for later work.

## Required Pre-Implementation Artifacts

Before code starts for a source-specific connector, the work must include:

- source-specific threat model
- credential storage plan
- consent and multi-person policy mapping
- synthetic fixture plan
- replay and audit plan
- public/private repository boundary decision
- redaction test plan
- failure-mode test plan

A connector without these artifacts is not implementation-ready.

## Connector Authority Boundary

Connectors may:

- discover source records
- read explicitly configured local files or approved credentialed sources
- normalize source records through existing adapters or adapter-equivalent normalization
- emit `Artifact` records and advisory `source_hints`
- report counts, warnings, and local audit metadata
- fail closed on unsafe config or missing authority

Connectors must not:

- classify final authorship or inclusion truth
- extract profile signals
- compile profiles
- export profiles
- assemble prompts
- call LLMs unless a future source-specific model boundary explicitly permits it outside public core
- publish content
- expose raw corpus search
- bypass public-safe export validation
- treat provider metadata as durable truth about a person

## Public Core Boundary

Public core may contain only generic, synthetic-testable connector logic. Private source-specific
connectors should live outside public core unless they are fully generic, fixture-backed, and do not
encode private deployment assumptions.

Public core must not gain mandatory dependencies on OAuth clients, database drivers, cloud SDKs,
vendor APIs, private schemas, private account layouts, or local device internals just to support a
private adapter.

## Configuration Standard

Every connector declaration must define:

- connector name and type
- enabled/disabled state
- source class
- adapter or normalization strategy
- storage mode
- source policy version
- local-only/network requirement state
- credential references when needed
- synthetic/private labeling

Config validation must fail closed on wrong shape, unsafe inline secrets, required missing
credentials, unsupported storage modes, and unapproved network behavior.

## Discovery and Ingestion Standard

Discovery must be safe to run before ingestion. It may report counts and warnings, but it must not
print raw text, configured paths, credentials, private identifiers, or provider locators.

Ingestion must flow through normalization and produce artifacts with opaque source IDs. Raw text may
exist in memory during local normalization, but persistence must follow artifact storage policy.

## Storage Standard

Default storage is `metadata_only`. `local_artifact_store` requires explicit operator choice and
ignored protected paths. Public-safe exports must never include raw text or private locators,
regardless of storage mode.

## Replay and Audit Standard

Every connector must define how to rebuild or explain why rebuild is limited. Local audit output must
record:

- connector version
- parser or normalization version
- storage mode
- source policy version
- discovered/included/excluded/quarantined counts
- credential reference names without values
- skipped source classes
- replay limitations

Audit output is local-private unless explicitly designed as public-safe aggregate metadata.

## Test Standard

Implementation requires tests for:

- valid synthetic config
- invalid config fail-closed behavior
- credential-missing and credential-redaction behavior
- source-specific consent contamination
- advisory hint handling
- opaque source IDs
- dry-run output without paths or raw text
- no unintended network/model calls in public core
- public-safe export validation after connector-derived profile generation

## Documentation Standard

Connector docs must include:

- source threat model link
- configuration example using synthetic paths or placeholders only
- credential handling notes using fake env var names only
- storage and retention tradeoffs
- replay/audit behavior
- known non-goals and blocked source classes

Docs must not include real account names, private source paths, provider IDs, table names, message
bodies, or credential-shaped placeholders.
