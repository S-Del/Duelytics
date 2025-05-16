from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.note import Note
from domain.repository import UnitOfWork


class NoteCommandRepository(ABC):
    @property
    @abstractmethod
    def uow(self) -> UnitOfWork:
        pass

    @abstractmethod
    def delete_by_id(self, id: UUID):
        pass

    @abstractmethod
    def register(self, note: Note):
        pass

    @abstractmethod
    def upsert(self, note: Note):
        pass
