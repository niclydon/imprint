# Artifact Storage Policy

Status: Sprint 01.5 remediation decision

## Decision

Imprint may store raw artifact text locally, but only inside a user-controlled Artifact Store scoped
to profile compilation, auditability, and regeneration.

This is not a general memory system. Imprint does not expose arbitrary recall, question-answering,
relationship lookup, or assistant memory APIs over the artifact store.

## Why

The Sprint 01 challenge is correct: auditability and regeneration are weak if Imprint only stores
derived signals. A user must be able to answer:

- Which artifacts supported this signal?
- Was the quoted or forwarded material excluded?
- Did a model upgrade change the extracted pattern?
- Can this profile be rebuilt from the same evidence window?

Those requirements need access to source text or a deliberate decision not to preserve it.

## Storage Modes

### Metadata-Only

Stores artifact metadata, classifications, evidence references, and hashes, but not raw text.

Use when:

- source systems are easy to re-harvest
- privacy risk is more important than local regeneration
- the user wants minimal local persistence

Tradeoff: profile regeneration requires re-reading the source system.

### Local Artifact Store

Stores normalized artifact text locally in ignored data paths.

Use when:

- auditability matters
- source systems may disappear
- connector access is intermittent
- extractor/model changes require fair recompilation

Tradeoff: the local store becomes a sensitive corpus and must be handled as protected data.

### Ephemeral

Keeps raw text only during a single run and discards it after signals and reports are generated.

Use when:

- the user wants one-off analysis
- no later audit is needed
- the source system remains the authority

Tradeoff: support metadata can explain the run, but cannot fully reproduce it without re-harvest.

## Default

The MVP default storage mode is `metadata_only`.

This is a deliberate privacy-first tradeoff. Default runs preserve support metadata, hashes,
classifications, and profile evidence references, but they do not guarantee full local
regeneration if the original source disappears.

The first real non-synthetic profile build should show the tradeoff plainly:

- choose `metadata_only` for lower retention and weaker auditability
- choose `local_artifact_store` for stronger audit/regeneration and higher privacy risk
- choose `ephemeral` for one-off analysis with no durable raw text

The public demo and synthetic examples must use `metadata_only`.

The MVP default should therefore be:

- synthetic examples in repo
- local ignored storage for user runs
- raw text stored only when the user explicitly enables `local_artifact_store`
- public-safe exports without raw text

## Security Posture

The local Artifact Store is protected data.

Required policies:

- store under ignored paths such as `data/` or another configured local path
- never write raw artifact text under `docs/`, `examples/`, or tracked fixture paths
- never commit local artifact stores, databases, dumps, or generated personal profiles
- support strict redaction for reports and exports
- record whether raw content was stored for each profile build
- fail closed if public-safe export attempts to include raw examples

Encryption should be supported as a future hardening option, but Sprint 02 schema work should not
depend on choosing a specific database encryption implementation.

## Evidence References

Profiles should reference evidence through non-raw support metadata by default:

- artifact IDs
- source IDs
- source type
- artifact type
- time window
- classification IDs
- extraction run IDs
- content hash or text fingerprint
- included/quarantined/excluded status

Public-safe exports must not include raw artifact text. Private-local reports may include redacted
excerpts. Full-local reports may include raw excerpts only when explicitly enabled.

## Boundary From Memory Systems

Imprint may:

- retain artifacts for compilation and audit
- re-run classification and extraction
- show why a profile signal exists
- compare profile versions

Imprint must not:

- answer arbitrary factual questions from the corpus
- serve as a personal knowledge graph
- provide long-term assistant memory retrieval
- expose raw corpus search as a downstream product contract
- let downstream consumers fetch raw artifacts by default

## Rejected Alternatives

### Never Store Raw Text

Rejected because it makes audit and regeneration dependent on source availability and connector
credentials.

### Always Store Raw Text

Rejected because it over-captures sensitive data and makes the safest mode unavailable.

### Treat Artifact Store as Memory

Rejected because it collapses Imprint into the category it is supposed to sit beside. The artifact
store exists for compilation, not recall.

## Sprint 02 Implications

Sprint 02 schemas must include:

- artifact storage mode
- content retention policy
- raw-content availability flag
- evidence references that work without raw text in public exports
- build metadata recording whether regeneration is possible from local storage
- default value of `metadata_only`
- explicit audit limitation text when raw content is not retained
