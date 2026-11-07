# Upgraded brief — AI repo gateway for vibe coders

Date: 07 November 2026 · Levers: altitude, depth, range · Pass: ambition_pass

## In short
- Goal beyond the goal: a non-expert builder goes from "I want to make X with AI" to a running, trusted starting point in one sitting, not a longer list of repos.
- Hard target: every listed repo carries topic, level and a "what you can build in an afternoon" line; level tags match a hand-labelled set at 85% or better; refresh every 6 hours with zero manual steps a week.
- Judge: ten real vibe coders doing task tests, a gold set of 100 hand-labelled repos, and a fresh reviewer for the code. Never the author.
- Decision needed: approve this brief (phase 0 is a competitor sweep and gap test, not a build), or keep the original request.

## Original request (verbatim)
> I wonder if there is anyone already doing this: I would like to create a platform which is a very handy one for vibe coding coders where we put all the trending AI repos, skills, high-star popular repos. GitHub might already do it, but we do our grouping, so beginners or developers at different levels could use it directly; our platform is a gateway, and for different topics. Is there already a developer social media doing this, or news trends we could follow immediately and put on the platform so it becomes a toolbox to recommend repos focused on AI? Or tell me popular topics we should target. Has Hugging Face already done this? Tell me what others haven't done and is worth doing. https://github.com/trending

## Kept as fixed
- Focus: AI repos, skills and tooling. Audience: vibe coders at different levels. Grouping by level and topic. A gateway, not a forum. GitHub Trending is one source. The competitor question must be answered before building.

## Altitude
- Goal beyond the goal: the user never reads twenty READMEs. The platform makes the choice for them and shows the first command to run. Success is return visits each week, not page views.
- Decisions this should force: 1 Curated top ten per topic vs full catalogue (for: trust and shareability; against: less coverage) · 2 One niche first (Claude Code skills, MCP servers, coding agents) vs all AI (for: a gap nobody owns, fast to test; against: smaller audience) · 3 Human-plus-model curation vs metrics only (for: stars are gameable; against: weekly editor time).
- Out of the loop: GitHub API token, a scheduled run (GitHub Actions cron), a Claude API classifier for topic and level, static hosting with a domain, a feedback form that feeds the gold set.

## Depth
- Best in the field, and what they do first: a developer-tools product researcher (the people behind OSS Insight, bestofjs, Wirecutter-style testing). They first use every existing tool for the same five tasks and write where each fails: GitHub Trending and Explore topics, Hugging Face trending, bestofjs, OSS Insight, star-history, trendshift, awesome-lists, Hacker News, daily.dev, Product Hunt, and the per-ecosystem registries (mcp.so, Smithery, Glama, skills marketplaces). Names are from memory; the sweep verifies them.
- Rawest source: GH Archive events (BigQuery public dataset) and the GitHub GraphQL API for stars, forks, releases and contributor counts over time; Hugging Face Hub API for downloads and likes; Hacker News Algolia API; PyPI and npm download counts. Not the trending page HTML, which has no history.
- Methods and tools: star velocity over 7 and 30 days with bot-star detection; sustained-vs-spike classification; README-based LLM tagging into topic and a three-step level ladder (beginner: one-click deploy, no API key; intermediate: local setup and env vars; advanced: fork and modify); each candidate actually run once before listing, earning a "works first try" badge; licence and supply-chain check for skills and MCP servers, which run with the user's credentials.
- Hard target (written as normal): a new user with a stated goal finds a runnable starter in under three minutes; level tags agree with the gold set at 85% or better; six-hourly refresh; zero manual steps a week.
- Judge (never the author): ten vibe coders recruited from Reddit or Discord doing the task test against GitHub Trending alone; the gold set; a Codex dual_dev audit of the pipeline code.
- Assumption to test adversarially: "grouping by level and topic is the gap." For twenty beginner goals, measure time-to-running-starter with existing tools first. If existing tools win, the product is the testing and security layer, not the grouping. Second assumption: stars predict "works first try". Test the correlation on 100 repos.

## Range
- The job in one sentence (verb, not noun): get a non-expert builder from an idea to a running, safe starting point in one sitting, with the reason to trust it.
- Crew and their actions: a competitor analyst runs the five-task test across every existing tool and logs failures; a newsletter editor picks ten per topic and cuts anything without a reason to care; a bootcamp instructor defines the level ladder and writes prerequisites per repo; a supply-chain auditor checks licence, maintenance and injection risk in skills and MCP servers before anything is listed; a community lead maps where vibe coders actually gather and what makes a list shareable.
- Red team and their actions: a sceptical senior developer argues this is another awesome-list that dies in three months and demands the automation proof; a forensic auditor checks that trending signals are not bought stars and that no listing points to malware.
- Borrowed field: consumer product testing (Wirecutter). Test, pick one, say why. A catalogue is what GitHub already is.

## Upgraded request (ready to run)
Phase 0, two days, no code beyond scripts: run the five-task test across the existing tools listed above and the per-ecosystem registries; write a one-page gap table (who covers what; where each fails a beginner); hand-label 100 repos for topic and level; test the two assumptions above from GH Archive data; recommend one niche to start with and the ten topics to target. Phase 1 only if phase 0 shows a gap: a static site refreshed six-hourly from GH Archive and the GitHub API, LLM-tagged, each listing run once and security-checked, judged by ten real users against GitHub Trending.

## Access or cost needed
- GitHub personal access token (free). BigQuery free tier for GH Archive (within the monthly free quota). Claude API for tagging (small, a few pounds a month at phase 0 scale). Two days of Po's time for phase 0 review and the hand-labelled set. A domain and hosting only at phase 1.
