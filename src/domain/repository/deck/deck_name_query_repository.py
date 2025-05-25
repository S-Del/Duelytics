from abc import ABC, abstractmethod

from domain.shared.unit import NonEmptyStr


class DeckNameQueryRepository(ABC):
    @abstractmethod
    def exists(self, name: NonEmptyStr) -> bool:
        pass

    @abstractmethod
    def read_all(self) -> set[NonEmptyStr]:
        pass
