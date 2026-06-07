# Imprint Documentation

This directory contains the public project documentation for Imprint.

Imprint is still pre-release. The docs are intentionally detailed because the project is defining its product boundaries, schema contracts, privacy posture, and provider-neutral model policy before broad implementation.

## Start Here

- [Project Strategy](PROJECT_STRATEGY.md) — overall strategy and project intent
- [Product Positioning](PRODUCT_POSITIONING.md) — what Imprint is and is not
- [Architecture](ARCHITECTURE.md) — system boundaries and major components
- [Roadmap](ROADMAP.md) — staged implementation plan
- [Public Build Guide](PUBLIC_BUILD_GUIDE.md) — public-first development rules

## Product Theory

- [Profile Theory](PROFILE_THEORY.md) — expression profile theory and claim boundaries
- [Interpretation Boundaries](INTERPRETATION_BOUNDARIES.md) — observation vs interpretation vs diagnosis
- [First Run Experience](FIRST_RUN_EXPERIENCE.md) — the first meaningful user experience
- [Memory Discipline](MEMORY_DISCIPLINE.md) — store less than you can
- [Competitive Analysis](COMPETITIVE_ANALYSIS.md) — product lessons from adjacent systems

## Privacy, Security, and Data Handling

- [Security and Privacy](SECURITY_PRIVACY.md) — security/privacy design overview
- [Privacy and Local Mode](PRIVACY_AND_LOCAL_MODE.md) — local-first and remote-provider posture
- [Artifact Storage Policy](ARTIFACT_STORAGE_POLICY.md) — metadata-only default and local artifact store modes
- [Evidence and Confidence](EVIDENCE_AND_CONFIDENCE.md) — support metadata and confidence semantics
- [Evidence Model](EVIDENCE_MODEL.md) — evidence structure and requirements

## Schema and Contracts

- [Schema](SCHEMA.md) — canonical schema overview
- [Schema Philosophy](SCHEMA_PHILOSOPHY.md) — why the schema layer exists
- [Signal Taxonomy](SIGNAL_TAXONOMY.md) — signal categories and definitions
- [Compiler Design](COMPILER_DESIGN.md) — deterministic profile compiler behavior
- [Profile Compilation Rules](PROFILE_COMPILATION_RULES.md) — eligibility, evidence, confidence, and safety rules
- [Confidence Model](CONFIDENCE_MODEL.md) — confidence semantics
- [Versioning Policy](VERSIONING_POLICY.md) — schema/profile/export versioning
- [Migration Strategy](MIGRATION_STRATEGY.md) — migration approach
- [Profile Stability](PROFILE_STABILITY.md) — profile update and drift policy
- [Schema Threat Model](SCHEMA_THREAT_MODEL.md) — schema abuse and misuse risks
- [Schema Risks](SCHEMA_RISKS.md) — adversarial schema review output

## Model Provider Policy

- [Model Provider Policy](MODEL_PROVIDER_POLICY.md) — BYOM/BYOP policy
- [Model Role Taxonomy](MODEL_ROLE_TAXONOMY.md) — inference role definitions
- [Model Capability Contracts](MODEL_CAPABILITY_CONTRACTS.md) — testable model capability requirements
- [Model Privacy Boundaries](MODEL_PRIVACY_BOUNDARIES.md) — remote/local model privacy rules
- [Extractor Versioning](EXTRACTOR_VERSIONING.md) — extractor/model/prompt versioning

## Derived Profiles, Exports, and Integrations

- [Derived Profile Model](DERIVED_PROFILE_MODEL.md) — master/context profile composition
- [Export Formats](EXPORT_FORMATS.md) — public-safe JSON, Markdown, first-run, and Mosvera export contracts
- [First-Run Output](FIRST_RUN_OUTPUT.md) — What Imprint Learned output contract
- [Mosvera Integration](MOSVERA_INTEGRATION.md) — expression overlay boundary
- [Export Boundaries](EXPORT_BOUNDARIES.md) — what core Imprint can and cannot export
- [Downstream Integrations](DOWNSTREAM_INTEGRATIONS.md) — integration posture
- [Connector Guide](CONNECTOR_GUIDE.md) — connector design rules
- [Configuration](CONFIGURATION.md) — configuration conventions

## Sprint Runbooks

Sprint runbooks live under [`sprints/`](sprints/).

Most useful next:

- [Sprint 03](sprints/SPRINT_03.md) — local ingestion framework
- [Sprint 02.5](sprints/SPRINT_02_5.md) — model provider policy
- [Sprint 02](sprints/SPRINT_02.md) — schema and contract design

Recent sprint narratives are available under [`narrative/`](narrative/).

## Reviews and Decision Artifacts

- [Architecture Challenge](ARCHITECTURE_CHALLENGE.md) — Sprint 01 adversarial review
- [Sprint 01.5 Architecture Review](SPRINT_01_5_ARCHITECTURE_REVIEW.md)
- [Sprint 02.5 Architecture Review](SPRINT_02_5_ARCHITECTURE_REVIEW.md)
- [Decisions](DECISIONS.md)
- [Open Questions](OPEN_QUESTIONS.md)
- [Risks](RISKS.md)
- [Ownership Matrix](OWNERSHIP_MATRIX.md)

## Public Repository Rule

Public docs and examples must remain synthetic and public-safe.

Never commit real messages, emails, transcripts, generated private profiles, database dumps, API keys, or local configs.
