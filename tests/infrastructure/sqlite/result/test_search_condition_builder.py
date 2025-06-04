from datetime import date
from typing import Any
from pytest import mark, raises

from domain.model.result import FirstOrSecond, ResultChar
from domain.repository.result import SearchResultsQuery
from domain.shared.unit import NonEmptyStr
from infrastructure.sqlite.config import ResultSchema
from infrastructure.sqlite.result import SearchType, SearchConditionBuilder


@mark.parametrize(
    ("value", "search_type", "expected_value"),
    [
        ("\\", "exact", "\\\\"),
        ("%", "exact","\\%"),
        ("_", "exact", "\\_"),
        ("a", "exact", "a"),
        ("b", "partial", "%b%"),
        ("c", "prefix", "c%"),
        ("d", "suffix", "%d")
    ]
)
def test_escape_like_param(
    value: str,
    search_type: SearchType,
    expected_value: str
):
    escaped = SearchConditionBuilder.escape_like_param(value, search_type)
    assert escaped == expected_value


@mark.parametrize(
    "search_type",
    ["invalid_search_type"]
)
def test_excape_like_param_invalid_search_type(search_type):
    with raises(ValueError):
        SearchConditionBuilder.escape_like_param("", search_type)


@mark.parametrize(
    ("query", "expected_where", "expected_params"),
    [(
        {"first_or_second": [FirstOrSecond('F'), FirstOrSecond('S')]},
        f" WHERE {ResultSchema.Columns.FIRST_OR_SECOND} IN (?, ?)",
        ['F', 'S']
    ), (
        {"result": [ResultChar('W'), ResultChar('L'), ResultChar('D')]},
        f" WHERE {ResultSchema.Columns.RESULT} IN (?, ?, ?)",
        ['W', 'L', 'D']
    ), (
        {"my_deck_name": NonEmptyStr("MY_DECK_NAME")},
        f" WHERE {ResultSchema.Columns.MY_DECK_NAME}"
        " LIKE ? ESCAPE '\\'",
        ["MY\\_DECK\\_NAME"]
    ), (
        {"opponent_deck_name": NonEmptyStr("OPPONENT_DECK_NAME")},
        f" WHERE {ResultSchema.Columns.OPPONENT_DECK_NAME}"
        " LIKE ? ESCAPE '\\'",
        ["OPPONENT\\_DECK\\_NAME"]
    ), (
        {"since": date.fromisoformat("2025-05-20")},
        f" WHERE {ResultSchema.Columns.REGISTERED_AT} >= ?",
        ["2025-05-20T00:00:00"]
    ), (
        {"until": date.fromisoformat("2025-05-20")},
        f" WHERE {ResultSchema.Columns.REGISTERED_AT} <= ?",
        ["2025-05-20T23:59:59"]
    ), (
        {
            "since": date.fromisoformat("2025-05-20"),
            "until": date.fromisoformat("2025-05-20")
        },
        f" WHERE {ResultSchema.Columns.REGISTERED_AT} >= ?"
        f" AND {ResultSchema.Columns.REGISTERED_AT} <= ?",
        ["2025-05-20T00:00:00", "2025-05-20T23:59:59"]
    )]
)
def test_search_condition_builder(
    query: SearchResultsQuery,
    expected_where: str,
    expected_params: list[Any]
):
    where_clause, params = SearchConditionBuilder().build(query)
    assert where_clause == expected_where
    assert params == expected_params
