# Own data: 100-repo candidate labelling and run-readiness signals

Source: this project's own pull from the GitHub search API on 7 November 2026 (scripts/pull_candidate_repos.py, scripts/sample_and_fetch.py), plus LLM-assigned candidate labels (Claude Sonnet, README-only) in data/labelled_repos_for_review.csv. The labels are CANDIDATES awaiting the owner's review; they are not yet a gold set. n = 100, sampled across 17 AI topic queries, top three plus three lower-half repos per query. Stars range 360 to 439,103, median 28,917.

## Takeaway
Stars carry almost no information about how easy a repo is to run (Spearman 0.08 between stars and a seven-signal readiness score). A README-based LLM labeller assigns a skill level to every repo with high or medium confidence in 97 of 100 cases, which makes level grouping cheap to produce; whether the labels are right is the owner's review to settle.

## Findings (own computation, reproducible from data/labelled_repos_for_review.csv)
- Level distribution (candidate labels): beginner 31, intermediate 33, advanced 28, not_runnable 8 (lists, courses, weights).
- Confidence: high 43, medium 54, low 3 (labring/sealos, docmost/docmost, jamwithai/production-agentic-rag-course).
- Topic distribution: mcp_server_or_skill 14, other 10, learning_resource_or_list 9, rag_knowledge 9, agent_framework 9, image_video_gen 8, evals_observability 7, browser_computer_use 7, coding_agent 7, voice_realtime 6, fine_tuning_training 6, model_weights_or_research 4, app_builder_ui 3, local_inference 1.
- Stars versus readiness: Spearman rho = 0.081 for the seven-signal score (Dockerfile, devcontainer, deploy or Colab badge, quickstart heading, lockfile, .github folder, licence file). Per signal: Dockerfile 0.05, devcontainer 0.07, deploy badge -0.29, quickstart 0.18, lockfile 0.05, CI folder 0.15, licence 0.04. Needs-API-key -0.03.
- Readiness by star band (mean score out of 7): under 5k stars 3.21 (n 19); 5k to 20k 3.90 (n 20); 20k to 60k 4.43 (n 30); over 60k 3.58 (n 31). Readiness peaks in the middle band and falls for the most-starred repos.
- Beginner-labelled repos have the highest median stars (103,218) against intermediate 28,365 and advanced 14,003. The top 50 by stars hold 23 beginner labels; the bottom 50 hold 8. Reading: the biggest repos are polished products (installers, hosted apps), while the long tail of trending repos is mostly intermediate or advanced. A beginner using GitHub Trending's long tail is therefore poorly served; the top of the chart is fine.
- Signals present: quickstart heading 73 of 100, lockfile or manifest 71, Dockerfile or compose 28, devcontainer 13, deploy or Colab badge 17, API key mentioned in README 37, licence file 94, .github folder 87.
- Staleness: 13 of 100 not pushed in the last 180 days (for example AUTOMATIC1111/stable-diffusion-webui, coqui-ai/TTS, haotian-liu/LLaVA, SciPhi-AI/R2R). High-star search results include abandoned repos with no warning.
- Topic versus level: coding agents are mostly beginner (6 of 7); MCP servers and skills mostly beginner (9 of 14); fine-tuning all advanced (6 of 6); voice mostly advanced (4 of 6); RAG and browser automation mostly intermediate.

## Inferences
- Rank by stars and a beginner sees polished products at the top and unrunnable research code below. A level filter changes the middle and tail of the list, not the head.
- The "deploy badge" signal is contaminated by Colab and Hugging Face Spaces links on research repos, which is why it correlates negatively with stars; a cleaner signal needs manual confirmation of a one-click path.
- Mechanical signals alone will not grade a repo; the README reading did most of the work. A production labeller needs the owner-reviewed gold set to measure agreement (target in the brief: 85 per cent).
- No repo was actually executed in this phase. "Works first try" remains untested.

## Gaps
- Labels are unreviewed. Sample is 100, drawn from search by stars, so it under-represents small new repos.
- Stargazer timestamps were not pulled (GitHub restricted the stargazers endpoint from July 2026, per the trust research note); star velocity was not computed.
- No execution test; no security scan; no licence compatibility check beyond presence of a licence file.
