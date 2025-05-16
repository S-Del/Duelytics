from injector import inject
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QGridLayout, QMessageBox, QWidget
from sys import exit
from typing import ClassVar

from application.deck.fetch.use_case import FetchAllDeckName
from application.exception import (
    ApplicationCriticalError, InvalidCommandError
)
from application.result.register import (
    RegisterResultCommand, RegisterResultScenario
)
from presentation.pyside6.shared import (
    FirstOrSecondRadioGroup,
    ResultRadioGroup,
    DeckNameInputGroup,
    NoteInputGroup
)
from . import ControlButtonGroup


class Tab(QWidget):
    TITLE: ClassVar[str] = "登録"

    @inject
    def __init__(self,
        register_result: RegisterResultScenario,
        fetch_all_deck_name: FetchAllDeckName
    ):
        super().__init__()

        self.register_result_scenario = register_result
        self.fetch_all_deck_name = fetch_all_deck_name

        self.first_or_second_radio_group = FirstOrSecondRadioGroup()
        self.result_radio_group = ResultRadioGroup()

        self.deck_name_input_group = DeckNameInputGroup()
        self.deck_name_input_group.deck_input_focused.connect(
            self.update_completer_deck_list
        )
        self.update_completer_deck_list()

        self.note_input_group = NoteInputGroup()
        self.control_button_group = ControlButtonGroup(
            self.on_click_register_button,
            self.on_click_clear_button
        )
        register_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        register_shortcut.activated.connect(self.on_click_register_button)

        layout = QGridLayout()
        layout.addWidget(self.first_or_second_radio_group, 0, 0)
        layout.addWidget(self.result_radio_group, 0, 1)
        layout.addWidget(self.deck_name_input_group, 0, 2)
        layout.addWidget(self.note_input_group, 1, 0, 1, 3)
        layout.addWidget(self.control_button_group, 2, 0, 1, 3)

        self.setLayout(layout)

    def update_completer_deck_list(self):
        try:
            deck_names = self.fetch_all_deck_name.handle()
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "アプリケーションエラー", str(ae))
            exit(1)
        self.deck_name_input_group.update_completer_deck_list(
            tuple(deck_names)
        )

    def on_click_clear_button(self):
        self.first_or_second_radio_group.reset()
        self.result_radio_group.reset()
        self.deck_name_input_group.reset()
        self.note_input_group.reset()

    def on_click_register_button(self):
        try:
            self.deck_name_input_group.validate()
        except ValueError as ae:
            QMessageBox.warning(self, "未入力項目", str(ae))
            return

        try:
            self.register_result_scenario.execute(
                RegisterResultCommand(
                    self.first_or_second_radio_group.value,
                    self.result_radio_group.value,
                    self.deck_name_input_group.my_deck_name,
                    self.deck_name_input_group.opponent_deck_name,
                    self.note_input_group.value
                )
            )
        except InvalidCommandError as ice:
            QMessageBox.warning(self, "入力エラー", str(ice))
            return
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "アプリケーションエラー", str(ae))
            exit(1)

        self.update_completer_deck_list()

        QMessageBox.information(self,
            "登録完了", "試合結果の登録が完了しました"
        )
        self.on_click_clear_button()
