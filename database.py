import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = "worldcup.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # WAL mode allows concurrent reads during writes
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id     TEXT UNIQUE,
                date            TEXT,
                group_name      TEXT,
                home_team       TEXT,
                away_team       TEXT,
                home_score      INTEGER,
                away_score      INTEGER,
                status          TEXT DEFAULT 'scheduled',
                stadium         TEXT,
                city            TEXT,
                data_source     TEXT DEFAULT 'seed',
                last_updated    TEXT,
                manual_override INTEGER DEFAULT 0
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_group   ON matches(group_name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_status  ON matches(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_teams   ON matches(home_team, away_team)")


def get_all_matches():
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM matches ORDER BY date, id")
        return [dict(row) for row in cursor.fetchall()]


def get_match_by_id(match_id):
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_match(match_id, home_score, away_score, status):
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE matches
            SET home_score = ?, away_score = ?, status = ?,
                data_source = 'manual', manual_override = 1, last_updated = ?
            WHERE id = ?
            """,
            (home_score, away_score, status, now, match_id),
        )


def reset_override(match_id):
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            "UPDATE matches SET manual_override = 0, last_updated = ? WHERE id = ?",
            (now, match_id),
        )


def upsert_match(match):
    """
    Insert or update a match from the API.
    If manual_override=1, preserves scores/status but updates metadata.
    Returns 'inserted', 'updated', or 'skipped'.
    """
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id, manual_override FROM matches WHERE external_id = ?",
            (match["external_id"],),
        ).fetchone()

        if existing is None:
            conn.execute(
                """
                INSERT INTO matches
                    (external_id, date, group_name, home_team, away_team,
                     home_score, away_score, status, stadium, city, data_source, last_updated)
                VALUES
                    (:external_id, :date, :group_name, :home_team, :away_team,
                     :home_score, :away_score, :status, :stadium, :city, 'api', :last_updated)
                """,
                {**match, "last_updated": now},
            )
            return "inserted"

        if existing["manual_override"] == 1:
            # Preserve scores/status; only update safe metadata
            conn.execute(
                """
                UPDATE matches
                SET stadium = ?, city = ?, external_id = ?, last_updated = ?
                WHERE id = ?
                """,
                (match.get("stadium"), match.get("city"), match["external_id"], now, existing["id"]),
            )
            return "skipped"

        conn.execute(
            """
            UPDATE matches
            SET date = ?, group_name = ?, home_team = ?, away_team = ?,
                home_score = ?, away_score = ?, status = ?,
                stadium = ?, city = ?, data_source = 'api', last_updated = ?
            WHERE id = ?
            """,
            (
                match.get("date"), match.get("group_name"),
                match.get("home_team"), match.get("away_team"),
                match.get("home_score"), match.get("away_score"), match.get("status"),
                match.get("stadium"), match.get("city"),
                now, existing["id"],
            ),
        )
        return "updated"


def has_data():
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        return count > 0
