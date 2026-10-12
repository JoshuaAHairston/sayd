from dataclasses import dataclass
from datetime import date
import psycopg

# --- plain data classes --------------------------------------------

@dataclass
class Quote:
    quote_id: int
    quote_text: str
    created_on: date
    tags: list[str]


@dataclass
class TagCount:
    tag_name: str
    quotes: int


# --- functions: all take an open connection as the first argument --

def find_missing_tags(conn: psycopg.Connection, tag_names: list[str]) -> list[str]:
    """Return the names that don't exist yet, compared case-insensitively."""
    normalized_tag_names = [tag.lower().strip() for tag in tag_names]

    found_tags = conn.execute(
        """
        SELECT tag_name
        FROM tags
        WHERE lower(tag_name) = ANY(%s)
        """,
        (normalized_tag_names,)

    ).fetchall()
    fast_lookup_found_tags = {tag[0].lower().strip() for tag in found_tags}
    missing_tags = []
    seen = set()

    for tag in tag_names: # had to do this to keep the casing the same instead of using normalized tags
        tag = tag.strip()
        if tag.lower() not in seen and tag.lower() not in fast_lookup_found_tags:
            missing_tags.append(tag)
            seen.add(tag.lower())
    return missing_tags


def add_quote(conn: psycopg.Connection, quote_text: str, tag_names: list[str]) -> int:
    """Insert the quote and link its tags in one transaction. Return the new quote_id."""
    return 0


def list_quotes(conn: psycopg.Connection) -> list[Quote]:
    """Every quote with its tags, one Quote per row."""
    return []


def list_tags(conn: psycopg.Connection) -> list[TagCount]:
    """Every tag with how many quotes carry it, including tags with 0."""
    return []


def delete_quote(conn: psycopg.Connection, quote_id: int) -> bool:
    """Delete by id. True if a quote was deleted, False if there was no such id."""
    return False