# Sprint 02.5 Adversarial Review Prompt - Model Provider Policy

Use this prompt after Sprint 02.5 completes.

---

You are a hostile principal architect reviewing Imprint's model provider and inference policy.

Read:

- `docs/sprints/SPRINT_02_5.md`
- all Sprint 02.5 outputs
- current schema docs and implementation
- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`

Your job is to determine whether Imprint has avoided provider lock-in, hidden privacy risk, and untracked model drift.

Focus on:

1. Provider neutrality
   - Does anything assume OpenAI, Anthropic, Gemini, Forge, Ollama, or another provider?

2. Model roles
   - Are classifier, extractor, validator, reporter, artifact generator, embeddings, and reranker roles distinct?

3. Durable profile risk
   - Are all profile-affecting model uses recorded in the build manifest?
   - Can model changes be separated from expression drift?

4. Experience-only generation
   - Can generated first-run artifacts accidentally mutate the profile?

5. Privacy
   - Are remote providers explicit?
   - Does the user know what data is sent where?

6. Capability contracts
   - Are capabilities specific enough to choose safe models?
   - Are they too vague to test?

Generate:

- `docs/SPRINT_02_5_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues,
- unresolved blockers,
- recommendations before Sprint 03,
- and a clear go/no-go recommendation.

Do not implement code.
