from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QLineEdit
from re import split


class KeywordInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("キーワード 指定")

        label = QLabel("メモに入力されたキーワードが記入された試合のみ検索")
        self._line_edit = QLineEdit()

        # ToDo: 実装後に削除
        self._line_edit.setPlaceholderText("未実装")
        self._line_edit.setDisabled(True)

        layout = QFormLayout()
        layout.addRow(label)
        layout.addRow(self._line_edit)

        self.setLayout(layout)

    @property
    def values(self) -> tuple[str, ...]:
        text = self._line_edit.text().strip()
        if not text:
            return ()
        values = split(r"\s+", text)
        return tuple(values)

    def reset(self):
        self._line_edit.setText("")
