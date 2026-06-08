# Sprint 14 Prompt - Service and Automation Planning

Use this prompt with GPT 5.5 for design. Use GPT 5.4 only after the service boundaries are clear.

You are implementing Sprint 14 for Imprint.

Design local/private service mode and automation around public-safe exports. Do not build a SaaS platform and do not expose raw corpora. Sprint 14 is optional for v0.1.0; do not start implementation until fresh-user/fresh-agent validation is complete and a service decision record justifies the need for service mode.

Read:

- `docs/sprints/SPRINT_14.md`
- `docs/EXPORT_FORMATS.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/SECURITY_PRIVACY.md`
- export, consumer, connector, and CLI code

Create the service/API design docs listed in Sprint 14. First create a service decision record explaining why service mode is needed and why CLI/file-drop mode is insufficient. Implement code only if the decision record justifies it, the design is clear, and scope remains small.

Critical constraints:

- no raw corpus exposure
- no private path exposure
- no credential exposure
- no prompt assembly
- no publishing workflows
- no LLM/provider calls
- no Mosvera/Broadside runtime adapters inside core
- batch and service outputs must be equivalent
- service mode must not be used to hide onboarding/docs gaps

Run tests before finishing.

Summarize files changed, tests run, service boundaries, and blockers before implementation or release.
