# Sprint 06 Implementation Plan - Profile Compiler

Status: implementation-ready plan  
Primary prompt: `docs/sprints/SPRINT_06_PROMPT.md`  
Adversarial gate to anticipate: `docs/sprints/SPRINT_06_ADVERSARIAL_PROMPT.md`

## Summary

Sprint 06 implements deterministic profile compilation from Sprint 05 signal candidates.

The compiler aggregates only durable, validated artifact-level observations into profile-level
expression patterns. It preserves evidence, confidence, versioning, and privacy boundaries. It does
not create first-run reports, publishing prompts, downstream writing instructions, private
connectors, provider code, embeddings, or LLM calls.

The plan is designed so the hostile Sprint 06 architecture review can answer “GO for Sprint 07”
without needing to infer intent from code.

## Required Inputs

Before implementation or audit, read:

- `docs/sprints/SPRINT_06_PROMPT.md`
- `docs/sprints/SPRINT_06_ADVERSARIAL_PROMPT.md`
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

## Implementation Scope

Implement:

- `src/imprint/compiler/` with a small deterministic compiler interface.
- A `ProfileCompiler.compile_profile(...)` entrypoint that accepts normalized artifacts,
  classification results, and artifact signal candidates.
- Strict signal eligibility filtering before any aggregation.
- Profile-level `Signal` and `Claim` objects using existing schemas where possible.
- `SignalSupport` metadata that preserves contributing signal IDs, artifact references, source
  IDs, source types, classification versions, signal versions, rule IDs, support counts, and
  limitations.
- A deterministic, named compiler confidence model.
- Build manifest integration that records compiler, classifier, extractor, policy, schema, export,
  artifact-store, and config-hash metadata.
- Minimal CLI integration only if it remains local, scoped, and provider-neutral.
- Documentation for compiler behavior, profile compilation rules, evidence policy, confidence
  formula, and version boundaries.
- Synthetic-fixture tests that prove safety gates, determinism, evidence preservation, and provider
  neutrality.

Do not implement:

- First-run report generation.
- Demo or sample article generation.
- Publishing prompts or downstream writing instructions.
- Remote APIs, LLM calls, embeddings, vector search, or provider-specific behavior.
- Psychological, diagnostic, personality, hidden-intent, or unsupported identity inference.
- Profile claims from quarantined, excluded, non-durable, or unreviewed bounded-interpretation
  signals.
- Raw text, snippets, filesystem paths, private local locators, or private corpus examples in
  public-safe profile output.

## Compiler Contract

### Inputs

`ProfileCompiler.compile_profile(...)` should take:

- `subject_id: str`
- `artifacts: list[Artifact]`
- `classifications: list[ArtifactClassificationResult]`
- `signal_candidates: list[ArtifactSignalCandidate]`
- optional `source_policy: SourcePolicy`
- optional policy flag for explicitly allowed bounded interpretations

The compiler must not read source files, raw artifact text, external services, environment secrets,
provider configuration, or private connector state.

### Outputs

The compiler should return an `ExpressionProfile` containing:

- stable `profile_id`
- `subject_id`
- `BuildManifest`
- `ArtifactStoragePolicy`
- `SourcePolicy`
- compiled profile-level `signals`
- corresponding `claims`
- bounded context-profile scaffolding only when it can be derived from safe classification/source
  metadata

The output must be serializable through existing Pydantic schemas and public-safe by default.

## Signal Eligibility Gate

Eligibility runs before aggregation and is the most important Sprint 06 safety boundary.

Compile only candidates where:

- `candidate.durable` is `true`
- `candidate.claim_level` is `observation`
- candidate evidence classification label is `included`
- the current classification result for the artifact is also `included`
- the candidate has a matching classification result and source ID
- source IDs pass path-like leak validation
- the signal model version is compatible with other durable support

Reject:

- `prohibited` candidates with a compiler error
- missing classification results with a compiler error
- candidate/classification source mismatches with a compiler error
- mixed durable signal model versions unless a future implementation explicitly partitions support
  or marks comparability limitations

Skip by default:

- `quarantined` candidates
- non-durable candidates
- excluded-artifact candidates
- `bounded_interpretation` candidates unless an explicit future policy permits review-gated
  inclusion

