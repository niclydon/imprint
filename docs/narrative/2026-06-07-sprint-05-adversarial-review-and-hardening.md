# Sprint 05: Adversarial Review and Post-Review Hardening

The adversarial review of Sprint 05 signal extraction implementation found the engine architecturally sound but identified four minor items that could be hardened without blocking profile compilation. Rather than deferring these to Sprint 06, we implemented all four as a post-review polish cycle, including discovery that the implementation had expanded significantly beyond the baseline rule set.

## The Review Gate

Sprint 05 had delivered a deterministic, artifact-scoped signal extractor with 8 baseline rules across 5 signal families (structure, lexical, rhetorical, formatting, tone). The adversarial review checked six dimensions:

1. **Claim boundaries** — does extraction stay artifact-level and avoid personality/diagnostic claims?
2. **Evidence discipline** — does every signal carry full support metadata?
3. **Classification boundary** — are excluded/quarantined/included semantics preserved?
4. **Privacy** — do source IDs remain opaque and no raw text leak?
5. **Determinism** — are there any LLMs, embeddings, or provider calls?
6. **Scalability** — does the baseline path remain linear?

All six passed. The engine preserved the classification boundary in code (excluded → no signals, quarantined → non-durable, included → durable observations), maintained evidence-first discipline with versioned confidence decomposition, enforced NO_RAW_TEXT policy, and had no provider dependencies. Scaling tests with 120 artifacts completed in 0.23s with zero cross-artifact logic.

**Verdict: GO for Sprint 06.** But four minor items were flagged for post-review treatment:

1. `signal_model_version` field missing from `ArtifactSignalEvidence` — extraction confidence model changes would not be trackable.
2. Source ID validation not schema-enforced — adapters could accidentally pass filesystem paths.
3. Confidence formula weights undocumented in code — future tuning discussions would lack rationale.
4. Profile compiler claim-level validation not specified as requirement — Sprint 06 design would need explicit guidance.

## Expanded Implementation Discovery

Before implementing the hardening items, we read the engine code to understand its current state. During this read, we discovered the implementation had been significantly extended beyond the baseline:

**Baseline (designed):** 8 rules across 5 families
- Structure (2): short_paragraphs, direct_opening
- Lexical (1): contractions
- Rhetorical (1): contrast_framing
- Formatting (2): bullet_usage, heading_usage
- Tone (2): question_marker, exclamation_marker

**Actual implementation:** 17 rules across 8 families
- All baseline rules (8)
- **Reasoning (3):** causal_explanation, tradeoff_framing, caveat_handling
- **Narrative (3):** ordered_sequence, before_after_transition, example_grounding
- **Anti-pattern (3):** question_burst, punctuation_emphasis, formatting_without_prose

The expansion was architecturally sound — all new rules remained deterministic, artifact-local, and public-safe. The anti-pattern rules were especially valuable: they included explicit guidance for downstream consumers such as "should not promote that into a stable uncertainty claim without recurrence" and "should not treat that as emotional ground truth." This protection mechanism prevents over-interpretation in profile compilation.

The implementation aligned with the SIGNAL_EXTRACTION_DESIGN.md and SIGNAL_EXTRACTION_RULES.md docs but had gone beyond what the SPRINT_05.md status indicated was done. Rather than flag this as scope creep, we updated the architecture review to document the expanded coverage and its benefits.

## Hardening Implementation

### 1. Signal Model Version Tracking

Added `signal_model_version: str` field to `ArtifactSignalEvidence` schema.

The engine was already hardcoding `SIGNAL_CONFIDENCE_MODEL_VERSION = "sprint05-rule-v1"`, but this constant was never exported to the signal output. This meant future changes to the confidence formula — weight adjustments, new components, clamping changes — would be invisible to historical analysis and would silently redefine the semantics of old signals.

**Fix:** The engine now populates `signal_model_version` from the constant when creating evidence metadata. Tests verify the field is present and correct (`test_signal_model_version_is_tracked`).

**Impact:** Signal output is now auditable across extraction rule changes. When confidence formulas change in future sprints, the version string changes, and any downstream consumer can detect the breakpoint.

### 2. Source ID Validation

