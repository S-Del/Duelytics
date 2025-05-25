from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QWidget
from typing import Literal

from presentation.pyside6.shared import RadioButtonWithStrValue


VALID_RADIO_VALUE = Literal["exact", "partial", "prefix", "suffix"]


class SearchTypeRadioGroup(QWidget):
    def __init__(self):
        super().__init__()

        exact_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "完全一致", "exact"
        )
        exact_radio.setChecked(True)
        partial_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "部分一致", "partial"
        )
        prefix_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "前方一致", "prefix"
        )
        suffix_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "後方一致", "suffix"
        )
        self._button_group = QButtonGroup()
        self._button_group.addButton(exact_radio)
        self._button_group.addButton(partial_radio)
        self._button_group.addButton(prefix_radio)
        self._button_group.addButton(suffix_radio)
        layout = QHBoxLayout()
        layout.addWidget(exact_radio)
        layout.addWidget(partial_radio)
        layout.addWidget(prefix_radio)
        layout.addWidget(suffix_radio)

        self.setLayout(layout)

    @property
    def value(self) -> VALID_RADIO_VALUE:
        checked = self._button_group.checkedButton()
        if not isinstance(checked, RadioButtonWithStrValue):
            raise TypeError("ラジオボタンの型が不正")
        return checked._value

    def reset(self):
        self._button_group.buttons()[0].setChecked(True)
