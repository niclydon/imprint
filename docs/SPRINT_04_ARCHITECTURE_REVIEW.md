# Sprint 04 Architecture Review: Classification Engine Implementation

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Post-implementation gate review  
**Context:** Evaluation of the implemented Sprint 04 classification engine against evidence boundaries, explainability, and Sprint 05 readiness

---

## Executive Summary

Sprint 04 now has a real implemented classifier, not just a design. The implementation remains
conservative, local-first, and artifact-scoped. It preserves the Sprint 03.5 ingestion boundary by
treating adapter metadata as advisory evidence rather than classification truth.

The implementation also closes the major pre-implementation gaps:

1. **Confidence scoring is now explicit and versioned.**
2. **Quarantine vs. exclusion behavior is now defined and testable.**
3. **Pathological-case handling is documented for the baseline rule set.**
4. **Performance targets and scaling assumptions are documented.**

**Verdict: GO for Sprint 05**

Sprint 05 can begin. The remaining concerns are not architectural blockers; they are follow-on
productization items such as large-scale benchmarking, broader source-family coverage, and future
audit-path design.

---

## Strengths: What Sprint 04 Implemented Correctly

### 1. Adapter Hints Remain Evidence, Not Truth

**Status: ✅ Excellent**

The classifier consumes normalized `Artifact` objects and re-assesses:

- adapter-provided authorship hints
- adapter-provided confidence hints
- adapter-provided inclusion/exclusion hints
- adapter-provided artifact-type hints

The JSONL path is especially important here: record-level metadata is preserved as `source_hints`
but does not automatically become final classification output.

**Result:** Sprint 03.5’s safety boundary holds in code, not just in docs.

### 2. Classification Remains Deterministic and Local-Only

**Status: ✅ Excellent**

The implemented classifier in `src/imprint/classification/engine.py`:

- is rule-based,
- has no provider or network dependency,
- keeps artifact decisions local to each artifact,
- does not invoke LLMs, embeddings, or remote APIs.

This preserves reproducibility and avoids provider drift inside the classification layer.

### 3. Confidence Scoring Is Now Explicit and Versioned

**Status: ✅ Resolved**

Sprint 04 now defines a versioned confidence contract:

- `model_version`
- `attribution`
- `authorship_origin`
- `evidence_strength`
- `source_reliability`
- `policy_fit`
- `contamination_penalty`
- `display`

The scoring model is deterministic, documented, and emitted as structured output. This is the
minimum needed to keep future changes visible instead of silently redefining confidence semantics.

### 4. Quarantine vs. Exclusion Is Operationally Defined

**Status: ✅ Resolved**

The implementation now follows a clear policy:

- **Exclude** artifacts that are confidently non-subject or low-value for profile construction
  (`assistant_output`, `template_or_notification`)
- **Quarantine** artifacts that may still matter contextually but have uncertain authorship,
  contamination, or parsing risk (`quoted_or_forwarded`, `unknown_speaker`, `missing_metadata`,
  `parser_uncertain`, `mixed_authorship`, `suspected_ai_assisted`,
  `human_directed_ai_assisted`, oversized artifacts)
- **Include** only artifacts that are low-contamination, confidently human-origin, and above the
  confidence floor

This closes a major ambiguity from the pre-implementation review.

### 5. Explainability Is First-Class in the Result Contract

**Status: ✅ Good**

Each classification result includes:

- artifact ID
- opaque source ID
- source type
- considered source hints
- rule IDs
- limitations
- evidence summary
- quote/forward likelihood
- template/notification likelihood
- assistant-output likelihood
- contamination risk
- structured confidence

This is sufficient for downstream review, debugging, and future audit tooling.

### 6. Privacy Boundary Still Holds

**Status: ✅ Good**

The classifier does not reconstruct local filesystem paths from opaque `source_id` values, and the
schema rejects path-like or raw-text fields in `source_hints`.

**Result:** The classification layer does not reopen the privacy leak fixed in Sprint 03.5.

---

## Remaining Risks (Not Sprint 05 Blockers)

### 1. Performance Targets Are Documented, Not Yet Benchmarked

