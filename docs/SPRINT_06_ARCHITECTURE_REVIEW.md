# Sprint 06 Architecture Review: Profile Compiler Implementation

**Reviewer:** Claude (Adversarial Principal Architect)  
**Status:** Post-implementation gate review  
**Context:** Evaluation of the implemented Sprint 06 profile compiler against expression-pattern boundaries, signal eligibility, evidence preservation, version compatibility, privacy enforcement, determinism, and Sprint 07 export readiness.

---

## Executive Summary

Sprint 06 delivers a deterministic, signal-driven profile compiler that aggregates artifact-level observations into expression profiles while maintaining all upstream boundaries from Sprint 04 (classification) and Sprint 05 (signal extraction). The compiler implements strict signal eligibility gates (durable observation only), preserves version metadata across the evidence chain, rejects prohibited claims, and enforces privacy by design.

**Key achievement:** The profile compiler successfully acts as a validation barrier, not just an aggregator. It blocks incompatible signal model versions, mismatched classifications, prohibited claims, and path-like source IDs — failing fast and clearly rather than silently corrupting downstream data.

**Verdict: GO for Sprint 07**

Sprint 07 exports and first-run experience can proceed. The remaining items are productization (report generation, publishing prompts, context profile enrichment) and are not architectural blockers.

---

## Detailed Findings by Focus Area

### 1. Claim Boundaries: Expression Patterns, Not Personality or Diagnosis

**Status: ✅ Excellent**

**Design enforces expression-pattern-only boundaries:**

The `_claim_text()` method produces claims with a strict template:

```python
"Across included artifacts, {observed_feature} appears in {included_count} {count_label}."
```

All compiled claims follow this structure. Examples from test fixtures:
- "Across included artifacts, all observed paragraphs are short appears in 2 artifacts."
- "Across included artifacts, the artifact uses heading formatting appears in 1 artifact."

This template makes person-level or diagnostic claims structurally impossible. There is no field for "the subject is X" or "indicates Y condition." The claim is always about the artifact set, never the person.

**Validation gates:**

Before compilation, the compiler checks `claim_level`:
- `PROHIBITED` → rejected outright (test: `test_prohibited_signals_are_rejected_even_if_constructed_unsafely`)
- `QUARANTINED` → excluded from durable support
- `BOUNDED_INTERPRETATION` → excluded unless explicit policy flag
- `OBSERVATION` → only this level supports durable claims

**No diagnostic inference:** The confidence formula operates on evidence components (attribution, authorship_origin, extraction, evidence_strength), not on inferred state. The formula output is explicitly labeled "summarizes support strength, not truth about a person" in both code comment and support metadata.

**Verdict: ✅ Claim boundaries are enforced by design. Expression-pattern-only scope is maintained.**

---

### 2. Signal Eligibility: Quarantined, Non-Durable, and Prohibited Signals Excluded

**Status: ✅ Excellent**

**Eligibility logic is explicit and multi-layered:**

The `_eligible_candidates()` method applies a filter cascade:

```python
1. Source ID validation (rejects paths)
2. Artifact and classification lookups (fails if missing)
3. Classification ID matching (fails if mismatched)
4. PROHIBITED level rejection (fails fast)
5. Durable check (skips non-durable)
6. Included classification check (skips quarantined/excluded)
7. BOUNDED_INTERPRETATION policy gate (skips unless flag set)
8. OBSERVATION-only filter (final gate)
```

**Test coverage:**

- ✅ `test_only_durable_observation_signals_compile` — durable observations enter profile support
- ✅ `test_quarantined_signals_do_not_support_profile_claims` — quarantined candidates → empty profile
- ✅ `test_excluded_artifacts_produce_no_profile_support` — excluded → no signals, no claims
- ✅ `test_non_durable_candidates_do_not_support_profile_claims` — non-durable → empty profile
- ✅ `test_prohibited_signals_are_rejected_even_if_constructed_unsafely` — PROHIBITED → CompilerError
- ✅ `test_bounded_interpretations_are_excluded_by_default` — BOUNDED_INTERPRETATION excluded by default
- ✅ `test_bounded_interpretations_compile_only_with_review_gated_policy` — with flag, BOUNDED_INTERPRETATION compiles with REVIEW_BASED validation

**Incompatible signal model versions are rejected:**

The `_reject_incompatible_signal_model_versions()` method checks that all eligible candidates come from the same signal model version. If multiple versions are present, compilation fails with `CompilerError: cannot merge incompatible signal model versions: ...` (test: `test_incompatible_signal_model_versions_are_rejected`).

This is a critical safety boundary: future extraction rule changes won't silently merge old and new signals into misleading profiles.

**Verdict: ✅ Signal eligibility gates are strict and tested. No quarantined, non-durable, or incompatible signals leak into durable support.**

