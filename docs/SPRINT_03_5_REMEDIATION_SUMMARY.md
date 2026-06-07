# Sprint 03.5 Remediation Summary

Status: Sprint 03.5 complete

## What Changed

- Adapter-local `source_id` locators now normalize to opaque stable `source-*` identifiers in
  canonical artifacts.
- JSONL record metadata such as `artifact_type`, `authorship_origin`,
  `authorship_confidence`, and `classification_label` is now treated as advisory hint metadata
  rather than canonical normalized classification output.
- Transcript JSON continues to emit `transcript_segment` as an adapter-obvious type hint from
  source shape, while filesystem-backed adapters emit `document`.
- Policy docs now state that adapters may briefly read raw text in memory for hashing and
  normalization, but `metadata_only` mode must not persist raw text.
- Sprint 04 documentation now requires re-assessment of adapter hints before classification.

## Tests Added

- Opaque source ID assertions for local text, markdown, and transcript adapters
- Stable source ID assertions across repeated ingestions
- JSONL hint assertions proving record-provided type/authorship/classification values stay advisory

## Remaining Risks

- Full local/private audit metadata for original filesystem locators is not implemented yet.
- Classification logic still needs to decide how much weight to assign adapter-observed source
  hints versus downstream evidence.

## Sprint 04 Readiness

Sprint 04 can begin. The ingestion layer now preserves the classification boundary and avoids
filesystem-path leakage in canonical artifact references.
