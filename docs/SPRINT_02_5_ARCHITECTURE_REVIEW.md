# Sprint 02.5 Model Provider Architecture Review

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Pre-delivery readiness gate  
**Context:** Evaluation of Sprint 02.5 planning and deliverables scope for model provider and inference policy

---

## Executive Summary

Sprint 02.5 has not been delivered yet. The scope is well-defined in the sprint planning document, but the work itself is in flight or pending.

This review serves as a **pre-delivery gate.** It identifies the specific deliverables that are non-negotiable for Sprint 02.5 to unblock Sprint 03 and flags the architectural risks that will emerge if this work is rushed or deferred.

**Verdict: CONDITIONAL CLEARANCE to start Sprint 02.5 work**

Do not start Sprint 02.5 extraction/classification code until Sprint 02.5 model policy work is complete. Deferring model policy to Sprint 03 will force extraction code to make ad-hoc provider decisions and the system will ship provider-locked.

---

## Sprint 02.5 Mandate (From Planning Doc)

Sprint 02.5 exists because:

1. Sprint 02 schema work is already underway and cannot wait for model provider decisions
2. Model provider policy must be separate from schema design
3. **Do not derail active Sprint 02 work** — add model policy as a patch after Sprint 02 lands if needed

**Core Position: Imprint is BYOM/BYOP** (Bring Your Own Model, Bring Your Own Provider)

This is not optional. The entire architecture depends on provider neutrality.

### Required Deliverables (From Sprint 02.5.md)

1. **MODEL_PROVIDER_POLICY.md** — Overall strategy for provider abstraction and neutrality
2. **MODEL_ROLE_TAXONOMY.md** — Named roles with capabilities (classifier, extractor, validator, etc.)
3. **MODEL_CAPABILITY_CONTRACTS.md** — Concrete capability requirements for each role
4. **MODEL_PRIVACY_BOUNDARIES.md** — What data is sent where, retention terms, local alternatives
5. **SPRINT_02_5_REMEDIATION_SUMMARY.md** — Executive summary of decisions and constraints

### Required Schema Patches (If Needed)

Update Sprint 02 schemas only if necessary:

- `docs/EXTRACTOR_VERSIONING.md` — add model role and capability metadata
- `docs/PRIVACY_AND_LOCAL_MODE.md` — document privacy boundaries
- `docs/EVIDENCE_AND_CONFIDENCE.md` — clarify how detector and model outputs combine
- `docs/SCHEMA.md` — add capability contract fields if missing

---

## Critical Design Questions That Sprint 02.5 Must Resolve

### 1. Model Role Taxonomy: Seven Roles or More?

**Question:** Sprint 02.5.md lists 8 roles:
- `classifier_llm`
- `signal_extractor_llm`
- `claim_validator_llm`
- `profile_summarizer_llm`
- `first_run_artifact_llm`
- `report_writer_llm`
- `embedding_model`
- `reranker_model`

Is this list complete? Missing roles?

**Why it matters:** The build manifest must record which model is used for each profile-affecting role. If roles are incomplete, manifests will have unlabeled model use.

**Risk:** If new roles are discovered during Sprint 03, the build manifest schema is incomplete and profiles already using it must be migrated.

**Recommendation:** Enumerate all expected roles for a five-year horizon. If uncertain, include `_llm` and `_model` catch-all roles for unanticipated uses. Document the list in both SCHEMA.md and the build manifest.

### 2. Capability Contracts: Can They Be Tested?

**Question:** Each role declares required capabilities. Can these be validated automatically?

Example: `classifier_llm` requires:
- structured output
- JSON schema output
- low-temperature operation

**How to test:** Can the system validate that a candidate model meets these? Is it:
- Manual checklist (human verifies provider documentation)?
- Automated probe (system runs a test query and checks output)?
- Provider metadata (system queries provider API for capability flags)?

**Risk:** If capabilities are vague, downstream systems will choose models that appear to fit but fail silently. Example: a model that "supports structured output" but doesn't actually respect the JSON schema, only emits JSON-like text.

**Recommendation:** Define testable capability contracts. For example:
- Structured output: model can accept and respect a JSON schema in the prompt; tested by comparing output against schema
- Low-temperature operation: model accepts temperature in range [0, 0.3] and produces deterministic output; tested by running same prompt multiple times and checking for identical output
- Long context: model accepts and correctly processes 100k+ token input; tested by probing its ability to cite artifacts from position N

