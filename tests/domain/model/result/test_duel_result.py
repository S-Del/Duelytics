from domain.model.result import FirstOrSecond, ResultChar
from tests.helpers import make_result


def test_duel_result():
    result = make_result(FirstOrSecond.FIRST, ResultChar.WIN)
    assert result.first_or_second.value == '先攻'
    assert result.first_or_second_raw.value == 'F'
    assert result.result.value == '勝利'
    assert result.result_raw.value == 'W'
    assert result.note == ""
