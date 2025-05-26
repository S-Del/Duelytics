from collections import Counter
from typing import Sequence

from domain.model.result import DuelResult, ResultChar, FirstOrSecond
from domain.shared.unit import NonNegativeInt
from . import Record


class RecordFactory:
    """複数の試合結果 (DuelResult) から、戦績を集計するクラス"""

    def __init__(self, results: Sequence[DuelResult]):
        self._first_or_second_counter = Counter(
            duel.first_or_second for duel in results
        )
        self._result_counter = Counter(
            duel.result for duel in results
        )
        self._result_with_side_counter = Counter(
            (duel.first_or_second, duel.result) for duel in results
        )

    def create(self) -> Record:
        """集計された戦績を Record として返す"""
        return Record(
            NonNegativeInt(self._first_or_second_counter[FirstOrSecond.FIRST]),
            NonNegativeInt(
                self._first_or_second_counter[FirstOrSecond.SECOND]
            ),
            NonNegativeInt(self._result_counter[ResultChar.WIN]),
            NonNegativeInt(self._result_counter[ResultChar.LOSS]),
            NonNegativeInt(self._result_counter[ResultChar.DRAW]),
            NonNegativeInt(
                self._result_with_side_counter[
                    (FirstOrSecond.FIRST, ResultChar.WIN)
                ]
            ),
            NonNegativeInt(
                self._result_with_side_counter[
                    (FirstOrSecond.SECOND, ResultChar.WIN)
                ]
            )
        )
