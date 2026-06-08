# Sprint 13.5 Adversarial Review Prompt - Private Adapter Enforcement Foundation

Review Sprint 13.5 as a hostile privacy/security architect.

Read:

- `docs/SPRINT_13_ARCHITECTURE_REVIEW.md`
- `docs/SPRINT_13_5_REMEDIATION_SUMMARY.md`
- consent boundary docs/code/tests
- redaction docs/code/tests
- replay manifest docs/code/tests
- audit log docs/code/tests
- connector leakage and authority boundary tests

Focus on:

- consent bypasses
- third-party content contamination
- credential redaction failures
- replay/version ambiguity
- audit log leakage
- public/private repo leakage
- connectors gaining classifier/export/LLM authority

Generate `docs/SPRINT_13_5_ARCHITECTURE_REVIEW.md` with blockers, recommendations, and clear GO/NO-GO for private adapter implementation planning.

Do not implement code.
