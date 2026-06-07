# Classification Rules

Status: Sprint 04 baseline

## Deterministic Rules

- `local_transcript_json` with explicit speaker metadata classifies to `human_origin` and may be
  included when contamination risk stays low.
- Missing transcript speaker metadata classifies to `unknown_speaker` and quarantines.
- Quote or forward markers raise quote/forward likelihood and quarantine the artifact.
- Template or notification markers classify to `template_or_notification` and exclude the artifact.
- Assistant markers classify to `assistant_output` and exclude the artifact.
- Oversized artifacts (>10MB text) classify to `parser_uncertain` and quarantine for manual review.
- JSONL-supplied authorship, confidence, inclusion, and artifact-type values remain advisory
  source hints. They do not automatically become final classification truth.
- Uncorroborated human-origin hints degrade to lower-confidence provisional outcomes rather than
  silently including the artifact.

## Quarantine vs Exclusion

- `exclude`: artifact is confidently non-subject or low-value for profile construction  
  Current Sprint 04 cases: `assistant_output`, `template_or_notification`
- `quarantine`: artifact may contain relevant context but has uncertain authorship, contamination, or
  parsing risk  
  Current Sprint 04 cases: `quoted_or_forwarded`, `unknown_speaker`, `missing_metadata`,
  `parser_uncertain`, `mixed_authorship`, `suspected_ai_assisted`,
  `human_directed_ai_assisted`, oversized artifacts
- `include`: artifact is low-contamination, confidently human-origin, and passes the confidence
  floor

Quarantined artifacts are preserved for review and downstream counts. They must not silently
support durable profile signals in Sprint 04.

## Pathological Cases

- mixed-language or contradictory source markers: quarantine if authorship becomes uncertain
- malformed or weak source metadata: quarantine rather than assume human-origin
- oversized artifacts (>10MB): quarantine with `parser_uncertain`
- filesystem paths or raw text in hint metadata: reject at schema validation
- unsupported source-shape heuristics: preserve artifact, lower confidence, and quarantine if risk
  stays material

## Rule Inventory

- Covered in Sprint 04: transcript speaker presence, quote/reply/forward markers,
  template/notification markers, assistant-output markers, oversized-artifact review, advisory
  JSONL hint re-assessment
- Deferred beyond Sprint 04: implicit email headers, translation detection, calendar/log/system
  message families, cross-artifact deduplication, multilingual heuristics

## Explainability Requirements

Every classification result records:

- artifact ID
- opaque source ID
- source type
- source hints considered
- rule IDs applied
- limitations
- evidence summary
- likelihoods for quote/forward, template/notification, assistant output, and contamination
