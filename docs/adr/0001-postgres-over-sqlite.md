# Use Postgres instead of SQLite

Sayd's data is small enough for SQLite, but we use Postgres from the start so there is no migration if SQLite ever becomes a limit, and to get practice with Postgres. Data access is raw SQL through `psycopg`, with no ORM.
