# Sprint 04 - Classification Engine
Primary Model: GPT 5.5
Reviewer: Gemini

Status:
Implemented baseline rule classifier

Build authorship, speaker confidence, AI-assistance, quote, template and notification classification with explainable confidence scoring.

Reviewer Prompt: Assume data is messy and users misuse the system. Generate CLASSIFICATION_RISKS.md.

## Sprint 03.5 Carry-Forward Requirements

Sprint 04 classifiers must treat adapter output as pre-classification ingestion data, not ground
truth.

Required behavior:

- re-assess any adapter-provided authorship hints
- re-assess any adapter-provided inclusion or exclusion hints
- treat JSONL record-level artifact type values as advisory metadata, not canonical type truth
- preserve opaque `source_id` values and avoid reconstructing local filesystem paths in exports
- require explainable evidence for durable classification outcomes

Implemented behavior:

- Added a deterministic rule-based local classifier over normalized artifacts.
- Added explainable classification outputs with rule IDs, considered source hints, likelihoods,
  limitations, and summary text.
- Quarantines uncertain authorship and excludes assistant/template-notification artifacts.
- Keeps classification artifact-level only and does not interpret the subject.
- Locks confidence scoring to `sprint04-rule-v1`.
- Documents explicit quarantine vs. exclusion policy and scaling targets.
