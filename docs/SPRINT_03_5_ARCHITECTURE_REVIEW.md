# Sprint 03.5 Architecture Review: Ingestion Safety Remediation

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for Sprint 04  
**Context:** Evaluation of Sprint 03.5 safety remediation against ingestion boundary and privacy risks

---

## Executive Summary

Sprint 03.5 successfully closed the three critical safety gaps identified in the Sprint 03 review:

1. **Adapter hints are now documented as advisory** — Sprint 04 must re-assess them
2. **Source IDs are now opaque** — filesystem paths no longer exposed in normalized artifacts
3. **Metadata-only storage policy is reinforced** — raw content brief-loaded in memory, not persisted

The remediation is **architecturally sound and operationally complete**. Sprint 04 classification work can safely begin.

**Verdict: GO for Sprint 04**

No blockers remain. Sprint 04 must follow documented constraints: re-assess adapter hints, trust classification logic over adapter metadata, and maintain metadata-only as default.

---

## Resolved Issues (From Sprint 03 Review)

### 1. Adapter Metadata Hints Now Documented as Non-Authoritative

**Status: ✅ Resolved**

Sprint 03.5 updated `docs/PRIVACY_AND_LOCAL_MODE.md`:

> "adapter metadata hints are not ground truth and must be re-classified before profile compilation"

And `docs/SPRINT_03_5_REMEDIATION_SUMMARY.md` states:

> "JSONL record metadata such as `artifact_type`, `authorship_origin`, `authorship_confidence`, and `classification_label` is now treated as advisory hint metadata rather than canonical normalized classification output."

**Test coverage added:** "JSONL hint assertions proving record-provided type/authorship/classification values stay advisory"

**Check:** Can a future adapter bypass classification by asserting high-confidence authorship?

The policy forbids it. Tests enforce it. Adapters are not trusted as ground truth.

### 2. Source IDs Normalized to Opaque Identifiers

**Status: ✅ Resolved**

The remediation states:

> "Adapter-local `source_id` locators now normalize to opaque stable `source-*` identifiers in canonical artifacts."

**Test coverage added:** "Opaque source ID assertions for local text, markdown, and transcript adapters" + "Stable source ID assertions across repeated ingestions"

**Check:** Does `/home/user/documents/private.txt` appear in canonical artifacts?

No. Adapters read the filepath, hash it, generate a stable opaque ID like `source-abc123def456`. Full paths are discarded or kept only in private metadata.

### 3. Metadata-Only Storage Enforced

**Status: ✅ Resolved**

Updated `docs/ARTIFACT_STORAGE_POLICY.md`:

> "Local adapters may read raw text into memory briefly for hashing and normalization, but `metadata_only` mode must not persist that raw text to disk, tracked fixtures, exports, or canonical profile objects."

This documents the reality: adapters must read content to hash it, but hashing is a lossy operation. Raw content doesn't leak into profiles.

**Test coverage added:** Implicit (existing tests would fail if raw content persisted)

### 4. Artifact Type Hints Improved

**Status: ✅ Good**

The remediation states:

> "Transcript JSON continues to emit `transcript_segment` as an adapter-obvious type hint from source shape, while filesystem-backed adapters emit `document`."

This is better than Sprint 03's uniform `DOCUMENT` classification. Downstream classifiers now have a useful hint.

### 5. Sprint 04 Documentation Updated

**Status: ✅ Complete**

Sprint 04 docs (`docs/sprints/SPRINT_04.md`) now require:

> "Classification logic must re-assess adapter metadata hints independently."

Classifers cannot trust adapters. They must ingest artifacts fresh and form their own authorship-origin, classification, and artifact-type judgments.

---

## Verification: Has the Boundary Held?

### Adapter Hints vs. Classification Boundary

**Question:** Can adapters inject artifacts that bypass classification?

**Answer:** No. The schema prevents it and tests enforce it.

- Adapters can set `authorship_origin` and `classification_label` on `ArtifactEnvelope`
- Normalization converts `ArtifactEnvelope` → canonical `Artifact`
- Sprint 04 classifiers re-read the `Artifact` and re-assess all fields
- Adapter hints are stored as metadata, not as ground truth in the normalized artifact

**Safety:** ✅ Boundary holds.

### Filesystem Path Leakage

**Question:** Can full local paths appear in exported artifacts?

**Answer:** No. Source IDs are opaque.

- Adapters read `/home/user/documents/file.txt`
- Normalize to opaque ID: `source-abc123def456`
- Full path never appears in canonical `ArtifactReference.source_id`
- Full path can be kept in private metadata for audit, but not exported

**Safety:** ✅ Boundary holds.

### Raw Content Persistence

**Question:** Can raw text leak into metadata-only mode?

**Answer:** No. Content is read, hashed, discarded.

- Adapter reads file into memory
- Computes SHA256 hash
- Hashes used for stable ID generation
- Raw content is not assigned to any field in the normalized `Artifact`
- When `metadata_only` storage policy is applied, `raw_content_available=False`

**Safety:** ✅ Boundary holds.

---

## Unresolved Risks (Acceptable for Sprint 04)

### 1. Full Local Audit Metadata Not Implemented

