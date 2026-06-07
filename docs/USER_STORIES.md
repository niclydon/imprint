# User Stories

Status: Sprint 01 output

## Writers

1. As a writer, I want Imprint to analyze my essays and notes so I can preserve my style while
   using AI-assisted drafting.
2. As a writer, I want AI-assisted drafts to be marked separately so my profile does not become a
   copy of the model's style.
3. As a writer, I want a first-run report that explains what Imprint learned before showing JSON.
4. As a writer, I want raw examples excluded from exports by default so I can safely use the
   profile in tools without leaking private drafts.

## Personal AI Builders

5. As a personal AI builder, I want a portable profile contract so my agent can use expression
   guidance without reading my raw messages.
6. As a personal AI builder, I want profile versions and drift notes so I can decide when an agent
   needs updated guidance.
7. As a personal AI builder, I want separate casual, technical, and long-form profiles so my agent
   can adapt to context.
8. As a personal AI builder, I want confidence and evidence metadata so I can suppress weak claims
   in downstream prompts.

## Researchers

9. As a researcher, I want synthetic corpora and public-safe fixtures so I can study expression
   profiling without private data.
10. As a researcher, I want signal taxonomies with non-examples so I can evaluate whether the
    system measures what it claims.
11. As a researcher, I want authorship-origin metadata so I can study AI-assisted writing drift.
12. As a researcher, I want reproducible profile outputs for the same corpus and settings so
    comparisons are meaningful.

## Executives

13. As an executive, I want a profile compiled from approved public and internal artifacts so my
    team can draft in my communication style without accessing all my private messages.
14. As an executive, I want source policy controls so casual messages do not shape formal public
    communication too strongly.
15. As an executive, I want profile outputs to avoid personality claims so the tool does not
    misrepresent me.

## Content Creators

16. As a creator, I want Imprint to identify differences between podcast transcripts, posts, and
    essays so each downstream format can stay authentic.
17. As a creator, I want quoted guest content excluded from my profile so collaborator speech does
    not become my voice.
18. As a creator, I want a human-readable profile report so I can edit or challenge what the system
    thinks it learned.

## Brand Teams

19. As a brand team, I want expression profiles for spokespeople or brand voices so content systems
    can apply consistent guidance.
20. As a brand team, I want approved-language enforcement to remain outside Imprint so the compiler
    stays focused on expression evidence.
21. As a brand team, I want public-safe examples so contributors can improve the project without
    seeing customer or executive data.

## Product Teams

22. As a product team, I want canonical JSON/YAML exports so multiple applications can consume the
    same profile.
23. As a product team, I want clear owner boundaries so my publishing app does not become a voice
    compiler by accident.
24. As a product team, I want privacy validation in CI so unsafe export behavior fails before
    release.
25. As a product team, I want a local-first default so the MVP can be evaluated without vendor
    credentials.

## Maintainers

26. As a maintainer, I want schema versioning and migration policy before implementation so early
    users are not trapped by unstable profile shapes.
27. As a maintainer, I want connector review checklists so private integration requests do not
    erode public-first safety.
28. As a maintainer, I want a docs index that distinguishes planning, normative architecture, and
    sprint outputs so contributors know what to follow.

## Acceptance Principles

Every user story should preserve these acceptance principles:

- The user owns the profile.
- The profile is evidence-backed.
- Public-safe mode does not leak raw private artifacts.
- AI assistance and speaker attribution are explicit.
- Imprint compiles expression; downstream tools apply it.
