# Signal Taxonomy

Status: Sprint 02 schema contract

A signal is an evidence-backed expression pattern. Signal names should describe observable behavior rather than personality traits.

## Lexical

**Definition:** word choice, phrase recurrence, jargon, register, contractions, and terminology patterns.

**Evidence requirements:** artifact references, source-type counts, time window, authorship-origin confidence, extraction method, and examples as hashes or private-local references rather than public raw text.

**Non-examples:** "is smart", "is technical", "has high openness".

**Confidence guidance:** high only when the pattern appears across multiple source types or a policy-declared single-source context with strong attribution.

## Tone

**Definition:** observable affective surface features such as directness, formality, hedging, enthusiasm markers, apology frequency, or imperative frequency.

**Evidence requirements:** token or classifier support, source mix, excluded/quarantined counts, and whether quoted or assistant-authored material was removed.

**Non-examples:** hidden emotional state, intent, manipulation, anger, anxiety.

**Confidence guidance:** lower confidence when artifacts are short, quoted, forwarded, template-driven, or mixed-authorship.

## Humor

**Definition:** observable humor devices such as understatement, callbacks, absurd comparisons, self-deprecation, or irony markers.

**Evidence requirements:** source context, artifact counts, time window, and claim level. Humor claims are context-sensitive and should usually remain observations.

**Non-examples:** "is funny", "is sarcastic by nature", inferred social intent.

**Confidence guidance:** require multiple artifacts unless the context profile explicitly covers a narrow performance or publication genre.

## Reasoning

**Definition:** visible explanation structure: evidence-before-generalization, tradeoff framing, decision criteria, causal chains, caveats, and uncertainty handling.

**Evidence requirements:** references to reasoning-bearing artifacts, extraction version, source-policy fit, and bounded interpretation labels when summarizing beyond directly counted features.

**Non-examples:** IQ, rationality, ideology, values, or cognitive diagnosis.

**Confidence guidance:** sensitive to source type; chat fragments are weak for long-form reasoning unless the source policy gives them explicit weight.

## Structure

**Definition:** formatting and organization patterns such as paragraph length, bullet usage, section order, conclusion placement, and transition style.

**Evidence requirements:** artifact type, length distribution, content availability flag, and filtered context support.

**Non-examples:** quality ranking, professionalism score, competence inference.

**Confidence guidance:** high when source type is stable; lower when source types mix chats, transcripts, and edited publications without context profiles.

## Narrative

**Definition:** story and explanation moves such as starting with incidents, escalating from concrete examples to general rules, or using before/after contrast.

**Evidence requirements:** supported claims, source diversity, and bounded interpretation when the pattern requires semantic extraction.

**Non-examples:** life story inference, motivation, trauma, ideology, identity claims.

**Confidence guidance:** cross-model semantic extraction is not comparable unless explicitly migrated.

## Anti-Patterns

**Definition:** patterns the profile says downstream consumers should avoid because they are unsupported, generic, misleading, or inconsistent with observed expression.

**Evidence requirements:** the positive observed pattern being protected, claim validation result, and export mode.

**Non-examples:** prompt instructions, provider settings, editorial workflow steps.

**Confidence guidance:** anti-patterns require the same evidence discipline as positive signals and must not become prompt-generation controls.
