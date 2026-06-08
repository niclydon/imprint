# Imprint Changes Log

Chronological per-phase record of significant work. See `docs/narrative/` for detailed documentary accounts.

---

## 2026-06-07

### Sprint 11: Adversarial Review — Packaging and Install Experience

**Decision:** Conduct comprehensive hostile architect review of Sprint 11 (packaging, install, onboarding, release readiness) to verify stranger installability, synthetic demo integrity, CLI usability, packaging quality, public safety, and release-readiness.

**What changed:**

**Sprint 11 packaging review:**
- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md` (164 lines) — Verified 6 focus areas: stranger installability (clean venv install works), synthetic demo integrity (generated outputs exclude private text/paths/creds), CLI usability (onboarding discoverable), packaging quality (credible metadata, reasonable deps), public safety (no tracked `.env`, local config, or private data), release readiness (CI and checklist adequate for v0.1.0 developer preview)
- `docs/narrative/2026-06-07-sprint-11-adversarial-review-packaging-ready.md` (450 lines, new) — Detailed narrative of review process, what was checked, what passed, numerical evidence, and what's unblocked
- 5 new onboarding tests added in Sprint 11; 100/100 total tests passing
- All exit criteria met; GO verdict

**Verification evidence:**
- Clean temp-venv install with `pip install -e ".[test]"` passed
- `python -c "import imprint; print(imprint.__version__)"` → `0.1.0`
- `imprint --help`, `imprint connectors-dry-run`, `imprint example` all passed
- Generated example exports contain zero raw artifact text, source paths, or credential patterns
- Static code analysis: zero private data in tracked files (only CSS `mask-*` property hits)
- GitHub Actions CI: Python 3.12 install, compile, and test checks green

**What's unblocked:**
- Package is production-ready for `v0.1.0` developer preview
- New users can install, run synthetic demo, and understand next steps without private infrastructure
- Release checklist provides concrete gate criteria before public tagging

**Still pending:** Run release checklist from fresh clone before tagging; confirm CI is green on pushed commit.

**Full story:** `docs/narrative/2026-06-07-sprint-11-adversarial-review-packaging-ready.md`

### Sprint 10: Pipeline diagram assets

**Decision:** Replace the monospace `configured sources -> harvest -> …` text box in “Evidence in, portable profiles out” with paired dark/light pipeline illustrations that follow the navbar theme toggle.

**What changed:**

- **Asset source:** Anvil `Public/DropBox/` via SSH/SCP — `3DD46FBC-9A8A-4D95-86D4-C68D67FA8237.png` (dark), `D753F74F-26A0-4656-B4E0-C241BC1EE336.png` (light); 1717×916 each
- **Web delivery** (`4aa5d41`): `pipeline-dark.webp` (50 KB), `pipeline-light.webp` (39 KB); theme swap via `data-theme` CSS in `web/index.html` + `web/styles.css`
- **`web/.gitignore`:** exclude source UUID PNGs and raw OG artifacts; commit WebP only

**Commits:** `4aa5d41`

**What's unblocked:** About-section pipeline matches hero/OG visual fidelity; paired light/dark asset pattern documented for future illustrations.

**Still pending:** Optional Mosvera `imagery.pipeline_*` registry entries; optional mobile-specific crop if label legibility needs it at narrow widths.

**Full story:** `docs/narrative/2026-06-07-pipeline-diagram-theme-assets.md`

### Sprint 10: Public Web Presence — delivered

**Decision:** Ship `imprint.niclydon.dev` as a static, glass-styled public front door — not an application UI — with credible social previews, mobile navigation, and a dual light/dark theme registered in Mosvera aesthetic `imprint`.

**What changed:**

- **`web/` landing site** (`32f4faf`): `index.html`, `styles.css`, favicon, touch icon, logo mark, social metadata, `DEPLOYMENT.md`; README links to https://imprint.niclydon.dev
- **Deploy path** (`e56d1b1`): repo-root `vercel.json` `outputDirectory: "web"`; Vercel project `imprint`, Cloudflare CNAME `imprint` → `cname.vercel-dns.com` (DNS only)
- **Glass overlay** (`b082536`): `ai-glass-futuristic` structure on frozen Imprint palette; Mosvera `template.imprint-base.json` + `composition.imprint.json` (local registry)
- **OG image** (`97d3ee6`): pure Forge `openai:gpt-image-2-q8` txt2img at 1536×832, cropped to 1200×630 (`web/og.png`, 970 KB); metadata in `web/og-gen.json` — no in-image text
- **Hero background** (`667d7e9`): `hero.webp` WebP derivative of OG (58 KB); `object-position: 58% 42%` — fixes baked-in "IMPRINT" text collision with centered glass card
- **Mobile + dual theme** (`b60506b`): slide-out nav drawer (≤900px), sun/moon toggle, `localStorage` + system preference, light palette on frost paper (`#e8edf2`); `web/theme.js`; Mosvera `palette_light` / `effects_light` on aesthetic `imprint`

**Commits:** `32f4faf`, `e56d1b1`, `b082536`, `c083c41` (superseded OG), `97d3ee6`, `667d7e9`, `b60506b`

