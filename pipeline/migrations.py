"""Versioned SQLite schema creation, applied only to a working database."""

import sqlite3

SCHEMA_VERSION = 1

SCHEMA_V1 = (
    """CREATE TABLE repos (
        github_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        renamed_from TEXT NOT NULL DEFAULT '[]',
        metadata_json TEXT NOT NULL,
        readme_sha TEXT,
        first_seen TEXT NOT NULL,
        last_seen TEXT NOT NULL
    )""",
    """CREATE TABLE snapshots (
        repo_id TEXT NOT NULL REFERENCES repos(github_id),
        run_id TEXT NOT NULL,
        observed_at TEXT NOT NULL,
        stars INTEGER NOT NULL CHECK (stars >= 0),
        forks INTEGER NOT NULL CHECK (forks >= 0),
        open_issues INTEGER NOT NULL CHECK (open_issues >= 0),
        pushed_at TEXT,
        PRIMARY KEY (repo_id, run_id)
    )""",
    "CREATE INDEX snapshots_repo_observed ON snapshots(repo_id, observed_at)",
    """CREATE TABLE scores (
        repo_id TEXT NOT NULL REFERENCES repos(github_id),
        run_id TEXT NOT NULL,
        score_version TEXT NOT NULL,
        components_json TEXT NOT NULL,
        coverage REAL NOT NULL CHECK (coverage BETWEEN 0 AND 1),
        total REAL CHECK (total BETWEEN 0 AND 100),
        PRIMARY KEY (repo_id, run_id, score_version)
    )""",
    """CREATE TABLE run_log (
        run_id TEXT PRIMARY KEY,
        started TEXT NOT NULL,
        finished TEXT,
        status TEXT NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
        budgets_json TEXT NOT NULL,
        rows_in INTEGER NOT NULL DEFAULT 0 CHECK (rows_in >= 0),
        rows_out INTEGER NOT NULL DEFAULT 0 CHECK (rows_out >= 0),
        gate_results_json TEXT NOT NULL DEFAULT '{}'
    )""",
)


def migrate(connection: sqlite3.Connection) -> None:
    """Create version 1 atomically or reject an unsupported schema version."""
    connection.execute("BEGIN IMMEDIATE")
    try:
        connection.execute("""CREATE TABLE IF NOT EXISTS schema_version (
            singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
            version INTEGER NOT NULL
        )""")
        row = connection.execute("SELECT version FROM schema_version WHERE singleton = 1").fetchone()
        if row is None:
            for statement in SCHEMA_V1:
                connection.execute(statement)
            connection.execute("INSERT INTO schema_version VALUES (1, ?)", (SCHEMA_VERSION,))
        elif row[0] != SCHEMA_VERSION:
            raise ValueError(f"Unsupported state schema version: {row[0]}")
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
