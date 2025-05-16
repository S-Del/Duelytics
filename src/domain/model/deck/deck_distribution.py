from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from domain.model.result import DuelResult


@dataclass(frozen=True)
class DeckDistribution:
    """複数の試合結果 (DuelResult) から、相手デッキ分布を集計するクラス。"""
    results: Sequence[DuelResult]

    def aggregate(self) -> Counter[str]:
        """{相手デッキ名: 対戦回数} の Counter を返す"""
        names = [result.opponent_deck_name for result in self.results]
        return Counter(names)
