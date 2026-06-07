# Export Formats

Status: Sprint 08 consumer-contract baseline

## Purpose

Imprint exports public-safe compiled `ExpressionProfile` data. Exports make profiles useful without
weakening ingestion, classification, signal extraction, profile compiler, evidence, confidence, or
privacy boundaries.

All public-safe exports are deterministic, local, provider-neutral, and generated from compiled
profile data only.

## Source of Truth

Canonical JSON is the machine-readable source of truth for downstream consumers. Consumer-specific
payloads are projections of canonical JSON. They may narrow fields for a use case, but they must not
introduce new evidence, raw text, generation controls, publishing behavior, or runtime integration
logic.

## Canonical JSON Export

The canonical JSON export includes:

- export ID, export type, export schema version, and mode
- profile ID and subject ID
- build manifest, artifact storage policy, and source policy metadata
- source summary and context summaries
- compiled expression patterns
- support summaries with opaque source IDs, rule IDs, classifier versions, signal model versions,
  support counts, confidence, and limitations
- compatibility warnings for version-sensitive profiles

It excludes:

- raw artifact text
- source snippets
- filesystem paths
- private local locators
- provider prompts
- generation controls
- downstream writing instructions
- prohibited or ungated bounded-interpretation claims

The deterministic serializer is `canonical_profile_json(profile)` in `src/imprint/exports/`.

## Human-Readable Markdown Export

The Markdown export is a concise profile summary for humans. It includes profile basis, observed
expression patterns, support counts, confidence summaries, limitations, privacy posture, and version
compatibility metadata.

It uses evidence-scoped language such as “Observed pattern” and “Supported by N included artifacts.”
It does not use diagnostic, personality, hidden-intent, or certainty language.

## First-Run Output

The first-run export is the “What Imprint Learned” experience. It is generated from compiled profile
data, not raw artifacts.

It includes profile overview, strongest observed patterns, limited-evidence cautions, high-level
excluded/quarantined boundary language, and what Imprint can and cannot say. This output is a
user-facing explanation, not durable profile evidence.

## Mosvera Expression Overlay

The Mosvera overlay is a public-safe bridge contract. It contains expression summaries and avoid
patterns derived from compiled profile signals.

It includes overlay version, source profile metadata, no-raw-text evidence policy, expression
summaries, anti-pattern summaries, opaque source IDs, mandatory compatibility warnings, and boundary
text.

It excludes provider prompts, image generation instructions, Mosvera runtime behavior, raw evidence,
and aesthetic-intent compilation.

## Sprint 08 Consumer Contracts

Sprint 08 adds deterministic consumer projections under `src/imprint/consumers/`:

- `mosvera_consumer_contract(profile)` for Mosvera expression overlays
- `broadside_consumer_contract(profile)` for publication-system input constraints
- `agent_consumer_contract(profile)` for safe application and agent lookup
- `human_cli_consumer_contract(profile)` for CLI inspection surfaces

Every consumer projection includes:

- source profile metadata
- no-raw-text evidence policy
- opaque source IDs where source support is shown
- compatibility metadata and warnings
- consumer contract schema version

Consumer projections must reject generation-control fields such as `prompt`, `system_prompt`,
`temperature`, `model_hint`, `provider`, and related decoding controls.

## Safety Enforcement

All public-safe exporters call shared safety validation before returning output. The validator
rejects:

- prohibited claims
- quarantined claims
- bounded interpretations unless explicitly allowed
- non-durable support exported as durable evidence
- mixed signal model versions inside exported support
- path-like or non-opaque source IDs
- generation-control keys such as `prompt`, `temperature`, `model_hint`, or `provider`

Consumer payloads are validated with the same public-safe payload checks.

## CLI

Supported export smoke commands:

```bash
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format json
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format markdown
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format first-run
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format mosvera
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format mosvera-consumer
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format broadside
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format agent
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format human-cli
```

The CLI compiles a local profile first, then emits the selected public-safe export or consumer
projection.
