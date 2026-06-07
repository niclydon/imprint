# Sprint 03.5 Prompt - Ingestion Safety Remediation

Use this prompt with GPT 5.4 from the repository root.

---

You are implementing Sprint 03.5 for Imprint.

Sprint 03 local ingestion is complete. Before Sprint 04 classification begins, resolve the ingestion safety issues identified by the adversarial review.

Read:

- `docs/sprints/SPRINT_03_5.md`
- `docs/SPRINT_03_ARCHITECTURE_REVIEW.md`
- `docs/IMPLEMENTATION_DRIFT.md`
- `docs/sprints/SPRINT_04.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`
- `src/imprint/adapters/`
- `tests/test_adapters.py`

Your tasks:

1. Document that adapter metadata hints are non-authoritative.
2. Update Sprint 04 docs/prompts so classification must re-assess adapter hints.
3. Ensure normalized artifact `source_id` values are opaque and do not expose full filesystem paths.
4. Preserve local paths only in local/private metadata if needed.
5. Add or update tests proving file paths do not leak into exported/source-facing IDs.
6. Improve artifact type hints where obvious, especially transcript JSON.
7. Create `docs/SPRINT_03_5_REMEDIATION_SUMMARY.md`.

Do not implement classification.
Do not implement signal extraction.
Do not call LLMs.
Do not add remote APIs.
Do not add private connectors.
Do not hard-code provider assumptions.

Run tests before finishing.

At the end, summarize:

- files changed
- tests run
- remaining risks
- whether Sprint 04 can begin
