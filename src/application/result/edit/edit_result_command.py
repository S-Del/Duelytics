from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from application.exception import InvalidCommandError


@dataclass(frozen=True)
class EditResultCommand:
    id: str
    first_or_second: Literal['F', 'S']
    result: Literal['W', 'L', 'D']
    my_deck_name: str
    opponent_deck_name: str = "不明"
    memo: str | None = None

    def __post_init__(self):
        try:
            self._validate_id()
            self._validate_my_deck_name()
            self._validate_opponent_deck_name()
            self._validate_note()
        except ValueError as ve:
            raise InvalidCommandError(
                f"コマンドオブジェクトの作成に失敗 {ve}"
            ) from ve

    def _validate_id(self):
        try:
            UUID(self.id)
        except ValueError as ve:
            raise ValueError(f"ID 指定の文字列が不正: {self.id}") from ve

    def _validate_my_deck_name(self):
        # 自分のデッキ名に None や空文字列は認めない、つまり必須項目である。
        if not self.my_deck_name.strip():
            raise ValueError(f"デッキ名が不正: {self.my_deck_name}")

    def _validate_opponent_deck_name(self):
        # 入力があるのに、空文字列や空白のみの意味の無い文字列場合は認めない。
        if not self.opponent_deck_name.strip():
            raise ValueError(f"相手のデッキ名が空か空白文字のみ")

    def _validate_note(self):
        # 任意の入力項目なので None は許される
        if self.memo is None:
            return
        # 入力があるのに、空文字列や空白のみの意味の無い文字列場合は認めない。
        if not self.memo.strip():
            raise ValueError(f"メモの内容が不正: {self.memo}")
