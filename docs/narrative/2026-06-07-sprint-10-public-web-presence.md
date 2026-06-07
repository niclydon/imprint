# Sprint 10: Public Web Presence at imprint.niclydon.dev

Imprint had schema foundations, a profile compiler, and adversarial-reviewed signal extraction — but no public surface a stranger could visit, share, or link from a README without landing in a GitHub tree. Sprint 10's mission was to ship a single-page landing site at `imprint.niclydon.dev` that explains the project honestly, renders social previews correctly, and visually aligns with the README hero without becoming an application UI. By the end of the day the site was live on Vercel, dressed in an `ai-glass-futuristic` overlay on a frozen Imprint palette, carrying a Forge-generated Open Graph card, responsive mobile navigation, and a dual light/dark theme registered in the local Mosvera aesthetic `imprint`.

This is not the Imprint product. It is the project's front door.

## The stake: public-first without a public door

`docs/sprints/SPRINT_10.md` defined the boundary early. The page must explain what Imprint is and is not, link to GitHub, carry favicon and OG assets, and communicate pre-release / open-source / local-first posture. It must not implement corpus upload, authentication, profile generation, dashboards, API backends, private connectors, or invasive analytics.

The visual direction pulled from three sources named in the sprint doc:

- niclydon.dev layout feel (modern, spacious, credible)
- niclydon.io color language (graphite, cerulean, amber punctuation)
- `docs/assets/imprint-hero.png` (evidence fragments converging into structured profiles)

Hard rejects: brains, faces, robots, digital twins, dashboard heroes, marketing funnel copy, infographics-as-hero.

The README already linked to a hero image in `docs/assets/`. What was missing was the hostname, the HTML, the deploy path, and the social metadata chain that makes a URL pasteable in LinkedIn, Bluesky, Discord, or iMessage without embarrassing previews.

## Phase 1: Static ship (commit `32f4faf`)

The first cut landed as plain HTML and CSS under `web/`:

| File | Role |
|------|------|
| `web/index.html` | Single-page content: hero, about, pipeline, boundaries, differentiation, privacy, status |
| `web/styles.css` | Imprint palette, typography (Inter Tight / Inter / JetBrains Mono), layout |
| `web/favicon.svg`, `web/apple-touch-icon.png` | Favicon and touch icon |
| `web/hero.webp` | Hero background (derived from branded hero art) |
| `web/logo-mark.svg` | Header mark |
| `web/DEPLOYMENT.md` | Vercel + Cloudflare topology |

Social metadata was wired in `index.html` for Open Graph and Twitter/X: canonical URL `https://imprint.niclydon.dev/`, OG image path `/og.png`, title and description carrying the evidence-first positioning without in-image text on the OG asset (that constraint came later; the first OG was a crop).

Deploy topology:

- **Hosting:** Vercel project `imprint`, team `niclydon`
- **Root directory:** `web/` (also mirrored in repo-root `vercel.json` with `"outputDirectory": "web"`)
- **Framework:** Other — static, no build command
- **Domain:** `imprint.niclydon.dev`
- **DNS:** Cloudflare zone `niclydon.dev`, CNAME `imprint` → `cname.vercel-dns.com`, **DNS only** (grey cloud — proxying Vercel through Cloudflare risks TLS/redirect loops)

Commit `e56d1b1` added monorepo output configuration and `.gitignore` rules for local `.vercel` dirs.

First production URL: **https://imprint.niclydon.dev**

README gained the site link. Exit criteria from `SPRINT_10.md` — public render, README link, favicon, pre-release messaging — were met at this layer. Social card quality and visual polish were not.

## Phase 2: ai-glass-futuristic overlay (commit `b082536`)

