# Sprint 02.5 Architecture Review: Model Provider and Inference Policy

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for Sprint 03  
**Context:** Evaluation of Sprint 02.5 model provider policy against BYOM/BYOP requirements and privacy/drift integrity

---

## Executive Summary

Sprint 02.5 delivered a **provider-neutral policy layer** that successfully avoids provider lock-in and establishes clear boundaries between profile-affecting and experience-only inference.

The work is philosophically sound and architecturally correct. However, it has introduced enforcement gaps and capability contract vagueness that will cause problems during Sprint 03 implementation.

**Verdict: CONDITIONAL GO for Sprint 03**

The model provider policy can ship. But Sprint 03 must:

1. **Implement capability verification before model selection.** The contracts are defined but validation code is missing.
2. **Enforce the promotion rule operationally.** Experience-only output cannot accidentally become durable.
3. **Implement privacy disclosure before remote inference.** Users must see what data is sent where.

If these are skipped, the project will have beautiful policy documents and profiles locked to whatever provider Sprint 03 hardcodes.

---

## Strengths: What Sprint 02.5 Got Right

### 1. BYOM/BYOP Is Actually Enforced

**Status: ✅ Excellent**

The MODEL_PROVIDER_POLICY.md is unambiguous:

> "Canonical Imprint schemas must not require OpenAI, Anthropic, Gemini, Forge, Ollama, LM Studio, OpenRouter, vLLM, llama.cpp, or any other provider."

And the implementation lives up to it:

- No SDK imports hardcoded in schemas
- No default provider assumption
- No secrets or credentials in canonical fields
- Provider metadata is for reproducibility only, not runtime clients

**Check:** Can you pull out Imprint's schema and use it with a completely different provider? Yes. The schema records what happened (provider_kind=`anthropic`, model_name=`claude-3.5-sonnet`) but doesn't prescribe how to invoke it.

This is **genuinely provider-neutral architecture.** Rare.

### 2. Profile-Affecting vs Experience-Only Is Explicit

**Status: ✅ Excellent**

MODEL_ROLE_TAXONOMY.md clearly separates:

**Profile-affecting:**
- classifier_llm
- signal_extractor_llm
- claim_validator_llm
- evidence_interpreter_llm
- confidence_assessor_llm
- drift_comparator_llm
- embedding_model
- reranker_model

**Experience-only:**
- profile_summarizer_llm
- first_run_artifact_llm
- report_writer_llm

With a **promotion rule:** "Experience-only output can affect durable profiles only through explicit promotion into the evidence pipeline."

This is operationally sound. A summarizer LLM cannot accidentally mutate the profile. Its output must go through classification, validation, and evidence gates.

### 3. Capability Contracts Are Specific

**Status: ✅ Good**

For each role, specific capabilities are declared:

- `classifier_llm`: structured_output, artifact_id_citation_support, low_temperature_operation
- `signal_extractor_llm`: structured_output, json_schema_output, artifact_id_citation_support
- `claim_validator_llm`: structured_output, taxonomy/rule_rationale_support
- `embedding_model`: stable_embedding_dimension, versioned_model_name

This is concrete. A downstream adapter can look at these requirements and decide: "Llama 2 doesn't support artifact_id_citation_support, so it's not suitable for signal extraction."

### 4. Local-First Remains Possible

**Status: ✅ Good**

MODEL_PROVIDER_POLICY.md says:

> "Imprint must remain useful without remote model credentials. A local-only run may use deterministic rules, local models, or synthetic examples."

And MODEL_PRIVACY_BOUNDARIES.md clarifies:

> "Remote use is optional and never required for public demos or default local mode."

This is correct. Imprint can run locally with rule-based classification and synthetic extraction. Remote providers are add-ons, not requirements.

### 5. Privacy Boundaries Are Explicit

**Status: ✅ Good**

MODEL_PRIVACY_BOUNDARIES.md lists what must be disclosed:

- what artifact text may be sent
- provider kind and name
- model role
- whether execution is local or remote
- retention/training terms
- whether local alternatives exist

