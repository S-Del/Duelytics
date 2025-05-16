from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(ABC, Generic[T]):
    _value: T

    @property
    def value(self) -> T:
        try:
            return deepcopy(self._value)
        except:
            return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other._value == self._value

    def __hash__(self) -> int:
        return hash((self.__class__, self._value))

    def __post_init__(self):
        self.validate(self._value)

    def validate(self, value: T):
        pass
