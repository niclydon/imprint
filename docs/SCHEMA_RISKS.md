# Sprint 02 Schema Review: Risks and Recommendations

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for Sprint 03  
**Context:** Evaluation of Sprint 02 schema design and Pydantic implementation against Sprint 01.5 constraints and five-year stability requirements

---

## Executive Summary

Sprint 02 delivered comprehensive schema design and a Pydantic implementation that **successfully encodes** most Sprint 01.5 architectural constraints.

The work is architecturally sound and production-ready for the MVP. However, it has introduced new risks:

1. **Extracter family taxonomy is incomplete.** The schema defines `ExtractorFamily` enum but `SEMANTIC_LLM` and `HYBRID_REVIEW` are vague. This will cause comparability classification to fail in edge cases.

2. **Model provider fields are platform-neutral but incomplete.** Build manifest records provider/name/version but lacks capability contracts. Downstream systems cannot automatically choose safe models.

3. **Context compilation strategy is hard-coded but untested.** The schema assumes `filtered_evidence_recompile` works at scale. No cost analysis or budget enforcement beyond count limits.

4. **Export forbidding is syntactic only.** The validator rejects fields in projection_metadata, but a downstream adapter could fork and add the fields anyway. The boundary is legible, not enforceable.

5. **Profile stability definition is vague on cross-model regeneration.** "Not comparable unless explicitly migrated" is correct, but migration policies are not specified. How are migrations invented and approved?

6. **AI detector handling prevents ground truth but allows weak evidence.** The validator `ai_detector_is_ground_truth: Literal[False]` works, but a weak detector score could still be weighted higher than other weak evidence without explicit policy.

7. **Long-term extensibility is constrained.** The schema uses `extra="forbid"`, which prevents forward-compatible field addition. If Sprint 03 needs new fields, every profile object requires schema migration.

**Verdict: CONDITIONAL GO for Sprint 03**

The schemas can ship for MVP. But three critical paths must be resolved before production:

1. **Define extractor family taxonomy and comparability decision tree operationally.**
2. **Design model capability contracts and provider abstraction for Sprint 02.5.**
3. **Publish evidence weighting rules to prevent AI detectors from becoming de facto ground truth.**

If these are skipped, the project will ship profiles that appear comparable when they are not, and downstream systems will make unsafe model choices.

---

## Strengths: What Sprint 02 Got Right

### 1. Artifact Storage Policy Constraints Are Enforced

**Status: ✅ Excellent**

The `ArtifactStoragePolicy` validator is tight:

```python
@model_validator(mode="after")
def metadata_only_discloses_limits(self) -> ArtifactStoragePolicy:
    if self.mode == ArtifactStorageMode.METADATA_ONLY:
        if self.raw_content_available:
            raise ValueError("metadata_only storage cannot declare raw_content_available=true")
        required = {
            AuditLimitation.RAW_CONTENT_UNAVAILABLE,
            AuditLimitation.REGENERATION_REQUIRES_REHARVEST,
        }
        if not required.issubset(set(self.audit_limitations)):
            raise ValueError("metadata_only storage must disclose...")
        return self
```

This enforces the Sprint 01.5 decision: metadata-only mode cannot pretend to offer full audit. Honest and unspoofable.

### 2. Claim Validation Is Mandatory and Structural

**Status: ✅ Excellent**

`Claim` has a model validator:

```python
if self.level == ClaimLevel.PROHIBITED and self.validation.status != ClaimValidationStatus.FAILED:
    raise ValueError("prohibited claims must have failed validation")
```

And `ExpressionProfile` checks for prohibited claims:

```python
prohibited = [claim.claim_id for claim in self.claims if claim.level == ClaimLevel.PROHIBITED]
if prohibited:
    raise ValueError(f"compiled expression profile contains prohibited claims: {prohibited}")
```

This means a prohibited claim **cannot exist in a compiled profile.** It's structural, not advisory. Excellent.

### 3. AI Detector Output Cannot Be Ground Truth

**Status: ✅ Good with caveats**

`ArtifactClassification` has:

```python
ai_detector_is_ground_truth: Literal[False] = False
```

And a validator:

```python
if self.ai_detector_score is not None and self.authorship_origin == AuthorshipOrigin.HUMAN_ORIGIN:
    if self.authorship_confidence < 0.5:
        raise ValueError("AI detector output alone cannot establish human authorship")
```

This prevents a detector output alone from creating authorship. Good guardrail.

**However:** The validator only checks one case (detector high, confidence low). A future implementation could use a detector score to weight evidence without violating this rule. The spirit is enforced, not the letter.

### 4. Context Profile Budget Is Explicit

**Status: ✅ Good**

`SourcePolicy` has:

