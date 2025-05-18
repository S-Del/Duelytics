from domain.model.result import FirstOrSecond, ResultChar
from tests.helpers import make_result


def test_duel_result():
    result = make_result(FirstOrSecond.FIRST, ResultChar.WIN)
    assert result.first_or_second.value == 'F'
    assert result.result.value == 'W'
    assert result.my_deck_name.value == "MY_DECK_NAME"
    assert result.opponent_deck_name.value == "OPPONENT_DECK_NAME"
    assert result.note == None
