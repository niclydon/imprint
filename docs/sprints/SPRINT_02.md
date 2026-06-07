# Sprint 02 - Schema and Contract Design

Architect: GPT 5.5
Implementer: GPT 5.4
Adversarial Reviewer: Gemini

## Mission
Design the language of the platform.
The schema is the product.

## Required Reading
- all Sprint 01 outputs
- all Sprint 01.5 outputs
- docs/SCHEMA.md
- docs/ARCHITECTURE.md
- docs/ARTIFACT_STORAGE_POLICY.md
- docs/EXTRACTOR_VERSIONING.md
- docs/EXPORT_BOUNDARIES.md
- docs/DERIVED_PROFILE_MODEL.md
- docs/EVIDENCE_AND_CONFIDENCE.md

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
- BuildManifest
- ArtifactStoragePolicy
- EvidenceReference
- ContextProfile
- ClaimLevel

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
- how attribution, authorship-origin, extraction, evidence strength and source diversity combine

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
- classifier, extractor, prompt, model and source-policy versioning
- expression drift versus compiler drift versus corpus drift

Generate: VERSIONING_POLICY.md

## Migration Strategy
Define upgrades across schema generations.
Generate: MIGRATION_STRATEGY.md

## Profile Stability
Define:
- what triggers profile regeneration
- what triggers drift updates
- minimum evidence thresholds
- profile comparability labels
- cross-model semantic extraction as `not_comparable` unless explicitly migrated

Generate: PROFILE_STABILITY.md

## Sprint 01.5 Required Gates

Before Pydantic implementation begins, schema planning must specify:

- `metadata_only` as the default artifact storage mode
- explicit raw-content availability and audit limitation fields
- mandatory claim validation behavior for prohibited claims
- build manifest fields for compiler, classifier, extractor, prompt, model and policy versions
- `comparable`, `partially_comparable` and `not_comparable` profile comparison semantics
- divergence object shape and collision labels for context profiles
- context profile compilation from filtered evidence, not hidden inheritance
- core export projections only; no generation-ready prompt exporter

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
Schema philosophy, taxonomy, confidence model, evidence model, versioning policy, migration strategy
and threat model all approved. Sprint 02 must also preserve Sprint 01.5 constraints: explicit
artifact storage mode, build manifest, no hidden derived-profile inheritance, bounded
authorship-origin claims, and no core prompt-generation exporter.
