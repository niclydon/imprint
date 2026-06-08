# Sprint 12 Evaluation and Quality Gates

Sprint 12 added the quality layer that makes Imprint exports reviewable before release or downstream
use.

The key implementation is `src/imprint/quality.py`, exposed through two CLI commands:

- `imprint validate-export <file>`
- `imprint diff profile-a.json profile-b.json`

`validate-export` emits a machine-readable PASS/FAIL report for canonical JSON exports, Mosvera
expression overlays, and Sprint 08 consumer contracts. It checks schema shape, export versions,
compatibility metadata, evidence policy, opaque source IDs, raw/private content fields, path-like
strings, credential-like strings, prohibited claims, and prompt/provider/generation-control fields.

`diff` validates both canonical JSON inputs, compares profile metadata and signal summaries, computes
comparability from the existing schema `ComparabilityResult`, and separates expression drift from
compiler, corpus, and schema drift.

The regression corpus remains synthetic. Tests generate public-safe example exports from
`examples/synthetic_corpus/transcript/synthetic-demo.json`, mutate them to simulate regressions, and
verify the quality gates fail closed.

Sprint 12 closes the main release-readiness gap left by Sprint 11: generated profile exports now have
a deterministic validation and comparison path.