```python
max_context_profiles: int = Field(default=5, ge=0)
allow_context_budget_override: bool = False
```

And `ExpressionProfile` validates:

```python
if len(self.context_profiles) > self.source_policy.max_context_profiles:
    if not self.source_policy.allow_context_budget_override:
        raise ValueError("context profile count exceeds source policy budget")
```

The MVP default of 5 contexts is explicit. Overrides require opt-in. Good.

### 5. Comparability Is Computed Automatically

**Status: ✅ Excellent**

`ComparabilityResult.from_manifests()` takes two `BuildManifest` objects and returns:
- label: `comparable`, `partially_comparable`, or `not_comparable`
- reasons: structured enum list
- explanation: human-readable text

The logic is systematic and auditable. Cross-model extraction is marked `NOT_COMPARABLE` without migration. Excellent.

### 6. Divergences Are Explicit and Structured

**Status: ✅ Good**

`DerivedProfileDivergence` has:
- signal_family, pattern, baseline_value, context_value, direction
- claim_level, collision_label
- support metadata

And a validator prevents prohibited claims in divergences. No hidden inheritance.

### 7. Export Projections Cannot Become Prompts

**Status: ✅ Good with limits**

`ProfileExport` has:

```python
FORBIDDEN_EXPORT_FIELDS = {
    "prompt", "system_prompt", "instruction", "temperature", "decoding", "model_hint", ...
}

@model_validator(mode="after")
def public_exports_fail_closed(self) -> ProfileExport:
    forbidden = set(self.projection_metadata).intersection(FORBIDDEN_EXPORT_FIELDS)
    if forbidden:
        raise ValueError(f"core exports cannot include generation-control fields: {sorted(forbidden)}")
```

The forbidden list is explicit and enforced syntactically. Good.

---

## Unresolved Risks (Not Blockers, But Require Documentation)

### 1. Extractor Family Taxonomy Is Vague

**Status: ⚠️ Incomplete**

The schema defines:

```python
class ExtractorFamily(StrEnum):
    RULE_BASELINE = "rule_baseline"
    SEMANTIC_LLM = "semantic_llm"
    HYBRID_REVIEW = "hybrid_review"
```

These are names, not operational definitions.

**Problems:**

1. **SEMANTIC_LLM covers all LLMs.** Claude, GPT, Llama, open-source, hosted, local — all are `semantic_llm`. But comparability rules treat `semantic_llm` from Llama as NOT_COMPARABLE to `semantic_llm` from Claude, thanks to `model_provider` check. So extractor family alone isn't the comparability boundary.

2. **HYBRID_REVIEW is undefined.** Is it humans + LLMs? Majority-vote across models? If a future Sprint 02.5 defines actual hybrid extraction, how does the family name disambiguate? There's no versioning within families.

3. **Comparability logic depends on model_provider too:**
   ```python
   if baseline.model_provider != candidate.model_provider:
       return cls(label=ComparabilityLabel.NOT_COMPARABLE, ...)
   ```
   So truly, the comparability is on (extractor_family, model_provider, model_name). The family alone is insufficient. This is correct but means extractor family is a misnomer — it's really a classification tool, not a comparability boundary.

**Implication:** The comparability logic is sound, but documentation must clarify that extractor family is not the same as comparability family. Two `semantic_llm` extractors using different models are `NOT_COMPARABLE` even though their families match.

**Recommendation:** Rename or clarify: extractor_family is an implementation classification, not a stability guarantee. Comparability is determined by (family, model_provider, model_name).

### 2. Model Provider Fields Enable Sprint 02.5 But Don't Lock In

**Status: ⚠️ Ready for Sprint 02.5**

The schema records model info:

```python
model_provider: str | None = None
model_name: str | None = None
model_version: str | None = None
```

But there's no:
- Capability contract (what can this model do?)
- Provider kind taxonomy (openai vs anthropic vs ollama)
- Local vs remote flag
- Retention/training policy

**Implication:** Sprint 02.5 must add these. But the schema is not locked in — the None defaults allow forward compatibility.

### 3. Context Compilation Cost Is Not Budgeted

**Status: ⚠️ Deferred**

The schema says `compilation_strategy: Literal["filtered_evidence_recompile"]`, meaning context profiles recompile from filtered evidence.

**Cost analysis:**
- If master profile extracts 1000 artifacts at cost C, a context that uses 200 artifacts costs ~0.2C.
- With 5 contexts, total cost is ~1 + 0.2*5 = 2C (master + contexts).
- But if a user has 20 source types and creates 20 contexts, cost is ~1 + 0.05*20 = 2C (cheap).
- If a user creates context for every (source_type, time_period, author) combination, cost explodes.

The schema doesn't prevent this. It only checks count.