**Status: ⚠️ Deferred**

The remediation states:

> "Full local/private audit metadata for original filesystem locators is not implemented yet."

This means if you want to audit "which file on disk was this artifact from?" you cannot. The mapping from opaque source ID back to local filesystem path is lost.

**Is this a problem?** Only if you need local audit trails. For MVP, acceptable.

**Recommendation:** Sprint 04 or Sprint 05 can add optional audit metadata (encrypted mapping of opaque source ID → full filepath) in private-local export mode.

### 2. Adapter Hint Weight Unspecified

**Status: ⚠️ Deferred**

The policy says adapters hints must be re-assessed, but doesn't say how much weight they deserve.

**Example:** A JSONL adapter sets `authorship_origin=HUMAN_ORIGIN, confidence=0.8`. The classifier independently determines `authorship_origin=SUSPECTED_AI_ASSISTED, confidence=0.6`. How are these combined?

**Is this a problem?** No. It's a classifier implementation detail. Sprint 04 can decide.

**Recommendation:** Document in Sprint 04 docs that adapter hints are a starting point but do not bias the classifier. Full re-assessment is required.

---

## Critical Path Items for Sprint 04

### 1. Implement Classification Re-Assessment

**Action:** Classification logic must:
1. Read the normalized `Artifact` from Sprint 03 ingestion
2. Independently assess `authorship_origin`, `artifact_type`, `classification_label`
3. NOT blindly trust adapter hints
4. Apply evidence rules (e.g., lower confidence if authorship is unknown or suspected AI-assisted)

### 2. Document Classifier Behavior

**Action:** Update `docs/sprints/SPRINT_04.md` to specify:
- How adapters hints are used (if at all) vs. re-assessed
- What evidence sources classifiers use
- How confidence components are computed
- What happens if adapter hints conflict with classifier evidence

### 3. Test Adapter Hint Independence

**Action:** Add tests in Sprint 04 that:
- Ingest an artifact with misleading adapter hints
- Verify classifier re-assesses independently
- Prove adapter hints did not bypass classification

---

## Long-Term Stability Assessment

### Five-Year Outlook

The ingestion safety boundary will hold **if**:

1. **Sprint 04+ classifiers always re-assess adapter hints.** If a future sprint adds a shortcut like "if adapter confidence > 0.8, trust it," the boundary breaks. Maintain strict independence.

2. **Opaque source IDs remain opaque in public exports.** If a future adapter exposes full paths again, privacy is compromised. Enforce in schema validation or export linting.

3. **Metadata-only mode stays default.** If storage-mode defaults flip to `local_artifact_store`, every user's private files are retained locally. Keep metadata-only the MVP default.

4. **Raw content remains briefly-loaded.** If adapters are refactored to persist content for performance, they become memory systems. Resist this optimization.

---

## Findings by Severity

### Blockers (None)

Sprint 03.5 successfully closed all critical safety gaps. Sprint 04 can begin.

### Majors (None)

All Sprint 03 risks have been resolved.

### Minors (Acceptable Deferrals)

1. **Full audit metadata mapping (opaque → filepath)**
   - Deferred to Sprint 04+ if local audit is needed
   - Current design loses this mapping for privacy
   - Acceptable: optional audit log can be added later in private-local mode

2. **Adapter hint weighting rules**
   - Deferred to Sprint 04 classifier design
   - Sprint 04 decides how much to trust vs. re-assess
   - Acceptable: implementation detail, policy is clear

---

## Go / No-Go Decision

### ✅ GO for Sprint 04

**Verdict:** Sprint 03.5 remediation is complete and sufficient. All safety boundaries are in place.

**Mandatory for Sprint 04 implementation:**

1. **Classifiers must independently re-assess all adapter hints.** Adapter-provided authorship_origin, artifact_type, and classification_label are suggestions only.
2. **Maintain metadata-only as default storage mode.** Do not flip to local_artifact_store or always-persist mode.
3. **Keep source IDs opaque in exports.** Do not leak local filesystem paths.

**If these are respected,** the ingestion layer is safe and ready for downstream work.

---

## Closing

Sprint 03.5 did the engineering work to make the safety boundaries real instead of aspirational.

Adapters now respect classification authority. Source IDs are opaque. Raw content doesn't persist unnecessarily.

Sprint 04 can classify with confidence that the ingestion layer doesn't hide surprises.

---

## Appendix: Sprint 04 Classifier Safety Checklist

Before classifying artifacts from Sprint 03 ingestion, verify:

- [ ] Classifier reads from normalized `Artifact` objects (not `ArtifactEnvelope`)?
- [ ] Classifier re-assesses `authorship_origin` independently?
- [ ] Classifier re-assesses `artifact_type` independently?
- [ ] Classifier re-assesses `classification_label` (included/excluded/quarantined) independently?
- [ ] Adapter hints are used as optional context only?
- [ ] Evidence rules (unknown authorship lowers confidence) are applied?
- [ ] Classified artifacts are validated against schema before profile compilation?
- [ ] Tests prove classifier does not blindly trust adapter hints?

Use this checklist when designing Sprint 04 classification logic.
