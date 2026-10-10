import argparse
import sys
from pathlib import Path

from sayd.db import connect
from sayd.migrate import MigrationError, migrate

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def run_migrate() -> int:
    with connect() as conn:
        try:
            applied = migrate(conn, MIGRATIONS_DIR)
        except MigrationError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1

    if applied:
        for version in applied:
            print(f"applied {version}")
    else:
        print("nothing to apply")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="manage.py", description="Sayd author commands")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("migrate", help="apply pending database migrations")

    args = parser.parse_args()
    if args.command == "migrate":
        return run_migrate()
    return 2


if __name__ == "__main__":
    sys.exit(main())