**Recommendation:** Document the cost model clearly and flag overages. Consider: should context budget also account for diversity (number of distinct source-type/time-period/author combinations)?

### 4. Evidence Weighting Rules Are Not Specified

**Status: ⚠️ Deferred to Runtime**

The schema records evidence:

```python
authorship_origin: AuthorshipOrigin
authorship_confidence: float = Field(ge=0, le=1)
ai_detector_score: float | None = Field(default=None, ge=0, le=1)
```

But the schema doesn't specify how these are combined or weighted.

**Example:** If authorship_origin is `SUSPECTED_AI_ASSISTED` with confidence 0.3 and ai_detector_score is 0.75, what is the final authorship for evidence weighting? The schema allows both fields but doesn't specify precedence or combination.

**Recommendation:** Document evidence weighting rules before Sprint 03 extraction code writes signals. Otherwise, extractors will make ad-hoc decisions and profiles will be inconsistent.

### 5. Migration Policy Is Declared But Not Defined

**Status: ⚠️ Architectural Gap**

`MIGRATION_STRATEGY.md` lists migration types but doesn't specify:
- Who approves a migration (reviewer process)?
- How is a migration ID assigned?
- What does "explicit migration" mean operationally?
- How does downstream code learn a migration was approved?

**Implication:** If a user rebuilds with a different LLM model, comparability is `NOT_COMPARABLE`. Good. But if they later want to compare across the model change, how do they invoke an explicit migration? Is there a migration registry? An approval flow?

**Recommendation:** Design the migration approval and registry process before Sprint 03 starts. Otherwise, users will have no way to declare cross-model comparisons.

### 6. Extended Enum Design May Cause Brittleness

**Status: ⚠️ Long-term Risk**

The schema uses many enums:

```python
class AuthorshipOrigin(StrEnum):
    UNKNOWN_SPEAKER = "unknown_speaker"
    QUOTED_OR_FORWARDED = "quoted_or_forwarded"
    ...
```

With `extra="forbid"` on the base model, adding a new `AuthorshipOrigin` value is a breaking change. An old extractor writing a profile with a new authorship origin value that a newer reader doesn't understand will fail validation.

**Mitigation:** The enums are strings, not integers, so serialization is safe. A system with an old enum can still read profiles with new enum values (they become strings). But validation at deserialization will fail.

**Recommendation:** Consider relaxing `extra="forbid"` for some models, or document a forward-compatibility strategy (e.g., unknown enum values coerce to a fallback category).

### 7. No Profile Versioning For User-Facing Regeneration

**Status: ⚠️ Missing Workflow**

The schema says profiles are identified by `profile_id` and includes `build_manifest` with versions. But there's no field for "v0.1 of this profile" vs "v0.2 of this profile from the same rebuild."

If a user regenerates their profile twice, both profiles have the same `profile_id` but different manifests. How do downstream systems distinguish them?

**Recommendation:** Either add a profile_version field or clarify that profile_id is scoped to the latest version only (older versions are archived, not referenced).

---

## Critical Path Items for Sprint 03

### 1. Publish Extractor Family Taxonomy

**Action:** Create a document that lists:
- `rule_baseline`: concrete extraction rules (e.g., paragraph length, token counts)
- `semantic_llm`: semantic extraction using LLM (includes provider and model)
- `hybrid_review`: human-reviewed hybrid extraction (includes review metadata)

And clarify that extractor family is not the comparability boundary — (family, model_provider, model_name) together are.

### 2. Design Evidence Weighting Rules

**Action:** Before Sprint 03 extraction code writes its first signal, document how to combine:
- authorship_origin
- authorship_confidence
- ai_detector_score
- policy weights

Example: If authorship_origin is `SUSPECTED_AI_ASSISTED`, reduce confidence by 0.2 and set policy action to `DOWNWEIGHT`. If ai_detector_score is high and authorship_origin is `HUMAN_ORIGIN`, flag for review rather than auto-accepting.

### 3. Design Migration Approval Process

**Action:** Define:
- Who approves migrations?
- Is there a migration registry or approval flow?
- How does downstream code learn that a migration was approved?
- Can users declare their own migrations or only approved ones?

### 4. Model Capability Contracts (Sprint 02.5)

**Action:** Define the set of capabilities required for each model role:
- classifier needs: structured output, confidence scoring
- extractor needs: low temperature, reproducible output, artifact citation
- validator needs: yes/no decision capability, rule-based logic
- reporter needs: prose generation, markdown, citation

Downstream code will use this to select models. Specification must be concrete enough to test.

---

## Long-Term Stability Assessment

### Five-Year Risk

The schema will survive five years **if**:

1. **Enum additions are infrequent.** The schema uses `extra="forbid"` which makes enum extension a breaking change. If Signal families, artifact types, or authorship origins must expand often, the schema becomes brittle.

