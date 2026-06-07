# Sprint 04 Architecture Review: Classification Engine Design

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for baseline implementation  
**Context:** Evaluation of Sprint 04 classification design against evidence boundaries and signal extraction readiness

---

## Executive Summary

Sprint 04 has specified a **conservative, rule-based classification engine** that respects adapter independence and maintains evidence boundaries.

The design is architecturally sound. However, it has introduced operational assumptions that will cause problems if not enforced during implementation:

1. **Rule evaluation is deterministic but incomplete.** Known pathological cases (mixed languages, corrupted data, edge timezones) are not addressed.
2. **Confidence scoring lacks guidance.** The spec says "confidence components" but doesn't specify how to compute them.
3. **Quarantine vs. exclusion logic is vague.** When uncertain, should an artifact be quarantined (preserved for review) or excluded (removed from profile)?
4. **Scaling assumptions are untested.** Rule evaluation on 1M artifacts is assumed to be O(n) but might have hidden quadratic paths.

**Verdict: CONDITIONAL GO for Implementation**

The design can be built. But four constraints must be enforced during Sprint 04 coding:

1. Define confidence component scoring explicitly (not just "explainable")
2. Specify quarantine vs. exclusion decision rules
3. Document known pathological cases and how they're handled
4. Establish performance targets for 1M-artifact scaling

If these are locked in, the classifier is production-ready.

---

## Strengths: What Sprint 04 Design Got Right

### 1. Adapter Hints Are Treated as Evidence, Not Truth

**Status: ✅ Excellent**

`CLASSIFICATION_DESIGN.md` states:

> "Adapter-provided metadata is treated as ingestion evidence, not final truth."

And `CLASSIFICATION_RULES.md` reinforces:

> "JSONL-supplied authorship, confidence, inclusion, and artifact-type values remain advisory source hints. They do not automatically become final classification truth."

**Check:** Can an adapter assert high-confidence human authorship and have it auto-included?

No. The rule states: "Uncorroborated human-origin hints degrade to lower-confidence provisional outcomes rather than silently including the artifact."

This is correct and enforces the Sprint 03.5 boundary.

### 2. Deterministic Local Classification

**Status: ✅ Good**

The design specifies:

> "The baseline classifier is deterministic and local-first. It uses rule evaluation over opaque source identifiers, safe metadata hints, and source-shape signals derived during normalization."

This is:
- ✅ Deterministic (reproducible across runs)
- ✅ Local (no API calls or LLM)
- ✅ Rule-based (explainable)
- ✅ Evidence-driven (metadata + source signals)

No surprises, no provider lock-in.

### 3. Clear Scope Boundaries

**Status: ✅ Excellent**

The design explicitly declares what it does NOT do:

- ❌ Extract signals
- ❌ Compile profiles
- ❌ Infer personality, intent, or diagnosis
- ❌ Use provider APIs, LLMs, or embeddings

This is correct. Classification is a precursor to extraction, not extraction itself.

### 4. Explainability as a First-Class Requirement

**Status: ✅ Good**

Every classification result includes:

- artifact ID
- opaque source ID
- source type
- source hints considered
- rule IDs applied
- limitations
- evidence summary
- likelihoods (quote/forward, template/notification, assistant output, contamination)

This allows downstream systems and users to understand why an artifact was classified as it was.

### 5. Conservative Defaults for Uncertainty

**Status: ✅ Good**

Examples from rules:
- "Missing transcript speaker metadata classifies to `unknown_speaker` and quarantines."
- "Quote or forward markers raise quote/forward likelihood and quarantine the artifact."
- "Uncorroborated human-origin hints degrade to lower-confidence provisional outcomes."

When uncertain, the system does not assume. It quarantines or downgrades confidence.

---

## Unresolved Design Questions (Must Be Answered During Implementation)

### 1. Confidence Component Scoring Is Undefined

**Status: ⚠️ Critical Specification Gap**

The design says classification produces "explicit evidence with rule IDs, considered hints, confidence, and contamination/quote/template likelihoods."

But how are these likelihoods computed?

**Example:** An artifact has a forward marker. The rule says "raise quote/forward likelihood." To what value? 0.8? 0.9? And the other likelihoods (template/notification, assistant_output)—are they 0.1 each?

**The problem:** If confidence scoring is not precisely defined, different implementations will diverge and profiles will be inconsistent.

**Recommendation:** Define a confidence model for Sprint 04 implementation:

