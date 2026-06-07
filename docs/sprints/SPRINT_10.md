# Sprint 10 - Public Web Presence

Primary Model: GPT 5.4
Reviewer: GPT 5.5
Status: **Complete** — 2026-06-07 (`imprint.niclydon.dev` live; glass overlay, Forge OG, mobile nav, dual theme)

## Mission

Create a single-page public landing site for Imprint at `imprint.niclydon.dev`.

The page should explain the project, give people something useful to share, and visually align with the README hero and Imprint aesthetic.

This is not an Imprint application UI.

## Required Reading

- `README.md`
- `docs/README.md`
- `docs/PRODUCT_POSITIONING.md`
- `docs/PROFILE_THEORY.md`
- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/assets/imprint-hero.png`
- `docs/assets/imprint-brand-board.png`

## Required Deliverables

- single-page landing page at `imprint.niclydon.dev`
- concise public description
- GitHub repository link
- favicon
- app icon / touch icon
- Open Graph image
- Twitter/X card image and metadata
- social preview metadata for LinkedIn, Bluesky, Discord, iMessage
- pre-release/open-source status messaging
- local-first/privacy positioning

## Visual Direction

Use an Imprint-specific aesthetic:

- niclydon.dev style/theme/modern layout feel
- niclydon.io color language
- dark graphite background
- cerulean and cyan primary accents
- amber punctuation
- evidence fragments, provenance lines, structured profile/blueprint imagery
- minimal image text

Avoid:

- brains
- faces
- robots
- digital twin imagery
- dashboards
- infographics as the hero
- marketing funnel language

## Content Requirements

The page should explain:

- what Imprint is
- what it is not
- why evidence-backed expression profiles matter
- current pre-release status
- how it differs from writing assistants, memory systems, and digital twins
- where to find the GitHub repo

## Non-Goals

Do not implement:

- corpus upload
- authentication
- profile generation
- dashboards
- API backend
- private connectors
- analytics requiring invasive tracking

## Exit Criteria

Sprint is complete when:

- `imprint.niclydon.dev` renders publicly — **done 2026-06-07** (`32f4faf`, Vercel project `imprint`)
- GitHub README links to the site — **done**
- social cards render correctly — **done** (`web/og.png` via Forge `gpt-image-2` txt2img; re-scrape recommended after OG swap)
- favicon and OG assets work — **done**
- page communicates pre-release/open-source/local-first posture — **done**
- no private data or private infrastructure details are exposed — **done**

**Beyond original exit criteria (same day):** mobile nav drawer (`b60506b`), light/dark theme toggle, Mosvera `palette_light` on aesthetic `imprint`.

**Full story:** `docs/narrative/2026-06-07-sprint-10-public-web-presence.md`
