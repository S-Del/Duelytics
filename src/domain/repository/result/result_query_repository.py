from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.result import DuelResult
from . import SearchResultsQuery


class ResultQueryRepository(ABC):
    @abstractmethod
    def search_by_id(self, id: UUID) -> DuelResult | None:
        pass

    @abstractmethod
    def search(self, query: SearchResultsQuery) -> tuple[DuelResult]:
        pass
