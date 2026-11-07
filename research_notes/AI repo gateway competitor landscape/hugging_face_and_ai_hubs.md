# Hugging Face and other AI-specific hubs as discovery gateways (state as of 7 November 2026)

Method note: pages were read with a fetch tool that summarises pages, not raw HTML. Where a fetch result was thin or a page is JavaScript-rendered, this is marked. Nothing was installed. Anything dated before 2026 is marked as older.

## 1. What Hugging Face offers for finding AI repositories, tools and starters (Trending, Papers, Collections, Blog, Learn); does it cover GitHub repos and tooling; any skill-level grouping?

### Takeaway
Hugging Face is a very strong discovery surface for models, datasets, Spaces and papers, with trending sorts, a weekly human-picked Spaces list and a daily papers email. It does not index GitHub repositories as listings (GitHub appears only as a link on Papers pages), it has no skill-level grouping on any browse surface I checked, and its only "level" signal is in course prerequisites.

### Cited Findings
- Models page: the visible sort control showed "Trending"; filters are task (about 44+ options), library, licence, language, parameter size, "Apps" (e.g. vLLM, Ollama), inference providers and hardware; no difficulty or beginner filter appeared. The page does not explain what "Trending" means. (Fetch summary of the live page, 7 Nov 2026.) — [HF Models](https://huggingface.co/models)
- Spaces page: categories include Image Generation, Video Generation, Text Generation, Speech Synthesis, OCR, Chatbots and others; cards carry labels such as "Agents" and "MCP" and "Featured"; the page showed a "Spaces of the week" heading dated 2 Nov 2026; no skill-level or beginner label. — [HF Spaces](https://huggingface.co/spaces)
- Spaces of the Week is officially "a curated weekly selection of standout Spaces chosen by the Hugging Face team"; a star icon marks author-owned (official) demos on model, dataset and paper pages. — [Hub docs: Featured Spaces](https://huggingface.co/docs/hub/spaces-featured)
- A community-built Space archives every featured Space since October 2021, which shows the weekly list is a long-running habit. (Third-party summary via search snippet.) — [spaces-of-the-week Space](https://huggingface.co/spaces/hysts/spaces-of-the-week/tree/main)
- Trending Papers page ("curated by AK and the research community") has Daily, Weekly and Monthly tabs; each entry shows an upvote count, and many entries link to a GitHub repository with a star count (example seen: VibeVoice, 56.5k stars) and an arXiv page. No categories or beginner grouping. — [HF Trending Papers](https://huggingface.co/papers/trending) and [HF Papers](https://huggingface.co/papers)
- Papers page offers a daily email of trending papers via a Subscribe button that requires login. — [HF Papers](https://huggingface.co/papers)
- Collections page is "community collections": sorted by "Trending" under the heading "Collections trending this week"; each collection is made by a user or organisation and can hold models, datasets or Spaces; no review process, filters or skill-level grouping were described. — [HF Collections](https://huggingface.co/collections)
- Blog: topic tags include community, guide, open source, collab, research, NLP, Audio, CV, RL, ethics, Diffusion, Game Development, LeRobot, Inference Providers. Posts are split into a main feed (team and enterprise orgs) and "Community Articles" sorted by Trending; no beginner or start-here tag and no weekly digest seen. — [HF Blog](https://huggingface.co/blog)
- Learn lists 12 courses (LLM Course, Context Course on context engineering for code agents, Robotics/LeRobot, a smol course, Agents Course, Deep RL, Computer Vision, Audio, Open-Source AI Cookbook, ML for Games, Diffusion, ML for 3D). The listing page states no audience, prerequisite or level for any course. — [HF Learn](https://huggingface.co/learn)
- The Agents Course states prerequisites of basic Python and basic LLM knowledge, and does not label itself "beginner"; its intro uses "from beginner to expert" as a scope phrase. So skill signalling exists only inside individual course intros. — [Agents Course intro](https://huggingface.co/learn/agents-course/unit0/introduction)
- The Hub's own documented object types are models, datasets, Spaces, plus papers, collections and kernels in the API; there is no "GitHub repository" object type. — [Hub API docs / OpenAPI](https://huggingface.co/docs/hub/api) and [OpenAPI spec (markdown)](https://huggingface.co/.well-known/openapi.md)

### Inferences
- A "vibe coder" looking for a runnable starter would find Spaces (demos) and the Open-Source AI Cookbook, but no listing type that says "clone this GitHub repo and run it" with a level label. This is the clearest gap for the planned gateway on the skill-level and GitHub-repo dimensions.
- Hugging Face's only human-curated layers are Spaces of the Week and the Papers page (AK-curated plus upvotes); Collections and Community Articles are user-made and ranked by trending.
- The Papers page is the one place Hugging Face meaningfully bridges to GitHub repos, but only for research papers with code, and ranked by upvotes.

### Gaps
- I could not confirm whether any Hugging Face page uses a "beginner" label I missed (for example inside individual Spaces or Collections); only top-level browse pages were read.
- Fetch summaries did not show the full set of sort options on Models/Spaces pages (only the currently selected one), so "most likes / most downloads" sort options in the web UI are not verified here.

## 2. How does Hugging Face rank trending (likes, downloads, time window)? Is the data available by API?

### Takeaway
Trending is a Hub-computed "trendingScore" driven by recent activity, and Hugging Face does not publish the formula or window on the pages I could read. Several secondary sources say recent likes over about a week; treat that as unverified. The data is available by public API, with no key needed for public listings.

### Cited Findings
- The official OpenAPI spec lists `GET /api/trending` ("Get the trending repositories") with optional `type` and `limit` parameters (no descriptions) and a "Trending repos" response with no schema. The spec text read does not define how trending is calculated or its time window. — [OpenAPI spec (markdown)](https://huggingface.co/.well-known/openapi.md)
- The same spec shows `trendingScore` as an allowed sort field (example text: "downloads, likes, lastModified, trendingScore") with `direction` of 1 or -1, documented in the kernels listing. — [OpenAPI spec (markdown)](https://huggingface.co/.well-known/openapi.md)
- The `huggingface_hub` client lists `trendingScore` alongside `downloads` and `downloadsAllTime` as expandable properties on repo info. — [HfApi reference](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api)
- A Hugging Face staff-linked dataset card for a trending-repos snapshot says: "The trending repositories reflect the likes given by Hugging Face users in the last week", with a `recent_likes` field described as likes "lately (last week)". It does not give the weighting formula. — [severo/trending-repos README](https://huggingface.co/datasets/severo/trending-repos/blob/main/README.md)
- A DEV Community guide gives an example call `https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=100`, says no API key is needed, filters match Hub tags, limit is up to 100 per page, and pagination uses a Link header. This is a third-party source. — [DEV Community guide](https://dev.to/scrapemint/the-hugging-face-hub-is-a-free-json-api-rank-trending-ai-models-without-a-key-39cb)
- A third-party article (title: top trending model had 17,924 downloads while fifth place had 393,062) suggests trending does not track downloads. I could not open the article (HTTP 403), so only its headline, from search results, is evidence. — [Level Up Coding article](https://levelup.gitconnected.com/hugging-faces-top-trending-model-had-17-924-downloads-fifth-place-had-393-062-20a6a7299866)
- All API calls are subject to Hub-wide rate limits; the OpenAPI spec is the current reference, and webhooks exist for real-time repo updates. — [Hub API docs](https://huggingface.co/docs/hub/api)

### Inferences
- The score is probably a short-window, like-driven momentum measure (hence low-download items can top it), but this is inference from one dataset card and one headline, not a documented formula.
- A gateway could reuse the public API for "what is moving on Hugging Face" without scraping.

### Gaps
- No official definition of trendingScore (formula, window, bot/spam handling) was found.
- I did not read the `/api/models`, `/api/spaces`, `/api/datasets` and papers endpoint sections of the OpenAPI spec (the file is about 409k characters; I read roughly the first 200k, and the listing endpoints were not in what the fetch returned). Sort options per endpoint are therefore not verified.
- Whether Papers/Collections trending is exposed with the same sort parameter was not verified.

## 3. Papers with Code (status in 2026), Replicate, Ollama, LangChain Hub / LangSmith, OpenAI Cookbook, Vercel AI templates, Together / Fireworks, Kaggle, Civitai

### Takeaway
Papers with Code is gone (older event, July 2025) and its URL now redirects to Hugging Face Trending Papers. None of the other hubs groups by skill level; most are metric- or catalogue-driven (run counts, pulls, alphabetical lists). Replicate has the most "intent-based" layer ("I want to…" collections) and Kaggle Learn has the clearest levels, but only for courses. Security or licence screening is rare: only Civitai and Hugging Face document file scanning, and both say it is not a guarantee.

### Cited Findings

#### Papers with Code
- paperswithcode.com returns a 302 redirect to https://huggingface.co/papers/trending (checked 7 Nov 2026). — [paperswithcode.com](https://paperswithcode.com)
- The shutdown was around 24 to 25 July 2025 (older event): coverage says Papers with Code stopped operating and Hugging Face's Julien Chaumond announced Trending Papers the next day, with a Meta partnership mentioned. The sources are secondary; no formal Meta statement was found. — [hyper.ai](https://hyper.ai/en/news/42900); [Codesota](https://codesota.com/papers-with-code)
- Reported loss: Hugging Face's replacement is described as lacking Papers with Code's broad SOTA leaderboards and task coverage (Papers with Code tracked thousands of tasks versus about 40 on Hugging Face, per one report). — [hyper.ai](https://hyper.ai/en/news/42900); [Codesota](https://codesota.com/papers-with-code)

#### Replicate
- Explore page sections: "Latest" spotlight, blog posts, Popular models (with run counts), Featured models, Official models (described as "always on, maintained, and have predictable pricing"), an "I want to…" task layer (generate images, caption videos, transcribe speech, each linking to a collection), and Latest models feed. No start-here page; a "Not sure where to start?" line links to docs. Run counts are shown but not explained. No newsletter mentioned on the page. — [Replicate Explore](https://replicate.com/explore)

#### Ollama library
- Sort by Popular or Newest only; capability tags (tools, thinking, vision, audio, embedding, cloud); each card shows parameter sizes, pull count, tag count and last-updated date; no categories, featured picks or getting-started section. — [Ollama library](https://ollama.com/library)

#### LangChain Hub / LangSmith prompt hub
- Official docs describe prompts stored, versioned and tested in LangSmith; the concepts page I read does not mention a public hub, curation or verification. — [LangSmith prompt concepts](https://docs.langchain.com/langsmith/prompt-engineering-concepts)
- A community guide says public prompts are user-generated and unverified and should be reviewed before production use; a separate "Context Hub" for agent and skill contexts is listed in docs (per a search summary). Treat both as secondary. — [Markaicode guide](https://www.markaicode.com/langsmith-hub-prompt-templates/); [LangSmith docs index](https://docs.langchain.com/langsmith/prompt-engineering-concepts)
- This is a prompt-sharing hub, not a repository or starter-project catalogue.

#### OpenAI Cookbook
- The site redirects from cookbook.openai.com to https://developers.openai.com/cookbook (308). The page has two sections, Articles (about 11) and Examples (about 49), apparently alphabetical; no filters, tags, featured section, authors, dates or beginner layer visible; each entry has a Markdown version and there is a single-file Markdown export. — [OpenAI Cookbook](https://developers.openai.com/cookbook)
- The GitHub repo is MIT-licensed, examples are mostly Python and need an OpenAI API key; the README says nothing about testing examples. — [openai/openai-cookbook](https://github.com/openai/openai-cookbook)

#### Vercel AI templates
- Template pages have a faceted filter (Use Case, Framework, CSS, Database, CMS, Authentication, Experimentation); the "AI" use case returns starters such as the Next.js AI chatbot, a customer-reviews summary template, an OpenAI Slackbot, AI SDK examples with Flask and FastAPI. These are scraped fragments from several Vercel domains, so exact facet options in November 2026 may differ. — [Vercel templates (search snapshot)](https://vercel.com/templates?type=ai)
- The AI templates landing page as fetched on 7 Nov 2026 showed a flat list with one-line descriptions; one entry marked "Experimental preview"; the fetch summary showed no filters, difficulty levels or licence or security info. — [Vercel AI templates](https://vercel.com/templates/ai)
- Templates are deployable starters, which is the closest match among all hubs to a "starter project" gateway, but they are Vercel-ecosystem only.

#### Together AI and Fireworks
- Together model library: category tabs (Chat, Image, Vision, Video, Audio, Transcribe, Code, Embeddings, Rerank, Moderation), 200+ models, price per 1M tokens, deployment tags, capability tags, "new" and "Free" badges; no featured section, no per-model quickstart on the page. — [Together AI models](https://www.together.ai/models)
- Fireworks model library: types LLM, Router, Vision, Embeddings, Reranks; filters by provider and serving method; 332 models listed; cards show price and context length; no featured section or beginner layer seen. — [Fireworks models](https://fireworks.ai/models)
- Both are commercial inference catalogues organised by price and capability, not by learner level.

#### Kaggle
- Kaggle's own Models, Notebooks and Learn pages were JavaScript-rendered and returned only page titles, so their structure is not verified from primary sources. — [Kaggle Models](https://www.kaggle.com/models); [Kaggle Learn](https://www.kaggle.com/learn)
- Secondary sources describe Kaggle Learn as free, short, browser-notebook micro-courses with beginner entry points (Python, Intro to Machine Learning, Pandas, SQL) followed by intermediate ones. — [KDnuggets](https://www.kdnuggets.com/7-free-kaggle-micro-courses-for-data-science-beginners)
- The Google and Kaggle 5-day Gen AI Intensive began as a live course in November 2024 (older) and was then published as self-paced; Google reports more than 140,000 developers took it; a later 5-day AI Agents Intensive is reported. Sources disagree on its level (beginner-friendly versus intermediate). — [Google blog](https://blog.google/technology/developers/google-kaggle-genai-intensive/); [Google recap](https://blog.google/innovation-and-ai/technology/developers-tools/google-kaggle-genai-intensive-recap-2025/); [GDG listing](https://gdg.community.dev/events/details/google-gdg-on-campus-oduduwa-university-ipetumodu-nigeria-presents-5-days-of-gen-ai)

#### Civitai
- The civitai.com/models page returned HTTP 403 to the fetch tool, so its browse layout (sort, period filters, categories) is not verified from the page. — [Civitai models](https://civitai.com/models)
- Civitai runs two file scans: ClamAV and picklescan (for dangerous pickle imports); a maintainer reply says safetensors need only the virus scan. He does not state that "verified" means safe, and users reported a case where a checkpoint flagged unsafe on Hugging Face showed as verified on Civitai. — [Civitai discussion 161](https://github.com/orgs/civitai/discussions/161)
- A third-party guide says the platform does not guarantee content is free of viruses or harmful components. — [Hakky security guide](https://book.st-hakky.com/en/security/thorough-explanation-of-civitai-risks-precautions-for-safe-use)

#### Hugging Face security screening (for the dimension 5 comparison)
- Every repo file under 2 GB is run through ClamAV at each commit; a warning shows if a file is flagged unsafe. — [Hub docs: Malware scanning](https://huggingface.co/docs/hub/security-malware)
- Pickle import scanning shows the imports inside pickled files on the Hub; the docs state it "is not 100% foolproof" and that safe/unsafe lists are best-effort. — [Hub docs: Pickle scanning](https://huggingface.co/docs/hub/security-pickle)
- The Security overview also lists secrets scanning and third-party scanners (Protect AI, JFrog). — [Hub docs: Security](https://huggingface.co/docs/hub/security)
- Scanning is aimed at files in Hub repos (weights and files), not at judging whether a project is safe to run end to end. This is my reading of the docs; they do not say it in these words.
- Licence: the Models page has a licence filter. — [HF Models](https://huggingface.co/models)

### Inferences
- Scoring the five dimensions from what I verified (Y = clearly present, P = partial, N = none seen, ? = not verified):

| Hub | 1 Skill level | 2 AI topic | 3 Editorial vs metrics | 4 Evidence of run/test | 5 Security/licence |
|---|---|---|---|---|---|
| HF Models/Datasets/Spaces | N | Y (task filters, categories) | Mostly metrics; Spaces of the Week and Featured are editorial | P (Spaces are live and show Running status; not a test record) | Y for files (ClamAV, pickle); licence filter |
| HF Papers | N | N | Mixed (curated plus upvotes) | N | N |
| HF Collections | N | P (user-made themes) | Community-made | N | N |
| HF Learn | P (prerequisites inside courses) | Y (by course topic) | Editorial | P (notebooks) | N |
| Replicate | N | Y ("I want to…") | Mixed (Official, Featured, run counts) | P (run counts show usage) | N |
| Ollama library | N | P (capability tags) | Metrics (Popular/Newest) | N | N |
| LangSmith prompt hub | N | ? | Community, unverified | N | N |
| OpenAI Cookbook | N | P (articles vs examples) | Editorial (vendor) | N | Licence only (MIT repo) |
| Vercel AI templates | N | Y (use case filter) | Vendor/community | P (deploy button implies runs; not verified) | N seen |
| Together / Fireworks | N | Y (categories) | Metrics/price | N | N |
| Kaggle | Y for Learn courses (secondary sources) | P | Mixed | Y (runnable notebooks) | ? |
| Civitai | ? | P | Metrics (not verified) | N | P (ClamAV and picklescan) |

- No hub in this set combines skill level, topic grouping, and run-evidence for GitHub repositories. This is the white space for the planned gateway.
- Security screening is aimed at model files, not at repos or starters; a gateway that screens repo code, dependencies and licences would be differentiated.

### Gaps
- Kaggle and Civitai primary pages were not readable by the fetch tool; their sort options, categories and level labels are from secondary sources or unverified.
- Vercel facet options come from search snippets across several Vercel domains, not one clean page read.
- LangChain's public Hub page itself (smith.langchain.com/hub) was not read; only docs and third-party guides.
- Together/Fireworks/Replicate pages were read once; I did not check their docs for any quickstart or tutorial hubs.
- Licence screening: I found no hub other than Hugging Face (licence filter) that exposes a licence filter on the pages I read; this is absence in what I read, not proof.

## 4. Has any hub launched a "for beginners" or "start here" layer for AI tooling in 2025 to 2026?

### Takeaway
I found no clear launch of a dedicated beginner or start-here layer for AI tooling by any of the hubs studied. The nearest items are courses (Hugging Face Learn, Kaggle's intensives) and general AI-tool directories launched in early 2026.

### Cited Findings
- Hugging Face Learn includes a Context Course on context engineering for code agents and an Open-Source AI Cookbook; neither is labelled beginner on the listing page. (Dates of launch not verified.) — [HF Learn](https://huggingface.co/learn)
- Kaggle and Google's 5-day Gen AI Intensive (November 2024, older) and a later AI Agents Intensive are course-style on-ramps, not browse layers for tooling. — [Google blog](https://blog.google/technology/developers/google-kaggle-genai-intensive/)
- Replicate's Explore page has only a "Not sure where to start?" link to docs. — [Replicate Explore](https://replicate.com/explore)
- Newly launched general AI-tool directories in 2026 include OpenResources (reported as 280 tools in nine categories, press release dated 12 February 2026), AI Directory (reported as launched 27 January 2026) and IndieAI Directory (reported as 10 February 2026). These come from press release or aggregator pages and are third-party, not the hubs studied. — [OpenResources press release](https://www.newsfilecorp.com/release/283413); [Product Hunt: AI Directory](https://www.producthunt.com/products/ai-directory-4/launches); [Claude Market directory roundup](https://claudemarket.ai/blog/best-ai-tool-directories-2026)
- A search for Hugging Face vibe-coding or app-builder beginner layers returned nothing relevant. — [search results used: Retool vibe coding report](https://retool.com/reports)

### Inferences
- The beginner layer for AI tooling (as opposed to learning courses) appears unclaimed among the major hubs, as of what I could find. Competition is more likely to come from general AI tool directories and vibe-coding tool rankings than from model hubs.

### Gaps
- The search tool is US-only and shallow; Hacker News threads, Product Hunt launches, and GitHub "awesome" lists were not systematically checked, so smaller beginner-oriented repo hubs could exist.
- I did not verify launch dates of HF Learn courses.

## 5. Which of these publish a "what's new this week" digest, and how?

### Takeaway
Only Hugging Face shows a weekly human-curated item (Spaces of the Week) and an official daily papers email. Most other hubs expose "Latest/Newest" lists rather than a digest. I found no official Hugging Face weekly email newsletter.

### Cited Findings
- Hugging Face: Spaces of the Week (weekly, team-chosen, on the Spaces page and in Hub docs). — [Hub docs: Featured Spaces](https://huggingface.co/docs/hub/spaces-featured)
- Hugging Face: daily trending papers email, subscribe requires login. — [HF Papers](https://huggingface.co/papers)
- Hugging Face: a community-built GitHub Action newsletter bot for daily papers exists, and a search found no official "Hugging Face Weekly" email. — [search result: Hub spaces-featured and community posts](https://huggingface.co/posts/mvaloatto/100154753019152)
- Hugging Face Collections page is framed as "Collections trending this week" (a weekly-window sort, not a digest). — [HF Collections](https://huggingface.co/collections)
- Replicate Explore has a "Latest" spotlight, blog posts and a Latest models feed; no newsletter mentioned on the page. — [Replicate Explore](https://replicate.com/explore)
- Ollama: Newest sort and last-updated dates on cards; no digest on the page (the blog was not read). — [Ollama library](https://ollama.com/library)
- Together: "new" badges and announcement banners above the library; no digest on the page. — [Together AI models](https://www.together.ai/models)
- Fireworks: "New" badge on cards; no digest seen. — [Fireworks models](https://fireworks.ai/models)
- OpenAI Cookbook: no dates or "latest" ordering visible on the index page. — [OpenAI Cookbook](https://developers.openai.com/cookbook)

### Inferences
- A weekly digest of "what is new and worth trying" for AI repos and tools is not a standard feature of these hubs; only Hugging Face's Spaces of the Week and papers email come close, and both are about Spaces and papers, not repos.

### Gaps
- Email newsletters from Replicate, Ollama, Kaggle, Civitai, LangChain, Vercel, Together and Fireworks were not checked (blogs and sign-up forms not read), so a newsletter may exist off the pages I read.
- Hacker News discussion of any of these hubs was not retrieved.
