# Signal Extraction Rules

Status: Sprint 05 baseline plus Sprint 05.5 artifact-local extension

## Durable Eligibility

- `included` classification -> durable `observation` signals allowed
- `quarantined` classification -> quarantined candidate signals only
- `excluded` classification -> no signal output

## Implemented Rules

- `structure_short_paragraphs` -> all observed paragraphs are short
- `structure_direct_opening` -> artifact opens with a short direct sentence
- `lexical_contractions` -> artifact includes contractions
- `rhetorical_contrast_framing` -> artifact uses a not-X-but-Y contrast structure
- `formatting_bullet_usage` -> artifact uses bullet formatting
- `formatting_heading_usage` -> artifact uses heading formatting
- `tone_question_marker` -> artifact uses explicit question markers
- `tone_exclamation_marker` -> artifact uses exclamation markers
- `reasoning_causal_explanation` -> artifact uses explicit causal explanation markers
- `reasoning_tradeoff_framing` -> artifact uses explicit tradeoff or exchange framing
- `reasoning_caveat_handling` -> artifact includes caveat or uncertainty markers
- `narrative_ordered_sequence` -> artifact uses explicit ordered sequence markers
- `narrative_before_after_transition` -> artifact uses an explicit before-and-after transition
- `narrative_example_grounding` -> artifact grounds a point with an explicit example marker
- `anti_pattern_question_burst` -> multiple questions should not be promoted into a stable
  uncertainty claim without recurrence
- `anti_pattern_punctuation_emphasis` -> clustered punctuation emphasis should not be treated as
  emotional ground truth
- `anti_pattern_formatting_without_explanatory_prose` -> formatting cues alone should not be
  promoted into a reasoning claim

## Evidence Policy

- every signal includes signal ID, artifact ID, source type, classification ID, classification
  model version, rule ID, observed feature, limitations, and no-raw-text evidence policy
- source IDs remain opaque
- observed features are generic summaries, not private excerpts

## Claim Boundary

- prefer `observation`
- use `quarantined` when the source artifact is not cleanly eligible for durable support
- do not emit `bounded_interpretation` in the baseline extractor
- do not emit `prohibited` signal outputs

## Deferred Coverage

- humor
- long-form reasoning chains
- narrative sequencing beyond explicit deterministic markers
- semantic tone inference
- cross-artifact recurrence or distribution signals
- multilingual or translation-aware extraction
