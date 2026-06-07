# Imprint

> Public-first identity and expression profile compiler.

Imprint analyzes human-authored artifacts such as writing, messages, transcripts, notes, and documents, then compiles structured expression profiles that downstream systems can use without reading the raw private corpus.

## Status

🚧 **Pre-release / active design**

Imprint is currently in architecture and schema planning. The repository is public-first by design, but the project is not yet ready for production use.

Current focus:

1. Schema and model-provider foundation complete
2. Preparing Sprint 03: local-only ingestion adapters
3. Keeping all examples synthetic and all private corpora out of git

## What Imprint is

Imprint turns evidence into reusable profiles:

```text
configured sources
  -> harvest
  -> classify
  -> extract signals
  -> compile profile
  -> export contracts
```

It is designed to produce evidence-backed expression profiles that can support:

- writing tools,
- publishing systems,
- agent personas,
- aesthetic/identity packs,
- profile comparison,
- drift analysis,
- and first-run “What Imprint Learned” reports.

## What Imprint is not

Imprint is not:

- a memory system,
- a data lake,
- a publishing platform,
- a model router,
- a voice-cloning service,
- a digital twin,
- a personality test,
- or a diagnostic system.

Imprint observes expression patterns. It does not diagnose people or infer mental health states.

## Core principles

- **Profile + Artifact:** a profile describes patterns; an artifact uses those patterns.
- **Evidence first:** every claim should answer “why do we believe this?”
- **Confidence is not truth:** confidence describes support strength, not certainty about a person.
- **Store less than you can:** durable signals matter more than maximal capture.
- **Local-first:** private corpora should remain under user control by default.
- **Public-safe:** examples, tests, and docs use synthetic data only.

## Start here

- `docs/README.md` — documentation map
- `docs/PROJECT_STRATEGY.md` — project strategy
- `docs/PRODUCT_POSITIONING.md` — what Imprint is and is not
- `docs/PROFILE_THEORY.md` — expression profile theory and claim boundaries
- `docs/SCHEMA.md` — canonical schema overview
- `docs/MODEL_PROVIDER_POLICY.md` — BYOM/BYOP model policy
- `docs/PRIVACY_AND_LOCAL_MODE.md` — privacy and local-first posture
- `docs/sprints/SPRINT_03.md` — next sprint

## Privacy stance

This repository is designed to be public from the beginning. Real corpora, secrets, local configs, generated private profiles, and private exports must stay out of git.

Use:

- `.env.example`
- `imprint.config.example.yaml`
- synthetic examples only

Never commit:

- `.env`
- `imprint.config.yaml`
- real messages
- real emails
- real transcripts
- real profile exports
- private database dumps

Raw local research and private notes belong under `private/`, which is ignored by git.

## License

MIT. See `LICENSE`.
