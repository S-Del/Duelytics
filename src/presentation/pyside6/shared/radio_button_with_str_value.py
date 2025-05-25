from typing import Generic, TypeVar

from PySide6.QtWidgets import (
    QRadioButton,
)


T = TypeVar('T')


class RadioButtonWithStrValue(QRadioButton, Generic[T]):
    def __init__(self, label: str, value: T):
        super().__init__()

        self.setText(label)
        self._value = value

    @property
    def value(self) -> T:
        return self._value
