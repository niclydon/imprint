# Sprint 01.5 Architecture Review

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for Sprint 02  
**Context:** Evaluation of Sprint 01.5 remediation work against adversarial findings from Sprint 01

---

## Executive Summary

Sprint 01.5 converted adversarial refusals into **specific architectural decisions** with concrete defaults, data shapes, and enforcement gates.

The remediation is **significantly stronger** than the initial adversarial review suggested. But it has introduced new risks:

1. The MVP default (`metadata_only` storage) sacrifices auditability for privacy — a real tradeoff with downstream consequences.
2. Context profile recompilation is specified but expensive — scale limits are not enforced or documented.
3. Comparability rules are explicit but rely on human judgment at runtime.
4. Claim validation is mandatory but the validation code does not yet exist.
5. Export review gates are well-designed but still vulnerable to incremental scope creep.

**Verdict: CONDITIONAL GO for Sprint 02**

The architecture is defensible if the implementation team commits to: (1) the metadata-only default and its audit limitations, (2) explicit context complexity budgets, (3) automated comparability checking, and (4) enforced validation at build time.

If any of these are skipped, the project will collapse into worse versions of the Sprint 01 problems.

---

## Resolved Issues (Actual Decisions Made)

### 1. Artifact Storage Default — Now Specified

**Status: ✅ Decided**

The MVP default is explicitly `metadata_only`. This is a **deliberate privacy-first tradeoff.**

What this means:
- Raw artifact text is NOT stored by default
- Profiles include support metadata, hashes, classifications, evidence references
- Full local regeneration is NOT guaranteed if original source disappears
- Audit is weak — users see artifact IDs and counts, but not the actual text

**Why this matters:**
The adversarial review said "the privacy/auditability tradeoff remains unresolved." Sprint 01.5 did resolve it — by choosing privacy over auditability for the MVP.

**However: This decision has downstream consequences:**

1. **Audit complaints will come.** A user will ask "why did you extract this signal?" and Imprint will say "34 artifacts in the 'chat_message' category from 2025-01 to 2025-03 contributed." That's not auditability; that's opacity with structure. This is acceptable, but the user experience team must know it.

2. **Regeneration requires re-harvesting.** If a user wants to rebuild their profile using a newer extractor, and their original data source is gone or changed, the profile cannot be regenerated from local storage. They must have live connector access. This is a constraint worth documenting.

3. **Private-local workflows are tier-2.** The `local_artifact_store` mode exists for users who want stronger audit, but it's not the default. This is a deliberate decision to protect privacy by default.

**Verdict on this decision:** It is honest, explicit, and defensible. It is not a flaw — it is a choice with known tradeoffs.

---

### 2. Divergence Model — Now Concrete

**Status: ✅ Designed (but cost unknown)**

DERIVED_PROFILE_MODEL.md specifies a concrete divergence shape:

```json
{
  "divergence": {
    "signal_family": "structure",
    "pattern": "shorter_paragraph_units",
    "baseline_value": {...},
    "context_value": {...},
    "direction": "context_is_more_direct",
    "claim_level": "observation",
    "support": {...}
  }
}
```

This is **massively better** than the empty `divergences: []` from the adversarial review.

**What this fixes:**
- No more hidden inheritance — divergences are explicit objects
- Downstream systems can parse divergences programmatically
- Collisions are preserved with labels (`context_specific`, `baseline_weak`, etc.)
- Evidence support is attached to every divergence

**However: Hidden costs remain:**

1. **Recompilation cost is not budgeted.**
   - DERIVED_PROFILE_MODEL.md says: "MVP context profiles should recompile signals from filtered evidence rather than merge master signals. This is more expensive but avoids hidden inheritance."
   - Translation: For each context profile, re-run extractors over filtered artifacts.
   - If the master profile uses 1000 artifacts and you have 5 contexts (casual, technical, published, email, podcast), you're potentially extracting 5000+ artifact units.
   - Cost scales linearly with contexts. The doc says "The MVP should keep the number of context profiles small and explicit." But what is "small"? 3? 5? 10? No guidance.
   - Sprint 02 must enforce a context budget or accept extraction costs that scale poorly.

