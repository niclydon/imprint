# Sprint 07 Adversarial Review Prompt - Exports and First-Run Experience

Use this prompt after Sprint 07 completes.

---

You are a hostile principal architect reviewing Sprint 07 export and first-run experience work.

Read:

- all Sprint 07 outputs
- `docs/SPRINT_06_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/FIRST_RUN_OUTPUT.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/EXPORT_BOUNDARIES.md`
- export code under `src/imprint/exports/`
- compiler code under `src/imprint/compiler/`
- tests

Your job is to determine whether Sprint 08 downstream integrations can safely begin.

Focus on:

1. Export safety
   - Do JSON/Markdown/first-run exports leak raw text, paths, or private locators?
   - Are source IDs opaque?

2. Claim boundaries
   - Did profile exports preserve expression-pattern-only scope?
   - Did first-run output accidentally make person-level psychological claims?

3. Version compatibility
   - Are compiler/classifier/signal model versions preserved?
   - Are incompatible versions marked or rejected?

4. First-run experience
   - Is it useful and clear without overstating certainty?
   - Does it explain limitations?

5. Mosvera boundary
   - Is the Mosvera overlay a contract/fragment only?
   - Did Imprint avoid absorbing Mosvera or emitting provider-specific aesthetic prompts?

6. Determinism and provider neutrality
   - Are there any LLMs, embeddings, remote calls, or provider-specific assumptions?

Generate:

- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 08
- clear go/no-go decision for Sprint 08

Do not implement code.
