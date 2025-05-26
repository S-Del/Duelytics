from domain.model.trend import WinRateTrend
from domain.shared.unit.percentage import Percentage
from tests.helpers import make_duel_result


def test_win_rate_trend():
    trend = WinRateTrend([]).aggregate()
    assert trend == tuple()

    results = [
        make_duel_result(result_char='W'),
        make_duel_result(result_char='L'),
        make_duel_result(result_char='L'),
        make_duel_result(result_char='W'),
        make_duel_result(result_char='W'),
        make_duel_result(result_char='L'),
        make_duel_result(result_char='W')
    ]
    trend = WinRateTrend(results).aggregate()
    assert trend[0] == Percentage.from_ratio(1 / 1)
    assert trend[1] == Percentage.from_ratio(1 / 2)
    assert trend[2] == Percentage.from_ratio(1 / 3)
    assert trend[3] == Percentage.from_ratio(2 / 4)
    assert trend[4] == Percentage.from_ratio(3 / 5)
    assert trend[5] == Percentage.from_ratio(3 / 6)
    assert trend[6] == Percentage.from_ratio(4 / 7)