If bounded interpretations are ever explicitly allowed, compiled claims must carry review-based
validation metadata and remain visibly distinct from observations.

## Aggregation Rules

Group eligible candidates by:

- profile signal family
- candidate name
- observed feature
- extraction rule ID

Project artifact signal families into profile families:

- `structure` and `formatting` -> `structure`
- `lexical` -> `lexical`
- `tone_marker` -> `tone`
- `rhetorical_pattern` and `reasoning` -> `reasoning`
- `narrative` -> `narrative`
- `anti_pattern` -> `anti_pattern`

Emit one profile-level signal per deterministic group. Keep the baseline linear or near-linear:
single-pass eligibility, hash grouping, and sorted deterministic output. Do not add pairwise
cross-signal comparisons to the Sprint 06 baseline.

## Claim Construction

Profile-level claims must use expression-pattern wording only.

Allowed shape:

- “Across included artifacts, short paragraph structure appears in 3 artifacts.”
- “Across included artifacts, contrast framing appears in 2 artifacts.”
- “Across included artifacts, question markers appear in 1 artifact.”

Forbidden shape:

- “The subject is analytical.”
- “The subject is anxious.”
- “The subject prefers written communication.”
- “The subject is skeptical.”
- Any diagnostic, personality-typing, emotional-state, intent, values, capability, or identity
  claim.

Every compiled claim must include:

- `claim_level`
- decomposed `Confidence`
- `SignalSupport`
- `ClaimValidation`
- rule IDs used for validation
- rationale that names the compiler confidence model

## Evidence and Privacy Requirements

Every compiled pattern must preserve:

- compiled profile signal ID or pattern ID
- contributing signal IDs
- artifact IDs through `EvidenceReference.artifact_ref`
- opaque source IDs
- source types
- classification IDs
- classification model versions
- signal model versions
- extraction rule IDs
- included, excluded, and quarantined support counts where applicable
- confidence summary
- limitations and audit limitations

Every public-safe profile output must exclude:

- raw artifact text
- source snippets
- local filesystem paths
- private locators
- private source names
- provider prompts or generation controls

Use only aggregate support and opaque references in compiled profiles.

## Versioning and Comparability

The build manifest must record:

- schema version
- compiler version
- compiler confidence model version in documentation and validation rationale
- classifier version
- extractor family, major version, minor version, prompt version, and code/model version
- model provider/name/version as `None` for local rule baseline
- source policy version
- authorship policy version
- export schema version
- artifact store mode
- config hash
- profile-affecting model invocations if a future non-baseline path adds any

Signal extraction model/version is a compatibility boundary. The Sprint 06 baseline should reject
mixed durable signal model versions rather than silently merging them.

The adversarial review will check whether incompatible classification versions are handled safely.
The implementation should either reject mixed classifier versions or record them clearly in support
and manifest metadata with a conservative comparability posture.

## Confidence Model

Define a named deterministic compiler confidence model.

The display confidence must summarize support strength, not truth about a person. It should account
for:

- average attribution confidence from supporting candidates
- average authorship-origin confidence
- average extraction confidence
- average evidence strength
- source diversity
- policy fit
- support count through a bounded support factor

The formula must:

- be deterministic
- be documented
- use existing decomposed `Confidence` fields
- avoid statistical certainty language
- avoid hiding weak safety components behind a single display score

## Context Profiles

Sprint 06 may add minimal context profile scaffolding only when it can be derived from safe metadata
without introducing hidden inheritance or expensive recomputation.

Allowed:

- context labels based on public-safe `source_type`
- included/quarantined/excluded counts by source type
- explicit `source_filters`
- no divergences unless evidence support is implemented

Do not implement:

- hidden fallback from context profiles to master profile signals
- untested divergence claims
- context explosion beyond `SourcePolicy.max_context_profiles`
- source filters that expose private source names or local locators

## Code Shape

Preferred structure:

```text
src/imprint/compiler/
  __init__.py
  engine.py
  validation.py   # add only if validation grows beyond engine readability
  rules.py        # add only if aggregation rules become nontrivial
  models.py       # add only if existing schemas are insufficient
```

