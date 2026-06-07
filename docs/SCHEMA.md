# Imprint Schema Plan

Status: planning

## Schema philosophy

The schema is the product contract. Everything else can change behind it.

Downstream systems should be able to consume an Imprint profile without knowing where the source data came from or seeing raw artifacts.

## Top-level profile shape

```json
{
  "imprint_version": "0.1",
  "profile_id": "example_subject_technical_longform",
  "subject": {},
  "profile_metadata": {},
  "source_summary": {},
  "identity": {},
  "expression": {},
  "voice": {},
  "reasoning": {},
  "structure": {},
  "platform_profiles": {},
  "anti_patterns": [],
  "sample_policy": {},
  "confidence": {},
  "drift": {},
  "exports": {}
}
```

## Subject

```json
{
  "subject": {
    "id": "example_subject",
    "display_name": "Example Subject",
    "profile_kind": "person",
    "consent_basis": "self",
    "locale": "en-US"
  }
}
```

For public examples, use fictional subjects only.

## Source summary

No raw private text required.

```json
{
  "source_summary": {
    "artifact_count": 1200,
    "included_count": 740,
    "quarantined_count": 380,
    "excluded_count": 80,
    "source_types": {
      "chat_message": 500,
      "email_sent": 300,
      "longform_article": 20,
      "transcript_segment": 100
    },
    "authorship_origin": {
      "human_origin": 600,
      "human_directed_ai_assisted": 100,
      "quoted_or_forwarded": 300,
      "unknown": 200
    }
  }
}
```

## Identity

```json
{
  "identity": {
    "stance": ["practitioner", "builder", "systems thinker"],
    "default_posture": "technical peer",
    "recurring_lens": [
      "operational reality over theory",
      "hidden system underneath visible behavior"
    ],
    "confidence": 0.84
  }
}
```

## Source policy

```json
{
  "sample_policy": {
    "include_raw_examples": false,
    "max_examples_per_section": 0,
    "source_weights": {
      "chat_message": {
        "lexical": 0.9,
        "tone": 0.8,
        "humor": 0.7,
        "structure": 0.1,
        "longform": 0.0
      },
      "longform_article": {
        "lexical": 0.7,
        "tone": 0.7,
        "reasoning": 1.0,
        "structure": 1.0,
        "longform": 1.0
      }
    }
  }
}
```

## Anti-patterns

```json
{
  "anti_patterns": [
    {
      "name": "generic_ai_conclusion",
      "description": "Ends with broad, obvious lesson unsupported by the specific evidence.",
      "severity": "high"
    },
    {
      "name": "corporate_thought_leadership",
      "description": "Uses polished but empty business language instead of operational specificity.",
      "severity": "medium"
    }
  ]
}
```

## Validation requirements

- No raw examples unless explicitly enabled.
- No private identifiers in public-safe mode.
- Every signal must include confidence.
- Every signal should include support metadata.
- Unknown authorship origin must reduce confidence.
- AI-assisted origin must be represented explicitly.
- Source weights must be visible in the profile.
