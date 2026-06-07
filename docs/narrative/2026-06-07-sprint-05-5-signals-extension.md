# Sprint 05.5 Narrative: Artifact-Local Signal Extension

## Status
Implemented and ready for closeout.

## Scope
- Extend deterministic, artifact-level signal extraction with three families that do not cross artifacts.
- Keep the metadata-only, public-safe output contract and the Sprint 04 classification boundary intact.
- No provider calls, no embeddings, no profile compilation, and no model prompts.

## Shipped Behavior
- Added `reasoning` signal rules for:
  - causal explanation markers
  - tradeoff/exchange framing
  - caveat or uncertainty markers
- Added `narrative` signal rules for:
  - ordered sequence markers
  - before/after transitions
  - explicit example grounding
- Added `anti_pattern` rules for:
  - question bursts (non-durable uncertainty claims)
  - punctuation emphasis (emotional overreach guardrail)
  - formatting-without-enough-explanatory-prose markers
- Extended source-hint derivation to emit marker counts/booleans used by the new rules.

## Evidence and Safety Boundaries
- Signals remain artifact-local and are gated by classification:
  - `included` artifacts produce durable candidates
  - `quarantined` artifacts produce non-durable candidates
  - `excluded` artifacts emit no signals
- Signal evidence remains no-raw-text and opaque.
- Existing no-personality/diagnostic guardrail remains active in signal schema validation.

## Documentation and Traceability
- Updated:
  - `docs/SIGNAL_EXTRACTION_DESIGN.md`
  - `docs/SIGNAL_EXTRACTION_RULES.md`
  - `docs/SIGNAL_TAXONOMY.md`
  - `docs/sprints/SPRINT_05.md`
  - `docs/sprints/SPRINT_05_5.md`
  - `docs/sprints/SPRINT_05_ARCHITECTURE_REVIEW.md` (sprints now includes 5.5 signal families)

## Open Items for Sprint 06
- Cross-artifact aggregation and profile compilation layer.
- Humour family and deeper reasoning/narrative sequencing beyond deterministic markers.
- Aggregated confidence drift controls in multi-artifact claim compilation.
