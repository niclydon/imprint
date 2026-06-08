# Sprint 12 - Evaluation, Validation, and Quality Gates

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Ready after Sprint 11 packaging and install experience

## Mission

Build the quality system that determines whether a profile, export, or release is trustworthy.

Sprint 12 is not about generating better profiles. Sprint 12 is about proving that generated profiles remain safe, comparable, deterministic, version-aware, and release-worthy.

The output of Sprint 12 should allow Imprint to answer:

- Is this export valid?
- Is this profile comparable to a previous profile?
- Did anything regress?
- Did privacy guarantees hold?
- Is this safe to release?

## Required Reading

- `docs/ROADMAP.md`
- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `src/imprint/compiler/`
- `src/imprint/exports/`
- `src/imprint/consumers/`
- `src/imprint/connectors/`
- `tests/`

## Core Goal

Make every profile and export measurable.

Introduce validation, comparison, compatibility analysis, regression testing, and release gating.

## Required Deliverables

### 1. Export validation

Implement or design:

```bash
imprint validate-export <file>
```

Validation must check:

- schema validity
- export version
- compiler version
- source ID format
- compatibility warnings
- no raw text leakage
- no filesystem path leakage
- no credential patterns
- consumer contract integrity

Output must be explicit: PASS or FAIL with reasons.

### 2. Profile comparison

Implement or design:

```bash
imprint diff profile-a.json profile-b.json
```

Compare:

- profile metadata
- compiler metadata
- classifier versions
- signal model versions
- schema/export versions
- signals and support counts
- confidence summaries
- compatibility warnings

Do not compare raw corpora.

### 3. Comparability state

Every comparison must produce one of:

- `COMPARABLE`
- `PARTIALLY_COMPARABLE`
- `NOT_COMPARABLE`

Reasons may include compiler version mismatch, classifier version mismatch, signal model mismatch, schema mismatch, export mismatch, corpus change, or missing metadata.

### 4. Regression corpus

Create a synthetic regression corpus that verifies:

- classification behavior
- signal extraction behavior
- compiler behavior
- export behavior
- consumer projection behavior
- connector dry-run behavior if useful

Synthetic only. No private data. No real writing samples.

### 5. Validation reports

Generate machine-readable validation reports with:

- status
- comparability state
- warnings
- privacy checks
- version checks
- schema checks
- release-gate summary

### 6. Release gates

A release candidate must fail if:

- raw text leaks
- source IDs are invalid
- exports are invalid
- schemas regress
- compatibility metadata disappears
- privacy guarantees weaken
- prohibited claims or prompt/provider fields leak into public-safe outputs

### 7. Drift detection

Detect and separate:

- compiler drift
- classifier drift
- signal-model drift
- corpus drift
- schema/export drift

Do not present implementation drift as expression drift.

## Documentation Requirements

Create or update:

- `docs/VALIDATION.md`
- `docs/PROFILE_COMPARISON.md`
- `docs/QUALITY_GATES.md`
- `docs/REGRESSION_CORPUS.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/ROADMAP.md`

## Non-Goals

Do not implement:

- LLM judges
- subjective voice scoring
- human review workflows
- model benchmarking
- publishing workflows
- private adapters
- service mode
- web UI

## Test Requirements

Add tests proving:

- export validation works
- profile comparison works
- comparability states work
- regression corpus executes
- privacy checks work
- release gates work
- version mismatches are detected
- drift detection separates software changes from expression changes

## Exit Criteria

Sprint 12 is complete only if:

- exports can be validated
- profiles can be compared
- comparability states exist
- regression corpus exists
- release gates exist
- privacy regressions fail tests
- version regressions fail tests
- all tests pass
