# Sprint 05.5 - Artifact-Local Signal Extension

Primary Model: None
Reviewer: Architecture review in parallel

Status:
Implemented

Scope:

- extend the deterministic artifact-level signal extractor without crossing into profile
  compilation
- add `reasoning`, `narrative`, and `anti_pattern` families only where they can be supported by
  explicit artifact-local markers
- keep public-safe evidence and metadata-only boundaries unchanged

Implemented behavior:

- `reasoning` rules:
  - causal explanation markers
  - tradeoff or exchange framing markers
  - caveat or uncertainty markers
- `narrative` rules:
  - ordered sequence markers
  - before/after transitions
  - example grounding markers
- `anti_pattern` rules:
  - question bursts should not become stable uncertainty claims without recurrence
  - punctuation emphasis should not become emotional ground truth
  - formatting without explanatory prose should not become a reasoning claim

Explicit non-goals preserved:

- no cross-artifact aggregation
- no profile compilation
- no humor extraction
- no semantic narrative understanding
- no LLMs, embeddings, or remote inference
