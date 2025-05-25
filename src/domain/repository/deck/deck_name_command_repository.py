from abc import ABC, abstractmethod

from domain.shared.unit import NonEmptyStr


class DeckNameCommandRepository(ABC):
    @abstractmethod
    def add(self, name: NonEmptyStr):
        pass
