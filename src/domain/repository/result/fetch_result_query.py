from datetime import date
from typing import Literal, Sequence, TypedDict

from domain.model.result import FirstOrSecond, ResultChar


class FetchResultQuery(TypedDict, total=False):
    first_or_second: Sequence[FirstOrSecond]
    result: Sequence[ResultChar]
    my_deck_name: str
    my_deck_name_search_type: Literal["exact", "partial", "prefix", "suffix"]
    opponent_deck_name: str
    opponent_deck_name_search_type: Literal["exact", "partial", "prefix", "suffix"]
    since: date
    until: date
    order: Literal["DESC", "ASC"]
