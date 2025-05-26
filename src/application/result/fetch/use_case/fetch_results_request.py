from typing import Literal, TypedDict, Sequence


class FetchResultsRequest(TypedDict, total=False):
    id: str
    first_or_second: Sequence[Literal['F', 'S']]
    result: Sequence[Literal['W', 'L', 'D']]
    my_deck_name: str
    my_deck_name_search_type: Literal["exact", "partial", "prefix", "suffix"]
    opponent_deck_name: str
    opponent_deck_name_search_type: Literal[
        "exact", "partial", "prefix", "suffix"
    ]
    since: str
    until: str
    order: Literal["DESC", "ASC"]
    limit: int
