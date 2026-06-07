# Sprint 01.5 Architecture Review

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for Sprint 02  
**Context:** Evaluation of remediation work against adversarial findings from Sprint 01

---

## Executive Summary

Sprint 01.5 took the refusals from the adversarial review and converted them into **constraint policies** rather than solutions.

The architecture blockers are not resolved. They are **mitigated with guardrails** that work only if followed.

**Verdict: CONDITIONAL GO for Sprint 02** 

Sprint 02 may proceed IF the implementation team commits to the policies in these documents. If implementation shortcuts the constraints for convenience, the project will collapse into the same paradoxes identified in Sprint 01.

---

## Resolved Issues (Actual Fixes)

### 1. Terminology: Moved from Diagnostic to Observational

**Status: ✅ Resolved**

The schema retired `identity.stance` and `identity.recurring_lens` in favor of:
- `expression_posture.patterns[]` (structured observations)
- `rhetorical_patterns` (evidence-backed observations)
- `claim_levels` (observation, bounded_interpretation, prohibited)

This is a real improvement. The schema example `"evidence_before_generalization"` is an observable pattern, not a personality claim. The claim-level system creates a safety valve.

**However:** The implementation must enforce claim validation. There is no validation framework yet. It's entirely possible for Sprint 02 extractors to ship fields labeled `bounded_interpretation` that are actually diagnostics (e.g., `"argumentative_personality"`). The policy is good; the enforcement mechanism is missing.

### 2. Export Boundaries: Downstream Owns Prompts

**Status: ✅ Resolved**

The phrase "publishing prompt contract exporter" is retired. Core Imprint exports profile contracts, not generation-ready prompts. Downstream adapters translate contracts into prompts.

This is clear and defensible. The boundary is explicit.

**However:** This boundary can be undermined by incremental creep. An "expression-to-prompt adapter" shipped in the same repo, then a "default adapter," then "adapter rules compiled into the schema," then suddenly Imprint is a prompt system. The policy document is a guardrail, not a wall.

### 3. AI Detection: Treated as Weak Evidence

**Status: ✅ Resolved**

Authorship-origin classification no longer claims to detect AI. Detectors may contribute weak evidence, but unknown remains unknown. Unknown authorship reduces confidence and may trigger quarantine.

This is appropriately cautious and honest.

**However:** "Weak evidence" is vague. If a detector is 85% accurate on technical writing and your corpus is technical, is that weak? The confidence-reduction rule ("unknown or weakly supported authorship reduces confidence") is implemented in code, not checked by policy. A careless implementation could weight AI-detector confidence higher than the policy intends.

---

## Unresolved Blockers (Not Fixed, Only Renamed)

### 1. LLM Coupling and Profile Determinism — NOT RESOLVED

**Original blocker:** Profile drift cannot be distinguished from model drift when using LLM extraction. Claiming a profile is "portable" across model versions is false.

**Remediation offered:** Record build manifest with all component versions. Label drift as `expression_drift`, `compiler_drift`, or `corpus_drift`.

**Hostile assessment:** This does NOT resolve the blocker. It DOCUMENTS it.

**The problem remains:** If a profile compiled with Claude 3.5 Sonnet is re-extracted with Llama 3.1, the semantic signals WILL change. Recording that this is `compiler_drift` does not make the profile portable or comparable. A downstream system consuming both profiles has no principled way to reconcile their differences.

**Example:** Master profile compiled with Claude says "frequently explains decisions through first-principles reasoning" (confidence 0.84). Same corpus re-extracted with Llama says "often provides step-by-step operational procedures" (confidence 0.76). Are these the same pattern described differently, or did the person's expression change? The manifest records the model change, but the downstream system still cannot answer the question.

**Impact:** Profiles are NOT stable across model changes. They are DOCUMENTED to be unstable. Users will assume a re-compiled profile using a different model is meaningfully comparable to the original — and it is not.

**Verdict:** Blocker remains. Mitigation is honest bookkeeping, not a fix. Sprint 02 must define what "comparable" means operationally and whether cross-model profile updates are even supported.

### 2. Artifact Storage and Auditability — DEFERRED, NOT RESOLVED

**Original blocker:** You cannot have auditability and regeneration without storing raw text locally. But storing raw text creates a privacy problem that contradicts the "we are not a memory system" claim.

**Remediation offered:** Three storage modes (metadata-only, local artifact store, ephemeral). Users choose.

**Hostile assessment:** This is a CHOICE, not a resolution.

**The problem remains:** 
- If you choose `metadata_only`, auditability is weak. A user asks "why did you extract this signal?" and Imprint says "see artifact ID 423" but doesn't show the text. Re-extracting requires re-harvesting from the original source, which may be gone or require credentials.
- If you choose `local artifact store`, Imprint becomes a repository of the user's sensitive communication history. This IS a memory system, despite the policy claim that "the artifact store exists for compilation, not recall."

**The DEFAULT is never specified:** The policy says MVP default should include "raw text stored only when the user explicitly enables the local Artifact Store." But then how does the default MVP provide auditability? It doesn't. So the default mode concedes auditability.

