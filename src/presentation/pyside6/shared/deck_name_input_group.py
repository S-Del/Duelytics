from typing import ClassVar, Sequence
from injector import inject
from PySide6.QtCore import QStringListModel, Qt, Signal
from PySide6.QtWidgets import (
    QCompleter, QFormLayout, QGroupBox, QLabel, QLineEdit
)

from . import OnFocusEventFilter


class DeckNameInputGroup(QGroupBox):
    # インプット要素にフォーカスが当たった時のシグナル
    deck_input_focused: ClassVar[Signal] = Signal()

    @inject
    def __init__(self):
        super().__init__("デッキ名 入力")

        self.list_model = QStringListModel()
        completer = QCompleter(self.list_model)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)

        my_deck_label = QLabel("自分のデッキ名 (必須)")
        self.my_deck_input = QLineEdit()
        self.my_deck_input.setCompleter(completer)
        self.my_deck_focused_filter = OnFocusEventFilter(
            self.emit_deck_input_focused, self
        )
        self.my_deck_input.installEventFilter(self.my_deck_focused_filter)

        opponent_deck_label = QLabel("相手のデッキ名")
        self.opponent_deck_input = QLineEdit()
        self.opponent_deck_input.setCompleter(completer)
        self.opponent_deck_focused_filter = OnFocusEventFilter(
            self.emit_deck_input_focused, self
        )
        self.opponent_deck_input.installEventFilter(
            self.opponent_deck_focused_filter
        )

        layout = QFormLayout()
        layout.addRow(my_deck_label, self.my_deck_input)
        layout.addRow(opponent_deck_label, self.opponent_deck_input)

        self.setLayout(layout)

    @property
    def my_deck_name(self) -> str:
        return self.my_deck_input.text().strip()

    @my_deck_name.setter
    def my_deck_name(self, value: str):
        self.my_deck_input.setText(value)

    @property
    def opponent_deck_name(self) -> str:
        deck_name = self.opponent_deck_input.text()
        return deck_name.strip() or "不明"

    @opponent_deck_name.setter
    def opponent_deck_name(self, value: str):
        self.opponent_deck_input.setText(value)

    @property
    def deck_names(self) -> tuple[str, str]:
        return self.my_deck_name, self.opponent_deck_name

    def reset(self):
        self.opponent_deck_input.setText("")

    def update_completer_deck_list(self, deck_names: Sequence[str]):
        self.list_model.setStringList(deck_names)

    def validate(self):
        if not self.my_deck_name:
            raise ValueError("自分のデッキ名が入力されていません")

    def emit_deck_input_focused(self):
        self.deck_input_focused.emit()
