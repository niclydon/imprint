# Imprint Schema Plan

Status: planning

## Schema philosophy

The schema is the product contract. Everything else can change behind it.

Downstream systems should be able to consume an Imprint profile without knowing where the source data came from or seeing raw artifacts.

## Sprint 01.5 terminology decision

Schema-level contracts should avoid broad `identity` claims.

Use:

- `expression_profile`
- `expression_posture`
- `rhetorical_patterns`
- `voice`
- `context_profiles`

Do not use machine-readable `identity.stance`, `identity.recurring_lens`, or personality-like
fields. Product prose may explain that Imprint serves identity and expression, but schemas should
model observable expression patterns only.

## Top-level profile shape

```json
{
  "imprint_version": "0.1",
  "profile_id": "example_subject_technical_longform",
  "subject": {},
  "profile_metadata": {},
  "build_manifest": {},
  "source_summary": {},
  "artifact_storage": {},
  "expression_profile": {},
  "expression_posture": {},
  "rhetorical_patterns": {},
  "voice": {},
  "reasoning": {},
  "structure": {},
  "context_profiles": [],
  "anti_patterns": [],
  "sample_policy": {},
  "evidence_policy": {},
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
      "unknown_speaker": 120,
      "missing_metadata": 80
    }
  }
}
```

## Expression posture

```json
{
  "expression_posture": {
    "claim_level": "observation",
    "patterns": [
      {
        "name": "evidence_before_generalization",
        "description": "Often introduces concrete operational evidence before summarizing.",
        "confidence": {
          "display": 0.84,
          "evidence_strength": 0.88,
          "attribution": 0.92,
          "extraction": 0.78
        },
        "support": {
          "artifact_count": 42,
          "source_types": ["technical_note", "article"],
          "date_range": "2025-01 to 2026-05"
        }
      }
    ]
  }
}
```

This shape is intentionally observation-based. It does not claim the subject "is analytical" or
has a fixed personality stance.

## Build manifest

Every profile build should record enough metadata to distinguish expression drift from compiler or
corpus drift.

```json
{
  "build_manifest": {
    "schema_version": "0.1",
    "compiler_version": "0.1.0",
    "classifier_version": "0.1.0",
    "extractor_family": "rule_baseline",
    "extractor_major_version": 0,
    "extractor_minor_version": 1,
    "extractor_prompt_version": "rule-baseline",
    "extractor_code_version": "0.1.0",
    "profile_affecting_model_invocations": [],
    "source_policy_version": "0.1",
    "authorship_policy_version": "0.1",
    "export_schema_version": "0.1",
    "artifact_store_mode": "metadata_only",
    "config_hash": "example-hash"
  }
}
```

## Artifact storage

Profiles should record whether raw content is locally available for audit and regeneration.

```json
{
  "artifact_storage": {
    "mode": "metadata_only",
    "raw_content_available": false,
    "public_safe_export": true
  }
}
```

Allowed modes are planned in `docs/ARTIFACT_STORAGE_POLICY.md`.

## Context profiles

Context profiles are explicit compiled views. They reference a baseline and declare filters rather
than using hidden inheritance.

```json
{
  "context_profiles": [
    {
      "profile_id": "example_subject_technical",
      "baseline_profile_id": "example_subject_master",
      "context": "technical",
      "filters": {
        "artifact_types": ["technical_note", "article"]
      },
      "divergences": []
    }
  ]
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
- Every profile must include build manifest metadata.
- Every signal must include a claim level.
- Prohibited claims must fail validation or be quarantined before compilation.
- Derived/context profiles must declare baseline references and filters.

Claim validation is mandatory, not advisory. Canonical and public-safe exports must fail if a
prohibited claim survives compilation. Private-local workflows may quarantine rejected claims for
review, but must not export them as profile guidance.

## Sprint 02.5 Model Provider Policy

Canonical schemas are provider-neutral. Imprint is BYOM/BYOP and does not assume any single hosted or local inference stack.

Build manifests should record profile-affecting model invocations as structured metadata: model role, provider kind, provider name, base URL kind without secrets, model name and version, prompt or policy version, decoding policy, seed if supported, capability flags, local versus remote execution, and known retention/training policy.

Core profile exports must remain profile projections, not generation-ready prompts. Experience-only generation can produce reports, summaries, demos, or first-run artifacts, but those outputs do not mutate durable profiles unless explicitly promoted through validated evidence.
