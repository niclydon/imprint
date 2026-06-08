# Sprint 12.5 - Quality Gate Hardening

Primary Model: GPT 5.5 for design and review, GPT 5.4 for implementation
Adversarial Reviewer: Gemini Antigravity or GPT 5.5
Status: Required before Sprint 13 or v0.1.0 release work

## Mission

Close the Sprint 12 adversarial review blockers before any private-adapter strategy work or public release tagging proceeds.

Sprint 12 successfully established validation, comparison, and release-gate infrastructure, but the adversarial review identified privacy-gate bypasses that undermine the public-safe export guarantees. Sprint 12.5 exists to harden those gates.

## Required Reading

- `docs/SPRINT_12_ARCHITECTURE_REVIEW.md`
- `docs/sprints/SPRINT_12.md`
- `docs/VALIDATION.md`
- `docs/PROFILE_COMPARISON.md`
- `docs/QUALITY_GATES.md`
- `docs/REGRESSION_CORPUS.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/EXPORT_FORMATS.md`
- `src/imprint/quality.py`
- `src/imprint/exports/safety.py`
- `tests/test_quality_gates.py`
- `tests/test_exports.py`

## Blocking Issues to Fix

### 1. JWT credential detection

Quality and export validators must reject JWT-shaped credentials.

Add detection for three-segment base64url token shapes such as:

```text
eyJ...eyJ...signature
```

Requirements:

- update shared credential detection where possible
- apply consistently to quality gates and export safety
- add tests proving JWTs fail validation

### 2. Base64-encoded credential detection

Validators must detect likely base64-encoded credential strings.

Requirements:

- scan plain strings first
- attempt safe bounded base64/base64url decoding for plausible strings
- rescan decoded content for credential patterns
- avoid excessive decoding, recursion, or false positives on short ordinary strings
- add tests proving encoded credentials fail validation

### 3. Percent-encoded path detection

Validators must reject encoded path separators and path-like values.

Requirements:

- detect `%2F`, `%2f`, `%5C`, `%5c`
- optionally URL-decode candidate values and rescan for path patterns
- add tests for Unix and Windows encoded paths

### 4. Root-level underscore metadata rejection

Public-safe canonical exports must not allow root-level private-looking fields such as:

- `_metadata`
- `_internals`
- `_debug`
- `_private`

Requirements:

- reject root-level underscore-prefixed keys in public-safe export validation
- decide whether nested underscore fields are allowed only in explicitly documented safe schema fields; default should be conservative
- add tests proving underscore metadata cannot bypass forbidden-key validation

### 5. Regression coverage for mixed classifier versions

Add regression tests for profile comparison and release gates involving mixed classifier versions.

Requirements:

- comparison output must expose mixed classifier versions
- release gate must not silently mark semantically ambiguous outputs as fully comparable
- validation report should include structured reason codes

## Major Recommendations to Address or Explicitly Defer

### Provider/model metadata future-proofing

Do not fully implement provider drift unless already modeled cleanly. But document the future compatibility requirement so Sprint 13+ does not accidentally erase it.

### Machine-readable release gate reasons

If practical, add structured fields such as:

- `blocking_failures`
- `required_reviews`
- `reason_codes`

At minimum, document this as required before release automation.

## Implementation Guidance

Prefer shared helper functions over duplicated regex logic. If `quality.py` and `exports/safety.py` both contain similar validation logic, either centralize it or make sure tests prove the behavior is consistent.

Validation should fail closed. False negatives are more dangerous than occasional conservative failures for v0.1.0.

## Non-Goals

Do not implement:

- private adapters
- service/API mode
- LLM judges
- subjective voice scoring
- provider drift modeling beyond documentation unless trivial
- broad schema redesign
- web UI

## Test Requirements

Add or update tests proving:

- JWT tokens fail export validation
- JWT tokens fail quality-gate privacy checks
- base64-encoded credentials fail validation
- base64url-encoded credentials fail validation if supported
- percent-encoded Unix paths fail validation
- percent-encoded Windows paths fail validation
- root-level underscore metadata fails validation
- forbidden keys nested under underscore metadata cannot bypass validation
- mixed classifier-version comparison produces appropriate warnings or comparability state
- all previous Sprint 12 tests still pass

## Documentation Requirements

Create or update:

- `docs/SPRINT_12_5_REMEDIATION_SUMMARY.md`
- `docs/VALIDATION.md`
- `docs/QUALITY_GATES.md`
- `docs/PROFILE_COMPARISON.md`
- `docs/RELEASE_CHECKLIST.md`

## Exit Criteria

Sprint 12.5 is complete only if:

- all three critical blockers from Sprint 12 are fixed
- underscore-prefixed metadata bypass is blocked
- mixed classifier-version regression coverage exists
- validation behavior is consistent across quality and export safety surfaces
- all tests pass
- the adversarial re-review produces GO for Sprint 13/v0.1.0 planning
