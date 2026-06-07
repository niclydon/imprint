# Sprint 09 Architecture Review: Private Connector Framework and Import Boundaries

**Reviewer:** Codex acting as hostile principal architect  
**Status:** Post-implementation gate review  
**Context:** Evaluation of Sprint 09 private connector framework work against public/private boundary,
connector authority, secret handling, source privacy, scope control, and operational safety.

## Executive Summary

Sprint 09 adds a generic connector framework for owner-operated private ingestion without adding real
private-service integrations. The implementation introduces connector config validation, connector
capability/discovery contracts, a connector registry, a generic local-directory connector, a synthetic
manifest connector, redaction utilities, a dry-run CLI, and synthetic-only tests.

**Verdict: GO for Sprint 10 public web presence and future private connector planning**

The sprint avoids live APIs, OAuth, LLM calls, remote providers, prompt assembly, publishing
workflows, real private service assumptions, and real private corpora. Connectors feed the existing
adapter normalization path and do not bypass classification, signal extraction, compiler, export, or
consumer-contract safety boundaries.

## Review Scope

Reviewed:

- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- `docs/CONNECTOR_GUIDE.md`
- `.env.example`
- `imprint.config.example.yaml`
- `src/imprint/connectors/`
- `src/imprint/adapters/`
- `src/imprint/cli.py`
- `tests/test_connectors.py`
- existing adapter/classification/export/consumer tests
- full test suite output
- connector CLI dry-run output
- static scan for remote/provider/LLM call surfaces in connector code

## Findings

### 1. Public / Private Boundary

**Status: PASS**

The public repository contains only generic connector framework code and synthetic fixtures. The
built-in connector types are `local_directory` and `manifest`, both backed by existing local adapters.
Deferred private services such as Gmail, iMessage, Plaud, Looki, databases, cloud storage, and live
APIs remain documented as future private work, not implemented in public core.

No real private credentials, real corpora, private service hostnames, personal account identifiers,
database DSNs, OAuth tokens, API keys, or real source IDs were added.

### 2. Connector Authority

**Status: PASS**

Connectors discover and ingest only. They do not classify, extract signals, compile profiles, export
profiles, assemble prompts, publish content, or call models.

Connector outputs flow through existing adapter normalization into `Artifact` records. Connector and
adapter metadata remain advisory; classification still re-assesses authorship and inclusion before
profile use.

### 3. Secret Handling

**Status: PASS**

Connector credentials are represented as env var references with required/optional flags. Runtime
validation fails closed when required credentials are missing. Error handling uses redaction utilities
that mask secret-like keys, token-like values, DSNs with embedded credentials, and local paths.

Tests verify required credential failure, inline secret-like label rejection, and path redaction in
load-time errors.

### 4. Source Privacy

**Status: PASS**

Normalized artifacts preserve opaque `source-*` IDs. Local paths may be read by adapters during local
normalization, but they do not survive in source IDs or public-safe artifacts. Dry-run output reports
counts and adapter types without printing configured paths or raw text.

### 5. Scope Control

**Status: PASS**

Sprint 09 did not add live APIs, OAuth, cloud SDKs, remote calls, LLM calls, embeddings, prompt
assembly, Mosvera/Broadside runtime adapters, publishing workflows, or UI/dashboard behavior.

Static scan found no network/provider/runtime call surfaces in `src/imprint/connectors/`.

### 6. Operational Safety

**Status: PASS**

Disabled connectors are inert and can reference missing private paths without running. Dry-run
discovery returns connector metadata and artifact counts only; it does not emit normalized artifacts or
persist data. Enabled connectors fail closed on invalid paths and invalid config shapes.

## Validation Evidence

- `pytest -q` -> 96 passed
- `python3 -m compileall -q src` -> passed
- `PYTHONPATH=src python3 -m imprint.cli connectors-dry-run --config imprint.config.example.yaml` -> passed
- static connector scan -> no remote/provider/LLM call surfaces

## Resolved Issues

1. Added a connector protocol, registry, config schema, and capability metadata.
2. Added dry-run/source-discovery behavior that avoids artifact persistence and path output.
3. Added generic local-directory and synthetic manifest connectors over existing adapters.
4. Added secret/path redaction utilities and fail-closed runtime validation.
5. Updated public configuration and connector docs with private/public boundaries.
6. Added synthetic-only tests for config validation, disabled connectors, advisory metadata, opaque
source IDs, path redaction, CLI dry-run, and no remote/provider calls.

## Unresolved Blockers

None for Sprint 10 public web presence.

Future private connector implementations remain blocked on source-specific threat models,
credential-storage rules, consent boundaries, replay/audit behavior, and synthetic fixtures for each
connector class.

## Recommendations Before Future Private Connectors

1. Add source-specific threat models before implementing Gmail, iMessage, Plaud, Looki, database, or
cloud connectors.
2. Keep private connector implementations outside public core unless they are generic and
synthetic-testable.
3. Add explicit storage-location policy before enabling `local_artifact_store` connectors for private
corpora.
4. Add file-based export validation UX only after there is a real operator workflow requiring it.
5. Keep consumer contracts as canonical JSON projections; do not bind them to connector runtime state.

## Gate Decision

**GO.**

Sprint 09 satisfies the connector framework, config validation, dry-run, redaction, synthetic testing,
public/private boundary, and scope-control requirements.
