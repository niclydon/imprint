# Imprint Roadmap

Status: current as of Sprint 11

Imprint has moved past the original planning roadmap. The public repository now contains the core expression-profile pipeline and the first safe downstream contract surfaces.

## Completed foundation

The following layers are implemented, documented, tested, and reviewed:

- public-safe project foundation
- schema contracts
- local artifact adapters
- classification engine
- signal extraction engine
- profile compiler
- public-safe JSON and Markdown exports
- first-run “What Imprint Learned” output
- Mosvera expression overlay export
- consumer contracts for Mosvera, Broadside, agents/apps, and CLI/human inspection
- generic private connector framework with dry-run, redaction, and synthetic-only examples
- public website at `imprint.niclydon.dev`
- public developer-preview packaging, quickstart, install docs, CI, and synthetic example exports

## Current public-MVP track

### Phase 10 — Public web presence and launch polish

Goal: keep the public site, README, docs, and social-share assets aligned with the implemented architecture.

Deliverables:

- deployed single-page public site
- dark/light visual assets
- favicon and app icon
- Open Graph image and social metadata
- current implementation status
- links to GitHub and core docs
- clear privacy/local-first positioning
- current roadmap and quickstart alignment

Exit criteria:

- live site describes what exists today
- README and website agree
- social previews render cleanly
- no stale sprint/status language remains
- no private infrastructure details are exposed

### Phase 11 — Packaging and install experience

Goal: make the public developer preview easy for a stranger to install and run against synthetic data.

Status: complete as of Sprint 11.

Deliverables:

- verified clean install path
- package metadata cleanup
- quickstart command sequence
- `imprint init` or equivalent bootstrap UX
- synthetic sample project / corpus
- documented run path from synthetic artifacts to profile export
- clear CLI help output
- GitHub Actions CI for tests and lint/type checks if appropriate
- release checklist for `v0.1.0`

Exit criteria:

- a new user can clone, install, run the synthetic example, and inspect exports without private infrastructure
- all examples are synthetic
- no provider credentials are required for baseline operation
- README quickstart works copy-paste

### Phase 12 — Evaluation and quality gates

Goal: make profile changes reviewable before release or downstream consumption.

Status: complete as of Sprint 12.

Deliverables:

- export validation command
- profile comparison / diff basics
- regression corpus using synthetic examples
- validation report format
- compatibility warning checks
- confidence/version drift checks
- fixture-based quality gate for public-safe exports

Exit criteria:

- profile/export changes can be compared deterministically
- compatibility warnings are visible and testable
- regressions in privacy, source IDs, raw-text leakage, or claim boundaries fail tests

### Phase 13 — Private adapter strategy

Goal: define safe source-specific implementation plans for real private adapters without adding private assumptions to public core.

Deliverables:

- Gmail threat model and connector plan
- iMessage/export threat model and connector plan
- transcript/Plaud/Looki threat model and connector plan
- database/cloud connector threat model templates
- credential storage rules
- consent and multi-person-source policy
- replay/audit behavior
- synthetic fixture requirements for each adapter class

Exit criteria:

- no private adapter starts without a source-specific threat model
- credential and consent boundaries are explicit
- each future adapter has synthetic fixtures and redaction tests before implementation

### Phase 14 — Service/API mode and automation

Goal: optionally run Imprint as a lightweight local/private service for multiple downstream consumers.

Deliverables:

- service/API design doc
- local-only service mode decision
- health endpoint
- export delivery mechanism, such as file-drop or webhook
- scheduled harvest/profile rebuild plan
- metrics and audit events
- authentication/authorization policy for private deployments
- parity tests between batch CLI and service output

Exit criteria:

- service mode does not weaken local-first/privacy boundaries
- downstream tools can fetch current public-safe profiles without raw corpus access
- batch and service outputs remain equivalent and versioned

## Later backlog

- interactive artifact review UI
- profile editor
- profile merge and branch support
- richer context-profile management
- consent-aware multi-person profiles
- profile signing / provenance attestations
- local-only embedding index
- browser extension for public writing samples
- Obsidian plugin
- richer Mosvera/Broadside adapters outside core Imprint

## Boundary rule

Imprint compiles expression profiles. It does not become a memory system, data lake, writing assistant, publishing platform, model router, Mosvera runtime, or private-source SaaS.
