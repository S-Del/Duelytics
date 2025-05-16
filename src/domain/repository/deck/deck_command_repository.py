from abc import ABC, abstractmethod


class DeckCommandRepository(ABC):
    @abstractmethod
    def register_all(self, *names: str):
        pass

    @abstractmethod
    def register(self, name:str):
        pass
