# Imprint Project Strategy

Status: planning
Audience: public contributors, downstream integrators, maintainers
Repository status: public-ready design, private deployment details must remain external

## One-line thesis

Imprint derives structured expression profiles from human-created artifacts so downstream systems can preserve a person's communication style, reasoning patterns, and expressive identity without hard-coding private data into application code.

## Product definition

Imprint is an identity and expression compiler.

It is not a writing assistant, publishing platform, memory system, or personal knowledge graph. Those systems can provide input to Imprint or consume its output, but Imprint owns the transformation from evidence to reusable expression profiles.

## Core jobs

1. Harvest candidate artifacts from configurable sources.
2. Classify each artifact by speaker, format, audience, provenance, and assistance risk.
3. Extract voice, expression, reasoning, structure, lexical, and anti-pattern signals.
4. Compile versioned expression profiles.
5. Export profiles through stable schemas for downstream systems.
6. Support public-by-default development without leaking private data, private infrastructure names, credentials, or personal corpus content.

## Public positioning

Imprint should be understandable as an open-source tool anyone can run against their own data.

> Imprint analyzes writing, messages, transcripts, and other human-authored artifacts to produce structured expression profiles for use in drafting, agents, brand systems, creative tools, and personal AI systems.

## Target users

- Builders with personal AI systems who want controlled voice and identity profiles.
- Writers who want to preserve style while using AI-assisted drafting.
- Teams that need brand or executive voice profiles with provenance and drift tracking.
- Researchers exploring stylometry, authorship signals, and AI-assisted writing drift.
- Downstream tools that need a clean expression-profile contract instead of raw writing samples.

## Non-goals

- Do not become a general personal data lake.
- Do not own raw long-term memory.
- Do not publish or store private data in the repository.
- Do not require any specific private platform, project, homelab, database, or model router.
- Do not assume one person's corpus shape.
- Do not train a model on private writing by default.
- Do not silently mix human-authored and AI-assisted writing as equivalent samples.

## Design principles

### Public first

All code, schemas, examples, docs, and tests must be safe for a public repository. Private details belong in ignored config, external source systems, or local fixtures that are never committed.

### Evidence, not vibes

Every compiled signal should be traceable to evidence metadata: source type, time range, confidence, speaker attribution, artifact class, and AI-assistance risk.

### Voice is multi-dimensional

A chat message can be useful for vocabulary and tone but weak for long-form structure. A published essay can be useful for structure and reasoning but less representative of casual vocabulary. Imprint must preserve these distinctions.

### Raw samples are not profiles

Few-shot examples are inputs. The product is the compiled expression profile. Downstream systems should not have to consume raw emails or private messages to produce good writing.

### Profiles are versioned

Identity and expression drift over time. Imprint should produce profile versions with source windows, model versions, extractor versions, and drift notes.

### Private deployments are configuration

All local paths, database URLs, API keys, person identifiers, source names, and downstream integration endpoints must be configuration-driven. The repository should contain examples only.

## Conceptual pipeline

```text
Configured sources
  -> harvester
  -> artifact registry
  -> classifier
  -> signal extractor
  -> profile compiler
  -> exporters
  -> downstream consumers
```

## Key concepts

### Artifact

A discrete unit of source material: a sent message, email, article, transcript segment, document section, commit note, or conversation turn.

### Speaker attribution

The identity confidence that an artifact was authored or spoken by the profile subject.

### Assistance risk

A classification indicating whether the artifact is human-originated, human-directed AI-assisted, AI-originated, copied/forwarded, quoted, template-generated, or unknown.

### Signal

A structured observation extracted from artifacts. Examples: lexical pattern, rhetorical move, reasoning pattern, structural pattern, humor pattern, anti-pattern.

### Expression profile

A compiled JSON/YAML object describing identity, voice, expression, reasoning, source weighting, anti-patterns, and platform-specific guidance.

## Success criteria

### Technical

- Runs with no private infrastructure using local file fixtures.
- Can be pointed at private resources through ignored config.
- Produces deterministic profile JSON for the same input corpus and model settings where possible.
- Keeps raw private artifacts out of generated public artifacts by default.
- Supports source weighting by signal dimension.
- Supports explicit exclusion and quarantine rules.
- Provides schema validation and profile diffing.

### Product

- A new user can understand the project in under five minutes.
- A user can run a sample profile build without credentials.
- A user can connect their own sources through documented adapters.
- A downstream system can consume a profile without understanding the original corpus.

### Security and privacy

- No secrets committed.
- No private corpus committed.
- No personal identifiers required in code.
- No source-specific assumptions embedded in core logic.
- Redaction and provenance are first-class.

## Project rename strategy

Current repository name: `voice-forge`.

Recommended public product name: `imprint`.

Migration path:

1. Keep repo path stable during planning.
2. Update docs, package metadata, CLI naming, and schema names to `imprint`.
3. Rename repository only after the public-safe baseline is complete.
4. Preserve historical notes that `voice-forge` was the internal predecessor.

## Recommended MVP

1. Local file source adapter for Markdown, JSONL, and plain text.
2. Artifact schema.
3. Classification schema.
4. Manual source weighting rules.
5. Basic signal extraction using configurable LLM provider.
6. Profile compiler.
7. JSON/YAML exporter.
8. Example synthetic corpus.
9. Privacy and public-build guardrails.
10. Mosvera-compatible export adapter.
