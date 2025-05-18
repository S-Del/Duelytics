from pytest import raises

from domain.shared.unit import NonEmptyStr


def test_empty_value():
    with raises(ValueError):
        NonEmptyStr("")
    with raises(ValueError):
        NonEmptyStr(" ")
    with raises(ValueError):
        NonEmptyStr("\n")
    with raises(ValueError):
        NonEmptyStr(" \n   \n\n ")

def test_to_str():
    non_empty_str = NonEmptyStr("TEST")
    assert non_empty_str.value == "TEST"
    assert str(non_empty_str) == "TEST"