This puts privacy in the user's hands. They can audit: "I sent my email corpus to OpenAI for signal extraction. That's a privacy boundary crossing I need to know about."

### 6. Schema Patches Are Minimal and Correct

**Status: ✅ Good**

Sprint 02.5 added fields to BuildManifest:

- model_role
- provider_kind
- provider_display_name
- model_name, model_version
- capability_flags
- local_vs_remote
- retention_policy

These are additive (no breaking changes) and necessary for drift analysis. A profile can say: "This profile was built with signal_extractor_llm from Anthropic using Claude 3.5 Sonnet. The model supports structured output and artifact citation."

---

## Unresolved Risks (Not Blockers, But Must Be Addressed in Sprint 03)

### 1. Capability Verification Is Defined But Not Implemented

**Status: ⚠️ Missing Enforcement**

MODEL_CAPABILITY_CONTRACTS.md defines what a model must support. But it doesn't say:

- Who verifies capabilities? A human, an automated check, provider metadata?
- What happens if a model claims to support structured_output but fails silently?
- Can capabilities change (e.g., a model updates and gains long_context support)?

**Example:** A downstream adapter configures Llama 2 for signal_extractor_llm. Llama 2 doesn't support json_schema_output. Should the system:
- Reject the configuration immediately?
- Accept it but downgrade signals to non-durable status?
- Attempt to use Llama anyway and fail at runtime?

The policy doesn't say.

**Recommendation:** Before Sprint 03 runtime code goes live, define:
- A capability verification function: `verify_model_capabilities(model_id, required_capabilities) → bool`
- A failure mode: reject configuration or downgrade to review-required status
- A testing strategy: how are capability claims validated?

### 2. Promotion Rule Is Philosophical But Not Enforced

**Status: ⚠️ Architectural Gap**

The policy says experience-only output can become durable only through "explicit promotion" via "artifact creation, classification, authorship-origin labeling, evidence support, confidence scoring, and claim validation gates."

But there's no:
- Code that enforces this rule
- Audit trail showing promotion happened
- Rejection mechanism if promotion fails

**Example:** A first_run_artifact_llm generates a summary. A user likes it and wants to add it to their evidence. What's the promotion flow? Is it:
1. Save the summary as a new artifact?
2. Classify it (authorship-origin = `assistant_output`)?
3. Re-ingest it through normal extraction?
4. Only then does it affect the profile?

Or can the summary somehow leak into evidence without going through classification?

**Recommendation:** Implement promotion as a required transformation:
```
experience_output → new Artifact → classify() → extract() → validate() → compile()
```
Each step must complete. Skipping any step prevents profile mutation.

### 3. Privacy Disclosure Is Required But Not Enforced

**Status: ⚠️ Missing Runtime Check**

MODEL_PRIVACY_BOUNDARIES.md says users should "be able to see" what data is sent where. But it doesn't specify:

- When is disclosure shown? During profile build? In a report?
- What if the user misconfigures and sends data to a remote provider accidentally?
- Is there a pre-flight check: "This profile uses OpenAI for signal extraction. 23MB of artifact text will be sent. Confirm?"

