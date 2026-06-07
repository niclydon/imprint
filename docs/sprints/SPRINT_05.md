# Sprint 05 - Signal Extraction
Primary Model: GPT 5.5
Reviewer: Claude

Status:
Implemented baseline signal extractor

Build lexical, tone, humor, reasoning, structure, narrative and anti-pattern extraction.

Reviewer Prompt: Challenge whether signals measure what they claim. Generate SIGNAL_VALIDITY_REVIEW.md.

Implemented baseline behavior:

- Added deterministic artifact-level signal extraction from classified artifacts.
- Implemented baseline families: structure, lexical, rhetorical_pattern, formatting, tone_marker.
- Preserved the Sprint 04 classification boundary: excluded artifacts emit no signals, quarantined
  artifacts emit quarantined candidates only.
- Emitted public-safe evidence metadata with no raw text.

Deferred beyond baseline:

- humor
- broad reasoning extraction
- narrative sequencing beyond contrast framing
- anti-pattern extraction
- cross-artifact recurrence and profile compilation

Follow-on:

- Sprint 05.5 extends the artifact-local extractor with deterministic `reasoning`, `narrative`,
  and `anti_pattern` rules while keeping cross-artifact aggregation deferred to Sprint 06.
