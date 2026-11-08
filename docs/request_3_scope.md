# Request 3 scope — design and discovery

Approved by Po on 08 November 2026 ("Yes to all three"), with two items added from the Geospatial_Dev integration plan of the same day (seams 2 and 3). This file is the detailed target; the paste text in `docs/dual_dev_requests.md` points here. Codex order this week per that plan: request 3 runs after Street vs Sky step 0, GeoHUB B3 fixes and the equity island.

## In short
- The site becomes a poster-style gallery (cream, condensed black headline with one orange word, monospace captions, thin frame lines, a grid of visual cards from each repo's GitHub social-preview image).
- Discovery widens: all 17 queries, a new skills-and-config-packs family, a new geospatial family, a lower star floor for repos under 90 days old, and a "Rising this week" strip from our own six-hourly star snapshots, every card still carrying trust score and level.
- The generator becomes reusable: it takes any listings file plus a theme, and exports one dated JSON per topic family that another site can consume.
- A weekly digest image for sharing. Ranking stays trust-first; stars never order a list except the clearly labelled Rising strip.

## A. Design (generator and templates)
- Visual language from the reference poster: background `#F4F1EA`, ink `#121212`, accent `#FF511D`, display face a free condensed sans (Google Fonts, for example Anton or Archivo Black), captions in a monospace (IBM Plex Mono or JetBrains Mono), thin 1 px frame lines and small corner marks, generous white space. Light theme by default; dark theme kept via `prefers-color-scheme`.
- Cards: `openGraphImageUrl` from the GitHub GraphQL repo node (add the field to `SEARCH_QUERY` and `RepoRecord`); fallback card with the repo name set large when the image is missing. Card shows name, one-line description, trust score, coverage, level (or "not yet labelled"), tested status, GitHub link. Images are hot-linked from GitHub, never downloaded into the repo.
- Pages: index (hero headline, Rising strip, then topics as card grids of ten with "see all"), topic pages (paginated grid), repo page (card hero, evaluated components table, dates), how we grade, status footer. All text escaped; outbound links unchanged policy.
- Accessibility: contrast at least 4.5:1 for body text, focus styles, the level filter usable by keyboard, images with alt text from the repo name.

## B. Discovery (config, sources, scoring inputs)
- Queries: default scope becomes all 17 existing queries plus two new families: `skills_packs` (GitHub topics `claude-skills`, `agent-skills`, `claude-code-skills`, `cursor-rules`, and repos whose root tree holds `SKILL.md` or `skills/`; star floor 300) and `geospatial` (topics `osmnx`, `geospatial`, `gis`, `urban-analytics`, `remote-sensing`, `space-syntax`, plus named repos: gboeing/osmnx, pysal/momepy, benchmark-urbanism/cityseer-api, microsoft/torchgeo, developmentseed/titiler, geopython/pygeoapi, opengeos/segment-geospatial, geopandas/geopandas, uscuni/neatnet, SMoG-KTH/PST; star floor 200).
- Star floor by age: repos created under 90 days ago qualify at one quarter of the family floor.
- Budget: the GraphQL budget stays 2,500 points a run; add a per-family cap so the widened scope cannot exceed it (estimate before building; the live run used 12 points for 6 queries).
- Rising: `velocity_7d` and `velocity_28d` from the snapshots table (null until two snapshots exist); the Rising strip shows the top twelve by 7-day gain among repos with trust score at least 50 and coverage at least 0.4, labelled "stars gained in 7 days, not a quality rank". No change to the trust score weights.
- Per-family export: `site/src/data/families/<family>.json`, dated, same row schema as listings plus `family`; `pipeline export families` command; gate 2 validates each file.

## C. Themed generator (seam 3)
- `pipeline site build --input <listings.json> --output <dir> --theme <theme.json>`; the theme file holds colours, font stacks, site name, tagline, footer line and optional about text; defaults in `pipeline/site/themes/ai_hub.json`. No logo handling. The generator must not read anything AI_Hub-specific outside the theme and the listings file, so a second repository can vendor or install it and build its own site with the same Actions-to-Pages pattern.
- A test builds the sample fixture with a second theme file and asserts the colours and names appear and no AI_Hub strings leak.

## D. Weekly digest image
- `pipeline digest image` renders a 1080 by 1350 PNG (LinkedIn and X friendly) of the Rising strip and three editor's picks in the poster style, using Pillow with the same fonts, saved to `site/dist/digest/<date>.png` and linked from the index. Mondays 07:00 UK in the workflow. No posting automation; Po posts it.

## Acceptance for the request
- Suite green at 80 per cent coverage or better; ruff clean; gate 5 passes on a 500-row build; every card has alt text; Lighthouse accessibility 90 or better on the index (run once by Claude in the acceptance task).
- A live dry run with the widened scope stays under 1,000 GraphQL points and under 10 minutes.
- Second-theme build test passes; a `families/geospatial.json` export validates and is non-empty on the dry run.
- Digest image renders offline from the fixture.

## Out of scope
- Labeller (request 4), sandbox tests and starter kits (request 5), weights v1 and fraud checks (request 6), domain and Cloudflare (request 7). GeoHUB content of any kind.
