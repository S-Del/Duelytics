from dataclasses import dataclass
from uuid import UUID

from application.exception import InvalidCommandError


@dataclass(frozen=True)
class IdForResult:
    id: str

    def __post_init__(self):
        try:
            self._validate_id()
        except ValueError as ve:
            raise InvalidCommandError(
                f"コマンドオブジェクトの作成に失敗: {ve}"
            ) from ve

    def _validate_id(self):
        try:
            UUID(self.id)
        except ValueError as ve:
            raise ValueError(f"ID 文字列の指定が不正") from ve

    @property
    def uuid(self) -> UUID:
        # このオブジェクトのインスタンス化時にバリデーション済みなので
        # ここで ValueError を把捉する必要は無い。
        return UUID(self.id)
