# Implementation Plan

Status: Sprint 01 output
Scope: architecture-to-schema handoff, not implementation code

## Readiness Decision

Sprint 02 can begin.

The architecture is coherent enough for schema work if Sprint 02 treats schemas as product
contracts rather than implementation objects.

## Non-Negotiable Constraints

- Do not add private connectors before public-safe local adapters.
- Do not require cloud providers for default behavior.
- Do not include raw examples in public-safe exports.
- Do not treat AI detection, speaker attribution, or confidence as certain truth.
- Do not generate diagnosis, personality claims, or intent claims.
- Do not let publishing, memory, persona, or brand workflows own core profile compilation.

## Sprint 02: Schema and Contract Design

Primary goal: define the language of the platform.

Deliverables:

- schema philosophy
- signal taxonomy
- confidence model
- evidence model
- versioning policy
- migration strategy
- profile stability policy
- schema threat model

Critical decisions:

- How artifact, classification, signal, profile, export, drift, source policy, and authorship
  policy objects relate.
- What support metadata every signal requires.
- How claim level is represented.
- How sample policy prevents raw text leakage.
- How derived profiles inherit from or diverge from master profiles.
- How public-safe, private-local, and full-local export modes differ.

Exit gate:

- A downstream consumer can understand the profile contract without knowing source internals.
- A privacy reviewer can verify that public-safe output contains no raw private artifacts.
- A maintainer can explain confidence semantics without pretending precision.

## Sprint 03: Registry and Local Adapters

Primary goal: ingest synthetic local artifacts without private dependencies.

Deliverables:

- local text, Markdown, JSONL, and transcript JSON adapters
- artifact normalization
- local registry
- synthetic fixtures
- adapter tests

Exit gate:

- Synthetic corpus can be harvested and normalized deterministically.
- Unknown speakers, quoted content, assistant output, and template-like records can be represented
  without influencing profiles yet.

## Sprint 04: Classification

Primary goal: classify artifacts before extraction.

Deliverables:

- speaker confidence
- authorship origin
- AI-assistance risk
- quote/forward/template/notification classification
- usable signal dimensions
- privacy sensitivity

Exit gate:

- High-risk artifacts can be quarantined.
- Classifications explain why an artifact is included, excluded, or down-weighted.

## Sprint 05: Signal Extraction

Primary goal: extract bounded observations.

Deliverables:

- lexical, tone, humor, reasoning, structure, narrative, platform fit, and anti-pattern signals
- support metadata
- confidence metadata
- no-LLM baseline where possible
- optional provider-backed extraction

Exit gate:

- Signals are observations or explicitly bounded interpretations.
- Prohibited diagnoses cannot enter compiled profiles.

## Sprint 06: Profile Compiler

Primary goal: compile versioned profiles from signals.

Deliverables:

- source weighting
- quarantine and exclusion mechanics
- confidence aggregation
- master profile
- derived context profiles
- drift notes
- first-run report inputs

Exit gate:

- The same synthetic corpus and settings produce stable profile output.
- Raw samples remain excluded by default.

## Sprint 07 and 08: Exports

Primary goal: make profiles useful downstream without coupling the core to consumers.

Deliverables:

- canonical Imprint JSON/YAML
- human-readable Markdown report
- Mosvera-compatible fragment
- publishing profile contract fragment
- export validation

Exit gate:

- Consumers can use profile outputs without direct corpus access.
- Consumer-specific exports are projections, not alternate profile sources of truth.
- Downstream adapters own prompt assembly and generation behavior.

## Sprint 09+: Private Connectors

Primary goal: support private deployments through generic, configurable adapters.

Deliverables:

- connector interface
- SQL, sent mail, chat export, transcript, and AI conversation skeletons
- synthetic connector fixtures
- local config and env var validation

Exit gate:

- No connector contains private paths, table names, source names, person identifiers, or secrets.
- Connectors can be disabled and tested without private services.

## Documentation Work Before Public Release

- Add or retire missing expected docs:
  - `docs/COMPETITIVE_ANALYSIS.md`
  - `docs/PRODUCT_POSITIONING.md`
  - `docs/MEMORY_DISCIPLINE.md`
  - `docs/EVIDENCE_AND_CONFIDENCE.md`
  - `docs/PRIVACY_AND_LOCAL_MODE.md`
- Add a docs index that marks normative, historical, and sprint-specific documents.
- Add public policy files listed in architecture docs if absent.
- Run working-tree and history scans before publishing.

## Implementation Discipline

Implement the smallest version that validates the contract:

1. public-safe local mode
2. synthetic corpus
3. deterministic baseline
4. explicit evidence and confidence
5. canonical export
6. first-run report

Avoid service mode, private connectors, rich downstream adapters, and advanced drift until the
profile contract proves stable.
