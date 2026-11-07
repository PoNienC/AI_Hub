"""Parse workflow YAML and enforce the approved schedule and publication boundary."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow():
    return yaml.safe_load((ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8"))


def test_yaml_schedule_dispatch_permissions_and_concurrency():
    document = workflow()
    assert document["on"]["schedule"] == [{"cron": "17 */6 * * *"}]
    assert "workflow_dispatch" in document["on"]
    assert set(document["on"]) == {"schedule", "workflow_dispatch"}
    assert document["permissions"] == {"contents": "write", "issues": "write"}
    assert document["concurrency"] == {"group": "refresh", "cancel-in-progress": False}
    assert document["jobs"]["refresh"]["env"]["GH_REPO"] == "${{ github.repository }}"


def test_workflow_checks_then_one_release_round_trip():
    steps = workflow()["jobs"]["refresh"]["steps"]
    commands = [step["run"] for step in steps if "run" in step]
    ordered = ["uv sync --frozen", "uv run pytest --cov=pipeline --cov-fail-under=80",
               "uv run ruff check .", "uv run pipeline release pull",
               "uv run pipeline run --no-release", "uv run pipeline release push",
               "uv run pipeline site build", "uv run pipeline gates"]
    positions = [next(index for index, command in enumerate(commands) if value in command)
                 for value in ordered]
    assert positions == sorted(set(positions))
    for value in ordered[3:]:
        step = next(step for step in steps if step.get("run") == value)
        assert "if" not in step and not step.get("continue-on-error", False)


def test_actions_pinned_and_builtin_token_only():
    text = (ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8")
    assert "secrets." not in text
    assert workflow()["jobs"]["refresh"]["env"]["GH_TOKEN"] == "${{ github.token }}"
    steps = [step for job in workflow()["jobs"].values() for step in job["steps"]]
    actions = [step for step in steps if "uses" in step]
    assert all(re.fullmatch(r"[\w-]+/[\w-]+@[0-9a-f]{40}", step["uses"]) for step in actions)
    assert any(step["uses"].startswith("astral-sh/setup-uv@") for step in actions)
    checkout = next(step for step in actions if step["uses"].startswith("actions/checkout@"))
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["with"]["token"] == "${{ github.token }}"
    for action, tag in [("upload-pages-artifact", "v3.0.1"), ("deploy-pages", "v4.0.5")]:
        assert re.search(rf"actions/{action}@[0-9a-f]{{40}} # {re.escape(tag)}\b", text)


def test_failure_reporting_and_diagnostic_retention():
    job = workflow()["jobs"]["refresh"]
    assert 0 < job["timeout-minutes"] <= 60
    report = next(step for step in job["steps"] if step.get("if") == "failure()")
    assert "gh issue create --label pipeline-failure" in report["run"]
    assert "--body-file state/failure-body.md" in report["run"]
    assert "state/failure-title.txt" in report["run"]
    assert "PIPELINE_LOG_URL" in report["run"]
    artefact = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/upload-artifact@"))
    assert artefact["if"] == "always()"
    for path in ("state/gateway.sqlite", "state/evidence.jsonl", "state/failures.jsonl", "state/logs/"):
        assert path in artefact["with"]["path"].splitlines()


def test_pages_upload_after_publication_and_deploy_permissions():
    document = workflow()
    steps = document["jobs"]["refresh"]["steps"]
    upload = next(step for step in steps if step.get("uses", "").startswith("actions/upload-pages-artifact@"))
    assert upload["with"]["path"] == "site/dist/"
    assert upload["with"]["retention-days"] == 14
    assert "if" not in upload and not upload.get("continue-on-error", False)
    assert steps.index(upload) > next(index for index, step in enumerate(steps)
                                      if step.get("run") == "uv run pipeline gates")
    deploy = document["jobs"]["deploy"]
    assert deploy["needs"] == "refresh"
    assert deploy["if"] == "github.ref == 'refs/heads/main'"
    assert deploy["permissions"] == {"pages": "write", "id-token": "write"}
    assert deploy["environment"] == {"name": "github-pages", "url": "${{ steps.deployment.outputs.page_url }}"}
    action = next(step for step in deploy["steps"] if step.get("uses", "").startswith("actions/deploy-pages@"))
    assert action["id"] == "deployment"
    assert "if" not in action and not action.get("continue-on-error", False)
    for scope in [document["permissions"], document["jobs"]["refresh"].get("permissions", {})]:
        assert "pages" not in scope and "id-token" not in scope


def test_docs_describe_preview_and_go_live():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "https://ponienc.github.io/AI_Hub/" in readme
    assert "uv run pipeline site build --input tests/fixtures/listings_sample.json --output site/dist.dry" in readme
    assert "uv run python -m http.server 8000 --bind 127.0.0.1 --directory site/dist.dry" in readme
    runbook = (ROOT / "docs/runbook.md").read_text(encoding="utf-8")
    for heading in ["Built-in token limits", "Pages visibility", "Site rollback"]:
        assert f"### {heading}" in runbook


def test_dependabot_parses_and_checks_weekly():
    document = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"))
    assert document["version"] == 2
    assert {item["package-ecosystem"] for item in document["updates"]} == {"uv", "github-actions"}
    assert all(item["schedule"]["interval"] == "weekly" for item in document["updates"])
