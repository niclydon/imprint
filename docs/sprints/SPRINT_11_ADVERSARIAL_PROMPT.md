# Sprint 11 Adversarial Review Prompt - Packaging and Install Experience

Use this prompt after Sprint 11 completes.

---

You are a hostile principal architect reviewing Sprint 11 packaging and install experience.

Read:

- `README.md`
- `docs/QUICKSTART.md`
- `docs/INSTALL.md`
- `docs/RELEASE_CHECKLIST.md`
- `pyproject.toml`
- `.env.example`
- `imprint.config.example.yaml`
- CLI implementation
- tests and CI workflow

Focus on:

1. Stranger installability
   - Can a new user clone, install, and run without private infrastructure?
   - Are commands copy-pasteable?

2. Synthetic demo integrity
   - Are examples synthetic?
   - Do outputs avoid private text, paths, credentials, and account details?

3. CLI usability
   - Is help clear?
   - Is the quickstart path discoverable?

4. Packaging quality
   - Is package metadata credible?
   - Are dependencies reasonable?
   - Is the supported Python version clear?

5. Public safety
   - Are `.env`, private configs, generated private outputs, and raw corpora ignored?
   - Did any private assumptions leak into examples/docs?

6. Release readiness
   - Is there a real v0.1.0 checklist?
   - Are tests/CI adequate for a developer preview?

Generate:

- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before v0.1.0 or Sprint 12
- clear go/no-go decision

Do not implement code.
