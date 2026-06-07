# Evidence Model

Status: Sprint 02 schema contract

## Principle

Every signal and claim must answer: why do we believe this?

Evidence is represented through public-safe references, aggregate support, provenance, and audit limitations. Raw text is not required and is not stored by default.

## Evidence Reference

An evidence reference records:

- artifact ID and optional artifact reference ID
- source ID and source type
- artifact type
- classification ID
- extraction run ID
- content hash or fingerprint
- timestamp or coarse time bucket
- inclusion status
- authorship origin and confidence
- raw-content availability

## Signal Support

Signal support aggregates references into:

- artifact count
- included, excluded, and quarantined counts
- source types
- time window
- source diversity score
- audit limitations

Public-safe support must use references and aggregates, not raw excerpts.

## Audit Limitations

Metadata-only storage is the MVP default. A profile must disclose when raw content is unavailable, when regeneration requires re-harvesting, and when audit can only show metadata, counts, hashes, and classifications.

## Excluded Evidence

Excluded and quarantined evidence remains visible in support counts. Quoted, forwarded, assistant-output, parser-uncertain, mixed-authorship, or suspected AI-assisted material must not silently support high-confidence claims.
