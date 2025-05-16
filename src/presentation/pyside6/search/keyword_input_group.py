from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QLineEdit
from re import split


class KeywordInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("キーワード 入力")

        label = QLabel("入力されたキーワードがメモに記入された試合のみ検索")
        self.line_edit = QLineEdit()

        # ToDo: 実装後に削除
        self.line_edit.setPlaceholderText("未実装")
        self.line_edit.setDisabled(True)

        layout = QFormLayout()
        layout.addRow(label)
        layout.addRow(self.line_edit)

        self.setLayout(layout)

    @property
    def values(self) -> tuple[str, ...]:
        text = self.line_edit.text().strip()
        if not text:
            return ()
        values = split(r"\s+", text)
        return tuple(values)

    def reset(self):
        self.line_edit.setText("")
