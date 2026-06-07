# Sprint 08 Prompt - Consumer Contracts and Integration Surfaces

Use this prompt with GPT 5.5 for design first. Use GPT 5.4 for implementation if code changes are needed.

---

You are implementing Sprint 08 for Imprint.

Sprint 08 defines downstream consumer contracts. Do not build full integrations.

Read:

- `docs/sprints/SPRINT_08.md`
- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`
- export code under `src/imprint/exports/`
- compiler code under `src/imprint/compiler/`
- tests

Create/update:

- `docs/CONSUMER_CONTRACTS.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/BROADSIDE_INTEGRATION.md`
- `docs/AGENT_CONSUMER_CONTRACT.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/EXPORT_FORMATS.md`

Implement only small deterministic contract helpers/tests if needed.

Do not implement:

- Mosvera runtime integration
- Broadside API integration
- publishing workflows
- prompt assembly
- provider-specific generation settings
- LLM calls
- remote APIs
- image generation instructions
- raw evidence export
- UI/dashboard behavior

Critical constraints:

- canonical JSON remains source of truth
- consumer-facing projections must preserve compatibility warnings
- no raw text or paths
- source IDs remain opaque
- no generation-control fields
- Mosvera consumes expression overlays only
- Broadside consumes constraints/summary only
- agents must not treat confidence as truth or bounded interpretations as facts

Run tests before finishing.

At the end, summarize:

- files changed
- tests run
- consumer contracts defined
- boundaries preserved
- blockers for Sprint 09/10
