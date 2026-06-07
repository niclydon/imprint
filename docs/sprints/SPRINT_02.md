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



## Sprint 01.5 Architecture Review Constraints

Before designing or implementing schemas, incorporate the conditional-go findings from `docs/SPRINT_01_5_ARCHITECTURE_REVIEW.md`.

Sprint 02 must explicitly account for these constraints:

### 1. Context Profile Budget

The schema/config model must include an explicit context profile budget.

MVP default recommendation:

```yaml
max_context_profiles: 5
```

The schema should make context cost visible. If the user requests more context profiles than the configured budget, the system should require an explicit override rather than silently recomputing unbounded context views.

### 2. Extractor Family Taxonomy

The profile build manifest must contain enough fields to compare builds without human judgment.

At minimum, design for:

- `extractor_family`
- `extractor_major_version`
- `extractor_minor_version`
- `extractor_prompt_version`
- `extractor_code_version`
- `model_provider`
- `model_name`
- `model_version`
- `source_policy_version`
- `schema_version`

### 3. Automated Comparability Decision

Profile comparison must not depend on informal human judgment.

The schema must support automatic classification of profile comparisons as:

- `comparable`
- `partially_comparable`
- `not_comparable`

The comparison object must also explain why.

### 4. Claim Validation Framework

Claim validation is mandatory.

The schema must support claim levels such as:

- `observation`
- `bounded_interpretation`
- `prohibited`
- `quarantined`

Public-safe exports must fail if prohibited claims survive compilation.

Do not rely on simple keyword matching alone. The schema should make room for rule-based, taxonomy-based, and review-based validation.

### 5. Export Schema Guardrails

Core Imprint exports must not become prompt-generation artifacts.

The schema should forbid or isolate fields that imply downstream model control, including:

- `prompt`
- `system_prompt`
- `instruction`
- `temperature`
- `decoding`
- `model_hint`
- provider-specific generation settings

If such fields are ever needed, they belong in downstream adapter packages, not canonical core Imprint profiles.

### 6. Unknown Authorship Categories

Do not use a single broad `unknown` category.

The schema should distinguish reasons such as:

- `unknown_speaker`
- `quoted_or_forwarded`
- `missing_metadata`
- `suspected_ai_assisted`
- `parser_uncertain`
- `mixed_authorship`
- `assistant_output`
- `human_origin`
- `human_directed_ai_assisted`

Unknown or weakly attributed material should reduce confidence or trigger quarantine according to source policy.

### 7. AI Detector Output Is Weak Evidence Only

The schema may record AI detector output as metadata, but detector output must never become ground truth.

Detector-derived signals should be bounded, weak evidence and should not silently promote or demote artifact authorship without corroboration.


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
