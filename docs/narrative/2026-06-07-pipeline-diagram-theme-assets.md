# Pipeline Diagram Replaces the Text Box on imprint.niclydon.dev

The Sprint 10 landing page shipped with a monospace placeholder under “Evidence in, portable profiles out” — a glass panel containing seven lines of CLI-shaped text: `configured sources -> harvest -> classify -> extract signals -> compile profile -> export contracts`. It was accurate and cheap to implement, but it read as documentation pasted into a marketing surface. The section deserved a visual that matched the glass aesthetic, the dual light/dark theme, and the evidence-flow story Imprint tells in prose elsewhere on the page. Two custom illustrations — one for dark mode, one for light — arrived through a local design handoff the same afternoon; this session replaced the text box with those assets and wired them to the existing theme toggle.

## The problem with the text pipeline

After `b60506b` landed mobile navigation and the sun/moon theme toggle, the about-section pipeline was the weakest visual on the page. Every other major block had either glass structure, illustrative hero art, or card grids. The pipeline block was the exception: JetBrains Mono cyan text on frosted glass, arrows in amber, no diagram.

The placeholder matched README copy and the architecture pipeline string:

```text
configured sources
  -> harvest
  -> classify
  -> extract signals
  -> compile profile
  -> export contracts
```

That string describes the **compiler's internal stages**. The replacement illustrations describe the **public story** at a slightly higher level: **Sources → Signals → Profile → Exports**, with iconography for chat, audio, documents, code, and folders on the left; signal-processing stages in the center; a profile dashboard and export targets on the right. The labels differ, but the slot on the page is the same — “how artifacts become portable profiles.” The operator's intent was explicit: these images were designed to replace the box, not supplement it.

Keeping both text and image would have been redundant. Keeping text alone left the site's best explanatory section looking unfinished next to the Forge-generated hero and OG art.

### Text stages vs diagram labels

The replacement is not a pixel-perfect rename of the monospace chain. The diagram compresses the public story into four labeled bands:

| Monospace placeholder (removed) | Diagram label (visual) | Visual content |
|-------------------------------|------------------------|----------------|
| configured sources | **SOURCES** | Chat, audio waveform, document, code hash, folder icons feeding a glowing data block |
| harvest + classify + extract signals | **SIGNALS** | Stacked processing frames: categorized shapes, waveform, data cubes, concentric rings |
| compile profile | **PROFILE** | Dashboard card with hex mark, metric lines, grid heatmap |
| export contracts | **EXPORTS** | Globe, document, code brackets, lock icons on dotted export paths |

The README and hero copy still use the seven-step compiler string elsewhere. The landing page diagram is allowed to be higher-level — it answers “what happens to my artifacts?” not “what are the CLI stage names?” That distinction matters for future doc work: do not “fix” the diagram labels to say `harvest` unless the art is regenerated.

## Asset retrieval from local DropBox

The operator pointed at a local file-share drop folder:

```
[local file-share drop folder]/ingestion_imports
```

From the Linux build host, direct file-share mounting failed. The path name was also slightly
misleading: **`ingestion_imports` did not contain the images**. That subdirectory held an
unrelated private export bundle, while the two PNGs were dropped in the parent local drop
folder.

**Working path:** copy from the local drop folder to `web/` using an operator-controlled
private machine path. Do not record hostnames, IPs, usernames, local source filenames, or absolute
local paths in public docs.

The original operator-only copy command was intentionally removed from this public narrative.

| Source asset | Role | Dimensions | PNG size |
|--------------|------|------------|----------|
| local dark-mode design drop | Dark-mode diagram | 1717×916 | 1,450,465 bytes |
| local light-mode design drop | Light-mode diagram | 1717×916 | 1,389,110 bytes |

**Dark illustration:** black field, electric blue glows, orange accent on “PROFILE”, horizontal flow with labeled stages SOURCES / SIGNALS / PROFILE / EXPORTS.

**Light illustration:** frost-paper gradient background (`#e8edf2` family), same layout and labels, softer shadows — aligned with the landed light-mode palette from `b60506b`.

No credentials involved. No ingestion pipeline run — these were design drops for the web repo, not Nexus bronze imports.

## Web delivery: WebP, theme swap, gitignore

Committing 2.8 MB of PNG to a static site would have been wasteful when the page already optimizes hero art as WebP. ImageMagick conversion:

```bash
convert local-dark-source.png -define webp:method=6 -quality 84 pipeline-dark.webp
convert local-light-source.png -define webp:method=6 -quality 84 pipeline-light.webp
```

| Deployed asset | Size | Source asset |
|----------------|------|--------------|
| `web/pipeline-dark.webp` | 50,352 bytes | local dark-mode design drop |
| `web/pipeline-light.webp` | 39,358 bytes | local light-mode design drop |

Compression ratio: roughly **29×** for dark, **35×** for light, with no visible quality loss at landing-page display width.

### HTML replacement

The `#pipeline` anchor (navbar “Pipeline” link) moved from a `<div role="img">` with `<pre>` to a `<figure class="pipeline pipeline-visual glass">` with two `<img>` elements:

- `pipeline-img--dark` → `/pipeline-dark.webp`
- `pipeline-img--light` → `/pipeline-light.webp`

Shared alt text: *“Imprint pipeline: sources flow through signal extraction and profile compilation to portable exports”*

