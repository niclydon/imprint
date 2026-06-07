# Architecture Decisions

Status: living document

## ADR-001: Imprint is a separate system, not a data-lake module

Decision: Imprint should live as an independent project/service rather than inside a personal data lake or memory system.

Rationale:

- The project should be public and reusable.
- The source data layer should be configurable.
- The expression compiler has multiple downstream consumers.
- Keeping it separate prevents the data lake from becoming an overbroad application host.

## ADR-002: Data systems are sources, not owners

Decision: Personal knowledge graphs, data lakes, and SQL databases are source systems for Imprint.

## ADR-003: Aesthetic pack systems consume profiles, they do not compile them

Decision: Aesthetic and identity pack systems consume Imprint profile fragments.

## ADR-004: Publishing systems apply voice, they do not own voice

Decision: Publishing systems consume profiles but do not maintain the canonical voice corpus.

## ADR-005: Voice is not one signal

Decision: Imprint models voice as multiple dimensions: lexical, tone, humor, structure, reasoning, narrative, platform fit, and anti-patterns.

## ADR-006: AI assistance is explicit provenance

Decision: Artifacts must classify AI assistance and authorship origin.

## ADR-007: Public examples are synthetic

Decision: All committed fixtures and example profiles must be synthetic.

## ADR-008: Raw examples are off by default in exports

Decision: Compiled profiles should not include raw artifact excerpts unless explicitly enabled.
