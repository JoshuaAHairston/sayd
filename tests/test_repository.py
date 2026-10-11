from sayd.repository import find_missing_tags

# The tags_table_and_connection fixture (conftest.py) seeds three tags: anxious, work, Rest


def test_unknown_tags_are_all_missing(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["hope", "joy"]) == ["hope", "joy"]


def test_existing_tag_is_not_missing(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["anxious", "hope"]) == ["hope"]


def test_no_tags_missing_when_all_exist(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["anxious", "work"]) == []


def test_empty_input_returns_empty_list(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, []) == []


def test_stored_lowercase_matches_typed_uppercase(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["Work"]) == []


def test_stored_mixed_case_matches_typed_lowercase(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["rest"]) == []


def test_keeps_the_authors_casing_for_missing_tags(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["Hope"]) == ["Hope"]


def test_strips_surrounding_whitespace(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["  work ", " hope "]) == ["hope"]


def test_duplicate_missing_tags_are_returned_once_ignoring_case(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["Hope", "hope", "HOPE"]) == ["Hope"]


def test_duplicate_existing_tags_are_not_missing(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["WORK", "work"]) == []


def test_preserves_input_order(tags_table_and_connection):
    assert find_missing_tags(tags_table_and_connection, ["hope", "joy", "anxious", "calm"]) == [
        "hope",
        "joy",
        "calm",
    ]