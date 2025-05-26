from pytest import mark
from typing import Sequence

from domain.model.record import RecordFactory
from tests.helpers import make_duel_result


@mark.parametrize(
    "results",
    [[
        make_duel_result(first_or_second_char='F', result_char='W'),
        make_duel_result(first_or_second_char='S', result_char='L'),
        make_duel_result(first_or_second_char='F', result_char='D')
    ]]
)
def test_record_factory(results: Sequence):
    record = RecordFactory(results).create()
    assert record.first_count.value == 2
    assert record.second_count.value == 1
    assert record.win_count.value == 1
    assert record.loss_count.value == 1
    assert record.draw_count.value == 1
    assert record.game_count.value == 3
