# Sprint 05 Architecture Review: Signal Extraction Implementation

**Reviewer:** Claude (Adversarial Principal Architect)  
**Status:** Post-implementation gate review  
**Context:** Evaluation of the implemented Sprint 05 signal extraction engine against claim boundaries, evidence discipline, classification boundary preservation, privacy enforcement, determinism, and profile-compilation readiness.

---

## Executive Summary

Sprint 05 delivers a deterministic, artifact-scoped signal extractor that respects all Sprint 04 classification boundaries and maintains the privacy-first evidence model. The implementation is conservative, well-tested, and architecturally sound.

**Key achievements:**

1. **Classification boundary is preserved in code.** Excluded artifacts produce no signals. Quarantined artifacts produce non-durable candidates only. Included artifacts produce durable observations.
2. **Evidence discipline is first-class.** Every signal carries versioned classification metadata, rule identifiers, observed features (generic, no raw text), and explicit evidence policy.
3. **Confidence decomposition is explicit.** Signal confidence is a weighted function of classification confidence, rule reliability, evidence strength, and policy fit—all recorded and auditable.
4. **No person-level or diagnostic claims.** All 8 baseline rules emit observable pattern descriptions only. No personality typing, diagnostic inference, or intent attribution.
5. **Determinism and local-first execution are enforced.** No LLMs, embeddings, remote APIs, or cross-artifact quadratic logic in the baseline path.
6. **Public-safe evidence export is built-in.** Signal output maintains NO_RAW_TEXT policy and opaque source IDs; no private text or paths leak.

**Verdict: GO for Sprint 06**

Sprint 05 is architecturally sound and ready for profile compilation. The remaining concerns are operational hardening items (rule coverage breadth, confidence model tuning, audit-path tooling) and do not block the next sprint.

---

## Detailed Findings by Focus Area

### 1. Claim Boundaries: Observation vs. Interpretation vs. Diagnosis

**Status: ✅ Excellent**

**What Sprint 05 Implements:**

The rule set emits only observations and quarantined candidates. No prohibited claims, no interpretations, no diagnostic inference.

**Examples of implemented claims (all observations):**

- `structure_short_paragraphs`: "All observed paragraphs are short."
- `lexical_contractions`: "The artifact includes contractions."
- `rhetorical_contrast_framing`: "The artifact uses a not-X-but-Y contrast structure."
- `formatting_bullet_usage`: "The artifact uses bullet formatting."
- `tone_question_marker`: "The artifact uses explicit question markers."
- `reasoning_causal_explanation`: "The artifact uses explicit causal explanation markers."
- `narrative_ordered_sequence`: "The artifact uses explicit ordered sequence markers."
- `anti_pattern_question_burst`: "The artifact stacks multiple questions; downstream consumers should not promote that into a stable uncertainty claim without recurrence."

These describe observable artifact patterns, not person-level traits.

**Expanded implementation:** The initial baseline of 8 rules has been extended to 17 rules across all 8 signal families:
- Structure (2), Lexical (1), Rhetorical (1), Formatting (2), Tone (2), Reasoning (3), Narrative (3), Anti-Pattern (3)

This expansion is architecturally sound; all new rules remain deterministic, artifact-local, and public-safe. The anti-pattern rules are especially valuable because they include explicit guidance for downstream consumers ("should not promote that into a stable uncertainty claim without recurrence").

**What's blocked:**

Tests verify that blocked terms do not appear in signal names or observed features:
- `analytical`, `introvert`, `anxious`, `depressed`, `bipolar`, `adhd`

This test (`test_signal_candidates_do_not_contain_personality_or_diagnostic_claims`) is a good boundary guard but is not exhaustive; it checks hardcoded strings, not semantic policy. For production, a validation layer should formalize the `ClaimLevel` enum enforcement (OBSERVATION, BOUNDED_INTERPRETATION, PROHIBITED) and quarantine or reject signals that attempt prohibited claims.

