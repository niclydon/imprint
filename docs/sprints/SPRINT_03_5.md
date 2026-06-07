# Sprint 03.5 - Ingestion Safety Remediation

Primary Model: GPT 5.4
Adversarial Reviewer: Gemini Antigravity
Status: Required before Sprint 04 classification work

## Mission

Resolve the ingestion safety issues identified in `docs/SPRINT_03_ARCHITECTURE_REVIEW.md` before Sprint 04 classification and validation work begins.

Sprint 03 delivered the local adapter framework. Sprint 03.5 exists to tighten privacy and classification-boundary guarantees before downstream classification code consumes adapter output.

## Required Reading

Read:

- `docs/SPRINT_03_ARCHITECTURE_REVIEW.md`
- `docs/IMPLEMENTATION_DRIFT.md`
- `docs/sprints/SPRINT_03.md`
- `docs/sprints/SPRINT_04.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`
- `src/imprint/adapters/`
- `tests/test_adapters.py`

## Core Issues to Resolve

### 1. Adapter Metadata Hints Are Non-Authoritative

Adapters may provide metadata hints such as:

- `authorship_origin`
- `authorship_confidence`
- `classification_label`
- `artifact_type`

These hints must never bypass Sprint 04 classification and validation.

Required decision:

> Adapter-provided metadata is advisory source metadata, not ground truth.

Required updates:

- document this rule in `docs/ARTIFACT_STORAGE_POLICY.md` or `docs/PRIVACY_AND_LOCAL_MODE.md`
- update Sprint 04 docs/prompts so classifiers must re-assess adapter hints
- add tests or schema assertions if practical

### 2. Opaque Source IDs

Normalized artifacts must not expose full filesystem paths as exported `source_id` values.

Required behavior:

- exported/source-facing `source_id` should be opaque and stable
- full local paths may be preserved only in local/private metadata if needed for audit
- public-safe exports must not leak local filesystem paths

Required implementation:

- update normalization/source adapter behavior as needed
- add tests proving local file paths are not exposed as artifact reference source IDs

### 3. Artifact Type Hints

Adapters should provide better artifact type hints where obvious.

Examples:

- transcript JSON -> transcript segment or transcript artifact type
- markdown/text -> document unless metadata says otherwise
- jsonl -> use record-provided type only as advisory metadata if schema supports it

These remain hints, not ground truth.

### 4. Adapter Raw Content Handling

Document that local adapters may briefly read raw content into memory for hashing and normalization, but must not persist raw content when the storage policy is metadata-only.

### 5. Duplicate Handling

Document that stable artifact IDs enable downstream deduplication. Sprint 03.5 does not need full deduplication unless it is small and clean.

## Required Deliverables

Create:

- `docs/SPRINT_03_5_REMEDIATION_SUMMARY.md`

Update as needed:

- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/sprints/SPRINT_04.md`
- adapter implementation under `src/imprint/adapters/`
- adapter tests under `tests/test_adapters.py`

## Forbidden Work

Do not:

- implement classification logic
- implement signal extraction
- call LLMs
- add remote APIs
- add private connectors
- add provider-specific code
- build storage engines beyond what is needed for safe normalization

## Exit Criteria

Sprint 03.5 is complete when:

- adapter hints are documented as non-authoritative
- Sprint 04 instructions require re-assessment of adapter hints
- source IDs are opaque in normalized artifacts
- tests prove file paths do not leak through source IDs
- artifact type hints are improved where straightforward
- tests pass
- no private data or provider assumptions are introduced
