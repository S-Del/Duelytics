from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.note import Note


class NoteQueryRepository(ABC):
    @abstractmethod
    def search_by_id(self, id: UUID) -> Note | None:
        pass
