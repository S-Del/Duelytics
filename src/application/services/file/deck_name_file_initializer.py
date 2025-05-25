from abc import ABC, abstractmethod


class IDeckNameFileInitializer(ABC):
    @abstractmethod
    def execute(self):
        pass