Added `validate_source_id()` function to the signal engine with three checks:

1. Reject filesystem paths: `/home/...`, `C:\...`, etc.
2. Reject path traversal: `../../../etc/passwd`
3. Reject file extensions: `.json`, `.yaml`, `.csv`, `.db`

The validation runs during signal candidate creation — before evidence is constructed — so a bad source ID (accidentally passed by an adapter) is caught early and raises `ValueError` with clear messaging.

**Test coverage:** `test_source_id_validation_rejects_paths` verifies that valid source IDs (`source-abc123`) pass while all three path-like patterns are rejected.

**Impact:** Adapters can no longer accidentally leak filesystem paths into the opaque-source-ID contract. The validation is deterministic and synchronous, adding negligible latency.

### 3. Confidence Formula Documentation

Added a 30-line docstring to `_signal_confidence()` method explaining the weight formula:

```
0.25 * attribution          # How well assigned to subject (highest weight)
+ 0.2 * authorship_origin  # Confidence subject authored artifact
+ 0.25 * extraction        # Rule reliability, bounded [0.2, 0.95]
+ 0.2 * evidence_strength  # Feature strength for this specific signal
+ 0.1 * policy_fit         # 1.0 for durable, 0.6 for quarantined
```

The docstring explains why these weights were chosen:
- Attribution and extraction carry equal weight because both represent fundamental quality gates.
- Authorship and evidence have secondary weight — necessary for context but not dominant.
- Policy fit has the lowest weight — it's a boundary condition, not a quality metric.
- The final score is clamped to [0.05, 0.95] to prevent overconfidence, then multiplied by classification confidence to preserve the dependency chain.

**Impact:** Future developers can understand the formula rationale without reverse-engineering it from code. Confidence tuning discussions now have an explicit starting point.

### 4. Sprint 06 Claim-Level Validation Requirement

Documented as a critical requirement for Sprint 06 profile compiler work:

The signal extraction engine emits three claim levels:
- `OBSERVATION`: directly supported pattern (preferred)
- `QUARANTINED`: non-durable candidate (artifact not cleanly eligible)
- `PROHIBITED`: diagnosis, personality typing, intent attribution (not emitted in baseline)

The baseline extractor prevents PROHIBITED claims through human review of hardcoded rule sets and schema validation. But the profile compiler — Sprint 06's scope — must explicitly validate claim levels:
1. Reject or quarantine any signal with `ClaimLevel.PROHIBITED`.
2. Validate `BOUNDED_INTERPRETATION` claims (deferred for future sprint) with evidence checks.
3. Only allow `OBSERVATION` claims in durable profile support.

This requirement was added to the architecture review and will be integrated into the Sprint 06 design docs.

## Test Coverage

Added two new tests beyond the original 10:

- `test_signal_model_version_is_tracked()`: Verifies all signals carry the correct extraction model version.
- `test_source_id_validation_rejects_paths()`: Verifies the validation function rejects paths, traversal, and extensions while accepting valid opaque IDs.

All 44 project tests pass. No regressions.

## What's Unblocked for Sprint 06

1. **Evidence export chain is now fully versioned.** Classification model version and signal model version are both tracked. Drift detection tools can identify exactly when either side of the chain changed.

2. **Privacy boundary is actively enforced.** Adapters can no longer accidentally pass filesystem paths into opaque source IDs.

3. **Confidence formula is documented and auditable.** Future tuning or formula changes can cite the original rationale.

4. **Profile compiler has explicit claim-level requirements.** Sprint 06 design can bake in validation as a first-class concern.

5. **Implementation expansion is documented.** The extended rule set (17 rules vs. 8 baseline) is now recorded in the architecture review with reasoning for each new family.

## What's Still Deferred

- Humor extraction (context-sensitive, would benefit from semantic extraction)
- Long-form reasoning chains beyond the current markers (would require semantic analysis)
- Semantic tone inference (would require LLM)
- Cross-artifact recurrence signals (profile-compilation scope)
- Confidence model tuning against labeled ground truth (production-scale work)

These remain in the deferred list intentionally and are documented in the design specs.

---

**See `CHANGES.md` Phase 2 for the chronological diff summary.**
