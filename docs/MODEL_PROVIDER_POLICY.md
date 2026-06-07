# Model Provider Policy

Status: Sprint 02.5 model policy contract

## Decision

Imprint is BYOM/BYOP: bring your own model and bring your own provider.

Canonical Imprint schemas must not require OpenAI, Anthropic, Gemini, Forge, Ollama, LM Studio, OpenRouter, vLLM, llama.cpp, or any other provider. Provider-specific clients, authentication, retry behavior, model menus, SDK types, and deployment assumptions belong in adapters or runtime configuration, not canonical profile schemas.

## Provider-Neutral Contract

Canonical schemas may record provider metadata only at the level needed for reproducibility, privacy review, and drift analysis:

- model role
- provider kind
- provider display name
- base URL kind, without secrets
- model name
- model version, if known
- profile-affecting vs experience-only scope
- prompt or extractor version
- decoding policy needed for reproducibility
- capability flags
- local versus remote execution
- retention and training policy, if known

Provider secrets, full bearer tokens, tenant IDs, private base URLs, homelab hostnames, and account-specific identifiers are not canonical schema fields.

## Profile-Affecting Inference

Profile-affecting inference changes durable profile content or validation state. It must be recorded in the build manifest because model changes can produce compiler drift.

Profile-affecting roles include classification, signal extraction, claim validation, evidence interpretation, confidence assessment, and drift/comparability analysis.

## Experience-Only Generation

Experience-only generation improves UX but does not define the durable profile. It must not mutate the profile unless a user explicitly promotes generated material into the evidence corpus and that material passes normal artifact classification, authorship-origin policy, evidence, confidence, and claim validation gates.

Examples include first-run delight artifacts, markdown report prose, demo articles, and explanatory summaries.

## Local-First Requirement

Imprint must remain useful without remote model credentials. A local-only run may use deterministic rules, local models, or synthetic examples. Remote providers are optional and must be visible when used.

## Rejected Alternatives

### Default Hosted Provider

Rejected because it creates provider lock-in and hidden privacy expectations.

### Opaque Model Alias

Rejected because aliases cannot support drift analysis, privacy disclosure, or reproducibility.

### Runtime Client in Core Schema

Rejected because schema contracts should describe what happened, not implement how to call a provider.
