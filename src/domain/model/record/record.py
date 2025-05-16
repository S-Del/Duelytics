from dataclasses import dataclass

from domain.shared.unit import NonNegativeInt, Percentage


@dataclass(frozen=True)
class Record:
    """戦績を表すデータクラス

    Attributes:
        first_count (NonNegativeValue): 先攻数
        second_count (NonNegativeValue): 後攻数
        win_count (NonNegativeValue): 勝利数
        loss_count (NonNegativeValue): 敗北数
        draw_count (NonNegativeValue): 引分数
        first_win_count (NonNegativeValue): 先攻での勝利数
        second_win_count (NonNegativeValue): 後攻での勝利数
    """
    first_count: NonNegativeInt
    second_count: NonNegativeInt
    win_count: NonNegativeInt
    loss_count: NonNegativeInt
    draw_count: NonNegativeInt
    first_win_count: NonNegativeInt
    second_win_count: NonNegativeInt

    def _safe_divide(self,
        numerator: NonNegativeInt,
        denominator: NonNegativeInt
    ) -> float:
        """0 除算を起こさない為の内部ヘルパーメソッド"""
        if denominator.value <= 0:
            return 0.0
        return int(numerator) / int(denominator)

    @property
    def game_count(self) -> NonNegativeInt:
        """この戦績のトータルの試合数"""
        return NonNegativeInt(int(self.first_count) + int(self.second_count))

    @property
    def win_rate(self) -> Percentage:
        """この戦績の勝率"""
        return Percentage.from_ratio(
            self._safe_divide(self.win_count, self.game_count)
        )

    @property
    def first_win_rate(self) -> Percentage:
        """この戦績の先攻での勝率"""
        return Percentage.from_ratio(
            self._safe_divide(self.first_win_count, self.first_count)
        )

    @property
    def second_win_rate(self) -> Percentage:
        """この戦績の後攻での勝率"""
        return Percentage.from_ratio(
            self._safe_divide(self.second_win_count, self.second_count)
        )

    @property
    def first_rate(self) -> Percentage:
        """この戦績における先攻率"""
        return Percentage.from_ratio(
            self._safe_divide(self.first_count, self.game_count)
        )

    @property
    def second_rate(self) -> Percentage:
        """この戦績における後攻率"""
        return Percentage.from_ratio(
            self._safe_divide(self.second_count, self.game_count)
        )
