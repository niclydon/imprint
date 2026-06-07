# Sprint 08 Adversarial Review Prompt - Consumer Contracts

Use this prompt after Sprint 08 completes.

---

You are a hostile principal architect reviewing Sprint 08 consumer contract work.

Read:

- all Sprint 08 outputs
- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/MOSVERA_INTEGRATION.md`
- `docs/BROADSIDE_INTEGRATION.md`
- `docs/AGENT_CONSUMER_CONTRACT.md`
- consumer code under `src/imprint/consumers/` if present
- export code under `src/imprint/exports/`
- tests

Focus on:

1. Boundary preservation
   - Did Sprint 08 avoid building real downstream integrations?
   - Did prompt assembly, publishing workflows, and runtime adapter behavior stay outside core Imprint?

2. Mosvera boundary
   - Is Mosvera still aesthetic intent/runtime only?
   - Does Imprint only provide expression overlays?

3. Broadside boundary
   - Does Imprint avoid platform publishing logic and editorial workflows?

4. Agent safety
   - Do agent contracts preserve warnings, limitations, no-raw-text policy, and confidence caveats?

5. Version compatibility
   - Are classifier/compiler/signal warnings visible in consumer-facing projections?

6. Privacy
   - Do consumer payloads avoid raw text, paths, private locators, and source leakage?

Generate:

- `docs/SPRINT_08_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 09/10
- clear go/no-go decision

Do not implement code.