Attributes: `width="1717" height="916"`, `loading="lazy"`, `decoding="async"` — responsive scaling via CSS `width: 100%`, intrinsic aspect ratio preserved for CLS.

### CSS theme binding

The site does not use `prefers-color-scheme` alone; it uses `data-theme` on `<html>` with manual override in `localStorage`. Pipeline images follow the same contract:

```css
.pipeline-img--light { display: none; }
[data-theme="light"] .pipeline-img--dark { display: none; }
[data-theme="light"] .pipeline-img--light { display: block; }
```

Default dark theme shows the dark diagram without a flash — the inline head script in `index.html` sets `data-theme` before paint, same as the rest of the page.

Removed styles: `.pipeline pre`, `.pipeline .arrow`, mobile `font-size` override for pre text.

New styles: `.pipeline-visual` with reduced padding (`0.65rem`), `overflow: hidden`, inner `border-radius` on images.

### Source artifact hygiene

`web/.gitignore` (new in this commit) excludes:

- `.vercel`
- Raw OG generation PNGs (`og-*-raw.png`, etc.)
- Source pipeline PNGs from local design handoff

Only WebP derivatives ship in git and on Vercel. Source PNGs remain on the workstation worktree for re-export if quality settings change.

## Deploy

Commit `4aa5d41` — *Replace text pipeline box with theme-aware diagram images*.

Push required rebase onto remote `be5e06b` (interleaved `chore: restore vercel deploy config` and sprint 07 docs from another session). Final push: `4aa5d41` on `main`.

Vercel production deploy from `web/`:

- Upload ~2.8 MB (includes full site asset tree)
- Alias: **https://imprint.niclydon.dev**
- Pipeline section: `https://imprint.niclydon.dev/#pipeline`

Verification: toggle sun/moon in navbar — diagram swaps between dark and light illustrations inside the glass frame.

### Session sequence (operator ↔ agent)

The work landed in three operator turns after the Sprint 10 narrative closeout (`103b471`):

1. **“Get the two image files”** from the local design handoff — agent copied the paired PNGs to `web/`.
2. **Transport clarification** — operator confirmed the right local transfer route when direct file-share mounting failed from the Linux host.
3. **“Those images are designed to replace the box…”** — operator named the target section (“Evidence in, portable profiles out”) and the monospace pipeline block as the element to remove.

No Forge regeneration. No img2img. These are finished design assets dropped from the operator's design workflow, not model output from the Sprint 10 OG pass.

## What was rejected

| Option | Why it lost |
|--------|-------------|
| Keep monospace text alongside images | Redundant; operator wanted replacement not augmentation |
| Single image for both themes | Light and dark illustrations exist as paired assets; forcing one would break contrast in one mode |
| Serve PNG directly (1.4 MB each) | Page weight; WebP at ~45 KB average won |
| `prefers-color-scheme` only via `<picture>` | Ignores manual theme toggle and `localStorage` persistence |
| Direct file-share mount | Tools/path failed; local copy route was reliable |
| Look inside `ingestion_imports/` only | Images were in the parent local drop folder |

## Relationship to Mosvera `imprint` aesthetic

The pipeline illustrations use the same electric blue / amber accent language as the landed light and dark palettes in the local Mosvera registry. They were not yet registered as separate Mosvera imagery primitives in this session — the registry still references the hero image for spotlit hero treatment. A follow-up could add `imagery.pipeline_dark` and `imagery.pipeline_light` to `template.imprint-base.json` if Forge or Loom needs to regenerate matching diagrams.

## What's unblocked

- The “Evidence in, portable profiles out” section now communicates visually at the same fidelity as the hero and OG art
- Theme toggle demonstrates paired asset design — useful reference for future section illustrations
- Local design handoff → WebP → Vercel is a proven flow for design drops without private ingestion

## What's still pending

- Register pipeline diagram paths in Mosvera `imprint` template if downstream generation should cite them
- Confirm mobile legibility at ≤520px — wide 1717×916 art scales down; labels may need a future cropped mobile variant
- Operator may want source PNGs archived under `docs/assets/` with semantic names (optional; currently gitignored in `web/`)
- Update primary Sprint 10 narrative (`2026-06-07-sprint-10-public-web-presence.md`) with a one-paragraph forward pointer to this doc — deferred to avoid rewriting a closed arc in place

## Files touched

| Path | Change |
|------|--------|
| `web/index.html` | `<figure id="pipeline">` with dual `<img>` |
| `web/styles.css` | `.pipeline-visual`, theme-aware display rules |
| `web/pipeline-dark.webp` | New deploy asset |
| `web/pipeline-light.webp` | New deploy asset |
| `web/.gitignore` | Source PNG + raw OG exclusions |
| `docs/narrative/2026-06-07-pipeline-diagram-theme-assets.md` | This document |
| `CHANGES.md` | Pipeline visual entry |
| `docs/sprints/SPRINT_10.md` | Beyond-exit-criteria note |

## Commit

```
4aa5d41 Replace text pipeline box with theme-aware diagram images
```

Parent narrative for full Sprint 10 site delivery: `docs/narrative/2026-06-07-sprint-10-public-web-presence.md`

See `CHANGES.md` Sprint 10 pipeline visual entry for the chronological diff summary.
