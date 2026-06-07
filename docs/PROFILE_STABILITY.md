# Profile Stability

Status: Sprint 02 schema contract

## Stability Claim

An Imprint profile is stable only relative to its build manifest, source policy, authorship policy, corpus window, and schema version.

## Regeneration Triggers

Regenerate a profile when:

- compiler version or compiler confidence model changes
- extractor family, major version, prompt version, or code version changes materially
- classifier or authorship policy changes
- source policy or context filters change
- raw corpus window changes
- claim validation rules change
- schema migration requires re-normalization

## Drift Update Triggers

Create a drift report when two builds are comparable or partially comparable and there is a meaningful change in signals, confidence, evidence support, source mix, or context divergences.

## Evidence Thresholds

MVP thresholds are schema-level constraints, not runtime extraction logic:

- every signal needs at least one evidence reference or aggregate support count
- compiled profile signals must preserve contributing signal IDs, rule IDs, and classifier/signal
  model versions
- bounded interpretations require explicit rationale and confidence components
- context divergences require baseline and context support counts
- weak authorship, unknown speaker, mixed authorship, or suspected AI-assisted evidence lowers confidence or triggers quarantine according to source policy

## Context Budget

Context profile budgets are explicit. MVP default is `max_context_profiles: 5`. Requests beyond the budget require an explicit override in policy or config.

## Comparability Labels

- `comparable`: expression drift may be reported.
- `partially_comparable`: changes may be reported with caveats.
- `not_comparable`: report compiler, schema, model, or corpus change rather than expression drift.

Cross-model semantic extraction is `not_comparable` unless explicitly migrated.
