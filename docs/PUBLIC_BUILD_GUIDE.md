# Public Build Guide

Status: planning

## Goal

Build Imprint in public from the beginning without leaking private data, private infrastructure details, personal corpus content, or credentials.

## Public development posture

The public repo should be generic. The private deployment should be configured.

That means:

- generic code
- generic schemas
- generic docs
- synthetic examples
- ignored private config
- ignored local exports
- no private fixtures

## Repository hygiene

### Required before first public push

- [ ] Rename product-facing docs to Imprint.
- [ ] Add/verify `.gitignore` for private config, data, exports, DBs, caches.
- [ ] Add `.env.example` only.
- [ ] Add `imprint.config.example.yaml` only.
- [ ] Add synthetic example corpus.
- [ ] Remove or quarantine real eval data if present.
- [ ] Run secret scan.
- [ ] Run private string scan.
- [ ] Run tests without private services.

### Existing repo caution

The current internal repository may already contain local files such as `.env`, evaluation samples, caches, or private service definitions. Before making it public, audit the full git history, not just the working tree.

Recommended command set:

```bash
git status --short
git ls-files
find . -maxdepth 3 -type f | sort
```

Then run a secret scanner across both working tree and history.

## Config pattern

Commit:

```text
.env.example
imprint.config.example.yaml
examples/synthetic_corpus/*
examples/profiles/synthetic_profile.json
```

Do not commit:

```text
.env
imprint.config.yaml
data/*
exports/*
private/*
corpus/*
*.sqlite
*.db
```

## Build-in-public content rules

Safe to share publicly:

- architecture decisions
- schema design
- synthetic examples
- lessons about privacy boundaries
- implementation progress
- generic connector patterns
- evaluation method
- screenshots using synthetic data

Do not share publicly:

- real samples from private messages or emails
- real profile exports
- private source names or hostnames
- real database schemas if they reveal private systems
- screenshots with real data
- logs containing prompts, message bodies, or tokens

## Issue hygiene

Public issues should avoid private references.

Good issue:

> Add source policy weights for chat artifacts so chat can influence lexical and tone signals without shaping long-form structure.

Bad issue:

> Make my messages from a specific person influence drafting less.

## Commit hygiene

Use generic commit messages:

Good:

```text
Add source weighting schema
Add synthetic transcript connector fixture
Implement public-safe export defaults
```

Bad:

```text
Add personal Gmail extractor
Fix private query for my messages
Export my publishing profile
```

## Public launch checklist

- [ ] Product name settled.
- [ ] README has public quickstart.
- [ ] No internal-only service names required to understand the project.
- [ ] Private deployment docs are either absent or clearly marked local-only.
- [ ] All examples are synthetic.
- [ ] Security policy exists.
- [ ] License chosen.
- [ ] First GitHub issues are generic.
- [ ] Build-in-public post has no screenshots of private data.
