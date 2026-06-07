# Sprint 07 Architecture Review: Exports and First-Run Experience

**Reviewer:** Codex acting as hostile principal architect  
**Status:** Post-implementation gate review  
**Context:** Evaluation of Sprint 07 export and first-run experience work against public-safe export boundaries, claim safety, version preservation, Mosvera separation, determinism, and Sprint 08 readiness.

## Executive Summary

Sprint 07 delivers a deterministic public-safe export layer for compiled Imprint profiles. The implementation adds canonical JSON, human-readable Markdown, first-run “What Imprint Learned,” and Mosvera expression overlay exports. Shared safety validation rejects prohibited claims, ungated bounded interpretations, non-durable durable support, mixed signal model versions, path-like source IDs, and generation-control fields.

**Verdict: GO for Sprint 08**

Sprint 08 downstream integration work can begin if it treats Sprint 07 exports as contracts and keeps prompt assembly, generation settings, publishing workflow, and runtime adapter behavior outside core Imprint.

## Review Scope

Reviewed:

- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/sprints/SPRINT_07.md`
- `src/imprint/exports/`
- `src/imprint/compiler/`
- `tests/test_exports.py`
- full test suite output

## Findings

### 1. Export Safety

**Status: PASS**

The shared safety layer in `src/imprint/exports/safety.py` validates public export profiles before payload construction. It rejects:

- prohibited claims
- quarantined claims
- bounded interpretations unless explicitly allowed
- non-durable support exported as durable evidence
- mixed signal model versions inside a support object
- path-like or non-opaque source IDs
- generation-control keys such as `prompt`, `temperature`, and `model_hint`

Tests verify that JSON, Markdown, first-run, and Mosvera outputs do not contain raw fixture text, source filenames, or fixture paths.

**Resolved issue:** Sprint 07 does not reuse `ProfileExport` alone as a safety boundary. It adds explicit recursive validation before output.

### 2. Claim Boundaries

**Status: PASS**

Exports preserve expression-pattern-only scope by projecting compiled claims directly and by using conservative framing in Markdown and first-run outputs:

- “Observed pattern”
- “Supported by N included artifacts”
- “Confidence summarizes support strength”
- “What Imprint Cannot Say”

The first-run output explicitly says Imprint cannot diagnose, infer intent, prove identity traits, or expose raw evidence. Tests assert that prohibited claims cannot export and that bounded interpretations remain policy-gated.

**Resolved issue:** The first-run output is useful without becoming a personality report or writing assistant.

### 3. Version Compatibility

**Status: PASS**

Canonical JSON preserves:

- compiler version
- classifier versions
- signal model versions
- schema version
- export schema version
- compatibility warnings

Mixed signal model versions are rejected by export safety if they appear in exported support. Mixed classifier versions are recorded rather than hidden.

**Recommendation:** Sprint 08 should decide whether mixed classifier versions require consumer-facing warnings in every downstream projection, not just canonical JSON.

### 4. First-Run Experience

**Status: PASS**

`first_run_summary(profile)` uses compiled profile data only. It reports profile overview, strongest observed patterns, limitations, and non-claims. It does not read raw artifacts, generate demo prose, or introduce provider behavior.

**Resolved issue:** The first-run experience is not raw JSON and does not overstate certainty.

### 5. Mosvera Boundary

**Status: PASS**

`mosvera_expression_overlay(profile)` emits a contract fragment only:

- overlay version
- source profile metadata
- no-raw-text evidence policy
- expression summaries
- avoid patterns
- boundary statement

It does not include provider prompts, image generation instructions, runtime behavior, raw evidence, or aesthetic-intent compilation.

**Resolved issue:** Imprint remains the expression compiler; Mosvera remains responsible for aesthetic intent and runtime behavior.

### 6. Determinism and Provider Neutrality

**Status: PASS**

The exporters are deterministic: tests compare repeated JSON and Markdown outputs. Static scan of `src/imprint/exports/` and `tests/test_exports.py` found no provider imports, HTTP clients, socket use, subprocess use, embeddings, API keys, or environment access.

The CLI smoke path works through the local compile pipeline and selected export format.

### 7. Documentation

**Status: PASS**

Sprint 07 added or updated:

- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/sprints/SPRINT_07.md`
- Sprint 07 narrative closeout doc

Docs clearly distinguish core export contracts from downstream adapter behavior.

## Unresolved Blockers

None for Sprint 08.

## Recommendations Before Sprint 08

1. Keep downstream prompt assembly outside core Imprint.
2. Treat canonical JSON as the source of truth for downstream projections.
3. Add consumer-specific export tests before any publishing or Mosvera runtime integration.
4. Preserve the no-raw-text public-safe boundary when adding YAML or file-output variants.
5. Decide whether classifier-version warnings should become mandatory in every consumer-facing export.

## Gate Decision

**GO for Sprint 08.**

Sprint 07 satisfies the export safety, claim boundary, version compatibility, first-run, Mosvera boundary, determinism, provider-neutrality, documentation, and test gates required for downstream integration planning.
