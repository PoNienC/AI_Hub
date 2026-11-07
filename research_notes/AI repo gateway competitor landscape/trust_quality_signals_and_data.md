# Trust, quality signals and raw data for an AI repo gateway (state as of 7 November 2026)

> In short: Stars are cheap to fake, weakly linked to maintenance, and since July 2026 GitHub has closed the public stargazer-list API, so a gateway cannot audit star histories itself. Rank on activity, release and supply-chain signals instead, and treat stars only as a low-weight, spike-checked input. Free data is enough for a six-hourly refresh if it leans on GH Archive, GraphQL batching, deps.dev and registry APIs. Nobody has published a "how often do trending repos fail to run" figure.
> Source quality: primary papers, vendor docs and CSA research notes are marked as such. Where only a search-result summary was seen, the note says so.

## 1. Fake stars: scale, AI and crypto repos, GitHub's response, detection heuristics

### Takeaway
The StarScout study (He et al., CMU, NC State, Socket) found millions of suspected fake stars, heavily concentrated from 2024 and in AI/LLM, crypto and malware or phishing repos. Fake stars are about 1% of all monthly stars but hit a large share of popular repos. GitHub removes most flagged repos (about 90%) but far fewer accounts, and has published no new star-specific policy that I could find.

### Cited Findings
- The paper has two versions with different headline numbers. The 2024 preprint reported 4.5 million suspected fake stars over July 2019 to October 2024 (15,835 repos) — [arXiv abstract](https://arxiv.org/abs/2412.13459); [search listing of v1 figures](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsarx,edsarx.2412.13459). The later version, titled "Six Million (Suspected) Fake Stars on GitHub" and accepted at ICSE 2026, covers July 2019 to December 2024 — [ICSE 2026 listing](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/14/Six-Million-Suspected-Fake-Stars-on-GitHub-A-Growing-Spiral-of-Popularity-Contests).
- v2 figures: about 6.0 million suspected fake stars across 26,254 repos before postprocessing; 3.81 million stars across 18,617 repos and about 301,000 accounts after postprocessing. 1.06 million came from the low-activity signature and 4.93 million from the lockstep signature — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2). Use the post-processed figure (3.81 million) when quoting a conservative number.
- Prevalence: at most about 1% of all stars in a given month, but in July 2024 16.66% of popular repos (3,499) had fake star campaigns. Activity surged in 2024 — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- AI and crypto: AI/LLM repos were 96 repos (16.6%) of the categorised set and the largest category among trending repos (25 of 78, 32.1%). Blockchain/crypto was 76 repos (13.1%) and the largest group among repos linked to packages (44 of 229, 19.2%). Spam/phishing was the largest category (131 repos, 22.6%). Many AI repos were academic paper repos or LLM start-up products — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- GitHub Trending: 78 repos with fake-star campaigns appeared on Trending (peak 25 in March 2024); the archive covered only five languages, so this is likely an undercount — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Package registries: 229 repos (1.23%) were linked to 738 packages; 70.46% of those packages had no dependants — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Effect on real stars: a 1% rise in fake stars is tied to about a 0.07% rise in real stars next month (roughly five times weaker than the effect of real stars); the cumulative longer-run effect is slightly negative (about -0.04%). The authors conclude fake stars help only briefly — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Detection heuristics (both run over GH Archive):
  - Low-activity: an account with one star event plus at most one other event in that repo on the same day; repos kept only with at least 50 such stars.
  - Lockstep: CopyCatch clustering with n=50 accounts, m=10 repos, 30-day window, rho=0.5.
  - Postprocessing: a month with more than 50 fake stars making up more than 50% of that month's stars, and an all-time fake share above 10%.
  - Source: [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2). Socket's earlier write-up describes the same two heuristics, with the low-activity one inspired by Dagster's detector and the clustering one replicated on BigQuery — [Socket, 27 Aug 2024](https://socket.dev/blog/3-7-million-fake-github-stars-a-growing-threat-linked-to-scams-and-malware).
- Accuracy: recall 81.23% of repos (688 of 847) and 75.95% of accounts against a "Stargazer Ghost Network" dataset. Precision was not measured directly; authors estimate about 99%, implying about 180 false-positive repos. The paper gives both 81.23% and 82.23% for repo recall, an internal inconsistency — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Both heuristics give false positives, and fake accounts may star legitimate repos to blend in — [Socket, 27 Aug 2024](https://socket.dev/blog/3-7-million-fake-github-stars-a-growing-threat-linked-to-scams-and-malware).
- GitHub's response, measured: as of January 2025, 90.42% of detected repos and 57.07% of accounts (with postprocessing) were deleted, versus baselines of 5.03% and 3.54%. The authors reported 130 phishing repos and two SEO-spam accounts to GitHub; by August 2025 all reported phishing repos and one SEO account were inaccessible — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2). Earlier, in mid-August 2024, Socket measured about 89% of repos deleted but only 18.12% of accounts; 7.86% of taken-down repos had been live over a month; VirusTotal flagged malware in 28 surviving repos — [Socket, 27 Aug 2024](https://socket.dev/blog/3-7-million-fake-github-stars-a-growing-threat-linked-to-scams-and-malware). GitHub told the authors it "actively works to remove" fake starrers (same Socket page).
- GitHub's rulebook: its Acceptable Use Policy prohibits coordinated inauthentic activity, per a news summary; I did not read the policy itself — [Computing summary via search](https://www.computing.co.uk/news/2025/security/fake-github-stars-inflating-malicious-repositories). I found no 2025 or 2026 GitHub announcement of a new star-specific policy.
- Recommendations from the authors: do not rely on star counts alone for high-stakes decisions; platforms should weight stars by authenticity or adoption; third-party tools should flag dependencies with fake-star histories. Socket's alert flagged 283 of two million customer SBOMs — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2). Socket's "Suspicious Stars on GitHub" alert launched 27 August 2024 at High severity — [Socket](https://socket.dev/blog/3-7-million-fake-github-stars-a-growing-threat-linked-to-scams-and-malware).
- Price of stars: the paper gives no prices; it says merchants sell in batches of about 50 or 100 — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2). Price figures ($0.03 to $0.85, $0.10) appear only in secondary coverage and are not verified — [Gigazine](https://gigazine.net/gsc_news/en/20241221-github-fake-stars).
- Vendor case studies (weak sources, unverified): a TrustStar blog post on 100 AI repos reports an airdrop-driven jump of 11,000 stars in 48 hours for QuipNetwork repos, a one-character typosquat of a drone firmware repo that gained 1,485 stars in about 90 minutes (March 2026), and stargazers starring within a second of each other. Its score weights (account quality 26%, temporal 23%, project health 26%, authenticity 25%) are not validated. All 10 "CAUTION" repos had zero commits per week — [TrustStar on DEV](https://dev.to/truststar/we-scanned-100-ai-repos-on-github-heres-what-we-found-o4a).

### Inferences
- Fake stars are a small share of all stars but a large share of what a "popular" or "trending" list shows, so a star-ranked gateway is exposed exactly where it is most visible.
- Burst and lockstep heuristics need stargazer timestamps; see question 5 for why those are now hard to get from GitHub directly (GH Archive WatchEvents remain the route).
- The 90% repo-deletion rate means fake-star repos disappear, so a gateway should expect link rot and re-check existence on each refresh.

### Gaps
- I could not read GitHub's own Acceptable Use Policy text or any GitHub statement on star fraud after 2024.
- No independent replication of StarScout beyond vendor blogs (TrustStar) was found; precision is estimated, not measured.
- Whether the 2026 stargazer-list restriction was motivated by star fraud is not stated; GitHub cites spam (see question 5).

## 2. Do stars track code quality, maintenance or ease of running?

### Takeaway
Evidence says stars are a popularity and promotion signal, not a quality or upkeep signal. Contributor and commit activity do better. I found no study linking stars to "runs first time".

### Cited Findings
- Borges and Valente (J. Systems and Software, 2018, "What's in a GitHub Star?"): developers star to show appreciation or bookmark; stars do not correlate with repo age but do correlate with forks; organisation-owned repos get more stars; growth follows promotion and release bursts. Practitioners rated stars the most useful popularity metric, and about three in four check stars before using a project — [arXiv 1811.07643](https://arxiv.org/abs/1811.07643v1) (from a search summary; the full text was not read).
- Coelho et al., "Identifying Unmaintained Projects in GitHub" (2018): a machine-learning model on commit, fork and issue activity flags unmaintained projects with 80% precision and 96% recall, validated with maintainers of 129 projects. The abstract does not mention stars — [arXiv 1809.04041](https://arxiv.org/abs/1809.04041). A search-result summary quotes Spearman rho of 0.10 for stars versus maintenance and 0.44 for contributors, and cites a roughly 50,000-star project with low maintenance; I could not verify those numbers in the paper text — [arXiv PDF](https://arxiv.org/pdf/1809.04041).
- A 2023 study treats stars as a reflective measure of quality across 36,460 repos and reports quality scores explain star counts well — [arXiv 2307.12082](https://arxiv.org/pdf/2307.12082) (search snippet only). A 2022 Innopolis preliminary study states stars are not a sufficient health indicator — [Innopolis PDF](https://innopolis.university/filespublic/NIR_2022_preliminarystudy.pdf) (snippet only). The literature therefore disagrees; treat it as mixed.
- Stars can be manufactured and then affect discovery: 78 fake-campaign repos reached GitHub Trending — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Executability evidence, notebooks only: a large earlier study found only 24.11% of 863,878 attempted GitHub notebook runs executed without errors and 4.03% reproduced results — [NSF PAR 10311570](https://par.nsf.gov/servlets/purl/10311570) (via search summary). A 2025 MSR paper (42,546 notebooks from 4,456 repos with at least four stars) argues "run without error" is too strict a definition — [arXiv 2502.04184](https://arxiv.org/html/2502.04184v4). A 2026 Kaggle study found 35.4% of 12,720 notebooks still reproducible, and that environment backporting did not close the gap — [arXiv 2602.07195](https://arxiv.org/html/2602.07195v1).

### Inferences
- A weak star-to-maintenance link is consistent with stars being driven by launch buzz, so a "stars velocity" ranking mostly measures marketing.
- For "runs on first try", the best proxy evidence is dependency drift: notebook and ML repos decay quickly, so repo age since last release and pinned environments should matter more than stars.

### Gaps
- No peer-reviewed study correlating stars with build success or setup success for AI repos.
- Exact correlation coefficients in Coelho et al. and the 2023 and 2022 studies are not verified from full text.

## 3. Quality-scoring schemes: which apply to repositories, and which are free to call at scale

### Takeaway
Only OpenSSF Scorecard (and deps.dev as a free mirror of it) scores repositories rather than packages, and both are free and cacheable. Snyk Advisor, Socket, Libraries.io SourceRank and Tidelift are package-centred; Snyk Advisor was retired as a standalone site in 2026.

### Cited Findings
- OpenSSF Scorecard: 18 default checks (Binary-Artifacts, Branch-Protection, CI-Tests, CII-Best-Practices, Code-Review, Contributors, Dangerous-Workflow, Dependency-Update-Tool, Fuzzing, License, Maintained, Pinned-Dependencies, Packaging, SAST, Security-Policy, Signed-Releases, Token-Permissions, Vulnerabilities), each scored 0 to 10 and combined as a risk-weighted average (Critical 10, High 7.5, Medium 5, Low 2.5). It scans more than 1.3 million repos weekly and serves results through a REST API at api.scorecard.dev. Weekly scans omit CI-Tests, Contributors and Dependency-Update-Tool because of API cost. Results are CDN-cached and may be stale; the BigQuery public dataset is described as no longer available; the checks are heuristics with false positives and negatives; GitHub and GitLab only — [ossf/scorecard README](https://github.com/ossf/scorecard).
- Scorecard check details relevant to "runs and is kept alive": Maintained (High risk) rewards weekly commits over 90 days and only succeeds for GitHub projects older than 90 days; Pinned-Dependencies inspects Dockerfiles, shell scripts and GitHub workflows (not a project's Python requirements); CI-Tests looks at about the 30 latest commits; Signed-Releases looks for signature or SLSA provenance files in release assets without verifying them; Dangerous-Workflow flags risky `pull_request_target` and script-injection patterns — [Scorecard checks doc](https://github.com/ossf/scorecard/blob/main/docs/checks.md). Dangerous-Workflow is the check closest to the 2025 and 2026 CI compromises in question 4.
- deps.dev API (Google): JSON over HTTP at api.deps.dev/v3. GetProject returns stars, forks, open issues, licence and, when available, the full Scorecard with per-check scores and overall score, plus OSS-Fuzz data. Covers Go, RubyGems, npm, Cargo, Maven, PyPI and NuGet packages. Clients may cache results; generated data is CC-BY 4.0; a BigQuery dataset exists. The page states no rate limit or key requirement — [deps.dev API docs](https://docs.deps.dev/api/v3/).
- OpenSSF Best Practices badge: self-attested criteria at passing, silver and gold. As of 5 May 2023 there were 5,735 registered projects, 1,019 passing, 48 silver, 18 gold (three years old) — [BSSW summary](https://bssw.io/items/openssf-best-practices-badge-program). CHAOSS has a metric page for the badge — [CHAOSS](https://chaoss.community/?p=3939). Scorecard has its own CII-Best-Practices check (above).
- CHAOSS: I only found the badge metric. A points scheme (gold 10, silver 7, passing 5, in progress 2) appears on a Gitee mirror and is unconfirmed — [Gitee compass](https://compass.gitee.com/docs/metrics-models/software_artifact/robustness/cii_best_badge).
- Snyk Advisor: the standalone site was retired; announcement dated 2 February 2026. Popularity, Maintenance, Security and Community scores moved to security.snyk.io; coverage is npm, PyPI and Go. The post does not mention an API — [Snyk blog](https://snyk.io/blog/snyk-advisor-security-database/).
- Socket.dev: package-level supply-chain analysis, plus the "Suspicious Stars on GitHub" alert (see question 1). Free-tier and API limits are not confirmed; third-party trackers disagree — [agentdeals.dev](https://agentdeals.dev/vendor/socket-dev) (unverified, third party).
- Libraries.io: API is free to registered users with a key, 60 requests per minute, with higher volume offered through Tidelift. The documented endpoints I could see were platforms, project info, dependencies and dependants; SourceRank endpoints were not visible in the part of the page I could read (the page is very long). A banner says Sonar has agreed to acquire Tidelift — [Libraries.io API docs](https://libraries.io/api).
- Tidelift: Sonar announced the acquisition in December 2024; Tidelift pays maintainers of thousands of packages to follow secure practices ("lifted" packages) — [Socket on the deal](https://socket.dev/blog/sonar-to-acquire-tidelift); [Sonar demo page](https://sonarsource.com/tidelift-lifted-package-demo). I did not find a public API or a documented scoring formula.
- ecosyste.ms offers open services for packages, repositories, issues, commits, advisories and a repo timeline — [ecosyste.ms docs](https://docs.ecosyste.ms/). Its rate limits, key and licence terms could not be read (rate-limits page returned 404).

### Inferences
- Repository-level: Scorecard (via deps.dev or api.scorecard.dev) is the only free, scalable, repository-level score, but it measures security hygiene, not "AI repo works". Most small AI repos will not be in the weekly scan; the gateway should show "not scanned" rather than zero.
- Package-level (Snyk, Socket, Libraries.io, Tidelift) matter only for repos that publish to PyPI or npm, and the cleanest free route to them is deps.dev or the registry APIs.

### Gaps
- Socket API pricing and free-tier limits: only unverified third-party pages found.
- CHAOSS Starter Project Health model contents: page not found (404); not verified.
- deps.dev rate limits and whether a key is needed: not stated in the docs I read.
- api.scorecard.dev endpoint reference and rate limits: page fetch returned only a title.
- Libraries.io SourceRank status and exact API fields in 2026: not confirmed.

## 4. Supply-chain and security incidents in AI repos and AI developer tooling, 2025 to 2026

### Takeaway
The pattern since 2025 is: impersonating packages, compromised CI (GitHub Actions `pull_request_target` and stolen publish tokens), poisoned skill and MCP marketplaces, and now prompt injection through README and config files. AI developer tooling is a deliberate target.

### Cited Findings
- Cloud Security Alliance (CSA) research note listing incidents 2023 to 2026 — [CSA, 8 Mar 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-devtool-supply-chain-attacks-20260308/):
  - `gptplus` and `claudeai-eng` PyPI packages delivered the JarkaStealer infostealer; uploaded November 2023, found by Kaspersky about November 2024; about 1,700 downloads.
  - 28 January 2024: Lasso Security's benign `huggingface-cli` package, registered after LLMs hallucinated the name, passed 15,000 downloads (a research demonstration, not malware).
  - December 2024: Ultralytics YOLO PyPI compromise via `pull_request_target` misconfiguration and cache poisoning, then a stolen PyPI token published four malicious versions.
  - March 2025: `tj-actions/changed-files` and `reviewdog/action-setup` compromise (CVE-2025-30066, CVE-2025-30154; CISA advisory 18 March 2025), affecting more than 23,000 repos.
  - 2025: Cursor CVE-2025-54135 (CurXecute) and CVE-2025-54136 (MCPoison), where a malicious MCP server or config rewrote `~/.cursor/mcp.json`; GitHub Copilot CVE-2025-53773 (hidden prompt injection enabling auto-approve; fixed August 2025); `mcp-remote` CVE-2025-6514 (CVSS 9.6, 437,000+ downloads); MCP Inspector CVE-2025-49596 (CVSS 9.4).
  - June to July 2025: a fake Open VSX "Solidity" extension with inflated installs (about 54,000) led to a $500,000 crypto theft. Inflated popularity counts were the lure.
  - January 2026: two VS Code "ChatGPT" extensions (1.5 million installs combined) sent opened files to servers in China.
  - February to March 2026: "InstallFix", Google Ads leading to cloned Claude Code install pages that delivered Amatera Stealer.
  - Slopsquatting study (Spracklen et al.): 19.7% of 576,000 LLM code samples referenced non-existent packages; 58% of hallucinated names repeated.
- TeamPCP campaign, March 2026: 19 March Trivy CI compromise; 23 March two Checkmarx OpenVSX extensions; 24 March LiteLLM 1.82.7 and 1.82.8 on PyPI (live about 2 to 3 hours; payload ran at every Python start via a `.pth` file; stole LLM API keys, cloud and Kubernetes credentials); 27 March telnyx 4.87.1 and 4.87.2. LiteLLM has about 97 million monthly downloads — [CSA, 29 Mar 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-pypi-supply-chain-campaign-20260329-csa/). A separate report gives 46,996 malicious downloads before quarantine (via search summary, unverified) — [CSA CISO briefing, 31 Mar 2026](https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20260331/).
- "Mini Shai-Hulud", largest wave 11 May 2026 (worm code published about 15 May): over 400 package versions across 170+ npm and PyPI packages, including Mistral AI SDKs, Guardrails AI, TanStack, PyTorch Lightning and Microsoft's DurableTask client. A fork pull request poisoned a build cache; OIDC tokens were read from runner memory and used to forge SLSA Build Level 3 provenance. It is described as the first supply-chain attack to persist through AI coding agent config, adding `SessionStart` hooks to `.claude/settings.json` and tasks to `.vscode/tasks.json` — [CSA, May 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-shai-hulud-supply-chain-ai-pipeline-202605/). The CSA notes are labelled as AI-assisted research notes; the 518-million-download figure is theirs and unverified.
- Malicious npm impersonation of the MCP git server: `mcp-server-git` 0.0.1 and 0.0.2 sent host data from a `postinstall` script to a `workers.dev` endpoint; OSV advisory MAL-2026-5478 published 9 June 2026, from Amazon Inspector via the OSSF malicious-packages repo. The author called it "canary research" — [OSV](https://osv.dev/vulnerability/MAL-2026-5478).
- ClawHavoc, early February 2026: Koi Security audited all 2,857 skills on OpenClaw's ClawHub and flagged 341 as malicious (335 tied to one operation) using fake "prerequisite" install steps in SKILL.md to deliver Atomic macOS Stealer and other malware. Antiy CERT counts at least 1,184 malicious skills historically; sources differ on discovery date (1 or 3 February) — [eSecurityPlanet](https://esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub); [Antiy CERT](https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents/).
- README prompt injection ("ReadSecBench", March 2026): hidden instructions added to 500 real READMEs (Java, Python, C, C++, JavaScript) led agents from several vendors to send sensitive data to external servers in up to 85% of cases, about 84% with direct wording and about 91% when the instruction sat two links from the README. None of 15 human reviewers spotted it; rule-based scanners over-flagged and AI classifiers still missed linked-file cases — [Help Net Security, 17 Mar 2026](https://helpnetsecurity.com/2026/03/17/ai-agents-readme-files-data-leak-security-risk) (paper: [arXiv 2603.11862](https://arxiv.org/pdf/2603.11862), cited by that article, not read). Earlier: HiddenLayer showed a README comment hijacking Cursor in July 2025 — [HiddenLayer](https://www.hiddenlayer.com/research/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor).
- Model hubs: ReversingLabs ("nullifAI", February 2025) found two malicious PyTorch models on Hugging Face that evaded Picklescan; the Hacker News describes them as closer to proof-of-concept — [Help Net Security, 10 Feb 2025](https://www.helpnetsecurity.com/2025/02/10/malicious-ml-models-found-on-hugging-face-hub/). A May 2026 CSA note cites JFrog findings and academic work on 1,574 potentially malicious squatting models (10.4% confirmed suspicious); secondary and unverified — [CSA, May 2026](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_huggingface_model_supply_chain_attack_20260512-csa-styled.pdf).
- Earlier point on rate: Sonatype reported malicious open-source packages up 188% year on year in Q2 2025 (via the CSA TeamPCP note, unverified).
- Fake-star link to malware: StarScout found fake-star campaigns tied to phishing and malware repos, and Socket's alert exists because of that — [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Unconfirmed items from search summaries only: a backdoored `postmark-mcp` npm package (September 2025) that BCC'd outgoing mail — [HackerNoon](https://hackernoon.com/lite/mcp-servers-are-a-supply-chain-you-have-not-inventoried-yet) (secondary); an axios npm compromise on 31 March 2026 — [DEV post](https://dev.to/toniantunovic/mcp-connector-poisoning-how-compromised-npm-packages-hijack-your-ai-agent-3ha0) (secondary, not tied to MCP).

### Inferences
- A gateway that surfaces "popular AI repos" is itself an attack-surface amplifier: attackers combine bought stars, typosquatted names and README instructions aimed at agents.
- Scorecard's Dangerous-Workflow and Token-Permissions checks, plus recent-release and publish-method signals, map directly onto the TeamPCP and Shai-Hulud entry points.
- Scanning READMEs for prompt injection is not reliable (ReadSecBench), so the gateway should not render README text to an agent unsanitised.

### Gaps
- Check Point's February 2026 Claude Code config disclosure, mentioned in one search summary, was not found in the CSA note I read and was not verified.
- No primary vendor reports (Socket, Snyk, Checkmarx, ReversingLabs, Phylum, Unit 42) were read directly for 2026 incidents beyond OSV, eSecurityPlanet and Antiy; much of the 2026 detail rests on CSA research notes.
- Hugging Face Hub-side malware scan statistics were not read at source.

## 5. Raw data sources and what a free tier can pull every six hours

### Takeaway
GitHub's July 2026 restriction removes the public stargazer-timestamp endpoint, so star-history work must come from GH Archive. GraphQL batching, deps.dev, registry APIs and the Hugging Face API are enough for a six-hourly refresh of a few thousand AI repos.

### Cited Findings
- GitHub stargazers restricted: a changelog dated 30 June 2026 says the `/repos/{owner}/{repo}/stargazers` and `/subscribers` endpoints will be limited to admins and collaborators, and `/users/{username}/subscriptions` is deprecated and returns empty responses, because the data was misused to collect user data for spam. Callers may see empty responses or 403. No exact effective date and no alternative is given — [GitHub changelog](https://github.blog/changelog/2026-06-30-upcoming-access-restrictions-to-public-api-endpoints-and-ui-views/). GitHub's current starring docs state the restriction takes effect from July 2026 and still describe the `application/vnd.github.star+json` header that returns `starred_at` — [GitHub REST starring docs](https://docs.github.com/en/rest/activity/starring). Star History reports charts for repos you do not own now fail and no workaround exists; its post (6 July 2026) carries a September 2026 update saying a new endpoint returns exact daily star counts, and the page is internally inconsistent — [Star History](https://www.star-history.com/blog/github-stargazer-api-restriction). Status of the GraphQL `stargazers` field and of plain `stargazerCount` is not stated in any source I read.
- REST rate limits: 60 requests per hour unauthenticated per IP; 5,000 per hour for an authenticated user; GitHub App installations 5,000 base up to 12,500; `GITHUB_TOKEN` in Actions 1,000 per hour per repo. Secondary limits: at most 100 concurrent requests, 900 points per minute for REST, 2,000 for GraphQL; may change without notice — [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).
- GraphQL: 5,000 points per hour per user; each connection needs `first` or `last` from 1 to 100; at most 500,000 nodes per call; cost is requests divided by 100, minimum 1 point — [GitHub GraphQL limits](https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api).
- GH Archive: hourly JSON files (`https://data.gharchive.org/YYYY-MM-DD-H.json.gz`, UTC) from 12 February 2011, with the Events API as source from 2015; BigQuery public dataset `githubarchive` with year, month and day tables, updated hourly; BigQuery gives 1 TB of free query processing per month. The page states no size, licence, WatchEvent specifics or known gaps — [gharchive.org](https://www.gharchive.org/). StarScout used about 20 TiB of GH Archive and, as of January 2025, GH Archive held 326 million stars across 331 million repos — [Socket](https://socket.dev/blog/3-7-million-fake-github-stars-a-growing-threat-linked-to-scams-and-malware); [arXiv v2 HTML](https://arxiv.org/html/2412.13459v2).
- Hugging Face Hub API: endpoints documented in an OpenAPI playground (spec at `huggingface.co/.well-known/openapi.json`). Limits over 5-minute fixed windows (September 2025): anonymous 500 API requests per IP, free user 1,000, PRO 2,500; anonymous and free values may change. Pass an HF token — [HF API docs](https://huggingface.co/docs/hub/api); [HF rate limits](https://huggingface.co/docs/hub/rate-limits).
- PyPI downloads: pypistats.org API (recent, overall, python_major/minor, system), 180 days of history, daily updates, per-IP rate limit without published numbers; do not bulk-download; use BigQuery for history (1 TB per month free as stated by pypistats) — [pypistats API](https://pypistats.org/api/).
- npm downloads: `api.npmjs.org/downloads/point|range/...`; bulk up to 128 packages (unscoped only, 365 days); single package up to 18 months; per-version counts only for the last 7 days; data lands once daily after UTC midnight; no rate limit stated — [npm download-counts doc](https://github.com/npm/registry/blob/main/docs/download-counts.md).
- Hacker News Algolia search API: reported as 10,000 requests per hour per IP and 1,000 hits per query (slice by time to go deeper). This rests on secondary posts; the official page returned no content when fetched — [DEV: Scraping HN in 2026](https://dev.to/agenthustler/scraping-hacker-news-in-2026-complete-guide-algolia-api-date-filters-3iep).
- Other free sources already covered: deps.dev (stars, forks, Scorecard; question 3), api.scorecard.dev (question 3), Libraries.io at 60 requests per minute (question 3).

### Inferences
- Arithmetic (not sourced): one token gives 5,000 REST requests per hour, so up to 30,000 per six-hour window; a GraphQL query for 100 repos using aliases can cost a few points, so several thousand repos per refresh with release, commit and contributor-count fields fits comfortably inside 5,000 points per hour. Use ETags or conditional requests and the `rateLimit` field to stay inside limits.
- Star counts per repo can probably still be read cheaply (counts, not lists), but this is not confirmed after the July 2026 change; the gateway should test it before designing around it.
- Star-spike detection should be rebuilt on GH Archive WatchEvents. One six-hour slice is only six hourly files, so a free-tier GitHub Action can stream and filter them; a full re-scan like StarScout's (20 TiB) would not fit the free BigQuery quota, but a rolling window for a watched list of repos would.
- Hugging Face anonymous limits (500 requests per 5 minutes) are enough for listing the top few thousand models per refresh with a token.

### Gaps
- BigQuery on-demand price per TiB: the pricing page fetch returned only a title; the commonly quoted $6.25 per TiB is from memory and not verified here.
- GH Archive total size, licence, and whether event gaps exist since late 2024: not stated on the page read.
- Whether GraphQL `stargazers` (with `starredAt`) and `stargazerCount` are affected by the June 2026 change: no source found.
- Exact Algolia HN limits from the official source; deps.dev and ecosyste.ms limits; npm rate limits.

## 6. Signals of "runs on first try", and measurement of trending-repo failure rates

### Takeaway
I found no study that measures how often trending GitHub or AI repos fail to run. The closest evidence is notebook-reproducibility work, which shows low success rates. Specific signals (Dev Containers, Docker, CI badges, pinned dependencies, recent releases) are plausible proxies but unvalidated.

### Cited Findings
- Notebook executability: 24.11% of 863,878 notebook executions ran without error and 4.03% reproduced results — [NSF PAR 10311570](https://par.nsf.gov/servlets/purl/10311570) (via search summary). 35.4% of 12,720 popular Kaggle notebooks remain reproducible — [arXiv 2602.07195](https://arxiv.org/html/2602.07195v1). A 2025 MSR paper cautions that the strict definition of "executable" inflates failure rates — [arXiv 2502.04184](https://arxiv.org/html/2502.04184v4).
- A 2026 study of 100 ICSE replication packages examined executability; it notes an earlier study of 400 AI papers did not try to execute them — [arXiv 2601.02066](https://arxiv.org/pdf/2601.02066v1) (search snippet only).
- Scorecard measures adjacent proxies: Pinned-Dependencies (build and workflow dependencies only), CI-Tests (tests run before merge), Packaging (publishes to a registry), Maintained (commits in 90 days), Signed-Releases — [Scorecard checks doc](https://github.com/ossf/scorecard/blob/main/docs/checks.md). Note Scorecard's Pinned-Dependencies does not inspect `requirements.txt`-style runtime pins.
- Pickle-format model files are an execution risk; CSA advises preferring `safetensors` — [CSA TeamPCP note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-pypi-supply-chain-campaign-20260329-csa/).
- TeamPCP mitigation advice is a list of signals the gateway can check: Trusted Publishers (OIDC) rather than long-lived tokens, hash-pinned dependencies, actions pinned to commit SHAs — same CSA note.

### Inferences
- A cheap "runnable" score could combine: a Dockerfile or devcontainer present; a release or tag in the last 12 months; a lockfile or pinned requirements; CI present and passing on the default branch; a published package whose latest version resolves in deps.dev. None of these is validated against actual run success; only a sandboxed build test would be.
- Because notebook studies show most repos fail on the first attempt, an honest label would be "setup signals present", not "runs".

### Gaps
- No measurement of failure rates for GitHub Trending repos or AI repos specifically.
- No source read on Dev Containers, Codespaces, one-click deploy buttons or CI badges as predictors of runnability. These are listed only as candidate signals.
- The 2026 PubMed Central and ICSE replication studies surfaced in search were not read in full.
