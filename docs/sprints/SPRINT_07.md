# Sprint 07 - Export Contracts and First-Run Experience

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Ready after Sprint 06 profile compiler review

## Mission

Build the first public-safe export layer for compiled Imprint profiles.

Sprint 07 turns compiled profiles into useful consumable artifacts while preserving all upstream safety boundaries from ingestion, classification, signal extraction, and profile compilation.

This sprint is no longer just “Mosvera exporter.” Mosvera compatibility is one export target. The broader goal is to define and implement export contracts for:

- machine-readable profile export
- human-readable profile summary
- first-run “What Imprint Learned” output
- future Mosvera expression overlay compatibility

Sprint 07 should make Imprint understandable and useful without leaking private evidence or turning into a writing assistant.

## Required Reading

Read before making changes:

- `docs/SPRINT_06_ARCHITECTURE_REVIEW.md`
- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/MODEL_PRIVACY_BOUNDARIES.md`
- `docs/sprints/SPRINT_07.md`
- `src/imprint/compiler/`
- `src/imprint/signals/`
- `src/imprint/classification/`
- `src/imprint/schemas/`
- `tests/test_compiler.py`
- `tests/test_signals.py`
- `tests/test_classification.py`

## Sprint 06 Carry-Forward Constraints

The Sprint 06 architecture review approved profile compilation for Sprint 07 with these constraints:

1. Do not weaken claim-level validation.
2. `PROHIBITED` signals remain errors.
3. `BOUNDED_INTERPRETATION` remains policy-gated.
4. Do not merge incompatible signal model versions without an explicit migration layer.
5. Keep source IDs opaque in all export formats.
6. Do not expose `artifact.reference.source_id` raw to consumers if it could contain implementation detail.
7. Maintain no-raw-text public-safe exports.
8. Profiles are summaries, not raw-text archives.
9. If context profiles are enriched, preserve explicit filter/divergence modeling.
10. Do not introduce hidden inheritance or implicit source-type magic.

## Required Export Targets

### 1. Canonical JSON Export

Machine-readable, public-safe, deterministic.

Must include:

- profile ID/version
- build manifest
- compiled expression patterns
- support summaries
- confidence summaries
- source type summaries
- limitations and audit constraints
- compatibility/version metadata

Must not include:

- raw artifact text
- filesystem paths
- private local locators
- provider prompts
- downstream writing instructions
- person-level diagnostic or psychological claims

### 2. Human-Readable Markdown Export

A concise profile summary for users and repo artifacts.

Must include:

- what the profile is based on
- high-confidence observed expression patterns
- limitations
- audit/privacy posture
- version/build metadata

Must not overstate certainty.

Use language like:

- “Observed pattern”
- “Supported by N included artifacts”
- “Limited by metadata-only storage”

Avoid language like:

- “The subject is...”
- “This proves...”
- “Personality...”

### 3. First-Run “What Imprint Learned” Export

This is the first meaningful user experience.

It should be generated from compiled profile data, not raw artifacts.

It should include:

- corpus/profile overview
- strongest observed patterns
- low-confidence or limited-evidence warnings
- what was excluded/quarantined at a high level
- what Imprint can and cannot say

It should make the user feel understood without implying that Imprint has become them, diagnosed them, or inferred private intent.

### 4. Mosvera Expression Overlay Contract

Define a public-safe export contract that Mosvera can consume later.

This sprint should define and possibly emit a minimal Mosvera-compatible expression fragment, but must not implement Mosvera runtime behavior.

Allowed:

- expression constraints
- observed structure/tone/rhetorical pattern summaries
- avoid lists based on interpretation boundaries
- source profile/version metadata
- no-raw-text evidence policy

Forbidden:

- provider-specific prompts
- image generation instructions
- Mosvera provider compilation
- copying raw Imprint evidence into Mosvera
- making Mosvera infer expression from private corpora

Boundary rule:

> Imprint compiles expression. Mosvera compiles aesthetic intent. Sprint 07 may define the bridge, not merge the systems.

## Required Implementation Scope

Allowed:

- export interfaces
- JSON export
- Markdown export
- first-run summary export
- Mosvera expression overlay contract/export skeleton
- public-safe serialization helpers
- CLI export command if small and scoped
- tests using synthetic profiles
- documentation of export formats

Forbidden:

- LLM calls
- remote APIs
- prompt generation for writing systems
- publishing workflows
- Broadside integration
- Mosvera runtime integration
- web UI
- first-run demo article generation
- raw evidence export by default

## Export Safety Requirements

Every public-safe export must enforce:

- no raw artifact text
- no filesystem paths
- no private local locators
- no prohibited claims
- no non-durable/quarantined signal support as durable evidence
- no hidden merge of incompatible signal versions
- no provider-specific generation settings

## Test Requirements

Add tests proving:

- JSON export is deterministic
- Markdown export is deterministic enough for snapshot-style validation
- public-safe exports contain no raw text or paths
- prohibited claims cannot export
- bounded interpretations remain policy-gated
- opaque source IDs remain opaque
- incompatible signal model versions cannot be silently exported as comparable
- first-run summary uses only compiled profile data
- Mosvera overlay contains expression summaries only, not raw evidence or provider prompts
- no LLM/provider calls are required

## Documentation Requirements

Create or update:

- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`

Update as needed:

- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `docs/sprints/SPRINT_07.md`

## Expected Code Shape

Prefer a structure like:

```text
src/imprint/exports/
  __init__.py
  json_export.py
  markdown_export.py
  first_run.py
  mosvera.py
  safety.py
```

Keep implementation deterministic and boring.

## Exit Criteria

Sprint 07 is complete only if:

- compiled profiles can export as public-safe JSON
- compiled profiles can export as human-readable Markdown
- first-run “What Imprint Learned” output exists
- Mosvera expression overlay contract exists
- all exports preserve profile/compiler safety boundaries
- no raw private text or paths leak
- no provider assumptions are introduced
- docs describe export formats and boundaries
- all tests pass

At the end, summarize:

- files changed
- tests run
- export formats implemented
- boundaries preserved
- remaining blockers for Sprint 08 / downstream integrations