### 3. Provider Abstraction: Interface or Configuration?

**Question:** How do extractors access models?

**Option A: Provider Interface**
```python
class ModelProvider:
    def classifier(self, config: ClassifierConfig) -> ClassifierLLM: ...
    def extractor(self, config: ExtractorConfig) -> ExtractorLLM: ...
    def validator(self, config: ValidatorConfig) -> ValidatorLLM: ...
```

**Option B: Configuration-Based**
```python
config.model_providers = {
    'classifier': 'anthropic:claude-3.5-sonnet',
    'extractor': 'ollama:llama2-local',
    'validator': 'openai:gpt-4',
}
```

**Risk of Option A:** If the interface is too rich, it becomes provider-specific. Someone will add Anthropic-specific fields and the abstraction breaks.

**Risk of Option B:** If configuration is too simple, it hides important details. Extractors won't know if a model supports structured output until they try to use it.

**Recommendation:** Use a hybrid: configuration specifies model identifier (e.g., `anthropic:claude-3.5-sonnet`), and a provider registry maps identifiers to capabilities and endpoints. Extractors query the registry before use.

### 4. Profile-Affecting vs Experience-Only Generation

**Question:** Which model uses are recorded in the build manifest?

**Clear Profile-Affecting:**
- Classification (authorship-origin labels)
- Signal extraction (claims, signals)
- Claim validation (pass/fail for prohibited claims)
- Confidence assessment (confidence components)

