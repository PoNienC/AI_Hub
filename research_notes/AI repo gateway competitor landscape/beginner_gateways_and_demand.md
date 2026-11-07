# Beginner-oriented and skill-levelled gateways to AI development, and evidence of demand for level-graded repo grouping (as of 7 November 2026)

Method note: pages were read only (no sign-ups). WebFetch summaries are produced by a small model, so figures shown on live pages (stars, counts) are as reported at fetch time (early November 2026) and will drift. Reddit could not be fetched directly (blocked), so Reddit evidence is thin and second-hand. Anything older than 2026 is dated in the text.

## 1. Which learning gateways grade by level, how do they define levels, and do they link to runnable repos?

### Takeaway
Level grading is common but loosely defined: most gateways use two or three labels (Beginner / Intermediate / Advanced) with no published criteria, and several big "for Beginners" brands do not grade internally at all. Only a few point to runnable code, and when they do it is via Codespaces/devcontainer, Binder or a bundled notebook, not via a curated "runnable repo" list. One new repo (datawhalechina/easy-vibe) grades by stage explicitly, and a December 2025 KDnuggets list is the nearest thing to a level-graded vibe-coding repo list.

### Cited Findings
**roadmap.sh**
- The AI Engineer roadmap page shows no beginner/intermediate/advanced labels on the roadmap itself. It reports about 371K GitHub stars, 3.2M+ registered users, about 52K Discord members and "hundreds of thousands of developers every month" — [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)
- Its projects page has three level filters (beginner / intermediate / advanced) but states no criteria; the one project visible when fetched ("OpenAI API in Python", labelled intermediate) links to an internal page, not to a GitHub repo — [roadmap.sh/ai-engineer/projects](https://roadmap.sh/ai-engineer/projects)
- A separate roadmap.sh "Vibe Coding" roadmap exists ("Step-by-step guide to master Vibe Coding in 2026"); no levels or vibe-coding-specific repo shown in the fetched content — [roadmap.sh/vibe-coding](https://roadmap.sh/vibe-coding)
- Third-party pages describe a 3-level reading of the AI engineer roadmap (Level 1 core concepts/prompting; Level 2 data layer/RAG; Level 3 agents/MCP/multimodal). These are unofficial and other guides use five levels — [thealanwang.github.io](https://thealanwang.github.io/alan-brain-site/02-Tech/06-AI/AI_learning_path)

**Microsoft repositories**
- generative-ai-for-beginners: about 123k stars; 21 lessons; no difficulty levels, instead lessons are labelled "Learn" (concept) or "Build" (concept plus code); Python and TypeScript samples for Azure OpenAI/OpenAI; a `.devcontainer` folder is present but Codespaces is not promoted in the README as seen — [GitHub](https://github.com/microsoft/generative-ai-for-beginners)
- ai-agents-for-beginners: about 79k stars, 18 lessons, 13 with short videos; "Azure Account Required" for Microsoft Foundry; some samples support OpenAI-compatible providers; `.env.example` and `.devcontainer` present; no level definitions — [GitHub](https://github.com/microsoft/ai-agents-for-beginners)
- AI-For-Beginners: about 70.6k stars; "12 Weeks, 24 Lessons"; sections I–IX are topic sections not difficulty levels; Binder badge and a Codespaces guide; `environment.yml`/`requirements.txt`; no stated prerequisites — [GitHub](https://github.com/microsoft/AI-For-Beginners)

**Course platforms**
- DeepLearning.AI short courses: filter shows 65 Beginner and 69 Intermediate courses; no Advanced label; 108 short courses; the page defines neither level and shows no learner counts or repo links — [deeplearning.ai/short-courses](https://www.deeplearning.ai/short-courses/)
- fast.ai Practical Deep Learning: no formal level; prerequisite is "some coding experience" (about a year, Python preferred) plus high-school maths; every chapter is a Jupyter notebook; GitHub link to fastai/course22; recommends Kaggle Notebooks or Paperspace and warns against local training unless you are experienced — [course.fast.ai](https://course.fast.ai/)
- Hugging Face Learn: 12 courses (LLM, Agents, Diffusion, Audio, Open-Source AI Cookbook, etc.); no level or prerequisite labels in the listing — [huggingface.co/learn](https://huggingface.co/learn)
- Anthropic Academy (Skilljar): about 23 offerings seen (22 courses plus 1 path); only "Advanced" appears in a title (MCP: Advanced Topics) and "introductory" in one description; no formal level tags seen — [anthropic.skilljar.com](https://anthropic.skilljar.com/). Third-party guides disagree on counts (13, 17, 21) and on whether Claude Code in Action needs coding experience — [secondary guide, treat with caution](https://dev.to/amareswer/anthropic-academy-free-claude-courses-and-certificates-22ki)
- Google Cloud Skills Boost: has introductory/intermediate/advanced tags in its catalogue and a "Gen AI Leader" path marked introductory; I could not confirm the current official definitions from a Google page — [Google Cloud blog (older)](https://cloud.google.com/blog/topics/training-certifications/new-generative-ai-trainings-from-google-cloud)
- Scrimba AI Engineer Path: no beginner/intermediate/advanced tiers; positioned for intermediate and advanced web developers, pointing beginners to its Frontend path or free JavaScript course; about 13.4 hours, Pro subscription — [Scrimba path page](https://m.scrimba.com/learn/aiengineer), [directory listing](https://www.techinterview.org/bootcamp_directory/p/scrimba-ai-engineer-path/)
- Codecademy: third-party listings tag Intro to Generative AI as Beginner (under an hour, no prerequisites); I did not reach an official level-definition page — [Careervira listing (third party)](https://www.careervira.com/course/intro-to-generative-ai)
- freeCodeCamp news page gave no curriculum levels or AI-curriculum detail in the fetched content — [freecodecamp.org/news](https://www.freecodecamp.org/news/)
- Kaggle Learn: page fetch returned only the title, so levels and learner counts were not verified — [kaggle.com/learn](https://www.kaggle.com/learn)

**Explicit level-graded vibe-coding material**
- datawhalechina/easy-vibe (about 20.4k stars): three stages — Stage 1 "Beginner Entry" (ideas, prototypes, AI features), Stage 2 "Junior and Mid-Level Developers" (frontend, backend, deployment, billing), Stage 3 "Advanced Developers" (Claude Code, MCP, Skills, agents, RAG) plus an appendix; local run steps `npm install` / `npm run dev`; an `examples` folder; does not appear to link a separate runnable repo per tutorial — [GitHub](https://github.com/datawhalechina/easy-vibe)
- KDnuggets, 3 December 2025, "10 GitHub Repositories to Master Vibe Coding": a list that does NOT label levels itself, but its "best for" cues map roughly to beginner (Awesome Vibe Coding), intermediate (Context Engineering Template, Rulebook AI, Claude Code Settings) and advanced (AI Coding Style Guide, Vibe Check MCP, Vibe Kanban); it gives few setup caveats (e.g. LiteLLM proxy; Docker sandbox for VibeKit). The level labels are an inference by the page reader, not the article — [KDnuggets](https://www.kdnuggets.com/10-github-repositories-to-master-vibe-coding)
- Another blog roundup sorts vibe-coding repos into beginner / intermediate / advanced-power-user tiers and says to "inspect before running" one of them — [secondary blog, via search summary](https://medium.com/write-a-catalyst/4-github-repos-every-vibe-coder-should-know-but-most-dont-64312aa29279)

### Inferences
- "Level" is almost always a self-declared label without criteria. A scheme that defines levels by measurable run-requirements (needs API key? needs Docker? needs GPU? needs a cloud account?) would be new relative to these gateways.
- No gateway found links beginners to a curated set of independent, runnable third-party repos. Microsoft's repos are self-contained courses; roadmap.sh projects pages point inward.
- Microsoft's three "for Beginners" repos (about 270k stars combined) show very large demand for beginner-framed AI repos, but they grade by topic and by "Learn/Build", not by skill level.

### Gaps
- Official Google Cloud level definitions, Codecademy official level pages, Kaggle Learn levels, freeCodeCamp AI curriculum and Hugging Face course prerequisites were not verified from primary pages (fetch returned titles only or third-party material).
- Usage figures (completions, enrolments) for DeepLearning.AI, Anthropic Academy, Scrimba and Kaggle were not found. Only roadmap.sh and GitHub star counts are available.
- roadmap.sh's AI Engineer roadmap node structure (and whether it has any level tagging) was not visible in the fetched text.

## 2. Open-source onboarding tools: what do they teach about grading tasks by difficulty?

### Takeaway
None of the main onboarding tools grade by difficulty on a defined scale. They use a single binary "easy / good first issue" signal plus eligibility rules (self-contained, small, well described). The maintainers' own labels are inconsistent. This is a gap a level-graded scheme could fill.

### Cited Findings
- first-contributions: about 56.7k stars and 112.3k forks; teaches one workflow (fork, clone, branch, edit, pull request) with GUI-tool tutorials; no difficulty grading — [GitHub](https://github.com/firstcontributions/first-contributions)
- Good First Issue (goodfirstissue.dev): "curates easy pickings from popular open-source projects"; shows issue counts, star counts and last activity; language filters; no difficulty levels or criteria stated — [goodfirstissue.dev](https://goodfirstissue.dev/)
- Up For Grabs: maintainers label suitable issues (suggested label "up-for-grabs"); criteria are tasks needing "no more than a few evenings", self-contained, and clearly described; no grading — [up-for-grabs.net](https://up-for-grabs.net/)
- CodeTriage: emails one open issue per day from repos you choose; "100,516 developers" on "10,678 open source repos"; no difficulty grading described — [codetriage.com](https://www.codetriage.com/)
- EddieHub support repo: stresses that open source is not only code; first PR practice, Discord first-timer channels; work sorted by type (Issues vs Discussions), not difficulty; about 343 stars on that repo — [GitHub](https://github.com/EddieHubCommunity/support)
- awesome-for-beginners: about 91.1k stars; about 250 entries across roughly 40 language sections (approximate, estimated by the fetch); labels are project-specific ("good first issue", "first-timers-only", "Level:Starter", "easy") with no shared scale — [GitHub](https://github.com/MunGell/awesome-for-beginners)
- GitHub itself: the "good first issue" label is used so people can find approachable issues; GitHub says an algorithm identifies the "most approachable issues" in each repo and surfaces them in various places — [GitHub Docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels)
- Octoverse 2025: 255,000 first-time open-source contributors in March 2025 (largest month on record); nearly 20% of the most popular projects among first-time contributors were AI-focused; only about 5.5% of repos have contributor guides; the report attributes first-contributions' continued popularity to newcomers wanting low-friction practice — [GitHub Blog, 28 October 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

### Inferences
- The onboarding ecosystem teaches "small, self-contained, well described" as the working definition of beginner-suitable, which can be reused as a criterion for "beginner-ready repo", but it grades issues, not whole repos for running.
- First-time contributors are heading to AI repos in large numbers (Octoverse), so the audience for a level-graded AI repo guide overlaps with these tools' audience.

### Gaps
- No evidence of how well Good First Issue or Up For Grabs perform (conversion from issue to merged PR). CodeTriage's 100k developers is the only usage count found.
- Hacktoberfest and "Level:" label conventions were not examined beyond the awesome-for-beginners mention.

## 3. What do vibe coders complain about when they try trending repos (Reddit, Hacker News, Discord, X)?

### Takeaway
I found no direct, well-evidenced Reddit/HN/Discord/X threads of vibe coders reporting failed trending-repo setups; Reddit was blocked and HN search returned nothing relevant. The closest evidence is (a) a general r/webdev thread on hours lost getting repos to run, (b) a May 2026 preprint showing less-experienced vibe coders are confused when code breaks, and (c) strong 2026 security evidence that fake "trending-looking" AI repos are being used to target AI-tool users. Treat the complaint evidence as a gap, not as proof of demand.

### Cited Findings
- r/webdev post "Anyone else tired of spending hours just getting a repo to run locally?" (posted roughly late February or early March 2025 per the snapshot's "308 days before 2 January 2026"; 77 comments; score 0). Poster: setup "2–6 hours gone before writing a single line of code" and "Docs are almost always wrong or incomplete". Replies: top comment (73 points) said cloning top repos and following the README is a standard first job task; others said Docker Compose or pinned versions already solve most of it; one said the problem is "Very language/runtime specific" with frequent issues in Python, rare in Node; several suspected the post was AI-generated marketing. This is a general developer thread, NOT specific to vibe coders, and the snapshot captured only 10 of 77 comments — [Reddit snapshot mirror](https://reddit.sentinel-team.org/posts/1q1wqsd/snapshots/2026-01-02T18%3A51%3A13.524069Z)
- Preprint (23 May 2026, Massey University and University of Auckland; 162 analysed Prolific respondents, 54 per group): all groups report vibe-coded output that "looks correct but fails when run"; less experienced participants relied more on re-prompting than debugging and reported more confusion when code broke; non-developers were the only group to report never checking AI code (about 45% of professionals always checked) — [arXiv:2605.24521](https://arxiv.org/html/2605.24521)
- Haskell Discourse, 11 April 2026: a maintainer asked how to filter vibe-coded packages out of dependencies because Hackage has no label and most READMEs do not disclose AI use; replies suggested detecting `CLAUDE.md`/`GEMINI.md` files; one said "vibe coded" signals "poor quality" to them. Shows trust concerns about vibe-coded repos from the maintainer side, not beginners' setup pain — [Haskell Discourse](https://discourse.haskell.org/t/how-to-filter-out-vibe-coded-dependencies/13918)
- Security, FakeGit / AgentBaiting (reported 21 July 2026; Island research): about 7,600 malicious GitHub repos tied to about 6,600 accounts; 800+ posing as AI Skills or MCP servers; over 14 million downloads from release assets across about 200 repos (may include bots); a clone of a 67,000-star project had only 63 stars and 18 forks yet looked established; Claude Code, Gemini and ChatGPT were each shown recommending or passing on install steps from malicious repos in Island's tests; payload SmartLoader then StealC infostealer (credentials, sessions, cloud API keys). Peak April 2026 — [Help Net Security](https://www.helpnetsecurity.com/2026/07/21/github-repos-malware-campaign-fakegit-ai-agents/); also [Cloud Security Alliance note](https://labs.cloudsecurityalliance.org/research/csa-research-note-fakegit-agentbaiting-mcp-supply-chain-2026/). Download totals described as possibly inflated by bot traffic by [Hexnode](https://www.hexnode.com/blogs/?p=47851) (seen via search summary, not fetched)
- Secret/key handling: a deployment checklist says AI tools sometimes hard-code secret API keys in route files — [13labs.au](https://www.13labs.au/guides/deploy-vibe-coded-app-checklist). A readme-ai GitHub discussion is a typical "invalid_api_key" setup failure — [GitHub discussion](https://github.com/eli64s/readme-ai/discussions/17). Both are anecdotal single items.
- Security quality of AI code (secondary roll-up, original sources named in it): 45% of AI code samples failed security benchmarks (Veracode); AI pull requests had 1.7x more issues (CodeRabbit); only 48% of developers always review AI code (Sonar) — [Hostinger roll-up](https://www.hostinger.com/blog/?p=8895); I did not open the original reports
- Hacker News search (Algolia, "vibe coding" plus "git clone") found no thread about setup failure; one sarcastic comment (ares623, 23 January 2026) — [HN item 46727400](https://news.ycombinator.com/item?id=46727400)
- Typical install failures for non-experts installing AI tools: npm EACCES permission errors, Node version below 18, WSL using Windows npm — [Anthropic support article](https://support.claude.com/en/articles/14552646-troubleshoot-claude-code-installation-and-authentication) (seen via search summary)

### Inferences
- The most solid, citable "what goes wrong" points are: repo setup is slow and docs are often wrong (general developers), less-experienced vibe coders cannot diagnose breakage (preprint), and fake or clone repos exploit star-count trust (FakeGit). Together these support a "trust and runnability" angle rather than only a "difficulty" angle.
- The FakeGit finding implies a trending list needs provenance checks (star-to-age ratio, original vs clone), and that AI assistants may not protect beginners.

### Gaps
- No direct quotes or counts from r/vibecoding, r/ClaudeAI, r/cursor, r/lovable, Discord or X: Reddit and X cannot be fetched with the available tools, and web search surfaced no matching threads. A manual Reddit search (or an API export) is needed.
- No count of how often "won't run" or "API key" appears in vibe-coder forums.
- Whether vibe coders (as opposed to developers) clone trending repos at all is unproven; Lovable/Replit/Bolt users mostly work in-browser (see section 4).

## 4. Surveys and reports on the size and skill profile of the vibe-coding population (2025–2026)

### Takeaway
The population is large but poorly measured. Best-sourced figures: Stack Overflow 2025 (professional developers mostly reject vibe coding), Lovable's June 2026 report (about 80% self-identified non-technical builders on its own platform), Vercel's 63% non-developer claim (unsourced), and one small academic survey (162 respondents). Most "vibe coders" use browser-based builders, not cloned repos.

### Cited Findings
- Stack Overflow Developer Survey 2025: 26,564 answered the vibe-coding question ("is 'vibe coding' part of your professional development work?"): 72.2% No, 5.3% emphatically no, 11.9% Yes, 0.4% emphatically yes, 2.8% somewhat, 2.1% "tried it". Overall AI use: 47.1% daily; 84% use or plan to use AI tools (76% prior year) — [Stack Overflow 2025 AI section](https://survey.stackoverflow.co/2025/ai)
- Lovable "A first look at the Build Economy" (9 June 2026): about 80% of builders self-identify in non-technical roles; fastest-growing groups are founders, designers and salespeople; survey respondent count not stated on the page; average 720 million monthly visits to Lovable projects. Vendor data, not independently audited — [Lovable blog](https://lovable.dev/en/blog/a-first-look-at-the-build-economy); secondary coverage gives survey size as 14,300+ and 66% from outside tech, unverified — [secondary coverage](https://ccstartup.com/blog/2026/06/09/500m-arr-146-staff-80-non-technical-builders/)
- Vercel blog: "About 63% of users exploring vibe tools are non-developers"; "Vibe coders only need English, a basic understanding of how technology works, and an idea." The figure has no named source on the page beyond Vercel's own State of Vibe Coding report — [Vercel](https://vercel.com/blog/what-you-need-to-know-about-vibe-coding). Secondary sources attribute the 63% differently — [Product Hunt discussion](https://www.producthunt.com/p/vibecoding/the-state-of-vibe-coding-2025-key-takeaways)
- Academic survey (Prolific, May 2026): groups were non-developers, novices, professionals; non-developers motivated by accessibility, novices by learning and experimentation. Adoption duration and independent coding hours, not group label, explained QA behaviour — [arXiv:2605.24521](https://arxiv.org/html/2605.24521)
- GitHub Octoverse 2025 (28 October 2025): 180M+ developers; 36M+ new in the year; nearly 80% of new developers use Copilot in their first week; 4.3M+ AI-related repos (nearly doubled in under two years); 1.1M+ public repos import an LLM SDK (+178% YoY) — [GitHub Blog](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Platform scale claims (company-reported, secondary): Lovable 25M+ projects created (TechCrunch, via Hostinger roll-up); OpenAI Codex 4M+ weekly developers (April 2026); Claude Code 115,000 active developers (July 2025) — [Hostinger roll-up](https://www.hostinger.com/blog/?p=8895). Another summary cites Lovable 8M registered users and Replit 50M users, unverified — [webhosting.today](https://webhosting.today/2026/06/10/lovable-bolt-and-replit-are-generating-millions-of-projects-every-week-traditional-hosting-is-not-where-they-land/)
- Learners trust AI accuracy more than professionals (49% vs 42%) per Stack Overflow 2025, as quoted by the Hostinger roll-up — [Hostinger roll-up](https://www.hostinger.com/blog/?p=8895)
- Search interest: no first-hand Google Trends data could be obtained. Secondary pages report "vibe coding platform" queries up about 2,400% YoY with a May 2026 spike (tool not stated) and one tracker calls the topic "Declining" (-17.7% over 28 days). These conflict and are unverified — [vibecoding.app](https://vibecoding.app/blog/state-of-vibe-coding-2026), [Graph8](https://graph8.com/trends/vibe-coding)

### Inferences
- The addressable group "vibe coders who might clone a repo" is a subset: Stack Overflow shows few professionals vibe-code, and Lovable-type users stay inside the platform. The likelier audience is novices and tinkerers using Claude Code, Cursor, Codex and similar tools locally.
- First-time contributors and new GitHub accounts (Octoverse) are the best evidence that many new, low-experience users arrive at GitHub each year.

### Gaps
- Original Vercel State of Vibe Coding report, a16z primary data, JetBrains State of Developer Ecosystem and Replit usage breakdowns were not retrieved. A search for a16z surfaced only a video summary with no data.
- No source separates "vibe coders who use GitHub repos" from those who only use hosted builders.
- Google Trends could not be accessed.

## 5. Has anyone published a scheme for rating a repository's "ease to run"?

### Takeaway
There is no widely adopted ease-to-run score for general repositories. The nearest established schemes are the ACM artifact badges (Available / Functional / Reusable / Results Reproduced) used in research, and informal launch badges (Open in Codespaces / Dev Container, Binder, Colab). None rate beginner difficulty.

### Cited Findings
- ACM-derived artifact badges: "Functional" means documented, complete, consistent and runnable; "Reusable" means Functional plus well packaged and documented for reuse; "Available" means archived in a public repository without evaluation; "Results Reproduced/Replicated" flag independent confirmation of results. Venues apply them differently — [PLDI 2026 artifacts call](https://pldi26.sigplan.org/track/pldi-2026-pldi-research-artifacts) (seen via search summary across SPLASH, CGO and PLDI pages). The ACM policy page itself returned HTTP 403 so was not read directly.
- Launch badges: a guide describes a clickable badge that opens a repo in a dev container to skip reading setup instructions — [gsdms.csir.co.za](https://gsdms.csir.co.za/news/launch-devcontainers-with-custom-badges); Microsoft AI-For-Beginners uses a Binder badge, `.devcontainer` and a Codespaces guide — [GitHub](https://github.com/microsoft/AI-For-Beginners)
- Dev container first-build is slow but later starts are fast, which is a usable proxy for "time to first run" but not a score — [Medium](https://medium.com/cwan-engineering/reproducible-local-development-with-dev-containers-0ed5fa850b36), [VU Amsterdam](https://ase.vu.nl/docs/framework/glossary/devcontainer)
- Hosted-IDE access: roadmap.sh notes Replit runs in any browser with no local setup, and Lovable is browser-only — [roadmap.sh best tools](https://roadmap.sh/vibe-coding/best-tools) (seen via search summary)
- Related quality signal: Octoverse says only about 5.5% of repos have contributor guides — [GitHub Blog](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Searches for "ease of setup" or "time to first run" scores returned no published rubric — searches run 7 November 2026; closest results [CSIR dev container guide](https://gsdms.csir.co.za/news/launch-devcontainers-with-custom-badges)

### Inferences
- A rubric based on observable signals (devcontainer present, `.env.example`, Docker Compose, pinned versions, one-click deploy badge, Colab or Binder badge, install in under N minutes in a clean container, required paid services) would be a new, defensible design, loosely modelled on ACM Functional/Reusable.
- Ease-to-run could be tested automatically (build in a clean container, record time and failures), which none of the gateways above do.

### Gaps
- Replit "Run on Replit" templates, "Deploy to Vercel/Heroku/Render" button usage, Colab badge statistics and OpenSSF-style scorecards for setup ease were not researched.
- ACM policy text not read from the primary page (HTTP 403).
- Academic work on repository executability or reproducibility of GitHub repos (for example studies of Jupyter notebook reproducibility) was not searched.
