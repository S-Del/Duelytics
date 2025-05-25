from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGroupBox, QVBoxLayout, QLabel
from typing import Literal


class ResultCheckboxGroup(QGroupBox):
    def __init__(self):
        super().__init__("試合結果 選択")

        label = QLabel("選択しなかった場合は全ての試合結果で検索")
        self._is_win_checkbox = QCheckBox("勝利")
        self._is_loss_checkbox = QCheckBox("敗北")
        self._is_draw_checkbox = QCheckBox("引分")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        layout.addWidget(self._is_win_checkbox)
        layout.addWidget(self._is_loss_checkbox)
        layout.addWidget(self._is_draw_checkbox)

        self.setLayout(layout)

    @property
    def values(self) -> tuple[Literal['W', 'L', 'D'], ...]:
        values: list[Literal['W', 'L', 'D']] = []
        if self._is_win_checkbox.isChecked():
            values.append('W')
        if self._is_loss_checkbox.isChecked():
            values.append('L')
        if self._is_draw_checkbox.isChecked():
            values.append('D')
        return tuple(values)

    def reset(self):
        self._is_win_checkbox.setChecked(False)
        self._is_loss_checkbox.setChecked(False)
        self._is_draw_checkbox.setChecked(False)
