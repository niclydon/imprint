# Open Questions

Status: Sprint 01 output
Sprint 02 blocker status: no critical blockers

## Critical Questions

None remain that block Sprint 02.

The architecture has a coherent product boundary and enough planning detail to begin schema work.
The questions below should be answered during Sprint 02 or before public release.

## Sprint 02 Questions

### Evidence

- What exact support metadata is required for every signal?
- Does support include artifact IDs, source-type counts, time windows, example hashes, or all of
  these?
- How can evidence be auditable without leaking raw text?
- Are evidence references stable across profile rebuilds?

### Confidence

- Is confidence statistical, model-derived, heuristic, or hybrid?
- Should confidence be decomposed into attribution confidence, extraction confidence, evidence
  strength, and source diversity?
- How should unknown authorship origin affect confidence?
- What confidence floor should suppress a signal from first-run reports?

### Claim Levels

- Should every signal declare `observation`, `bounded_interpretation`, or `prohibited`?
- Should prohibited claims fail validation, quarantine the signal, or both?
- Which words are too interpretive for public-safe reports without supporting evidence?

### Master and Derived Profiles

- Do derived profiles inherit from a master profile or compile independently from filtered signals?
- What happens when a casual profile and technical profile disagree?
- Can downstream consumers request a blend, or should Imprint export separate profiles only?

### Raw Content Policy

- Can local-only full mode include raw examples?
- If raw examples are enabled, should they be capped, redacted, and separately marked?
- Should public-safe mode validate that no raw sample-like strings exist in exports?

### Versioning

- What is the difference between schema version, profile version, extractor version, model version,
  and export version?
- Which changes require profile regeneration?
- Which changes require migration?
- Which changes only require export regeneration?

## Product Questions

- Is "identity" the right term, or does it invite overclaiming?
- Should the first-run report avoid the word "identity" entirely and focus on expression?
- Is the first run allowed to compare contexts if evidence is uneven?
- What minimum evidence threshold is needed before saying "technical writing differs from casual
  writing"?
- Should Imprint include an explicit consent model for team, executive, and brand profiles in the
  first schema generation?

## Public Adoption Questions

- Which docs are normative for contributors?
- Should missing source docs be generated before or after Sprint 02?
- What public launch license and acceptable-use stance should the repo use?
- How should contributors test privacy behavior without private data?
- What should the project do when users request clone, diagnosis, or surveillance use cases?

## Deferred Questions

These should not block Sprint 02:

- Whether to implement service mode.
- Which private connectors to prioritize.
- Whether to support embeddings in the MVP.
- Whether to support profile signing.
- Whether to include a web UI.
- Whether to publish package distributions.

## Answering Standard

Every answer should preserve the core boundary:

```text
Imprint compiles evidence-backed expression profiles.
It does not become memory, publishing, diagnosis, cloning, or a private data lake.
```
