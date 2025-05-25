from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QLabel, QLineEdit, QVBoxLayout


class IdInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("ID 入力")

        label = QLabel("入力があった場合は他の検索条件は無視される")
        self._input = QLineEdit()
        self._input.setPlaceholderText("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
        # Completer を導入するべきかどうか
        # ID なら手入力せずにコピペするはず？？

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        layout.addWidget(self._input)

        self.setLayout(layout)

    @property
    def id(self) -> str | None:
        id = self._input.text().strip()
        if not id:
            return None
        return id

    def reset(self):
        self._input.setText("")
