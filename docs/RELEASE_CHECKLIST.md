# Release Checklist

Status: Sprint 11 `v0.1.0` developer-preview checklist

Use this checklist before tagging or announcing a public developer-preview release.

## Package Readiness

- [ ] `pyproject.toml` has credible package metadata, license metadata, Python support, and project URLs.
- [ ] `python -m venv .venv && source .venv/bin/activate && pip install -e ".[test]"` succeeds in a clean environment.
- [ ] `python -c "import imprint; print(imprint.__version__)"` prints the intended release version.
- [ ] `imprint --help` lists the public onboarding commands.

## Synthetic Quickstart

- [ ] `imprint connectors-dry-run --config imprint.config.example.yaml` runs without credentials.
- [ ] `imprint example` writes public-safe outputs under `exports/synthetic-demo/`.
- [ ] `imprint export-profile --source-type local_markdown --path examples/synthetic_corpus/markdown --format json` emits canonical JSON.
- [ ] README and `docs/QUICKSTART.md` commands work copy-paste from the repository root.

## Test and CI

- [ ] `pytest -q` passes.
- [ ] `python -m compileall -q src` passes.
- [ ] GitHub Actions runs tests on push and pull request.
- [ ] CI uses only committed synthetic fixtures and public configuration.

## Public Safety

- [ ] No `.env`, `imprint.config.yaml`, private corpora, generated private exports, database dumps, or local profiles are tracked.
- [ ] Public examples are synthetic.
- [ ] Generated public-safe exports contain no raw artifact text, filesystem paths, provider prompts, credentials, DSNs, account IDs, or private source IDs.
- [ ] Disabled private connector examples remain inert and optional.
- [ ] `.gitignore` keeps local private data and generated outputs out of git.

## Documentation

- [ ] `README.md` includes the copy-paste quickstart.
- [ ] `docs/QUICKSTART.md` explains the synthetic first run.
- [ ] `docs/INSTALL.md` documents the clean install path.
- [ ] `docs/CONFIGURATION.md` documents the safe default config and output behavior.
- [ ] `docs/EXPORT_FORMATS.md` documents supported export formats.
- [ ] `docs/SPRINT_11_ARCHITECTURE_REVIEW.md` has a go/no-go decision.

## Release Decision

`v0.1.0` is ready only when the package can be installed, tested, and run against synthetic data by a
new user without private infrastructure or credentials.
