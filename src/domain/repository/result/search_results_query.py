from datetime import date
from typing import Literal, Sequence, TypedDict

from domain.model.result import FirstOrSecond, ResultChar
from domain.shared.unit import NonEmptyStr, PositiveInt


class SearchResultsQuery(TypedDict, total=False):
    first_or_second: Sequence[FirstOrSecond]
    result: Sequence[ResultChar]
    my_deck_name: NonEmptyStr
    my_deck_name_search_type: Literal["exact", "partial", "prefix", "suffix"]
    opponent_deck_name: NonEmptyStr
    opponent_deck_name_search_type: Literal["exact", "partial", "prefix", "suffix"]
    since: date
    until: date
    order: Literal["DESC", "ASC"]
    limit: PositiveInt