2. **Comparability across divergences is unmapped.**
   - Can you compare divergences across extractor versions? The extractor versioning policy says cross-model semantic extraction is `not_comparable`. But divergences ARE semantic. So if a user rebuilds with a new model, are divergences invalidated?
   - The docs don't explicitly forbid reporting divergence drift, but the logic suggests they should. Sprint 02 needs to clarify.

3. **The divergence shape is locked in early.**
   - Once profiles with this divergence shape ship, the schema is committed.
   - If Sprint 02 implementation discovers the shape is missing fields (e.g., divergence severity, historical drift, context weight), changing it breaks existing profiles.
   - The shape is good but is it complete? No second-order review before shipping.

**Verdict on this decision:** It is concrete and defensible, but the cost implications are deferred. Sprint 02 must enforce context budgets and clarify divergence comparability.

---

### 3. Comparability Rules — Now Explicit

**Status: ✅ Decided (but enforcement is human-dependent)**

EXTRACTOR_VERSIONING.md specifies an operational comparability table:

| Label | Required Conditions | Allowed Claim |
|-------|-------------------|---------------|
| `comparable` | same schema family, same extractor family/major, same source policy, comparable corpus | expression drift may be reported |
| `partially_comparable` | schema compatible, minor extractor/model changes, changed source mix | report changes with caveats |
| `not_comparable` | different extractor family, different LLM family, incompatible schema, different corpus | compiler/corpus change only |

**What this fixes:**
- No more pretending a profile rebuilt with a different model is the same as the original
- Three-state comparability prevents false expression drift claims
- Downstream systems can see WHY two profiles are incomparable

**However: The judgment is manual and context-dependent:**

1. **"Comparable extractor family" is not defined.**
   - Does Claude 3.5 Sonnet + Sonnet 4.0 count as the same family? Presumably yes.
   - Does Claude 3.5 Sonnet + Llama 3.1 count as the same family? Presumably no.
   - But what about Claude 3.5 Sonnet + Claude 3.5 Haiku? Or Claude + another provider using similar prompts?
   - The spec says "same extractor family and major version" but doesn't enumerate families.
   - Sprint 02 must publish an explicit family taxonomy or the comparability judgments will be inconsistent.

2. **"Comparable source policy version" requires version matching.**
   - If the source policy says "include email and chat but exclude drafts," and in v0.2 it says "include email and chat and drafts," are they comparable?
   - The docs assume version numbers are meaningful but don't specify the versioning scheme.
   - Two profiles with policy v0.1 might have different included sources if the policy was reinterpreted. Comparability will be falsely claimed.

3. **Who decides comparability at runtime?**
   - When a user rebuilds their profile with a new extractor, does Imprint automatically label it `not_comparable`?
   - Or does a human reviewer examine the manifest and decide?
   - If automatic, what's the decision tree? (The docs don't specify.)
   - If human, this doesn't scale to per-user profiles.

**Verdict on this decision:** The logic is sound and the table is well-designed. But the taxonomies and decision automation are incomplete. Sprint 02 must make these operational.

---

### 4. Claim Validation — Now Mandatory

**Status: ✅ Mandated (but implementation missing)**

SCHEMA.md says:

> "Claim validation is mandatory, not advisory. Canonical and public-safe exports must fail if a prohibited claim survives compilation."

This is a **hard gate.** Profiles with prohibited claims cannot ship.

**What this fixes:**
- No accidental diagnostic claims in the profile
- No personality-typing schemas
- No intent attribution
- Validation is enforced at build time, not trust

**However: The validation code does not exist yet.**

1. **What is a "prohibited claim"?**
   - The policy lists examples: diagnosis, intent attribution, personality typing, unsupported identity.
   - But how do you programmatically detect these?
   - Example: A signal named `"high_analytical_thinking"` is probably prohibited, but `"frequently_cites_evidence_before_generalizing"` is probably allowed. How does the validator distinguish?
   - Rule-based validators will have false positives and false negatives.

2. **Who defines the prohibited word list?**
   - If a keyword list is used (e.g., "analytical", "ambitious", "introverted"), maintainers will fight over whether specific words are forbidden.
   - Some interpretations are context-dependent. "High" is allowed in "high confidence" but prohibited in "high neuroticism."
   - The validation rule must be smarter than a word list.

