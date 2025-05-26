from datetime import date
from uuid import UUID, uuid4

from application.result.fetch.use_case import FetchResultsByQuery
from domain.model.result import FirstOrSecond, ResultChar, DuelResult
from domain.repository.result import SearchResultsQuery, ResultQueryRepository
from domain.shared.unit import NonEmptyStr, PositiveInt


class SpyResultQueryRepository(ResultQueryRepository):
    """検索用メソッドに渡された引数 (query)が正しいか検証するためのクラス

    このクラスのメソッドが呼び出された場合、最後に渡された引数を保持する。
    主に FetchResultQuery が正しく渡されているか検証用。
    """

    def __init__(self):
        self._last_query: SearchResultsQuery | None = None
        self._last_id: UUID | None = None

    def search(self, query: SearchResultsQuery) -> tuple[DuelResult]:
        self._last_query = query
        return tuple() # 返す値は不要

    def search_by_id(self, id: UUID) -> DuelResult | None:
        self._last_id = id
        return None # 返す値は不要


def test_builds_correct_fetch_query():
    repository = SpyResultQueryRepository()
    fetch_result = FetchResultsByQuery(repository)
    # ID を指定した場合の検証
    id = uuid4()
    fetch_result.handle({
        "id": str(id),
        "first_or_second": ['F'],
        "result": ['W'],
        "my_deck_name": "my_deck_name",
        "my_deck_name_search_type": "exact",
        "opponent_deck_name": "opponent_deck_name",
        "opponent_deck_name_search_type": "exact",
        "since": "2025-05-14",
        "until": "2025-05-14"
    })
    # query は作成されず last_query は None で、
    # ID のみでの検索が行われていなければならない。
    assert repository._last_query is None
    assert repository._last_id == id

    repository = SpyResultQueryRepository()
    fetch_result = FetchResultsByQuery(repository)
    # ID が指定されなかった場合の検証
    fetch_result.handle({
        "first_or_second": ['F'],
        "result": ['W'],
        "my_deck_name": "my_deck_name",
        "my_deck_name_search_type": "exact",
        "opponent_deck_name": "opponent_deck_name",
        "opponent_deck_name_search_type": "exact",
        "since": "2025-05-14",
        "until": "2025-05-14",
        "limit": 50
    })
    # query が作成され、指定したパラメータをすべて取得できなければならない。
    query = repository._last_query
    assert query is not None
    assert query.get("first_or_second") == [FirstOrSecond.FIRST]
    assert query.get("result") == [ResultChar.WIN]
    assert query.get("my_deck_name") == NonEmptyStr("my_deck_name")
    assert query.get("my_deck_name_search_type") == "exact"
    assert query.get("opponent_deck_name") == NonEmptyStr("opponent_deck_name")
    assert query.get("opponent_deck_name_search_type") == "exact"
    assert query.get("since") == date.fromisoformat("2025-05-14")
    assert query.get("until") == date.fromisoformat("2025-05-14")
    assert query.get("order") == "DESC"
    assert query.get("limit") == PositiveInt(50)
