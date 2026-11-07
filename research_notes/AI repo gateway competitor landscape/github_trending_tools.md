# GitHub-native and generic repository discovery tools (state as of 7 November 2026)

Method note: all pages were read on or around 7 November 2026 through a fetch tool that summarises pages with a small model. Summaries can miss page sections, so "not shown" means "not visible in the fetched text", not "proven absent". No tool was installed or run. The five dimensions are: (1) skill-level grouping, (2) AI-topic grouping, (3) human/editorial curation versus pure metrics, (4) evidence the repo was run or tested, (5) security or licence screening.

## 1. What do GitHub Trending, Explore, Topics and Collections offer, and is there any skill-level grouping?

### Takeaway
GitHub's native tools rank by popularity or momentum (stars, recent star gain) and group by language or topic tag. None of them offers skill-level grouping, an AI filter on Trending, testing evidence or security/licence screening. The only beginner signal is the "good first issue" label (for contributors, not for repo users) and one hand-written beginner Collection about machine learning.

### Cited Findings
- github.com/trending has two tabs (Repositories, Developers), a spoken-language dropdown, a programming-language dropdown, and a date range of Today / This week / This month. There is no AI filter on the page — [GitHub Trending](https://github.com/trending)
- The Trending page does not explain how "trending" is computed and shows no earlier-date history; only the current window is displayed — [GitHub Trending (with spoken-language parameter)](https://github.com/trending?since=daily&spoken_language_code=en). Caveat: in this fetch the first five repos were nushell, ruff, Homebrew, tokio and svelte (none AI), which may be a cached or partial render, so do not infer that AI repos are absent from Trending generally.
- No official Trending API exists; third-party scrapers (Apify actors, npm and GitHub projects) scrape the HTML page, and they warn that page changes can break them. This is a vendor claim, not confirmed by GitHub docs; sources disagree on refresh timing ("roughly every 6 hours" versus "throughout the day"); about 25 repos are shown per language/window — [Apify GitHub Trending Scraper](https://apify.com/devilscrapes/github-trending-scraper), [johnku2011/github-trending-api](https://github.com/johnku2011/github-trending-api), [thedillonb/GitHub-Trending](https://www.github.com/thedillonb/GitHub-Trending). I found no GitHub changelog entry for a Trending API in 2026.
- github.com/explore is organised by content type, not skill: Open Source Fridays promo, Trending repositories, a GitHub Blog item, a Popular topic, one "Collection recommended by GitHub" (Game Engines, 64 items), staff-recommended Marketplace tools, Trending developers. Top-level tabs: Explore, Topics, Trending, Collections, Events, GitHub Sponsors. No beginner/intermediate/advanced labels — [GitHub Explore](https://github.com/explore)
- GitHub docs say Explore gives personalised recommendations of projects and good first issues based on your own contributions and stars, and that topics can be browsed at github.com/topics/<topic>. Docs describe no skill-level filter; "good first issue" is the nearest beginner signal — [GitHub Docs: finding ways to contribute](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- GitHub docs say "Many of GitHub's repository rankings depend on the number of stars a repository has" — [GitHub Docs: saving repositories with stars](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)
- Topics: github.com/topics/ai lists 197,069 public repos, sorted by most stars by default, with options for fewest stars, most/fewest forks, recently updated, and least recently updated; language filters (Python 62,146; TypeScript 39,674; JavaScript 20,745 …); related topics deep-learning, machine-learning, neural-network; no beginner section — [GitHub topic: ai](https://github.com/topics/ai)
- The Topics index features 16 topics (Awesome Lists, Chrome, Code quality, Compiler, CSS, Database, Front end, JavaScript, Node.js, npm, Project management, Python, React, React Native, Scala, TypeScript); none is AI-related. "llm" and "claude-code" appear only under "Popular topics" — [GitHub Topics](https://github.com/topics)
- Collections page is described as "Curated lists and insight into burgeoning industries, topics, and communities"; 22 shown with "Load more". AI-relevant: "Getting started with machine learning". Beginner-oriented: "How to choose (and contribute to) your first open source project", "Learn to Code". The page does not say who curates — [GitHub Collections](https://github.com/collections)
- Topics and Collections content lives in the github/explore repository, described as "community-curated content for GitHub Topics and Collections"; contributions are checked by lint tests; content licence CC-BY-4.0. Collections are "hand-picked repositories, developers, organizations, videos, and articles that share a common theme" — [github/explore](https://github.com/github/explore)
- Older context (dated 2014, updated 2019): GitHub staff "Showcases" were hand-grouped trending repos; the post does not say how trending is computed — [GitHub blog: Showcasing interesting projects in Explore](https://github.blog/news-insights/showcasing-interesting-projects-in-explore/)
- Per-repo GitHub tags are owner-supplied topics, so AI-topic grouping depends on how well repo owners tag — [GitHub topic: ai](https://github.com/topics/ai) (page shows topic tags on every listing)

### Inferences
- GitHub is strongest on (2) AI topic via `topic:` tags and weakest on (1), (4) and (5). It is a feed of popularity, not a judgement of usability.
- The one real gap GitHub leaves open is "what can a beginner actually run", which none of Trending, Topics or Collections touches.
- Topic pages sorted by stars favour old, huge repos; "recently updated" is the only freshness lever.

### Gaps
- Exact Trending algorithm: GitHub does not publish it; I found nothing official.
- Whether spoken-language filtering covers AI repos well; not tested.
- Total number of Collections and last-commit date of github/explore were not visible.

## 2. What do star-history, OSS Insight, Best of JS, Trendshift, gitstar-ranking, GitHunt, Awesome lists and 2025–2026 entrants offer, and where do they stop?

### Takeaway
Almost all are metric-driven (stars, star velocity, events) with little or no human judgement; the human-curated ones (Awesome lists, Best of JS, Pinokio "Featured") do not test code. OSS Insight's trending rankings are currently paused because its data is wrong, and the long-standing gitstar-ranking repo is now archived. None offers skill-level grouping, bar one weak, unexplained "difficulty estimate" claim on GitTrend.

### Cited Findings

**Star History (star-history.com)**
- Star-growth graphs for any repo, plus Star Map, Star Compare, Top Committers (with an "AI Coding" category), a Chrome extension and an RSS feed; weekly top-20 list "Updated Oct 30, 2026 – Nov 5, 2026" showing star gains. Maintained by Bytebase, originally built by @tim_qian — [Star History](https://www.star-history.com)
- Business model: sponsored placements (Bytebase, Dify, SerpApi shown) and a "Promote your product" link; no pricing or API shown — [Star History](https://www.star-history.com)
- Lacks: (1), (3), (4), (5); (2) only through the AI Coding list.

**OSS Insight (ossinsight.io)**
- Free analytics platform run and sponsored by PingCAP (TiDB Cloud); built on GitHub REST API and GH Archive; homepage claims "over 10 billion GitHub events" (docs page says "5+ billion rows" — inconsistent) — [OSS Insight](https://ossinsight.io), [OSS Insight docs](https://ossinsight.io/docs)
- Star-based rankings are currently paused: GitHub changed how its public events feed is paginated, so star, PR and issue data from mid-2025 onward is incomplete; data before May 2025, repo totals and commit activity are unaffected. The trending page shows only this notice — [OSS Insight trending](https://ossinsight.io/trending)
- Collections are curated repo lists (monthly/historical rankings per technical field); anyone can propose one by pull request with a .yml file — [OSS Insight docs](https://ossinsight.io/docs)
- Repo (pingcap/ossinsight): Apache-2.0, 2,523 stars, last push 5 November 2026, not archived; describes "LLM-powered natural-language queries" over the data — [GitHub API: pingcap/ossinsight](https://api.github.com/repos/pingcap/ossinsight)
- Lacks: (1), (4), (5); (3) light (PR-submitted collections); (2) via collections only, and currently without live star rankings.

**Best of JS (bestofjs.org)**
- Ranks by stars added yesterday ("Hot Projects") and previous month; tracks 3,654 projects (1,524 active); tag list (AI tag: 103 projects); data refreshed from GitHub every 24 hours, last update 7 November 2026 01:19 GMT; visitors recommend projects via GitHub issue template; a "Featured" section and "Recently Added" list. Run by Michael Rambeau, funded via GitHub Sponsors; scope includes "AI tooling" but is JavaScript-ecosystem only — [Best of JS](https://bestofjs.org)
- Repo: MIT, 3,137 stars, last push 7 November 2026 — [GitHub API: bestofjs/bestofjs](https://api.github.com/repos/bestofjs/bestofjs)
- Lacks: (1), (4), (5); (2) only an AI tag; human curation of what is admitted (project list) but not tested.

**Trendshift (trendshift.io)**
- Ranks by "daily momentum" (formula not given); Daily/Weekly/Monthly/Yearly views, Live mentions feed, Developers, Insights, Stats; created by Julian Li (liweiyi88) — [Trendshift](https://trendshift.io)
- Topics are "AI-categorized trends, curated by Trendshift": about 64 topics including AI agent, AI coding assistant, AI skills, AI infrastructure, LLM inference, RAG, vector database, voice agent. No beginner/skill grouping — [Trendshift topics](https://trendshift.io/topics)
- Business model: sponsor slot (Bifrost featured; "180K+ monthly visitors" claimed) with a flat-rate advertising offer; paid "Signal" plan at $9/month for AI search and API v1 (MCP server and "Deep insights" listed as coming soon); API terms bar redistribution/resale of raw data — [Trendshift](https://trendshift.io), [Trendshift Signal](https://trendshift.io/signal)
- Lacks: (1), (4), (5); (3) metrics-led with AI-generated topic labels; (2) strong.

**GitTrend (gittrend.io; est. 2026)**
- Ranked by star velocity; Daily trending, "Rising stars" (repos under 6 months old), "Hidden gems" (under 2,000 stars with outsized recent activity), trending developers; topics derived from descriptions, README content and declared topics; claims 50M+ repos tracked and 50,000+ actively ranked daily; list dated 6 November 2026; "purely algorithmic" — [GitTrend](https://gittrend.io), [GitTrend about](https://gittrend.io/about)
- Methodology: GH Archive events ingested hourly; star/fork totals verified against GitHub GraphQL; snapshot history begins 28 March 2026; publishes no ratings or reviews because "stars are a popularity signal, not a quality measure"; data CC0 — [GitTrend methodology](https://gittrend.io/methodology)
- The about page says each repo page has a "difficulty estimate", but the one repo page I checked (nilbuild/githunt) showed "Skill level: Not rated" and no setup or security section. Treat the claimed difficulty feature as unconfirmed — [GitTrend about](https://gittrend.io/about), [GitTrend repo page](https://gittrend.io/repo/nilbuild/githunt)
- Operator unnamed. Business model: Google AdSense ads, "Advertise" slots, paid "video reel" promotion, Buy-me-a-coffee; states it takes no money for ranking or inclusion — [GitTrend about](https://gittrend.io/about), [GitTrend](https://gittrend.io)
- Lacks: (4), (5); (1) at best a weak unverified estimate; (2) topic categories exist (AI Agent, AI Coding Assistant, AI Infrastructure); (3) algorithmic.

**WhatsTrending.ai**
- Ranks by stars gained in a 7-day window (31 October to 7 November 2026 shown), also 30-day gain; trend labels Accelerating/Steady/Stalled/Declining; topic rankings for MCP, RAG/vector search, coding agents, agent frameworks; 77,342 snapshots over 142 days since 19 June 2026; free CSV/JSON, README badge and API; operator not named; no testing or verification; no licence column — [WhatsTrending.ai](https://whatstrending.ai/repos)
- A search snippet described "trust scores" and about 2,246 AI/ML repos, but the page I fetched did not mention trust scores; unconfirmed — [search result listing](https://whatstrending.ai/repos)
- Lacks: (1), (3), (4), (5).

**SignalAI (signal-ai-two.vercel.app)**
- "GitHub's trending AI repos ranked and scored. Updated daily." Categories All/Agents/LLMs/Infra/UX/Other; filters for time window (Today to 90 days), source type, minimum relevance score and minimum stars; scoring method and operator not stated; no skill or tested labels. Hosted on a vercel.app subdomain, so likely a small or early-stage project — [SignalAI](https://signal-ai-two.vercel.app/repos)
- Lacks: (1), (4), (5); (3) algorithmic.

**GitHunt**
- Chrome new-tab extension and web app, by Kamran Ahmed (MIT). Most-starred repos by day/week/month with one language filter. Repo now described as "Hunt the most starred projects on any date on GitHub", 3,211 stars, last push 6 November 2026, active — [GitHub API: kamranahmedse/githunt](https://api.github.com/repos/kamranahmedse/githunt), [freeCodeCamp: GitHunt](https://www.freecodecamp.org/news/how-to-find-trending-github-projects-using-githunt-in-chrome-cb2d2a8f2468/)
- A third-party extension-audit page flagged the Chrome extension as "Could be malicious" and "Removed" (low-quality source; check store status directly) — [Extension Auditor via search result](https://extensionauditor.com/scan/githunt-khpcnaokfebphakjgdgpinmglconplhp)
- Lacks: all five dimensions apart from basic language filter.

**Gitstar Ranking (gitstar-ranking.com)**
- The site did not resolve from my fetch tool (DNS error) on 7 November 2026, so I could not read it; unverified whether it is online. Its source repo k0kubun/gitstar-ranking ("GitHub star ranking for users, organizations and repositories") is **archived**, MIT, 825 stars, last push 3 November 2026 — [GitHub API: k0kubun/gitstar-ranking](https://api.github.com/repos/k0kubun/gitstar-ranking). Treat as effectively end-of-life. It is a cumulative-star leaderboard, not a trending tool (from the repo description only).

**Awesome lists**
- sindresorhus/awesome: 532.7k stars, CC0, last push 2 September 2026; pull requests "temporarily disabled" and only collaborators can create issues/PRs; no dedicated AI section (AI lists scattered across categories) — [sindresorhus/awesome](https://github.com/sindresorhus/awesome), [GitHub API](https://api.github.com/repos/sindresorhus/awesome)
- Admission rules for new lists: at least 30 days old, not AI-generated, CC0 or Creative Commons licence, awesome-lint passed, entries must exclude unmaintained/archived/undocumented projects, applicant must review four other PRs. This is human gatekeeping of the list, not testing of listed code — [awesome PR template](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md)
- Hannibal046/Awesome-LLM: 27.5k stars, CC0, organised by topic (papers, open LLMs, evaluation, training frameworks, inference, applications, tutorials). Self-described "opinionated"; no beginner section. **Last push 31 July 2025**, so about 15 months stale — [Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM), [GitHub API](https://api.github.com/repos/Hannibal046/Awesome-LLM)
- steven2358/awesome-generative-ai: 12.8k stars, CC0, grouped by modality; has DISCOVERIES.md for up-and-coming projects; last push 30 October 2026; includes commercial products such as Jasper and Midjourney; criteria in CONTRIBUTING.md not read — [awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai), [GitHub API](https://api.github.com/repos/steven2358/awesome-generative-ai)
- e2b-dev/awesome-ai-agents: 30.8k stars, 1.1k open pull requests (backlog), licence "Other", last push 21 August 2026; maintained by the company E2B, whose docs link carries UTM tracking, so it is vendor-run — [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents), [GitHub API](https://api.github.com/repos/e2b-dev/awesome-ai-agents). (One fetch of the API call failed with a connection reset; the second succeeded.)
- Lacks (all four): (1) skill level; (4) testing; (5) security/licence screening beyond list-level licence. Strong on (3) human curation and (2) topic grouping. Freshness varies from days to over a year.

**Newer 2025–2026 curated AI lists and directories**
- bobpage0451/ai-trending-repos: 14 stack layers, tables with stars/forks/licence/language per project, "Last updated: 2026-11-03 (refreshed bi-weekly)"; MIT; only 5 stars; selection method not explained; no testing claims; sections by stack layer not skill — [ai-trending-repos](https://github.com/bobpage0451/ai-trending-repos)
- Awesome Open Source AI (awesomeosai.com): index by Core/Model/Serving/Agents/RAG/Media/Training etc.; shows licence, stars and language per entry; no skill labels; unverified performance claims; operator unnamed; newsletter signup; no last-updated date — [awesomeosai.com](https://awesomeosai.com/)
- Vibe-coding lists: 0xWelt/Awesome-Vibe-Coding, filipecalegario/awesome-vibe-coding (about 3.9k stars per an aggregator), acvnace/awesome-vibe-coding-resources (appears the most beginner-oriented, with a "What is vibe coding" section and course links), taskade/awesome-vibe-coding, techiediaries/awesome-vibe-coding. These list tools and learning resources, not trending repos. I did not open the repos directly, so details come from a search summary — [search listing of vibe-coding lists](https://github.com/0xWelt/Awesome-Vibe-Coding), [awesome.ecosyste.ms entry](https://awesome.ecosyste.ms/lists/acvnace%2Fawesome-vibe-coding-resources)
- Editorial roundups (ByteByteGo "Top AI GitHub Repositories in 2026", daily.dev, Firecrawl blog, Medium): human-picked but one-off articles; some sponsored or affiliate-linked — [ByteByteGo](https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026), [Firecrawl](https://www.firecrawl.dev/blog/best-github-repos), [daily.dev](https://daily.dev/posts/top-ai-github-repositories-in-2026-v10mv2s4d)
- GitGyan: an "open-source, AI-powered GitHub discovery engine" listed on an AI Tinkerers (Atlanta) talk page; I could not read it (HTTP 403), so features and any skill classification are unknown — [AI Tinkerers talk](https://atlanta.aitinkerers.org/talks/rsvp_jokrqK7-x3w)

### Inferences
- The field has converged on one pattern: GH Archive or GitHub API star deltas, a topic taxonomy (often AI-generated), a free site monetised by ads/sponsors/API. The pattern is fragile: GitHub's 2024–2025 event-feed changes broke star counting at OSS Insight and prompted GitTrend to switch to snapshot differences and GraphQL checks.
- GitTrend's "Hidden gems" and "Rising stars" views are the nearest thing to editorial slicing, but they are algorithmic filters, not judgement of difficulty.
- Awesome lists give the best human curation but go stale (Awesome-LLM, 15 months) or become vendor-run (awesome-ai-agents).
- Skill-level grouping (dimension 1) appears absent across every tool checked. That is the clearest white space.

### Gaps
- Gitstar Ranking site could not be loaded; current status unverified.
- GitTrend's "difficulty estimate" could not be confirmed on a live repo page; I checked only one repo (a non-AI one).
- Star History pricing/API not found; Star History and OSS Insight monetisation beyond sponsorship not stated.
- OSS Insight "AI features" were not described on the pages read.
- Trendshift and SignalAI/WhatsTrending scoring formulas not published on pages read.
- No Hacker News or Product Hunt launch threads were retrieved (search returned none for these tools), so launch-era claims and user criticism are not covered.

## 3. Which have an AI/LLM focus, and which group repos by what a beginner could run?

### Takeaway
AI focus is common and growing (Trendshift, GitTrend, WhatsTrending.ai, SignalAI, ai-trending-repos, Awesome-LLM and others). I found no tool that groups AI repos by what a beginner can run; the nearest are Pinokio (hardware/platform filters for one-click local AI apps) and GitHub's beginner Collections.

### Cited Findings
- AI-specific or AI-heavy: SignalAI (AI repos only) — [SignalAI](https://signal-ai-two.vercel.app/repos); WhatsTrending.ai (AI/ML topic rankings: MCP, RAG, coding agents, agent frameworks) — [WhatsTrending.ai](https://whatstrending.ai/repos); Trendshift (about 64 topics, a quarter of them AI-related) — [Trendshift topics](https://trendshift.io/topics); GitTrend (AI Agent, AI Coding Assistant, AI Infrastructure topics) — [GitTrend](https://gittrend.io); Star History "AI Coding" committers category — [Star History](https://www.star-history.com); Best of JS AI tag, 103 projects — [Best of JS](https://bestofjs.org)
- Pinokio: free MIT-licensed desktop launcher (repo pinokiocomputer/pinokio, 8,374 stars, last push 5 November 2026) that installs local AI apps through scripts and bundles Python, Node.js, Git and Conda. Its online catalogue filters by type, platform (macOS/Windows/Linux) and GPU (NVIDIA/AMD/Apple), sorted by recommended, latest or check-ins — [Pinokio](https://pinokio.co/), [GitHub API](https://api.github.com/repos/pinokiocomputer/pinokio), [Decrypt guide](https://decrypt.co/232430/how-to-run-ai-on-your-local-computer-with-pinokio?amp=1)
- Pinokio's "Featured" label is not explained, and a Pinokio security note says app developers "remain responsible for the security of their own code" — [Pinokio](https://pinokio.co/)
- A reviewer notes base-spec laptops without a discrete GPU struggle with most flagship Pinokio apps — [Decrypt](https://decrypt.co/232430/how-to-run-ai-on-your-local-computer-with-pinokio?amp=1) (secondary, SEO-style source)
- GitHub's beginner-oriented content is limited to Collections such as "Getting started with machine learning" and "Learn to Code", and the "good first issue" label for contributors — [GitHub Collections](https://github.com/collections), [GitHub Docs](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- Hugging Face Spaces (trending page): sort by relevance, task tags (Image Generation, Chatbots, Agents, MCP), "Featured" label, and runtime status per app (Running, Paused, hardware variants) — [Hugging Face Spaces](https://huggingface.co/spaces). This shows apps that run in the browser, not GitHub repos.

### Inferences
- "Beginner" in existing tools means "no coding needed to use" (Pinokio, Spaces demos), not "easy repo to read or modify". A gateway's skill levels would need its own definition (for example, no setup / needs Python / needs GPU or API keys).
- Pinokio and Hugging Face are adjacent competitors for the "just run it" job, but neither starts from GitHub trending.

### Gaps
- No evidence found of any trending tool with beginner/intermediate/advanced labels for AI repos.
- Pinokio's operator and business model are not stated on its site.

## 4. Is there any tool that marks repos as "runs on first try", "one-click deploy", or verified-working?

### Takeaway
One-click deploy exists (Railway templates, Pinokio scripts) but "verified" labels are undefined or absent; no tool I found tests repos and publishes the result. The closest are weekly health checks that only read GitHub metadata.

### Cited Findings
- Railway lists 1,548 AI templates that deploy a stack (services, databases, volumes, variables) in one click. There is no platform-wide verification system; "Official" in a title seems to mean the upstream image is used, one title says "(Verified)" and another "[Premium Template]" with no definition; many listings have no named creator; pricing is usage-based with a free trial; per-listing cost claims are the listers' own — [Railway AI templates](https://railway.com/deploy/category/ai)
- glincker/awesome-selfhosted-ai: self-hosted AI list "health-checked weekly, dead projects removed automatically". The check reads GitHub API data (stars, last push, licence, status) and moves archived, deleted or year-idle projects to UNMAINTAINED.md. It does not install or run anything. Author GDS K S (thegdsks); post dated 31 October 2026 — [DEV Community post](https://dev.to/thegdsks/i-built-a-self-hosted-ai-list-that-checks-itself-weekly-3m0a), [repo](https://github.com/glincker/awesome-selfhosted-ai)
- Awesome Open Source AI shows per-entry licence, stars and language but offers no run-test or verification method — [awesomeosai.com](https://awesomeosai.com/)
- WhatsTrending.ai states it does not audit or verify the projects it lists — [WhatsTrending.ai](https://whatstrending.ai/repos)
- GitTrend: "no synthesized ratings or reviews"; stars are not a quality measure — [GitTrend methodology](https://gittrend.io/methodology)
- A web search for a directory verifying that projects deploy on first try returned none — [search results incl. Railway and selfhostedAI](https://railway.com/deploy/category/ai). josStorer/selfhostedAI is a one-click installer collection that looks old (roughly 1,300 days per the search summary) — [josStorer/selfhostedAI](https://github.com/josStorer/selfhostedAI)
- Hugging Face Spaces status labels (Running/Paused) show whether a hosted demo is currently up, which is the closest live "does it run" signal in the survey — [Hugging Face Spaces](https://huggingface.co/spaces)

### Inferences
- "Tested before listing" is unoccupied space. Health-checks for liveness (archived or idle) exist; execution tests (clone, install, launch, record result) do not appear in any surveyed tool.
- A deploy template existing is not proof of working; undefined "Verified" tags show the risk of weak labels.

### Gaps
- I did not examine Vercel/Netlify "Deploy" buttons, Replit/Codespaces "open in" badges or Docker Hub verified publishers; these may carry weaker run signals.
- Pinokio's script testing process, if any, was not found.

## 5. Security or licence screening, and what business model does each use?

### Takeaway
Security screening is effectively absent across the survey; licence display is patchy (shown in Awesome Open Source AI and bobpage0451 tables; list-level only for Awesome lists). Business models are mostly free-with-ads/sponsors, with paid APIs emerging (Trendshift Signal, $9 per month).

### Cited Findings
- Licence/security coverage: Awesome Open Source AI shows per-entry licence — [awesomeosai.com](https://awesomeosai.com/); bobpage0451/ai-trending-repos includes licence column — [repo](https://github.com/bobpage0451/ai-trending-repos); glincker list records licence in weekly checks — [DEV post](https://dev.to/thegdsks/i-built-a-self-hosted-ai-list-that-checks-itself-weekly-3m0a); GitTrend shows licence on repo pages (MIT shown for githunt) but no security section — [GitTrend repo page](https://gittrend.io/repo/nilbuild/githunt); awesome-lint rules apply to list licensing, not to listed repos — [awesome PR template](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md); Pinokio leaves code security to app authors — [Pinokio](https://pinokio.co/)
- Business models:
  - GitHub Trending/Explore/Topics: free (part of GitHub); Explore links GitHub Sponsors — [GitHub Explore](https://github.com/explore)
  - Star History: free, sponsored placements, "Promote your product" — [Star History](https://www.star-history.com)
  - OSS Insight: free; sponsored by PingCAP/TiDB Cloud; open-source Apache-2.0 — [OSS Insight](https://ossinsight.io)
  - Best of JS: free; GitHub Sponsors — [Best of JS](https://bestofjs.org)
  - Trendshift: sponsor slot, flat-rate advertising, paid Signal plan $9/month — [Trendshift Signal](https://trendshift.io/signal)
  - GitTrend: AdSense, ad slots, paid video-reel promotion, tip jar; says no money for ranking — [GitTrend about](https://gittrend.io/about)
  - WhatsTrending.ai: free CSV/JSON, API and badge; no pricing stated — [WhatsTrending.ai](https://whatstrending.ai/repos)
  - Awesome lists: free, CC0; some vendor-run (E2B) — [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)
  - Railway: usage-based hosting revenue, free trial — [Railway AI templates](https://railway.com/deploy/category/ai)
  - Awesome Open Source AI: newsletter and a link to svgdiagram.ai — [awesomeosai.com](https://awesomeosai.com/)

### Inferences
- A paid AI search/API layer on top of free rankings (Trendshift) is the monetisation direction among newer entrants.
- Sponsor-based listings and ranking independence are in tension; only GitTrend states a no-pay-for-ranking policy.

### Gaps
- Star History, WhatsTrending.ai and Pinokio revenue models are not stated on pages read.
- No tool was found that runs vulnerability or secret scanning or checks licence compatibility for the repos it lists.

## Summary matrix (what each tool lacks, from the findings above)

| Tool | Data freshness (7 Nov 2026) | (1) Skill level | (2) AI topic | (3) Curation | (4) Run/tested | (5) Security/licence |
|---|---|---|---|---|---|---|
| GitHub Trending | current window only | none | none | metrics | none | none |
| GitHub Topics/Collections | live / community PRs | none (beginner Collections only) | topic tags | human + owner tags | none | none |
| Star History | week to 5 Nov | none | AI Coding committers only | metrics | none | none |
| OSS Insight | star rankings paused | none | collections only | metrics + PR collections | none | none |
| Best of JS | daily, 7 Nov | none | AI tag (JS only) | human-curated admission | none | none |
| Trendshift | live | none | strong (about 64 topics) | metrics + AI labels | none | none |
| GitTrend | 6 Nov | claimed, unconfirmed | topics | algorithmic | none | licence only |
| WhatsTrending.ai | 7 Nov | none | strong | metrics | explicitly none | none |
| SignalAI | daily claimed | none | AI-only | algorithmic | none | none |
| GitHunt | active repo | none | none | metrics | none | none |
| Gitstar Ranking | site unreachable; repo archived | none | none | metrics | none | none |
| Awesome lists | 2025 to Oct 2026 | none | yes | human | none | none |
| ai-trending-repos | 3 Nov | none | by stack layer | human | none | licence column |
| Pinokio | live | none (hardware filters) | yes | "Featured" (unexplained) | one-click install scripts, no verification stated | author-responsible |
| Railway AI templates | live | none | yes | none | one-click deploy, no verification | none |