**Deferred beyond current implementation:**

- `humor` extraction (context-sensitive, deferred)
- long-form reasoning chains beyond causal/tradeoff/caveat (semantic, deferred)
- semantic tone inference (would require LLM, deferred)
- cross-artifact recurrence signals (profile-compilation scope, deferred)

The deferral is appropriate and documented in the design specs.

**Risk:** ⚠️ **Minor**

The claim-level boundary is enforced by the signal ID and evidence metadata but is not yet machine-validated at the profile-compilation stage. Sprint 06 should add explicit claim-level validation before signals enter the profile compiler.

**Verdict: ✅ Claim boundary holds in the baseline extractor.**

---

### 2. Evidence Discipline: Support Trail, Confidence Components, and Versioning

**Status: ✅ Excellent**

**What Sprint 05 Delivers:**

Each signal carries comprehensive evidence metadata:

```python
ArtifactSignalEvidence(
    signal_id=signal_id,
    artifact_id=artifact.artifact_id,
    source_id=artifact.reference.source_id,
    source_type=artifact.reference.source_type,
    classification_id=classification_result.classification.classification_id,
    classification_label=classification_result.classification.label,
    classification_model_version=classification_result.confidence.model_version,
    rule_id=rule_id,
    observed_feature=observed_feature,
    evidence_policy=SignalEvidencePolicy.NO_RAW_TEXT,
    limitations=["non-included artifacts cannot produce durable support"] if not durable else [],
)
```

**Answering the Evidence Questions (from EVIDENCE_AND_CONFIDENCE.md):**

- ✅ **What artifacts supported this?** `artifact_id` + `source_id` (opaque)
- ✅ **What source types contributed?** `source_type` + `source_id`
- ✅ **What classification made the artifacts usable?** `classification_label` + `classification_id`
- ✅ **What extraction method produced the signal?** `rule_id` + hardcoded confidence model version
- ✅ **What evidence was excluded or quarantined?** `limitations` field explicitly notes non-included artifacts
- ✅ **Is raw text available locally for audit?** Implicit: `source_id` is opaque; raw text is not exported but original artifacts are retained locally

**Confidence Decomposition (Excellent):**

Signal confidence is computed from six independent components:

```python
Confidence(
    attribution=classification_result.confidence.attribution,
    authorship_origin=classification_result.confidence.authorship_origin,
    extraction=clamp(rule_reliability, low=0.2, high=0.95),
    evidence_strength=evidence_strength,
    source_diversity=1.0,  # single-artifact baseline
    policy_fit=1.0 if durable else 0.6,
)
```

The display score is a weighted average:
```
0.25 * attribution
+ 0.2 * authorship_origin
+ 0.25 * extraction
+ 0.2 * evidence_strength
+ 0.1 * policy_fit
* classification_result.confidence.display
```