3. **What happens to borderline claims?**
   - A claim labeled `bounded_interpretation` ("cautiously inferred") is allowed if evidence-backed.
   - But "cautious" is subjective. An extractor might claim "likely prefers written communication over spoken" as `bounded_interpretation` with 0.62 confidence. Is that OK?
   - The policy says "confidence-scored" but doesn't specify a minimum. Can a claim with 40% confidence ship as `bounded_interpretation`?

4. **Quarantine vs. rejection.**
   - SCHEMA.md mentions "quarantine" for private-local workflows. This means rejected claims are hidden from users but preserved internally for review.
   - This creates a hidden corpus of rejected claims. If a maintainer later decides those claims are safe, they could be "promoted" without explicit re-review.
   - Is there a promotion process? Who approves it?

**Verdict on this decision:** The mandate is strong and necessary. But the validation framework must be designed before implementation or Sprint 02 will ship profiles with prohibited claims disguised as observations.

---

### 5. Export Review Gate — Now Explicit

**Status: ✅ Designed (but vulnerable to scope creep)**

EXPORT_BOUNDARIES.md specifies:

> "Does this exporter decide how a model should generate text in a specific downstream workflow?"
> 
> If yes, it is an adapter concern, not a core Imprint exporter.

**Allowed core exporter behavior:**
- emit structured profile fields
- emit constraints and anti-patterns
- emit evidence and confidence metadata
- emit target-consumer identifiers

**Disallowed core exporter behavior:**
- assemble system prompts
- tune prompts for a provider or model
- encode editorial workflow steps
- decide sampling or decoding behavior
- generate drafts

**What this fixes:**
- Core Imprint does not become a text generation system
- Prompt assembly is downstream's responsibility
- Boundary is testable and reviewable

**However: The boundary is still vulnerable:**

1. **"Emit constraints" is vague.**
   - A constraint like "tends to open discussions with concrete evidence" is useful downstream.
   - But an adaptive downstream system could compile that into a prompt: "Start your response with concrete evidence from real projects."
   - Is that the exporter's fault or the adapter's? The line is blurry.
   - The policy forbids "assemble system prompts" but allows "emit constraints." The assembly happens in the adapter, so technically Imprint is clean. But the intent is leaked.

2. **"Target-consumer identifiers" could become prompts.**
   - A profile could export `"target_audience": "executive"` and `"depth_level": "high_level_only"`.
   - A downstream adapter trivially converts this: `"Format all responses for an executive audience with high-level summaries only."`
   - Imprint didn't write the prompt, but it provided the data that becomes a prompt.
   - Where is the line? The docs say "excluded from canonical schema semantics" but Imprint still exports the metadata.

3. **No enforcement mechanism.**
   - The review gate ("Does this exporter decide how a model should generate?") is a principle, not code.
   - A future maintainer might add a field like `"recommended_temperature": 0.7` to help downstream adapters.
   - Is that a boundary violation? The policy doesn't say.
   - Without a linter or schema validator that enforces the gate, the boundary erodes incrementally.

**Verdict on this decision:** The gate is well-articulated and the list of disallowed behaviors is clear. But the implementation must add automated checks (e.g., a linter that rejects new fields named `*_prompt`, `*_instruction`, `*_guidance`) or the boundary will be incrementally violated.

---

## Upgraded Issues (Problems Become Clearer)

### 1. Context Profile Recompilation Cost

**Status: Specified but budgeted at zero**

The policy says recompilation "is more expensive but avoids hidden inheritance." It also says "the number of context profiles should be small and explicit."

But there is no explicit budget or limit. A user could request 50 contexts, and the compiler would recompute extractors over the entire corpus for each one.

**Question for Sprint 02:** What is the maximum number of context profiles? Is this enforced? What happens if a user requests more?

### 2. Authorship-Origin Weighting

**Status: Specified but unsure about edge cases**

EVIDENCE_AND_CONFIDENCE.md says unknown authorship "should reduce confidence" and "may trigger quarantine."

But "unknown" can mean many things:
- A message from a Slack thread with replies stripped out (unclear speaker)
- A forwarded email with the original author removed (authorship unclear)
- AI detection returned 0.45 (not AI, but uncertain)
- No metadata available at all

Different types of unknown should probably have different weight reductions. The policy doesn't distinguish.

