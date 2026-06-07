# Five-Year Risks

Status: Sprint 01 output
Scenario: Imprint v5.0 exists and has real users, contributors, private deployments, and multiple
downstream consumers.

## Executive Summary

The largest five-year risk is not that Imprint fails to add enough features. It is that Imprint
adds too many adjacent responsibilities and loses the clean expression-compiler contract.

## Wrong Abstractions

### Identity Object Becomes Too Broad

If `identity` accumulates biography, values, preferences, memories, relationships, and personality
claims, the schema will become unsafe and incoherent.

Stable contract: identity should stay limited to expression-relevant, evidence-backed posture and
profile subject metadata.

### Signal Taxonomy Becomes a Junk Drawer

New signal families will be tempting: persuasion, leadership, emotional state, worldview,
creativity, neurotype, credibility. Many should be rejected or represented only as bounded
observations.

Stable contract: every signal needs evidence requirements, non-examples, claim level, confidence,
and support metadata.

### Derived Profiles Become Inconsistent

Five years in, users may have dozens of derived profiles: casual, executive, podcast, newsletter,
technical, investor, support, social. If inheritance rules are weak, exports will contradict each
other.

Stable contract: derived profiles need explicit source filters, inherited fields, overrides, and
conflict handling.

### Exporters Become Product Forks

Consumer-specific exporters may evolve their own vocabulary and capabilities. If a Mosvera export
and publishing export disagree about voice, the canonical profile has failed.

Stable contract: canonical Imprint profile first; exporters are projections.

## Migration Risks

### Early Schema Names Survive Too Long

Poor names in v0.1 may become locked into downstream systems. Sprint 02 should spend real time on
names, not just fields.

### Confidence Semantics Change

If confidence begins as one number and later splits into attribution, extraction, evidence, and
agreement confidence, old profiles may be misread.

Mitigation: version confidence semantics explicitly from the start.

### Authorship-Origin Taxonomy Expands

AI-writing workflows will keep changing. The authorship-origin enum must support unknown,
mixed-origin, and future categories without breaking old exports.

### Raw Content Policy Changes

Users may request richer examples over time. If public-safe, private-local, and full-local modes
are not explicit early, migration could accidentally expose raw samples.

## Privacy Failures

### Public Examples Derived From Private Cadence

Even fictional examples can leak if they preserve private cadence, unusual phrases, or metadata
patterns. Synthetic generation needs its own hygiene policy.

### Private Connectors Normalize Bad Defaults

Private connectors can silently shape the core around one operator's data model. Connector
interfaces must remain generic, and connector tests must use synthetic data.

### Profile Exports Become Too Revealing

A profile can leak sensitive information without raw quotes. Source counts, time windows, platform
labels, and anti-patterns can reveal behavior. Public-safe mode needs conservative metadata.

## Scaling Risks

### Large Corpora Create False Confidence

More artifacts do not automatically mean stronger evidence. A large low-quality corpus can drown
out a smaller high-quality source.

### Longitudinal Drift Becomes Noisy

Drift can reflect real expression change, source mix change, model change, extractor change, or
AI-assistance contamination. Drift reports must separate these causes.

### Contributor Ecosystem Adds Unsafe Connectors

A public project with many stars will attract connector PRs. Review policy must reject hard-coded
private details and ambiguous consent assumptions.

## Stable Contracts

These should remain stable across five years:

- Artifact provenance is explicit.
- Authorship origin is explicit.
- Speaker confidence is explicit.
- Signals are evidence-backed and claim-labeled.
- Profiles are versioned.
- Raw examples are off by default.
- Public examples are synthetic.
- Canonical profile exports are source of truth.
- Downstream systems consume profiles, not raw corpus.
- Imprint does not diagnose, clone, publish, or act as a memory system.

## v5.0 Success Criteria

Imprint v5.0 is successful if:

- users can still run it locally without private infrastructure
- public contributors can test it with synthetic fixtures
- downstream systems can migrate across profile versions
- private deployments can add sources without changing core code
- profile outputs remain auditable without exposing raw content
- the project still explains itself as an expression compiler in one sentence
