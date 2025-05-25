from typing import Literal
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QVBoxLayout

from presentation.pyside6.shared import RadioButtonWithStrValue


VALID_RADIO_VALUE = Literal['W', 'L', 'D']


class ResultRadioGroup(QGroupBox):
    def __init__(self):
        super().__init__("試合結果 選択")

        self._win_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE]("勝利", 'W')
        self._win_radio.setChecked(True)
        self._loss_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE]("敗北", 'L')
        self._draw_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE]("引分", 'D')
        self._button_group = QButtonGroup()
        self._button_group.addButton(self._win_radio)
        self._button_group.addButton(self._loss_radio)
        self._button_group.addButton(self._draw_radio)

        layout = QVBoxLayout()
        layout.addWidget(self._win_radio)
        layout.addWidget(self._loss_radio)
        layout.addWidget(self._draw_radio)
        self.setLayout(layout)

    @property
    def value(self) -> VALID_RADIO_VALUE:
        checked_button = self._button_group.checkedButton()
        if not isinstance(checked_button, RadioButtonWithStrValue):
            raise TypeError("ラジオボタンの型が不正")
        return checked_button._value

    @value.setter
    def value(self, value: VALID_RADIO_VALUE):
        if value == 'W':
            self._win_radio.setChecked(True)
            return
        if value == 'L':
            self._loss_radio.setChecked(True)
            return
        if value == 'D':
            self._draw_radio.setChecked(True)
            return
        raise ValueError(f"指定された値が不正: {value}")

    def reset(self):
        self._button_group.buttons()[0].setChecked(True)
