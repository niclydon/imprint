# Sprint 11 - Packaging and Install Experience

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: **Complete** — 2026-06-07 (`imprint example`, quickstart/install docs, CI, clean install smoke)

## Mission

Make Imprint usable by a stranger as a public developer preview.

Sprint 11 is not a feature sprint. It is a packaging, onboarding, and release-readiness sprint. The core architecture exists; this sprint makes the repo installable, runnable, understandable, and safe for someone who is not the project author.

## Required Reading

Read before making changes:

- `README.md`
- `docs/README.md`
- `docs/ROADMAP.md`
- `docs/CONFIGURATION.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md`
- `docs/sprints/SPRINT_10.md`
- `pyproject.toml`
- `.env.example`
- `imprint.config.example.yaml`
- `src/imprint/cli.py`
- `tests/`

## Core Goal

A new user should be able to:

1. clone the repository,
2. install Imprint in a clean environment,
3. run the synthetic example,
4. generate a profile/export without credentials,
5. understand what happened,
6. and know what is safe/not safe to configure next.

## Required Deliverables

### 1. Clean install path

Verify and document a clean install path.

Expected options:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

or an equivalent modern package-manager flow if the repo uses one.

The install path must not require private services, model providers, credentials, or homelab infrastructure.

### 2. README quickstart

Update the README with a copy-paste quickstart that runs against synthetic data only.

The quickstart should include:

- clone
- install
- run tests or smoke check
- initialize/sample config if available
- run synthetic connector/adapters
- produce at least one public-safe export
- inspect output

### 3. CLI onboarding

Improve CLI help and onboarding where needed.

Potential commands:

- `imprint --help`
- `imprint init`
- `imprint connectors-dry-run`
- `imprint export`
- `imprint demo` or `imprint example` if useful and scoped

Do not add broad new behavior. Prefer wiring existing pipeline pieces into a safe synthetic demo path.

### 4. Synthetic sample project

Provide a clear synthetic sample corpus/project.

It should include:

- sample input artifacts
- sample config
- expected output location
- documented command sequence
- no real names, private content, accounts, paths, tokens, or source IDs

### 5. Generated example outputs

Include or document generated example outputs if safe and deterministic.

Potential outputs:

- canonical JSON export
- Markdown profile summary
- first-run “What Imprint Learned” output
- Mosvera expression overlay fragment
- consumer contract examples

All outputs must be synthetic and public-safe.

### 6. CI / release hygiene

Add or verify:

- GitHub Actions test workflow if absent
- Python version compatibility
- test command
- package metadata
- license metadata
- project URLs
- basic lint/type command if already supported
- release checklist for `v0.1.0`

Do not add heavy tooling unless it is clearly worth it.

### 7. Public safety scan

Verify:

- no private corpus files are tracked
- no `.env` or local config files are tracked
- no credentials, DSNs, hostnames, or account IDs are included
- ignored private paths still work
- synthetic JSONL fixtures are intentionally allowed if needed

## Non-Goals

Do not implement:

- real private connectors
- Gmail/iMessage/Plaud/Looki/database adapters
- service/API mode
- web UI
- LLM extraction
- remote provider calls
- publishing workflows
- Mosvera runtime integration
- Broadside API integration
- profile editor
- private source storage engine

## Test Requirements

Add tests or smoke checks proving:

- package imports work after install
- CLI help works
- synthetic config validates
- synthetic connector dry-run works
- synthetic pipeline can produce public-safe output if scoped
- outputs contain no raw private text or paths
- no credentials are required

## Documentation Requirements

Create or update:

- `README.md`
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/CONFIGURATION.md`
- `docs/README.md`
- `.env.example`
- `imprint.config.example.yaml`

## Exit Criteria

Sprint 11 is complete only if:

- a new user can install Imprint locally
- the README quickstart works copy-paste
- the synthetic example requires no private infrastructure
- at least one public-safe export path is documented and tested
- package metadata is credible for public developer preview
- CI or documented test command is clear
- release checklist exists
- all tests pass

At the end, summarize:

- install command verified
- quickstart commands verified
- files changed
- tests run
- remaining blockers for `v0.1.0`
