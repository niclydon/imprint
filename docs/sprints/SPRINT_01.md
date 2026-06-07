# Sprint 01 - Architecture and Product Definition

Primary Model: GPT 5.5
Adversarial Reviewer: Gemini (Antigravity)

## Mission
Determine what Imprint is, what it is not, and why it should exist as an independent project.

No implementation is allowed.

## Required Reading
- docs/PROJECT_STRATEGY.md
- docs/ARCHITECTURE.md
- docs/SECURITY_PRIVACY.md
- docs/ROADMAP.md
- docs/DECISIONS.md
- docs/PUBLIC_BUILD_GUIDE.md

## Product Thesis Validation
Answer:
- Why does Imprint exist?
- What problem exists today?
- Why do memory systems, PKGs, publishing systems, voice tools, and persona systems not solve it?
- Why should Imprint be independent?
- What happens if Imprint never exists?

Generate: PRODUCT_THESIS.md

## Canonical User Stories
Create at least 20 user stories across:
- writers
- personal AI builders
- researchers
- executives
- content creators
- brand teams
- product teams

Generate: USER_STORIES.md

## Ownership Matrix
For each capability determine owner, upstream dependencies, downstream consumers and rationale:
- ingestion
- storage
- embeddings
- classification
- signal extraction
- profile compilation
- drift
- evaluation
- export generation
- publishing
- persona generation

Generate: OWNERSHIP_MATRIX.md

## Five-Year Review
Assume Imprint v5.0 exists.
Identify future pain points, wrong abstractions, migration risks and stable contracts.

Generate: FIVE_YEAR_RISKS.md

## Public Open Source Audit
Assume 1000 GitHub stars and external contributors.
Identify hidden assumptions, private coupling and documentation gaps.

Generate: PUBLIC_ADOPTION_REVIEW.md

## Required Deliverables
- GAP_ANALYSIS.md
- RISKS.md
- IMPLEMENTATION_PLAN.md
- OPEN_QUESTIONS.md
- PRODUCT_THESIS.md
- USER_STORIES.md
- OWNERSHIP_MATRIX.md
- FIVE_YEAR_RISKS.md
- PUBLIC_ADOPTION_REVIEW.md

## Forbidden Work
- code
- schemas
- APIs
- connectors
- databases

## Adversarial Review Prompt
Assume the architecture is wrong.
Find hidden coupling, migration failures, privacy failures, scaling risks and conceptual flaws.
Generate ARCHITECTURE_CHALLENGE.md.

## Exit Criteria
No unresolved critical architectural questions remain.
