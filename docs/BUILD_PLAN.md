# Imprint Build Plan

This document contains the sprint-by-sprint model strategy.

Sprint 1
- Primary: GPT 5.5
- Adversarial Reviewer: Gemini (Antigravity)
- Goal: architecture, boundaries, risks, implementation plan.

Sprint 2
- Architect: GPT 5.5
- Implementer: GPT 5.4
- Adversarial Reviewer: Gemini (Antigravity)
- Goal: schemas, contracts, versioning.

Sprint 3
- Primary: GPT 5.4
- Adversarial Reviewer: Claude
- Goal: artifact registry and local adapters.

Sprint 4
- Primary: GPT 5.5
- Adversarial Reviewer: Gemini (Antigravity)
- Goal: classification engine.

Sprint 5
- Primary: GPT 5.5
- Adversarial Reviewer: Claude
- Goal: signal extraction.

Sprint 6
- Primary: GPT 5.5
- Adversarial Reviewer: Gemini (Antigravity)
- Goal: profile compiler.

Sprint 7
- Primary: GPT 5.4
- Adversarial Reviewer: GPT 5.5
- Goal: Mosvera exporter.

Sprint 8
- Primary: GPT 5.4
- Adversarial Reviewer: GPT 5.5
- Goal: publishing exports.

Sprint 9+
- Primary: GPT 5.4
- Repetitive implementation: Codex Spark
- Adversarial Reviewer: Grok Build
- Goal: private connectors.

See chat history for the detailed prompts; expand this file later into the full runbook.

# Phase 7 / Sprint 10 - Public Web Presence

Primary Model: GPT 5.4
Reviewer: GPT 5.5
Status: **Complete** — 2026-06-07

Goal:
Create the single-page public web presence for `imprint.niclydon.dev`.

Deliverables:
- landing page — **shipped** (`web/`, https://imprint.niclydon.dev)
- favicon/app icon — **shipped**
- Open Graph image — **shipped** (Forge `gpt-image-2` txt2img, `web/og-gen.json`)
- social metadata — **shipped**
- README/repo links — **shipped**
- concise public positioning copy — **shipped**
- mobile navigation + light/dark theme — **shipped** (`b60506b`, stretch goal)

Boundary:
This is a public project landing page, not a product UI and not a corpus/profile interface.

Narrative: `docs/narrative/2026-06-07-sprint-10-public-web-presence.md`

