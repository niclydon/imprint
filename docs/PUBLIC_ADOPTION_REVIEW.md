# Public Adoption Review

Status: Sprint 01 output
Scenario: public repository with 1000 GitHub stars and external contributors

## Verdict

Imprint is plausible as a public-first open-source project, but only if the public/private boundary
is enforced as a product requirement rather than a maintainer preference.

## What External Contributors Will Understand

The current docs make several things clear:

- Imprint is an identity and expression compiler.
- Public examples must be synthetic.
- Private deployment details belong in config.
- Raw samples are not the product.
- Profiles are versioned.
- AI assistance and speaker attribution are important.
- Downstream tools consume profiles rather than raw artifacts.

This is enough to orient serious contributors.

## What Will Confuse Contributors

### Too Many Planning Docs Without a Normative Index

The repo contains architecture docs, sprint prompts, roadmap docs, and narrative notes. A
contributor needs a docs index that says which files are:

- normative architecture
- sprint outputs
- historical narrative
- future work
- implementation guides

### Missing Expected Docs

The preflight checklist and Sprint 01 prompt reference docs that are absent:

- `docs/COMPETITIVE_ANALYSIS.md`
- `docs/PRODUCT_POSITIONING.md`
- `docs/MEMORY_DISCIPLINE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`

Either add them or update prompts/checklists to point to the Sprint 01 outputs that supersede
them.

### Product Name History

`PROJECT_STRATEGY.md` mentions a previous repository name. That is acceptable during planning, but
public-facing docs should not force contributors to understand internal rename history.

### Schema Plan Exists Before Sprint 02

`docs/SCHEMA.md` already sketches top-level shape. Sprint 02 should treat it as planning input, not
approved contract.

## Hidden Private Coupling Risks

- Source adapter examples may accidentally reflect one operator's corpus shape.
- SQL connector docs may include unique private table concepts.
- First-run examples may copy private expression cadence.
- Export names may align too closely with one downstream private consumer.
- Local config examples may include realistic-looking paths that reveal private infrastructure.

## Public-First Requirements

Before public release:

- Add `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md` if absent.
- Add a docs index.
- Add or resolve missing expected planning docs.
- Run secret scan against working tree and git history.
- Run private-string scan against docs, examples, tests, and history.
- Verify all examples are synthetic.
- Verify default config uses local-only, no-network behavior.
- Verify public-safe exports contain no raw examples.
- Verify tests run without credentials.

## Contributor Guidance Needed

The project should tell contributors:

- how to add a signal family
- how to reject a proposed signal family
- how to add a connector safely
- how to write synthetic fixtures
- how to validate no raw content leaks
- how to handle AI-assisted artifacts
- how to phrase observations without diagnosis
- how downstream export PRs should avoid owning generation behavior

## Likely Misuse Requests

Public contributors and users may ask for:

- clone behavior
- personality typing
- mental health inference
- employee monitoring
- relationship analysis
- ghostwriting automation as the core product
- scraping public social profiles without consent
- detector-based accusations of AI use

Default answer: these are outside Imprint unless reframed as consent-based, evidence-backed,
expression-profile compilation with strict boundaries.

## Market Lessons for Public Positioning

Current products make the positioning sharper:

- Writing tools prove voice-fit matters.
- Brand platforms prove organizations pay for consistency.
- Memory layers prove persistent context is infrastructure.
- Digital-mind tools prove personal representation has demand and risk.
- AI-detection tools prove authorship uncertainty matters.

Reference set: Spiral, Jasper, WRITER, Personal AI, Delphi, Zep, Mem0, and Originality.ai public
product or documentation pages listed in `docs/PRODUCT_THESIS.md`.

Imprint should position against the gap between these categories:

```text
Not a writer. Not a clone. Not a memory store.
A local-first expression profile compiler with provenance.
```

## Adoption Health Metrics

Public adoption should be measured by:

- successful local quickstart runs
- profile builds from synthetic corpus
- number of downstream consumers using canonical exports
- privacy scan pass rate
- schema migration success
- contributor PRs that add fixtures without private leakage
- issues resolved by docs rather than maintainer tribal knowledge

Do not measure success primarily by:

- generated content volume
- monetization
- number of private connectors
- number of raw artifacts stored
- clone realism

## Final Public Adoption Decision

The project can be public-first if maintainers keep the boundary strict. The most important public
artifact after Sprint 02 will be a schema and docs set that makes unsafe contributions obviously
out of scope.
