# Signal Extraction Design

Status: Sprint 05 baseline plus Sprint 05.5 artifact-local extension

## Goal

Sprint 05 extracts deterministic, artifact-level candidate signals from classified artifacts. It
does not compile profiles and does not make person-level claims.

## Design

- Signal extraction consumes normalized `Artifact` objects plus `ArtifactClassificationResult`
  outputs from Sprint 04.
- Only `included` artifacts may produce durable signal support.
- `quarantined` artifacts may emit quarantined candidate signals for review, but not durable
  support.
- `excluded` artifacts emit no signals.
- The baseline extractor is deterministic, local-first, and artifact-local. It does not compare
  every artifact to every other artifact.

## Implemented Families

- `structure`
- `lexical`
- `rhetorical_pattern`
- `formatting`
- `tone_marker`
- `reasoning`
- `narrative`
- `anti_pattern`

Sprint 05.5 keeps the same artifact-local boundary and adds only deterministic markers:

- `reasoning`: causal markers, tradeoff framing, caveat or uncertainty markers
- `narrative`: ordered sequence markers, before/after transitions, explicit example grounding
- `anti_pattern`: question bursts, punctuation emphasis bursts, formatting without enough
  explanatory prose

## Confidence Model

Signal confidence is derived from:

- classification attribution confidence
- classification authorship-origin confidence
- rule reliability
- evidence strength
- policy fit

The baseline extractor records these in the existing decomposed `Confidence` object and uses the
Sprint 04 classification confidence as an explicit input boundary.

## Boundary

- Signals are observations about artifacts, not claims about a person.
- No raw text is emitted in public-safe signal outputs.
- No provider APIs, LLMs, embeddings, or remote inference are used.
- No durable support is built from quarantined or excluded artifacts.
- Cross-artifact aggregation remains out of scope and belongs to Sprint 06.
- Humor remains deferred until there is a narrower deterministic contract worth shipping.
