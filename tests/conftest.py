from collections.abc import Iterator

import psycopg
import pytest

from sayd.config import get_settings
from sayd.db import connect


@pytest.fixture
def db() -> Iterator[psycopg.Connection]:
    url = get_settings().test_database_url
    if not url:
        pytest.fail("TEST_DATABASE_URL is not set")
    if not url.split("?")[0].endswith("_test"):
        pytest.fail("TEST_DATABASE_URL must point at a database whose name ends in _test")

    with connect(url) as conn:
        conn.execute("drop schema public cascade")
        conn.execute("create schema public")
        conn.commit()
        yield conn


@pytest.fixture
def tags_table_and_connection(db: psycopg.Connection) -> psycopg.Connection:
    """A tags table seeded with: anxious, work, Rest (stored mixed case on purpose)."""
    db.execute(
        """
        CREATE TABLE tags (
            tag_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            tag_name TEXT NOT NULL
        )
        """
    )
    db.execute("CREATE UNIQUE INDEX tags_tag_name_key ON tags (lower(tag_name))")
    for name in ("anxious", "work", "Rest"):
        db.execute("INSERT INTO tags (tag_name) VALUES (%s)", (name,))
    return db
