# Migration Strategy

Status: Sprint 02 schema contract

## Principle

Migrations preserve meaning or declare non-comparability. They must not silently reinterpret expression drift as profile change.

## Migration Types

- `schema_only`: field rename or structural move with preserved semantics.
- `policy_migration`: source, authorship, evidence, or validation policy changed.
- `extractor_migration`: extractor family or version changed.
- `corpus_rebuild`: source corpus changed or raw evidence had to be re-harvested.
- `export_projection`: downstream projection shape changed without changing canonical profile semantics.

## Requirements

Each migration records source version, target version, migration ID, compatibility claim, and warnings. Cross-model semantic extraction is `not_comparable` unless an explicit migration policy says otherwise.

## Metadata-Only Constraint

When raw content is unavailable, migrations that require re-extraction must declare that regeneration depends on live source access or user-provided artifacts. They must not pretend local replay is possible.

## Prohibited Claim Handling

Migrations must re-run claim validation. A migrated public-safe export fails if prohibited claims survive compilation.
