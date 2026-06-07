# Classification Design

Status: Sprint 04 baseline

## Goal

Sprint 04 classifies normalized artifacts conservatively before any signal extraction or profile
interpretation.

## Design

- Classification consumes normalized `Artifact` objects plus export-safe `source_hints`.
- Adapter-provided metadata is treated as ingestion evidence, not final truth.
- The baseline classifier is deterministic and local-first. It uses rule evaluation over opaque
  source identifiers, safe metadata hints, and source-shape signals derived during normalization.
- Classification produces explicit evidence with rule IDs, considered hints, confidence, and
  contamination/quote/template likelihoods.
- Classification confidence uses a versioned component model: `attribution`,
  `authorship_origin`, `evidence_strength`, `source_reliability`, `policy_fit`,
  `contamination_penalty`, and `display`.

## Confidence Model

- `model_version`: `sprint04-rule-v1`
- `attribution`: 0.95 when opaque source IDs and normalized source type are present
- `authorship_origin`: the classifier's final authorship confidence
- `evidence_strength`: higher for corroborated source-shape signals, lower for oversized or weakly
  evidenced artifacts
- `source_reliability`: transcript-with-speaker > local text/markdown > advisory JSONL
- `policy_fit`: 1.0 when the final label matches the quarantine/exclusion policy tree
- `contamination_penalty`: derived from quote/forward, template/notification, assistant-output,
  mixed-authorship, and oversized-artifact risk
- `display`: weighted local heuristic  
  `0.15*attribution + 0.35*authorship_origin + 0.20*evidence_strength + 0.15*source_reliability + 0.15*policy_fit - 0.20*contamination_penalty`, clamped to `[0.05, 0.95]`

This model is deterministic and intentionally conservative. Sprint 05 should treat the version as a
compatibility boundary if formulas change.

## Boundary

- Classification does not extract signals.
- Classification does not compile profiles.
- Classification does not infer personality, intent, or diagnosis.
- Classification does not use provider APIs, LLMs, or embeddings.
