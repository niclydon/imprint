# Sprint 11 Architecture Review: Packaging and Install Experience

**Reviewer:** Codex acting as hostile principal architect
**Status:** Post-implementation gate review
**Context:** Evaluation of Sprint 11 against stranger installability, synthetic demo integrity, CLI
usability, packaging quality, public safety, CI, and release-readiness.

## Executive Summary

Sprint 11 makes Imprint runnable as a public developer preview. A new user can clone the repo,
install the package in a clean virtual environment, inspect CLI help, dry-run synthetic connectors,
generate public-safe example exports, and read quickstart/install documentation without private
services or credentials.

**Verdict: GO for Sprint 12 evaluation and quality gates.**

The sprint does not add real private connectors, live APIs, OAuth, service mode, LLM calls, remote
provider calls, publishing workflows, Mosvera runtime integration, Broadside API integration, or
private corpus assumptions.

## Review Scope

Reviewed:

- `README.md`
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/CONFIGURATION.md`
- `docs/README.md`
- `pyproject.toml`
- `.env.example`
- `imprint.config.example.yaml`
- `.github/workflows/tests.yml`
- `examples/README.md`
- `examples/synthetic_corpus/`
- `src/imprint/cli.py`
- `tests/test_onboarding.py`
- connector, export, and full test-suite output
- clean temp-venv install and CLI smoke output
- tracked-file public-safety scan

## Findings

### 1. Stranger Installability

**Status: PASS**

`README.md`, `docs/QUICKSTART.md`, and `docs/INSTALL.md` document a copy-paste editable install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

The install path was verified in a temporary virtual environment. Package import, `imprint --help`,
connector dry-run, and the synthetic example command all worked after install.

### 2. Synthetic Demo Integrity

**Status: PASS**

`imprint example` uses `examples/synthetic_corpus/transcript/synthetic-demo.json`, a committed
synthetic transcript with speaker metadata. It generated:

- `profile.imprint.json`
- `profile.md`
- `what-imprint-learned.md`
- `mosvera.expression.json`
- `human-cli.consumer.json`

The command produced 3 artifacts, 6 candidate signals, and 4 compiled profile signals. Generated
outputs were checked for raw synthetic transcript text, source file names, source paths, and private
credential markers.

### 3. CLI Usability

**Status: PASS**

The CLI now exposes a clear onboarding command:

```bash
imprint example
```

The command writes deterministic public-safe exports to ignored `exports/synthetic-demo/` by default
and prints only counts plus output filenames. It does not print corpus paths.

### 4. Packaging Quality

**Status: PASS**

`pyproject.toml` now includes developer-preview metadata, Python `>=3.12`, MIT license metadata,
project URLs, classifiers, keywords, and the existing `imprint` console script. Dependencies remain
small and aligned with current code.

### 5. Public Safety

**Status: PASS**

The public path requires no credentials. Optional `.env.example` model and private connector values
are commented out. `imprint.config.example.yaml` uses synthetic enabled sources and one disabled
private example. Generated exports go under ignored `exports/`.

Tracked-file scans found no committed `.env`, local config, private corpus directory, generated
exports, or credential patterns. Regex hits were limited to existing CSS `mask-*` properties.

### 6. Release Readiness

**Status: PASS WITH FOLLOW-UP**

`docs/RELEASE_CHECKLIST.md` gives a concrete `v0.1.0` checklist, and GitHub Actions now runs Python
3.12 install, compile, and test checks. This is sufficient for a developer preview.

Before tagging `v0.1.0`, run the release checklist from a fresh clone and confirm GitHub Actions is
green on the pushed commit.

## Validation Evidence

- `pytest -q` -> 100 passed
- `python3 -m compileall -q src` -> passed
- clean temp-venv `pip install -e ".[test]"` -> passed
- clean temp-venv `python -c "import imprint; print(imprint.__version__)"` -> `0.1.0`
- clean temp-venv `imprint --help` -> passed
- clean temp-venv `imprint connectors-dry-run --config imprint.config.example.yaml` -> passed
- clean temp-venv `imprint example` -> generated 5 output files, 4 profile signals
- focused onboarding/export/connector tests -> passed
- tracked-file safety scan -> no private data or credential-pattern hits

## Resolved Issues

1. Added copy-paste README and docs quickstart.
2. Added clean install documentation.
3. Added `imprint example` for deterministic synthetic public-safe exports.
4. Added synthetic transcript input with enough metadata to exercise inclusion and compilation.
5. Added onboarding tests for import, CLI help, config validation, and generated outputs.
6. Added GitHub Actions test workflow.
7. Added package metadata and project URLs.
8. Commented optional credential-like values in `.env.example`.

## Unresolved Blockers

None for Sprint 12.

Release tagging still requires running the checklist from a fresh clone and confirming CI is green on
the pushed commit.

## Recommendations Before `v0.1.0`

1. Run `docs/RELEASE_CHECKLIST.md` from a fresh clone.
2. Confirm GitHub Actions passes on `main`.
3. Decide whether to publish generated synthetic example outputs as release artifacts rather than
   committed files.
4. Add a `validate-export` command in Sprint 12 to formalize public-safety checks for generated
   files.

## Gate Decision

**GO.**

Sprint 11 satisfies the install, quickstart, synthetic demo, package metadata, CI, public-safety, and
release-readiness requirements for a public developer preview.
