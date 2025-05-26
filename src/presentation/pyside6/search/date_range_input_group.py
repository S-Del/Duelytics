from datetime import datetime
from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QLineEdit
from typing import ClassVar, Literal

from presentation.pyside6.search import SortByDateRadioGroup


class DateRangeInputGroup(QGroupBox):
    DATE_FORMAT: ClassVar[str] = "yyyy-MM-dd"

    def __init__(self):
        super().__init__("期間 入力")

        label = QLabel("入力が無かった場合は全期間で検索")

        since_label = QLabel("期間開始 年月日")
        self._since_input = QLineEdit()
        self._since_input.setPlaceholderText(DateRangeInputGroup.DATE_FORMAT)

        until_label = QLabel("期間終了 年月日")
        self._until_input = QLineEdit()
        self._until_input.setPlaceholderText(DateRangeInputGroup.DATE_FORMAT)

        self._sort_radio = SortByDateRadioGroup()

        layout = QFormLayout()
        layout.addRow(label)
        layout.addRow(since_label, self._since_input)
        layout.addRow(until_label, self._until_input)
        layout.addRow(self._sort_radio)

        self.setLayout(layout)

    def reset(self):
        self._since_input.setText("")
        self._until_input.setText("")
        self._sort_radio.reset()

    @property
    def since(self) -> str | None:
        since = self._since_input.text().strip()
        if not since:
            return None
        try:
            datetime.strptime(since, "%Y-%m-%d")
        except ValueError:
            return None
        return since

    @property
    def until(self) -> str | None:
        until = self._until_input.text().strip()
        if not until:
            return None
        try:
            datetime.strptime(until, "%Y-%m-%d")
        except ValueError:
            return None
        return until

    @property
    def order_by(self) -> Literal["DESC", "ASC"]:
        return self._sort_radio.order_by
