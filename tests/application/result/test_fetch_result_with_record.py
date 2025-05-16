from datetime import date
from uuid import UUID, uuid4

from application.result.fetch import FetchResultWithRecord
from domain.model.result import DuelResult
from domain.model.result.first_or_second import FirstOrSecond
from domain.model.result.result_string import ResultChar
from domain.repository.result import FetchResultQuery, ResultQueryRepository


class SpyResultQueryRepository(ResultQueryRepository):
    """検索用メソッドに渡された引数 (query)が正しいか検証するためのクラス

    このクラスのメソッドが呼び出された場合、最後に渡された引数を保持する。
    主に FetchResultQuery が正しく渡されているか検証用。
    """

    def __init__(self):
        self.last_query: FetchResultQuery | None = None
        self.last_id: UUID | None = None

    def search(self, query: FetchResultQuery) -> tuple[DuelResult]:
        self.last_query = query
        return tuple() # 返す値は不要

    def search_by_id(self, id: UUID) -> DuelResult | None:
        self.last_id = id
        return None # 返す値は不要


def test_builds_correct_fetch_query():
    repository = SpyResultQueryRepository()
    fetch_result = FetchResultWithRecord(repository)
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
    assert repository.last_query is None
    assert repository.last_id == id

    repository = SpyResultQueryRepository()
    fetch_result = FetchResultWithRecord(repository)
    # ID が指定されなかった場合の検証
    fetch_result.handle({
        "first_or_second": ['F'],
        "result": ['W'],
        "my_deck_name": "my_deck_name",
        "my_deck_name_search_type": "exact",
        "opponent_deck_name": "opponent_deck_name",
        "opponent_deck_name_search_type": "exact",
        "since": "2025-05-14",
        "until": "2025-05-14"
    })
    # query が作成され、指定したパラメータをすべて取得できなければならない。
    query = repository.last_query
    assert query is not None
    assert query.get("first_or_second") == [FirstOrSecond.FIRST]
    assert query.get("result") == [ResultChar.WIN]
    assert query.get("my_deck_name") == "my_deck_name"
    assert query.get("my_deck_name_search_type") == "exact"
    assert query.get("opponent_deck_name") == "opponent_deck_name"
    assert query.get("opponent_deck_name_search_type") == "exact"
    assert query.get("since") == date.fromisoformat("2025-05-14")
    assert query.get("until") == date.fromisoformat("2025-05-14")
    assert query.get("order") == "DESC"
