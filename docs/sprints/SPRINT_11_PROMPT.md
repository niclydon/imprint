# Sprint 11 Prompt - Packaging and Install Experience

Use this prompt with GPT 5.5 for design first. Use GPT 5.4 for implementation after the plan is clear.

---

You are implementing Sprint 11 for Imprint.

The core architecture is already implemented. Your task is to make Imprint installable, runnable, and understandable as a public developer preview.

Read:

- `docs/sprints/SPRINT_11.md`
- `README.md`
- `docs/ROADMAP.md`
- `docs/CONFIGURATION.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/EXPORT_FORMATS.md`
- `pyproject.toml`
- `.env.example`
- `imprint.config.example.yaml`
- `src/imprint/cli.py`
- `tests/`

Do not add major product features.

Implement and document the public install/quickstart path:

1. clean local install
2. CLI help/onboarding
3. synthetic config/demo path
4. public-safe example export
5. README quickstart
6. install docs
7. release checklist
8. CI/test workflow if missing or obviously incomplete

Forbidden:

- real private connectors
- live APIs
- OAuth
- LLM calls
- remote provider calls
- service/API mode
- publishing workflows
- Mosvera runtime integration
- Broadside API integration
- private corpus assumptions

Public safety requirements:

- examples must be synthetic
- no credentials required
- no private paths or source IDs
- no raw private text in outputs
- no `.env` or local config committed

Run the full test suite before finishing.

At the end, summarize:

- install path verified
- quickstart commands verified
- outputs generated or documented
- files changed
- tests run
- blockers for v0.1.0