Keep the implementation small, deterministic, and boring. Use existing schemas first. Add schema
fields only when required to preserve Sprint 06 evidence/version metadata.

## CLI Scope

If CLI integration is added, provide a minimal command:

```text
imprint compile --source-type <adapter> --path <local-fixture-or-dir> --subject-id <opaque-id>
```

The command should run:

1. ingest
2. classify
3. extract signals
4. compile profile

The CLI may print a compact summary. It should not emit raw profile JSON by default unless a future
export mode handles public-safe serialization explicitly.

## Documentation Plan

Create:

- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`

Update as needed:

- `docs/README.md`
- `docs/PROFILE_STABILITY.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/VERSIONING_POLICY.md`
- `docs/PROFILE_THEORY.md`
- `docs/sprints/SPRINT_06.md`

Do not create `docs/SPRINT_06_ARCHITECTURE_REVIEW.md` during implementation. That file belongs to
the post-implementation adversarial review.

Create `docs/PROFILE_COMPILER_RISKS.md` only if doing an explicit self-review pass. Otherwise leave
risk generation to the adversarial reviewer.

## Test Plan

Add `tests/test_compiler.py` with synthetic fixtures only.

Required tests:

- durable observation candidates compile into profile signals
- excluded artifacts produce no profile support
- quarantined candidates do not support durable profile claims
- non-durable candidates do not support durable profile claims
- prohibited candidates are rejected
- bounded interpretations are excluded by default
- bounded interpretations require explicit review-gated policy if allowed
- support metadata includes artifact IDs, source IDs, rule IDs, classification versions, and signal
  model versions
- source IDs remain opaque
- raw fixture text does not appear in serialized public-safe profile output
- filesystem paths do not appear in serialized public-safe profile output
- compilation is deterministic across repeated runs
- incompatible signal model versions are rejected, partitioned, or marked non-comparable
- no LLM/provider calls are required
- CLI compile smoke test passes if CLI integration exists

Also run the existing suite:

```text
pytest -q
```

If a formatter/linter is configured and available, run it without rewriting unrelated files.

## Adversarial Review Readiness Checklist

Before declaring Sprint 06 complete, verify:

- Claim boundaries: compiled claims remain expression-pattern-focused and contain no person-level,
  diagnostic, psychological, hidden-intent, or personality claims.
- Signal eligibility: quarantined, excluded, non-durable, prohibited, and unreviewed bounded
  interpretation candidates cannot become durable profile support.
- Evidence discipline: each compiled pattern preserves contributing signal IDs, artifact IDs,
  source IDs, rule IDs, classification versions, signal versions, support counts, confidence, and
  limitations.
- Version compatibility: mixed signal model versions are not silently merged; mixed classifier
  versions are either safely represented or rejected.
- Privacy: serialized profiles avoid raw text, paths, snippets, private locators, and non-opaque
  source IDs by default.
- Determinism and provider neutrality: no remote calls, provider imports, LLM invocations,
  embeddings, or nondeterministic ordering.
- Scalability: baseline compilation is single-pass/grouping-based, not pairwise cross-signal
  analysis.
- Docs: compiler behavior, evidence policy, confidence model, versioning, and non-goals are
  documented.
- Tests: all new compiler tests and existing tests pass.

## Exit Criteria

Sprint 06 is complete only when:

- deterministic profile compilation exists
- only durable, validated observation signals compile by default
- signal model versioning is preserved in profile support metadata
- prohibited and quarantined claims cannot enter durable profiles
- profile patterns are evidence-backed
- public-safe profile output excludes raw text and paths
- no providers, LLMs, or embeddings are introduced
- docs describe implemented compiler rules
- all tests pass
- no implementation artifact preempts the separate adversarial review

## Sprint 07 Handoff

Sprint 07 exports may begin only after the adversarial review produces a GO decision or identifies
only non-blocking recommendations.

Known handoff items for Sprint 07:

- canonical Imprint JSON/YAML export from compiled `ExpressionProfile`
- Mosvera-compatible fragment projection
- export validation against public-safe evidence and generation-control boundaries
- first-run/report work remains separate from Sprint 06 and should not reuse compiler internals as
  prompt assembly logic
