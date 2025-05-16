from PySide6.QtCore import Qt
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QVBoxLayout
from typing import Literal

from presentation.pyside6.shared import RadioButtonWithStrValue


VALID_RADIO_VALUE = Literal['F', 'S']


class FirstOrSecondRadioGroup(QGroupBox):
    def __init__(self):
        super().__init__("先/後 選択")

        self.first_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "先攻", 'F'
        )
        self.first_radio.setChecked(True)
        self.second_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "後攻", 'S'
        )
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.first_radio)
        self.button_group.addButton(self.second_radio)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.first_radio)
        layout.addWidget(self.second_radio)
        self.setLayout(layout)

    @property
    def value(self) -> VALID_RADIO_VALUE:
        checked_button = self.button_group.checkedButton()
        if not isinstance(checked_button, RadioButtonWithStrValue):
            raise TypeError("ラジオボタンの型が不正")
        return checked_button.value

    @value.setter
    def value(self, value: VALID_RADIO_VALUE):
        if value == 'F':
            self.first_radio.setChecked(True)
            return
        if value == 'S':
            self.second_radio.setChecked(True)
            return
        raise ValueError(f"指定された値が不正: {value}")

    def reset(self):
        self.button_group.buttons()[0].setChecked(True)
