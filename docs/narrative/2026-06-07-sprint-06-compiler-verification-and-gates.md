# Sprint 06: Compiler Architecture Review and Verification Gates

The adversarial review of Sprint 06 profile compiler implementation examined the boundary between artifact-level signal aggregation and profile-level compilation. The compiler successfully enforces strict eligibility gates, preserves the full evidence chain with version metadata, and prevents claim-level violations from silently entering durable support. All seven architectural gates passed; the compiler is ready for Sprint 07 export and first-run experience work.

## The Seven Architectural Gates

The Sprint 06 adversarial review focused on seven dimensions, each with explicit pass/fail criteria:

### 1. Claim Boundaries: Expression Patterns Only, No Personality or Diagnosis

The risk was that profile compilation could upgrade artifact-level observations into person-level psychological or diagnostic claims. The gate checked whether the compiler enforces expression-pattern-only boundaries.

**What we found:** The `_claim_text()` method produces claims with a rigid template:

```python
"Across included artifacts, {observed_feature} appears in {included_count} {count_label}."
```

Examples from the test suite:
- "Across included artifacts, all observed paragraphs are short appears in 2 artifacts."
- "Across included artifacts, the artifact uses heading formatting appears in 1 artifact."

This template makes person-level claims structurally impossible. There is no field for "the subject is X" or "indicates Y condition." The claim is always about the artifact set, never the person.

**Validation layer:** The compiler checks `claim_level` before compilation:
- `ClaimLevel.PROHIBITED` → `CompilerError` (rejects immediately)
- `ClaimLevel.QUARANTINED` → skipped from durable support
- `ClaimLevel.BOUNDED_INTERPRETATION` → excluded unless `allow_bounded_interpretations=True`
- `ClaimLevel.OBSERVATION` → only this level supports durable claims

Test coverage: `test_prohibited_signals_are_rejected_even_if_constructed_unsafely` creates a PROHIBITED signal and verifies the compiler rejects it with `CompilerError: prohibited signal cannot compile: ...`

**Verdict: ✅ PASS** — Claim boundaries are enforced by template design and validation logic. Expression-pattern-only scope is maintained.

### 2. Signal Eligibility: Quarantined, Non-Durable, and Prohibited Signals Excluded from Durable Support

The risk was that quarantined signals (from uncertain artifacts), non-durable signals (from low-confidence candidates), or prohibited signals could leak into durable profile support, poisoning the profile with weak or unsafe claims.

**What we found:** The `_eligible_candidates()` method implements a multi-stage filter cascade:

```python
1. Source ID validation (validate_source_id() - rejects paths)
2. Artifact lookup (fails if missing)
3. Classification lookup (fails if missing)
4. Classification ID matching (fails if mismatched)
5. PROHIBITED level rejection (fails with CompilerError)
6. Durable check (skips if durable=false)
7. Included classification check (skips if quarantined/excluded)
8. BOUNDED_INTERPRETATION policy gate (skips unless flag set)
9. OBSERVATION-only filter (final gate)
```

Each stage filters out candidates that don't meet the durable support bar. Only signals passing all nine checks enter the eligible list.

Test coverage:
- ✅ `test_only_durable_observation_signals_compile` — durable observations enter profile support
- ✅ `test_quarantined_signals_do_not_support_profile_claims` — quarantined candidates produce empty profile
- ✅ `test_excluded_artifacts_produce_no_profile_support` — excluded artifacts produce no signals, no claims
- ✅ `test_non_durable_candidates_do_not_support_profile_claims` — non-durable candidates skipped
- ✅ `test_prohibited_signals_are_rejected_even_if_constructed_unsafely` — PROHIBITED level rejects
- ✅ `test_bounded_interpretations_are_excluded_by_default` — BOUNDED_INTERPRETATION excluded by default
- ✅ `test_bounded_interpretations_compile_only_with_review_gated_policy` — BOUNDED_INTERPRETATION compiles with explicit flag

**Additional safety:** The compiler rejects incompatible signal model versions rather than silently merging them. The `_reject_incompatible_signal_model_versions()` method checks that all eligible candidates come from the same signal extraction version. If candidates came from different signal model versions, compilation fails with:

```
CompilerError: cannot merge incompatible signal model versions: sprint05-rule-v1, other-v1
```

This is a critical boundary: future extraction rule changes (e.g., from v1 to v2) won't silently merge old and new signals into misleading profiles. Test coverage: `test_incompatible_signal_model_versions_are_rejected`.

**Verdict: ✅ PASS** — Signal eligibility gates are strict, multi-layered, and tested. No quarantined, non-durable, prohibited, or incompatible signals leak into durable support.

### 3. Evidence Discipline: Full Support Chain Preserved with Versioning

The risk was that profile compilation could lose track of which artifacts, signals, and rules contributed to each compiled claim, making it impossible for downstream consumers to audit the evidence chain.

**What we found:** Every compiled `Signal` preserves a `SignalSupport` object containing:

