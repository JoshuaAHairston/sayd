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
