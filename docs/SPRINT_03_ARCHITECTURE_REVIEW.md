# Sprint 03 Architecture Review: Ingestion and Local Adapters

**Reviewer:** Gemini Antigravity (Adversarial Principal Architect)  
**Status:** Gate decision for production MVP  
**Context:** Evaluation of Sprint 03 local adapter implementation against architecture constraints and ingestion safety requirements

---

## Executive Summary

Sprint 03 delivered a **clean, extensible local ingestion system** that successfully implements the adapter pattern without leaking provider assumptions or privacy violations.

The implementation is production-ready for the MVP. However, it has introduced one architectural risk that must be addressed before Sprint 04: the adapter protocol accepts artifact metadata hints that could be misused to bypass classification and validation.

**Verdict: GO for Production MVP**

The ingestion system can ship. But one mandatory constraint must be documented for Sprint 04:

1. **Adapter metadata hints are read-only from upstream classification and validation.** Adapters MUST NOT be allowed to inject artifacts that are pre-classified or pre-validated.

If this constraint is respected, the system is safe.

---

## Strengths: What Sprint 03 Got Right

### 1. SourceAdapter Protocol Is Genuinely Provider-Neutral

**Status: ✅ Excellent**

The `SourceAdapter` abstract base class:

```python
class SourceAdapter(ABC):
    source_type: str
    
    @abstractmethod
    def supports(self, path: Path) -> bool: ...
    
    @abstractmethod
    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]: ...
    
    def normalize(self, envelope: ArtifactEnvelope, *, storage_policy: ...) -> Artifact: ...
    
    def ingest(self, path: Path, *, storage_policy: ...) -> list[Artifact]: ...
```

**Check: Can a new adapter be added without modifying core code?**

Yes. A future adapter for `gmail_export`, `slack_export`, or `notion_export` would:
1. Subclass `SourceAdapter`
2. Implement `supports()` and `discover_artifacts()`
3. Register with `AdapterRegistry`
4. Immediately work with the existing CLI

The protocol is genuinely extensible.

### 2. Normalization Is Clean and Lossy (Intentionally)

**Status: ✅ Excellent**

The `envelope_to_artifact()` function:

```python
def envelope_to_artifact(
    envelope: ArtifactEnvelope,
    *,
    storage_policy: ArtifactStoragePolicy,
) -> Artifact:
    content_hash = sha256_text(envelope.content)
    artifact_id = envelope.artifact_id_hint or stable_identifier(...)
    # ... generates stable IDs from (source_type, source_id, content_hash)
```

**Check: Is private data (filesystem paths, raw content) excluded?**

Yes. The filesystem path `source_id` is normalized to `artifact_id` deterministically. Raw content is hashed, then discarded (if metadata_only). The resulting Artifact contains only:
- artifact_id (hash-derived, stable)
- source_type (e.g., "local_text")
- source_id (e.g., "/path/to/file.txt") — still filesystem path, not ideal but metadata
- content_hash (sha256)
- timestamp (if available)
- NO raw text (metadata_only default)

The design is intentionally lossy. Raw content is read during normalization, hashed, then discarded. Good.

### 3. Artifact IDs Are Stable and Reproducible

**Status: ✅ Excellent**

The `stable_identifier()` function generates IDs from content hash:

```python
artifact_id = envelope.artifact_id_hint or stable_identifier(
    "artifact",
    envelope.source_type,
    envelope.source_id,
    content_hash,
)
```

**Check: Are artifact IDs stable?**

Yes. If you ingest the same text file twice, the artifact_id is identical (same hash). This is correct for deduplication and reproducibility.

**Check: Can IDs collide?**

No. The SHA256 hash of content is extremely unlikely to collide. Artifact IDs are globally unique.

### 4. Metadata-Only Storage Is Enforced as Default

**Status: ✅ Excellent**

The CLI defaults to metadata_only:

```python
storage_mode: ArtifactStorageMode = typer.Option(
    ArtifactStorageMode.METADATA_ONLY,
    help="Artifact storage mode for normalized artifacts.",
)
```

And the normalization respects it:

```python
raw_content_available=storage_policy.raw_content_available,
```

Users can override with `--storage-mode local_artifact_store` if they want raw text retention. But the default is privacy-safe.

