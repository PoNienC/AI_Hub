"""Offline JSON fixture loading and shared validated example records."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from pipeline.models import RepoRecord, Score


@pytest.fixture
def load_fixture() -> Callable[[str], Any]:
    """Return a fresh copy of recorded JSON for each fixture request."""
    def load(name: str) -> Any:
        return json.loads((Path(__file__).parent / "fixtures" / name).read_text(encoding="utf-8"))

    return load


@pytest.fixture
def repo() -> RepoRecord:
    """Supply a minimal repository with a stable node identifier."""
    return RepoRecord(
        github_id="R_1", full_name="example/agent", html_url="https://github.com/example/agent",
        created_at="2025-01-01T00:00:00Z", stars=100, forks=5, open_issues=2,
    )


@pytest.fixture
def score() -> Score:
    """Supply a versioned result for model and storage tests."""
    return Score(repo_id="R_1", run_id="run_1", score_version="v0", coverage=0.5, total=75)
