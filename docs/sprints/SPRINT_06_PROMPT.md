# Sprint 06 Prompt - Profile Compiler

Use this prompt with GPT 5.5 for design first. If implementation is approved, use GPT 5.4 for code changes.

---

You are implementing Sprint 06 for Imprint.

Sprint 06 builds the profile compiler. This is the first layer that aggregates artifact-level signals into reusable expression profiles, so it must be conservative, evidence-backed, versioned, and strict about claim boundaries.

## Required Reading

Read before making changes:

- `docs/sprints/SPRINT_06.md`
- `docs/SPRINT_05_ARCHITECTURE_REVIEW.md`
- `docs/SIGNAL_EXTRACTION_DESIGN.md`
- `docs/SIGNAL_EXTRACTION_RULES.md`
- `docs/SIGNAL_TAXONOMY.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/CONFIDENCE_MODEL.md`
- `docs/PROFILE_STABILITY.md`
- `docs/VERSIONING_POLICY.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/SCHEMA.md`
- `docs/SCHEMA_RISKS.md`
- `src/imprint/classification/`
- `src/imprint/signals/`
- `src/imprint/schemas/`
- `tests/test_classification.py`
- `tests/test_signals.py`
- `tests/test_schemas.py`

## Mission

Implement deterministic profile compilation from signal candidates.

The compiler should aggregate durable artifact-level observations into profile-level expression patterns while preserving evidence, confidence, versioning, and safety boundaries.

Sprint 06 does **not** generate first-run reports, demo artifacts, publishing prompts, or downstream writing instructions.

## Core Rule

Profiles may summarize supported expression patterns. Profiles must not invent person-level psychological, diagnostic, or intent claims.

Good profile-level claim:

- “Across included artifacts, short paragraph structure appears frequently.”
- “Contrast framing appears in multiple included artifacts.”
- “Question markers appear in a minority of included artifacts.”

Bad profile-level claim:

- “The subject is analytical.”
- “The subject is anxious.”
- “The subject prefers written communication.”
- “The subject is skeptical.”

## Sprint 05 Carry-Forward Constraints

The Sprint 05 architecture review approved signal extraction for Sprint 06 with these constraints:

1. Add or preserve `signal_model_version` in compiled profile support metadata.
2. Treat signal extraction model/version as a compatibility boundary.
3. Enforce claim-level validation before any signal enters a compiled profile.
4. Reject `PROHIBITED` signals.
5. Treat `BOUNDED_INTERPRETATION` signals as review-gated unless explicitly allowed by policy.
6. Exclude quarantined and non-durable signals from durable profile support.
7. Preserve opaque source IDs.
8. Do not expose raw private text in public-safe profile output.
9. Add validation against path-like source IDs if feasible.
10. Document confidence formula/version compatibility in the compiler output.

## Required Implementation Scope

Allowed:

- profile compiler interfaces
- deterministic aggregation of durable signals
- profile support/evidence summaries
- profile confidence summaries
- signal family aggregation
- profile build manifest integration
- claim-level validation gate
- tests using synthetic fixtures
- docs for compiler behavior and evidence policy
- minimal CLI integration if clean and scoped

Forbidden:

- first-run report generation
- demo article generation
- publishing prompt generation
- remote APIs
- LLM calls
- embeddings/vector search
- provider-specific code
- psychological/diagnostic inference
- profile claims based on quarantined artifacts
- raw private text in public-safe output

## Profile Compilation Requirements

### 1. Signal Eligibility

Only durable signals may support compiled profiles.

Do not compile:

- excluded-artifact signals
- quarantined signals
- non-durable candidate signals
- prohibited claims
- bounded interpretations without explicit policy approval

### 2. Claim Validation Gate

Before profile aggregation, validate every signal claim level.

Required behavior:

- `observation` may compile if durable and supported
- `quarantined` must not compile into durable support
- `prohibited` must fail compilation or be rejected
- `bounded_interpretation` must be review-gated or excluded by default

### 3. Evidence Preservation

Every compiled profile pattern must include support metadata:

- profile pattern ID
- contributing signal IDs
- artifact IDs
- opaque source IDs
- source types
- classification model versions
- signal model versions
- rule IDs
- support counts
- confidence summary
- limitations

### 4. Signal Model Versioning

The compiler must preserve or expose the signal extraction model/version used to produce supporting signals.

If signals from incompatible signal model versions are mixed, the compiler must either:

- reject compilation,
- mark the profile as partially comparable,
- or clearly partition support by version.

Do not silently merge incompatible signal model versions.

### 5. Confidence Summary

Profile confidence must summarize support strength. It must not imply truth about a person.

Confidence should account for:

- number of supporting durable signals
- classification confidence compatibility
- signal confidence compatibility
- source diversity if available
- limitations and exclusions

Keep the confidence calculation deterministic and versioned.

### 6. Privacy

Compiled profiles must remain public-safe by default.

Do not include:

- raw artifact text
- filesystem paths
- private local locators
- source snippets unless explicitly marked private/local and excluded from public export

### 7. Performance

Keep baseline compilation linear or near-linear in number of signals.

Do not add cross-signal quadratic analysis to the baseline path.

## Test Requirements

Add tests proving:

- only durable observation signals compile
- quarantined signals do not support profiles
- prohibited signals fail or are rejected
- bounded interpretations are not compiled by default
- profile support metadata includes artifact IDs, source IDs, rule IDs, classification versions, and signal model versions
- opaque source IDs remain opaque
- raw text does not appear in public-safe compiled profile output
- compilation is deterministic
- incompatible signal model versions are rejected, partitioned, or marked non-comparable
- no LLM/provider calls are required

## Documentation Requirements

Create or update:

- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`
- `docs/PROFILE_COMPILER_RISKS.md` only if doing self-review, otherwise leave adversarial review to Gemini/Claude

Update as needed:

- `docs/PROFILE_STABILITY.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/VERSIONING_POLICY.md`
- `docs/PROFILE_THEORY.md`
- `docs/sprints/SPRINT_06.md`

## Expected Code Shape

Prefer a structure like:

```text
src/imprint/compiler/
  __init__.py
  engine.py
  rules.py
  models.py   # only if schema objects are not already sufficient
  validation.py
```

Keep implementation small, deterministic, and boring.

## Exit Criteria

Sprint 06 is complete only if:

- deterministic profile compilation exists
- only durable, validated observation signals compile by default
- signal model versioning is preserved in profile support metadata
- prohibited and quarantined claims cannot enter durable profiles
- profile patterns are evidence-backed
- public-safe profile output excludes raw text and paths
- no providers, LLMs, or embeddings are introduced
- docs describe implemented compiler rules
- all tests pass

At the end, summarize:

- files changed
- tests run
- compiler behavior implemented
- non-goals preserved
- remaining blockers for Sprint 07 exports / first-run experience
