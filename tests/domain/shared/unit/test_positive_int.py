from pytest import mark, raises

from domain.shared.unit import PositiveInt


@mark.parametrize(
    "invalid_value",
    [
        0, -1
    ]
)
def test_invalid_values(invalid_value: int):
    with raises(ValueError):
        PositiveInt(invalid_value)
