from pytest import mark
from typing import Sequence

from domain.model.deck import DeckDistribution
from domain.model.result import FirstOrSecond, ResultChar
from tests.helpers import make_result


@mark.parametrize(
    "results",
    [(
        make_result(
            FirstOrSecond.FIRST,
            ResultChar.WIN,
            opponent_deck_name="DECK_1"
        ),
        make_result(
            FirstOrSecond.FIRST,
            ResultChar.WIN,
            opponent_deck_name="DECK_1"
        ),
        make_result(
            FirstOrSecond.FIRST,
            ResultChar.WIN,
            opponent_deck_name="DECK_1"
        ),
        make_result(
            FirstOrSecond.FIRST,
            ResultChar.WIN,
            opponent_deck_name="DECK_2"
        ),
        make_result(
            FirstOrSecond.FIRST,
            ResultChar.WIN,
            opponent_deck_name="DECK_3"
        ),
    )]
)
def test_deck_distribution(results: Sequence):
    distribution = DeckDistribution(results).aggregate()
    assert distribution["DECK_1"] == 3
    assert distribution["DECK_2"] == 1
    assert distribution["DECK_3"] == 1
