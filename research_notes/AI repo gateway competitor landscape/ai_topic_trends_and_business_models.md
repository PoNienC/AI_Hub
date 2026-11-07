# AI open-source topic trends (2025–2026) and developer-discovery business models

Position as of 7 November 2026. Items older than 2026 are marked "(2025)" or with an explicit year. Evidence quality varies: GitHub Octoverse, Stack Overflow and Star History are primary or near-primary; many directory-revenue figures are self-reported or third-party estimates and are flagged. Several numbers come from vendor or aggregator pages and are labelled as such. Where I only saw a search-result summary and did not open the page, I say so.

## 1. Which AI categories grew fastest on GitHub in 2025 and 2026?

### Takeaway
The fastest growth sits in (a) coding agents and agent "harnesses" (Claude Code, Codex, OpenCode, Cline, OpenClaw, Hermes), (b) local and server inference engines (vLLM, SGLang, llama.cpp, Ollama), (c) MCP servers and agent skills or config packs, and (d) workflow/agent builders (n8n, Dify, RAGFlow). Octoverse 2025 (data to August 2025) and Octoverse 2026 (data to September 2026) both put AI infrastructure and agent tooling at the top, but GitHub publishes ranked lists, not per-category growth percentages, so the category ranking below is my synthesis.

### Cited Findings
- Octoverse 2025: AI-related repositories exceeded 4.3 million; 1.13M+ public repos import an LLM SDK, with 693k+ created in the last 12 months (+178% YoY, Aug 2025 vs Aug 2024) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2025: six of the 10 fastest-growing open-source repos by contributors were AI infrastructure, with growth between 2,301% and 6,836%. The ten were zen-browser/desktop, cline/cline, vllm-project/vllm, astral-sh/uv, microsoft/vscode, infiniflow/ragflow, sgl-project/sglang, continuedev/continue, comfyanonymous/ComfyUI, home-assistant/core (per-project percentages appear only in a chart image) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2025: six of the top 10 projects by total contributors were AI-centric (vllm #1, openai/codex #3, transformers #4, ollama #7, llama.cpp #8, volcengine/verl #9), averaging +150% contributor growth; aider also named as fast-growing — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2025: MCP reached 37k stars in eight months; modelcontextprotocol/servers is in the top 10 by contributors — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2025: popular first-time-contributor projects included bolt.new (spelled "slackblitz/bolt.new" in the source), vllm, ComfyUI and ollama; nearly 20% of top first-timer projects were AI — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2025: Shell was the fastest-rising language in AI repos (+324%); TypeScript AI repos +77.9%; Python 582,196 AI repos (+50.7%) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2026 (published 28 October 2026, 12 months to 30 September): agents started more than 40% of PRs in September 2026, up from 17% in March; 110 million agent-started PRs in September. GitHub calls this a floor and it is vendor-reported — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/); also reported by [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/10/29/github-octoverse-agents-started-more-than-40-percent-of-september-pull-requests.aspx) (my fetch of that page returned HTTP 403; I saw only a search summary)
- Octoverse 2026: fastest-growing community repos by contributors were farion1231/cc-switch, punkpeye/awesome-mcp-servers, omacom/omarchy, firstcontributions/first-contributions, ggml-org/llama.cpp, open-vsx.org, sglang, vllm, helium, vllm-ascend. Fastest single-vendor repos: anthropics/claude-code, openai/codex, anomalyco/opencode, vscode, github/copilot-cli, zed, google-gemini/gemini-cli, BerriAI/litellm, winget-pkgs, Kilo-Org/kilocode — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- Octoverse 2026: most-engaged community repos: openclaw, vllm, llama.cpp, omarchy, cc-switch, sglang. Most-engaged vendor repos: hermes-agent, opencode, earendil-works/pi, stablyai/orca, pingdotgg/t3code, graphify, paperclip, litellm, oh-my-pi — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- Octoverse 2026: repos created in 2026 with an agent configuration file logged 8x as many commits as those without; interoperability / reverse-engineering repos rose from ~30,000 (2025) to 130,000+ (2026) — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- Simon Willison on Octoverse 2026: about 220 million merged PRs/month (roughly triple), ~7.38 billion commits/month, ~30.3 million new repos/month (doubling); attributes it to agentic engineering. His post gives no AI-topic breakdown — [Simon Willison](https://simonwillison.net/2026/Oct/28/github-octoverse-2026/)
- MCP ecosystem 2025: 11,415 MCP servers registered in 2025 (quality-filtered, author's own count); about 31M weekly npm downloads across MCP servers and devtools; top packages @playwright/mcp (951k weekly), context7-mcp (397k); Google Trends interest for MCP peaked around August 2025 and had declined by early December 2025 — [Glama, State of MCP in 2025](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- MCP ecosystem 2026: one secondary source puts the whole ecosystem at about 15,930 servers across registries in May 2026 (not independently verified) — [signalcensus](https://signalcensus.pages.dev/articles/mcp-server-marketplace-economics-2026) (low-quality aggregator, treat with caution)
- A16z Top 100 Gen AI consumer apps, 6th edition (9 March 2026): web ranking by SimilarWeb visits and mobile by Sensor Tower MAU as of January 2026; a secondary summary says only three image generators remain in the top 100 as video, music and voice tools take places (unverified against the a16z text) — [a16z](https://a16z.com/100-gen-ai-apps-6/); summary at [The Neuron](https://www.theneuron.ai/explainer-articles/a16z-just-ranked-the-100-most-popular-ai-apps-heres-the-full-list-and-what-it-tells-us-/)
- A March 2026 analysis of about 100 GitHub Trending projects (Feb–Mar 2026) grouped them into ten categories (personal AI agents, coding agents, security automation, local LLM inference, workflow builders, RAG/search, MCP ecosystem, system-prompt collections, token optimisation, browser automation) but gave no per-category counts — [DEV Community](https://dev.to/ji_ai/what-100-trending-github-projects-tell-us-about-where-ai-is-actually-going-4977) (single author, low weight)
- Trendshift 2025 monthly snapshots show AI-agent leaders by month (for example Dify in February 2025; OpenManus 10.3% and browser-use 4.1% share of the agent category in March 2025). These are shares of trending activity, not star gains — [Trendshift March 2025](https://trendshift.io/insights/fragmentation/2025/3), [February 2025](https://trendshift.io/insights/fragmentation/2025/2)
- OSS Insight's AI trending page (categories: AI agents, LLM tools, MCP servers, coding agents, RAG, inference, vector DB, vibe coding, AI assistants; 28-day growth) returned no repository data when I fetched it, and it states GitHub's public events feed has been incomplete since 1 March 2026, so its growth figures are lower bounds — [OSS Insight](https://ossinsight.io/trending/ai)
- Octoverse 2025 lists ComfyUI as the only image-generation repo among its fastest growers; I found no Octoverse table for voice/realtime, evals/observability or fine-tuning — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

### Inferences
- Ranking by growth (my synthesis from Octoverse lists, Star History and Glama): 1) coding agents and agent harnesses; 2) personal / autonomous agents (OpenClaw, Hermes); 3) agent skills, rules and config packs; 4) MCP servers and registries; 5) LLM inference engines (vLLM, SGLang, llama.cpp); 6) local-model runners (Ollama, Open WebUI); 7) workflow and agent builders (n8n, Dify, RAGFlow); 8) AI app builders / vibe coding (bolt.new and similar); 9) browser automation and computer use (browser-use, Playwright MCP, OpenManus); 10) RAG and knowledge/memory tools; 11) image/video generation tooling (ComfyUI); 12) LLM gateways and observability (LiteLLM).
- Voice/realtime, evals/observability and fine-tuning show no headline growth in the sources I could read. That is absence of evidence, not evidence of absence.
- MCP interest as a search term appears to have peaked in 2025 even as the server count kept rising; agent skills and config packs look like the 2026 successor.

