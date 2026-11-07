# Developer news, social platforms, newsletters and directories as discovery gateways for AI repos (state as of 7 November 2026)

Method note: the page-reading tool returns model-written summaries, not raw page text. Quotes below are as reported by that tool. Items marked "verify" should be checked against the primary page before a decision. Many figures are self-reported marketing claims.

## 1. Developer social and feed platforms: how do they surface repos, and how big are they?

### Takeaway
Discovery on these platforms is ranked by engagement metrics (votes, upvotes, composite traction scores), not by skill level or tested status. Only Hacker News's Show HN has a "can people run it" rule; daily.dev has tag filters and a feed API. Reddit is closing its RSS feeds and public API, so it is a poor ingestion source.

### Cited Findings
- **daily.dev**: its own advertising page claims an audience of "1 million+ active developers". This is an ad-platform claim, not an audited monthly figure. — [daily.dev blog](https://daily.dev/blog/developer-marketing-platforms-comparison-channel-mix/)
- daily.dev: a BuySellAds listing gives 100K active daily users and 15M monthly views (undated, may be stale). — [BuySellAds](https://discover.buysellads.com/daily-dev)
- daily.dev Public API (beta): REST base `https://api.daily.dev/public/v1`; feeds (For You, trending, tag/source filtered, most discussed), search of posts/tags/sources, bookmarks, custom feeds, tags; OpenAPI spec; an MCP server at `https://api.daily.dev/mcp`. — [daily.dev docs](https://docs.daily.dev/docs/plus/public-api)
- daily.dev API limits: 300 requests/minute per IP; 60 requests/minute per user (shared across tokens, OAuth apps and MCP calls); Plus subscribers get higher limits and extra endpoints. — [daily.dev docs](https://docs.daily.dev/docs/plus/public-api)
- daily.dev: an earlier search snippet said the Public API is restricted to Plus subscribers; the docs page fetched later says any user can use it and Plus raises limits. These conflict; the docs page is the more direct source. — [docs (any user)](https://docs.daily.dev/docs/plus/public-api); snippet source [docs index](https://docs.daily.dev/public-api.md)
- daily.dev feeds can be filtered by tag and source (so a topic grouping exists), but no skill-level grouping appeared in the API description. — [daily.dev docs](https://docs.daily.dev/docs/plus/public-api)
- **Hacker News**: the official API is at `https://hacker-news.firebaseio.com/v0/`, MIT-licensed repo, and the docs say "There is currently no rate limit." — [HN API on GitHub](https://github.com/HackerNews/API)
- Hacker News Show HN rules: must be something people can run or try; excludes blog posts, lists, newsletters, landing pages and "quickly generated one-offs" because "anybody can do that now". The rules do not mention AI-generated projects directly. — [Show HN rules](https://news.ycombinator.com/showhn.html)
- Hacker News guidelines: "Please don't put generated text in HN posts"; users are asked not to automate posting. — [HN guidelines](https://news.ycombinator.com/newsguidelines.html)
- Hacker News Show HN is under strain from AI-built projects. Secondary blogs report submissions "tripled" and moderators moving to restrict Show HN for new accounts (March 2026). No official HN announcement was found. — [keydiscussions](https://keydiscussions.com/2026/03/09/hacker-news-moves-toward-restricting-show-hn-posts-amid-the-ai-slop-wave/); [feedbagel analysis](https://feedbagel.com/post/analysis-of-ai-generated-project-proliferation-in-hacker-news-show-hn-submission)
- **Reddit**: r/vibecoding size estimates conflict: about 392,000 (GummySearch, undated) versus about 252,000 as of May 2026 (blog citing FreeSubStats). — [GummySearch](https://gummysearch.com/r/vibecoding/); [sorceress.games](https://sorceress.games/blog/vibe-coding-reddit-top-threads-decoded-2026)
- Reddit: r/opensource moderators reportedly barred projects that use, are made by or are intended for AI, effective 24 October 2026 (secondary report). — [Help Net Security](https://helpnetsecurity.com/2026/10/26/reddit-r-opensource-ai-ban)
- **Peerlist Launchpad**: weekly launch; ranked by an aggregate score of upvotes, comments, views, link visits and traction; first two days shown in random order; verified-profile votes weigh more; only verified users can launch; free to launch as of October 2026. — [Peerlist help](https://help.peerlist.io/individual/launchpad/guidelines-faqs); [Peerlist blog](https://peerlist.io/blog/commentary/peerlist-launchpad-the-path-forward)
- **DEV Community / Forem**: API v1 needs an `accept: application/vnd.forem.api-v1+json` header and an API key on many endpoints; rate limits and reuse terms not stated on the page read. — [Forem API](https://developers.forem.com/api/)
- DEV Community serves per-author RSS at `dev.to/feed/<user>` (seen in search results). — [example feed](https://dev.to/feed/techloghub)
- **Hashnode**: tag feeds such as `hashnode.com/n/ai` exist (seen via a third-party scraper); official API/RSS terms not confirmed. — [Apify scraper page](https://apify.com/automation-lab/hashnode-scraper)
- **GitHub scale context**: GitHub's Octoverse 2026 (published 28 October 2026, updated 6 November 2026) reports more than 225 million developers, 25 million public repos by industry growth, and over 40% of pull requests started by agents as of September 2026. It gives no total count of "AI repos". — [GitHub blog](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- **GitHub Trending**: no official API; the page is server-rendered HTML (about 25 repos per language/time window, refreshed roughly every few hours per vendor claims). Third-party scrapers and tools (OSSInsight, Trendshift) fill the gap. — [Apify scraper](https://apify.com/themineworks/github-trending-scraper); [OSSInsight](https://ossinsight.io/blog/introducing-trending-page); [Trendshift](https://trendshift.io/repositories/128454)

### Inferences
- Every platform here ranks on popularity or engagement. None groups by skill level, and none shows evidence a repo was run, except HN's "must be runnable" admission rule (which is a gate, not a displayed badge).
- daily.dev is the only feed with a documented API and tag-level topic filters, which makes it the most structured gateway of this group.
- AI-generated project floods on HN and Reddit are the clearest signal of demand for a filtered, trust-led layer.

### Gaps
- Official audience figures for DEV, Hashnode, Peerlist, HN: not found in this pass.
- X/Twitter AI-dev accounts, Discord servers and YouTube channels: not researched (no sourced findings).
- r/ClaudeAI, r/LocalLLaMA, r/MachineLearning, r/artificial member counts: not retrieved.
- HN Algolia API terms and rate limits: the Algolia page returned only a title, so nothing confirmed.
- Hashnode and Peerlist API/RSS documentation: not found.

## 2. AI newsletters: frequency, size, repo selection, difficulty rating

### Takeaway
The big AI newsletters are daily or weekly, human-edited news digests with 100k to 1M+ readers (self-reported) and sell sponsorship. None found rates difficulty or tested status. Repo-focused issues exist (Changelog Nightly, Console) but are small or minimally explained.

### Cited Findings
- **TLDR AI**: TLDR's advertiser page lists about 1.15M subscribers and a 47% open rate (nav menu says 1.1M); a search snippet from an earlier version of the page said about 1M and 44%. Audience: AI/ML engineers, researchers and technical leaders. — [TLDR advertise](https://advertise.tldr.tech/audiences/ai-engineers/)
- TLDR: a roundup says 1.25M+ and daily; TLDR charges up to $18,000 per placement. Counts conflict across sources. — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)
- TLDR describes itself as a collective of technical newsletters with over 5 million subscribers. — [TLDR sponsorships](https://sponsorships.tldr.tech/)
- **Ben's Bites**: sponsor pages claim 140k+ to 150k+ subscribers, sends Tuesday and Thursday, 37% open rate; a partner catalogue says 120,000+. Roundup says daily with hands-on tutorials and a directory. — [Ben's Bites ads](https://ads.bensbites.com/); [partners](https://catalog.bensbites.com/partners); [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)
- **The Rundown AI**: roundup gives conflicting sizes ("about 1 million" and "2M+"), daily, $25,000 to $40,000 per primary sponsorship slot. — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)
- **AlphaSignal**: roundup says 175K+, weekly. Its own Substack says 12,000+ subscribers and "200,000+ AI developers" as readers; its Hugging Face page says 25,000+ weekly readers. Figures conflict and are unverified. — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/); [AlphaSignal Substack](https://alphasignalai.substack.com); [Hugging Face](https://huggingface.co/organizations/AlphaSignal/activity/all)
- **The Batch** (DeepLearning.AI): 1.7M+, weekly (roundup). **Import AI**: 96K+, weekly, free (roundup). — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)
- General AI newsletter sponsor pricing: top-5 AI newsletters $30 to $80 CPM. — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)
- **Changelog Nightly**: sent every night at 10pm US Central; features "top new and top starred projects on GitHub before they blow up"; no stated grouping or rating; no official archive; open source; sponsorship "possible in the future". — [Changelog Nightly](https://changelog.com/nightly)
- A search snippet says Changelog Nightly sorts picks into first-time, newly open-sourced and repeat groups, and GitHub's Explore newsletter sends daily, weekly or monthly emails. Second-hand; verify. — [Changelog news item](https://changelog.com/news/8nk)
- **Console** (console.dev): weekly (Thursday; latest 5 November 2026), 30k+ subscribers, reviews 2 to 3 developer tools with "What we like" / "What we don't like", RSS and MCP available, sponsors labelled "[sponsor]". Method of choosing and testing not stated. — [Console](https://console.dev/)

### Inferences
- Console is the closest to an editorial, reasoned review (likes and dislikes), but it covers few tools and says nothing on skill level or security.
- Newsletter size claims vary by 2x to 10x between sources, so the report writer should quote ranges and label them self-reported.
- Newsletters are not ingestible sources for a platform (no APIs); they are competitors for attention and potential distribution partners.

### Gaps
- Latent Space and Last Week in AI: not covered by any source retrieved.
- GitHub's own Explore emails and Octoverse as a discovery email: only a second-hand snippet; no primary page read.
- Whether any of these newsletters rates difficulty: no evidence found in any source read (absence of evidence, not proof).
- Rundown AI and AlphaSignal own media kits: not read.

## 3. AI tool directories: repos or only products? Monetisation?

### Takeaway
Directories are mainly product-centric and monetise through paid listings, sponsorship and pay-per-click. There's An AI For That is the only one found indexing repositories (40,000+) and states human review of submissions. No directory shows tested or security-screened status.

### Cited Findings
- **There's An AI For That (TAAFT)**: 50,000+ AI tools, 40,000+ repositories, 140,000+ entities; 4.5M+ visits a month; free to browse; builders pay one-time launch fees, brands pay for sponsorship or pay-per-click, plus "data partnerships". "Staff review every submission before it goes live", 1 to 2 days; automated and manual checks retire dead tools. Whether repos come from GitHub is not stated. — [TAAFT about](https://theresanaiforthat.com/about/)
- **Futurepedia**: paid "Verified Enhanced Listing + 1,000 Clicks" ($497); page notes it may earn compensation from listings; separate $197 submission product on Gumroad. Tool counts vary by source (28,000+ versus 5,700+). — [Futurepedia enhanced](https://www.futurepedia.io/enhanced); [Gumroad](https://futurepedia.gumroad.com/l/submit-tool)
- **Toolify**: paid placements (one source: $99 permanent placement, border highlight, "verified" badge) and a sponsorship marketplace. Vendor-sourced. — [poweredbyai.app](https://poweredbyai.app/alternatives/toolify); [mybesh](https://mybesh.com/tool/toolify)
- **Product Hunt**: the v2 API docs say "By default the Product Hunt API must not be used for commercial purposes", with contact required for business use; asks for attribution; fair-use rate limits at its discretion. — [Product Hunt API docs](https://api.producthunt.com/v2/docs)
- **Ben's Bites** runs a catalogue/directory alongside the newsletter. — [Creative AI News](https://www.creativeainews.com/articles/ai-newsletter-landscape-2026/)

### Inferences
- "Verified" in Toolify and Futurepedia is tied to paid listings in the sources found, so it is not evidence of testing or security review.
- TAAFT's repository index shows repos can sit inside a product directory, but without level grouping or run evidence in the material read.

### Gaps
- AI Tool Report and other Product Hunt alternatives (beyond the vibe-coding ones in section 4): not researched.
- Futurepedia, Toolify and TAAFT own terms of use on scraping or re-use: not read.
- Product Hunt audience size: not retrieved.

## 4. Is there a 2025 to 2026 product describing itself as a gateway, toolbox or launchpad for vibe coders?

### Takeaway
Yes, several, but all small. The closest direct competitor is Vybe Guide (launched 30 January 2026): a free directory of 50,760 open source projects for vibe coders in 19 categories. It ranks on stars, forks and recency, with no skill levels, no run evidence and no security data in the sources read.

### Cited Findings
- **Vybe Guide** (vybeguide.ai): launched 30 January 2026 per press release; "50,000+" in headline and 50,760 in body; 19 categories; browse by language; trending, rankings and search; free, with accounts to save projects and get updates; "curated" claims; daily updates via "AI-powered analysis"; rankings track GitHub stars. The release mentions no skill levels, no security screening and no testing. — [press release (blog copy)](https://abnews-wire.blogspot.com/2026/01/vybe-guide-launches-as-definitive-open.html); [Barchart](https://www.barchart.com/story/news/37328832/vybe-guide-launches-as-the-definitive-open-source-discovery-platform-for-vibe-coders-and-ai-assisted-developers)
- Vybe Guide (independent article): ranking "emphasises stars, forks, and recency"; each entry shows stars, licence, documentation status and last commit date; does not show OSV advisories or OpenSSF scores; licence conflicts not flagged; no published API or data export; no published audit precision or recall; AI-generated similarity suggestions, saved collections synced to GitHub, daily digest emails. — [AICerts](https://www.aicerts.ai/news/?p=16460)
- Vybe Guide site pages could not be fetched directly (404 on `vybe.guide` and `vybeguide.ai` paths tried), so first-hand verification of the live site is missing. — see [AICerts](https://www.aicerts.ai/news/?p=16460) for third-party description
- **Vibe Coders' Kit** (Product Hunt): "Helping vibe coders organize their AI toolkit"; stores MCPs, prompts, agents, skills and tech stacks; launched 10 January 2026, relaunched 14 July 2026 with "one command to install anyone's Claude Code setup"; very low votes (single digits). — [Product Hunt](https://www.producthunt.com/products/vibe-coders-kit/launches)
- **Vibe Coding Tools Directory** (Product Hunt): "curated vibe-coding tools"; launched 2025; 8 points. GitHub repos not mentioned. — [Product Hunt](https://www.producthunt.com/products/vibe-coding-tools-directory)
- Other 2026 vibe-coding directories named in search results: Vibe Coding hub (launched 14 January 2026), vAppHunt ("producthunt for vApps", 10 January 2026), Vibe Coding Gallery (11 March 2026), VibeLaunch (curated directory for AI-built products), VibeKing (leaderboard of vibe-coded products), NNhub. These list products built by vibe coding, not repos for vibe coders. — [Vibe Coding (PH)](https://www.producthunt.com/products/vibe-coding-3/launches); [vAppHunt](https://www.producthunt.com/products/vapphunt/launches); [Vibe Coding Gallery](https://www.producthunt.com/products/vibe-coding-gallery/launches); [VibeLaunch](https://www.stork.ai/en/vibelaunch); [VibeKing](https://hunted.space/product/vibeking); [NNhub](https://hunted.space/product/nnhub)
- GitHub-hosted "awesome" lists are the de facto curated layer: filipecalegario/awesome-vibe-coding (3,851 stars at the time of the snippet), 0xWelt/Awesome-Vibe-Coding (sections for communities, projects, learning; a roundup labels its overview as beginner-suited), acvnace and ai-for-developers lists. — [KDnuggets](https://www.kdnuggets.com/10-github-repositories-to-master-vibe-coding); [Awesome-Vibe-Coding](https://github.com/0xWelt/Awesome-Vibe-Coding); [sourcepulse](https://www.sourcepulse.org/projects/2335337)
- Trendshift lists trending repos including awesome-vibe-coding and vibe-coding platforms (for example vibesdk); it is a trend tracker, not a vibe-coder gateway. — [Trendshift](https://trendshift.io/repositories/128454)

### Inferences
- No product found combines skill-level grouping, AI-topic grouping, run evidence and security screening for repos aimed at vibe coders. Vybe Guide has topic categories and daily digests but, per the sources, stars-based ranking and no security data.
- The vibe-coding Product Hunt entries have single-digit engagement, which suggests the niche is crowded with tiny projects and not yet owned by anyone.
- The gap in the market per these sources: trust signals (tested, security-scanned) and difficulty levels.

### Gaps
- First-hand view of Vybe Guide's live site, traffic and any level labels: not obtained.
- Whether other tools (for example awesome lists' websites, "Easy-Vibe", "vibe-coding-cn") offer level grouping: only star counts seen in snippets; not verified.
- Traffic or user numbers for any of the above: not found.

## 5. Terms of service and APIs: what can a new platform legally and technically ingest?

### Takeaway
Safest sources: GitHub REST/GraphQL API (metadata, rate-limited), Hacker News Firebase API (no stated rate limit), and daily.dev's public API for personal or own-token use. Product Hunt's API is non-commercial by default, Reddit is closing RSS (13 November 2026) and its public API (to March 2027), and HN's Terms ban scraping and commercial republishing. Treat legal conclusions as needing a lawyer's check.

### Cited Findings
- **GitHub REST API limits**: 60 requests/hour unauthenticated per IP; 5,000/hour with a personal access token or app acting for a user; search has tighter limits. — [GitHub rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
- **GitHub Terms of Service, API terms (section H)** (as summarised by the fetch tool): do not share tokens to exceed rate limits; abuse or excessive requests may lead to suspension; do not use the API to download data for spamming or to sell users' personal information. — [GitHub ToS](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)
- GitHub ToS (as summarised): "these Terms do not restrict lawful access to or use of the contents of public repositories"; making a repo public gives other users a licence to use, display and reproduce it by forking as GitHub's functions allow. The summary also described a section D.9 on automated access for commercial AI systems with a 700-million-user threshold; this looks unusual, so verify against the page before relying on it. — [GitHub ToS](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)
- GitHub Trending: no official API or export (vendor and developer sources agree); scraping its HTML is a separate legal question not answered by the sources. — [Apify scraper](https://apify.com/themineworks/github-trending-scraper)
- GitHub Acceptable Use Policies page: the URL tried returned 404; not read. — [attempted URL](https://docs.github.com/en/site-policy/github-terms/github-acceptable-use-policies)
- **Hacker News API**: Firebase base URL, no rate limit stated, MIT-licensed docs repo, only public users' items; no separate API terms on the page. — [HN API](https://github.com/HackerNews/API)
- **Y Combinator site terms** (as summarised): prohibit "data mining, robots, scraping or similar data gathering or extraction methods", prohibit commercial use or republishing of Site content unless authorised, and grant YC a broad licence over user content. The summary did not mention the API. — [YC legal](https://www.ycombinator.com/legal/)
- **Reddit**: Reddit announced on 30 September 2026 (per secondary reports) that RSS ends 13 November 2026 ("no replacement" outside moderation); new public API access requests stopped 31 October 2026; access removed for unregistered apps from 12 January 2027; public access closes for all remaining apps in March 2027; Devvit developer platform replaces it. — [TechWyse (1 October 2026)](https://www.techwyse.com/news/social-media/reddit-rss-feeds-ending-public-api-shutdown-2027); [Pillitteri](https://pasqualepillitteri.it/en/news/19942/reddit-shuts-down-rss-feeds-ai-scraping)
- Reddit Data API Terms (last revised 20 July 2026 per a vendor page) require a separate agreement for commercial use. Vendor source only. — [Postiz](https://postiz.com/blog/reddit-api-limits-rules-and-posting-restrictions-explained)
- Reddit's original posts are cited by TechWyse as r/modnews `1wubgvt` and r/redditdev `1wubcvf`; Reddit domains could not be fetched here, so these are unverified first-hand. — [TechWyse](https://www.techwyse.com/news/social-media/reddit-rss-feeds-ending-public-api-shutdown-2027)
- **Product Hunt API v2**: "By default the Product Hunt API must not be used for commercial purposes"; contact hello@producthunt.com for business use; attribution requested; read-only by default; discretionary rate limits. — [Product Hunt API docs](https://api.producthunt.com/v2/docs)
- **daily.dev**: Public API is governed by its Terms of Service "Public API section"; the summarised terms say "personal and own-token integrations are permitted" and that competing products and other restricted uses are covered in that section, whose text was not retrieved. — [daily.dev ToS](https://daily.dev/tos/); [daily.dev API docs](https://docs.daily.dev/docs/plus/public-api)
- **DEV/Forem**: copyright notice 2026 Forem, Inc.; licensing section and rate limits not visible in the page read. — [Forem API](https://developers.forem.com/api/)
- **Newsletter and directory content**: Console offers RSS and MCP; TAAFT, Futurepedia and Toolify terms not read. — [Console](https://console.dev/)

### Inferences
- Rank by ease and safety for a startup: (1) GitHub API for repo metadata (stars, licence, last commit) with a token; (2) HN Firebase API for mentions, keeping to links and titles and not republishing commentary (Terms ban commercial republishing of site content); (3) daily.dev API only for personal-scale use; (4) Product Hunt only with written permission; (5) Reddit, effectively unavailable after March 2027 without a commercial deal.
- Show metadata and links back (facts, not bulk text) and add original editorial value; this lowers copyright and terms risk, but is not legal advice.
- A trend feature built on GitHub data should compute its own velocity from the API rather than scrape github.com/trending.

### Gaps
- Exact current text of daily.dev ToS "Public API" section: only the navigation summary was read.
- HN Algolia API terms and limits: not retrieved.
- Reddit Data API Terms and Reddit's own announcement: Reddit domains blocked for the fetch tool; only secondary sources.
- GitHub AUP (scraping clause) and robots.txt for github.com/trending: not read.
- Hashnode, Peerlist, DEV terms on republishing: not found.
- No legal review; this is a reading of public pages only.

## 6. Scorecard against the five gateway dimensions (derived from the findings above)

### Takeaway
No source found meets more than two of the five dimensions. Topic grouping and some editorial curation exist; skill-level grouping, evidence of running, and security screening were not found anywhere in the material read.

### Cited Findings
- **Skill-level grouping**: not found for daily.dev, HN, Reddit, Peerlist, Changelog Nightly, Console, TAAFT, Vybe Guide. One roundup labels a GitHub awesome list's overview as suited to beginners (a label by a third party, not a feature). — [KDnuggets](https://www.kdnuggets.com/10-github-repositories-to-master-vibe-coding); [Vybe Guide release](https://abnews-wire.blogspot.com/2026/01/vybe-guide-launches-as-definitive-open.html)
- **AI topic grouping**: daily.dev tag filters, Vybe Guide's 19 categories, TAAFT categories (inferred from its index), Hashnode tag feeds. — [daily.dev docs](https://docs.daily.dev/docs/plus/public-api); [Vybe Guide release](https://abnews-wire.blogspot.com/2026/01/vybe-guide-launches-as-definitive-open.html); [Apify Hashnode page](https://apify.com/automation-lab/hashnode-scraper)
- **Editorial versus metrics**: metrics-led: daily.dev, HN, Reddit, Peerlist (composite score), Vybe Guide (stars, forks, recency), GitHub Trending. Editorial: Console (written pros and cons), Changelog Nightly (unexplained picks), TAAFT (staff review of submissions), the big newsletters (human-edited). — [Peerlist](https://help.peerlist.io/individual/launchpad/guidelines-faqs); [AICerts](https://www.aicerts.ai/news/?p=16460); [Console](https://console.dev/); [TAAFT](https://theresanaiforthat.com/about/)
- **Evidence it was run or tested**: only HN's Show HN rule (project must be something people can run, early and rough accepted). Console reviews "reflect Console's assessment at publication" with no test method stated. — [Show HN](https://news.ycombinator.com/showhn.html); [Console](https://console.dev/)
- **Security screening**: Vybe Guide does not display OSV advisories or OpenSSF scores; no other source mentions it. — [AICerts](https://www.aicerts.ai/news/?p=16460)

### Inferences
- The unoccupied space is the combination: level labels plus run evidence plus security data over a topic grouped AI-repo index.
- Vybe Guide is the closest competitor and the one most worth a first-hand review before design decisions.
- "Verified" badges in directories are paid features in the sources found, so a platform claiming tested status should show its method.

### Gaps
- Direct inspection of live sites (Vybe Guide, TAAFT, Futurepedia, Toolify, Console) for level labels or badges: not done beyond page summaries.
- A full competitor scan beyond these sources (for example other open-source discovery tools) belongs to adjacent researchers.
