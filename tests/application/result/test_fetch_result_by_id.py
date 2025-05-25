from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from application.result import IdForResult
from application.result.fetch.use_case import FetchResultById
from domain.repository.result import ResultQueryRepository
from tests.helpers import make_duel_result


def test_fetch_result_by_id_success(
    result_query_repository_mock: ResultQueryRepository,
    fetch_result_by_id: FetchResultById
):
    raw_id = uuid4()
    duel_result_dummy = make_duel_result(raw_id)
    cast(
        MagicMock, result_query_repository_mock.search_by_id
    ).return_value = duel_result_dummy
    result_data = fetch_result_by_id.handle(IdForResult(str(raw_id)))

    assert result_data is not None
    cast(
        MagicMock, result_query_repository_mock.search_by_id
    ).assert_called_once_with(raw_id)
    assert result_data.id == duel_result_dummy.id
    assert (
        result_data.first_or_second_raw
        == duel_result_dummy.first_or_second.value
    )
    assert result_data.result_raw == duel_result_dummy.result.value
    assert result_data.my_deck_name == duel_result_dummy.my_deck_name.value
    assert (
        result_data.opponent_deck_name
        == duel_result_dummy.opponent_deck_name.value
    )
    assert result_data.note == ""


def test_fetch_result_by_id_not_found_expected_none(
    result_query_repository_mock: ResultQueryRepository,
    fetch_result_by_id: FetchResultById
):
    cast(
        MagicMock, result_query_repository_mock.search_by_id
    ).return_value = None
    result_data = fetch_result_by_id.handle(IdForResult(str(uuid4())))
    assert result_data is None
