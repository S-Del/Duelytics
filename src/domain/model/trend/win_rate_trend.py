from typing import Sequence

from domain.model.result import DuelResult, ResultChar
from domain.shared.unit import Percentage


class WinRateTrend:
    """渡された複数の試合結果から勝率の推移を算出する

    このクラスは、
    渡された results がどのような順序であるかの知識は持たず、関知しない。
    よって、事前にソートを行ってからこのクラスに results を渡すこと。
    どのような順での勝率の推移を得たいかは、利用側の知識である。

    Args:
        results: Sequence[DuelResult]: 複数の試合結果オブジェクト
    """

    def __init__(self, results: Sequence[DuelResult]):
        self._results = tuple(results)

    def aggregate(self) -> tuple[Percentage, ...]:
        win_count = 0
        win_rate_trend: list[Percentage] = []
        for game_count, result in enumerate(self._results, 1):
            if result.result == ResultChar.WIN:
                win_count += 1
            win_rate_trend.append(
                Percentage.from_ratio(win_count / game_count)
            )
        return tuple(win_rate_trend)
