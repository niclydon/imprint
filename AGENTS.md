# Agent Guide for Imprint

This is the canonical handoff document for AI coding agents working in this repository.

## What Imprint is

Imprint is an open-source, local-first expression profile compiler. It ingests artifacts, classifies authorship and inclusion safety, extracts evidence-backed expression signals, compiles versioned profiles, and exports public-safe contracts for downstream systems.

## What Imprint is not

Imprint is not a memory system, data lake, writing assistant, publishing platform, model router, Mosvera runtime, Broadside runtime, digital twin, personality test, or SaaS service.

## Architecture map

Read `REPO_MAP.md` before changing code.

Pipeline:

1. connectors discover configured sources
2. adapters normalize artifacts
3. classification decides authorship, inclusion, quarantine, and exclusion
4. signal extraction emits artifact-level observations
5. compiler aggregates durable signals into expression profiles
6. exporters produce public-safe JSON, Markdown, first-run, and overlay contracts
7. consumers project canonical JSON for Mosvera, Broadside, agents/apps, and CLI/human inspection
8. quality gates validate exports, comparison, drift, and release safety
9. service mode, if used, serves public-safe contracts only

## Safe first commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
python3 -m pytest -q
imprint --help
imprint example
```

Validation commands:

```bash
imprint validate-export exports/synthetic-demo/profile.imprint.json
imprint diff exports/synthetic-demo/profile.imprint.json exports/synthetic-demo/profile.imprint.json
```

## Required reading before substantial changes

- `README.md`
- `docs/ROADMAP.md`
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/sprints/`
- latest relevant `docs/SPRINT_*_ARCHITECTURE_REVIEW.md`

## Hard boundaries

Do not introduce:

- real private data
- real source paths
- credentials, DSNs, tokens, account IDs, private URLs
- raw text in public-safe exports
- hidden model/provider calls
- prompt assembly inside core Imprint
- Mosvera or Broadside runtime behavior inside core Imprint
- private connector implementations without threat models and synthetic fixtures

## Test expectations

Run the full test suite before finishing:

```bash
python3 -m pytest -q
```

For packaging or release-related changes, also verify:

```bash
python3 -m compileall -q src
imprint example
```

## Sprint work

Sprint plans and prompts live in `docs/sprints/`. Follow the active sprint prompt exactly. If an adversarial review identifies blockers, create a remediation sprint before continuing.

## Commit hygiene

Keep commits scoped. Do not mix private infrastructure changes with public docs/code. Do not commit generated private outputs.
