# Product Thesis

Status: Sprint 01 output
Audience: maintainers, contributors, downstream integrators

## Thesis

Imprint exists because people increasingly use AI systems to draft, answer, publish, teach,
summarize, and represent them, but the reusable contract for a person's expression is weak.
Most tools either keep raw examples in prompts, bury style inside a memory system, or let each
downstream app invent its own partial voice model.

Imprint should be an independent expression compiler: it turns human-created artifacts into
versioned, evidence-backed expression profiles that downstream systems can use without reading
the raw corpus.

## Problem

Today, the common approaches fail in predictable ways:

- Raw few-shot prompts leak private samples, age poorly, and do not explain confidence.
- Writing assistants optimize for immediate content generation, not durable expression contracts.
- Memory systems store facts and preferences but do not separate identity, expression, voice,
  provenance, contamination, and context-specific profile variants.
- Publishing systems need voice, but if they compile voice directly they become private corpus
  owners by accident.
- Persona and clone systems optimize for simulation, delegation, or conversation, which creates
  consent and overclaiming risks when the real need is a bounded expression profile.
- Brand systems enforce approved language, but they usually assume an organization-owned brand
  workflow rather than a local, owner-operated identity compiler.

## Why Imprint Is Independent

Imprint should not live inside a personal knowledge graph, publishing app, model router, memory
layer, or aesthetic pack system.

Independence gives the project a clean contract:

- Source systems provide evidence; they do not decide what the subject sounds like.
- Imprint classifies, extracts, compiles, versions, and exports expression profiles.
- Downstream systems apply profiles; they do not need raw private artifacts.
- Private deployments remain configuration; public code remains generic and reusable.
- The profile schema can become a stable contract across many consumers.

This separation prevents the most likely failure mode: every consumer quietly building its own
voice corpus with different privacy rules and no provenance trail.

## What Imprint Owns

Imprint owns:

- Normalized artifact metadata from configured sources.
- Speaker attribution and authorship-origin classification.
- AI-assistance, quote, forwarded-content, template, and notification risk handling.
- Signal extraction across lexical, tone, humor, reasoning, structure, narrative, platform fit,
  and anti-pattern dimensions.
- Source weighting and quarantine policy.
- Master profile plus derived profiles by context.
- Versioned profile compilation.
- Confidence, evidence support, and drift metadata.
- Public-safe, private-local, and full-local export modes.

## What Imprint Must Not Own

Imprint must not own:

- Raw long-term memory.
- A general personal data lake.
- Publishing workflows or draft generation.
- Visual brand systems or aesthetic pack resolution.
- Chatbot, clone, or persona behavior.
- Model routing infrastructure.
- Private connectors with hard-coded deployment details.
- Medical, psychological, personality, or intent diagnosis.
- Monetization, audience growth, or market-share optimization.

## Competitive Lessons

Current public products validate demand but also clarify Imprint's boundary:

- Spiral emphasizes training on someone's voice and automating writing tasks. Imprint should learn
  from the user value of voice-fit while not becoming a writing automation product.
- Jasper Brand Voice and Brand IQ show that voice controls are useful in generation workflows.
  Imprint should instead produce the portable profile contract those workflows can consume.
- WRITER shows that enterprise buyers value enforced brand standards and knowledge grounding.
  Imprint should keep approved-language enforcement and enterprise workflow outside its core.
- Personal AI and Delphi validate the desire for personal representation, but their digital-mind
  posture is broader than Imprint's evidence-backed expression boundary.
- Zep and Mem0 validate persistent memory as infrastructure for agents. Imprint should integrate
  with memory layers as sources or consumers, not compete as a memory store.
- Originality.ai validates the importance of authorship and AI-contamination signals, while also
  showing why detector output should be treated as evidence with uncertainty, not truth.

References used for current market posture:

- Spiral product page: <https://spiral.computer/product>
- Jasper Brand Voice help: <https://help.jasper.ai/hc/en-us/articles/18618693085339-Brand-Voice>
- Jasper Brand IQ: <https://www.jasper.ai/brand-iq>
- WRITER Brand: <https://writer.com/brand/>
- WRITER Knowledge Graph: <https://writer.com/product/graph-based-rag/>
- Personal AI training page: <https://www.personal.ai/train-your-own-small-language-model>
- Delphi docs: <https://docs.delphi.ai/chat-with-a-delphi>
- Zep memory docs: <https://help.getzep.com/v2/memory>
- Mem0 homepage: <https://mem0.ai/>
- Originality.ai product page: <https://originality.ai/>
- Originality.ai plagiarism help: <https://help.originality.ai/en/article/plagiarism-checker-1s05jkm/>

## What Happens If Imprint Does Not Exist

If Imprint does not exist, voice and expression modeling will keep fragmenting:

- Private writing samples will be pasted into prompts and app configs.
- Publishing, agent, memory, and brand systems will each compile competing voice models.
- AI-assisted samples will contaminate human-origin profiles without explicit weighting.
- Downstream consumers will need raw corpus access to get useful style guidance.
- Users will have no portable profile they own, audit, diff, or regenerate.
- Public contributors will lack a safe reference implementation for owner-operated expression
  profiling.

## Product Thesis Verdict

The thesis is coherent and strong enough for schema work.

The essential product is not "AI that writes like you." It is "a public-safe compiler that turns
evidence about expression into a portable, versioned, privacy-preserving profile."

Sprint 02 can proceed if schema work preserves that boundary.
