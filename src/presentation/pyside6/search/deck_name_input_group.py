from injector import inject
from PySide6.QtCore import QStringListModel, Qt, Signal
from PySide6.QtWidgets import (
    QCompleter, QFormLayout, QGroupBox, QLabel, QLineEdit
)
from typing import ClassVar, Literal, Sequence

from presentation.pyside6.shared import OnFocusEventFilter
from . import SearchTypeRadioGroup


class DeckNameInputGroup(QGroupBox):
    """デッキ名を指定して検索するための入力要素をまとめたグループ

    shared/ 内にも同名のクラスがあるが、
    あちらは「自分のデッキ名」の入力が必須となっており、
    「登録」「編集」の際に利用することを想定している。
    「検索」では自分のデッキ名の入力は必須では無い。
    """
    deck_input_focused: ClassVar[Signal] = Signal()

    def __init__(self):
        super().__init__("デッキ名 入力")

        label = QLabel("入力しなかった場合は全てのデッキ名で検索")

        self.list_model = QStringListModel()
        completer = QCompleter(self.list_model)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)

        my_deck_label = QLabel("自分のデッキ名")
        self.my_deck_input = QLineEdit()
        self.my_deck_input.setCompleter(completer)
        self.my_deck_focused_filter = OnFocusEventFilter(
            self.emit_deck_input_focused, self
        )
        self.my_deck_input.installEventFilter(self.my_deck_focused_filter)
        self.my_deck_search_type_radio = SearchTypeRadioGroup()

        opponent_deck_label = QLabel("相手のデッキ名")
        self.opponent_deck_input = QLineEdit()
        self.opponent_deck_input.setCompleter(completer)
        self.opponent_deck_focused_filter = OnFocusEventFilter(
            self.emit_deck_input_focused, self
        )
        self.opponent_deck_input.installEventFilter(
            self.opponent_deck_focused_filter
        )
        self.opponent_deck_search_type_radio = SearchTypeRadioGroup()

        layout = QFormLayout()
        layout.addRow(label)
        layout.addRow(my_deck_label, self.my_deck_input)
        layout.addRow(self.my_deck_search_type_radio)
        layout.addRow(opponent_deck_label, self.opponent_deck_input)
        layout.addRow(self.opponent_deck_search_type_radio)

        self.setLayout(layout)

    @property
    def my_deck_name(self) -> str | None:
        deck_name = self.my_deck_input.text().strip()
        if not deck_name:
            return None
        return deck_name

    @property
    def my_deck_search_type(self) -> Literal[
        "exact", "partial", "prefix", "suffix"
    ]:
        return self.my_deck_search_type_radio.value

    @property
    def opponent_deck_name(self) -> str | None:
        deck_name = self.opponent_deck_input.text().strip()
        if not deck_name:
            return None
        return deck_name

    @property
    def opponent_deck_search_type(self) -> Literal[
        "exact", "partial", "prefix", "suffix"
    ]:
        return self.opponent_deck_search_type_radio.value

    def reset(self):
        self.my_deck_input.setText("")
        self.opponent_deck_input.setText("")
        self.my_deck_search_type_radio.reset()
        self.opponent_deck_search_type_radio.reset()

    def update_completer_deck_list(self, deck_names: Sequence[str]):
        self.list_model.setStringList(deck_names)

    def emit_deck_input_focused(self):
        self.deck_input_focused.emit()
