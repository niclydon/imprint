# Sprint 08 - Consumer Contracts and Integration Surfaces

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Ready after Sprint 07 export review

## Mission

Define the downstream consumer contracts that make Imprint exports usable by external systems without moving prompt assembly, publishing workflows, model configuration, or runtime integration into core Imprint.

Sprint 08 is about **consumer contracts**, not full integrations.

The output of Sprint 07 is a set of public-safe exports. Sprint 08 defines how consumers should read, validate, and use those exports.

## Required Reading

Read before making changes:

- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/MODEL_PRIVACY_BOUNDARIES.md`
- `src/imprint/exports/`
- `src/imprint/compiler/`
- `tests/test_exports.py`

## Sprint 07 Carry-Forward Constraints

Sprint 08 must preserve these review findings:

1. Treat canonical JSON as the source of truth for downstream projections.
2. Keep downstream prompt assembly outside core Imprint.
3. Keep generation settings outside core Imprint.
4. Keep publishing workflows outside core Imprint.
5. Keep Mosvera runtime behavior outside core Imprint.
6. Preserve no-raw-text public-safe boundaries.
7. Preserve opaque source IDs.
8. Add consumer-specific tests before any publishing or Mosvera runtime integration.
9. Decide whether classifier-version warnings are mandatory in every consumer-facing projection.

## Consumer Surfaces

Define contracts for these consumers.

### 1. Mosvera Consumer Contract

Purpose:
Allow Mosvera to consume an Imprint expression overlay without learning from raw private corpora or taking over profile inference.

Allowed:

- expression summaries
- observed structure/rhetorical/tone constraints
- avoid lists derived from interpretation boundaries
- source profile/version metadata
- no-raw-text evidence policy
- compatibility warnings

Forbidden:

- raw evidence
- source artifact text
- provider-specific visual prompts
- image generation instructions
- Mosvera runtime behavior
- aesthetic compilation inside Imprint

Boundary:

> Imprint compiles expression. Mosvera compiles aesthetic intent.

### 2. Broadside Consumer Contract

Purpose:
Allow Broadside or similar publishing systems to consume Imprint profile exports as input constraints, not as drafting logic.

Allowed:

- profile summary
- observed expression patterns
- confidence/limitations
- compatibility warnings
- public-safe first-run summary references

Forbidden:

- article generation prompts
- editorial workflow logic
- publishing schedules
- platform-specific formatting
- model parameters
- raw evidence

Boundary:

> Imprint tells Broadside what expression patterns are supported. Broadside decides how publishing workflows use them.

### 3. Agent / Application Consumer Contract

Purpose:
Allow future agents, apps, or tools to read Imprint exports safely.

Allowed:

- canonical JSON validation
- version compatibility checks
- profile metadata display
- evidence summary display
- safe pattern lookup

Forbidden:

- treating confidence as truth
- treating bounded interpretations as facts
- using quarantined/non-durable support as durable evidence
- inferring personality or diagnosis from profile patterns
- silently ignoring compatibility warnings

### 4. Human / CLI Consumer Contract

Purpose:
Define how a person using the CLI should inspect export outputs.

Allowed:

- summary display
- limitations display
- compatibility warnings
- export validation commands

Forbidden:

- dumping raw corpus text by default
- presenting profile claims as identity truth
- hiding audit limitations

## Required Deliverables

Create or update:

- `docs/CONSUMER_CONTRACTS.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/BROADSIDE_INTEGRATION.md`
- `docs/AGENT_CONSUMER_CONTRACT.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/EXPORT_FORMATS.md`

Implement only if needed:

- consumer contract validator helpers
- compatibility warning helpers
- consumer-specific export projection tests
- CLI validation command if small and scoped

## Required Implementation Scope

Allowed:

- contract schemas/types if existing exports need them
- deterministic validators for consumer payloads
- consumer-specific safety checks
- compatibility-warning helpers
- tests for Mosvera/Broadside/agent contract payloads
- docs describing contracts and boundaries

Forbidden:

- Mosvera runtime integration
- Broadside API integration
- publishing workflows
- prompt assembly
- provider-specific generation settings
- LLM calls
- remote APIs
- embedding/vector search
- image generation instructions
- raw evidence export
- UI/dashboard implementation

## Version and Warning Policy

Sprint 08 must decide and document whether these warnings are mandatory in every consumer-facing export:

- mixed classifier versions
- incompatible signal model versions
- compiler version changes
- metadata-only audit limitations
- bounded interpretation policy state
- non-comparable or partially comparable profile state

Default recommendation:

Consumer-facing exports should surface compatibility warnings, not just canonical JSON.

## Test Requirements

Add tests proving:

- Mosvera consumer payload contains no raw evidence, prompts, provider settings, or generation instructions
- Broadside consumer payload contains no publishing workflow or platform-specific formatting logic
- agent consumer payload preserves warning/compatibility metadata
- consumer projections preserve opaque source IDs
- consumer projections preserve no-raw-text policy
- mixed classifier-version warnings appear in consumer-facing projections if required by policy
- validators reject generation-control fields such as `prompt`, `temperature`, `model_hint`, `provider`, or `system_prompt`
- no remote/provider calls are required

## Expected Code Shape

Prefer a small module if implementation is needed:

```text
src/imprint/consumers/
  __init__.py
  contracts.py
  validation.py
  mosvera.py
  broadside.py
  agents.py
```

Do not build real downstream integrations yet.

## Exit Criteria

Sprint 08 is complete only if:

- consumer contracts are documented
- Mosvera/Broadside/agent boundaries are explicit
- compatibility warning policy is documented
- consumer-facing projections preserve export safety rules
- tests prove no prompts/provider settings/raw evidence leak into consumer contracts
- no runtime integrations are introduced
- all tests pass

At the end, summarize:

- files changed
- tests run
- consumer contracts defined
- boundaries preserved
- remaining blockers for Sprint 09 private connectors or Sprint 10 web presence