**What's unblocked:** Stable public URL and social preview chain for README/docs; Mosvera `imprint` documents dark + light palettes for downstream branded generation.

**Still pending:** Social cache re-scrape (LinkedIn/X); optional font self-hosting; optional Mosvera pack export to repo.

**Full story:** `docs/narrative/2026-06-07-sprint-10-public-web-presence.md`

### Sprints 08–10: Adversarial Architecture Reviews — Boundary Verification

**Decision:** Conduct comprehensive hostile architect reviews of Sprints 08 (consumer contracts), 09 (connector framework), and 10 (web presence) to verify boundaries are preserved, non-goals remain deferred, and test coverage is comprehensive.

**What changed:**

**Sprint 08 consumer contracts review:**
- `docs/SPRINT_08_ARCHITECTURE_REVIEW.md` (155 lines) — Verified 6 focus areas: boundary preservation (no prompt assembly, publishing, runtime adapters), Mosvera boundary (expression overlay only), Broadside boundary (constraints only), agent safety (warnings mandatory), version compatibility (mixed versions warn), privacy (no raw text, opaque IDs)
- 11 new tests added; 82/82 total tests passing
- All exit criteria met; GO verdict

**Sprint 09 connector framework review:**
- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md` (143 lines) — Verified 6 focus areas: public/private boundary (synthetic examples only, no real credentials), connector authority (discovery/ingest only, no classification bypass), secret handling (env var refs, fail-closed validation, redaction in errors), source privacy (opaque IDs, no path leaks), scope control (no live APIs, OAuth, LLMs), operational safety (dry-run safe, disabled connectors inert)
- 14 new tests added; 96/96 total tests passing
- All exit criteria met; GO verdict

**Sprint 10 web presence review:**
- `docs/SPRINT_10_ARCHITECTURE_REVIEW.md` (570 lines, new) — Verified 10 focus areas: public/private boundary (no creds, no private data), content accuracy (claims verified, no overstatement), visual alignment (brand language, no dashboard mockups), social metadata (OG cards correct, provenance tracked), accessibility (mobile nav, dual theme), performance (1.5 KB code, optimized assets), security (no XSS, injection, leaks), deployment integrity (Vercel + Cloudflare verified), non-goals (no corpus upload, app UI), documentation (comprehensive, traceable)
- Pre-existing site verified against 10 gates; all passed
- All exit criteria met + 2 stretch goals delivered; GO verdict

**Verification evidence:**
- `docs/narrative/2026-06-07-sprints-08-10-adversarial-reviews.md` (570 lines) — Detailed narrative of the review process, what was checked, what was rejected, numerical observations, and what's unblocked
- Static code analysis: zero remote/provider/LLM calls, zero credential leaks across all three sprints
- Test suite: 82 → 96 → verified; all hostile vectors tested
- Boundary integrity: public/private separation holds; no scope creep

**What's unblocked:**
- Downstream systems can safely consume Sprint 08 consumer contracts
- Private deployments can add real connectors via ignored local config (Sprint 09)
- Imprint has a credible public front door with working social metadata (Sprint 10)

**Commits:** `6a33538` (Sprint 10 review document)

**Full story:** `docs/narrative/2026-06-07-sprints-08-10-adversarial-reviews.md`

### Phase: Sprint 07 Adversarial Review — Export Layer and First-Run Experience Readiness

**Verdict:** GO for Sprint 08

Conducted comprehensive adversarial review of Sprint 07 exports and first-run experience against 6 architectural focus areas:

1. **Export safety** — All formats validated; no raw text, paths, or private metadata leak. Shared safety layer rejects prohibited claims, quarantined support, non-durable evidence, mixed signal model versions, path-like source IDs, and generation-control fields.
2. **Claim boundaries** — Expression-pattern-only scope preserved. All exports use "observed pattern" language; first-run explicitly states what Imprint cannot say.
3. **Version compatibility** — Compiler, classifier, and signal model versions preserved in all machine-readable exports. Mixed classifier versions warn; mixed signal model versions reject.
4. **First-run experience** — Useful, clear, non-overstated. Sorted by confidence, warns about low-confidence patterns and metadata-only storage limits.
5. **Mosvera boundary** — Contract/fragment only. Expression summaries and anti-patterns; no provider prompts, aesthetic-intent compilation, or runtime behavior.
6. **Determinism and provider neutrality** — All exports deterministic (byte-for-byte reproducible). No LLMs, embeddings, remote calls, or provider assumptions.

**Evidence:**
- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md` — Detailed findings (147 lines)
- `tests/test_exports.py` — 10 comprehensive tests, all passing
- Full test suite: 71/71 passing
- All 10 Sprint 06 carry-forward constraints remain enforced

**Handoff to Sprint 08:**
- Canonical JSON is the source of truth for downstream projections.
- Downstream prompt assembly and publishing workflow are Sprint 08 scope, not Imprint.
- No architectural blockers remain.

Full story: `docs/narrative/2026-06-07-sprint-07-adversarial-review-exports-ready.md`

---

## Earlier Phases

See `docs/narrative/2026-06-07-sprint-06-compiler-verification-and-gates.md` for Sprint 06 adversarial review and earlier narrative docs in `docs/narrative/` by date.