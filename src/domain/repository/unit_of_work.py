from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from types import TracebackType
from typing import TypeVar


Self = TypeVar("Self", bound="UnitOfWork")


class UnitOfWork(AbstractContextManager[Self], ABC):
    """コネクション取得や、トランザクション管理を行うクラス。"""

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None:
        pass
