from dataclasses import dataclass
from uuid import UUID

from domain.shared import Entity


@dataclass(frozen=True, eq=False)
class Note(Entity):
    """ユーザーが入力したメモ等

    試合結果が持つ ID と紐づく

    Attributes:
        _id (UUID):
            試合結果と紐づく ID
        _content (str):
            メモ内容の文字列
    """
    _id: UUID
    _content: str

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def id_raw(self) -> UUID:
        return self._id

    @property
    def content(self) -> str:
        return self._content

    def __str__(self) -> str:
        return "\n".join([
            f"ID: {self.id}",
            f"メモ: {self.content}"
        ])
