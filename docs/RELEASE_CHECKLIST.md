# Release Checklist

Status: Sprint 12 `v0.1.0` developer-preview checklist

Use this checklist before tagging or announcing a public developer-preview release.

## Package Readiness

- [ ] `pyproject.toml` has credible package metadata, license metadata, Python support, and project URLs.
- [ ] `python -m venv .venv && source .venv/bin/activate && pip install -e ".[test]"` succeeds in a clean environment.
- [ ] `python -c "import imprint; print(imprint.__version__)"` prints the intended release version.
- [ ] `imprint --help` lists the public onboarding commands.

## Synthetic Quickstart

- [ ] `imprint connectors-dry-run --config imprint.config.example.yaml` runs without credentials.
- [ ] `imprint example` writes public-safe outputs under `exports/synthetic-demo/`.
- [ ] `imprint export-profile --source-type local_transcript_json --path examples/synthetic_corpus/transcript/synthetic-demo.json --format json` emits canonical JSON.
- [ ] `imprint validate-export exports/synthetic-demo/profile.imprint.json` passes.
- [ ] `imprint diff exports/synthetic-demo/profile.imprint.json exports/synthetic-demo/profile.imprint.json` reports `COMPARABLE`.
- [ ] README and `docs/QUICKSTART.md` commands work copy-paste from the repository root.

## Test and CI

- [ ] `pytest -q` passes.
- [ ] `python -m compileall -q src` passes.
- [ ] Sprint 12 quality-gate tests pass.
- [ ] GitHub Actions runs tests on push and pull request.
- [ ] CI uses only committed synthetic fixtures and public configuration.

## Public Safety

- [ ] No `.env`, `imprint.config.yaml`, private corpora, generated private exports, database dumps, or local profiles are tracked.
- [ ] Public examples are synthetic.
- [ ] Generated public-safe exports contain no raw artifact text, filesystem paths, provider prompts, credentials, DSNs, account IDs, or private source IDs.
- [ ] `validate-export` fails intentionally mutated raw-text, path, source-ID, and compatibility regressions.
- [ ] Disabled private connector examples remain inert and optional.
- [ ] `.gitignore` keeps local private data and generated outputs out of git.

## Documentation

- [ ] `README.md` includes the copy-paste quickstart.
- [ ] `docs/QUICKSTART.md` explains the synthetic first run.
- [ ] `docs/INSTALL.md` documents the clean install path.
- [ ] `docs/CONFIGURATION.md` documents the safe default config and output behavior.
- [ ] `docs/EXPORT_FORMATS.md` documents supported export formats.
- [ ] `docs/VALIDATION.md`, `docs/PROFILE_COMPARISON.md`, `docs/QUALITY_GATES.md`, and `docs/REGRESSION_CORPUS.md` document release gates.
- [ ] `docs/SPRINT_11_ARCHITECTURE_REVIEW.md` has a go/no-go decision.
- [ ] `docs/SPRINT_12_ARCHITECTURE_REVIEW.md` has a go/no-go decision.

## Release Decision

`v0.1.0` is ready only when the package can be installed, tested, and run against synthetic data by a
new user without private infrastructure or credentials.
