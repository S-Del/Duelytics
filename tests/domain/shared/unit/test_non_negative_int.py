from pytest import raises

from domain.shared.unit import NonNegativeInt


def test_negative_value():
    with raises(ValueError):
        NonNegativeInt(-1)


def test_to_int():
    assert int(NonNegativeInt(1)) == 1