```
forward_likelihood = has_forward_marker ? 0.85 : 0.1
template_likelihood = has_template_marker ? 0.9 : 0.05
assistant_likelihood = has_assistant_marker ? 0.9 : 0.05
contamination_likelihood = max(forward, template, assistant)

confidence = {
    attribution: 0.95,  # opaque_source_id is stable
    authorship_origin: (1 - contamination_likelihood),
    extraction: 0.5,  # rule-based is less reliable than LLM
    evidence_strength: (if_corroborated ? 0.8 : 0.4),
    source_diversity: (source_type_count / total_types),
    policy_fit: 1.0,
    display: mean([authorship_origin, extraction, evidence_strength])
}
```

Without this, "confidence" is meaningless.

### 2. Quarantine vs. Exclusion Decision Logic Is Vague

**Status: ⚠️ Specification Ambiguity**

The rules say:
- "Quote markers...quarantine"
- "Template markers...exclude"
- "Assistant markers...exclude"

But what's the difference? And when is quarantine used vs. exclusion?

**The problem:** If an artifact is excluded, it disappears from the profile entirely. If it's quarantined, it's preserved for review. These are very different outcomes.

**Questions that need answers:**

1. Is quarantine temporary (user reviews, then accepts/rejects) or permanent (quarantined artifacts never become signals)?
2. When should an artifact be quarantined vs. excluded?
   - Quote: quarantine (user might want to keep their own analysis) or exclude (it's not their words)?
   - Template: exclude (not valuable) or quarantine (might be useful for context)?
   - Assistant: exclude (not human-origin) or quarantine (might be evidence of their process)?
3. If quarantined, do they contribute to profile evidence at all?

**Recommendation:** Define a decision tree:

```
if template_or_notification:
    action = EXCLUDE  # Not human-original, not valuable for profile
elif assistant_output:
    action = EXCLUDE  # Not human-original, could indicate AI feedback loop
elif quote_or_forward:
    action = QUARANTINE  # Preserve but don't include; user might explain why they shared it
elif unknown_speaker:
    action = QUARANTINE  # Preserve for review; uncertain about who wrote it
elif contamination_likelihood > 0.7:
    action = QUARANTINE  # Preserve but flag high contamination risk
else:
    action = INCLUDE  # Low contamination, presumed human-origin
```

### 3. Pathological Cases Are Not Addressed

**Status: ⚠️ Known Unknowns**

The design covers common cases (transcripts, templates, assistant markers) but what about:

1. **Mixed language artifacts:** An email with English + Spanish + machine translation. How is speaker origin classified?
2. **Corrupted encoding:** A file with mojibake or encoding errors. Does rule evaluation break?
3. **Timestamps from the future or distant past:** A file dated year 2300 or 1800. How does this affect time-window logic?
4. **Massive artifacts (10MB+ text):** Does rule evaluation scale linearly or blow up on memory?
5. **Synthetic or generated content:** An artifact that's a dump of a language model's parameters. Not human-origin, not assistant-generated.

**Recommendation:** Document known pathological cases and how they're handled:

```
PATHOLOGICAL_CASES = [
    ("mixed_language", "Email with multiple languages", "Quarantine with mixed_language flag"),
    ("encoding_corruption", "Mojibake or encoding errors", "Exclude with encoding_error flag"),
    ("future_timestamp", "File dated > 2 years in future", "Exclude with timestamp_invalid flag"),
    ("massive_artifact", "> 10MB text", "Process but flag size; split if needed"),
    ("synthetic_content", "Parameter dumps or generated data", "Exclude with synthetic_flag"),
]
```

### 4. Scaling Assumptions Are Untested

**Status: ⚠️ Performance Assumption**

The design assumes "deterministic rule evaluation" scales linearly (O(n) with n artifacts).

But are there hidden quadratic loops?

**Examples:**
- Does comparing an artifact to all previous artifacts to detect duplicates become O(n²)?
- Does computing source diversity across all sources become O(n * num_sources)?
- Does storing rule-evaluation results for explainability grow unbounded in memory?

**Recommendation:** Establish performance targets and test before scale-up:

```
Performance targets:
- Classify 1M artifacts in < 1 hour (< 1ms per artifact)
- Memory footprint < 2GB for classification state
- No quadratic loops in rule evaluation
- Explainability output < 1KB per artifact
```

### 5. Rule Completeness Is Unknown

**Status: ⚠️ Unknown Coverage**

The rules cover:
- ✅ Transcripts (speaker metadata)
- ✅ Templates and notifications
- ✅ Assistant output
- ✅ Quotes and forwards
- ✅ Unknown speaker

But what about:
- Email BCC/CC fields (forwarding without explicit markers)?
- Slack replies vs. threads (implicit conversation context)?
- Translated content (how to detect and classify)?
- Headers and metadata from email/calendar that aren't content?
- Auto-generated logs and system messages?

**Recommendation:** Build a rule inventory and explicitly document what's covered and what's deferred:

```
RULE_INVENTORY = {
    "Covered in Sprint 04": [
        "explicit_speaker_label",
        "template_notification_marker",
        "assistant_output_marker",
        "quote_forward_marker",
    ],
    "Deferred to Sprint 05+": [
        "implicit_cc_forwarding",
        "thread_context_detection",
        "translation_detection",
        "auto_generated_content",
        "system_logs",
    ]
}
```

---

## Critical Path Items for Sprint 04 Implementation

### 1. Lock Down Confidence Scoring Model

**Action:** Before implementing the classifier, specify:
- How each confidence component is computed
- What values they take (0.0-1.0?)
- How display confidence is derived
- How unknown authorship reduces confidence

### 2. Define Quarantine vs. Exclusion Decision Tree

**Action:** Specify when each action is taken and document the logic clearly.

### 3. Document Pathological Cases

**Action:** For each known edge case (mixed language, encoding corruption, etc.), document how it's handled.

### 4. Establish Scaling Performance Targets

**Action:** Set explicit targets (1M artifacts in <1 hour, <2GB memory) and plan test strategy.

### 5. Build Rule Inventory

**Action:** Document what's covered in Sprint 04 and what's deferred.

---

## Long-Term Stability Assessment

### Five-Year Outlook

The classification design will hold **if**:

1. **Rule set remains curated.** If rules proliferate (every user can add custom rules), the system becomes unpredictable. Keep rules minimal and vetted.

2. **Confidence scoring stays stable.** If Sprint 05 changes how confidence is computed, all Sprint 04 profiles become incomparable. Version the scoring model.

3. **Pathological cases don't multiply.** If every edge case requires a new rule, the system becomes unmaintainable. Handle edge cases at the boundary (reject/quarantine) rather than with more rules.

4. **Performance scales linearly.** If rule evaluation becomes quadratic at 10M artifacts, the system fails at scale. Monitor performance early.

---

## Findings by Severity

### Blockers (None)

The design is architecturally sound and can be implemented.

### Majors (Must Specify Before Implementation Begins)

1. **Confidence Component Scoring Model**
   - Design explicitly specifies "confidence" but not how to compute it
   - Implementation will make ad-hoc decisions if this isn't locked down
   - Impacts profile comparability and downstream weighting

2. **Quarantine vs. Exclusion Decision Logic**
   - Rules mention both but don't specify when to use each
   - Different implementations will diverge
   - Impacts what gets preserved vs. discarded

3. **Scaling Performance Targets**
   - No targets specified for 1M artifacts
   - Unknown if rule evaluation is actually O(n) or has hidden quadratic loops
   - Blocks production deployment decisions

### Minors (Acceptable to Defer or Document in Code)

4. **Pathological Case Inventory**
   - Known edge cases (mixed language, encoding corruption) are not documented
   - Acceptable: can be added during Sprint 04 implementation as discovered

5. **Rule Completeness Inventory**
   - Not clear what's covered vs. deferred
   - Acceptable: document in code comments what's implemented and what's future work

---

## Go / No-Go Decision

### ✅ CONDITIONAL GO for Sprint 04 Implementation

**Verdict:** The classification design is ready for implementation, PROVIDED that the major specification gaps are closed first.

**Mandatory before Sprint 04 coding begins:**

1. **Define confidence component scoring model** — exact formulas, not "explainable"
2. **Define quarantine vs. exclusion decision logic** — explicit tree, not suggestions
3. **Establish performance scaling targets** — 1M artifacts in <1 hour, <2GB memory
4. **Document rule completeness** — what's in Sprint 04, what's future work

**If these are locked in,** Sprint 04 implementation can proceed with confidence that classifier behavior will be predictable and consistent.

---

## Closing

Sprint 04 design is philosophically sound: conservative, rule-based, evidence-driven, explainable. The implementation challenges are operational, not architectural.

The gaps aren't blockers—they're specification work that needs to happen before coding. Lock them down, and the classifier is production-ready.

---

## Appendix: Sprint 04 Implementation Checklist

Before shipping Sprint 04 classifier, verify:

- [ ] Confidence component scoring model defined and implemented?
- [ ] Quarantine vs. exclusion decision logic explicit and tested?
- [ ] Performance targets met (1M artifacts in <1 hour)?
- [ ] Pathological cases documented and handled?
- [ ] Rule set curated and minimal?
- [ ] Explainability output < 1KB per artifact?
- [ ] Tests prove adapter hints don't bypass logic?
- [ ] No diagnostic or personality claims in rules?
- [ ] Classification boundary preserved (no signal extraction)?

Use this checklist when reviewing Sprint 04 implementation.
