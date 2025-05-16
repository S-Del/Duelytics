from pytest import mark
from typing import Sequence

from domain.model.record import RecordFactory
from domain.model.result import FirstOrSecond, ResultChar
from tests.helpers import make_result


@mark.parametrize(
    "results",
    [[
        make_result(FirstOrSecond.FIRST, ResultChar.WIN),
        make_result(FirstOrSecond.SECOND, ResultChar.LOSS),
        make_result(FirstOrSecond.FIRST, ResultChar.DRAW)
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
