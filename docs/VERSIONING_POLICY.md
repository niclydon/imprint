# Versioning Policy

Status: Sprint 02 schema contract

## Versioned Surfaces

Build manifests record separate versions for:

- schema
- compiler
- classifier
- extractor family, major, minor, prompt, and code
- model provider, name, and version
- source policy
- authorship policy
- export schema
- migration policy

## Semantic Roles

- **Schema version** controls field compatibility.
- **Compiler version** controls aggregation and validation behavior.
- **Classifier version** controls artifact classification and authorship-origin labels.
- **Extractor versions** control signal semantics.
- **Prompt version** applies only to extractor prompts, not core export prompts.
- **Model fields** identify semantic extraction dependencies.
- **Source policy version** defines inclusion, exclusion, weighting, and context budgets.

## Drift Categories

- `expression_drift`: comparable builds show changed expression patterns.
- `compiler_drift`: compiler, classifier, or validation behavior changed.
- `corpus_drift`: source mix, time window, or artifact set changed materially.
- `schema_drift`: schema migration changed representation.

## Comparability

Comparability must be computed from structured fields:

- `comparable`: same schema family, extractor family and major version, source policy, and compatible corpus.
- `partially_comparable`: schema-compatible with minor extractor, prompt, model, or source-mix caveats.
- `not_comparable`: different extractor family, cross-model semantic extraction without migration, incompatible schema, or materially different corpus.

The comparison result must include machine-readable reasons.