```python
SignalSupport(
    signal_ids=[...],                      # Contributing artifact-level signal IDs
    classification_model_versions=[...],   # Which classifier produced artifact labels
    signal_model_versions=[...],           # Which extractor produced signals
    rule_ids=[...],                        # Which extraction rules fired
    evidence_refs=[...],                   # Full references to contributing artifacts
    artifact_count=N,                      # Total artifacts in this compiled signal
    included_count=N,                      # How many were INCLUDED
    excluded_count=0,
    quarantined_count=0,
    source_types=[...],                    # Source type diversity
    source_diversity=float,
    audit_limitations=[...],               # Public-safe disclosure
)
```

Each `EvidenceReference` includes:
- `artifact_ref.artifact_id` (opaque artifact identifier)
- `artifact_ref.source_id` (opaque, validated to not contain paths)
- `classification_id` (which classification was used)
- `authorship_origin` (the authorship label from classification)

The support object is the audit trail. If a downstream consumer questions where a claim came from, they can follow: signal ID → evidence refs → artifact IDs and source IDs, then cross-reference the build manifest for model versions.

Test coverage: `test_profile_support_preserves_public_safe_versioned_metadata` verifies all four key properties:
- Source IDs start with `source-`, no paths
- Classification and signal model versions are recorded
- Evidence references point to valid artifacts and source IDs
- Raw content is marked unavailable

**Build manifest records full lineage:**

The profile's `BuildManifest` includes:
- `schema_version="0.1"`
- `compiler_version="sprint06-rule-v1"`
- `classifier_version="sprint04-rule-v1,sprint04-rule-v2"` (all versions seen)
- `extractor_code_version="sprint05-rule-v1,sprint05-rule-v2"` (signal versions)
- `model_provider=None`, `model_name=None`, `model_version=None` (no LLM dependency)
- `config_hash="sha256:..."` (deterministic fingerprint for reproducibility)

Test coverage: `test_mixed_classifier_versions_are_recorded_in_support_and_manifest` creates artifacts classified with two different versions and verifies both are recorded in the manifest and support metadata.

**Verdict: ✅ PASS** — Evidence discipline is excellent. Full support chain is preserved with opaque source IDs and version metadata recorded throughout.

### 4. Version Compatibility: Incompatible Changes Detected and Rejected

The risk was that profiles built from signals extracted with incompatible versions would silently merge, creating profiles that look consistent but combine semantically different signals.

**What we found:** The compiler enforces two version boundaries:

**Signal model version (strict rejection):**
- All eligible signals must come from the same `signal_model_version`
- If different versions are present, compilation fails outright
- Test: `test_incompatible_signal_model_versions_are_rejected`

This prevents future extraction rule changes (e.g., from `sprint05-rule-v1` to `sprint06-rule-v2`) from silently merging incompatible signal semantics. If the extractor changes, the version changes, and any attempt to compile mixed versions fails loudly.

**Classifier version (recorded for downstream review):**
- Mixed classifier versions are recorded in the build manifest and support metadata
- The compiler does NOT reject mixed versions; instead, it flags them for downstream review
- This is correct: a classifier version change may represent a bug fix (compatible) or a semantic change (breaking). Recording both versions lets downstream tools make the decision
- Test: `test_mixed_classifier_versions_are_recorded_in_support_and_manifest`

**Configuration hash for reproducibility:**

The `_config_hash()` method creates a deterministic hash over:
- Compiler version
- All artifact IDs
- All classification IDs
- All signal IDs
- All signal model versions

Two profiles built from the same inputs will have the same config hash. Profiles with different hashes are not directly comparable. Test: `test_compilation_is_deterministic` verifies byte-for-byte output reproducibility.

**Verdict: ✅ PASS** — Version compatibility is enforced and documented. Incompatible signal model versions are rejected; classifier versions are recorded for downstream review.

### 5. Privacy: No Raw Text, Opaque Source IDs, No Filesystem Paths

The risk was that compiled profiles could expose raw artifact text, filesystem paths, or private metadata that should remain local.

**What we found:** Privacy is enforced at three levels:

**Raw text exclusion:**

Test `test_public_safe_compiled_profile_excludes_raw_text_and_paths` serializes the entire profile to JSON and verifies it contains:
- ✅ No artifact text excerpts (e.g., "Start here")
- ✅ No filenames (e.g., "signal-transcript.json")
- ✅ No filesystem paths (e.g., "/tests/fixtures/")

The compiled profile includes only:
- Pattern descriptions (generic, e.g., "the artifact uses heading formatting")
- Metadata (artifact IDs, source types, version info)
- Support counts and confidence scores
- Opaque evidence references

**Source ID opacity and validation:**

Every source ID is validated on compilation. Test: `test_path_like_source_ids_are_rejected`. The validation rejects:
- Absolute paths (`/home/...`)
- Windows paths (`C:\...`)
- Path traversal (`../../../`)
- File extensions (`.json`, `.yaml`, `.csv`, `.db`)

If an adapter accidentally passes a path, compilation fails loudly with: `ValueError: source_id cannot expose filesystem paths`.

**Artifact metadata safety:**

`EvidenceReference.artifact_ref` contains:
- `artifact_id` (opaque)
- `source_id` (opaque, validated)
- `source_type` (e.g., "local_transcript_json", safe string)
- `artifact_type` (e.g., "transcript_segment", enum)

