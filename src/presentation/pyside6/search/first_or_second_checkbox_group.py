from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGroupBox, QVBoxLayout, QLabel
from typing import Literal


class FirstOrSecondCheckboxGroup(QGroupBox):
    def __init__(self):
        super().__init__("先/後 選択")

        label = QLabel("選択しなかった場合は両方の結果を検索")
        self.is_first_checkbox = QCheckBox("先攻")
        self.is_second_checkbox = QCheckBox("後攻")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        layout.addWidget(self.is_first_checkbox)
        layout.addWidget(self.is_second_checkbox)

        self.setLayout(layout)

    @property
    def values(self) -> tuple[Literal['F', 'S'], ...]:
        values: list[Literal['F', 'S']] = []
        if self.is_first_checkbox.isChecked():
            values.append('F')
        if self.is_second_checkbox.isChecked():
            values.append('S')
        return tuple(values)

    def reset(self):
        self.is_first_checkbox.setChecked(False)
        self.is_second_checkbox.setChecked(False)
