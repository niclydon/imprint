# Sprint 12.5 Prompt - Quality Gate Hardening

Use this prompt with GPT 5.4 for implementation after reading the Sprint 12 review. Use GPT 5.5 or Gemini for adversarial re-review.

You are implementing Sprint 12.5 for Imprint.

Sprint 12 produced validation, comparison, and release-gate infrastructure, but the adversarial review found blockers. Fix those blockers before Sprint 13 or v0.1.0 release work proceeds.

Read:

- `docs/sprints/SPRINT_12_5.md`
- `docs/SPRINT_12_ARCHITECTURE_REVIEW.md`
- `src/imprint/quality.py`
- `src/imprint/exports/safety.py`
- `tests/test_quality_gates.py`
- `tests/test_exports.py`

Required fixes:

1. Detect JWT-shaped credentials.
2. Detect base64/base64url-encoded credentials.
3. Detect percent-encoded filesystem paths.
4. Reject root-level underscore-prefixed private metadata fields.
5. Add regression coverage for mixed classifier-version comparisons.
6. Create `docs/SPRINT_12_5_REMEDIATION_SUMMARY.md`.

Keep the implementation conservative and fail-closed. Prefer shared helpers over duplicated regexes.

Do not implement private adapters, service mode, LLM judges, web UI, or broad schema redesign.

Run the full test suite before finishing.

At the end, summarize files changed, tests run, blockers fixed, and any remaining release risks.
