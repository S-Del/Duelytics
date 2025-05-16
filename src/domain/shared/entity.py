from abc import ABC
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Entity(ABC):
    _id: UUID

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def id_raw(self) -> UUID:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other._id == self._id

    def __hash__(self) -> int:
        return hash((self.__class__, self._id))