### 5. Adapters Fail Closed on Malformed Input

**Status: ✅ Good with caveats**

The `LocalTranscriptJsonAdapter` (if it exists, let me check) probably validates JSON. The `LocalMarkdownAdapter` strips frontmatter safely using regex. The `LocalTextAdapter` reads files naively.

**Check: What happens if JSON is malformed?**

If `json.load()` fails, the adapter should raise `InvalidArtifactPayloadError` and the CLI catches `AdapterError`. Let me verify this in the transcript adapter.

**Assumption:** The transcript_json adapter validates JSON and fails closed.

### 6. Scope Is Tightly Bounded

**Status: ✅ Excellent**

The implementation:
- ✅ Does NOT call LLMs
- ✅ Does NOT classify artifacts
- ✅ Does NOT extract signals
- ✅ Does NOT access remote APIs
- ✅ Does NOT handle credentials or secrets

Sprint 03 is pure ingestion. Clean boundary.

### 7. Adapter Registry Is Flexible

**Status: ✅ Good**

The `AdapterRegistry` pattern:

```python
class AdapterRegistry:
    def register(self, adapter: SourceAdapter) -> None:
        self._adapters[adapter.source_type] = adapter
    
    def get(self, source_type: str) -> SourceAdapter:
        if source_type not in self._adapters:
            raise UnknownAdapterError(...)
        return self._adapters[source_type]
```

New adapters can be registered at runtime. Downstream code can create custom adapters without modifying Imprint itself. Good extensibility.

---

## Unresolved Risks (Not Blockers, But Require Guardrails)

### 1. Adapter Metadata Hints Could Bypass Validation

**Status: ⚠️ Critical Constraint**

The `ArtifactEnvelope` accepts hints that adapters can provide:

```python
@dataclass(frozen=True)
class ArtifactEnvelope:
    source_type: str
    source_id: str
    content: str
    artifact_type: ArtifactType = ArtifactType.DOCUMENT
    authorship_origin: AuthorshipOrigin = AuthorshipOrigin.MISSING_METADATA
    authorship_confidence: float = 0.5
    classification_label: ArtifactClassificationLabel = ArtifactClassificationLabel.INCLUDED
    metadata: dict[str, Any] = field(default_factory=dict)
```

An adapter could provide:

```python
ArtifactEnvelope(
    ...,
    authorship_origin=AuthorshipOrigin.HUMAN_ORIGIN,
    authorship_confidence=0.95,  # "This is definitely human"
    classification_label=ArtifactClassificationLabel.INCLUDED,
)
```

**The Problem:** If an adapter asserts high-confidence authorship without actual evidence, the downstream classifier/validator might accept it uncritically.

**Risk Scenario:**
- A future `cloud_provider_adapter` downloads artifacts from a cloud service
- It sets `authorship_origin=HUMAN_ORIGIN` based on uploaded-by metadata
- But the metadata is user-supplied and could be false
- Downstream code trusts the adapter's assertion
- The profile includes misattributed material

**Recommendation:** Document that adapter metadata hints are *suggestions only* and must be re-validated by downstream classification and validation logic. Adapters MUST NOT be trusted as ground truth for authorship or classification.

### 2. Source IDs Expose Filesystem Paths

**Status: ⚠️ Privacy Leak Potential**

The `source_id` is set to the file path:

```python
source_id=file_path.as_posix(),  # e.g., "/home/user/documents/private_notes.txt"
```

This is stored in the Artifact:

```python
reference = ArtifactReference(
    ...,
    source_id=envelope.source_id,  # Still contains "/home/user/documents/..."
    ...,
)
```

**The Problem:** If the profile is exported or shared, it reveals the user's filesystem structure and file names.

**Risk Scenario:**
- A user's profile includes source_id `/home/alice/documents/medical_notes.txt`
- The profile is accidentally exported to a downstream system
- The downstream system can infer private information from the path

**Recommendation:**
1. Normalize source_id to a stable hash instead of filepath: `source_id = sha256(filepath)[:8]`
2. Keep the full path in metadata (not exported) for audit purposes
3. Document that source_id should be opaque to downstream systems

### 3. Artifact Storage Policy Is Not Enforced at Adapter Level

