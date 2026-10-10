import hashlib
from pathlib import Path

import psycopg

LOCK_ID = 7_351_001  # any fixed number; every runner must use the same one


class MigrationError(Exception):
    pass


def checksum(sql: str) -> str:
    return hashlib.sha256(sql.encode()).hexdigest()


def migrate(conn: psycopg.Connection, directory: Path) -> list[str]:
    conn.execute("select pg_advisory_lock(%s)", (LOCK_ID,))
    conn.commit()
    try:
        conn.execute(
            """
            create table if not exists schema_migrations (
                version text primary key,
                checksum text not null,
                applied_at timestamptz not null default now()
            )
            """
        )
        applied = dict(conn.execute("select version, checksum from schema_migrations").fetchall())
        conn.commit()

        files = sorted(directory.glob("*.sql"))

        for path in files:
            if applied.get(path.stem, checksum(path.read_text())) != checksum(path.read_text()):
                raise MigrationError(f"{path.name} was edited after it was applied")

        newly_applied: list[str] = []
        for path in files:
            if path.stem in applied:
                continue
            sql = path.read_text()
            with conn.transaction():
                conn.execute(sql.encode())
                conn.execute(
                    "insert into schema_migrations (version, checksum) values (%s, %s)",
                    (path.stem, checksum(sql)),
                )
            newly_applied.append(path.stem)
        return newly_applied
    finally:
        conn.rollback()
        conn.execute("select pg_advisory_unlock(%s)", (LOCK_ID,))
        conn.commit()
