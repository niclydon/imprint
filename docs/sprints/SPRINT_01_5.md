# Sprint 01.5 - Architecture Remediation

Primary Model: GPT 5.5
Adversarial Reviewer: Gemini Antigravity
Status: Required before Sprint 02

## Mission

Resolve the architectural blockers raised in `docs/ARCHITECTURE_CHALLENGE.md` before schema work begins.

Sprint 01.5 is not an implementation sprint.

Its job is to convert adversarial findings into explicit architectural decisions, updated documents, and Sprint 02-ready constraints.

## Required Reading

Read:

- `docs/ARCHITECTURE_CHALLENGE.md`
- `docs/ARCHITECTURE.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/PRODUCT_THESIS.md`
- `docs/OWNERSHIP_MATRIX.md`
- `docs/SCHEMA.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/MEMORY_DISCIPLINE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/ROADMAP.md`
- `docs/sprints/SPRINT_02.md`

## Core Problems to Resolve

### 1. Artifact Storage and Auditability

The architecture currently wants auditability without clearly owning raw artifact persistence.

Resolve:

- Does Imprint store raw artifact text locally?
- If yes, under what mode and policy?
- If no, how does audit, regeneration, and evidence review work?
- What is the security posture for local raw corpora?
- How does Imprint remain distinct from a general memory system?

Expected decision direction:

Imprint may own a local, user-controlled Artifact Store scoped to profile compilation and auditability. That is not the same as owning a general assistant memory system.

Required output:

- `docs/ARTIFACT_STORAGE_POLICY.md`

### 2. Extractor Versioning and Determinism

The architecture currently treats profile drift as if it only reflects user expression changes.

Resolve:

- How are extractor model, prompt, code, schema, and configuration versions recorded?
- How do we distinguish expression drift from compiler drift?
- How can profiles be compared fairly across model changes?
- What must be stamped into every profile build?

Required output:

- `docs/EXTRACTOR_VERSIONING.md`

### 3. Export Boundaries

The roadmap includes “prompt contract” language that risks making Imprint a generation/publishing system.

Resolve:

- What can Imprint export?
- What must downstream adapters own?
- Are prompt fragments allowed in core?
- How does Imprint avoid owning ghostwriting workflows?

Expected decision direction:

Core Imprint exports profile contracts, observed patterns, constraints, evidence, and warnings. Downstream adapters translate those contracts into prompts or generation-specific instructions.

Required output:

- `docs/EXPORT_BOUNDARIES.md`

### 4. Derived Profile Model

The architecture assumes master and derived profiles but lacks inheritance semantics.

Resolve:

- What is a master profile?
- What is a derived profile?
- Do derived profiles inherit, override, or compile independently?
- How are divergences represented?
- How are context collisions handled?

Expected decision direction:

Avoid hidden inheritance. Derived profiles should be explicit compiled views with baseline profile references, context filters, divergences, and overrides.

Required output:

- `docs/DERIVED_PROFILE_MODEL.md`

### 5. Terminology and Interpretation Safety

The adversarial review correctly identified that schema terms like `identity`, `stance`, and `recurring_lens` may invite overclaiming.

Resolve:

- Should schema contracts use `identity`?
- What safer terminology should be used?
- How do we preserve product-level language without schema-level overclaiming?
- What fields are allowed in machine-readable contracts?

Expected decision direction:

Use `expression_profile`, `expression_posture`, `rhetorical_patterns`, and `context_profiles` in schema-level contracts. Reserve broad “identity” language for product/prose if used at all.

Required updates:

- `docs/PROFILE_THEORY.md`
- `docs/SCHEMA.md`
- `docs/INTERPRETATION_BOUNDARIES.md`

### 6. Authorship-Origin and AI Assistance

The architecture must not imply reliable AI detection.

Resolve:

- What does authorship-origin classification mean?
- What metadata can determine it?
- What remains unknown?
- How should unknown or suspected AI-assisted text be weighted?

Expected decision direction:

Authorship origin is evidence-based metadata classification, not magical AI detection. Unknown remains unknown.

Required updates:

- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`

## Required Deliverables

Create:

- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/EXTRACTOR_VERSIONING.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/SPRINT_01_5_REMEDIATION_SUMMARY.md`

Update as needed:

- `docs/SCHEMA.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/ROADMAP.md`
- `docs/sprints/SPRINT_02.md`

## Forbidden Work

Do not:

- implement code,
- create Pydantic schemas,
- add source adapters,
- add storage logic,
- add API endpoints,
- add prompt exporters,
- or start Sprint 02 implementation.

## Exit Criteria

Sprint 01.5 is complete only when:

- artifact storage policy is explicit,
- extractor versioning policy is explicit,
- export boundaries are explicit,
- derived profile model is explicit,
- schema terminology is safer,
- authorship-origin classification is bounded,
- Sprint 02 can proceed without resolving architectural blockers.
