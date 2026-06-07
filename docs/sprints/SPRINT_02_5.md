# Sprint 02.5 - Model Provider and Inference Policy

Primary Model: GPT 5.5
Implementation Model: GPT 5.4 if schema patches are needed
Adversarial Reviewer: Gemini Antigravity
Status: Required after Sprint 02 schema work, before Sprint 03 ingestion implementation

## Mission

Define how Imprint selects, configures, records, and constrains LLMs and other inference models.

Sprint 02.5 exists because Sprint 02 schema work is already underway. Do not derail active Sprint 02 work. Instead, use this sprint to add a provider-neutral model policy layer and patch schemas after Sprint 02 lands.

## Core Position

Imprint is BYOM/BYOP by design:

- Bring your own model.
- Bring your own provider.
- Bring your own local or hosted inference stack.

Imprint must not assume OpenAI, Anthropic, Gemini, Forge, Ollama, LM Studio, OpenRouter, vLLM, llama.cpp, or any other single provider.

## Required Reading

Read:

- `docs/sprints/SPRINT_02.md`
- Sprint 02 outputs and schema implementation
- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/SCHEMA.md`

## Model Role Taxonomy

Define model roles such as:

- `classifier_llm`
- `signal_extractor_llm`
- `claim_validator_llm`
- `profile_summarizer_llm`
- `first_run_artifact_llm`
- `report_writer_llm`
- `embedding_model`
- `reranker_model`

## Profile-Affecting vs Experience-Only Inference

Separate model use into two categories.

### Profile-affecting inference

Affects durable profile outputs and must be recorded in the build manifest.

Examples:

- classification
- signal extraction
- claim validation
- evidence interpretation
- confidence assessment
- drift/comparability analysis

### Experience-only generation

Does not define the profile and must not mutate the profile unless explicitly promoted through validated evidence.

Examples:

- first-run delight artifact
- markdown report prose
- demo article
- explanatory summary

## Provider Abstraction

Define provider kinds such as:

- `openai_compatible`
- `anthropic`
- `gemini`
- `ollama`
- `lm_studio`
- `local_http`
- `forge`
- `custom`

Provider-specific implementation belongs in adapters. Canonical schemas must remain provider-neutral.

## Capability Contracts

Each model role must declare required capabilities.

Examples:

- structured output
- JSON schema output
- low-temperature operation
- long context
- stable embedding dimension
- deterministic seed support if available
- artifact ID citation support
- local-only support
- no-retention provider policy

## Build Manifest Requirements

For every profile-affecting model invocation, the build manifest must be able to record:

- model role
- provider kind
- provider name
- base URL kind, without secrets
- model name
- model version if known
- extractor family
- extractor version
- prompt version
- schema version
- temperature or decoding policy
- seed if supported
- capability flags
- local vs remote execution
- retention/training policy if known

## Privacy Requirements

Remote providers must be explicit.

Users should know:

- what artifact text is sent,
- to which provider,
- for which model role,
- whether the provider is remote or local,
- whether data retention/training terms are known,
- and whether a local alternative exists.

## Required Deliverables

Create:

- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/MODEL_ROLE_TAXONOMY.md`
- `docs/MODEL_CAPABILITY_CONTRACTS.md`
- `docs/MODEL_PRIVACY_BOUNDARIES.md`
- `docs/SPRINT_02_5_REMEDIATION_SUMMARY.md`

Update as needed:

- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`
- `docs/sprints/SPRINT_03.md`

Patch schema implementation only if Sprint 02 has already created model-related schemas or build manifest schemas that assume a provider.

## Forbidden Work

Do not:

- hard-code a provider,
- add actual provider clients,
- add API keys or secrets,
- implement model calls,
- implement LLM extraction logic,
- implement embeddings,
- or add Forge/local homelab-specific assumptions to canonical code.

## Exit Criteria

Sprint 02.5 is complete only when:

- Imprint has an explicit BYOM/BYOP policy,
- model roles are named and scoped,
- profile-affecting inference is separated from experience-only generation,
- build manifests can record provider/model/prompt/capability metadata,
- remote provider privacy boundaries are documented,
- no schema assumes one provider,
- and Sprint 03 can proceed without model-provider ambiguity.