The initial page read as competent static HTML. It did not yet carry the glassmorphism, atmosphere mesh, cinematic depth, and motion vocabulary that had been applied elsewhere in the niclydon estate (Castbook's `ai-glass-futuristic` structural DNA).

**Decision:** Apply `ai-glass-futuristic` overlay mechanics while **freezing** the Imprint palette. No warm cinematic-lab drift. Midnight `#111318`, electric `#5ba4cf`, cyan `#7ec8e3`, amber `#d4a853` stay fixed; what changes is structure — frosted `.glass` panels, cerulean/amber atmosphere gradients, blueprint grid, film grain, spotlit hero treatment, `.lift` hover with sheen sweep, staggered `.reveal` entrance.

Changes in `web/styles.css` and `web/index.html`:

- Fixed `.atmos` and `.grain` layers behind content
- Glass primitive with `backdrop-filter: blur(18px) saturate(140%)`
- Sticky glass header
- Hero panel as inline glass card over dimmed background image
- Section cards (pipeline, outcomes, compare panels, diff cards, privacy grid, status banner) upgraded to glass surfaces

**Mosvera registration (local, not in git):**

Because Mosvera MCP was not enabled in the Grok session, the aesthetic was written directly to the operator's local registry:

- `~/.config/mosvera/registry/template.imprint-base.json` — template `imprint-base`
- `~/.config/mosvera/registry/composition.imprint.json` — composition id `imprint`

The template captured palette, glass effects, motion (`320ms cubic-bezier(0.16, 1, 0.3, 1)`), imagery treatment, and voice strings. This makes the landing page a reference implementation of a named Mosvera aesthetic, not just a one-off CSS file.

Operator feedback on the glass overlay: positive — "look amazing" on the atmosphere and panel treatment. That feedback justified keeping the overlay as the canonical public face rather than reverting to flat sections.

## Phase 3: OG image — three generations

Social sharing needed a dedicated 1200×630 asset. The sprint required OG + Twitter card metadata; the image quality became a multi-iteration story.

### Attempt 1: ImageMagick crop from hero

Early `web/og.png` was cropped from hero source material. Functional for metadata tags, not aligned with the glass aesthetic story.

### Attempt 2: Forge img2img from hero (commit `c083c41`)

Route: Forge `http://127.0.0.1:8642` / `https://forge.niclydon.io` → `openai:gpt-image-2` with `docs/assets/imprint-hero.png` as reference, strength `0.35`. Produced a branded image closer to README hero language.

**Problem discovered later:** The hero-derived art had **"IMPRINT" baked into the image** on the left side. When that art served as the page background behind a centered glass hero panel, the panel obscured part of the word. Two competing brand signals — background poster vs. foreground card — read as a layout bug.

### Attempt 3: Pure txt2img gpt-image-2 (commit `97d3ee6`)

**Decision:** Replace img2img OG with a fresh **text-to-image** generation — no hero reference.

Metadata recorded in `web/og-gen.json`:

```json
{
  "model_used": "openai:gpt-image-2-q8",
  "dispatch_tier": "cloud-openai",
  "size_requested": "1536x832",
  "size_final": "1200x630",
  "mode": "txt2img",
  "notes": "No img2img reference. Title/description in HTML meta only."
}
```

Forge credentials loaded via `eval "$(~/projects/secrets-vault/bin/sv get forge)"` — keys never written to docs or git.

Final `web/og.png`: **970,028 bytes**. Same aesthetic family (document stream → holographic structure, Imprint palette) but **no in-image title text** — title and description live in HTML meta only, as required for OG hygiene.

Push note: commit `97d3ee6` initially failed push because `main` was behind remote; `git pull --rebase origin main` reconciled with merge commit `848622f`, then push succeeded as `97d3ee6` on rebased history.

## Phase 4: Hero background swap (commit `667d7e9`)

The centered glass hero panel blocking baked-in "IMPRINT" text was not fixable by nudging `object-position` alone — the poster composition assumed left-side branding, while the page layout assumed a centered content card.

**Decision:** Swap `web/hero.webp` for a WebP derivative of the txt2img OG art.

Conversion via ImageMagick:

```
convert og.png -define webp:method=6 -quality 82 hero.webp
```

| Asset | Dimensions | Size |
|-------|------------|------|
| `og.png` | 1200×630 | 970 KB |
| `hero.webp` (new) | 1200×630 | 58 KB |
| `hero.webp` (old, branded) | 1600×1067 | 114 KB |

CSS tuning in `web/styles.css`:

- `object-position: 58% 42%` — holographic tower right, calmer left band for the card
- `min-height: 32rem` on `.hero` — wide OG composition has vertical room
- Hero image opacity `0.44` (dark theme baseline)

**Outcome:** Landing page and social preview now share the same visual language. No duplicate "Imprint" word fight between background and foreground.

Rejected alternative: keep branded hero and only reposition — band-aid; document stream still competed with card legibility.

Rejected alternative: generate a separate 16:9 hero crop from the same prompt — best long-term, deferred as extra generation step; OG derivative was sufficient.

## Phase 5: Mobile navigation and dual theme (commit `b60506b`)

Two operator requests closed the sprint's UX gaps:

1. **Mobile-friendly version** — the page hid most nav links below 768px, leaving GitHub as the only visible link. No drawer, no touch-optimized CTAs, no safe-area handling.
2. **Light mode + navbar toggle** — dark-only presentation; no `prefers-color-scheme` respect, no manual override, no Mosvera light palette.

### Mobile

| Breakpoint | Behavior |
|------------|----------|
| ≤900px | Desktop nav hidden; hamburger opens slide-out drawer |
| ≤768px | Hero typography tightened, CTAs stack full-width, grids single-column |
| ≤520px | Brand mark shrinks, status pill compacts, footer links stack |

Implementation:

- `web/theme.js` — nav drawer open/close, backdrop click, Escape key, resize auto-close, link tap close
- `web/index.html` — `#nav-toggle`, `#nav-drawer`, `#nav-backdrop`, duplicate nav links in drawer
- `body.nav-open { overflow: hidden }` during drawer
- `env(safe-area-inset-*)` padding on header and drawer for notched phones
- Touch targets: buttons `min-height: 2.75rem` on small screens

### Light / dark theme

Theme system uses `data-theme="dark"|"light"` on `<html>`:

- Inline head script sets theme before first paint (prevents flash)
- `web/theme.js` persists choice in `localStorage` key `imprint-theme`
- Default: system `prefers-color-scheme` when no stored preference
- Navbar **sun/moon icon button** (`#theme-toggle`) — sun shown in dark mode (click → light), moon shown in light mode (click → dark)

**Dark palette (frozen):**

| Token | Value |
|-------|-------|
| `--midnight` (background) | `#111318` |
| `--electric` | `#5ba4cf` |
| `--cyan` | `#7ec8e3` |
| `--amber` | `#d4a853` |
| `--white` (text) | `#edf1f5` |

**Light palette (landed):**

| Token | Value | Notes |
|-------|-------|-------|
| `--midnight` (background) | `#e8edf2` | Frost paper |
| `--electric` | `#3d8bb5` | Deepened for contrast on light |
| `--cyan` | `#2d7fa3` | Deepened for contrast on light |
| `--amber` | `#b8872e` | Deepened for contrast on light |
| `--white` (text) | `#111318` | Inverted semantic role |
| `--glass` | `rgba(255,255,255,0.78)` | Daylight frosted panels |

Light-mode hero background opacity drops to `0.26` with softer gradient washes so the dark OG art does not overpower frost paper.

`web/logo-mark.svg`: letterform `I` fill changed to `currentColor` so the mark inherits theme text color.

### Mosvera light-mode registration

Light palette and effects were added to the local `imprint` aesthetic (not committed to imprint repo):

**`~/.config/mosvera/registry/template.imprint-base.json`** — added `palette_light`, `effects_light`, `voice_light`

**`~/.config/mosvera/registry/palette.imprint-light.json`** — standalone palette id `imprint-light` for `get_palette`

**`~/.config/mosvera/registry/composition.imprint.json`** — `overrides` block with matching `palette_light`, `effects_light`, `voice_light`

Voice string for light mode: *"Frosted daylight glass carrying evidence-backed expression profiles."*

Dark and light are now a **dual-theme aesthetic** under one composition id `imprint`, not two separate aesthetics.

## Deploy cadence

Each substantive web change was deployed manually from `web/`:

```bash
cd web
npx vercel@latest --prod --yes
```

Observed production aliases: `https://imprint.niclydon.dev`

Final deploy after mobile/theme commit `b60506b`: upload ~39 KB (HTML/CSS/JS delta), build region `iad1`, ready in ~5–7s.

Live verification:

- `curl -sI https://imprint.niclydon.dev/og.png` → `200`, `content-length: 970028`
- Hero WebP served from `/hero.webp` at 58 KB

## Privacy and non-goals upheld

Per `web/DEPLOYMENT.md` and sprint boundaries:

- No analytics scripts
- Google Fonts from `fonts.googleapis.com` (documented; self-hosting noted as optional hardening)
- No credentials, corpus paths, or private infrastructure in HTML
- No application UI — static explanation only

## Commit map

| SHA | Summary |
|-----|---------|
| `32f4faf` | Initial static landing site + README link |
| `e56d1b1` | Vercel monorepo `outputDirectory: web` |
| `b082536` | ai-glass-futuristic overlay |
| `c083c41` | Forge img2img OG (superseded) |
| `97d3ee6` | Pure gpt-image-2 txt2img OG |
| `667d7e9` | Hero background ← OG WebP derivative |
| `b60506b` | Mobile nav drawer + light/dark theme |

## What was rejected and why

| Option | Why it lost |
|--------|-------------|
| Branded hero with baked-in "IMPRINT" as page background | Centered glass card obscured the word; poster-vs-card collision |
| img2img OG only | Same text-in-image problem when reused as hero; pure txt2img fixed it |
| `object-position` nudge on old hero | Band-aid; busy document stream still fought the card |
| Serving `og.png` directly as hero (970 KB) | Performance; WebP at 58 KB won |
| Separate Mosvera aesthetic id for light mode | Operator asked for light mode **on** `imprint`; dual-theme overrides are cleaner |
| Mobile nav that only hides links | Insufficient; drawer required for About/Pipeline/Boundaries/Privacy reachability |

## What's unblocked

- README and docs can cite a stable public URL with credible previews
- Social sharing has a dedicated OG asset with generation provenance (`og-gen.json`)
- Mosvera `imprint` aesthetic documents dark + light palettes for downstream Forge/Loom branded generation
- Sprint 11+ work on export formats and first-run experience can link to a polished public front door

## What's still pending

- Social cache refresh (LinkedIn Post Inspector, X Card Validator) after OG swap — platforms cache aggressively
- Optional: self-host fonts to remove Google Fonts network dependency
- Optional: export `imprint` Mosvera pack into repo or enable `mosvera-mcp` in agent sessions
- Optional: dedicated 16:9 hero generation tuned for centered card (if OG crop proves insufficient at extreme aspect ratios)
- `web/.gitignore` for raw generation artifacts (`og-*-raw.png`) — present locally, not yet committed

## Exit criteria re-check (`SPRINT_10.md`)

| Criterion | Status |
|-----------|--------|
| `imprint.niclydon.dev` renders publicly | ✅ |
| GitHub README links to site | ✅ |
| Social cards render correctly | ✅ (OG at `/og.png`; re-scrape recommended) |
| Favicon and OG assets work | ✅ |
| Pre-release / open-source / local-first posture | ✅ |
| No private data exposed | ✅ |
| Mobile-friendly | ✅ (added post-initial ship) |
| Dual theme | ✅ (stretch beyond original sprint doc) |

Sprint 10 web presence is **delivered**. The page is the explanation layer; the compiler remains in Python under `src/imprint/`.

See `CHANGES.md` Sprint 10 entry for the chronological diff summary.