**Example:** A user runs `imprint compile --source=gmail --artifact-storage=metadata_only`. The system silently sends email bodies to OpenAI for extraction (because that's the default extractor). The user never sees the privacy boundary crossing.

**Recommendation:** Add a pre-flight privacy audit:
```
if profile.build_manifest.uses_remote_inference():
    show_privacy_disclosure(user)
    require_explicit_confirmation(user)
```

### 4. Decoding Policy Is Recorded But Not Validated

**Status: ⚠️ Vague Requirements**

MODEL_CAPABILITY_CONTRACTS.md mentions "declared decoding policy" (temperature, seed, determinism) but doesn't specify:

- What is "low-temperature operation"? 0.0-0.3? 0.0-0.5?
- Does determinism require seed support or just low temperature?
- What if a model's decoding policy changes between versions?

**Example:** A profile is built with Claude 3.5 Sonnet at temperature 0.2. Six months later, Anthropic releases Claude 4.0 with different temperature behavior. Is the profile still reproducible?

**Recommendation:** Define decoding policies as version-specific:
```
decoding_policy: {
    temperature: 0.2,
    seed: "deterministic",
    model_version: "claude-3.5-sonnet-20250101"
}
```

### 5. Experience-Only Roles Can Drift Undetected

**Status: ⚠️ Drift Opacity**

The policy says experience-only inference "does not define the durable profile." But what if an experience-only model changes?

**Example:** The profile_summarizer_llm is updated from Claude 3.5 to GPT-4. The durable profile is unchanged, but the summary a user sees is completely different. Is this drift or expected change?

The policy has no answer.

**Recommendation:** Record experience-only model metadata separately from profile-affecting metadata. When experience-only models change, generate a drift report marked as "UX change only—profile content unaffected."

---

## Critical Path Items for Sprint 03

### 1. Implement Capability Verification

**Action:** Build a capability verification function before accepting any model configuration:

```python
def verify_model_capabilities(model_id: str, role: ModelRole) -> CapabilityVerificationResult:
    required = ROLE_REQUIREMENTS[role]
    model_capabilities = get_model_capabilities(model_id)  # API, metadata, human review
    if not required.issubset(model_capabilities):
        return CapabilityVerificationResult(
            passed=False,
            missing_capabilities=required - model_capabilities,
            failure_mode=get_failure_mode(role)  # reject or downgrade
        )
    return CapabilityVerificationResult(passed=True)
```

### 2. Implement Promotion Pipeline

**Action:** Make experience-only output transformation non-bypassable:

```python
def promote_experience_output_to_profile(
    generated_artifact: str,
    model_role: ExperienceOnlyRole,
    source_profile: ExpressionProfile
) -> EvidenceReference | None:
    # Create new artifact
    artifact = Artifact(text=generated_artifact, source_type="model_promoted")
    
    # Classify (authorship_origin must be assistant_output)
    classification = classify_artifact(artifact)
    assert classification.authorship_origin == AuthorshipOrigin.ASSISTANT_OUTPUT
    
    # Extract signals (recompile from promoted artifact)
    signals = extract_signals(artifact, source_profile.source_policy)
    
    # Validate claims
    for signal in signals:
        validation_result = validate_claim(signal.claim)
        if validation_result.status == ClaimValidationStatus.FAILED:
            return None  # cannot promote; failed validation
    
    # Only if all gates pass does the evidence become durable
    return create_evidence_reference(artifact, classification, signals)
```

### 3. Implement Privacy Audit Pre-Flight

**Action:** Before building a profile with remote inference, show users:

```python
def pre_flight_privacy_audit(config: ProfileBuildConfig) -> PrivacyAuditReport:
    report = PrivacyAuditReport()
    for role, model_id in config.model_assignments.items():
        model = get_model_metadata(model_id)
        if model.execution_environment == "remote":
            report.add_disclosure(
                role=role,
                model_id=model_id,
                data_sent=estimate_data_volume(config.artifact_corpus, role),
                provider=model.provider,
                retention_policy=model.retention_policy,
                local_alternative_exists=check_local_alternative(role)
            )
    return report

# Usage:
audit = pre_flight_privacy_audit(config)
if audit.remote_inference_count > 0:
    user_confirms = show_disclosure_and_get_consent(audit)
    if not user_confirms:
        abort_build()
```

### 4. Define Decoding Policy Version-Specificity

**Action:** Update build manifest decoding policy to include model version:

```python
class DecodingPolicy(ImprintSchemaModel):
    temperature: float = Field(ge=0.0, le=2.0)
    seed: int | None = None
    determinism_required: bool = False
    model_version: str  # e.g., "claude-3.5-sonnet-20250101"
    policy_version: str  # decoding policy version, separate from model version
```

---

## Long-Term Stability Assessment

### Five-Year Outlook

The model provider policy will hold up **if**:

1. **Role taxonomy remains stable.** If new roles are added every sprint, the policy proliferates. Define all roles upfront or establish a strict role addition gate.

2. **Capability flags are versioned.** If `structured_output` has different meanings in different model versions, the contract breaks. Version capabilities alongside models.

3. **Experience-only promotion is never bypassed.** If sprint 04 adds a "quick summarize" feature that injects text directly into the profile, the entire policy collapses. Enforce promotion strictly.

4. **Remote provider use remains optional.** If a future sprint makes Anthropic (or any provider) the default, BYOM/BYOP is dead. Never depend on a specific provider.

5. **Privacy disclosures scale.** If the system ends up with 50 models calling 10 different providers, disclosure becomes overwhelming. Keep the model ecosystem clean and curated.

### Migration Hazards

1. **Adding a new capability flag requires manifests to know about it.** If a new flag is created (e.g., `ray_distributed_support`), old profiles don't know if the model supports it. Plan capability versioning ahead.

2. **Experience-only model changes are invisible in drift reports.** Future users won't understand why a 2-year-old profile summary looks different. Document this as expected behavior.

3. **Provider deprecation is not handled.** If OpenAI deprecates GPT-4, profiles using it are stuck. Design a model deprecation and migration policy before it happens.

---

## Findings by Severity

### Blockers (None)

Sprint 02.5 is architecturally sound and ready for Sprint 03.

### Majors (Must Implement Before Sprint 03 Deployment)

1. **Capability Verification Implementation**
   - Define how capabilities are verified (API, metadata, human review, or test-based)
   - Implement rejection or downgrade logic when capabilities are missing
   - Test all role/model pairs before shipping

2. **Promotion Pipeline Enforcement**
   - Make experience-only output transformation non-bypassable
   - Implement artifact creation → classification → extraction → validation chain
   - Audit that no experience-only output leaks into durable profiles

3. **Privacy Pre-Flight Audit**
   - Implement disclosure generation before profile build
   - Require explicit user confirmation for remote inference
   - Test that privacy audit catches all remote model uses

### Minors (Address But Not Critical for Sprint 03)

4. **Decoding Policy Versioning**
   - Version decoding policies separately from models
   - Record policy version in build manifest
   - Document what "low-temperature operation" means concretely

5. **Experience-Only Drift Reporting**
   - Separate experience-only model changes from profile changes
   - Generate drift reports for UX-only changes
   - Document that UX drift is expected and doesn't invalidate profiles

6. **Model Deprecation Policy**
   - Design what happens when a model is deprecated
   - Define replacement/migration strategy
   - Communicate deprecation schedule to users upfront

---

## Go / No-Go Decision

### ✅ GO for Sprint 03

**Verdict:** Sprint 02.5 model provider policy is production-ready. The BYOM/BYOP principle is enforced and verifiable.

**Mandatory before sprint 03 extraction code ships:**

1. **Implement capability verification.** No model can be used without verifying it meets its role's contract.
2. **Implement promotion pipeline.** Experience-only output must transform through classification→extraction→validation before becoming durable.
3. **Implement privacy audit pre-flight.** Users must see and confirm privacy boundary crossings before profile build.

**If these are done,** Sprint 03 can build profiles that work with any provider.

**If these are skipped,** Sprint 03 will hardcode a provider and BYOM/BYOP becomes marketing fiction.

---

## Closing

Sprint 02.5 delivered what it promised: a provider-neutral policy layer that makes Imprint genuinely portable across inference platforms.

The implementation work in Sprint 03 will determine whether the policy is genuine or theater.

Do the implementation work right, and Imprint can switch providers at compile time. Cut corners, and profiles become locked to whatever Sprint 03 hardcodes.

---

## Appendix: Capability Verification Checklist

Before a model is used for any role, verify:

- [ ] Model supports structured output (if required by role)?
- [ ] Model supports artifact ID citation (if required by role)?
- [ ] Model supports low-temperature operation (if required by role)?
- [ ] Model can operate locally or only remotely (user preference)?
- [ ] Model's retention/training terms are known (if remote)?
- [ ] Local alternative exists (for user awareness)?
- [ ] Embedding dimension is stable (if embedding_model)?
- [ ] Decoding policy is recorded (temperature, seed, determinism)?

Use this checklist before every profile build.
