# Sprint 12 Adversarial Review Prompt - Evaluation and Quality Gates

Review Sprint 12 as a hostile release/security architect.

Read Sprint 12 outputs, validation code, comparison code, release-gate docs, regression corpus, and tests.

Focus on:

- false PASS validation states
- privacy leaks that validators miss
- path or credential leakage
- profile comparison overclaiming comparability
- implementation drift presented as expression drift
- missing compatibility warnings
- release gates that are too weak
- synthetic regression corpus gaps

Generate `docs/SPRINT_12_ARCHITECTURE_REVIEW.md` with blockers, recommendations, and a clear go/no-go before Sprint 13 or v0.1.0.

Do not implement code.
