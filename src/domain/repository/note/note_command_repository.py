from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.note import Note


class NoteCommandRepository(ABC):
    @abstractmethod
    def delete_by_id(self, id: UUID):
        pass

    @abstractmethod
    def register(self, note: Note):
        pass

    @abstractmethod
    def upsert(self, note: Note):
        pass
