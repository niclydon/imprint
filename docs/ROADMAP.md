# Imprint Roadmap

Status: planning

## Phase 0 — Public-safe foundation

Goal: make the repository safe to publish before adding private connectors.

Deliverables:

- Project rename plan from internal name to Imprint.
- README rewritten around public product concept.
- `.env.example` with generic values only.
- `imprint.config.example.yaml` with synthetic sources.
- Public-safe `.gitignore`.
- Security and privacy docs.
- Synthetic fixture corpus.
- Schema-first profile format.
- CI that runs without private dependencies.

Exit criteria:

- Secret scan passes.
- No private corpus or deployment details in repo.
- A new user can run the synthetic example locally.

## Phase 1 — Core schemas and local MVP

Goal: compile a basic expression profile from local files.

Deliverables:

- Pydantic schemas for artifacts, classifications, signals, profiles, exports.
- Local Markdown/text/JSONL source adapters.
- SQLite artifact registry with explicit Artifact Store modes.
- CLI commands: `init`, `harvest`, `classify`, `extract`, `compile`, `export`, `audit`.
- Rule-based baseline extractors.
- Optional LLM extractor through OpenAI-compatible endpoint.
- JSON/YAML exporters.
- Human-readable Markdown report.

Exit criteria:

- Synthetic corpus produces stable profile output.
- Tests validate schemas and privacy defaults.
- No provider credentials required for basic mode.
- Profile builds record artifact storage mode and build manifest metadata.

## Phase 2 — Source weighting and contamination controls

Goal: make voice multi-dimensional instead of treating all samples equally.

Deliverables:

- Source policy config.
- Signal-dimension weights: lexical, tone, humor, reasoning, structure, narrative, longform.
- Authorship-origin classifier.
- AI-assistance risk classifier.
- Quote/forward/template classifier.
- Quarantine and exclusion mechanics.
- Profile confidence scoring.
- Drift baseline support.
- Compiler/corpus/expression drift separation.

Exit criteria:

- Chat-like samples can influence lexical/tone but not long-form structure.
- AI-assisted samples can be retained as low-weight or reference-only.
- Quarantined artifacts do not influence compiled profiles.
- Drift reports do not present model or extractor changes as expression drift.

## Phase 3 — Export adapters

Goal: make Imprint useful to downstream systems.

Deliverables:

- Aesthetic pack fragment exporter.
- Publishing profile contract exporter.
- Generic agent persona exporter.
- Profile diff command.
- Profile validation command.
- Export metadata with source counts and confidence.

Exit criteria:

- Downstream systems can consume exported profile JSON without direct corpus access.
- Exported artifacts contain no raw private text by default.
- Core exports remain profile contracts; downstream adapters own prompt assembly and generation.

## Phase 4 — Private connector framework

Goal: support private data sources without compromising public repo safety.

Deliverables:

- Connector interface.
- Local SQL connector using configured query files.
- Sent mail connector skeleton.
- Chat export connector skeleton.
- Transcript connector skeleton.
- AI conversation export connector skeleton.
- Connector test harness using synthetic fixtures.

Exit criteria:

- Connectors can be configured entirely outside the repo.
- Tests use fake data only.
- Each connector emits normalized artifacts with provenance.

## Phase 5 — Service mode and automation

Goal: run Imprint as a lightweight service for multiple consumers.

Deliverables:

- FastAPI service mode.
- Scheduled harvest jobs.
- Scheduled profile rebuilds.
- Webhook or file-drop export delivery.
- Prometheus metrics.
- Health endpoint.
- Basic auth or bearer token support for private deployments.

Exit criteria:

- Downstream tools can fetch the latest profile over HTTP.
- Batch and API modes produce equivalent profile versions.

## Phase 6 — Evaluation and quality gates

Goal: measure whether profiles improve downstream generation.

Deliverables:

- Blind A/B eval harness.
- Voice authenticity rubric.
- Drift reports.
- Anti-pattern detector.
- Platform fit scoring.
- Regression corpus using synthetic examples.

Exit criteria:

- Profile changes can be evaluated before release.
- Downstream output can be scored against profile rules.

## Phase 7 — Public release

Goal: publish a useful public project with safe defaults.

Deliverables:

- Public GitHub repository.
- Release v0.1.0.
- Quickstart docs.
- Example synthetic profile.
- Architecture diagram.
- Contributor guide.
- Security policy.
- Roadmap issues.
- Build-in-public launch post.

Exit criteria:

- Users can run the project without private infrastructure.
- Project purpose is clear.
- Privacy posture is credible.

## Backlog ideas

- Web UI for reviewing artifacts and quarantines.
- Interactive profile editor.
- Profile merge and branch support.
- Cross-profile comparison.
- Consent-aware multi-person profiles.
- Profile signing or provenance attestations.
- Local-only embedding index.
- Browser extension for collecting public writing samples.
- Obsidian plugin.
- Static-site profile viewer.
