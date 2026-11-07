# Registries and marketplaces for AI coding-agent extensions (skills, MCP servers, rules, plugins, templates) as of 7 November 2026

Method note: pages were read only (nothing installed). Several pages were read through an automatic page summariser, so figures marked "page claim" are what the page displayed on 7 November 2026 and may not be independently checkable. Items I could not read directly are listed under Gaps in each section.

## Q1. What are the live MCP registries, and how do they rank, verify and count servers?

### Takeaway
There is one official, deliberately unopinionated metadata registry (preview, DNS/GitHub namespace verification, no code scanning) and a crowd of aggregators with very different sizes (Glama 117,029; PulseMCP 21,576; GitHub MCP Registry 771). Ranking is by popularity or recency, "official/verified" badges are about publisher identity, and none of the ones I read shows evidence that a listing was run or tested by the registry itself. Smithery has changed: its proxy and hosting shut down on 31 October 2026.

### Cited Findings

**Official MCP Registry (registry.modelcontextprotocol.io)**
- Still described as "in preview", with possible breaking changes or data resets before general availability; it is the official metadata repository backed by Anthropic, GitHub, PulseMCP and Microsoft — [MCP docs: Registry about](https://modelcontextprotocol.io/registry/about)
- It stores metadata (`server.json`) that points to packages on npm, PyPI, Docker Hub etc., not the code itself — [MCP docs: Registry about](https://modelcontextprotocol.io/registry/about)
- Verification is namespace authentication only: reverse-DNS names (`io.github.user/server`, `com.example/server`) tied to a verified GitHub account or domain; publishers prove ownership by GitHub, DNS or HTTP challenge — [MCP docs: Registry about](https://modelcontextprotocol.io/registry/about)
- Security scanning is explicitly delegated to underlying package registries and to downstream aggregators; maintainers can manually take down spam or malicious servers; AI-based spam detection and community reporting are only "under consideration" — [MCP docs: Registry about](https://modelcontextprotocol.io/registry/about)
- It is meant to be consumed by aggregators/marketplaces, not directly by host apps, and "deliberately unopinionated" so aggregators add curation and ratings — [MCP docs: Registry about](https://modelcontextprotocol.io/registry/about)
- The registry front page shows no total count; the API returns only a page `count` and `nextCursor`, no total — [Registry site](https://registry.modelcontextprotocol.io/), [Registry API](https://registry.modelcontextprotocol.io/v0.1/servers?limit=1)
- Third-party count (single author, API pull, latest version of each server): 30,375 unique servers (99,114 server-version records) on 10 September 2026, up from about 9,650 in May 2026; new servers per month rose from 407 (Sept 2025 launch) to 6,265 (Aug 2026) — [DEV: The MCP registry by the numbers](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc)
- Same analysis: 54.8% remote-only, 38.9% local package only; 22.9% list no source repository; "the schema has no auth method, security-review status, uptime check, or usage count"; 98.9% marked active and the registry "adds; it does not prune" — [DEV: The MCP registry by the numbers](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc)
- A search summary mentions a later blog claim of 52,042 servers on 28 October 2026; I did not open it, so treat it as unverified — [search result via apideck/eseospace list, not fetched](https://www.apideck.com/blog/mcp-server-directories)

**Glama (glama.ai/mcp/servers)**
- Page claim: "117,029 servers", updated 2026-11-07 — [Glama](https://glama.ai/mcp/servers)
- Default sort is search relevance; other sorts are recent usage, date added/updated, weekly npm downloads, weekly PyPI downloads, GitHub stars — [Glama](https://glama.ai/mcp/servers)
- Each card shows three A-F grades labelled license, quality and maintenance (some "Not graded"); no separate security score; method not explained on the page — [Glama](https://glama.ai/mcp/servers)
- Filters include categories (Developer Tools 28,153; Search 16,346; Databases 6,295; Security 6,221), hosting (Remote 45,937; Local 44,262; Hybrid 21,976) and author status (Claimed 10,570; Official 7,755) — [Glama](https://glama.ai/mcp/servers)
- The page shows no testing or "it runs" evidence from Glama itself — [Glama](https://glama.ai/mcp/servers)

**PulseMCP (pulsemcp.com)**
- Page claim: 21,576 servers (title "21,570+"); 42 per page over 514 pages — [PulseMCP](https://www.pulsemcp.com/servers)
- Default sort "Recommended" (method unexplained); also last updated, alphabetical, recently released, and most popular (all time / month / week) — [PulseMCP](https://www.pulsemcp.com/servers)
- Badges are "reference" (Anthropic reference), "official" and "community"; popularity is "Est Visitors (Week)", method undefined — [PulseMCP](https://www.pulsemcp.com/servers)
- New submissions and listing changes are "currently paused" while the site reworks ingestion — [PulseMCP](https://www.pulsemcp.com/servers)

**mcp.so**
- No total server count shown on the home page; shows Featured (described as hand-picked and production-ready), Trending (by star count), New, and Rankings — [mcp.so](https://mcp.so)
- Home page lists categories: Developer Tools, AI & Agents, Cloud & Infrastructure, Memory & Knowledge, Media & Design — [mcp.so](https://mcp.so)
- Also lists MCP clients, remote servers, CLI tools, "Loops", Agent Skills, Agents and Collections, so it is partly cross-type — [mcp.so](https://mcp.so)
- FAQ says listings go live after review and advises preferring official or well-maintained servers; no formal security badge system described — [mcp.so](https://mcp.so)

**Smithery (smithery.ai)**
- Smithery joined Arcade.dev; its MCP Proxy, managed identity, API, Connect, Toolbox, accounts/API keys, CLI and SDKs shut down on 31 October 2026 — [Smithery: future](https://smithery.ai/future), [Arcade blog](https://arcade.dev/blog/smithery-joins-arcade)
- What remains: the public smithery.ai directory (now run by Arcade.dev) and "a curated set of verified servers" whose pages list direct vendor MCP URLs — [Smithery: future](https://smithery.ai/future)
- Acquisition date is reported as 5 August 2026 by secondary sources; one review reports Arcade's homepage did not mention it on 28 October 2026; terms not disclosed — [runtimewire](https://runtimewire.com/article/arcade-acquires-smithery-agent-tool-supply-chain)
- The home page makes no ranking, verification or scanning claims — [Smithery](https://smithery.ai)
- A vendor (Bawbel) scan of the top 500 Smithery servers by install rank (497 scanned) found 76 (15.3%) with at least one finding; the author sells a scanner, calls findings "structural risk indicators", not proof of exploitation — [DEV: We scanned 500 MCP servers on Smithery](https://dev.to/bawbel/we-scanned-500-mcp-servers-on-smithery-here-is-what-we-found-4g8i)

**Composio (composio.dev/toolkits)**
- Not an MCP registry as such: page claim of 1,728 toolkits in 20 categories (largest: Data & Analytics 253; Developer Tools & DevOps 222; Productivity & PM 214), "20,000+ tools" via MCP or direct API — [Composio toolkits](https://composio.dev/toolkits)
- No vetting or review process described; new toolkits added weekly on request — [Composio toolkits](https://composio.dev/toolkits)

**Others**
- GitHub MCP Registry (github.com/mcp): 771 entries on the day read, publisher shown, Install button; no stated review or relationship to the official registry — [GitHub MCP Registry](https://github.com/mcp)
- Docker MCP Catalog: calls itself "the largest library of containerized MCP servers", "built by the community"; the page states no count, signing or scanning detail — [Docker Hub MCP](https://hub.docker.com/mcp)
- MCP Market (mcpmarket.com) has separate MCP-server and skills directories, rankings and a paid-skills seller page — [MCP Market skills](https://mcpmarket.com/tools/skills)

**Research on registry vetting**
- Academic study of 67,057 servers across six public registries: weak vetting and ownership checks let adversarial or hijacked servers reach hosts; its MCPInspect tool flagged 833 vulnerable servers and 18 with suspicious tool descriptions — [arXiv 2510.16558](https://arxiv.org/abs/2510.16558)

### Inferences
- "Number of servers listed" is not comparable across sites: Glama, PulseMCP and the official registry count different things (crawled repos, curated listings, version-deduplicated metadata). A vibe coder cannot treat any figure as "usable servers".
- No MCP registry I read grades by skill level. Topic grouping exists (Glama, mcp.so, Composio have category lists); PulseMCP's categories are about provenance (reference/official/community), not topic.
- Official-registry growth (about 3x in four months) with no pruning and no scanning means badges like "official" and "claimed" are about identity, not safety or function.

### Gaps
- mcp.so total count and ranking method not shown on pages I could read.
- Glama's grade formulas and whether it runs any servers (Glama is known for server pages with "inspect"/tool listings, but I did not verify this).
- A verified current count for the official registry (the 52,042 figure is from a search summary only).
- Smithery's current server count and what "verified" means after the Arcade change.

## Q2. What are the live marketplaces for Claude Code skills and plugins and for Cursor rules, and how do they curate?

### Takeaway
Anthropic runs a tiered plugin system (official, community, third-party) with a web marketplace showing "Anthropic verified" badges; community lists (awesome-claude-code, awesome-claude-skills) are hand-picked or PR-based with no stated testing; skills.sh is a metrics-ranked leaderboard with third-party security audits (Gen, Socket, Snyk) shown per skill. I could not read cursor.directory (HTTP 429).

### Cited Findings

**Anthropic plugin marketplaces**
- Two general marketplaces: `claude-plugins-official` (plugins Anthropic maintains plus partners and other authors) and `claude-plugins-community` / `claude-community` ("third-party plugins that their authors submitted to Anthropic"); topic marketplaces include `anthropics/skills` and `anthropics/knowledge-work-plugins` — [Anthropic's marketplaces](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md)
- Most of the official marketplace comes from partners and other authors, not Anthropic — [Anthropic's marketplaces](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md)
- "Anthropic doesn't review third-party marketplaces" — [Anthropic's marketplaces](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md)
- Web catalog at claude.com/marketplace: page claim "529 plugins", filter "Works with Claude / Claude Code", an "Anthropic verified" label on 22 of the 24 cards visible, but the page does not define it, shows no categories, sort or install counts (the docs say install counts are shown, so the page may vary) — [Claude Marketplace](https://claude.com/marketplace/plugins), [Anthropic's marketplaces](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md)
- Trust model: plugin can run arbitrary code with user privileges via hooks, monitors, MCP servers and `bin/`; every plugin shows the same warning that Anthropic "cannot verify that they will work as intended or that they won't change" — [Plugin security and trust](https://code.claude.com/docs/en/plugins/security.md)
- Safeguards: marketplace names `claude-plugins-official`/`claude-community` accepted only from `github.com/anthropics/` repos; community catalog pins nearly every plugin to a commit SHA and Claude Code refuses a different commit; optional `sha256` archive pinning — [Plugin security and trust](https://code.claude.com/docs/en/plugins/security.md)
- Official marketplace repo: 46.3k stars; external plugins submitted by form and "must meet quality and security standards for approval", but criteria and timelines are not published — [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Official marketplace plugin pages in Claude Code show "Last updated" and two token-cost estimates ("Every turn" and "When invoked") — [Install and manage plugins](https://code.claude.com/docs/en/discover-plugins)
- Enterprise-only upload scanning: when a member uploads or edits a third-party skill or plugin, Claude returns pass / warn / fail (1-2 minutes); it excludes MCP servers, skills shared via MCP, and items installed before enabling; "a pass doesn't mean safe in every respect" — [Claude Help: skill and plugin scanning](https://support.claude.com/en/articles/15927065)

**Anthropic skills repo and Agent Skills standard**
- `anthropics/skills`: about 188.3k stars; example skills in creative/design, development, enterprise/communication, and document skills (docx, pdf, pptx, xlsx); spec at agentskills.io; disclaimer says skills are "for demonstration and educational purposes only" and users should "test skills thoroughly" — [anthropics/skills](https://github.com/anthropics/skills)

**Community lists**
- awesome-claude-code (hesreallyhim): about 57.4k stars; "hand-picked"; PRs restricted to collaborators; page shows a security policy and a tests folder but no stated vetting or entry count — [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- awesome-claude-skills (ComposioHQ): about 79.0k stars; claims "1000+" skills but the itemised list has roughly 160 entries, about 78 of them Composio's own app-automation skills; 11 topic categories; contribution steps include "test across Claude.ai, Claude Code and API"; no security audit statement — [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

**skills.sh (community, Vercel-linked)**
- Leaderboard ranked by installs with tabs All Time, Trending (24h), Hot; top entry find-skills (vercel-labs/skills) with 4.2M installs; total not stated ("All Time 1,275,896" unlabelled) — [skills.sh](https://skills.sh)
- Topic filters (React, Next.js, Design & UI, Mobile, Agent workflows, Databases, Testing, Marketing), plus Official and Packs views; installs for 20 agents including Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini — [skills.sh](https://skills.sh)
- Audits page shows "combined security audit results from Gen Agent Trust Hub, Socket, and Snyk" per skill (Gen verdict, Socket alert count, Snyk risk level); unaudited skills show "Pending" — [skills.sh audits](https://skills.sh/audits)

**Other skill hubs**
- MCP Market: page claim 379,621 skills, 20 categories, "Official Skills" publishers, some "Premium" paid skills ($19), no security or testing badges; ranking figures unexplained — [MCP Market skills](https://mcpmarket.com/tools/skills)
- ClawHub (OpenClaw ecosystem): featured / trending / official / new tabs, download counts, "signed manifests", "moderated releases" and an Audits link; page showed 30 skills and 12 plugins (likely a partial view) — [ClawHub](https://clawhub.ai)
- One search summary says SkillsMP lists 96,000+ skills with "zero security audit" per a third-party directory; not verified — [DEV: Agent skills gold rush](https://dev.to/meimakes/the-agent-skills-gold-rush-has-a-malware-problem-2jai)

**Cursor rules**
- Cursor Directory (cursor.directory): shows "80.3k+ developers" and trending collections with unlabelled figures (e.g. 31.1k Front End); rules are added by pull request to `packages/data/src/rules/` in its GitHub repo, MCP servers via the website — [search summary of cursor.directory](https://cursor.directory/?q=ai), [repo mirror](https://github.com/maydayv/cursor.directory)
- Cursor now has an official plugins repo (github.com/cursor/plugins) — appeared in search results only; contents not read — [cursor/plugins](https://github.com/cursor/plugins)

### Inferences
- Metrics (installs, stars, downloads) drive ranking on skills.sh, MCP Market, ClawHub and Glama; only Anthropic's "verified" label, mcp.so "Featured", and the two awesome lists are editorial, and none publishes its criteria.
- Of everything read, skills.sh is the only skills site with per-listing third-party security results visible in the UI.
- No skills or plugin marketplace read groups by skill level (beginner/advanced); topic grouping is common.

### Gaps
- cursor.directory pages returned HTTP 429 twice; its categories, counts, moderation and any scanning are unconfirmed.
- Windsurf rules/marketplace, Codex skill directory, Cline, and Copilot marketplaces were not researched.
- What "Anthropic verified" requires is not defined on pages I read.
- awesome-claude-code's real selection criteria (CONTRIBUTING.md) were not read.

## Q3. What template galleries exist for vibe-coding tools, and do they grade by difficulty?

### Takeaway
Galleries exist for Lovable, v0, Vercel and Bolt, grouped by topic and persona/use case. I found no gallery that grades by difficulty or skill level; one fetch said Vercel does, but I could not corroborate it.

### Cited Findings
- Lovable templates: "228 results"; categories All / Websites / Apps with 21 subcategories (e.g. Portfolio, Ecommerce, SaaS, Internal Tools, Dashboards) and 14 audience/persona filters (e.g. Founders); described as "Production-ready apps from the Lovable community"; no difficulty, ranking or remix counts visible in the content read — [Lovable templates](https://lovable.dev/templates)
- v0 templates: 13 categories (Apps & Games, Landing Pages, Dashboards, Components, Login & Sign Up, E-commerce, AI, Animations, Design Systems, Layouts, Agents and others); community-published with author handles; "Trending" featured section; two unlabelled numbers per card; no difficulty levels mentioned — [v0 templates](https://v0.app/templates)
- Vercel templates: filters by framework, use case, CSS, database; large catalogue across Next.js, Nuxt, SvelteKit, Astro, Hono, Python, Go, Rust, plus AI SDK chatbots and storefronts — [Vercel templates](https://vercel.com/templates). The summariser also claimed "sorting and difficulty levels", which I could not confirm from the listing content; treat as unverified.
- Bolt: a press-style write-up says Bolt launched a Template Marketplace of full-stack apps (portfolios, dashboards, storefronts); bolt.diy offers 15+ starter templates; I did not reach an official Bolt template page — [createwith.com write-up](https://www.createwith.com/tool/bolt/updates/bolt-launches-free-template-marketplace-with-full-stack-ready-made-apps)
- Replit templates: the URL tried (replit.com/templates) returned 404, so unconfirmed — [Replit templates](https://replit.com/templates)

### Inferences
- Template galleries are topic- and persona-based, not skill-based; a beginner cannot filter by difficulty on the galleries I could read.
- Galleries are tool-specific (a Lovable template does not carry to Bolt), and none of them is linked to skills or MCP servers.

### Gaps
- Replit's current template gallery URL, and official Bolt template gallery details.
- Whether any gallery shows run/remix counts or quality checks (not visible in what I read).
- Whether Vercel's gallery has any difficulty grouping.

## Q4. Which security incidents and research concern malicious or prompt-injecting MCP servers, skills or rules files, and which registries now scan?

### Takeaway
There is solid evidence on all three vectors: tool poisoning and rug pulls (Invariant Labs, April 2025), a real backdoored MCP package (postmark-mcp, September 2025), hidden-Unicode rules files (Pillar, March 2025), and large skill-registry problems (ClawHavoc, January 2026; Snyk ToxicSkills, February 2026). Scanning is patchy: the official MCP registry delegates it; skills.sh shows third-party audits; ClawHub reportedly added scanning after ClawHavoc; Anthropic scans only in an Enterprise setting.

### Cited Findings

**MCP**
- Tool Poisoning Attack named by Invariant Labs on 1 April 2025: malicious instructions in tool descriptions "invisible to users but visible to AI models"; example in Cursor read `~/.cursor/mcp.json` and `~/.ssh/id_rsa`; a server can change a tool description after approval (rug pull); recommends showing full descriptions, hash-pinning tools and versions — [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- Invariant released MCP-Scan (hash-pinning) in April 2025; Snyk acquired Invariant in June 2025 (secondary source) — [search summary, unverified primary](https://labs.cloudsecurityalliance.org/research-rb/csa-whitepaper-mcp-security-tool-poisoning-20260506-csa-styl/)
- postmark-mcp (npm): a lookalike of Postmark's package; version 1.0.16 (17 September 2025) added a BCC line forwarding emails to an attacker; reported as about 1,500 weekly downloads / 1,643 total; Postmark said it had no involvement; billed as the first malicious MCP server in the wild — [Koi Security via search summary](https://koi.ai/blog/postmark-mcp-npm-malicious-backdoor-email-theft), [The Hacker News](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html) (both pages blocked on direct fetch; details from search summaries)
- arXiv 2510.16558 (October 2025): 67,057 servers over six registries; weak vetting and ownership checks; 833 vulnerable servers and 18 with suspicious tool descriptions flagged; the abstract does not mention typosquatting, though a search summary of the paper does ("names that closely resemble" legitimate ones) — [arXiv 2510.16558](https://arxiv.org/abs/2510.16558)
- arXiv 2604.01905 (April 2026): Connor detector; dataset of 114 malicious PoC servers; F1 94.6%; found two malicious servers in a real-world run (search summary says over 1,672 marketplace servers) — [arXiv 2604.01905](https://arxiv.org/abs/2604.01905)
- OWASP MCP Top 10 lists tool poisoning as MCP03:2025 (secondary source) — [search summary](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-ai-agent-exfiltration-2/)
- Vendor scan: top 500 Smithery servers, 15.3% had at least one finding (see Q1; commercial author) — [DEV: Bawbel](https://dev.to/bawbel/we-scanned-500-mcp-servers-on-smithery-here-is-what-we-found-4g8i)

**Rules files**
- Pillar Security "Rules File Backdoor", published 18 March 2025: hidden instructions in rule files via invisible Unicode; affects Cursor and GitHub Copilot; Cursor said the risk is the user's responsibility; GitHub added a hidden-Unicode warning on github.com on 1 May 2025 — [Pillar Security](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)

**Skills**
- ClawHavoc (ClawHub, January 2026): 1,184 malicious skills across 12 compromised publisher accounts; first published 3 January, found by Snyk 22 January, removed 28 January; ClawHub reportedly then added automated malware scanning, mandatory reviews for new skills, download-velocity monitoring and publisher identity checks — [OWASP Agentic Skills Top 10 case studies](https://owasp.github.io/www-project-agentic-skills-top-10/case-studies)
- Snyk ToxicSkills (5 February 2026): 3,984 skills from ClawHub and skills.sh; 1,467 (36.82%) with any flaw; 534 (13.4%) with a critical issue; 76 confirmed malicious payloads; 8 malicious skills still live on ClawHub at publication — [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/). Note: the OWASP page gives 533 critical, and some secondary sites misuse "1,467" as a malicious count (it is the count of flawed skills).
- Koi Security reported 341 malicious skills of 2,857 on OpenClaw's registry (February 2026), per a search summary — [DEV: gold rush](https://dev.to/meimakes/the-agent-skills-gold-rush-has-a-malware-problem-2jai)
- Search summary also names scanner-bypass research ("SkillCloak", Cloud Security Alliance) and "Plugin4Shell" (version-pin bypass, Claude Code, fixed) — not read directly — [DEV: gold rush](https://dev.to/meimakes/the-agent-skills-gold-rush-has-a-malware-problem-2jai)

**Who scans now**
- Official MCP Registry: no code scanning; namespace auth plus manual takedown only — [MCP docs](https://modelcontextprotocol.io/registry/about)
- skills.sh: per-skill Gen / Socket / Snyk results — [skills.sh audits](https://skills.sh/audits)
- Anthropic: Enterprise upload scanning (pass/warn/fail) — [Claude Help](https://support.claude.com/en/articles/15927065); plugin SHA pinning in community marketplace — [Plugin security](https://code.claude.com/docs/en/plugins/security.md)
- ClawHub: scanning reportedly added after ClawHavoc (OWASP page); its own page names "scanners" without detail — [OWASP case studies](https://owasp.github.io/www-project-agentic-skills-top-10/case-studies), [ClawHub](https://clawhub.ai)
- Glama, PulseMCP, mcp.so, Composio, MCP Market, GitHub MCP Registry: no scanning claim on the pages read (Q1, Q2)
- Manifold Security scores 7,700+ MCP servers (commercial product) — [search summary](https://dev.to/om_shree_0709/manifold-security-just-scored-7700-mcp-servers-heres-why-that-number-should-worry-you-1c22)

### Inferences
- The only real-world malicious MCP case found is postmark-mcp (npm), i.e. a package-registry problem as much as an MCP one; most MCP findings elsewhere are vulnerability or PoC counts, not confirmed malware in registry listings. I found no 2026 study that counts confirmed-malicious servers in registries.
- Skills have the strongest evidence of actual in-the-wild malice (ClawHavoc, ToxicSkills), so a "tested/scanned" signal has most value there.
- A scan result (even a "pass") is not evidence that the listing was run for its intended task; Anthropic's own page says a pass does not mean safe in every respect.

### Gaps
- Trail of Bits and Palo Alto Unit 42 write-ups were not read; typosquatting evidence specific to MCP registries rests on a search summary of arXiv 2510.16558.
- Primary Koi page blocked (redirect); The Hacker News page returned 403 on direct fetch.
- Snyk-Invariant acquisition and OWASP MCP03 code come from secondary summaries.
- Whether Smithery, Glama or PulseMCP now run security scans: not stated on the pages read.

## Q5. Is any site already cross-ecosystem (skills + MCP + repos + templates in one place)?

### Takeaway
Several third-party sites combine skills, MCP servers and plugins; none I read also includes starter templates or groups by skill level. Their counts are self-reported and inconsistent, and only one (agenticskills.io) claims manual review.

### Cited Findings
- mcp.so lists MCP servers, clients, remote servers, CLI tools, Agent Skills, agents, loops and collections — [mcp.so](https://mcp.so)
- MCP Market: MCP servers, skills (page claim 379,621), clients, a "Market Hub" that installs and syncs skills across Claude, Cursor and Codex — [MCP Market](https://mcpmarket.com/tools/skills)
- AgenticSkills.io: skills plus MCP servers; page claims 195+ skills and 141 MCP servers indexed; manual review of "whether it works, is maintained, and follows security best practices"; rates documentation, maintenance, install count, compatibility, security practices; topic categories (Development & Code, Security, Content & Marketing, Data & Analytics, etc.); "Works Well With" pairings; no skill-level grouping; no automated scanning claimed — [AgenticSkills.io](https://agenticskills.io/learn/claude-skills-marketplace)
- ClaudeMarket (claudemarket.ai) is described in a search snippet as one place for 13,870+ MCP servers, 4,384+ agent skills and Claude Code / OpenClaw / Hermes / Codex plugins; direct fetch returned 429 — [ClaudeMarket](https://www.claudemarket.ai/?page=208)
- skills.sh supports 20 agents but lists skills only — [skills.sh](https://skills.sh)
- Claude Code plugins bundle skills, agents, hooks and MCP servers in one unit, so the official marketplace is cross-type in packaging terms — [Plugin security](https://code.claude.com/docs/en/plugins/security.md)
- AgentInit hosts a git-based marketplace for skills, MCP servers and rules (search snippet only) — [agentinit/marketplace](https://github.com/agentinit/marketplace)
- A search for beginner/difficulty filters in MCP directories found only blog guides and an unconfirmed claim that MyMCPShelf filters by "easy" or "beginner-friendly" — [search results](https://mcp-find-web.vercel.app/blog/mcp-servers-no-code-non-developers)

### Scorecard (my assessment from the pages read; Y = present, P = partial, N = not seen, ? = could not check)

| Registry | 1 Skill-level grouping | 2 Topic grouping | 3 Editorial vs metrics | 4 Evidence listing was run/tested | 5 Security screening |
|---|---|---|---|---|---|
| Official MCP Registry | N | N (no categories) | Neither: unopinionated metadata | N | P: DNS/GitHub namespace auth, manual takedown, no code scan |
| Glama | N | Y (categories, attributes) | Metrics plus A-F grades (method unstated) | N seen | N seen (license/quality/maintenance grades only) |
| PulseMCP | N | P (provenance classes) | Mixed: official/reference flags plus visitor metric | N | N |
| mcp.so | N | Y (5 top categories) | Mixed: hand-picked Featured, star-based Trending | N | N (review before listing, no badge) |
| Smithery | N | ? | Curated "verified" set remains | N | N (vendor scan exists, not Smithery's) |
| Composio toolkits | N | Y (20 categories) | Vendor catalogue | N | N |
| GitHub MCP Registry | N | ? | Unclear | N | N |
| Claude Marketplace / plugins | N | N seen | Editorial label ("Anthropic verified", undefined) | N | P: pins, Enterprise scan, warning only |
| awesome-claude-code | N | Y (resources) | Editorial (hand-picked) | N stated | N stated |
| awesome-claude-skills | N | Y (11 categories) | PR-based, vendor-led | P: "test across platforms" guidance | N |
| skills.sh | N | Y (topics, packs) | Metrics (installs) plus Official view | N | Y: Gen, Socket, Snyk audits |
| MCP Market | N | Y (20 categories) | Metrics plus paid featured | N | N |
| ClawHub | N | ? | Metrics (downloads) plus Official | N | P: scanning reportedly added post-ClawHavoc |
| cursor.directory | ? | Y (collections by stack) | Metrics (popularity) | ? | ? |
| AgenticSkills.io | N | Y | Editorial | P: manual "works" check claimed | P: manual best-practice review only |
| Lovable / v0 / Vercel template galleries | N | Y (category, persona, framework) | Mixed | N | N |

### Inferences
- Dimension 1 (skill level) is empty across everything read; this is the clearest gap.
- Dimension 4 (evidence a listing was run) is almost empty: the only claim is AgenticSkills.io's manual check; GitHub-star-style popularity is used as a proxy elsewhere.
- Dimension 5 is strongest on skills.sh and weakest on large MCP aggregators.
- Cross-ecosystem sites exist (mcp.so, MCP Market, AgenticSkills.io, ClaudeMarket) but templates for vibe-coding tools are not combined with skills and MCP anywhere I looked.

### Gaps
- ClaudeMarket and cursor.directory could not be read directly (HTTP 429), so their features are unconfirmed.
- Self-reported counts (ClaudeMarket 13,870 servers/4,384 skills; AgenticSkills.io 69,849 skills on skills.sh in February 2026; MCP Market 379,621 skills) conflict with each other and with skills.sh's own figures; none independently checked.
- Windsurf, Codex, Replit and Bolt official extension directories were not researched.