**What the remediation actually does:** It makes the privacy/auditability tradeoff explicit and lets the user decide. That's honest, but it's not a resolution. The tradeoff still exists; it's just more transparent.

**Verdict:** Blocker remains. Policy successfully reframes the problem as a user choice, but the underlying tension is unresolved. Implementation must decide: Is Imprint a local memory store for power users, or a stateless compiler for privacy-conscious users? You cannot be both.

### 3. Derived Profile Inheritance — CONSTRAINED BUT INCOMPLETE

**Original blocker:** No operational model for how derived profiles inherit, override, or merge signals. When master and context profiles diverge, how is this represented?

**Remediation offered:** Explicit compiled views with baseline references, filters, divergences, and collision labels. No hidden inheritance.

**Hostile assessment:** This is PHILOSOPHICALLY sound but OPERATIONALLY vague.

**What we know:**
- Derived profiles reference a baseline profile ID and version ✓
- They declare context filters (e.g., artifact_types: ["technical_note"]) ✓
- They record divergences (e.g., "casual artifacts use shorter paragraphs") ✓
- Collisions are preserved, not flattened ✓

**What we don't know:**
- How are divergences represented in the schema? (The SCHEMA.md shows only structure, no example divergence object.)
- How are context-specific signals compiled? Do they re-run extractors for filtered evidence? Re-compile the baseline signals with context weights? Use a merge rule?
- If re-running extractors per context, how is cost amortized? That's O(n_contexts) extraction runs.
- If using merge rules, what are they? This is deferred to Sprint 02.
- How does "preserve the conflict" work in practice? Example: baseline says "high lexical complexity," casual says "low lexical complexity," technical says "very high." Does the export include all three? An array of context values?

**The schema SHAPE is there, but the LOGIC is not.** Example:
```json
"context_profiles": [
  {
    "baseline_profile_id": "example_subject_master",
    "context": "technical",
    "divergences": []
  }
]
```

The `divergences` array is empty in the schema example. This is not a coincidence; it's a signal that the divergence model is incomplete.

**Verdict:** Blocker is constrained (no hidden inheritance) but not resolved (merge semantics are TBD). Sprint 02 must define the divergence data model and compilation logic.

---

## Deferred Non-Blockers (Acceptable to Defer)

### 1. Exact Database Encryption Mechanism
✅ Acceptable. Implementation detail. Can be added later without schema changes.

### 2. Exact Drift Distance Metrics
✅ Acceptable. Deferred to Sprint 02 after evidence model is finalized.

### 3. Downstream Prompt Adapter Design
✅ Acceptable. Outside core scope. Adapters are separate projects.

### 4. Private Connector Prioritization
✅ Acceptable. Doesn't block core schema.

---

## Findings by Severity

### Blockers (Must Fix Before Sprint 02 Ends)

1. **Profile Comparability Across Model Changes**
   - Problem: Re-extracting with different LLM produces incomparable results
   - Current state: Documented in build manifest, not solved
   - Action: Define "compatible" operationally (same extractor family? same model family?). Decide: do we support cross-model migration or not?
   - Risk: Users assume profiles are model-agnostic. They are not.

2. **Artifact Storage Default**
   - Problem: Metadata-only default concedes auditability; local storage default creates privacy risk
   - Current state: Policy offers modes, does not specify default
   - Action: Specify the MVP default storage mode. Accept the tradeoff. Acknowledge the downstream consequence.
   - Risk: If default is metadata-only, early users get weak auditability and complain. If default is local, early users get privacy risk and complain.

3. **Claim Validation Framework**
   - Problem: Schema allows prohibited claims; enforcement is missing
   - Current state: Policy defines claim levels, no validator exists
   - Action: Build validation into the schema compiler. Prohibited claims must fail schema validation or be quarantined before profile export.
   - Risk: If claim validation is not enforced, extractors will ship prohibited claims and the safety guardrail becomes decorative.

### Majors (Should Fix Before Sprint 02, Can Defer If Documented)

4. **Divergence Model Completeness**
   - Problem: How divergences are represented, stored, and merged is undefined
   - Current state: Policy says "explicit divergences" but schema example is empty
   - Action: Document a concrete divergence object with examples. Define how downstream systems consume divergences.
   - Mitigation: If deferred, document that context profiles may not be usable until Sprint 02.x.

5. **Downstream Adapter Boundary**
   - Problem: "Downstream systems own prompt assembly" is clear in principle but can be violated incrementally
   - Current state: Policy exists, no enforcement mechanism
   - Action: Define what counts as a core export vs. an adapter projection. Document the review gate: "Is this prompt-generation logic? If yes, it belongs in an adapter, not core."
   - Mitigation: If deferred, establish a design review process for new exporters.

6. **Context Profile Compilation Cost**
   - Problem: Re-running extractors for each context is expensive; merge rules are cheaper but require clear semantics
   - Current state: Policy says "should compile" signals but does not specify the algorithm
   - Action: Decide on implementation strategy before Sprint 02 schema design. Cost matters.
   - Mitigation: If deferred, at least define the extraction cost model so Sprint 02 can make an informed choice.