**Question for Sprint 02:** What is the confidence reduction for each type of unknown? Is this configurable per source?

### 3. Detector Output as "Weak Evidence"

**Status: Disallowed but with loopholes**

EVIDENCE_AND_CONFIDENCE.md forbids treating AI detectors as ground truth. But it allows them as "weak evidence."

Example: A detector says "probably AI-assisted" (85% confidence). This is weak evidence. But weak evidence from a high-confidence detector might be weighted higher than weak evidence from a parsing heuristic.

**Question for Sprint 02:** How are multiple weak evidence sources ranked and weighted? What's the precedence?

---

## Unresolved Tensions (Acknowledged But Not Closed)

### 1. Privacy vs. Auditability — Now an Intentional Tradeoff

The metadata-only default sacrifices auditability. Users cannot fully audit a profile without access to source text.

**Is this acceptable for the MVP?** 

The remediation says yes: privacy is more important. But this is a value judgment, not a technical resolution. Future versions might flip it.

**Implication:** Early adopters using metadata-only will not be able to migrate to local_artifact_store without re-harvesting sources. Plan for that.

### 2. Determinism vs. Semantic Extraction

LLM-based extraction is non-deterministic. Rebuilt profiles with different models will differ. The policy says to document this and label comparability.

**But:** Downstream systems might still treat a rebuilt profile as a refresh and ignore the incomparability warning.

**Implication:** The profile versioning and comparability system must be robust enough that downstream systems cannot accidentally merge incomparable profiles.

### 3. Context Explosion

Context profiles recompile from filtered evidence, which is expensive. But users want many contexts (casual, technical, published, email, podcast, executive, teaching, parenting, etc.).

**Cost vs. usability tradeoff remains unresolved.**

**Implication:** Sprint 02 must set a hard limit on contexts or accept extraction costs that scale poorly.

---

## New Risks Introduced by Specific Decisions

### 1. Metadata-Only Privacy Model Locks in Early

**Risk:** If metadata-only becomes the public default and attracts users, switching to local_artifact_store later will require re-harvesting or accepting limited audit.

**Mitigation:** Document the limitations clearly in the MVP launch. Let users choose explicitly.

### 2. Divergence Shape Is Locked In

**Risk:** Once profiles with the divergence structure ship, changes require migration. If Sprint 02 discovers the shape is missing fields, it's a breaking change.

**Mitigation:** Have Sprint 02 schema designers review the divergence shape for completeness before implementation.

### 3. Claim Validation Lacks Implementation

**Risk:** If validation code is incomplete or weak, prohibited claims will leak into profiles disguised as observations.

**Mitigation:** Build and test the claim validator before generating the first user profile. Do not ship validation as a promise.

### 4. Export Review Gate Is Human-Enforced

**Risk:** The boundary between core and adapter is a design principle, not code. Future scope creep is likely.

**Mitigation:** Add automated linters that reject exporter fields based on naming conventions or semantic patterns. Make the boundary enforceable, not just aspirational.

---

## Findings by Severity

### Blockers (Must Fix Before Sprint 02 Ends)

**1. Claim Validation Implementation**
- Current state: Mandatory policy, code doesn't exist
- Action: Build and test the claim validator. Publish the prohibited word/pattern list and decision rules.
- Risk: Prohibited claims ship if validation is skipped

**2. Context Budget and Enforcement**
- Current state: "should be small and explicit," no hard limit
- Action: Define max number of contexts. Enforce in schema. Document cost model per context.
- Risk: Users request 100 contexts; system thrashes

**3. Automated Comparability Checking**
- Current state: Table of conditions, human judgment required
- Action: Build decision tree for automatic comparability labeling. Publish extractor family taxonomy.
- Risk: Manual comparability decisions are inconsistent; misleading labels

### Majors (Should Fix Before Sprint 02, Can Defer If Documented)

**4. Divergence Model Completeness Review**
- Current state: Concrete shape provided, not independently verified
- Action: Have schema designers review divergence fields for completeness. Can they represent all planned divergence types?
- Mitigation: If deferred, flag it as a pre-Sprint-02-1 task

