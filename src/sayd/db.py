import psycopg

from sayd.config import get_settings


def connect(url: str | None = None) -> psycopg.Connection:
    return psycopg.connect(url or get_settings().database_url)
