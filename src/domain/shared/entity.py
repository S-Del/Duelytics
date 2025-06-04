from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Entity(ABC):
    id: UUID = field(
        # True でコンストラクタに渡すことが出来る。
        # デフォルト True だが明示している。
        init=True,
        # コンストラクタに id が渡されなかった場合は uuid4 で生成する。
        default_factory=uuid4,
        # Entity を継承したクラスが独自の属性を持てるように。
        # これを指定しないと、
        # 既定値のないフィールドは、既定値を持つフィールドの後に表示できません
        # というエラーになる
        kw_only=True
    )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.id == self.id

    def __hash__(self) -> int:
        return hash((self.__class__, self.id))
