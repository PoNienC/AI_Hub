"""One failure record shared by rollback, the append-only log and issue text."""

from __future__ import annotations

from datetime import datetime

from pydantic import AwareDatetime, Field, JsonValue

from pipeline.budgets import BudgetExceeded
from pipeline.gates import GateFailure
from pipeline.models import Identifier, NonNegativeInt, Record
from pipeline.store import StateStore


class RunFailure(Record):
    """A failed run retained outside the promoted database."""

    run_id: Identifier
    started: AwareDatetime
    finished: AwareDatetime
    failed_step: Identifier
    reason: str
    rows_in: NonNegativeInt
    rows_out: NonNegativeInt
    previous_count: NonNegativeInt | None = None
    log_path: str
    budgets: dict[str, JsonValue] = Field(default_factory=dict)

    @property
    def issue_title(self) -> str:
        """Name the gate, budget or execution stage that stopped the run."""
        return f"Pipeline failure: {self.failed_step}"

    @property
    def issue_body(self) -> str:
        """Render diagnostics from exactly the record appended to failures.jsonl."""
        previous = "first run" if self.previous_count is None else str(self.previous_count)
        return (
            f"Run: {self.run_id}\nStarted: {self.started.isoformat()}\n"
            f"Finished: {self.finished.isoformat()}\nFailing gate, budget or stage: {self.failed_step}\n"
            f"Reason: {self.reason}\nRows in: {self.rows_in}\nRows out: {self.rows_out}\n"
            f"Previous successful count: {previous}\nLog: {self.log_path}\n"
        )


def abort_run(
    error: Exception, *, store: StateStore | None, stage: str, run_id: str,
    started: datetime, finished: datetime, rows_in: int, rows_out: int,
    log_path: str, previous_count: int | None = None,
    budgets: dict[str, JsonValue] | None = None,
) -> RunFailure:
    """Discard this run's working copy and return its single diagnostic record.

    Gate and budget errors are deliberately sanitised by their producers. Other
    exceptions retain their type only, avoiding credentials or source payloads.
    """
    if store is not None:
        store.rollback()
    failed_step = stage
    reason = type(error).__name__
    if isinstance(error, GateFailure):
        failed_step, reason = error.gate, str(error)
    elif isinstance(error, BudgetExceeded):
        failed_step, reason = f"budget.{error.resource}", str(error)
    return RunFailure(
        run_id=run_id, started=started, finished=finished, failed_step=failed_step,
        reason=reason, rows_in=rows_in, rows_out=rows_out, previous_count=previous_count,
        log_path=log_path, budgets={} if budgets is None else budgets,
    )
