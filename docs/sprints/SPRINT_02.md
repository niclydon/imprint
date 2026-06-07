# Sprint 02 - Schema and Contract Design

Architect: GPT 5.5
Implementer: GPT 5.4
Adversarial Reviewer: Gemini

## Mission
Design the language of the platform.
The schema is the product.

## Required Reading
- all Sprint 01 outputs
- docs/SCHEMA.md
- docs/ARCHITECTURE.md

## Schema Philosophy
Before creating any schema explain:
- why it exists
- what problem it solves
- alternatives considered

Generate: SCHEMA_PHILOSOPHY.md

## Required Core Objects
- Artifact
- Classification
- Signal
- Profile
- Export
- Drift
- SourcePolicy
- AuthorshipPolicy

## Signal Taxonomy
Define:
- lexical
- tone
- humor
- reasoning
- structure
- narrative
- anti-patterns

For each provide:
- definition
- evidence requirements
- non-examples
- confidence guidance

Generate: SIGNAL_TAXONOMY.md

## Confidence Philosophy
Define exactly what confidence means.
Answer:
- statistical?
- heuristic?
- model-derived?
- hybrid?

Generate: CONFIDENCE_MODEL.md

## Evidence Philosophy
Every signal must answer:
Why do we believe this?

Generate: EVIDENCE_MODEL.md

## Versioning Strategy
Define:
- profile versioning
- schema versioning
- export versioning

Generate: VERSIONING_POLICY.md

## Migration Strategy
Define upgrades across schema generations.
Generate: MIGRATION_STRATEGY.md

## Profile Stability
Define:
- what triggers profile regeneration
- what triggers drift updates
- minimum evidence thresholds

Generate: PROFILE_STABILITY.md

## Schema Threat Model
Analyze:
- profile poisoning
- attribution failures
- AI contamination
- prompt injection
- multi-user confusion

Generate: SCHEMA_THREAT_MODEL.md

## Implementation Prompt
Implement approved schemas only.
Pydantic v2, validation, serialization, JSON schema generation and tests.
No storage, APIs, connectors or harvesting.

## Adversarial Review Prompt
Assume schemas must survive five years.
Find migration, coupling, naming and extensibility risks.
Generate SCHEMA_RISKS.md.

## Exit Criteria
Schema philosophy, taxonomy, confidence model, evidence model, versioning policy, migration strategy and threat model all approved.
