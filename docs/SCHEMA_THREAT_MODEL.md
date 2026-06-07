# Schema Threat Model

Status: Sprint 02 schema contract

## Profile Poisoning

Risk: malicious or unrepresentative artifacts skew a profile.

Schema controls: artifact classification, source policy, authorship origin, evidence references, quarantine counts, confidence components, and source diversity.

## Attribution Failures

Risk: quoted, forwarded, assistant-authored, parser-uncertain, or mixed-authorship material is attributed to the subject.

Schema controls: explicit authorship-origin categories, origin reasons, attribution confidence, source-policy actions, and quarantine states.

## AI Contamination

Risk: AI-generated or AI-assisted material becomes ground truth about a person.

Schema controls: suspected AI-assisted and assistant-output categories, detector output as weak metadata only, policy weights, and confidence reduction.

## Prompt Injection

Risk: artifact text contains instructions that influence extractors or downstream consumers.

Schema controls: core profiles do not contain generation prompts or provider decoding controls; evidence references can record prompt-injection risk metadata without executing instructions.

## Multi-User Confusion

Risk: artifacts from multiple people or organizations collapse into one profile.

Schema controls: subject IDs, source IDs, authorship-origin categories, mixed-authorship labels, artifact references, and source-policy filters.

## Export Scope Creep

Risk: core exports become prompt-generation artifacts.

Schema controls: export projection metadata, forbidden generation-control fields, public-safe claim validation, and separation of downstream adapter concerns.
