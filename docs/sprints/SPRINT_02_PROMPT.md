# Sprint 02 Prompt - Schema and Contract Design

Use this prompt with GPT 5.5 from the repository root.

---

You are the Chief Schema Architect for Imprint.

Sprint 01 and Sprint 01.5 are complete. Your task is Sprint 02: Schema and Contract Design.

Read all relevant planning documents before making changes, especially:

- `docs/sprints/SPRINT_02.md`
- `docs/SPRINT_01_5_ARCHITECTURE_REVIEW.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/EXTRACTOR_VERSIONING.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/SCHEMA.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/MEMORY_DISCIPLINE.md`

Do not implement runtime behavior yet.
Do not create source adapters.
Do not create an API service.
Do not add private integrations.
Do not build prompt-generation logic.

Your job is to design and document the schema layer, then implement approved schema contracts only if the architecture is sufficiently clear.

## Required schema design outputs

Create or update:

- `docs/SCHEMA_PHILOSOPHY.md`
- `docs/SIGNAL_TAXONOMY.md`
- `docs/CONFIDENCE_MODEL.md`
- `docs/EVIDENCE_MODEL.md`
- `docs/VERSIONING_POLICY.md`
- `docs/MIGRATION_STRATEGY.md`
- `docs/PROFILE_STABILITY.md`
- `docs/SCHEMA_THREAT_MODEL.md`

## Required schema families

Design schemas for:

- Artifact
- ArtifactReference
- ArtifactStoragePolicy
- ArtifactClassification
- AuthorshipOrigin
- SourcePolicy
- Signal
- SignalSupport
- Claim
- ClaimValidation
- ExpressionProfile
- ContextProfile
- DerivedProfileDivergence
- BuildManifest
- ExtractorManifest
- ComparabilityResult
- ProfileExport
- DriftReport

## Sprint 01.5 constraints that must be encoded

1. Context profile budgets must exist and be explicit.
2. Extractor family taxonomy and build manifests must be sufficient for automated comparison.
3. Comparability must be computed from structured fields, not informal human judgment.
4. Claim levels must support `observation`, `bounded_interpretation`, `prohibited`, and `quarantined`.
5. Public-safe exports must fail if prohibited claims survive compilation.
6. Core profile schemas must not contain prompt-generation fields or provider-specific decoding controls.
7. Unknown authorship must be split into specific reason categories.
8. AI detector output must be metadata or weak evidence only, never ground truth.
9. Derived profiles must avoid hidden inheritance and should represent explicit context filters, divergences, and overrides.
10. Metadata-only artifact storage is the MVP default, and the schema must make its audit limitations visible.

## Implementation scope

After the schema design docs are complete, implement schema contracts only.

Implementation requirements:

- Pydantic v2
- validation
- serialization
- JSON schema generation
- tests using synthetic data only

Create implementation under:

- `src/imprint/schemas/`

Do not implement:

- harvesting
- storage engines
- source adapters
- LLM extractors
- prompt exporters
- API endpoints

## Exit criteria

Sprint 02 is complete only if:

- schema philosophy is documented,
- signal taxonomy is documented,
- confidence and evidence models are documented,
- versioning and migration policies are documented,
- profile stability policy is documented,
- schema threat model is documented,
- Sprint 01.5 review constraints are represented in schemas,
- schema tests pass,
- and no private data or private integration assumptions are introduced.

If schema implementation is unsafe because the design is still unresolved, stop after writing the design docs and clearly explain what remains blocked.
