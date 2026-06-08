# Sprint 13.5 Prompt - Private Adapter Enforcement Foundation

Use this prompt with GPT 5.4 for implementation after reading the Sprint 13 review. Use GPT 5.5 or Gemini for adversarial re-review.

You are implementing Sprint 13.5 for Imprint.

Sprint 13 produced private-adapter threat models, but the adversarial review found enforcement gaps. Close those gaps before any real private adapter implementation begins.

Read:

- `docs/sprints/SPRINT_13_5.md`
- `docs/SPRINT_13_ARCHITECTURE_REVIEW.md`
- connector framework docs and code
- adapter/classification tests

Required work:

1. Define enforceable consent boundary model.
2. Expand redaction for real-world credentials.
3. Define connector replay manifest.
4. Define connector audit log contract.
5. Add multi-person synthetic fixture standards.
6. Add public/private repository leakage detection.
7. Add adapter authority boundary tests.
8. Create `docs/SPRINT_13_5_REMEDIATION_SUMMARY.md`.

Do not build real private adapters or live API integrations.

Run tests before finishing.

Summarize files changed, tests run, gaps fixed, and remaining blockers before Gmail/iMessage/database/transcript adapter work.
