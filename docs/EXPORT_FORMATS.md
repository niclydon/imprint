# Export Formats

Status: Sprint 07 baseline

## Purpose

Sprint 07 defines public-safe export formats for compiled `ExpressionProfile` objects. Exports make
profiles useful without weakening ingestion, classification, signal extraction, or profile compiler
boundaries.

All Sprint 07 exports are deterministic, local, provider-neutral, and generated from compiled
profile data only.

## Canonical JSON Export

The canonical JSON export is the machine-readable public-safe contract.

It includes:

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

The Markdown export is a concise profile summary for humans.

It includes:

- profile basis and build metadata
- observed expression patterns
- support counts and source types
- confidence summaries
- limitations and privacy posture
- version compatibility metadata

It uses evidence-scoped language such as “Observed pattern” and “Supported by N included artifacts.”
It does not use diagnostic, personality, hidden-intent, or certainty language.

## First-Run Output

The first-run export is the “What Imprint Learned” experience. It is generated from compiled
profile data, not raw artifacts.

It includes:

- profile overview
- strongest observed patterns
- limited-evidence cautions
- high-level excluded/quarantined boundary language
- what Imprint can and cannot say

This output is a user-facing explanation, not durable profile evidence.

## Mosvera Expression Overlay

The Mosvera overlay is a public-safe bridge contract. It contains expression summaries and avoid
patterns derived from compiled profile signals.

It includes:

- overlay version
- source profile metadata
- no-raw-text evidence policy
- expression summaries
- anti-pattern summaries
- explicit boundary text

It excludes provider prompts, image generation instructions, Mosvera runtime behavior, raw evidence,
and aesthetic-intent compilation.

## Safety Enforcement

All public-safe exporters call shared safety validation before returning output. The validator
rejects:

- prohibited claims
- quarantined claims
- bounded interpretations unless explicitly allowed
- non-durable support exported as durable evidence
- mixed signal model versions inside exported support
- path-like or non-opaque source IDs
- generation-control keys such as `prompt`, `temperature`, or `model_hint`

## CLI

Sprint 07 adds:

```bash
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format json
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format markdown
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format first-run
imprint export-profile --source-type local_transcript_json --path tests/fixtures/local_transcript_json/signal-transcript.json --format mosvera
```

The CLI compiles a local profile first, then emits the selected export format.
