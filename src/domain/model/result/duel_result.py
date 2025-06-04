from dataclasses import dataclass, replace
from datetime import datetime

from domain.shared import Entity
from domain.shared.unit import NonEmptyStr
from . import FirstOrSecond, ResultChar


# eq=False をしておかないと Entity で実装した __eq__ が上書きされてしまう
@dataclass(frozen=True, eq=False)
class DuelResult(Entity):
    """1 試合の結果を表すエンティティ

    Attributes:
        id (UUID):
            親クラス Entity から継承される UUID。
        registered_at (datetime):
            試合結果が登録された日時
        first_or_second (FirstOrSecond):
            先攻なら 'F'、後攻なら 'S'
        result (ResultChar):
            試合結果を表す。勝利なら 'W'、敗北なら 'L'、引分なら 'D'。
        my_deck_name (NonEmptyStr):
            自分が使用したデッキ名
        opponent_deck_name (NonEmptyStr):
            対戦相手が使用したデッキ名
        memo (NonEmptyStr | None):
            メモ
    """
    registered_at: datetime
    first_or_second: FirstOrSecond
    result: ResultChar
    my_deck_name: NonEmptyStr
    opponent_deck_name: NonEmptyStr
    memo: NonEmptyStr | None = None

    def update(self,
        first_or_second: FirstOrSecond,
        result: ResultChar,
        my_deck_name: NonEmptyStr,
        opponent_deck_name: NonEmptyStr,
        memo: NonEmptyStr | None
    ) -> "DuelResult":
        return replace(
            self,
            first_or_second=first_or_second,
            result=result,
            my_deck_name=my_deck_name,
            opponent_deck_name=opponent_deck_name,
            memo=memo
        )