**Ambiguous:**
- Artifact summarization (is it used in evidence or just for UI display?)
- Report prose generation (is it part of the profile or just how it's presented?)
- Explanatory text (does downstream code depend on it or is it decorative?)

**Risk:** If report prose is generated with an LLM and that generation affects what downstream systems think the profile says, then the LLM is profile-affecting and must be recorded in the manifest. But Sprint 02 schema suggests report generation is experience-only.

**Recommendation:** Define profile-affecting strictly: any model use that determines what a downstream system will do is profile-affecting and must be in the manifest. Anything that just makes the profile prettier is experience-only. Document examples clearly.

### 5. Remote Provider Data Flow: What Gets Sent?

**Question:** When using OpenAI, Anthropic, Gemini, or another remote provider, what artifact data is sent?

**Scenarios:**
- Full artifact text (privacy risk)
- Artifact hash and metadata (privacy-safe)
- Artifact ID only (most privacy-safe, but less useful to the model)
- Heuristically determined (e.g., send full text for short artifacts, hash for long ones)

**Risk:** If data flow is not specified, extractors will send full artifact text by default to maximize accuracy, and users will unknowingly leak private data to remote providers.

**Recommendation:** Define a default privacy mode (metadata or hash only) and allow opt-in to full text only when the user explicitly configures local-only or ephemeral storage (not metadata-only). Document which providers offer no-retention policies and which don't.

### 6. Local-Only Constraint for Sensitive Roles

**Question:** Should the claim validator always run locally?

The validator determines if a claim is prohibited. If the validator runs on a remote LLM, a provider could theoretically suppress certain claims. This is a trust boundary.

**Risk:** Users with metadata-only storage (the MVP default) will unknowingly have their profiles validated by a remote provider.

**Recommendation:** The claim validator should run locally or on a trusted provider only. Document this constraint explicitly. If local validation is required, classify the validator as a "critical role" and require local execution.

### 7. Model Capability Drift and Profile Invalidation

**Question:** If a model is deprecated, what happens to profiles that depend on it?

**Scenario:** A profile is built with `gpt-4-turbo`. Six months later, OpenAI deprecates it. Downstream systems want to rebuild the profile. Should they:
- Use `gpt-4o` as a replacement (different model, `NOT_COMPARABLE`)?
- Refuse to rebuild (profile is stale)?
- Use an explicit migration policy (profile can be rebuilt if user approves)?

**Risk:** If there's no policy, users will either accept incorrect comparability or be stuck with stale profiles.

**Recommendation:** Define a model lifecycle policy. When a model is deprecated:
1. Flag all profiles using it as `capability_expired`
2. Recommend a replacement model (if available)
3. Require explicit user opt-in to use the replacement
4. Mark the rebuilt profile as `NOT_COMPARABLE` unless an explicit migration was approved

---

## Risk Assessment: What Could Go Wrong

### 1. Provider Lock-In Despite BYOM/BYOP Claims

**Risk:** Imprint claims to be provider-neutral but hardcodes one provider.

**Example:** The extractor uses Claude for semantic extraction. The schema says model_provider is nullable and configurable. But the extraction code is hardcoded to call `anthropic_client.messages.create()`. A user wanting to use Ollama or Gemini would need to fork the code.

**Mitigation:** Code review must verify that model calls are abstracted through a provider interface, not hardcoded to one provider.

**Severity:** HIGH. This violates the core mission.

### 2. Capability Contracts Are Too Vague to Enforce

**Risk:** Contracts say "supports structured output" but some models "support" it by emitting valid JSON without actually respecting the schema.

**Example:** A model emits `{"field": "value"}` that happens to be valid JSON but doesn't constrain itself to the required schema. The extractor gets malformed output but the model passed the "structured output" capability check.

**Mitigation:** Define testable capabilities with concrete examples. "Structured output" means: model is passed a JSON schema, must only emit JSON that validates against that schema, must never emit schema violations.

**Severity:** HIGH. Silent failures will cause profiles to be incorrect.

### 3. Privacy Boundaries Are Aspirational, Not Enforced

**Risk:** The policy says "remote providers should be explicit" but code doesn't check.

**Example:** An extractor sends full artifact text to a remote provider without asking the user. The build manifest records the provider but the user never knew their private data was sent.

**Mitigation:** Add a pre-flight check: before calling a remote provider, verify the artifact storage mode allows it. Metadata-only → don't send full text. Local_artifact_store → ask the user. Ephemeral → OK to send.

**Severity:** HIGH. Privacy incident waiting to happen.

### 4. Model Roles Proliferate Unmanagededly

**Risk:** By Sprint 06, there are 50 model roles, each with different capability contracts.

**Mitigation:** Establish a role addition gate. New roles require explicit review and documentation. Don't allow ad-hoc roles like `summarizer_llm_v2` or `report_writer_alternative`.

**Severity:** MEDIUM. The system becomes unmaintainable but doesn't break.

### 5. Evidence Weighting Assumes One Model Provider

**Risk:** Confidence components are designed assuming one extractor model. If a profile uses two models (Claude for lexical, Llama for tone), how are confidences combined?

**Mitigation:** Design confidence as model-agnostic, then add model_agreement as an optional component if multiple models are used.

**Severity:** MEDIUM. Profiles with mixed-model extraction will be confusing.

### 6. Capability Contracts Become Outdated

**Risk:** A capability contract says "low temperature operation: 0.0-0.3". In six months, new models with better determinism allow 0.0-0.5. The contract is outdated and overly restrictive.

**Mitigation:** Version capability contracts separately from models. Allow providers to declare exceeding capabilities and have code accept the upgrade.

**Severity:** LOW. This is more an evolution problem than a stability problem.

---

## Mandatory Deliverables (Non-Negotiable for Sprint 03)

### 1. MODEL_ROLE_TAXONOMY.md

**Must include:**
- List of all model roles (classifier, extractor, validator, summarizer, reporter, embedding, reranker, ...)
- For each role: profile-affecting or experience-only?
- For each role: default provider (if any)
- For each role: fallback or is it required?

### 2. MODEL_CAPABILITY_CONTRACTS.md

**Must include:**
- For each role, list of required capabilities
- For each capability, testable definition and examples
- For each capability, list of models known to support it
- Versioning scheme (v0.1, v0.2) if capability definition changes

### 3. MODEL_PRIVACY_BOUNDARIES.md

**Must include:**
- For each role and provider kind, what data is sent?
- For each remote provider, what are the retention/training terms?
- Which roles must run locally only (critical roles)?
- How artifact storage mode (metadata-only, local, ephemeral) constrains remote provider use?

### 4. MODEL_PROVIDER_POLICY.md

**Must include:**
- Core position: BYOM/BYOP (Bring Your Own Model/Provider)
- Provider kinds: openai, anthropic, gemini, ollama, lm_studio, custom, ...
- Provider abstraction: how does code access models?
- Model capability verification: manual, automated, provider API?
- Deprecation policy: what happens when a model is deprecated?
- Fallback strategy: if a model fails, what's the fallback?

### 5. Build Manifest Patches

**Must update:**
- BuildManifest to include model_role_assignments (which role uses which model)
- Build manifest to include capability_verification_date (when was this model's capabilities last checked?)
- Extractor versions to include model_role field

---

## Risks If Sprint 02.5 Is Deferred

If Sprint 02.5 is deferred to Sprint 03 or later:

1. **Sprint 03 extraction code will make ad-hoc provider decisions.** Hardcoding to Anthropic or OpenAI.
2. **Capability contracts will be implicit in code, not explicit.** Difficult to change models later.
3. **Privacy boundaries will be unclear.** Users won't know if their data is sent to remote providers.
4. **Build manifests will record which provider was used but not why or how.** Makes auditing and debugging impossible.
5. **Profiles will be provider-locked even if the schema claims provider neutrality.**

**Implication:** If you ship extraction code before defining model provider policy, you're committed to that choice.

---

## Go / No-Go Decision

### ⚠️ CONDITIONAL GO for Sprint 02.5 Work

**Verdict:** It is safe to begin Sprint 02.5 model provider work in parallel with Sprint 03 extraction work, **as long as**:

1. **Extraction code does NOT hard-code provider calls.** Must use a provider abstraction layer.
2. **Build manifest records model role and provider at build time.** Even if the provider choice is temporary.
3. **Model privacy boundaries are documented before Sprint 03 code is released.** Even if enforcement comes later.

**If these are satisfied,** profiles built during development can survive a provider change later.

**If these are skipped,** profiles will be permanently provider-locked.

---

## Recommendations for Sprint 02.5 Execution

### Week 1: Finalize Model Role Taxonomy

1. List all planned model roles (classifier, extractor, validator, summarizer, reporter, embeddings, reranker)
2. For each role, determine: profile-affecting or experience-only?
3. For each role, determine: can it be local-only or must it accept remote?
4. Document default provider assumption (Claude, GPT, etc.) or state none

### Week 2: Define Capability Contracts

1. For each role, list required capabilities (structured output, low-temperature, long context, etc.)
2. For each capability, write testable definition with examples
3. Collect list of candidate models for each role and their capabilities
4. Document any capability conflicts (e.g., low-temperature requires stable model)

### Week 3: Document Privacy Boundaries

1. For each (role, provider) pair, specify what data is sent
2. For each remote provider, document retention/training terms
3. Identify critical roles that must run locally (claim validator?)
4. Document how artifact storage mode (metadata-only, local) constrains provider choice

### Week 4: Synthesize Policy and Patch Schemas

1. Write MODEL_PROVIDER_POLICY.md with core BYOM/BYOP position
2. Patch Sprint 02 schemas if needed (add model_role_assignments, capability flags)
3. Write SPRINT_02_5_REMEDIATION_SUMMARY.md with decisions and constraints
4. Update EXTRACTOR_VERSIONING.md, PRIVACY_AND_LOCAL_MODE.md with model metadata

---

## Closing

Sprint 02.5 is not just documentation—it's the foundation for the entire inference layer. If you get it right, Sprint 03 can plug in any combination of models. If you defer it, you're committing to a specific provider for the next three years.

Do this work first. Do it thoroughly. Then Sprint 03 extraction code can be provider-agnostic.

---

## Appendix: Model Role Decision Tree

Use this to finalize the role taxonomy:

```
For each inference task in the system:
  1. Is the output part of the durable profile? → Profile-affecting
  2. Can the output change if the model changes? → Profile-affecting
  3. Will downstream code make different decisions based on this output? → Profile-affecting
  4. If profile-affecting:
     a. Can it run locally only? → Mark as local-optional
     b. Must it use a remote provider? → Mark as remote-required
     c. Can it use any provider? → Mark as provider-flexible
     d. Assign a model role name (e.g., signal_extractor_llm)
  5. If experience-only:
     a. Is it visible to users? → Mark as user-facing
     b. Can it use lower-quality/cheaper models? → Mark as cost-optimizable
     c. Assign a descriptive name (e.g., report_writer_llm)
```

For example:
- **Artifact classification** → Profile-affecting, local-optional, role = classifier_llm
- **Signal extraction** → Profile-affecting, local-optional, role = signal_extractor_llm
- **Claim validation** → Profile-affecting, local-required (trust boundary), role = claim_validator_llm
- **Report prose** → Experience-only, user-facing, cost-optimizable, role = report_writer_llm
- **First-run artifact** → Experience-only, user-facing, role = first_run_artifact_llm