### Minors (Acceptable as Implemented or Deferred)

7. **Terminology Collision** (Resolved in Sprint 01.5)
   - `identity` vs. `expression` vs. `voice` is now clear. `expression_profile` and `context_profiles` are distinct.

8. **Dead Document References**
   - Fixed. MEMORY_DISCIPLINE.md and EVIDENCE_AND_CONFIDENCE.md now exist.

---

## What Sprint 01.5 Got Right

1. **Honest About Tradeoffs**
   - The remediation documents do not pretend to solve unsolvable problems. They name the tradeoffs and push decisions to stakeholders.

2. **Strong Constraints on Interpretation**
   - The claim-level system and interpretation boundaries are clear and defensible.

3. **Rigorous Versioning Framework**
   - Build manifests and drift type labels are well-conceived. Users will understand why profiles changed.

4. **Clear Product Boundary**
   - Imprint is not trying to be a memory system, AI detector, personality classifier, or generation system. The ownership matrix is crisp.

5. **Synthetic-First Commitment**
   - The public-first requirement for all examples and fixtures is maintained. This keeps the project open-source-safe.

---

## What Sprint 01.5 Did Not Do

1. **Make profiles deterministic**
   - Models still produce non-deterministic outputs. Different models produce incomparable results. Booking-keeping ≠ determinism.

2. **Resolve the privacy/auditability tradeoff**
   - The tension still exists. Metadata-only is privacy-safe but audit-weak. Local storage is audit-strong but privacy-risky.

3. **Prevent downstream contamination**
   - The boundary between core and adapters is declared but not enforced. Incremental creep is possible.

4. **Specify how divergences work**
   - The model is philosophically correct (no hidden inheritance) but operationally incomplete.

5. **Build validation enforcement**
   - Safety guardrails (claim levels, evidence requirements) exist in policy but not in code.

---

## Recommendations for Sprint 02

### Must Do

1. **Implement claim-level validation** in the profile compiler. Prohibited claims must not survive to export.
2. **Specify the artifact storage default.** Accept the tradeoff. Document it.
3. **Define profile comparability.** What does it mean for two profile versions to be "comparable"? Same model family? Same extractor version? If re-extracting with a different model, what's the customer-facing story?
4. **Flesh out the divergence model** with concrete schema examples and merge rules.

### Should Do

5. **Build an extraction cost model.** Decide whether to re-run extractors for context profiles or merge master signals with context weights.
6. **Design a schema review gate.** Ensure new fields don't accidentally leak diagnostic claims, prompt material, or memory-system features.
7. **Document the artifact storage impact on the customer experience.** If metadata-only is default, how will users audit their profiles?

### Can Defer

8. Exact encryption mechanism for local artifact stores.
9. Cross-model profile migration strategy (if not planned for MVP).

---

## Go / No-Go Decision

### ✅ GO for Sprint 02

**Conditional:** The architecture is **sound** if the implementation team honors the constraints.

**Mandatory conditions:**
- Claim validation must be enforced (not optional).
- Default artifact storage mode must be specified and documented.
- Profile comparability across model versions must be defined (even if the answer is "not comparable without recompilation").
- Divergence data model must be finalized before schema serialization.

**If these conditions are met,** Sprint 02 can proceed without architectural collapse.

**If these conditions are skipped,** Sprint 02 will re-create the same problems from Sprint 01.

### Why Conditional Go, Not Clean Go?

The remediation successfully **constrained** the problem space without **solving** the core tensions. This is a valid approach — it acknowledges hard tradeoffs and makes them explicit. However, **constraints only work if followed.** 

The next failure point is implementation culture. Will the Sprint 02 team ask themselves "is this a prohibited claim?" before adding a field? Will they resist the temptation to add "helpful" downstream features into core? Will they enforce validation rules even when they seem overly strict?

The documents say yes. The implementation must prove it.

---

## Unresolved Questions for Sprint 02 Kickoff

1. **Profile Stability:** If a user re-extracts their profile using a newer LLM model, under what conditions is the profile still considered "the same person"? Is comparability optional?

2. **Default Privacy Posture:** Metadata-only (audit-weak, privacy-safe) or local storage (audit-strong, privacy-risky)? This decision shapes the entire early-user experience.

3. **Divergence Compilation:** Will context extraction re-run extractors (expensive, fair) or use merge rules (cheap, potentially unfair)? What's the cost model?

4. **Downstream Scope Creep:** Who reviews new exporters to ensure they don't become hidden prompt generators? What's the gate?

5. **Claim Validation Enforcement:** How strictly will the validator reject prohibited claims? Should they fail hard, or warn and quarantine?

These are not blockers for Sprint 02 schema work. But they are dependencies for Sprint 02 implementation. Start those conversations now.

---

## Closing

Sprint 01.5 did the honest work of naming problems instead of hiding them. The remediation documents are guardrails, not guarantees.

Sprint 02 may proceed. But the hard part begins now.

Good luck.
