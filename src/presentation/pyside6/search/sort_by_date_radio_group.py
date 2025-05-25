from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget
)
from typing import Literal

from presentation.pyside6.shared import RadioButtonWithStrValue


VALID_RADIO_VALUE = Literal["DESC", "ASC"]


class SortByDateRadioGroup(QWidget):
    def __init__(self):
        super().__init__()
        radio_group_label = QLabel("検索結果の並び順を指定")

        radio_group = QWidget()
        desc_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "新しい順", "DESC"
        )
        desc_radio.setChecked(True)
        asc_radio = RadioButtonWithStrValue[VALID_RADIO_VALUE](
            "古い順", "ASC"
        )
        self._radio_group = QButtonGroup()
        self._radio_group.addButton(desc_radio)
        self._radio_group.addButton(asc_radio)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(desc_radio)
        radio_layout.addWidget(asc_radio)
        radio_group.setLayout(radio_layout)

        layout = QVBoxLayout()
        layout.addWidget(radio_group_label)
        layout.addWidget(radio_group)

        self.setLayout(layout)

    @property
    def order_by(self) -> VALID_RADIO_VALUE:
        checked = self._radio_group.checkedButton()
        if not isinstance(checked, RadioButtonWithStrValue):
            raise TypeError("ラジオボタンの型が不正")
        return checked.value

    def reset(self):
        self._radio_group.buttons()[0].setChecked(True)
