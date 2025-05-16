from dataclasses import dataclass
from datetime import datetime

from domain.shared import Entity
from . import FirstOrSecond, FirstOrSecondJP, ResultChar, ResultStringJP


# eq=False をしておかないと Entity で実装した __eq__ が上書きされてしまう
@dataclass(frozen=True, eq=False)
class DuelResult(Entity):
    """1 試合の結果を表すデータクラス

    Attributes:
        _id (UUID):
            親クラス Entity から継承される UUID。
        _registerd_at (datetime):
            試合結果が登録された日時
        _first_or_second (FirstOrSecond):
            先攻なら 'F'、後攻なら 'S'
        _result (ResultChar):
            試合結果を表す。勝利なら 'W'、敗北なら 'L'、引分なら 'D'。
        _my_deck_name (str):
            自分が使用したデッキ名
        _opponent_deck_name (str):
            対戦相手が使用したデッキ名
        _note (str | None):
            メモ等
    """
    _registered_at: datetime
    _first_or_second: FirstOrSecond
    _result: ResultChar
    _my_deck_name: str
    _opponent_deck_name: str
    _note: str | None = None

    @property
    def registered_at(self) -> str:
        return self._registered_at.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def registered_at_raw(self) -> datetime:
        return self._registered_at

    @property
    def registered_at_isoformat(self, timespec="seconds") -> str:
        return self._registered_at.isoformat(timespec=timespec)

    @property
    def first_or_second(self) -> FirstOrSecondJP:
        return FirstOrSecondJP[self._first_or_second.value]

    @property
    def first_or_second_raw(self) -> FirstOrSecond:
        return self._first_or_second

    @property
    def result(self) -> ResultStringJP:
        return ResultStringJP[self._result.value]

    @property
    def result_raw(self) -> ResultChar:
        return self._result

    @property
    def my_deck_name(self) -> str:
        return self._my_deck_name

    @property
    def opponent_deck_name(self) -> str:
        return self._opponent_deck_name

    @property
    def note(self) -> str:
        return self._note or ""

    def __str__(self) -> str:
        return "\n".join([
            f"ID: {self.id}",
            f"登録日時: {self.registered_at}",
            f"先/後: {self.first_or_second.value}",
            f"試合結果: {self.result.value}",
            f"自分のデッキ名: {self.my_deck_name}",
            f"相手のデッキ名: {self.opponent_deck_name}",
            f"メモ: {self.note}"
        ])