This formula is defensible:
- Attribution and extraction carry equal weight (most important).
- Authorship-origin and evidence strength have secondary weight (necessary, but not dominant).
- Policy fit has the lowest weight (it's a boundary condition, not a quality score).
- All components are clamped to [0.05, 0.95] to prevent extreme overconfidence or underconfidence.
- The final score is multiplied by the classification confidence, properly chaining the dependency.

**Versioning:**

The signal extraction confidence model is versioned as `SIGNAL_CONFIDENCE_MODEL_VERSION = "sprint05-rule-v1"`. However, this version string is **hardcoded in the engine**, not propagated to the signal output.

**Risk:** ⚠️ **Minor**

The signal confidence output does not include the extraction model version, only the classification model version. This means future changes to the extraction confidence formula will not be visible in the signal history. Recommendation: add a `signal_model_version` field to `ArtifactSignalEvidence` so old vs. new extraction rules are comparable.

**Verdict: ✅ Evidence discipline is excellent. Confidence decomposition is transparent and auditable.**

---

### 3. Classification Boundary: Excluded/Quarantined/Included Handling

**Status: ✅ Excellent**

**What Sprint 05 Enforces:**

The boundary is enforced at the entry point:

```python
def extract_from_result(
    self,
    artifact: Artifact,
    classification_result: ArtifactClassificationResult,
) -> list[ArtifactSignalCandidate]:
    if classification_result.classification.label == ArtifactClassificationLabel.EXCLUDED:
        return []
    # ... proceed to signal extraction
```

And again at the signal level:

```python
durable = classification_result.classification.label == ArtifactClassificationLabel.INCLUDED
claim_level = ClaimLevel.OBSERVATION if durable else ClaimLevel.QUARANTINED
```

**Tests Confirm the Boundary:**

- `test_excluded_artifacts_produce_no_signals()` ✅ Excluded → empty list
- `test_quarantined_artifacts_do_not_support_durable_signals()` ✅ Quarantined → non-durable, claim_level=QUARANTINED
- `test_included_artifacts_produce_durable_signals()` ✅ Included → durable, claim_level=OBSERVATION

**Quarantine Semantics:**

Quarantined artifacts produce signals, but they are marked:
- `durable=False`
- `claim_level=ClaimLevel.QUARANTINED`
- `limitations` includes: "non-included artifacts cannot produce durable support"

This is exactly what the design requires: quarantined signals are visible for review but do not contribute to durable profile compilation.

**Batch Processing:**

The `extract_batch` method enforces the boundary for each artifact independently. There is no cross-artifact leakage that could promote quarantined signals by aggregation.

**Verdict: ✅ Classification boundary is preserved and tested.**

---

### 4. Privacy: Source ID Opacity and Public-Safe Evidence

**Status: ✅ Good, with Minor Observations**

**What Sprint 05 Implements:**

1. **Source ID remains opaque:**
   - Source ID is passed through from the artifact without reconstruction.
   - It is never used to reconstruct filesystem paths or private locators.
   - Test `test_each_signal_includes_public_safe_evidence_metadata()` verifies: `assert not ("signal-transcript.json" in signal.source_id)`

2. **No raw text in signal output:**
   - Evidence policy is hardcoded as `SignalEvidencePolicy.NO_RAW_TEXT`.
   - Observed features are generic descriptions, not excerpts: "The artifact uses bullet formatting" not "Found: •\nFound: •\nFound: •".

3. **Generic observed features:**
   - All observed features are summary descriptions, not examples or private text.
   - Examples: "All observed paragraphs are short", "The artifact includes contractions", "The artifact uses heading formatting."

**Verification:**

The test `test_each_signal_includes_public_safe_evidence_metadata()` checks:
```python
assert signal.evidence.no_raw_text is True
assert signal.source_id.startswith("source-")
assert "signal-transcript.json" not in signal.source_id
```

This is good but relies on fixture data naming conventions. For production, this should be:
- A property-based assertion that source_id never contains path separators or file extensions.
- An audit export that maps opaque source IDs to local paths only in a private-local output mode.

**Source ID validation is now enforced:** ✅

The `validate_source_id()` function in the signal engine validates that source IDs do not contain:
- Filesystem path separators (`/`, `\`)
- Windows drive letters (`C:\`, etc.)
- Path traversal patterns (`..`)
- File extensions (`.txt`, `.json`, `.yaml`, `.csv`, `.db`)

This validation is called during signal candidate creation, catching bad source IDs early. Tests verify rejection of all path patterns.

**Verdict: ✅ Privacy boundary is strong and actively enforced.**

---

### 5. Determinism and Provider Neutrality

**Status: ✅ Excellent**

**What Sprint 05 Delivers:**

- **No LLMs:** All rule implementations use deterministic local logic (string pattern matching, count thresholds).
- **No embeddings:** No semantic similarity, nearest-neighbor, or vector comparisons.
- **No remote APIs:** All processing is local-only.
- **No provider assumptions:** No hardcoded model names, API keys, or provider-specific heuristics.

**Determinism Test:**

```python
def test_signal_extraction_is_deterministic_and_local_only() -> None:
    first = [signal.model_dump(mode="json") for signal in extractor.extract_batch(artifacts, classifications)]
    second = [signal.model_dump(mode="json") for signal in extractor.extract_batch(artifacts, classifications)]
    assert first == second
```

This test runs the same extraction twice and verifies the outputs are byte-for-byte identical. ✅ Passes.

**Rule Details:**

- `structure_short_paragraphs`: compares `short_paragraph_count == paragraph_count` (direct equality)
- `lexical_contractions`: checks `contraction_count > 0` (simple threshold)
- `rhetorical_contrast_framing`: checks `uses_contrast_framing` hint (boolean flag from adapter)
- `formatting_bullet_usage`: checks `uses_bullets` hint (boolean flag)
- `tone_question_marker`: checks `question_count > 0` (simple threshold)

All rules are based on metadata hints or counts, not on semantic inference. The hints themselves (e.g., `contraction_count`) come from the adapter's deterministic parsing of artifact content, not from ML models.

**Verdict: ✅ Determinism and provider neutrality are guaranteed.**

---

### 6. Scalability and Linear-Time Guarantee

**Status: ✅ Good**

**What Sprint 05 Implements:**

```python
def extract_batch(self, artifacts: list[Artifact], classifications: list[ArtifactClassificationResult]) -> list[ArtifactSignalCandidate]:
    classification_by_artifact = {result.artifact_id: result for result in classifications}
    candidates: list[ArtifactSignalCandidate] = []
    for artifact in artifacts:
        result = classification_by_artifact[artifact.artifact_id]
        candidates.extend(self.extract_from_result(artifact, result))
    return candidates
```

**Algorithmic Complexity:**

- Dictionary lookup: O(1) per artifact
- Per-artifact rule evaluation: O(1) (constant number of rules, each runs in O(1))
- Total: O(n) where n = number of artifacts

**Scaling Test:**

```python
def test_signal_extraction_handles_simple_linear_batch() -> None:
    artifacts = []
    for index in range(120):
        artifact = LocalTranscriptJsonAdapter().ingest(...)[0]
        artifact.artifact_id = f"{artifact.artifact_id}-{index}"
        artifacts.append(artifact)
    classifications = RuleBasedArtifactClassifier().classify_artifacts(artifacts)
    signals = RuleBasedSignalExtractor().extract_batch(artifacts, classifications)
    assert len(classifications) == 120
    assert len(signals) >= 120
```

✅ Passes. The test confirms that 120 artifacts are processed without error and produce at least 120 signals (some artifacts produce multiple signals).

**No Cross-Artifact Logic:**

- No aggregation across artifacts.
- No pairwise comparisons.
- No recurrence counting across the corpus.
- No thresholds based on corpus-wide statistics.

All of these are explicitly deferred to future sprints.

**Verdict: ✅ Baseline extractor maintains linear-time guarantee. Scaling targets are documented (1M artifacts in <1 hour).**

---

## Issues and Blockers

### Resolved from Pre-Implementation Phase

1. ✅ **Signal extraction dependency on classification:** Properly bounded. Excluded/quarantined/included logic is explicit and tested.
2. ✅ **Evidence metadata structure:** Defined in schemas and implemented. Every signal carries the required fields.
3. ✅ **Confidence scoring model:** Defined, versioned, and implemented. Components are auditable.
4. ✅ **Claim-level boundary:** Observation/quarantined distinction is enforced in code.
5. ✅ **Privacy enforcement:** Source ID opacity and no-raw-text policy are implemented.

### Resolved in Post-Review Hardening

1. ✅ **Signal-model versioning now exported**
   - Added `signal_model_version` field to `ArtifactSignalEvidence`.
   - Engine populates it from `SIGNAL_CONFIDENCE_MODEL_VERSION = "sprint05-rule-v1"`.
   - Tests verify it is present and correct.

2. ✅ **Source ID validation now enforced**
   - Added `validate_source_id()` function in signal engine.
   - Validates against filesystem paths, path traversal (`..`), and file extensions.
   - Called during signal candidate creation; rejects bad source IDs early.
   - Tests verify rejection of `/paths`, `C:\paths`, `../traversal`, and `.json` extensions.

3. ✅ **Confidence formula weights now documented**
   - Added comprehensive docstring to `_signal_confidence()` method.
   - Explains weight rationale: 25% attribution (most important), 20% authorship (necessary), 25% extraction (core rule quality), 20% evidence (feature strength), 10% policy (boundary condition).
   - Clamping and dependency chain documented.

### Remaining Minor Items (Deferred to Sprint 06)

1. **Claim-level validation not yet automated**
   - Prohibited claims are blocked by human review of hardcoded rule set, not by schema validation.
   - Recommendation: Add a validation layer in profile compilation that rejects signals with `ClaimLevel.PROHIBITED` or triggers manual review for `BOUNDED_INTERPRETATION`.
   - Severity: Minor. Good for the profile compiler to enforce, not required in signal extraction.

### No Blockers

✅ No architectural issues that prevent profile compilation.

---

## Remaining Risks (Not Sprint 06 Blockers)

### 1. Rule Coverage Has Expanded Beyond Initial Baseline

**Status: ✅ Excellent**

Sprint 05 now implements 17 rules across all 8 signal families:
- Core families (5): Structure (2), Lexical (1), Rhetorical (1), Formatting (2), Tone (2)
- Extended families (3): Reasoning (3), Narrative (3), Anti-Pattern (3)

This expansion is architecturally sound and adds significant value:
- Reasoning rules capture causal explanation, tradeoff framing, and caveat handling.
- Narrative rules identify ordered sequences, before-after transitions, and example grounding.
- Anti-pattern rules provide explicit guidance to downstream consumers ("should not promote without recurrence").

Deferred for future work:
- `humor` (context-sensitive, would benefit from semantic extraction)
- Long-form reasoning chains beyond the current markers (would require semantic analysis)
- Semantic tone inference (would require LLM)
- Cross-artifact recurrence signals (profile-compilation scope)

**For Sprint 06+:** Continue expanding rule coverage in a planned, documented way. Each new rule should have tests and evidence metadata, and should be tracked in the versioned confidence model.

### 2. Confidence Model Tuning Is Empirical

**Status: ⚠️ Acceptable**

The hardcoded `rule_reliability` and `evidence_strength` values (0.72–0.9) are reasonable defaults but have not been benchmarked against ground truth.

Example:
```python
rule_reliability=0.82,  # structure_short_paragraphs
evidence_strength=0.72,
```

These feel defensible (short paragraphs are a reliable signal, but not perfect), but they should be:
1. Documented in a config file, not hardcoded.
2. Tuned against real data if this scales beyond research/MVP.

**For production:** Add a configuration layer for rule parameters and periodically re-tune against labeled data.

### 3. Profile Compilation Has Not Been Designed Yet

**Status: ⚠️ Blocked by Sprint 06 design**

Sprint 05 produces individual artifact-level signals. Sprint 06 will need to:
- Aggregate signals across artifacts into person-level profile dimensions.
- Handle drift detection and profile versioning.
- Validate claim levels at the profile level.
- Export public-safe profiles.

This is out of scope for Sprint 05 review. Recommend that Sprint 06 design includes explicit handling of:
- Signal aggregation semantics (how many durable signals of type X = profile dimension strength Y).
- Confidence recomputation at the profile level.
- Temporal drift detection (signals vs. old profile values).

---

## Go / No-Go Decision

### ✅ GO for Sprint 06

**Verdict:** Sprint 05 signal extraction is architecturally sound, well-tested, and ready for profile compilation.

**Constraints and assumptions for Sprint 06:**

1. **Classification boundary remains sacred.** Do not aggregate quarantined signals into durable profile support without explicit review promotion.
2. **Confidence remains decomposed.** Any future changes to confidence formulas must increment `signal_model_version`.
3. **Privacy enforcement stays first-class.** Source ID opacity and no-raw-text policy must be preserved through profile compilation and export.
4. **No cross-artifact leakage in profiling.** If Sprint 06 aggregates signals, ensure the aggregation does not reveal artifact-local details that should remain private.
5. **Claim validation is mandatory at the profile level.** Any signals marked `QUARANTINED` or `PROHIBITED` should fail profile validation or trigger manual review.
6. **Rule versioning is documented.** Any new rules added beyond Sprint 05 must be tracked in the rule inventory and model version.

**Before Sprint 06 ships:**

- [x] Add `signal_model_version` field to `ArtifactSignalEvidence` (resolved post-review).
- [x] Document confidence formula weights in code or design doc (resolved post-review).
- [x] Add source ID validation to the signal engine (resolved post-review).
- [ ] **Implement claim-level validation in profile compiler (critical):** Reject or quarantine signals with `ClaimLevel.PROHIBITED`, validate `BOUNDED_INTERPRETATION` with evidence checks.
- [ ] Design the profile compilation boundary and confidence recomputation logic (critical).

---

## Appendix A: Review Checklist

### Claim Boundaries
- [x] No personality typing in rules.
- [x] No diagnostic claims.
- [x] No intent attribution.
- [x] Observation vs. quarantined distinction is clear.
- [x] PROHIBITED claim level is defined but not used in baseline (appropriate deferral).

### Evidence Discipline
- [x] Every signal has artifact ID, source ID, classification ID, rule ID.
- [x] Classification model version is recorded.
- [x] Signal model version is exported and tracked.
- [x] Observed features are generic, not private excerpts.
- [x] Evidence policy is explicit (NO_RAW_TEXT).
- [x] Limitations are documented.

### Classification Boundary
- [x] Excluded artifacts produce no signals.
- [x] Quarantined artifacts produce non-durable signals.
- [x] Included artifacts produce durable observations.
- [x] Tests verify all three paths.
- [x] No cross-artifact promotion of quarantined signals.

### Privacy
- [x] Source IDs are opaque (not paths).
- [x] No raw text in public-safe output.
- [x] Observed features do not leak private content.
- [ ] Source ID format is not schema-validated (minor gap).

### Determinism and Provider Neutrality
- [x] No LLMs in the baseline extractor.
- [x] No embeddings.
- [x] No remote APIs.
- [x] Determinism is tested.
- [x] Local-only execution is guaranteed.

### Scalability
- [x] Baseline extractor is O(n).
- [x] No cross-artifact quadratic logic.
- [x] Scaling test with 120 artifacts passes.
- [x] Targets are documented (1M artifacts <1 hour).

### Documentation and Tests
- [x] Tests cover happy path, excluded, quarantined, determinism, scaling, evidence metadata, personality claims.
- [x] Design docs (SIGNAL_EXTRACTION_DESIGN.md, SIGNAL_EXTRACTION_RULES.md, SIGNAL_TAXONOMY.md) are synchronized with implementation.
- [x] CLI is wired correctly.

---

## Closing

Sprint 05 successfully delivers a deterministic, boundary-respecting signal extractor that serves as a solid foundation for profile compilation. The remaining work is operational hardening and cross-artifact aggregation logic, neither of which blocks the next sprint.

The implementation shows discipline in staying artifact-scoped, respecting the classification boundary, and maintaining evidence-first practices. This is a healthy place to begin Sprint 06.

---

**Sign-off:** ✅ GO for Sprint 06 profile compilation.