---

### 3. Evidence Discipline: Full Support Chain Preservation

**Status: ✅ Excellent**

**Every compiled signal preserves the evidence chain:**

```python
SignalSupport(
    signal_ids=[...],                      # Contributing artifact-level signals
    classification_model_versions=[...],   # Which classifier produced artifact labels
    signal_model_versions=[...],           # Which extractor produced signals
    rule_ids=[...],                        # Which extraction rules fired
    evidence_refs=[...],                   # References to contributing artifacts
    artifact_count=N,
    included_count=N,
    excluded_count=0,
    quarantined_count=0,
    source_types=[...],
    source_diversity=float,
    audit_limitations=[...],               # Public-safe disclosure
)
```

**Evidence references remain opaque:**

Each `EvidenceReference` includes:
- `artifact_ref.artifact_id` (artifact identifier)
- `artifact_ref.source_id` (opaque, validated to not contain paths)
- `classification_id` (which classification was used)
- `authorship_origin` (the authorship label)

Tests verify opaque source IDs:
- ✅ `test_profile_support_preserves_public_safe_versioned_metadata` — source IDs start with `source-`, no paths
- ✅ `test_path_like_source_ids_are_rejected` — `/private/source.txt` rejected

**Version metadata is preserved end-to-end:**

Test `test_mixed_classifier_versions_are_recorded_in_support_and_manifest` demonstrates that if artifacts were classified with different versions (e.g., `sprint04-rule-v1` and `sprint04-rule-v2`), the profile records both in:
1. Signal support: `support.classification_model_versions`
2. Build manifest: `profile.build_manifest.classifier_version`

Downstream consumers can detect version mismatches and treat the profile as compatibility-sensitive.

**Build manifest records full lineage:**

```python
BuildManifest(
    schema_version="0.1",
    compiler_version="sprint06-rule-v1",
    classifier_version="sprint04-rule-v1,sprint04-rule-v2",  # all versions seen
    extractor_family=ExtractorFamily.RULE_BASELINE,
    extractor_code_version="sprint05-rule-v1,sprint05-rule-v2",  # signal versions
    model_provider=None,                   # no LLM dependency
    model_name=None,
    model_version=None,
    source_policy_version="sprint06-source-policy-v1",
    authorship_policy_version="sprint06-authorship-policy-v1",
    config_hash="sha256:...",              # deterministic configuration fingerprint
)
```

Test `test_compiler_uses_no_provider_or_llm_manifest_dependencies` confirms `model_provider`, `model_name`, and `model_version` are all `None`.

**Verdict: ✅ Evidence discipline is excellent. Full support chain is preserved with opaque source IDs and version metadata recorded throughout.**

---

### 4. Version Compatibility: Incompatible Changes Detected and Rejected

**Status: ✅ Excellent**

**The compiler enforces two key compatibility boundaries:**

**Signal model version:**
- All eligible signals must come from the same `signal_model_version`.
- If different versions are present, compilation fails outright.
- This prevents Future extraction rule changes (e.g., from v1 to v2) from silently merging incompatible signal semantics.

**Classifier version (recorded but not rejected):**
- Mixed classifier versions are recorded in the build manifest and support metadata.
- The compiler does not reject mixed versions; instead, it flags them for downstream review.
- This is correct: a classifier version change may represent a bug fix (compatible) or a semantic change (breaking). Recording both versions lets downstream tools make the decision.

**Configuration hash for reproducibility:**

The `_config_hash()` method creates a deterministic hash over:
- Compiler version
- All artifact IDs
- All classification IDs
- All signal IDs
- All signal model versions

This fingerprint is recorded in the build manifest. Two profiles built from the same artifacts and signals will have the same config hash. Profiles with different hashes are not directly comparable (test: `test_compilation_is_deterministic` verifies byte-for-byte reproducibility).

**Versioning policy document is complete:**

`docs/VERSIONING_POLICY.md` defines:
- Versioned surfaces (schema, compiler, confidence formula, classifier, extractor, model fields)
- Drift categories (expression_drift, compiler_drift, corpus_drift, schema_drift)
- Comparability rules with machine-readable reasons

**Verdict: ✅ Version compatibility is enforced and documented. Incompatible signal model versions are rejected; classifier versions are recorded for downstream review.**

---

### 5. Privacy: No Raw Text, Opaque Source IDs, No Paths

**Status: ✅ Excellent**

**Raw text is never included in compiled profiles:**

Test `test_public_safe_compiled_profile_excludes_raw_text_and_paths` verifies the compiled profile JSON contains:
- ✅ No artifact text excerpts (e.g., "Start here")
- ✅ No filenames (e.g., "signal-transcript.json")
- ✅ No filesystem paths (e.g., "/tests/fixtures/")

