from dataclasses import dataclass
from datetime import datetime

from domain.shared import Entity
from domain.shared.unit import NonEmptyStr
from . import FirstOrSecond, ResultChar

# eq=False をしておかないと Entity で実装した __eq__ が上書きされてしまう
@dataclass(frozen=True, eq=False)
class DuelResult(Entity):
    """1 試合の結果を表すデータクラス

    Attributes:
        id (UUID):
            親クラス Entity から継承される UUID。
        registerd_at (datetime):
            試合結果が登録された日時
        first_or_second (FirstOrSecond):
            先攻なら 'F'、後攻なら 'S'
        result (ResultChar):
            試合結果を表す。勝利なら 'W'、敗北なら 'L'、引分なら 'D'。
        my_deck_name (str):
            自分が使用したデッキ名
        opponent_deck_name (str):
            対戦相手が使用したデッキ名
        note (str | None):
            メモ等
    """
    registered_at: datetime
    first_or_second: FirstOrSecond
    result: ResultChar
    my_deck_name: NonEmptyStr
    opponent_deck_name: NonEmptyStr
    note: str | None = None

    @property
    def registered_at_isoformat(self, timespec="seconds") -> str:
        return self.registered_at.isoformat(timespec=timespec)
