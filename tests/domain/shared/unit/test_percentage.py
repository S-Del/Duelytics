from domain.shared.unit import Percentage


def test_to_str():
    p = Percentage(50)
    assert str(p) == "50.0%"


def test_custom_format():
    p = Percentage(1.111)
    assert format(p, ".2f") == "1.11"
