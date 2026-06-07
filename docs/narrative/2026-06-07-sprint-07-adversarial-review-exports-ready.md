# Sprint 07 Narrative: Adversarial Review — Export Layer and First-Run Experience Readiness

**Date:** 2026-06-07  
**Status:** Adversarial review complete, GO verdict for Sprint 08  
**Reviewer:** Claude (Adversarial Principal Architect)

---

## Context

Sprint 07 shipped four deterministic, public-safe export formats for compiled Imprint profiles: canonical JSON, human-readable Markdown, first-run "What Imprint Learned," and a Mosvera expression overlay contract. The core risk was not serialization itself—it was ensuring that every upstream safety boundary from ingestion through profile compilation remained intact in the export layer.

This narrative records the adversarial review that validated export safety, claim boundaries, version metadata preservation, first-run clarity, Mosvera boundary enforcement, and determinism.

---

## Review Scope

The adversarial review examined:

1. **Export safety** — Do any export formats leak raw text, filesystem paths, or private metadata?
2. **Claim boundaries** — Did exports preserve expression-pattern-only scope, or did person-level psychological claims slip through?
3. **Version compatibility** — Are compiler, classifier, and signal model versions preserved and visible?
4. **First-run experience** — Is the "What Imprint Learned" output useful and clear without overstating certainty?
5. **Mosvera boundary** — Is the overlay a contract/fragment only, with no provider prompts or aesthetic-intent compilation?
6. **Determinism and provider neutrality** — Are there any LLMs, embeddings, remote calls, or provider-specific assumptions?

Supporting evidence:

- `src/imprint/exports/` (5 modules: `__init__.py`, `json_export.py`, `markdown_export.py`, `first_run.py`, `mosvera.py`, `safety.py`)
- `tests/test_exports.py` (10 comprehensive tests)
- `docs/EXPORT_FORMATS.md`, `docs/FIRST_RUN_OUTPUT.md`, `docs/MOSVERA_INTEGRATION.md`, `docs/EXPORT_BOUNDARIES.md`
- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md` (detailed findings)

---

## Key Findings

### 1. Export Safety: All Formats Validated

**Verdict: PASS**

All public-safe exports validate before returning output. The shared safety layer (`safety.py`) enforces:

- **Prohibited claims rejected.** Any claim marked `PROHIBITED` raises `ExportSafetyError` immediately.
- **Quarantined support excluded.** Signals with quarantined or excluded artifact counts are rejected.
- **Non-durable evidence blocked.** Only durable signals from included artifacts can export.
- **Mixed signal model versions rejected.** If a signal has multiple signal model versions in its support, export fails.
- **Path-like source IDs rejected.** Source IDs must match `^source-[A-Za-z0-9_-]+$` and cannot contain `/`, `\`, `..`, or Windows drive letters.
- **Generation-control fields blocked.** Fields like `prompt`, `temperature`, `model_hint`, `top_p`, `system_prompt` cannot appear in exports.
- **Raw text and paths removed.** Recursive scan of all exported payloads rejects path-like strings.

Test evidence: `test_public_safe_exports_contain_no_raw_text_or_paths` runs all four export formats and verifies no raw fixture text ("Start here"), no filenames ("signal-transcript.json"), and no fixture paths ("/tests/fixtures/") leak.

**Observed:** The safety layer is strict and early: it validates the profile *before* serialization, not after. This prevents subtle payload-construction bugs from creating exfiltration vectors.

### 2. Claim Boundaries: Expression-Pattern-Only Scope Preserved

**Verdict: PASS**

All exports reject prohibited claims and use conservative, evidence-scoped language:

- **JSON export:** Projects claim text from the compiler directly (which is always "Across included artifacts, ..."). Includes validation methods and rule IDs, but never assertion logic.
- **Markdown export:** Uses "Observed pattern: {name}" language, confidence and support counts. Footer explicitly states "Confidence summarizes support strength, not truth about a person."
- **First-run export:** Opens with "compiled a public-safe expression profile from normalized, classified, and validated signal metadata. It did not use raw artifact text." Explicitly states "cannot diagnose, infer intent, or prove identity traits" and "cannot say what the subject is, feels, wants, believes, or intends."
- **Mosvera overlay:** Summaries labeled "observed_expression_pattern," no psychological or diagnostic claims.

Test evidence: `test_prohibited_claims_cannot_export_even_if_profile_is_mutated` creates a prohibited claim and verifies export fails. `test_markdown_export_is_deterministic_and_conservative` verifies no "The subject is...", "Personality...", or over-confident language appears.

**Observed:** The claim text template from the compiler (`"Across included artifacts, {observed_feature} appears in {count} {label}."`) makes person-level claims structurally impossible. Downstream systems cannot accidentally interpret "short paragraphs" as "the subject is brief."

### 3. Version Compatibility: Metadata Fully Recorded

**Verdict: PASS**

Version metadata is preserved in all machine-readable exports:

**Canonical JSON:**
- Compiler version (from build manifest)
- Classifier versions (collected from all signals, comma-separated if mixed)
- Signal model versions (collected from all signals)
- Schema version and export schema version
- Warnings if multiple classifier versions are present

**Markdown:**
- Compiler version and export schema version in basis section
- Classifier and signal model versions in compatibility section
- Warnings (e.g., "multiple classifier versions are represented in support metadata")

**Mosvera overlay:**
- Source profile ID, compiler version, and signal model versions in metadata

**Safety enforcement:** Mixed signal model versions are rejected by export validation (line 83 in `safety.py`). Mixed classifier versions are allowed but explicitly warned. This asymmetry is intentional: signal model version changes have semantic implications; classifier version changes may be backward-compatible.

Test evidence: `test_incompatible_signal_versions_cannot_export_as_comparable` mutates a signal's support to include mixed signal model versions and verifies export fails with "mixed signal model versions cannot export."

**Observed:** Downstream systems can audit comparability without needing to reconstruct version information from other sources. The explicit warnings mean a consumer doesn't need to know that "mixed classifier versions" is a red flag—the export tells them.

### 4. First-Run Experience: Useful, Clear, Non-Overstated

**Verdict: PASS**

The first-run output (`first_run.py:7–80`) is a human-readable markdown summary generated from compiled profile data only:

**Structure:**
- **Opening:** Explains what was done and what was not done (no raw artifact text).
- **Profile Overview:** Metadata-only summary (profile ID, pattern count, support counts, artifact storage mode).
- **Strongest Observed Patterns:** Top 5 patterns sorted by descending confidence, with support counts and confidence scores.
- **Limits and Cautions:** Explicit negatives (cannot diagnose, infer intent, prove identity traits), quarantine/exclusion explanation, metadata-only storage limitation, low-confidence warnings, compatibility warnings.
- **What Imprint Cannot Say:** Three explicit prohibitions (cannot say what subject is/feels/wants, cannot treat punctuation as psychological ground truth, cannot expose raw evidence).

**Data source:** Calls `canonical_profile_export(profile)`, which validates the profile. It then extracts only profile metadata, expression patterns, confidence, and support counts. It does not include or generate raw text, downstream instructions, generation prompts, or drafts.

Test evidence: `test_first_run_summary_uses_compiled_profile_data_only` verifies the output contains "What Imprint Learned," "Observed pattern," "raw artifact text," and "diagnose" while excluding raw text ("Start here") and person-level claims ("The subject is").

**Observed:** The 5-pattern limit balances usefulness (covers ~30% of typical profiles) with non-overwhelming output. Users can access full JSON export for complete list. Language is consistently bounded: "observed pattern" not "personality trait," "supported by" not "proves," "confidence summarizes support strength" not "certainty about the person."

### 5. Mosvera Boundary: Contract/Fragment Only

**Verdict: PASS**

The Mosvera overlay (`mosvera.py:12–50`) is a public-safe bridge contract, not a runtime:

**What the overlay contains:**
- Overlay version and source profile metadata (profile ID, compiler version, signal model versions)
- Evidence policy: raw_text_included=False, source_references="opaque_metadata_only", generation_controls_included=False
- Expression summaries: for each signal, family, name, claim text, confidence, support artifact count, source types
- Avoid patterns: same structure as expression summaries, separated for Mosvera to distinguish "what to do" from "what to avoid"
- Explicit boundary statement: "Imprint compiles expression; Mosvera owns aesthetic intent and runtime behavior"

**What the overlay does NOT contain:**
- Provider-specific prompts (no "OpenAI prompt:", "Claude system prompt:", etc.)
- Image generation instructions
- Model settings, decoding controls, or temperature hints
- Raw Imprint evidence or source snippets
- Aesthetic-intent compilation
- Runtime behavior or workflow instructions

**Safety enforcement:** `assert_public_safe_payload(overlay)` validates no generation-control keys appear. Anti-patterns are explicitly separated from expression summaries.

Test evidence: `test_mosvera_overlay_contains_expression_only_no_provider_prompts` verifies contract name, evidence policy structure, expression summaries presence, and absence of "prompt," "provider," and raw text in serialized output.

**Observed:** The boundary is clear in code and in documentation (`MOSVERA_INTEGRATION.md`). The review rule is explicit: "If a field tells Mosvera how to call or tune a model, it does not belong in the Sprint 07 overlay."

### 6. Determinism and Provider Neutrality: Verified

**Verdict: PASS**

All exports are deterministic and provider-neutral:

**Determinism:**
- JSON export uses `json.dumps(..., sort_keys=True)` and sorted collections.
- Markdown export sorts patterns by descending confidence, then family, then name.
- First-run export sorts patterns by descending confidence.
- Mosvera overlay uses canonical JSON, which is deterministic.

Test evidence: `test_canonical_json_export_is_deterministic` and `test_markdown_export_is_deterministic_and_conservative` run exports twice and verify byte-for-byte identical output.

**Provider neutrality:**
- No LLM imports or calls in any export module.
- No embeddings, vector operations, or semantic models.
- No remote API calls, webhooks, or external dependencies.
- BuildManifest fields `model_provider`, `model_name`, `model_version` are all None.
- All logic is rule-based: grouping, sorting, filtering, serialization.

Test evidence: Static scan of `src/imprint/exports/` found no provider imports, HTTP clients, or environment access. CLI smoke paths work through local compile pipeline only.

---

## Carry-Forward Constraints Enforced

All 10 Sprint 06 carry-forward constraints remain intact:

1. ✅ Claim-level validation not weakened. PROHIBITED signals fail export.
2. ✅ PROHIBITED signals remain errors.
3. ✅ BOUNDED_INTERPRETATION remains policy-gated.
4. ✅ Incompatible signal model versions are rejected.
5. ✅ Source IDs remain opaque in all exports.
6. ✅ No raw `artifact.reference.source_id` exposed; validated format required.
7. ✅ No raw text in public-safe exports.
8. ✅ Profiles are summaries, not raw-text archives.
9. ✅ Context profiles use explicit filters; no hidden inheritance.
10. ✅ Source filters validated; no implicit source-type magic.

---

## Testing Evidence

**Total test suite:** 71 tests, all passing.  
**New export tests:** 10 (as of Sprint 07).

### Export-Specific Tests (test_exports.py)

1. `test_canonical_json_export_is_deterministic` — Verifies JSON determinism.
2. `test_markdown_export_is_deterministic_and_conservative` — Verifies Markdown determinism and conservative language.
3. `test_public_safe_exports_contain_no_raw_text_or_paths` — Runs all 4 formats; no leaks.
4. `test_prohibited_claims_cannot_export_even_if_profile_is_mutated` — Prohibited claim gate enforced.
5. `test_bounded_interpretations_remain_policy_gated_for_exports` — Policy gate enforced.
6. `test_opaque_source_ids_remain_opaque_in_json_export` — Source ID opacity verified.
7. `test_incompatible_signal_versions_cannot_export_as_comparable` — Version validation enforced.
8. `test_first_run_summary_uses_compiled_profile_data_only` — Data source verified.
9. `test_mosvera_overlay_contains_expression_only_no_provider_prompts` — Boundary enforced.
10. `test_export_cli_smoke_for_all_formats` — CLI integration verified.

**Invocation:** `python3 -m pytest tests/ -q` (all 71 tests pass in 0.32s).

---

## Unresolved Observations (Not Blockers)

### First-Run Pattern Limit
The first-run output shows top 5 patterns. Largest fixture has ~17 signals; 5 covers ~30% of typical profiles. Users can access full JSON export for complete list. Not a blocker; current scope is synthetic/testing.

### Mixed Classifier Versions
Mixed classifier versions are allowed but warned. Downstream consumers must decide if "partially comparable" is acceptable. Warning is explicit in export; schema records versions for audit. Documented in Sprint 08 integration guide recommendations.

### Confidence Interpretation
First-run displays confidence (display score: 0.05–0.95). Language is qualified throughout ("summarizes support strength, not truth about a person"; "limited evidence warnings"). Ensure downstream UI/UX reinforces support-strength interpretation.

---

## Handoff to Sprint 08

Sprint 08 downstream integration can proceed with the canonical export contract as the source of truth. Recommendations:

1. **Keep downstream prompt assembly outside Imprint.** Treat canonical JSON as a contract, not a template.
2. **Treat canonical JSON as the source of truth for all projections.** Markdown, first-run, and Mosvera are derivations.
3. **Add consumer-specific export tests before publishing or Mosvera integration.**
4. **Preserve no-raw-text public-safe boundary** when adding YAML or file-output variants.
5. **Decide whether classifier-version warnings should become mandatory** in every downstream export.

No architectural blockers remain. Publishing workflows, brand enforcement, approval gates, and model-specific prompt assembly are downstream concerns, not Imprint scope.

---

## Delivery Evidence

- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md` — Comprehensive adversarial review (6 focus areas + documentation + testing)
- `src/imprint/exports/` — Implementation (5 modules, 500+ lines)
- `tests/test_exports.py` — Test suite (183 lines, 10 tests)
- `docs/EXPORT_FORMATS.md`, `docs/FIRST_RUN_OUTPUT.md`, `docs/MOSVERA_INTEGRATION.md`, `docs/EXPORT_BOUNDARIES.md` — Contract documentation
- All tests passing: `pytest -q` (71/71 ✓)

---

## See Also

- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md` — Full adversarial review findings and verdict
- `docs/narrative/2026-06-07-sprint-07-export-contracts.md` — Sprint 07 implementation narrative (export design and shipped behavior)
- `docs/CHANGES.md` — Chronological per-phase log (to be updated)

---

**Sign-off:** ✅ GO for Sprint 08 downstream integrations.