**Status: ⚠️ Needs follow-through**

Sprint 04 now documents targets such as:

- 1M artifacts in under 1 hour
- under 2GB steady-state memory
- linear scaling in artifact count
- under 1KB explainability output per artifact

However, these are still targets and assumptions, not measured benchmark results.

**Assessment:** Acceptable for Sprint 05 start. Not sufficient for production-scale claims.

### 2. Pathological Case Coverage Is Curated, Not Exhaustive

**Status: ⚠️ Acceptable**

Sprint 04 now documents and partially handles:

- oversized artifacts
- malformed/weak metadata
- unsupported source-shape heuristics
- mixed-language or contradictory-marker uncertainty

But several families remain deferred:

- implicit email forwarding without markers
- translation detection
- system/log/auto-generated content families
- cross-artifact context reconstruction

**Assessment:** This is a bounded MVP rule inventory, not an architectural failure.

### 3. Confidence Model Stability Now Depends on Version Discipline

**Status: ⚠️ Watch item**

The implementation is materially better because confidence is versioned. But this creates a new
operational requirement: future changes must actually bump the model version and treat old/new
results as potentially non-comparable.

**Assessment:** Manageable, but only if future work is disciplined.

### 4. No Full Local Audit Mapping Yet

**Status: ⚠️ Deferred**

Opaque source IDs protect privacy, but there is still no dedicated private-local audit surface that
maps those IDs back to original local file locators when a user explicitly needs review.

**Assessment:** Not a blocker for Sprint 05 classification/extraction work. Relevant for later
review tooling.

---

## Sprint 05 Readiness

### What Sprint 05 Can Reliably Assume

- classification output is deterministic and local-first
- adapter hints do not bypass classification
- quarantine/exclusion semantics are explicit
- confidence output has a stable versioned shape
- opaque source IDs remain opaque
- explainability output exists for every classification result

### What Sprint 05 Should Not Assume

- large-scale throughput has been benchmarked
- every real-world source family is covered by rules
- quarantined artifacts are automatically resolvable without future review tooling
- confidence formulas may change silently

---

## Findings by Severity

### Blockers

None.

### Majors

1. **Benchmark gap**
   - Performance targets are documented but not yet validated at scale
   - Matters for deployment claims, not for Sprint 05 feature work

2. **Coverage gap**
   - Deferred source families still need explicit future rules
   - Matters for breadth, not baseline architecture

### Minors

3. **Audit-path deferral**
   - No private-local opaque-ID-to-path mapping yet

4. **Version-governance dependency**
   - Confidence stability now depends on disciplined model-version updates

---

## Go / No-Go Decision

### ✅ GO for Sprint 05

**Verdict:** Sprint 04 implementation is architecturally sound and sufficiently specified for the
next sprint.

**Recommended carry-forward constraints for Sprint 05:**

1. Treat `ClassificationConfidence.model_version` as a compatibility boundary.
2. Do not add cross-artifact quadratic logic to the baseline classifier path.
3. Keep quarantined artifacts out of durable signal support unless a later review stage explicitly
   promotes them.
4. If Sprint 05 broadens source-family coverage, update the documented rule inventory and
   pathological-case list at the same time.

---

## Closing

Sprint 04 is no longer waiting on specification closure. The major design gaps from the earlier
review have been addressed in code, schema, tests, and docs.

The remaining work is practical hardening: benchmark the current implementation, widen rule
coverage carefully, and add private-local audit tooling when needed.

That is a healthy place to start Sprint 05.

---

## Appendix: Sprint 05 Carry-Forward Checklist

Before shipping Sprint 05 work that depends on classification, verify:

- [x] Confidence component scoring model defined and implemented
- [x] Quarantine vs. exclusion logic explicit and tested
- [ ] Performance targets benchmarked at meaningful scale
- [x] Pathological cases documented for current baseline
- [x] Rule inventory distinguishes covered vs deferred behavior
- [x] Tests prove adapter hints do not bypass logic
- [x] No diagnostic or personality claims in rules
- [x] Classification boundary preserved (no signal extraction)