**5. Export Linting**
- Current state: Review gate is a principle, no automated check
- Action: Build a linter that rejects exporter fields matching `*_prompt`, `*_instruction`, `*_guidance`, `*_system`, etc.
- Mitigation: If deferred, document that the boundary is human-enforced and track violations

**6. Authorship-Origin Taxonomy and Weighting**
- Current state: "unknown reduces confidence," no weights specified
- Action: Enumerate authorship-origin types and assign confidence reduction per type.
- Mitigation: If deferred, make unknown-handling configurable and observable in profiles

### Minors (Acceptable as Specified)

**7. Terminology and Schema Boundaries** ✅
- The expression_posture / rhetorical_patterns / voice distinction is clear. No changes needed.

**8. Metadata-Only Default** ✅
- Deliberate tradeoff. Acceptable. Document clearly for users.

---

## What Sprint 01.5 Got Right

1. **Made hard choices instead of deferring them**
   - Specified metadata-only as default (not "metadata-only or local, user's choice")
   - Specified divergence structure (not "divergences TBD")
   - Specified comparability table (not "comparability TBD")

2. **Added operational details**
   - Concrete JSON shapes for divergences with field names
   - Explicit support metadata structure
   - Tables for decision trees (comparability, claim levels)

3. **Enforced boundaries in policy**
   - Claim validation is mandatory, not advisory
   - Export review gate has explicit allowed/disallowed behaviors
   - Context recompilation is specified, not hidden

4. **Honest about tradeoffs**
   - Metadata-only sacrifices auditability for privacy — acknowledged
   - Context recompilation is expensive — acknowledged
   - Determinism is limited — acknowledged with mitigation (build manifest)

---

## What Sprint 01.5 Did Not Do

1. **Did not build the claim validator**
   - Validation is mandated but code is missing
   - Without code, this is still a policy promise

2. **Did not publish the extractor family taxonomy**
   - Comparability rules reference "same extractor family" but families are not defined

3. **Did not enforce context budgets**
   - Policy says "small and explicit," no hard limit or cost model

4. **Did not add automated export linting**
   - Review gate is a principle, not enforced

---

## Go / No-Go Decision

### ✅ GO for Sprint 02

**Verdict:** The architecture is sound and significantly improved.

**Mandatory conditions for Sprint 02:**

1. **Implement claim validation before generating any user profile.** Publish the prohibited patterns and decision rules.
2. **Define and enforce a context profile budget.** Document the cost model and set a hard limit.
3. **Build automated comparability labeling.** Publish extractor family taxonomy and implement the decision tree.
4. **Independently review divergence shape for completeness.** Consult schema designers before implementation.
5. **Add export linting.** Use naming conventions or semantic patterns to reject exporter fields that encroach on prompt generation.

**If these conditions are met,** Sprint 02 can proceed with confidence that the architecture is implemented as designed.

**If these conditions are skipped,** Sprint 02 will create new problems:
- Prohibited claims will leak into profiles
- Contexts will proliferate and crash the system
- Profile comparability will be falsely claimed
- Export boundaries will erode
- The next adversarial review will have much harder things to say

---

## Recommendations for Sprint 02

### Critical Path

1. **Build and test claim validation** (before any user profiles)
2. **Publish extractor family taxonomy** (before comparability is used)
3. **Implement context budget enforcement** (before context profiles ship)
4. **Add export linting** (before new exporters are accepted)
5. **Independent divergence review** (before serialization)

### Design Decisions to Make

1. **Authorship-origin weighting:** Enumerate unknown types and assign confidence reductions
2. **Comparability automation:** Define the decision tree and edge cases
3. **Divergence promotion:** Define the process for moving quarantined claims to `bounded_interpretation`
4. **Context limits:** Specify max contexts and cost per context

### Documentation to Update

1. **Claim validator rules:** Publish the decision tree
2. **Extractor family taxonomy:** List families and major versions
3. **Cost model:** Document extraction cost per context
4. **Metadata-only limitations:** Explain to users what they cannot audit

---

## Closing

Sprint 01.5 did the harder work: it made decisions instead of deferring them. The architecture is now specific enough to build and specific enough to fail in concrete ways.

The implementation team must honor these decisions. Skipping enforcement mechanisms or ignoring cost constraints will erode the architecture incrementally.

This is a strong, defensible design. But only if built as specified.

Good luck.
