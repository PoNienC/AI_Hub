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


def test_workflow_checks_then_one_release_round_trip():
    steps = workflow()["jobs"]["refresh"]["steps"]
    commands = [step["run"] for step in steps if "run" in step]
    ordered = ["uv sync --frozen", "uv run pytest --cov=pipeline --cov-fail-under=80",
               "uv run ruff check .", "uv run pipeline release pull",
               "uv run pipeline run --no-release", "uv run pipeline release push"]
    positions = [next(index for index, command in enumerate(commands) if value in command)
                 for value in ordered]
    assert positions == sorted(set(positions))
    for value in ordered[-3:]:
        step = next(step for step in steps if step.get("run") == value)
        assert "if" not in step and not step.get("continue-on-error", False)


def test_actions_pinned_and_only_approved_secret_used():
    text = (ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8")
    assert set(re.findall(r"secrets\.([A-Za-z_][A-Za-z_0-9]*)", text)) == {"GH_TOKEN"}
    steps = workflow()["jobs"]["refresh"]["steps"]
    actions = [step for step in steps if "uses" in step]
    assert all(re.fullmatch(r"[\w-]+/[\w-]+@[0-9a-f]{40}", step["uses"]) for step in actions)
    assert any(step["uses"].startswith("astral-sh/setup-uv@") for step in actions)
    checkout = next(step for step in actions if step["uses"].startswith("actions/checkout@"))
    assert checkout["with"]["persist-credentials"] is False


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


def test_dependabot_parses_and_checks_weekly():
    document = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"))
    assert document["version"] == 2
    assert {item["package-ecosystem"] for item in document["updates"]} == {"uv", "github-actions"}
    assert all(item["schedule"]["interval"] == "weekly" for item in document["updates"])
