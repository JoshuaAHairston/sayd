from sayd.db import connect


def test_connects_using_database_url():
    with connect() as conn:
        assert conn.execute("select 1").fetchone() == (1,)