2. **Model roles remain stable.** The build manifest assumes roles are (classifier, extractor, validator, reporter). If Sprint 03+ adds new roles, the manifest schema needs new fields.

3. **Export semantics don't drift.** The forbidden fields list prevents prompt generation, but if downstream systems accumulate enough projection_metadata to become de facto prompts, the boundary erodes.

4. **Migration policy gets explicit.** Currently, migration is philosophically correct but operationally vague. Without a concrete approval/registry process, users will create ad-hoc migrations and the profile ecosystem fragments.

5. **Evidence weighting stabilizes.** The confidence components are well-designed, but the combination rules must be stable. If every sprint changes how components combine, profile drift becomes meaningless.

### Migration Hazards

1. **Adding a new SignalFamily requires all profiles to be invalid until re-compiled.** The Signal model includes `family: SignalFamily`, so a new family is a breaking change.

2. **Renaming an enum value looks like a breaking change but might be safe if backward-compatible coercion exists.** (E.g., rename `SUSPECTED_AI_ASSISTED` → `AI_ASSISTED_SUSPECTED`.) The serialized string changes, but deserialization can coerce.

3. **Adding a required field to Claim breaks existing profiles.** Currently, all Claim fields have defaults or are optional. Good. But future fields might not.

### Recommendation

The schema will serve the MVP and likely the first three sprints. But **by Sprint 05, plan a major schema revision.** When you have real production profiles, you'll understand the edge cases and can design a more flexible schema.

Until then:
- Document forward-compatibility assumptions clearly
- Design migrations conservatively (prefer additive changes)
- Establish a breaking-change review gate before schema changes are merged

---

## Findings by Severity

### Blockers (None)

The Sprint 02 schema is architecturally sound and can ship for MVP.

### Majors (Must Clarify Before Sprint 03)

1. **Extractor family is vague.** Document the taxonomy and clarify that (family, model_provider, model_name) together define comparability.
2. **Evidence weighting rules are unspecified.** Document how to combine authorship_origin, confidence, detector_score, and policy weights.
3. **Migration process is philosophically correct but operationally vague.** Design an approval/registry flow.

### Minors (Address But Not Critical)

4. **Context compilation cost is not budgeted.** Document the cost model and consider tracking diversity.
5. **Model capability contracts are missing.** Sprint 02.5 will add these, but document what they must include.
6. **Profile versioning workflow is unclear.** Clarify if profile_id is scoped to latest version or has sub-versions.
7. **Enum brittleness for long-term stability.** Document forward-compatibility strategy or plan major revision by Sprint 05.

---

## Go / No-Go Decision

### ✅ GO for Sprint 03

**Verdict:** The Sprint 02 schema design and implementation are production-ready for the MVP.

**Mandatory before Sprint 03 extraction code ships:**

1. **Publish extractor family taxonomy.** Clear definition of what rule_baseline, semantic_llm, and hybrid_review mean operationally.
2. **Publish evidence weighting rules.** How to combine authorship_origin, confidence, detector_score, and policy weights in signal compilation.
3. **Design migration approval process.** How users declare cross-model migrations and how the system records approval.

**If these are skipped,** Sprint 03 extraction code will make ad-hoc decisions and profiles will be inconsistent.

---

## Closing

Sprint 02 did the hard work: they encoded the entire Sprint 01.5 architecture into Pydantic. The constraints are now structural, not advisory.

What remains is operational. The schema is a language; Sprint 03 must define the vocabulary precisely (what are extractors, what weights evidence, how migrations work).

That work is non-trivial. Do it well, and the project will have durable profiles. Skip it, and profiles will appear stable while being incomparable.

---

## Appendix: Schema Validation Coverage

### Enforced at Build Time ✅

- Artifact storage mode and audit limitations must match
- Prohibited claims cannot compile
- AI detector output cannot become ground truth alone
- Context profiles cannot exceed budget (without override)
- Export projections cannot include generation-control fields
- Drift reports cannot claim expression drift on not_comparable profiles
- Divergences cannot include prohibited claims

### Not Enforced (Deferred to Runtime/Policy) ⚠️

- Evidence weighting rules (combination of authorship_origin, confidence, detector_score)
- Migration approval and registry
- Extractor family taxonomy and operationalization
- Context compilation cost budgeting
- Model capability contracts
- Profile versioning workflow
- Forward-compatibility enum coercion

### Architectural Decisions Encoded ✅

- Metadata-only default with explicit audit limitations
- Explicit authorship-origin categories (9 types)
- Build manifest with all component versions
- Automated comparability from structured fields
- Three-state comparability labels (comparable, partially, not_comparable)
- Context profiles as explicit compiled views
- Core exports forbidden from generation control fields
