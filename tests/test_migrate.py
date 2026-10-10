from pathlib import Path

import psycopg
import pytest

from sayd.migrate import MigrationError, migrate


def write(directory: Path, name: str, sql: str) -> None:
    (directory / name).write_text(sql)


def table_exists(conn: psycopg.Connection, name: str) -> bool:
    row = conn.execute("select to_regclass(%s) is not null", (name,)).fetchone()
    assert row is not None
    return row[0]


def applied_versions(conn: psycopg.Connection) -> list[str]:
    rows = conn.execute("select version from schema_migrations order by version").fetchall()
    return [row[0] for row in rows]


def test_applies_migrations_in_order(db, tmp_path):
    # written in reverse order: 0002 only works if 0001 ran first
    write(tmp_path, "0002_add_row.sql", "insert into a values (1);")
    write(tmp_path, "0001_create_a.sql", "create table a (id int);")

    applied = migrate(db, tmp_path)

    assert applied == ["0001_create_a", "0002_add_row"]
    assert applied_versions(db) == ["0001_create_a", "0002_add_row"]


def test_does_not_reapply(db, tmp_path):
    write(tmp_path, "0001_create_a.sql", "create table a (id int);")
    migrate(db, tmp_path)

    assert migrate(db, tmp_path) == []  # would raise "already exists" if it ran again


def test_applies_only_new_migrations(db, tmp_path):
    write(tmp_path, "0001_create_a.sql", "create table a (id int);")
    migrate(db, tmp_path)
    write(tmp_path, "0002_create_b.sql", "create table b (id int);")

    assert migrate(db, tmp_path) == ["0002_create_b"]


def test_failed_migration_rolls_back(db, tmp_path):
    write(tmp_path, "0001_create_a.sql", "create table a (id int);")
    write(tmp_path, "0002_bad.sql", "create table b (id int); select * from nope;")

    with pytest.raises(psycopg.Error):
        migrate(db, tmp_path)

    assert table_exists(db, "a")
    assert not table_exists(db, "b")  # the table created before the error is gone
    assert applied_versions(db) == ["0001_create_a"]


def test_edited_migration_is_rejected(db, tmp_path):
    write(tmp_path, "0001_create_a.sql", "create table a (id int);")
    migrate(db, tmp_path)
    write(tmp_path, "0001_create_a.sql", "create table a (id int, extra int);")

    with pytest.raises(MigrationError):
        migrate(db, tmp_path)
