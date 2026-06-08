# Imprint

**Website:** [imprint.niclydon.dev](https://imprint.niclydon.dev)

![Imprint hero: evidence fragments converging into a structured expression profile](docs/assets/imprint-hero.png)

> Public-first identity and expression profile compiler.

Imprint analyzes human-authored artifacts such as writing, messages, transcripts, notes, and documents, then compiles structured expression profiles that downstream systems can use without reading the raw private corpus.

## Status

🚧 **Pre-release / active development**

Imprint is open-source and public-first by design, but not yet ready for production use.

Current focus:

1. Packaging and onboarding for a public developer preview
2. Public landing site at [imprint.niclydon.dev](https://imprint.niclydon.dev)
3. Keeping all examples synthetic and all private corpora out of git

## Quickstart

This path uses only the committed synthetic corpus. It does not require private services,
credentials, model providers, or network connectors.

```bash
git clone https://github.com/niclydon/imprint.git
cd imprint
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"

imprint --help
imprint connectors-dry-run --config imprint.config.example.yaml
imprint example

sed -n '1,80p' exports/synthetic-demo/what-imprint-learned.md
sed -n '1,80p' exports/synthetic-demo/profile.md
```

Expected example outputs are written under `exports/synthetic-demo/`, which is ignored by git.
The generated files include canonical JSON, Markdown, first-run summary, Mosvera expression overlay,
and human CLI consumer-contract examples.

For a fuller walkthrough, see `docs/QUICKSTART.md`.

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
- `docs/QUICKSTART.md` — copy-paste synthetic onboarding path
- `docs/INSTALL.md` — clean install and local verification
- `docs/PROJECT_STRATEGY.md` — project strategy
- `docs/PRODUCT_POSITIONING.md` — what Imprint is and is not
- `docs/PROFILE_THEORY.md` — expression profile theory and claim boundaries
- `docs/SCHEMA.md` — canonical schema overview
- `docs/EXPORT_FORMATS.md` — public-safe export contracts
- `docs/MODEL_PROVIDER_POLICY.md` — BYOM/BYOP model policy
- `docs/PRIVACY_AND_LOCAL_MODE.md` — privacy and local-first posture
- `docs/RELEASE_CHECKLIST.md` — `v0.1.0` release checklist

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