The compiled profile includes only:
- Pattern descriptions (generic, e.g., "the artifact uses heading formatting")
- Metadata (artifact IDs, source types, version info)
- Support counts and confidence scores
- Opaque evidence references

**Source IDs are opaque and validated:**

Every source ID is validated on compilation (test: `test_path_like_source_ids_are_rejected`). The validation rejects:
- Absolute paths (`/home/...`)
- Windows paths (`C:\...`)
- Path traversal (`../../../`)
- File extensions (`.json`, `.yaml`, `.csv`, `.db`)

If an adapter accidentally passes a path, compilation fails loudly.

**Artifact metadata is safe:**

`EvidenceReference` includes `artifact_ref`, which contains:
- `artifact_id` (opaque)
- `source_id` (opaque, validated)
- `source_type` (e.g., "local_transcript_json", safe string)
- `artifact_type` (e.g., "transcript_segment", enum)

No filesystem paths or raw content are preserved.

**Audit limitations are disclosed:**

Every profile's `SignalSupport` includes:
```python
audit_limitations=[
    AuditLimitation.RAW_CONTENT_UNAVAILABLE,
    AuditLimitation.AGGREGATE_EVIDENCE_ONLY,
    AuditLimitation.HASH_ONLY_REFERENCE,
]
```

This explicitly tells downstream consumers: "This profile summary is aggregate; individual artifact text is not available."

**Verdict: ✅ Privacy is enforced by design. No raw text, opaque source IDs, no paths in exported profiles.**

---

### 6. Determinism and Provider Neutrality

**Status: ✅ Excellent**

**Compiler is deterministic:**

Test `test_compilation_is_deterministic` verifies that running the same compiler on the same inputs produces byte-for-byte identical JSON output.

The compiler uses only deterministic operations:
- `defaultdict` and `sorted()` for grouping (deterministic ordering)
- `fmean()` for averaging (deterministic)
- `sha256()` for hashing (deterministic)
- No random seeds, no shuffling, no network calls

**No LLM or embedding dependencies:**

Test `test_compiler_uses_no_provider_or_llm_manifest_dependencies` verifies:
- ✅ `model_provider` is `None`
- ✅ `model_name` is `None`
- ✅ `model_version` is `None`
- ✅ `profile_affecting_model_invocations` is empty

The compiler uses only local, rule-based logic. No API calls, no embeddings, no semantic inference.

**Provider-neutral confidence model:**

The confidence formula weights artifact-level components (attribution, authorship_origin, extraction, evidence_strength, policy_fit) and applies a deterministic support-count factor. No model-specific tuning or provider-specific assumptions.

Formula documented in code and design spec:
```
display = clamp(
  (0.20*avg(attribution) + 0.20*avg(authorship_origin) + 0.20*avg(extraction)
   + 0.20*avg(evidence_strength) + 0.10*source_diversity + 0.10*avg(policy_fit))
  * min(1.0, 0.55 + 0.15 * included_support_count),
  low=0.05, high=0.95
)
```

**Verdict: ✅ Determinism and provider neutrality are guaranteed. No external dependencies, deterministic algorithm, reproducible output.**

---

### 7. Scalability: Linear-Time Baseline, No Cross-Signal Quadratic Logic

**Status: ✅ Excellent**

**Compilation time is linear in artifacts:**

The algorithm:
1. Build lookup dicts: O(n) for artifacts, classifications, signals
2. Group signals by pattern key: O(n log n) for sorting
3. Compile signals: O(n) for each signal, O(n) for evidence refs per signal

Total: O(n log n) due to sorting, which is acceptable.

**No cross-signal quadratic logic:**

The compiler does NOT:
- Compare every signal to every other signal
- Build pairwise similarity matrices
- Perform O(n²) distance calculations
- Recurse across signal chains

Each signal is compiled independently based on its artifact grouping. The grouping uses deterministic hashing and sorting, not comparisons.

**Evidence preservation is linear:**

For each compiled signal, the compiler:
- Creates evidence references from contributing candidates (direct iteration)
- Records version metadata (set union, then sorted list)
- Hashes support metadata for the profile ID (single hash, not pairwise)

No nested loops across signals.

**Verdict: ✅ Baseline compiler scales linearly. No quadratic cross-artifact logic.**

---

## Unresolved Items and Deferred Work

### Items Resolved in Implementation

1. ✅ **Claim-level validation** — Compiler rejects PROHIBITED, gates BOUNDED_INTERPRETATION, allows OBSERVATION.
2. ✅ **Signal eligibility** — Only durable observation signals from included artifacts compile into durable support.
3. ✅ **Version compatibility** — Incompatible signal model versions rejected; classifier versions recorded.
4. ✅ **Evidence preservation** — Full support chain maintained with opaque source IDs and version metadata.
5. ✅ **Privacy enforcement** — No raw text, opaque source IDs, validated against paths.

