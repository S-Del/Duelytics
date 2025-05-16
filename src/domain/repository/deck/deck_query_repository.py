from abc import ABC, abstractmethod


class DeckQueryRepository(ABC):
    @abstractmethod
    def exists(self, deck_name: str) -> bool:
        pass

    @abstractmethod
    def fetch_all(self) -> frozenset[str]:
        pass
