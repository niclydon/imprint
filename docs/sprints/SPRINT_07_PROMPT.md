# Sprint 07 Prompt - Export Contracts and First-Run Experience

Use this prompt with GPT 5.5 for design first. Use GPT 5.4 for implementation after the design is clear.

---

You are implementing Sprint 07 for Imprint.

Sprint 07 builds the public-safe export layer for compiled profiles. It must make compiled profiles usable without weakening any upstream safety boundary.

Read:

- `docs/sprints/SPRINT_07.md`
- `docs/SPRINT_06_ARCHITECTURE_REVIEW.md`
- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/DERIVED_PROFILE_MODEL.md`
- `src/imprint/compiler/`
- `src/imprint/signals/`
- `src/imprint/schemas/`
- tests

Implement public-safe exports for compiled profiles:

1. canonical JSON export
2. human-readable Markdown export
3. first-run “What Imprint Learned” output
4. Mosvera expression overlay contract/export skeleton

Do not implement:

- LLM calls
- remote APIs
- prompt generation for writing systems
- image generation
- publishing workflows
- Broadside integration
- Mosvera runtime behavior
- web UI
- demo article generation
- raw evidence export by default

Critical constraints:

- no raw artifact text in public-safe exports
- no filesystem paths
- source IDs remain opaque
- prohibited claims cannot export
- bounded interpretations remain policy-gated
- quarantined/non-durable signals cannot become durable evidence
- incompatible signal model versions cannot be silently treated as comparable
- first-run output must be generated from compiled profile data, not raw artifacts
- Mosvera overlay must contain expression summaries and constraints only, not provider prompts or raw evidence

Create/update docs:

- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`

Add tests proving export safety, determinism, and boundary preservation.

Run tests before finishing.

At the end, summarize:

- files changed
- tests run
- export formats implemented
- safety boundaries preserved
- blockers for Sprint 08
