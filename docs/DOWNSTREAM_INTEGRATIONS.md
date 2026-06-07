# Downstream Integrations

Status: planning

## Integration principle

Downstream systems should consume compiled profiles, not raw private artifacts.

Imprint exports structured expression profiles. Consumers decide how to apply them.

## Aesthetic pack systems

Role: identity and aesthetic packaging.

Imprint should export a voice/expression fragment that an aesthetic pack system can merge into a resolved identity pack.

The aesthetic system should own final pack resolution. Imprint should not own visual identity.

## Publishing systems

Role: publishing and draft generation.

Publishing systems should consume either:

1. a resolved pack that includes Imprint voice data, or
2. a publishing-specific prompt contract export from Imprint.

Publishing systems should not own voice compilation.

## Model routers

Role: model capability provider.

Imprint may call an OpenAI-compatible endpoint for classification, extraction, embeddings, or evaluation. Model routers should not own expression profiles.

## Media systems

Role: speaker identification and transcript production.

Media systems can provide speaker-attributed transcript segments. Imprint then decides how those transcript artifacts contribute to expression profiles.

## Export modes

### Public-safe

No raw private examples. Suitable for public demos.

### Private-local

May include redacted examples and richer source support metadata.

### Full-local

May include raw examples. Must be local-only and ignored.

## Integration anti-patterns

Avoid:

- Downstream systems reading raw private messages directly.
- Publishing systems maintaining competing voice corpora.
- Aesthetic systems ingesting private data directly.
- Model routers embedding private identity assumptions.
- Exported profiles containing raw corpus text by default.
