from collections import Counter
from typing import Sequence

from domain.model.result import DuelResult
from domain.shared.unit import NonNegativeInt, PositiveInt, Percentage
from . import EncounteredDeckStats


class DeckDistribution:
    """複数の試合結果 (DuelResult) から、相手デッキ分布を集計するクラス。"""

    def __init__(self, results: Sequence[DuelResult]):
        self._total_game_count = NonNegativeInt(len(results))
        self._raw_distribution = self._aggregate_raw_distribution(results)

    def _aggregate_raw_distribution(self,
        results: Sequence[DuelResult]
    ) -> frozenset[EncounteredDeckStats]:
        if not results:
            return frozenset()

        non_empty_names = [result.opponent_deck_name for result in results]
        distribution: set[EncounteredDeckStats] = set()
        for name, count in Counter(non_empty_names).items():
            try:
                deck = EncounteredDeckStats(
                    name,
                    PositiveInt(count),
                    Percentage.from_ratio(count / self._total_game_count.value)
                )
            except ValueError:
                continue
            distribution.add(deck)

        return frozenset(distribution)

    @property
    def entries(self) -> tuple[EncounteredDeckStats, ...]:
        return tuple(self._raw_distribution)

    @property
    def total_game_count(self) -> int:
        return self._total_game_count.value
