from PySide6.QtWidgets import QGroupBox, QTextEdit, QVBoxLayout


class NoteInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("メモ 入力")

        self._text_edit = QTextEdit()
        self._text_edit.setPlaceholderText("特筆事項があれば入力")
        self._text_edit.setTabChangesFocus(True)

        layout = QVBoxLayout()
        layout.addWidget(self._text_edit)

        self.setLayout(layout)

    @property
    def value(self) -> str | None:
        note = self._text_edit.toPlainText().strip()
        if not note:
            return None
        return note

    @value.setter
    def value(self, value: str):
        self._text_edit.setText(value)

    def reset(self):
        self._text_edit.clear()
