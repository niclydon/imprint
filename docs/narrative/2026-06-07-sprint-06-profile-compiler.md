# Sprint 06 Narrative: Profile Compiler

## Status

Implemented and ready for adversarial review.

## Context

Sprint 05 and 05.5 produced deterministic, artifact-local signal candidates. Those candidates were
useful, but they were not yet reusable profiles. Sprint 06 added the missing aggregation layer:
turning durable artifact-level observations into public-safe expression profile patterns without
crossing into personality, diagnosis, intent, provider prompts, or downstream writing instructions.

The work was guided by `docs/sprints/SPRINT_06_IMPLEMENTATION_PLAN.md`, with the adversarial review
prompt kept in view so the implementation would be easy to audit later.

## Shipped Behavior

- Added `src/imprint/compiler/` with a deterministic `ProfileCompiler`.
- Added a `compile_profile(...)` contract that accepts normalized artifacts, classification
  results, and artifact signal candidates.
- Added strict eligibility gates before aggregation:
  - durable candidates only
  - included classification only
  - matching artifact, source ID, and classification ID
  - no prohibited claims
  - no quarantined, excluded, non-durable, or default bounded-interpretation support
  - no mixed durable signal model versions
- Added deterministic grouping by profile family, candidate name, observed feature, and rule ID.
- Added profile-level `Signal` and `Claim` construction with evidence-backed aggregate wording.
- Added minimal source-type context profile scaffolding with explicit filters and counts only.
- Added `imprint compile` as a local CLI summary flow: ingest -> classify -> extract -> compile.

## Evidence and Safety Boundaries

Compiled profile support now preserves:

- contributing signal IDs
- artifact references and opaque source IDs
- source types
- classification IDs
- classification model versions
- signal model versions
- extraction rule IDs
- support counts
- confidence and audit limitations

Public-safe profile output remains metadata-only by default. The compiler does not read raw artifact
text, source files, environment secrets, provider configuration, remote APIs, embeddings, or private
connector state.

The claim boundary is intentionally conservative. Profile claims use aggregate expression-pattern
language such as “Across included artifacts...” and do not infer psychology, diagnosis, hidden
intent, values, capability, or identity traits.

## Documentation and Traceability

Added:

- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`
- `docs/sprints/SPRINT_06_IMPLEMENTATION_PLAN.md`
- `tests/test_compiler.py`

Updated:

- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/PROFILE_STABILITY.md`
- `docs/PROFILE_THEORY.md`
- `docs/README.md`
- `docs/VERSIONING_POLICY.md`
- `docs/sprints/SPRINT_06.md`
- `src/imprint/cli.py`
- `src/imprint/schemas/models.py`

## Test Coverage

The compiler test suite verifies:

- durable observations compile
- excluded artifacts produce no support
- quarantined and non-durable candidates do not support profile claims
- prohibited candidates are rejected
- bounded interpretations are excluded by default and review-gated if explicitly allowed
- support metadata preserves IDs, versions, rules, and source references
- raw fixture text and paths do not appear in serialized profile output
- compilation is deterministic
- incompatible signal model versions are rejected
- path-like source IDs are rejected
- missing artifact/classification links and classification mismatches are rejected
- no provider or LLM dependencies appear in the profile manifest
- CLI compile smoke path works

Final validation: `pytest -q` passed with 61 tests.

Ruff is configured in `pyproject.toml`, but unavailable in this environment:
`python3 -m ruff check .` reports `No module named ruff`.

## What Remains for Adversarial Review

Sprint 06 intentionally did not create `docs/SPRINT_06_ARCHITECTURE_REVIEW.md` or
`docs/PROFILE_COMPILER_RISKS.md`. Those belong to a separate hostile review pass.

The reviewer should focus on:

- whether claim boundaries stayed expression-pattern-only
- whether eligibility gates are strict enough
- whether evidence/version metadata is complete
- whether mixed classifier versions should be rejected instead of recorded
- whether context scaffolding is too permissive for Sprint 07 exports
- whether the compiler confidence formula is conservative enough

## Handoff to Sprint 07

Sprint 07 should build export projections from compiled `ExpressionProfile` objects. The next
natural deliverables are canonical Imprint JSON/YAML and a Mosvera-compatible fragment. Export work
must keep prompt assembly, generation controls, first-run reports, and downstream writing behavior
outside the Sprint 06 compiler.
