from pytest import mark
from typing import Sequence

from domain.model.deck import DeckDistribution
from domain.model.result import DuelResult
from tests.helpers import make_duel_result


@mark.parametrize(
    "results",
    [(
        make_duel_result(opponent_deck_name="DECK_1"),
        make_duel_result(opponent_deck_name="DECK_1"),
        make_duel_result(opponent_deck_name="DECK_1"),
        make_duel_result(opponent_deck_name="DECK_2"),
        make_duel_result(opponent_deck_name="DECK_2"),
        make_duel_result(opponent_deck_name="DECK_3"),
        make_duel_result(opponent_deck_name="DECK_4")
    )]
)
def test_deck_distribution(results: Sequence[DuelResult]):
    distribution = DeckDistribution(results)
    assert distribution.total_game_count == 7

    sorted_distribution = sorted(
        distribution.entries,
        key=lambda item: item.count.value,
        reverse=True
    )
    assert len(sorted_distribution) == 4
    assert sorted_distribution[0].name.value == "DECK_1"
    assert sorted_distribution[0].count.value == 3
    assert sorted_distribution[1].name.value == "DECK_2"
    assert sorted_distribution[1].count.value == 2

#   DeckDistribution は順序を持たないため、entries の sorted の後であっても、
#   対戦回数が同じ 1 である DECK_3 と DECK_4 が、
#   sorted_distribuiton の何番目に格納されているかは不明である。
#   よって、以下のようなテストはすべきではない。
#   assert sorted_distribution[2].name.value == "DECK_3" <- DECK_4 の可能性
#   assert sorted_distribution[3].name.value == "DECK_4" <- DECK_3 の可能性
#   どちらかになっていれば良い (or) のであれば以下の様にテストする。
    assert (
        sorted_distribution[2].name.value == "DECK_3"
        or sorted_distribution[2].name.value == "DECK_4"
    )
    assert (
        sorted_distribution[3].name.value == "DECK_3"
        or sorted_distribution[3].name.value == "DECK_4"
    )
#   もしくは以下の様に、重複の無い Set 構造で取得して比較する。
    name_set = {
        sorted_distribution[2].name.value,
        sorted_distribution[3].name.value
    }
    assert name_set == {"DECK_3", "DECK_4"}
#   回数は判明しているためテストできる
    assert sorted_distribution[2].count.value == 1
    assert sorted_distribution[3].count.value == 1
