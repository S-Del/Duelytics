from application.result.fetch.use_case import DistributionDataMapper
from domain.model.deck import DeckDistribution
from tests.helpers import make_duel_result

def test_top_n_with_other():
    distribution = DeckDistribution([
        make_duel_result(),
        make_duel_result(),
        make_duel_result(),
        make_duel_result(),
        make_duel_result(opponent_deck_name="DECK1"),
        make_duel_result(opponent_deck_name="DECK1"),
        make_duel_result(opponent_deck_name="DECK1"),
        make_duel_result(opponent_deck_name="DECK2"),
        make_duel_result(opponent_deck_name="DECK2"),
        make_duel_result(opponent_deck_name="DECK3")
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
