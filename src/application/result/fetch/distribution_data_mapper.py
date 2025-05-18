from application.result.fetch import EncounteredDeckData
from domain.model.deck import DeckDistribution, EncounteredDeckStats
from domain.shared.unit.percentage import Percentage


class DistributionDataMapper:
    def __init__(self, distribution: DeckDistribution):
        self._desc_stats = sorted(
            distribution.entries,
            key=lambda item: item.count.value,
            reverse=True
        )
        self._total_game_count = distribution.total_game_count

    def _convert_to_data(self,
        stats: EncounteredDeckStats
    ): return EncounteredDeckData(
        stats.name.value, stats.count.value, str(stats.encounter_rate)
    )

    def top_n_with_other(self,
        top_n: int = 5,
        other_label: str = "その他"
    ) -> list[EncounteredDeckData]:
        if not self._desc_stats:
            return []
        if len(self._desc_stats) <= top_n:
            return [self._convert_to_data(stats) for stats in self._desc_stats]

        data_list: list[EncounteredDeckData] = [
            self._convert_to_data(stats) for stats in self._desc_stats[:top_n]
        ]

        other = self._desc_stats[top_n:]
        other_count = sum(stats.count.value for stats in other)
        p = Percentage.from_ratio(other_count / self._total_game_count)
        data_list.append(EncounteredDeckData(
            other_label,
            other_count,
            str(p)
        ))

        return data_list
