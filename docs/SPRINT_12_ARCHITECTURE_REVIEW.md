# Sprint 12 Architecture Review: Evaluation and Quality Gates

**Reviewer:** Codex acting as hostile release/security architect
**Status:** Post-implementation gate review
**Context:** Evaluation of Sprint 12 validation, comparison, regression, and release-gate work.

## Executive Summary

Sprint 12 adds deterministic quality gates for public-safe profile exports. The implementation gives
operators two concrete commands:

```bash
imprint validate-export <file>
imprint diff profile-a.json profile-b.json
```

The validator fails closed on malformed exports, raw/private content fields, path-like values,
credential-like values, invalid source IDs, missing compatibility metadata, missing mandatory
consumer warnings, prohibited claims, and prompt/provider/generation-control leakage.

The comparison command validates both inputs, computes schema-level comparability from build
manifests, separates expression drift from compiler/corpus/schema drift, and refuses to present
not-comparable changes as expression drift.

**Verdict: GO for Sprint 13 private adapter strategy.**

## Review Scope

Reviewed:

- `src/imprint/quality.py`
- `src/imprint/cli.py`
- `tests/test_quality_gates.py`
- `tests/fixtures/regression/sprint12/`
- `docs/VALIDATION.md`
- `docs/PROFILE_COMPARISON.md`
- `docs/QUALITY_GATES.md`
- `docs/REGRESSION_CORPUS.md`
- `docs/RELEASE_CHECKLIST.md`
- existing export, consumer, schema, connector, and onboarding tests

## Findings

### 1. False PASS Validation Risk

**Status: PASS**

Validation emits explicit check objects and fails the release gate on privacy, schema, compatibility,
source-ID, and consumer-contract failures. Tests mutate generated exports to prove raw text/path,
invalid source IDs, and missing compatibility metadata fail.

### 2. Privacy Leak Coverage

**Status: PASS**

The validator scans recursive JSON values for raw/private content fields, path-like strings,
credential-like strings, DSNs, and existing export-safety forbidden keys. It also validates source IDs
through the existing opaque source-ID rule.

### 3. Consumer Compatibility Warnings

**Status: PASS**

Consumer contracts and Mosvera overlays must include evidence policy and mandatory compatibility
warnings. Missing warnings fail validation where warnings are required.

### 4. Profile Comparison Overclaiming

**Status: PASS**

Comparability is computed through the existing `ComparabilityResult.from_manifests` schema contract.
Changed corpus fingerprints produce `NOT_COMPARABLE`. The report sets
`implementation_drift_reported_as_expression` to false and suppresses expression drift for
not-comparable profiles.

### 5. Regression Corpus

**Status: PASS**

The executable regression path uses synthetic Sprint 11 example outputs plus Sprint 12 mutation tests.
No private data or real source files were introduced.

## Validation Evidence

- `pytest -q tests/test_quality_gates.py` -> passed
- `pytest -q` -> 109 passed
- `python3 -m compileall -q src` -> passed
- clean temp-venv `pip install -e ".[test]"` -> passed
- clean temp-venv `imprint example` -> generated canonical, Markdown, first-run, Mosvera, and human CLI outputs
- clean temp-venv `imprint validate-export` -> passed for canonical JSON, Mosvera overlay, and human CLI consumer contract
- clean temp-venv `imprint diff` -> reported `COMPARABLE` and did not report implementation drift as expression drift
- tracked-file public-safety scan -> no private data or credential-pattern hits

## Resolved Issues

1. Added machine-readable validation reports.
2. Added public-safe JSON export and consumer contract validation.
3. Added deterministic profile comparison reports.
4. Added drift categorization for compiler, corpus, schema, and expression drift.
5. Added synthetic regression corpus marker and quality-gate tests.
6. Added release-gate documentation and checklist entries.

## Unresolved Blockers

None for Sprint 13.

## Recommendations Before `v0.1.0`

1. Run `validate-export` against all generated JSON release artifacts.
2. Add a CI step that runs `imprint example` and validates generated outputs.
3. Keep comparison conservative until there is a formal corpus-equivalence registry.
4. Avoid adding subjective quality scoring until the deterministic gates stay stable.

## Gate Decision

**GO.**

Sprint 12 satisfies the validation, comparison, regression, privacy, compatibility, and release-gate
requirements for the developer preview.
