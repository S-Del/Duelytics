from tests.helpers import make_duel_result


def test_duel_result():
    result = make_duel_result(first_or_second_char='F', result_char='W')
    assert result.first_or_second.value == 'F'
    assert result.result.value == 'W'
    assert result.my_deck_name.value == "MY_DECK_NAME"
    assert result.opponent_deck_name.value == "OPPONENT_DECK_NAME"
    assert result.note == None
