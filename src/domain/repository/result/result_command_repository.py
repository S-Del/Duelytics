from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.result import DuelResult
from domain.repository.result import UpdateResultCommand


class ResultCommandRepository(ABC):
    @abstractmethod
    def register(self, result: DuelResult):
        pass

    @abstractmethod
    def update(self, command: UpdateResultCommand):
        pass

    @abstractmethod
    def delete_by_id(self, id: UUID):
        pass
