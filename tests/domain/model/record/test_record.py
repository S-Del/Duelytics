from pytest import mark

from domain.model.record import Record
from domain.shared.unit import NonNegativeInt, Percentage


def n(v: int) -> NonNegativeInt:
    """NonNegativeInt のショートカット関数"""
    return NonNegativeInt(v)


@mark.parametrize(
    ("first_count", "second_count", "expected_value"),
    [
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 2)
    ]
)
def test_game_count(first_count: int, second_count: int, expected_value: int):
    _ = n(0)
    record = Record(n(first_count), n(second_count),_,_,_,_,_)
    assert record.game_count == n(expected_value)


@mark.parametrize(
    ("numerator", "denominator", "expected_value"),
    [
        (  1, 1,  1.0),
        (100, 2, 50.0),
        (  1, 0,  0.0)
    ]
)
def test_safe_divide(numerator: int, denominator: int, expected_value: float):
    _ = n(0)
    record = Record(_, _, _, _, _, _, _)
    assert record._safe_divide(n(numerator), n(denominator)) == expected_value


@mark.parametrize(
    ("game_count", "win_count", "expected_value"),
    [
        (  1,  0,   0.0),
        (  0,  1,   0.0),
        (  1,  1, 100.0),
        (100, 50,  50.0)
    ]
)
def test_win_rate(
    game_count: int,
    win_count: int,
    expected_value: float
):
    _ = n(0)
    record = Record(
        n(game_count),_,
        n(win_count),_,_,_,_
    )
    assert record.win_rate == Percentage(expected_value)


@mark.parametrize(
    ("first_count", "first_win_count", "expected_value"),
    [
        (  1,  0,   0.0),
        (  0,  1,   0.0),
        (  1,  1, 100.0),
        (100, 50,  50.0)
    ]
)
def test_first_win_rate(
    first_count: int,
    first_win_count: int,
    expected_value: float
):
    _ = n(0)
    record = Record(
        n(first_count),_,_,_,_,
        n(first_win_count),_
    )
    assert record.first_win_rate == Percentage(expected_value)
