# Schema Philosophy

Status: Sprint 02 schema contract

## Principle

The Imprint schema is the platform contract. Runtime harvesters, extractors, storage engines, and downstream adapters may change, but exported profiles must remain understandable from structured fields alone.

Imprint schemas describe observed expression patterns. They do not model personality, diagnose people, infer hidden intent, or prescribe how a generation model should behave.

## Why Schemas Exist

Schemas exist to make five properties explicit:

1. **Evidence**: every signal and claim must say why it is believed.
2. **Boundary**: claims are labeled as observations, bounded interpretations, quarantined material, or prohibited material.
3. **Comparability**: two builds can be compared automatically from manifests and source-policy fields.
4. **Auditability limits**: metadata-only storage is the MVP default, so profiles must disclose when raw content is unavailable.
5. **Projection safety**: core exports contain profile data, not prompts, provider controls, or workflow instructions.

## Design Rules

- Prefer structured enums over prose labels when a downstream decision depends on them.
- Prefer aggregate support and artifact references over raw excerpts in public-safe exports.
- Keep authorship-origin evidence separate from claim confidence.
- Treat AI detector output as weak metadata unless corroborated by source or role evidence.
- Make context profiles explicit compiled views over filtered evidence, not inherited overlays.
- Preserve quarantined and prohibited claim states so validators can fail safely.

## Alternatives Rejected

### Prompt-Centric Profile Contract

Rejected because it couples Imprint to downstream model behavior, provider controls, and generation workflows.

### Raw-Corpus-First Contract

Rejected for the MVP because it increases privacy risk. Local raw storage is allowed only as an explicit non-default storage mode.

### Human-Judged Comparability

Rejected because profile drift claims must scale and be reproducible. The schema must expose enough manifest structure for automated comparability classification.

### Single Confidence Score

Rejected because confidence conflates attribution, authorship, extraction quality, evidence strength, source diversity, and policy fit. A display score may exist only as a derivation from named components.

## Implementation Boundary

Sprint 02 implements schema contracts only: Pydantic models, validation, serialization, JSON schema generation, and synthetic tests. It does not implement harvesting, storage engines, source adapters, LLM extractors, prompt exporters, or API endpoints.
