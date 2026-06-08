# Profile Comparison

Status: Sprint 12 baseline

`imprint diff` compares two canonical JSON profile exports without reading raw corpora.

## Command

```bash
imprint diff profile-a.imprint.json profile-b.imprint.json
```

The command validates both inputs, then emits a deterministic JSON comparison report.

## Comparability States

Every comparison reports:

- `COMPARABLE`
- `PARTIALLY_COMPARABLE`
- `NOT_COMPARABLE`

The state is computed from structured build manifest fields using the schema-level
`ComparabilityResult` contract.

## Compared Fields

The report compares:

- profile and export IDs
- schema family and schema version
- compiler version
- classifier versions
- extractor family, major, minor, prompt, and code versions
- model provider/name/version metadata
- source policy version
- export schema version
- source summary fingerprint
- signal IDs and stable signal hashes
- support count deltas
- compatibility warnings

## Drift Categories

Comparison separates:

- `expression_drift`
- `compiler_drift`
- `corpus_drift`
- `schema_drift`

Implementation drift must not be presented as expression drift. If profiles are `NOT_COMPARABLE`,
`expression_drift` is not reported even when signal payloads differ.

## Corpus Policy

Sprint 12 treats profiles as corpus-compatible only when the source-summary fingerprint and build
manifest `config_hash` match. A changed corpus fingerprint produces `NOT_COMPARABLE` with
`corpus_drift`.

This is intentionally conservative. Future sprints may add a richer controlled-corpus equivalence
registry, but no manual override exists in Sprint 12.
