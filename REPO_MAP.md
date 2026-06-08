# Imprint Repository Map

## Top-level purpose

Imprint compiles evidence-backed expression profiles from human-authored artifacts and exports public-safe contracts for downstream systems.

## Important directories

- `src/imprint/adapters/` — normalize local files and structured records into artifacts.
- `src/imprint/connectors/` — discover configured sources and feed adapters. Connectors ingest only.
- `src/imprint/classification/` — classify authorship, inclusion, exclusion, quarantine, and risk.
- `src/imprint/signals/` — extract artifact-level expression observations.
- `src/imprint/compiler/` — compile durable signals into profile-level expression patterns.
- `src/imprint/exports/` — produce public-safe JSON, Markdown, first-run, and overlay exports.
- `src/imprint/consumers/` — project canonical exports for downstream consumer contracts.
- `src/imprint/quality.py` — validation, comparison, release gates, and quality checks.
- `src/imprint/service.py` — local/private service facade for public-safe exports only.
- `tests/` — synthetic tests only. No real corpora.
- `examples/` — synthetic onboarding corpus and demo assets.
- `docs/` — architecture, policies, reviews, roadmap, and sprint plans.
- `web/` — public landing site.

## Canonical flow

```text
configured sources
  -> connectors
  -> adapters
  -> classification
  -> signals
  -> compiler
  -> exports
  -> consumer projections
  -> validation / quality gates
```

## Source of truth

Canonical JSON export is the source of truth for downstream projections. Consumer-specific payloads are views, not independent profile schemas.

## Privacy model

Public-safe exports must not contain raw text, private paths, credentials, source snippets, or private connector config. Source IDs must remain opaque.

## Service mode

Service mode is optional, local/private, disabled by default, and may expose only public-safe contracts. It must preserve batch/CLI parity.