### Deferred to Sprint 07 and Beyond

1. **Report generation and export formats** — Sprint 07 will handle exporting profiles to human-readable formats.
2. **Publishing contracts and downstream prompts** — Experience layer (how profiles are used by applications) is Sprint 07+.
3. **Context profile enrichment** — Minimal scaffolding implemented; future work can add richer filtering, divergence tracking, and inheritance policies.
4. **Bounded interpretation review workflow** — Compiler supports the flag; actual review UI/tool is not in scope.
5. **Confidence model tuning** — Baseline weights documented; production tuning against labeled data is future work.
6. **Multi-voice profile support** — Basic context profiles by source type; more sophisticated voice separation (casual vs. technical) is deferred.

### No Blockers

All seven architectural gates passed. No architectural issues prevent Sprint 07.

---

## Go / No-Go Decision

### ✅ GO for Sprint 07

**Verdict:** Sprint 06 profile compiler is architecturally sound, strictly bounded, and ready for export and first-run experience work.

**Recommended carry-forward constraints for Sprint 07:**

1. Do not weaken claim-level validation. PROHIBITED signals must remain errors; BOUNDED_INTERPRETATION must remain policy-gated.
2. Do not merge incompatible signal model versions without an explicit migration layer.
3. Keep source IDs opaque in all export formats. Do not expose `artifact.reference.source_id` as-is to consumers.
4. Maintain the no-raw-text policy in exports. Profiles are summaries, not raw-text archives.
5. If context profiles are enriched, preserve the explicit filter/divergence model. No hidden inheritance or implicit source-type magic.

**Before Sprint 07 ships:**

- [ ] Report generation and export format contracts (critical for MVP).
- [ ] First-run experience testing (feature evaluation).
- [ ] Context profile enrichment if needed (product-level decision).
- [ ] Confidence model baseline tuning against labeled data (not required for MVP but advisable).

---

## Appendix: Review Checklist

### Claim Boundaries
- [x] No personality typing in compiled claims.
- [x] No diagnostic claims.
- [x] No intent attribution.
- [x] Expression-pattern-only scope enforced by design.
- [x] Claim template prevents person-level claims structurally.

### Signal Eligibility
- [x] Quarantined signals excluded from durable support.
- [x] Non-durable signals excluded.
- [x] Excluded artifacts produce no signals, no claims.
- [x] Prohibited signals rejected with CompilerError.
- [x] Bounded interpretations excluded by default, gated by policy flag.
- [x] Tests verify all eligibility paths.

### Evidence Discipline
- [x] Every compiled signal preserves contributing artifact IDs, source IDs, rule IDs, version metadata.
- [x] Source IDs are opaque and validated.
- [x] Classification model versions recorded.
- [x] Signal model versions recorded.
- [x] Build manifest records full lineage.
- [x] Configuration hash enables reproducibility verification.

### Version Compatibility
- [x] Incompatible signal model versions rejected.
- [x] Classifier versions mixed (recorded, not rejected).
- [x] Comparability information is machine-readable.
- [x] Version boundaries are documented.

### Privacy
- [x] No raw text in compiled profiles.
- [x] No filesystem paths in exported data.
- [x] Source IDs are opaque.
- [x] Source ID validation prevents path leakage.
- [x] Audit limitations disclosed.
- [x] Serialized profile contains no private data.

### Determinism and Provider Neutrality
- [x] Compiler is deterministic (byte-for-byte identical output).
- [x] No LLMs, embeddings, or remote API calls.
- [x] No model provider dependencies.
- [x] Confidence formula is deterministic and documented.
- [x] Local rule-based logic only.

### Scalability
- [x] Baseline compilation is O(n log n).
- [x] No cross-signal quadratic logic.
- [x] Evidence preservation is linear.
- [x] No pairwise comparisons or distance matrices.

### Testing
- [x] 17 compiler tests, all passing.
- [x] Tests cover happy path, eligibility boundaries, version handling, privacy, determinism, and error paths.
- [x] CLI is wired and smoke-tested.

---

## Closing

Sprint 06 successfully implements a strict, evidence-driven profile compiler that acts as a critical validation barrier in the pipeline. It rejects incompatible versions, prohibited claims, and malformed inputs; it preserves full evidence chains with opaque source IDs; and it maintains the privacy and determinism guarantees established in earlier sprints.

The implementation is ready for profile export and first-run experience work. The remaining scope is productization, not architecture.

---

**Sign-off:** ✅ GO for Sprint 07 exports and first-run experience.
