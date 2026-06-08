# Sprint 12 Prompt - Evaluation, Validation, and Quality Gates

Use this prompt with GPT 5.5 for design. Use GPT 5.4 for implementation after the plan is clear.

You are implementing Sprint 12 for Imprint.

The installable developer preview exists. Your task is to add validation, comparison, regression, and release gates so profiles and exports can be trusted.

Read:

- `docs/sprints/SPRINT_12.md`
- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/RELEASE_CHECKLIST.md`
- compiler, export, consumer, connector code
- tests

Implement or document:

- `imprint validate-export <file>`
- `imprint diff profile-a.json profile-b.json`
- comparability states
- synthetic regression corpus
- validation report format
- release-gate checks
- drift category detection

Do not add:

- LLM judges
- human review workflows
- private adapters
- publishing workflows
- service/API mode
- web UI

Public safety requirements:

- raw text leakage fails validation
- source path leakage fails validation
- credential-pattern leakage fails validation
- missing compatibility metadata fails validation where required
- prohibited claims fail validation

Run tests before finishing.

Summarize files changed, commands added, tests run, and blockers before v0.1.0.
