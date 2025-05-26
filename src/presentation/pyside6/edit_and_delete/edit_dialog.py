from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from sys import exit

from application.events import EventAggregator
from application.exception import (
    ApplicationCriticalError, ApplicationOperationWarning
)
from application.exception.invalid_command_error import InvalidCommandError
from application.result.edit import EditResultCommand, EditResultScenario
from application.result.fetch.use_case import ResultData
from presentation.events import StatusBarMessageEvent
from presentation.pyside6.shared import (
    DeckNameInputGroup,
    FirstOrSecondRadioGroup,
    ResultRadioGroup,
    NoteInputGroup
)


class EditDialog(QDialog):
    def __init__(self,
        parent: QWidget | None,
        target: ResultData,
        edit_result: EditResultScenario,
        event_aggregator: EventAggregator
    ):
        super().__init__(parent)
        self.setWindowTitle("試合結果 編集")
        self._event_aggregator = event_aggregator
        self._target = target
        self._edit_result = edit_result
        self._first_or_second_group = FirstOrSecondRadioGroup()
        self._first_or_second_group.value = target.first_or_second_raw
        self._result_group = ResultRadioGroup()
        self._result_group.value = target.result_raw
        self._deck_name_group = DeckNameInputGroup()
        self._deck_name_group.my_deck_name = target.my_deck_name
        self._deck_name_group.opponent_deck_name = target.opponent_deck_name
        self._note_group = NoteInputGroup()
        if target.note:
            self._note_group.value = target.note

        form_layout = QGridLayout()
        form_layout.addWidget(self._first_or_second_group, 0, 0)
        form_layout.addWidget(self._result_group, 0, 1)
        form_layout.addWidget(self._deck_name_group, 0, 2)
        form_layout.addWidget(self._note_group, 1, 0, 1, 3)

        self._cancel_button = QPushButton("キャンセル")
        self._cancel_button.clicked.connect(self.reject)
        self._accept_button = QPushButton("続行")
        self._accept_button.clicked.connect(self.on_click_accept_button)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self._cancel_button)
        button_layout.addWidget(self._accept_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_click_accept_button(self):
        try:
            self._edit_result.handle(
                EditResultCommand(
                    self._target.id,
                    self._first_or_second_group.value,
                    self._result_group.value,
                    self._deck_name_group.my_deck_name,
                    self._deck_name_group.opponent_deck_name,
                    self._note_group.value
                )
            )
            QMessageBox.information(self,
                "編集完了", "指定された試合結果の編集が完了しました"
            )
            self.accept()
        except ApplicationOperationWarning as aow:
            self._event_aggregator.publish(
                StatusBarMessageEvent(aow.msg, aow.details)
            )
            self.accept()
        except InvalidCommandError as ice:
            QMessageBox.warning(self,
                "コマンドオブジェクトの作成に失敗", str(ice)
            )
            self.reject()
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "データベースエラー", str(ae))
            exit(1)
