# Sprint 08 Architecture Review: Consumer Contracts and Integration Surfaces

**Reviewer:** Codex acting as hostile principal architect  
**Status:** Post-implementation gate review  
**Context:** Evaluation of Sprint 08 consumer contract work against downstream-boundary preservation,
consumer warning visibility, no-raw-text privacy, opaque source IDs, and Sprint 09/10 readiness.

## Executive Summary

Sprint 08 delivers deterministic consumer contract projections for Mosvera, Broadside, agents/apps,
and human/CLI inspection. The implementation keeps canonical JSON as the source of truth and adds a
small `src/imprint/consumers/` layer that narrows canonical public-safe data into consumer-specific
views.

**Verdict: GO for Sprint 09/10 planning**

The sprint avoids real integrations. It does not add Mosvera runtime behavior, Broadside API calls,
publishing workflow logic, prompt assembly, provider-specific model configuration, remote APIs, LLM
calls, embedding search, image generation instructions, or UI/dashboard behavior.

## Review Scope

Reviewed:

- `docs/CONSUMER_CONTRACTS.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/BROADSIDE_INTEGRATION.md`
- `docs/AGENT_CONSUMER_CONTRACT.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/EXPORT_FORMATS.md`
- `src/imprint/consumers/`
- `src/imprint/exports/`
- `src/imprint/cli.py`
- `tests/test_consumers.py`
- `tests/test_exports.py`
- full test suite output
- static scan for remote/provider/runtime terms in consumer/export code

## Findings

### 1. Boundary Preservation

**Status: PASS**

The implementation adds contract helpers only. Consumer payloads are derived from
`canonical_profile_export(profile)` and validated before return. No downstream system becomes part of
core Imprint.

Preserved exclusions:

- no prompt assembly
- no publishing workflows
- no provider settings
- no Mosvera runtime behavior
- no Broadside API behavior
- no image generation instructions
- no remote API calls

### 2. Canonical JSON Source of Truth

**Status: PASS**

All consumer projections flow through canonical JSON first. This preserves the Sprint 07 finding that
canonical JSON is the machine-readable source of truth. Consumer-specific contracts are views, not
new profile schemas.

### 3. Mosvera Boundary

**Status: PASS**

Mosvera receives expression summaries, avoid patterns, source profile metadata, opaque source IDs,
no-raw-text policy, and compatibility warnings. The boundary remains:

> Imprint compiles expression. Mosvera compiles aesthetic intent.

No aesthetic compilation, runtime adapter behavior, provider tuning, or visual-generation instruction
was added.

### 4. Broadside Boundary

**Status: PASS**

Broadside receives profile summary, observed expression patterns, support metadata, limitations, and
compatibility warnings. It does not receive article-generation prompts, editorial process logic,
publishing schedules, platform formatting, or model parameters.

### 5. Agent Safety

**Status: PASS**

The agent contract preserves warning metadata, no-raw-text policy, source IDs, limitations, and
explicit usage rules. Tests assert that confidence is not truth and that the projection includes safe
pattern lookup only.

### 6. Version Compatibility

**Status: PASS**

Sprint 08 makes compatibility warnings mandatory in every consumer-facing projection. The helper
surfaces compiler, classifier, signal, schema, export, and consumer contract versions. Tests verify
mixed classifier-version warnings appear in consumer projections.

The existing export safety policy still rejects mixed signal model versions within a support object.
Consumer warnings also surface multiple signal model versions across profile patterns when present.

### 7. Privacy and Source Safety

**Status: PASS**

Consumer payloads use opaque `source-*` IDs and preserve no-raw-text policy. The shared validator
rejects path-like strings and generation-control keys, now including `provider`.

Tests verify consumer payloads avoid raw fixture text, fixture filenames, paths, provider prompts,
image-generation language, and Broadside publishing logic.

### 8. Determinism and Local Execution

**Status: PASS**

The helpers are deterministic pure projections over canonical JSON. Static scan found no remote API,
socket, subprocess, hosted-provider SDK, or network client usage in the consumer/export code paths.

Validation evidence:

- `pytest -q` -> 82 passed
- `python3 -m compileall -q src` -> passed
- static term scan -> only forbidden terms in tests and validators

## Resolved Issues

1. Consumer-facing compatibility warnings are mandatory, not optional.
2. Mosvera overlay now preserves opaque source IDs and warning metadata.
3. Broadside has an explicit constraints-only contract.
4. Agent consumption has explicit safety rules for confidence, bounded interpretations, and durable
evidence.
5. Validators reject `provider` alongside prompt and generation-control fields.

## Unresolved Blockers

None for Sprint 09/10 planning.

## Recommendations Before Sprint 09/10

1. If future consumers need richer display payloads, keep them projections of canonical JSON.
2. Add a dedicated CLI validation command only when there is a real file-based export-validation UX.
3. Keep Mosvera runtime adapters and Broadside publication adapters outside core Imprint.
4. If profile comparison enters Sprint 09/10, pass explicit comparability state into consumer
warnings rather than inferring it locally.

## Gate Decision

**GO.**

Sprint 08 satisfies consumer contract, boundary preservation, warning visibility, privacy, and test
coverage requirements.
