# Risks

Status: Sprint 01 output

## Critical Risks

No unresolved critical architectural risks block Sprint 02. The critical risks below are release
blockers if they appear in implementation.

### Private Data Leak

Risk: private artifacts, paths, identifiers, profiles, screenshots, or credentials enter the
public repo.

Controls:

- synthetic examples only
- ignored local config, data, exports, and private directories
- secret and private-string scanning before public push
- public-safe export mode as default
- no raw examples unless explicitly enabled in local-only mode

### Wrong Speaker Compilation

Risk: Imprint compiles someone else's words into the subject's profile.

Controls:

- speaker confidence on every artifact
- quote, forward, template, assistant-output, and unknown-origin quarantine
- source-specific attribution rules
- visible included/quarantined/excluded counts
- profile confidence penalties for weak attribution

### AI Contamination

Risk: AI-generated or AI-assisted text becomes treated as human-origin voice.

Controls:

- authorship-origin classification
- dimension-specific weighting
- assistant output excluded from voice signals by default
- AI-assisted samples retained only with explicit policy
- drift reports that can identify AI-era style changes

### Overclaiming About People

Risk: profile outputs drift from observable expression into personality, mental health, intent, or
identity diagnosis.

Controls:

- claim-level classification
- prohibited diagnosis validation
- weak observation preferred over strong interpretation
- first-run report framed as expression evidence, not personality assessment

## High Risks

### Imprint Becomes a Memory System

The architecture says Imprint is not memory, but storage and artifact registry work can quietly
expand. The test is simple: if a feature exists to answer arbitrary questions from remembered
facts, it is outside Imprint.

### Imprint Becomes a Writing Assistant

Export prompts and first-run reports can slide into draft generation. Imprint may export guidance
for writing systems, but writing systems should own generation.

### Schema Freezes Too Early

The schema is the product contract. A shallow Sprint 02 schema would lock in weak names,
over-broad objects, or missing evidence semantics. Versioning and migration must be designed before
schemas are implemented.

### Confidence Becomes Fake Precision

A numeric confidence score can look authoritative even when it blends heuristic, model-derived,
and statistical evidence. Sprint 02 must define what each confidence value means and what it does
not mean.

### First Run Feels Like a JSON Dump

If the first run prioritizes raw profile JSON, users will not understand the value. The report
should lead with "What Imprint Learned" and show supported observations before infrastructure
artifacts.

## Moderate Risks

### Contributor Confusion

The repo has many planning docs and sprint prompts. External contributors may not know which docs
are normative. Add a docs index or maintainer guide before public release.

### Over-Engineered MVP

The roadmap includes service mode, private connectors, drift, evals, and multiple exporters.
The MVP should stay CLI-first with local synthetic data and basic profile compilation.

### Under-Specified Local Mode

Local mode is central to trust. The default should not call cloud providers, require credentials,
or emit raw examples.

### Export Coupling

Mosvera, publishing, agent, and aesthetic pack exports can make Imprint depend on downstream
formats too early. Keep canonical Imprint JSON/YAML as the stable source of truth.

### Evaluation Ambiguity

Voice authenticity is subjective. Evaluation should distinguish schema validation, privacy
validation, evidence support, and downstream generation quality.

## Long-Term Risks

- Profile objects become too large for downstream systems.
- Derived profiles conflict with master profile guidance.
- Private connector framework invites unsafe convenience shortcuts.
- AI-detection models change and invalidate contamination assumptions.
- Public users expect "clone me" behavior and misread the product.
- Enterprise users pressure the project toward brand enforcement rather than expression
  compilation.

## Risk Posture

The current architecture has the right instincts: public-first, evidence-backed, profile-oriented,
and downstream-agnostic. The biggest risk is not conceptual incoherence. It is implementation drift.
