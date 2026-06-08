# Release Checklist

Status: Sprint 12.5 `v0.1.0` developer-preview checklist

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
- [ ] `imprint diff` reports structured `release_gate.reason_codes` and no required reviews for identical synthetic exports.
- [ ] README and `docs/QUICKSTART.md` commands work copy-paste from the repository root.

## Test and CI

- [ ] `pytest -q` passes.
- [ ] `python -m compileall -q src` passes.
- [ ] Sprint 12 quality-gate tests pass.
- [ ] Sprint 12.5 credential/path/private-metadata regression tests pass.
- [ ] Mixed classifier-version comparison regression tests pass and produce `release_gate.status: WARN`.
- [ ] GitHub Actions runs tests on push and pull request.
- [ ] CI uses only committed synthetic fixtures and public configuration.

## Public Safety

- [ ] No `.env`, `imprint.config.yaml`, private corpora, generated private exports, database dumps, or local profiles are tracked.
- [ ] Public examples are synthetic.
- [ ] Generated public-safe exports contain no raw artifact text, filesystem paths, provider prompts, credentials, DSNs, account IDs, or private source IDs.
- [ ] Generated public-safe exports contain no JWT credentials, base64/base64url-encoded credentials, percent-encoded paths, or underscore-prefixed metadata.
- [ ] `validate-export` fails intentionally mutated raw-text, path, encoded-path, credential, encoded-credential, source-ID, private-metadata, and compatibility regressions.
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
- [ ] `docs/SPRINT_12_5_REMEDIATION_SUMMARY.md` summarizes fixed blockers and verification.
- [ ] `docs/SPRINT_12_5_ARCHITECTURE_REVIEW.md` has a GO decision for Sprint 13/v0.1.0 planning.

## Release Decision

`v0.1.0` is ready only when the package can be installed, tested, and run against synthetic data by a
new user without private infrastructure or credentials, and Sprint 12.5 hardened validation has
produced a GO decision.
