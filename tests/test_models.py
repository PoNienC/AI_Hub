"""Validate enum boundaries and the publication contract without network access."""

from typing import Literal, get_args, get_origin

import pytest
from pydantic import ValidationError

from pipeline.models import Evidence, Listing, RepoRecord, Score, Snapshot


def examples(repo, score):
    return {
        RepoRecord: repo.model_dump(),
        Snapshot: {"repo_id": "R_1", "run_id": "run_1", "observed_at": "2026-11-07T00:00:00Z",
                   "stars": 100, "forks": 5, "open_issues": 2},
        Evidence: {"repo_id": "R_1", "source": "scorecard", "status": "present",
                   "fetched_at": "2026-11-07T00:00:00Z"},
        Score: score.model_dump(),
        Listing: {"repo": repo.model_dump(), "score": score.model_dump(), "tested": "untested",
                  "score_version": "v0"},
    }


def contains_literal(annotation):
    return get_origin(annotation) is Literal or any(contains_literal(arg) for arg in get_args(annotation))


ENUM_FIELDS = [
    (model, name, get_origin(field.annotation) is list)
    for model in (RepoRecord, Snapshot, Evidence, Score, Listing)
    for name, field in model.model_fields.items() if contains_literal(field.annotation)
]


@pytest.mark.parametrize("model,field,is_list", ENUM_FIELDS)
def test_every_enum_rejects_unknown_values(model, field, is_list, repo, score):
    data = examples(repo, score)[model]
    data[field] = ["unknown_value"] if is_list else "unknown_value"
    with pytest.raises(ValidationError):
        model.model_validate(data)


@pytest.mark.parametrize("model", [RepoRecord, Snapshot, Evidence, Score, Listing])
def test_valid_round_trip_and_unknown_fields(model, repo, score):
    data = examples(repo, score)[model]
    record = model.model_validate(data)
    assert model.model_validate_json(record.model_dump_json()) == record
    with pytest.raises(ValidationError):
        model.model_validate(data | {"unexpected": True})


@pytest.mark.parametrize("required", ["score_version", "tested"])
def test_listing_requires_explicit_status_and_version(required, repo, score):
    data = examples(repo, score)[Listing]
    del data[required]
    with pytest.raises(ValidationError):
        Listing.model_validate(data)


@pytest.mark.parametrize("change", [{"coverage": 1.1}, {"total": -1}, {"total": 101}, {"total": float("nan")}])
def test_score_bounds(change, score):
    with pytest.raises(ValidationError):
        Score.model_validate(score.model_dump() | change)


def test_nullable_labels_and_unevaluated_checks(repo, score):
    listing = Listing(repo=repo, score=score, tested="untested", score_version="v0")
    assert listing.level is None and listing.topic is None
    assert listing.label_status == "pending"
    assert listing.unevaluated_checks == ["fake_stars", "typosquat", "sandbox_test"]


def test_repository_rejects_naive_date_and_negative_counts(repo):
    for change in ({"created_at": "2026-11-07T00:00:00"}, {"stars": -1}):
        with pytest.raises(ValidationError):
            RepoRecord.model_validate(repo.model_dump() | change)
