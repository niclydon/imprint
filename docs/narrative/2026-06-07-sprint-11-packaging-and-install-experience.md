# Sprint 11 Packaging and Install Experience

Sprint 11 turned Imprint from an implemented local compiler into a public developer preview that a
new user can install, run against synthetic data, and inspect without private infrastructure.

The sprint added a scoped `imprint example` command that compiles the committed synthetic transcript
corpus and writes public-safe exports under ignored `exports/synthetic-demo/`. The command is a thin
wrapper over the existing adapter, classifier, signal extractor, compiler, and exporter path. It does
not introduce a service mode, live APIs, model calls, private connectors, or downstream runtime
integrations.

## What changed

- README now has a copy-paste quickstart.
- `docs/QUICKSTART.md` documents the synthetic first-run path.
- `docs/INSTALL.md` documents clean editable install and local smoke checks.
- `docs/RELEASE_CHECKLIST.md` captures the `v0.1.0` developer-preview gate.
- `examples/README.md` documents the synthetic corpus.
- `imprint.config.example.yaml` includes synthetic Markdown, JSONL chat, and transcript connector
  examples.
- `.github/workflows/tests.yml` runs compile and pytest checks on Python 3.12.
- `pyproject.toml` includes public package metadata and project URLs.
- `tests/test_onboarding.py` verifies package import, CLI help, synthetic config validation, and
  public-safe example output generation.

## Validation

- `pytest -q` passed with 100 tests.
- `python3 -m compileall -q src` passed.
- Clean temp-venv install with `pip install -e ".[test]"` passed.
- `imprint --help` passed after install.
- `imprint connectors-dry-run --config imprint.config.example.yaml` discovered only synthetic
  enabled sources plus one disabled private example.
- `imprint example` generated canonical JSON, Markdown, first-run, Mosvera expression, and human CLI
  consumer outputs with 4 compiled profile signals.
- Public-safety scan found no tracked `.env`, local config, private data, generated exports, or
  credential patterns. The only regex hits were CSS `mask-*` properties in the existing web styles.

## Boundary held

The sprint kept the implementation local, deterministic, synthetic, and provider-neutral. Generated
example exports exclude raw artifact text, source paths, credentials, provider prompts, and private
source IDs.

Sprint 11 is delivered. The next track is evaluation and quality gates before broader release work.