No filesystem paths or raw content are preserved anywhere.

**Audit limitations disclosure:**

Every profile's `SignalSupport` includes:

```python
audit_limitations=[
    AuditLimitation.RAW_CONTENT_UNAVAILABLE,
    AuditLimitation.AGGREGATE_EVIDENCE_ONLY,
    AuditLimitation.HASH_ONLY_REFERENCE,
]
```

This explicitly tells downstream consumers: "This profile summary is aggregate; individual artifact text is not available."

**Verdict: ✅ PASS** — Privacy is enforced by design. No raw text, opaque source IDs, no paths in exported profiles.

### 6. Determinism and Provider Neutrality

The risk was that profile compilation could introduce non-determinism (randomness, timing-dependent behavior) or create undeclared dependencies on LLMs, embeddings, or external providers.

**What we found:** The compiler is deterministic and provider-neutral.

**Determinism test:**

Test `test_compilation_is_deterministic` runs the same compiler on the same inputs twice and compares the JSON output. Both runs produce byte-for-byte identical results.

The compiler uses only deterministic operations:
- `defaultdict` and `sorted()` for grouping (deterministic ordering)
- `fmean()` for averaging (deterministic)
- `sha256()` for hashing (deterministic)
- No random seeds, no shuffling, no network calls

**No LLM or embedding dependencies:**

Test `test_compiler_uses_no_provider_or_llm_manifest_dependencies` verifies:
- ✅ `profile.build_manifest.model_provider` is `None`
- ✅ `profile.build_manifest.model_name` is `None`
- ✅ `profile.build_manifest.model_version` is `None`
- ✅ `profile.build_manifest.profile_affecting_model_invocations` is empty

The compiler uses only local, rule-based logic. No API calls, no embeddings, no semantic inference.

**Provider-neutral confidence formula:**

The confidence formula weights artifact-level components (attribution, authorship_origin, extraction, evidence_strength, policy_fit) and applies a deterministic support-count factor. No model-specific tuning or provider-specific assumptions.

Formula (documented in code and `docs/PROFILE_COMPILATION_RULES.md`):

```
display = clamp(
  (0.20*avg(attribution) + 0.20*avg(authorship_origin) + 0.20*avg(extraction)
   + 0.20*avg(evidence_strength) + 0.10*source_diversity + 0.10*avg(policy_fit))
  * min(1.0, 0.55 + 0.15 * included_support_count),
  low=0.05, high=0.95
)
```

**Verdict: ✅ PASS** — Determinism and provider neutrality are guaranteed. No external dependencies, deterministic algorithm, reproducible output.

### 7. Scalability: Linear-Time Baseline, No Cross-Signal Quadratic Logic

The risk was that profile compilation could introduce O(n²) cross-artifact or cross-signal logic that would fail to scale.

**What we found:** Baseline compiler is O(n log n) and contains no quadratic logic.

**Compilation algorithm:**

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

**Verdict: ✅ PASS** — Baseline compiler scales linearly. No quadratic cross-artifact logic.

## Summary: All Seven Gates Passed

| Gate | Result | Evidence |
|---|---|---|
| Claim boundaries | ✅ PASS | Template design + validation layer prevent person-level claims |
| Signal eligibility | ✅ PASS | Multi-stage filter cascade + version checking |
| Evidence discipline | ✅ PASS | Full support chain preserved with opaque IDs and versioning |
| Version compatibility | ✅ PASS | Signal versions rejected if incompatible; classifier versions recorded |
| Privacy | ✅ PASS | No raw text, opaque source IDs, paths validated and rejected |
| Determinism | ✅ PASS | Byte-for-byte reproducibility; no LLMs, embeddings, or providers |
| Scalability | ✅ PASS | O(n log n) baseline; no quadratic cross-signal logic |

## What's Unblocked for Sprint 07

1. **Expression profiles are now computable** from ingested and classified artifacts and extracted signals.
2. **Profile evidence chains are fully versioned and traceable** back to source artifacts and extraction rules.
3. **Claim-level validation is enforced:** PROHIBITED claims rejected, BOUNDED_INTERPRETATION policy-gated, OBSERVATION-only for durable support.
4. **Incompatible extraction rule changes are detected and rejected** (signal model version mismatch causes compilation error).
5. **Profile privacy is enforced:** no raw text, opaque source IDs, validated against path leakage.
6. **Sprint 07 can proceed** with export formats, report generation, and first-run experience design.

## Carry-Forward Constraints for Sprint 07

1. Do not weaken claim-level validation. PROHIBITED signals must remain errors; BOUNDED_INTERPRETATION must remain policy-gated.
2. Do not merge incompatible signal model versions without an explicit migration layer.
3. Keep source IDs opaque in all export formats. Do not expose `artifact.reference.source_id` as-is to consumers.
4. Maintain the no-raw-text policy in exports. Profiles are summaries, not raw-text archives.
5. If context profiles are enriched, preserve the explicit filter/divergence model. No hidden inheritance or implicit source-type magic.

---

**See `CHANGES.md` Phase 3 and 3.5 for the chronological diff summary.**
