# Imprint Web — Deployment

## Topology

- **Repo:** `github.com/niclydon/imprint`
- **Site root:** `web/` (Vercel Root Directory setting)
- **Hosting:** Vercel (team `niclydon`)
- **Domain:** `imprint.niclydon.dev`
- **DNS:** Cloudflare (zone `niclydon.dev`)

## Vercel project setup

1. Create project `imprint` (or `imprint-web`) linked to `niclydon/imprint`.
2. Set **Root Directory** to `web`.
3. Framework preset: **Other** (static HTML, no build command).
4. Output directory: `.` (default — serves `index.html` and assets from `web/`).
5. Add domain `imprint.niclydon.dev` in Vercel project settings.

## Cloudflare DNS

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `imprint` | `cname.vercel-dns.com` | DNS only (grey cloud) |

Keep the record **DNS only**. Proxying Vercel through Cloudflare can cause TLS/redirect loops.

Vercel issues TLS for `imprint.niclydon.dev` after DNS propagates.

## Deploy trigger

Push to `main` → Vercel rebuilds automatically (when Git integration is configured).

Manual deploy from `web/`:

```bash
cd web
npx vercel --prod
```

## Local preview

```bash
cd web
python3 -m http.server 8080
# open http://localhost:8080
```

## Social preview verification

After deploy, verify link previews:

- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- Paste URL in Discord or iMessage for embed check

OG image: `https://imprint.niclydon.dev/og.png` (1200×630)

## Privacy

No analytics scripts. Google Fonts loaded from `fonts.googleapis.com` (documented; optional hardening: self-host fonts).