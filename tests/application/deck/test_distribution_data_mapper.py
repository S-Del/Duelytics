from application.result.fetch.use_case import DistributionDataMapper
from domain.model.deck import DeckDistribution
from domain.model.result import FirstOrSecond, ResultChar
from domain.shared.unit.non_empty_str import NonEmptyStr
from tests.helpers import make_result

def test_top_n_with_other():
    distribution = DeckDistribution([
        make_result(FirstOrSecond('F'), ResultChar('W')),
        make_result(FirstOrSecond('F'), ResultChar('W')),
        make_result(FirstOrSecond('F'), ResultChar('W')),
        make_result(FirstOrSecond('F'), ResultChar('W')),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK1")
        ),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK1")
        ),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK1")
        ),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK2")
        ),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK2")
        ),
        make_result(
            FirstOrSecond('F'),
            ResultChar('W'),
            opponent_deck_name=NonEmptyStr("DECK3")
        )
    ])

    data_list = DistributionDataMapper(distribution).top_n_with_other(3)
    assert len(data_list) == 4
    assert data_list[0].name == "OPPONENT_DECK_NAME"
    assert data_list[0].count == 4
    assert data_list[1].name == "DECK1"
    assert data_list[1].count == 3
    assert data_list[2].name == "DECK2"
    assert data_list[2].count == 2
    # Top 3 を取得しているので、それ以外は「その他」になる。
    assert data_list[3].name == "その他" # つまり DECK3
    assert data_list[3].count == 1
