from dataclasses import dataclass

from domain.shared.unit import NonEmptyStr, PositiveInt, Percentage


@dataclass(frozen=True, eq=False)
class EncounteredDeckStats:
    """1 回以上対戦した相手デッキを表すデータクラス"""

    name: NonEmptyStr
    count: PositiveInt
    encounter_rate: Percentage

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.name == self.name

    def __hash__(self) -> int:
        return hash((self.__class__, self.name))