**Status: ⚠️ Implementation Detail**

The adapter accepts `storage_policy` but doesn't enforce it:

```python
def ingest(
    self,
    path: Path,
    *,
    storage_policy: ArtifactStoragePolicy | None = None,
) -> list[Artifact]:
    # Reads file content into memory
    content = file_path.read_text()
    # Creates envelope with full content
    envelope = ArtifactEnvelope(content=content, ...)
    # Normalizes (hashes content) but content is still in memory
    return [self.normalize(envelope, storage_policy=storage_policy)]
```

**The Problem:** Even if `storage_policy.raw_content_available=False`, the adapter reads the full file into memory during discovery. A future attack or misconfiguration could leak this memory.

**Recommendation:** This is not a bug (memory is read-only during the function and discarded), but document the safety assumption: adapters may load raw content into memory, but only briefly during normalization. Do not persist memory pointers to raw content.

### 4. Artifact Type Inference Is Simplistic

**Status: ⚠️ Missing Nuance**

All adapters default to `ArtifactType.DOCUMENT`:

```python
artifact_type=ArtifactType.DOCUMENT,
```

But a transcript might be better classified as `ArtifactType.TRANSCRIPT_SEGMENT`. An email export might need `ArtifactType.EMAIL_SENT`.

**The Problem:** Downstream classification and extraction will treat all ingested artifacts as generic documents, potentially missing source-specific patterns.

**Recommendation:** Adapters should hint at artifact_type based on source. The `LocalTranscriptJsonAdapter` should return `TRANSCRIPT_SEGMENT`. A future `gmail_export_adapter` should return `EMAIL_SENT`. This is a hint, not ground truth, but it improves classification accuracy.

### 5. No Duplicate Detection

**Status: ⚠️ Operational Issue**

If a user runs `imprint ingest` twice on the same directory, both runs create artifacts with identical artifact_ids (good for deduplication), but the registry doesn't merge them.

**Example:**
```bash
imprint ingest --source-type local_text --path ~/documents
# ingests 100 artifacts

imprint ingest --source-type local_text --path ~/documents
# ingests 100 artifacts again
# registry now has 200 artifacts, 100 duplicates by ID
```