### Gaps
- No per-category star-growth table from OSS Insight (page empty on fetch; events feed incomplete since March 2026).
- No Sequoia report was read; a16z content is only via secondary summaries.
- I read only part of the Octoverse 2026 official page (via extraction); it gave no AI-topic or LLM-SDK counts in what I saw.

## 2. Which AI repositories gained the most stars in 2025 and 2026, and what categories?

### Takeaway
2026 produced record star velocity: OpenClaw passed 200,000 stars in 88 days and reached about 388,577 by 2 September 2026; DeepSeek Harness reportedly hit 200,000 in 15 days. Most top gainers are coding-agent harnesses, agent skills/config packs and personal agents, not classic ML libraries. Stars measure attention, not usage (several of these repos are config collections).

### Cited Findings
200K+ table (as of 2 September 2026) — [Star History: DeepSeek Harness blog](https://www.star-history.com/blog/deepseek-harness-beats-openclaw-fastest-200k-stars):
- openclaw/openclaw — personal AI agent; created 24 Nov 2025; 200K on 19 Feb 2026 (88 days); 388,577 stars at 2 Sep 2026.
- deepseek-ai/deepseek-harness — agent / coding harness; created 13 Aug 2026; 200K on 27 Aug 2026 (15 days); 208,834 at 2 Sep 2026. Single-source claim; the Star History post itself says OpenClaw's record stood for six months; I found no independent confirmation.
- NousResearch/hermes-agent — personal / autonomous agent; created 22 Jul 2025; 200K on 24 Jun 2026 (338 days); 239,699 at 2 Sep 2026.
- anomalyco/opencode — open-source coding agent; created 30 Apr 2025; 200K on 22 Aug 2026 (480 days); 203,145 at 2 Sep 2026.
- n8n-io/n8n — workflow automation with AI agents; created 2019; 200K on 13 Aug 2026; 203,097 at 2 Sep 2026 (older repo, included for its AI-agent pivot).

Star Race page (last updated 4 September 2026; stars and creation month as shown; the page gives no categories) — [Star History star race](https://www.star-history.com/star-race):
- ultraworkers/claw-code — Mar 2026 — ~195k (name suggests a Claude Code clone; category unverified)
- affaan-m/ECC (Everything Claude Code) — Jan 2026 — ~248k on the Star Race page; the repo README claims 182K+ and a skills-site page lists about 252,817, so counts conflict across snapshots. Category: agent harness performance / skills and config pack — [ECC repo](https://github.com/affaan-m/ECC)
- garrytan/gstack — Mar 2026 — ~131k (category not verified)
- DietrichGebert/ponytail — Jun 2026 — ~124k (category not verified)
- Graphify-Labs/graphify — Apr 2026 — ~115k (knowledge-graph / RAG-style tool inferred; also in Octoverse 2026 most-engaged vendor list)
- VoltAgent/awesome-design-md — Mar 2026 — ~114k (curated list / design rules for coding agents, inferred from name)
- JuliusBrussee/caveman — Apr 2026 — ~103k (category not verified)
- karpathy/autoresearch — Mar 2026 — ~95k (autonomous research agent, inferred from name)
- nexu-io/open-design — Apr 2026 — ~94k
- odysseus-dev/odysseus — May 2026 — ~87k
- paperclipai/paperclip — Mar 2026 — ~80k
- career-ops-hq/career-ops — Apr 2026 — ~70k
- MemPalace/mempalace — Apr 2026 — ~59k (agent memory, inferred)
- FoundationAgents/OpenManus — Mar 2025 — ~58k (general agent; 10K stars in 2 days) (2025)
- karpathy/nanochat — Oct 2025 — ~58k (small LLM training, inferred) (2025)
- deepseek-ai/DeepSeek-R1 — Jan 2025 — ~92k (model repo) (2025)
- Significant-Gravitas/AutoGPT — Mar 2023 — ~187k (older, still large)
- nomic-ai/gpt4all — Mar 2023 — ~77k (local inference; older)

Category labels marked "inferred" or "unverified" come from repo names only.

Other counts:
- Ollama passed 162k stars, Dify ~130k and n8n 150k+ in early March 2026 — [DEV Community, 6 March 2026](https://dev.to/ji_ai/what-100-trending-github-projects-tell-us-about-where-ai-is-actually-going-4977); OSS Insight later showed Dify ~153,218 and n8n ~201,007 (undated) — [OSS Insight compare](https://ossinsight.io/compare/langgenius/dify/n8n-io/n8n)
- OpenClaw reportedly overtook React at 250,829 stars on 3 March 2026 — [DEV Community](https://dev.to/derivinate/openclaw-just-became-githubs-most-starred-project-heres-why-2ii0) (secondary, low weight; I saw only a search summary)
- Hermes Agent: one secondary source gave about 160k around May 2026 — [dev.to comparison](https://dev.to/rosgluk/openclaw-vs-hermes-agent-stars-downloads-usage-2026-b07); consistent with Star History's later 239,699
- n8n gained 112,000+ stars in 2025 and topped Socket's JavaScript Rising Stars for 2025 — [Socket via Plushcap](https://www.plushcap.com/content/socket/blog/socket-n8n-tops-2025-javascript-rising-stars-as-workflow-platforms-gain-momentum) (2025)
- MCP specification repo: 37k stars in eight months (2025) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- punkpeye/awesome-mcp-servers is the second-fastest community repo by contributors in Octoverse 2026, so an awesome list can be a top-growth repo — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- Star History excludes skills, curricula and awesome-style aggregators from its 200K list — [Star History blog](https://www.star-history.com/blog/deepseek-harness-beats-openclaw-fastest-200k-stars)

### Inferences
- That is about 25 named AI repos with approximate counts and dates. Coding-agent harnesses and skill packs dominate 2026; personal agents are the biggest single phenomenon; classic frameworks (LangChain and similar) do not appear in the 2026 fast-growth lists I saw.
- Star velocity can be inflated by hype and cross-promotion; a discovery platform should show several signals (commits, releases, contributors), not stars alone.

### Gaps
- No clean, independent 2025 calendar-year "stars gained" ranking for AI repos was found (no Star History year-in-review; OSS Insight page empty).
- Star Race gives no categories, so several labels are inferred.
- Counts for some repos (ECC) conflict between snapshots; all are approximate.

## 3. What are beginners asking about most?

### Takeaway
Beginner demand clusters around using AI to write code ("vibe coding", Claude Code, Cursor, Lovable, Bolt), running models locally (Ollama), and building simple agents/RAG. Stack Overflow 2025 shows very high AI adoption among learners, and Ollama is the most-used agent orchestration tool in that survey. I found no clean Reddit or YouTube volume data.

### Cited Findings
- Stack Overflow 2025: 84% use or plan to use AI tools (76% in 2024); daily use 47.1% of all respondents — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Learners: 39.5% of those learning to code use AI daily, 18.7% weekly; 47.4% partly and 33.1% mostly use AI to learn new concepts — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Trust is low: more distrust output accuracy (46%) than trust it (33%); 3.1% highly trust — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Agents: 14.1% use agents daily at work, 9% weekly; 37.9% have no plans; 69% of agent users report higher productivity — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Agent orchestration tools used: Ollama 51.1%, LangChain 32.9%, LangGraph 16.2%, Vertex AI 15.1%, AutoGen 12%, CrewAI 7.5%. Data storage: Redis 42.9%, GitHub MCP Server 42.8%, Supabase 20.9%, ChromaDB 19.7%, pgvector 17.9%. Observability: Grafana+Prometheus 43%, Sentry 31.8%, LangSmith 12.5% — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Out-of-the-box agents: ChatGPT 81.7%, GitHub Copilot 67.9%, Gemini 47.4%, Claude Code 40.8% — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Technology section: Ollama used by 15.3% of all respondents (14.4% of people learning to code), RAG 10.6%, LangGraph 3%; GPT models 81.4%, Claude Sonnet 42.8%, Gemini Flash 35.3%, Llama 17.8%; Cursor 17.9%, Claude Code 9.7% — [Stack Overflow 2025 technology](https://survey.stackoverflow.co/2025/technology)
- Vibe coding: 72.2% say they do not do it, 15.1% do or somewhat do — [Stack Overflow 2025 AI](https://survey.stackoverflow.co/2025/ai)
- Search volume: about 110,000 US monthly searches for "vibe coding" in mid-2026, down from a peak near 165,000 in March 2026; "vibe coding platform" grew about 2,400% YoY. The source is a tool directory (commercial interest) using Google Keyword Planner via DataForSEO — [vibecoding.app](https://vibecoding.app/blog/state-of-vibe-coding-2026)
- Search behaviour is learning-oriented ("how to use vibe coding", plus Claude Code, Lovable and Bolt queries) — [Dataconomy](https://dataconomy.com/?p=90740) (secondary; search summary only)
- Conflicting signal: Graph8 reports a 17.7% drop in "active market interest" over 28 days, method unclear — [Graph8](https://graph8.com/trends/vibe-coding)
- MCP: Google Trends interest peaked around August 2025 and fell by December 2025; r/mcp had 80k members and 7.3M visitors in 2025 — [Glama](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- First-time contributors favour vscode, bolt.new, vllm, ComfyUI and ollama (2025) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

### Inferences
- Draft shortlist of 12 topics a new platform could target, ordered by a blend of growth and beginner demand (my judgement, not a published ranking):
  1. Coding agents (Claude Code, Codex, OpenCode, Cline, Gemini CLI) — highest growth, high learner demand
  2. Agent skills, rules and config packs — very high 2026 star growth; cursor.directory shows demand
  3. MCP servers — largest registry volume; search interest cooling, so curation and quality signals are the gap
  4. Local LLM runners (Ollama, llama.cpp, Open WebUI) — most-used orchestration tool in SO 2025; beginner friendly
  5. AI app builders / vibe coding (bolt.new and similar) — strong learner search interest
  6. Workflow and agent builders (n8n, Dify) — large stars, low-code beginner entry
  7. Personal and autonomous agents (OpenClaw, Hermes, OpenManus)
  8. RAG and knowledge/memory tools (RAGFlow, vector stores) — RAG 10.6% in SO
  9. Browser automation and computer use (browser-use, Playwright MCP)
  10. Inference serving (vLLM, SGLang) — top growth but less beginner-oriented
  11. Image and video generation tooling (ComfyUI) — beginner demand likely, growth evidence thin
  12. LLM gateways, evals and observability (LiteLLM, LangSmith-style) — LiteLLM is fast-growing in Octoverse 2026, but audience is advanced
  Optional 13–15: voice/realtime, fine-tuning, agent frameworks (LangGraph, CrewAI) — evidence of growth is weaker in what I read.
- Stack Overflow respondents are developers, not true beginners, so beginner demand is under-measured.

### Gaps
- No Google Trends export, Reddit post-volume data or YouTube tutorial counts were found.
- Stack Overflow 2025 admiration/desire figures for LangChain, Hugging Face and others could not be read (page truncated).

## 4. How do developer directories and curated lists make money, and which died?

### Takeaway
Revenue is mostly sponsorship and advertising to developers (newsletters, in-feed ads), plus job boards and paid or featured listings. Pure directories without an owned audience earn little; the money flows to those with distribution (TLDR, daily.dev, Product Hunt). Failure is common among AI tools themselves, which is a freshness risk for any directory.

### Cited Findings
- TLDR (own advertising page, November 2026): 14 newsletters; TLDR Tech 1.6M subscribers (47% open rate), TLDR AI about 1.1–1.15M (47%), TLDR Dev 470k; 8M+ weekly readers claimed; 22% VP-level or above; each issue has up to 3 advertisers in Primary, Secondary and Quick Links slots; no public prices — [TLDR advertise](https://advertise.tldr.tech/)
- TLDR pricing is unpublished by TLDR; a 2023 write-up reported $15,000 top, $10,000 programming and $5,000 quick-link slots and an unverified $5M annual revenue estimate; a 2026 report says up to $18,000 per placement. All third-party — [Reletter TLDR](https://reletter.com/publications/tldr), [Beehiiv deep dive](https://thenewsletternewsletter.beehiiv.com/p/tldr-deep-dive)
- daily.dev: ad-funded; listed by EthicalAds as a publisher; its own pricing comparison lists $2,000–$10,000 per month for in-feed ads; uses Carbon, EthicalAds and an in-house ad system; about $11M raised (seed March 2023 per aggregators). Revenue estimates conflict wildly ($1M to $43M, all third-party); no confirmed figure — [EthicalAds publisher page](https://www.ethicalads.io/publishers/dailydev/), [StartupHub](https://www.startuphub.ai/startups/daily-dev), [daily.dev ads comparison](https://daily.dev/blog/developer-marketing-platforms-comparison-channel-mix/). I could not fetch the EthicalAds page (redirect); facts come from a search summary.
- Product Hunt: acquired by AngelList (reported about $20M); five sponsorship products (promoted listings, email, topic ads, newsletter, job postings); advertising the majority of revenue, with about $2.9M projected from ads and about $0.4M from Ship and Founder Club subscriptions. Figures come from a secondary summary and appear to date to around 2020 — [Four Week MBA](https://fourweekmba.com/how-does-product-hunt-make-money/), [AngelList acquisition](https://www.streetinsider.com/Insiders+Blog/AngelList+Acquires+Startup+Company+Product+Hunt/12301802.html). Ryan Hoover's own post on first revenue returned 404 — [Ryan Hoover](https://ryanhoover.me/post/how-we-made-our-first-dollar-at-product-hunt)
- Best of JS: a solo project by Michael Rambeau (Osaka); the only funding route stated is GitHub Sponsors; no ads or revenue figures — [Best of JS about](https://bestofjs.org/about)
- cursor.directory: Starter Story podcast reports about $34–35K per month and 99.8% margin (self-reported); paid job listings are described as a core revenue source and MCP developers reportedly pay to be featured (stormy.ai, unverified); G2 says 250,000+ visits per month — [Starter Story summary](https://rosetta.to/u/starterstory/my-website-makes-35k-month-built-in-3-hours?t=0), [stormy.ai](https://stormy.ai/blog/how-to-build-monetize-profitable-web-directory-2025), [G2](https://www.g2.com/products/cursor-directory/discuss). No primary disclosure found.
- There's An AI For That: Romanian-run catalogue; 54,102 tools shown on 7 October 2026; claims 5M+ monthly visitors and 2.5M+ newsletter subscribers (third-party directory, unverified); a $49 one-time paid listing per third-party pages. TAAFT's own revenue is not published — [Nick Launches](https://nicklaunches.com/resources/ai-directories/theres-an-ai-for-that)
- A small AI-tools directory listed for sale on Flippa reported $1.5K–$2.6K per month, giving a sense of the low end — [Flippa listing](https://flippa.com/13392265-profitable-ai-tools-directory-generating-1-5k-2-6k-month-with-dr-71-3k-organic-visitors-multiple-revenue-streams-and-huge-growth-potential)
- Smithery (MCP registry plus hosting): described as freemium with hosted servers and a router; no funding amount confirmed; third-party pages disagree on size (about 6,000 servers claimed) — [Respan Smithery profile](https://www.respan.ai/market-map/compare/orthogonal-vs-smithery), [stork.ai](https://stork.ai/en/smithery)
- MCP monetisation: remote MCP API providers (Bright Data, Exa, Tavily) charge per request; Glama said it was developing revenue-sharing for authors; at least $73M raised by MCP-ecosystem startups (the article's own table sums to about $86M); of 81 MCP-related companies tracked, at least half had gone dead or pivoted by December 2025 — [Glama](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
- One post estimates only 3–6% of MCP servers carry any monetisation, with no cited source — [DEV Community](https://dev.to/t49qnsx7qtkpanks/15000-mcp-servers-97m-monthly-downloads-and-almost-no-one-getting-paid-4g7b) (weak)
- AI tool mortality (ToolDirectory.AI, updated 7 November 2026; self-published by a directory): 2,862 tools tracked, 395 retired (13.8%, including acquisitions), 167 hard shutdowns (about 5.8%), 228 acquisitions. Retirements by year: 2023: 23, 2024: 63, 2025: 134, 2026: 156. Developer Tools had the most retirements (59). Among 248 with a known cause: shut down 40.7%, acquired and sunset 32.7%, domain lapsed 23.4%, abandoned 3.2% — [ToolDirectory.AI research](https://tooldirectory.ai/research/ai-tool-mortality)
- Named example: Phind (developer AI answer engine) shut down on 16 January 2026 with no sunset period; the same site's counts differ between snapshots (July 2026: 217 retired; September 2026: 146 shut down, 70 acquired-and-sunset, 90 acquired-and-shipping), so its numbers are unstable — [ToolDirectory.AI graveyard](https://tooldirectory.ai/ai-graveyard)
- OpenAI deprecated the Assistants API, with shutdown on 26 August 2026 (platform risk for tools built on it) — [ToolDirectory.AI graveyard](https://tooldirectory.ai/ai-graveyard)

### Inferences
- Revenue ladder for a new site (my synthesis): sponsored placement in a newsletter or feed > job board > featured or paid listings > affiliate > API/data licensing. Best of JS shows a sponsor-funded, solo-maintained, low-cost site can survive without real revenue.
- Roughly one in seven tracked AI tools has retired (per one directory's own count), so freshness checks and archived-repo flags are a differentiator.
- I found no verified example of API access as a directory revenue line.

### Gaps
- No primary revenue data for TAAFT, Futurepedia, cursor.directory, Smithery or Best of JS.
- daily.dev recruiting revenue not found; Product Hunt data is old.
- Hacker News and Indie Hackers threads on directory economics were not retrieved.
- The ToolDirectory.AI mortality data are self-published and not peer-reviewed. Smithery pricing not confirmed.

## 5. What is the life cycle of "awesome" lists?

### Takeaway
I found no peer-reviewed or large-scale measured study of awesome-list decay. The evidence is anecdotal: link rot around 14% in one informal check, frequent abandonment, and survivors that rely on automated link checks, contribution rules and age-based pruning.

### Cited Findings
- A GitHub user reported checking all URLs across awesome lists and estimating about 14% unavailable (informal) — [awesome-php issue 886](https://github.com/ziadoz/awesome-php/issues/886), [awesome issue 1810](https://www.Github.com/sindresorhus/awesome/issues/1810) (I saw only search summaries of these pages)
- awesome-mobx maintainer suggested removing items over two years old; tools and articles treated differently — [awesome-mobx issue 86](https://urls.greenkeeper.io/mobxjs/awesome-mobx/issues/86)
- A Fallout issue tracks awesome-dotnet-style lists by date of last merged PR, marking several as abandoned (most recent from 2023) — [Fallout issue 599](https://github.com/Fallout-build/Fallout/issues/599)
- Community comments: a Julia forum post says a single maintainer cannot manage a general-purpose list; a Zig forum post says only a few list items are still relevant and maintained — [Julia Discourse](https://discourse.julialang.org/t/update-awesome-julia-list/21038), [Ziggit](https://ziggit.dev/t/zig-projects-lists-awesome-lists-external-resource-collections/3337/3)
- The Go project deprecated its unmaintained project list and pointed to awesome-go as the maintained alternative — [Go wiki](https://go.googlesource.com/wiki/+/2a0fad1acf00ec8d85c1ab3a38977449fabd9766)
- An aggregator list (cuuupid/awesome-lists) was archived on 17 June 2023 — [awesome-lists](https://www.github.com/cuuupid/awesome-lists/blob/master/curated_lists.json) (search summary only)
- Ecosyste.ms indexes awesome lists with "Last updated" dates: on its first page, awesome-selfhosted was updated 6 November 2026 and awesome-windows on 13 April 2024; the top list, build-your-own-x, has 554,187 stars. The page gives no total count or stale share — [Ecosyste.ms Awesome](https://awesome.ecosyste.ms/)
- A DEV post describes building a self-regulating curation system for stale lists — [DEV Community](https://dev.to/jtorchia/stale-awesome-lists-how-i-built-a-self-regulating-curation-system-18lc) (not opened; low weight)
- punkpeye/awesome-mcp-servers is among the fastest-growing repos by contributors in Octoverse 2026, showing a topical awesome list can thrive in a hot area with many contributors — [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)

### Inferences
- Likely survival factors (my synthesis from anecdotes, not proven by data): several maintainers, automated link-checking in CI, strict contribution guidelines, and a hot topic that keeps contributors arriving.
- An opportunity: automated freshness signals (last commit, archived flag, release date) address the main failure mode.

### Gaps
- No quantified share of awesome lists that go stale, or time to staleness. Ecosyste.ms holds last-updated data for thousands of lists and could be analysed directly through its API.
- No academic paper found (Google Scholar and MSR proceedings were not searched directly).
- Several awesome-list items above come from search summaries; I did not open those pages.
