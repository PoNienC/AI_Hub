"""GitHub GraphQL repository search with pagination and explicit cost accounting.

Contributor coverage uses mentionableUsers.totalCount as a proxy: mentionable
users are not necessarily contributors. The optional REST fallback calls
contributors?per_page=1&anon=true and reads the last-page Link-header count.
It is disabled by default; when enabled, it replaces the proxy for each unique
repository after search. REST results may be cached and include anonymous users.

GitHub reports actual GraphQL cost only after execution. Reserve one point per
attempt and reconcile every reported cost before accepting data, including
partial-error responses. Answered non-success responses without rateLimit use
a logged four-point estimate for this bounded search query. This conservative
estimate covers up to 100 repositories with three child connections each; it
is not a measured charge and must be revisited if SEARCH_QUERY changes.
Lost responses retain a minimum-cost reservation and an unmeasured-call
counter; a later successful response cannot make such a run acceptable, so
the source aborts. No call is sent once the budget is exhausted.

Project verification on 07 November 2026 confirmed that REST and GraphQL
accept X-GitHub-Api-Version: 2026-03-10. If GitHub rejects that value, change
the shared header to 2022-11-28 as the fallback.

References:
https://docs.github.com/en/graphql/reference/repos
https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
https://docs.github.com/en/rest/repos/repos#list-repository-contributors
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, Self
from urllib.parse import parse_qs, quote, urlsplit

import httpx

from pipeline.budgets import Budget
from pipeline.config import Settings
from pipeline.http import HttpClient, HttpRequestError
from pipeline.models import RepoRecord

LOG = logging.getLogger(__name__)
GRAPHQL_URL = "https://api.github.com/graphql"
# About three points from (1 + 3 * 100) / 100, plus one point of headroom.
GRAPHQL_ERROR_COST_ESTIMATE = 4
SEARCH_QUERY = """
query RepositorySearch($query: String!, $first: Int!, $after: String) {
  search(query: $query, type: REPOSITORY, first: $first, after: $after) {
    nodes {
      ... on Repository {
        id nameWithOwner url description stargazerCount forkCount pushedAt createdAt
        primaryLanguage { name }
        licenseInfo { spdxId }
        issues(first: 1, states: OPEN) { totalCount }
        repositoryTopics(first: 100) { nodes { topic { name } } }
        latestRelease { tagName publishedAt }
        mentionableUsers(first: 1) { totalCount }
        readme: object(expression: "HEAD:README.md") { oid }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
  rateLimit { cost remaining }
}
"""


class GitHubResponseError(RuntimeError):
    """Malformed or unusable GitHub data, with no raw response in the message."""

    def __init__(self, query_name: str, reason: str) -> None:
        self.query_name = query_name
        super().__init__(f"GitHub query {query_name!r}: {reason}")


class GraphQLError(GitHubResponseError):
    """GraphQL reported errors, even if partial data was returned."""


class GitHubRateLimitError(GitHubResponseError):
    """GitHub's remote allowance is exhausted."""


def _map_node(node: dict[str, Any], query_name: str) -> RepoRecord:
    release = node["latestRelease"] or {}
    return RepoRecord(
        github_id=node["id"], full_name=node["nameWithOwner"], html_url=node["url"],
        description=node["description"], language=(node["primaryLanguage"] or {}).get("name"),
        stars=node["stargazerCount"], forks=node["forkCount"], open_issues=node["issues"]["totalCount"],
        created_at=node["createdAt"], pushed_at=node["pushedAt"],
        licence_spdx=(node["licenseInfo"] or {}).get("spdxId"),
        topics=[item["topic"]["name"] for item in node["repositoryTopics"]["nodes"]],
        release_tag=release.get("tagName"), release_published_at=release.get("publishedAt"),
        contributor_count=node["mentionableUsers"]["totalCount"], contributor_source="mentionable_users",
        readme_sha=(node["readme"] or {}).get("oid"), query_tags=[query_name],
    )


class GitHubSource:
    """Fetch bounded repository searches and deduplicate on stable node identifiers."""

    def __init__(
        self, settings: Settings, *, budget: Budget | None = None,
        client: httpx.Client | None = None, sleep: Callable[[float], None] | None = None,
    ) -> None:
        if settings.github_token is None or not settings.github_token.get_secret_value().strip():
            raise ValueError("GH_TOKEN or GITHUB_TOKEN is required for GitHub GraphQL")
        self.settings = settings
        self.budget = Budget.from_settings(settings) if budget is None else budget
        options = {} if sleep is None else {"sleep": sleep}
        self.http = HttpClient(self.budget, client=client, timeout_seconds=settings.http_timeout_seconds,
                               retries=settings.http_retries, **options)
        self._headers = {
            "Authorization": f"Bearer {settings.github_token.get_secret_value()}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }
        self.rate_limit_remaining: int | None = None

    def _account_response(self, response: httpx.Response, query_name: str) -> None:
        try:
            payload = response.json()
        except ValueError:
            if response.is_success:
                raise GitHubResponseError(query_name, "invalid JSON response") from None
            payload = {}
        if not isinstance(payload, dict):
            if response.is_success:
                raise GitHubResponseError(query_name, "response must be an object")
            payload = {}
        data = payload.get("data") or {}
        rate = data.get("rateLimit") if isinstance(data, dict) else None
        if rate is not None:
            if not isinstance(rate, dict) or any(
                type(rate.get(key)) is not int or rate[key] < 0 for key in ("cost", "remaining")
            ):
                raise GitHubResponseError(query_name, "invalid rateLimit counters")
            self.budget.record_graphql_cost(rate["cost"])
            self.rate_limit_remaining = rate["remaining"]
        elif not response.is_success:
            LOG.warning(
                "Estimated GitHub GraphQL cost as %d points for HTTP %d response without rateLimit counters",
                GRAPHQL_ERROR_COST_ESTIMATE, response.status_code,
            )
            self.budget.record_graphql_cost(GRAPHQL_ERROR_COST_ESTIMATE)
        if payload.get("errors"):
            raise GraphQLError(query_name, "GraphQL returned errors; partial data discarded")
        if response.is_success and rate is None:
            raise GitHubResponseError(query_name, "missing rateLimit counters")
        if self.rate_limit_remaining == 0:
            raise GitHubRateLimitError(query_name, "remote rate limit exhausted")
        if response.is_success and self.budget.github_unmeasured_calls:
            raise GitHubResponseError(query_name, "earlier GraphQL cost is unmeasured; run aborted")

    def search(
        self, queries: Mapping[str, str] | None = None, *, all_queries: bool = False,
        per_query_cap: int | None = None,
    ) -> list[RepoRecord]:
        """Return deduplicated records; the cap counts nodes visited per query.

        Results are only returned after every selected query succeeds. Duplicate
        nodes keep the latest metadata and accumulate their matched query tags.
        """
        cap = self.settings.per_query_cap if per_query_cap is None else per_query_cap
        if type(cap) is not int or not 1 <= cap <= 1000:
            raise ValueError("per_query_cap must be an integer between 1 and 1000")
        selected = self.settings.selected_queries(all_queries=all_queries) if queries is None else queries
        records: dict[str, RepoRecord] = {}
        for query_name, query in selected.items():
            after = None
            seen_cursors: set[str] = set()
            visited = 0
            while visited < cap:
                if self.rate_limit_remaining == 0:
                    raise GitHubRateLimitError(query_name, "remote rate limit exhausted")
                first = min(100, cap - visited)
                response = self.http.request(
                    "POST", GRAPHQL_URL, source="github", headers=self._headers, retryable=True,
                    json={"query": SEARCH_QUERY, "variables": {"query": query, "first": first, "after": after}},
                    before_attempt=self.budget.reserve_graphql,
                    on_response=lambda response, name=query_name: self._account_response(response, name),
                )
                if not response.is_success:
                    raise HttpRequestError("github", f"HTTP {response.status_code}")
                try:
                    search = response.json()["data"]["search"]
                    nodes, page = search["nodes"], search["pageInfo"]
                    if not isinstance(nodes, list) or len(nodes) > first or type(page["hasNextPage"]) is not bool:
                        raise ValueError("Invalid search page")
                    for node in nodes:
                        record = _map_node(node, query_name)
                        previous = records.get(record.github_id)
                        if previous is not None:
                            record.query_tags = list(dict.fromkeys(previous.query_tags + record.query_tags))
                        records[record.github_id] = record
                    visited += len(nodes)
                    if not page["hasNextPage"] or visited >= cap:
                        break
                    after = page["endCursor"]
                    if not nodes or not isinstance(after, str) or not after or after in seen_cursors:
                        raise ValueError("Pagination did not advance")
                    seen_cursors.add(after)
                except (KeyError, TypeError, ValueError, AttributeError):
                    raise GitHubResponseError(query_name, "malformed repository page or pagination") from None
        if self.settings.contributor_fallback:
            for record in records.values():
                record.contributor_count = self._rest_contributors(record.full_name)
                record.contributor_source = "rest_contributors"
        return list(records.values())

    def _rest_contributors(self, full_name: str) -> int:
        path = "/repos/" + "/".join(quote(part, safe="") for part in full_name.split("/")) + "/contributors"
        response = self.http.request(
            "GET", "https://api.github.com" + path, source="github", headers=self._headers,
            params={"per_page": 1, "anon": "true"}, before_attempt=self.budget.charge_github,
        )
        if response.status_code == 204:
            return 0
        if response.status_code != 200:
            raise HttpRequestError("github", f"contributors HTTP {response.status_code}")
        try:
            contributors = response.json()
            if not isinstance(contributors, list) or len(contributors) > 1:
                raise ValueError("Invalid contributors response")
            last = response.links.get("last", {}).get("url")
            if last:
                parsed = urlsplit(last)
                params = parse_qs(parsed.query)
                if parsed.scheme != "https" or parsed.netloc != "api.github.com" or parsed.path != path:
                    raise ValueError("Invalid pagination URL")
                count = int(params["page"][0])
                if params.get("per_page") != ["1"] or count < 1 or not contributors:
                    raise ValueError("Invalid last page")
                return count
            if response.headers.get("Link"):
                raise ValueError("Missing last-page count")
            return len(contributors)
        except (KeyError, TypeError, ValueError):
            raise GitHubResponseError(full_name, "malformed contributors pagination") from None

    def close(self) -> None:
        """Release the owned HTTP client."""
        self.http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
