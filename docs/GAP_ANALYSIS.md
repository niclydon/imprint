# Gap Analysis

Status: Sprint 01 output
Verdict: architecture is coherent; no critical blocker prevents Sprint 02

## Executive Summary

The current architecture is ready for schema work. The core separation is sound:

```text
source systems -> Imprint expression compiler -> downstream consumers
```

The main gaps are not implementation blockers. They are precision gaps that Sprint 02 must close:
evidence semantics, confidence semantics, versioning, migration, and public-safe output rules.

## Source Document Gaps

The Sprint 01 prompt required several planning documents that are not present in the repository:

- `docs/COMPETITIVE_ANALYSIS.md`
- `docs/PRODUCT_POSITIONING.md`
- `docs/MEMORY_DISCIPLINE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`

This is a planning hygiene gap, not a critical architecture blocker. The generated Sprint 01
outputs cover the missing themes, but the repo should eventually add or explicitly retire these
expected source docs so future sprint prompts do not depend on absent files.

## Architecture Strengths

- The product has a clear independent boundary.
- The roadmap defers private connectors until after public-safe schemas and local MVP behavior.
- Public examples are synthetic by decision.
- Raw examples are off by default in exports.
- Voice is modeled as multi-dimensional instead of a single style score.
- AI assistance and speaker attribution are first-class risks.
- CLI-first architecture keeps the MVP useful without a service.
- Downstream systems consume profiles instead of raw corpus data.

## Product Boundary Gaps

### 1. Memory Boundary Needs Operational Language

The docs say Imprint is not a memory system, but future contributors will need concrete tests:

- Imprint may store artifact metadata needed to compile and audit profiles.
- Imprint should not become a recall API for arbitrary facts.
- Imprint should not retrieve memories to answer user questions.
- Imprint should not store more raw content than needed for compilation.

Sprint 02 should encode this in schema names and export modes.

### 2. Publishing Boundary Needs Consumer Examples

The architecture says publishing systems apply voice. That is correct. The gap is that a future
export contract could accidentally become a drafting prompt with content-generation behavior.

Guardrail: exports may describe expression rules, constraints, anti-patterns, and platform fit.
They should not include draft-generation workflows as core product behavior.

### 3. Clone and Persona Boundary Needs Stronger Refusal Language

The profile theory forbids diagnosis and intent attribution. It should also avoid "digital twin"
claims. Imprint can export expression profiles for agent systems, but it must not claim to model a
person's mind, values, consciousness, or future choices.

## Public-First Gaps

### 1. Git History Audit Is Still Required

The working tree is public-oriented, but public safety requires history inspection before launch.
The current docs acknowledge this. It remains a release gate.

### 2. Missing Contributor-Facing Policy Files

Architecture docs mention `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.
They are not visible in the current root listing. This is not a schema blocker, but it is a public
release blocker.

### 3. Example Profile Policy Needs More Detail

The docs say synthetic examples only. Sprint 02 should define what makes an example safely
synthetic:

- fictional names
- fictional organizations
- no transformed private snippets
- no real message cadence copied from a private corpus
- no private source names preserved in metadata

## Profile Theory Gaps

### 1. Identity Is Underdefined

The `Identity -> Expression -> Voice` model is useful, but "identity" could invite overclaiming.
For Imprint, identity should mean observable expression posture and stable self-presentation
metadata, not personality, psychology, or biography.

### 2. Interpretation Needs Machine-Readable Labels

The docs define Observation > Interpretation > Diagnosis. Sprint 02 should require every signal to
declare its claim level:

- observation
- bounded interpretation
- prohibited diagnosis, which must fail validation or be quarantined

### 3. Master and Derived Profiles Need Clear Merge Rules

The docs endorse a master profile plus derived profiles. Sprint 02 should decide whether derived
profiles inherit, override, or separately compile dimensions. Without this, downstream consumers
may receive contradictory guidance.

## First-Run Gaps

`What Imprint Learned` is the right first meaningful user experience. The gap is sequencing.

The first run should generate:

- source summary
- included/quarantined/excluded counts
- strongest observations with support metadata
- context differences where evidence is sufficient
- confidence caveats
- one canonical profile artifact

The first run should wait on:

- drift claims without a baseline
- personality labels
- raw excerpts by default
- downstream-specific persona cards
- private connector setup
- multi-profile merge features

## Competitive Gap

The competitor set confirms demand for voice, brand, memory, clone, and originality workflows.
Imprint's gap is not a missing market feature. It is a trust boundary:

- It should be more inspectable than writing assistants.
- It should be less expansive than clone products.
- It should store less than memory systems.
- It should be more portable than brand voice settings inside one SaaS.
- It should treat AI-detection as uncertain evidence, not a verdict.

## Sprint 02 Readiness

Sprint 02 can begin safely.

Required Sprint 02 guardrails:

- Define exact schema semantics before Pydantic implementation.
- Require support metadata for every signal.
- Make claim level explicit.
- Make sample policy explicit.
- Make authorship origin explicit.
- Make source weighting dimension-specific.
- Make version and migration policy first-class.
- Validate public-safe mode as the default.