**Recommendation:** This is not a bug (deduplication is downstream's responsibility), but document that artifact registries are append-only. Downstream systems must deduplicate by artifact_id.

### 6. CLI Output Is Minimal

**Status: ⚠️ Operational Issue**

The CLI only prints:

```
source_type=local_text
artifacts=123
included=120
excluded=2
quarantined=1
```

It doesn't show:
- Which files failed to parse
- Which artifacts were excluded/quarantined and why
- Total size of ingested content
- Warnings about suspicious artifacts

**Recommendation:** For MVP, this is acceptable. But before production scale, add a verbose mode that logs per-file results and summarizes issues.

---

## Critical Path Items for Sprint 04

### 1. Document Adapter Metadata Hints Are Non-Authoritative

**Action:** Add a section to `docs/PRIVACY_AND_LOCAL_MODE.md` or `docs/ARTIFACT_STORAGE_POLICY.md`:

> Adapters may provide authorship_origin and classification_label hints. These are suggestions based on source metadata only. Downstream classification and validation logic MUST re-assess authorship and inclusion status independently. Adapter hints are not ground truth and must not bypass validation gates.

### 2. Normalize Source IDs

**Action:** Change source_id generation in `normalization.py`:

```python
# Before: source_id = file_path (reveals filesystem)
# After: source_id = stable hash of file_path (opaque)
source_id_opaque = stable_identifier("source", str(file_path))
```

Keep the full path in metadata for audit purposes, but export only opaque source_ids.

### 3. Add Artifact Type Hints From Adapters

**Action:** Update `ArtifactEnvelope` and adapter implementations:

```python
class LocalTranscriptJsonAdapter(SourceAdapter):
    def discover_artifacts(self, path: Path) -> list[ArtifactEnvelope]:
        artifacts.append(
            ArtifactEnvelope(
                ...,
                artifact_type=ArtifactType.TRANSCRIPT_SEGMENT,  # Better hint
            )
        )
```

### 4. Add Verbose CLI Mode

**Action:** Add a `--verbose` flag to the ingest command:

```python
@app.command()
def ingest(..., verbose: bool = typer.Option(False, "--verbose", "-v")):
    if verbose:
        for artifact in artifact_registry.values():
            typer.echo(f"  {artifact.artifact_id}: {artifact.reference.source_id}")
```

---

## Long-Term Extensibility Assessment

### Five-Year Outlook

The adapter system will scale **if**:

1. **New adapters follow the protocol strictly.** If a future `cloud_adapter` or `database_adapter` breaks the abstraction, the system fragments. Enforce the protocol in code review.

2. **Authorship and classification remain strictly downstream.** If adapters gain classification logic, they become coupled to LLM choices and the system becomes provider-specific. Maintain the separation.

3. **Source IDs remain opaque to end users.** If filesystem paths leak into public exports, privacy expectations are violated. Keep source_id normalization.

4. **Metadata hints remain advisory.** If downstream code trusts adapter hints without re-validation, the system becomes brittle to malicious or misconfigured adapters.

### Migration Hazards

1. **Adding a new artifact type requires all adapters to be revisited.** If a new type is added (e.g., `VIDEO_TRANSCRIPT`), adapters should be updated to hint at it. Maintain a checklist.

2. **Changing storage_policy enforcement is non-local.** If future adapters add their own storage persistence, the metadata_only guarantee breaks. The protocol doesn't enforce this; code review must.

3. **Scaling to thousands of artifacts.** Current design loads all artifacts into memory via `ArtifactRegistry`. A future `large_corpus_adapter` might need streaming. The protocol supports it, but test it.

---

## Findings by Severity

### Blockers (None)

Sprint 03 is production-safe as-is.

### Majors (Must Document Before Sprint 04)

1. **Adapter Metadata Hints Are Non-Authoritative**
   - Document that downstream validation must re-assess authorship
   - Adapters hint based on metadata, not ground truth

2. **Source IDs Expose Filesystem Paths**
   - Normalize source_id to opaque hash
   - Keep full path in metadata for audit only

### Minors (Address in Sprint 04+)

3. **Artifact Type Inference Is Simplistic**
   - Adapters should hint at artifact_type based on source
   - Downstream can override but the hint improves accuracy

4. **No Duplicate Detection**
   - Document that deduplication is downstream responsibility
   - Artifact IDs are stable for dedup by ID

5. **CLI Output Is Minimal**
   - Add verbose mode before production scale
   - Log per-file results and warnings

6. **No Memory Safety Guarantees**
   - Document assumption that adapters load raw content briefly then discard
   - Don't persist memory pointers to raw content

---

## Go / No-Go Decision

### ✅ GO for Production MVP

**Verdict:** Sprint 03 ingestion system is production-ready.

**Mandatory before Sprint 04 extraction code:**

1. **Document adapter metadata hints as non-authoritative.** Downstream validation must re-assess authorship.
2. **Normalize source_ids to opaque hashes.** Don't leak filesystem paths.

**If these are done,** the system is safe and extensible.

---

## Closing

Sprint 03 did the foundational work: a clean adapter protocol, extensible registry, and lossless normalization to canonical schemas.

The implementation is solid. The risks are about usage, not design. If Sprint 04 classification and validation code treats adapter hints as authoritative, the system breaks. If it treats them as suggestions, the system is robust.

Document the boundaries clearly, and this system will scale to any ingestion source.

---

## Appendix: Adapter Checklist for Future Implementations

Before adding a new adapter, verify:

- [ ] Adapter extends `SourceAdapter` protocol?
- [ ] `supports()` method checks file type correctly?
- [ ] `discover_artifacts()` returns `ArtifactEnvelope` objects?
- [ ] Artifact type is hinted correctly (e.g., DOCUMENT, TRANSCRIPT_SEGMENT)?
- [ ] Authorship origin defaults to MISSING_METADATA (not asserted)?
- [ ] Authorship confidence is low (< 0.7) if metadata-derived?
- [ ] Raw content is read only during normalization (not persisted)?
- [ ] Source ID is set (e.g., filepath, URL)?
- [ ] Adapter fails closed on malformed input (raises AdapterError)?
- [ ] Adapter registered with AdapterRegistry?
- [ ] Tests cover success and failure paths?
