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

from application.exception import ApplicationCriticalError
from application.result.edit import EditResultCommand, EditResultScenario
from application.result.fetch.use_case import FetchResultData
from presentation.pyside6.shared import (
    DeckNameInputGroup,
    FirstOrSecondRadioGroup,
    ResultRadioGroup,
    NoteInputGroup
)


class EditDialog(QDialog):
    def __init__(self,
        parent: QWidget | None,
        target: FetchResultData,
        edit_result: EditResultScenario
    ):
        super().__init__(parent)
        self.setWindowTitle("試合結果 編集")

        self.target = target
        self.edit_result = edit_result
        self.first_or_second_group = FirstOrSecondRadioGroup()
        self.first_or_second_group.value = target.first_or_second_raw
        self.result_group = ResultRadioGroup()
        self.result_group.value = target.result_raw
        self.deck_name_group = DeckNameInputGroup()
        self.deck_name_group.my_deck_name = target.my_deck_name
        self.deck_name_group.opponent_deck_name = target.opponent_deck_name
        self.note_group = NoteInputGroup()
        if target.note:
            self.note_group.value = target.note

        form_layout = QGridLayout()
        form_layout.addWidget(self.first_or_second_group, 0, 0)
        form_layout.addWidget(self.result_group, 0, 1)
        form_layout.addWidget(self.deck_name_group, 0, 2)
        form_layout.addWidget(self.note_group, 1, 0, 1, 3)

        self.cancel_button = QPushButton("キャンセル")
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button = QPushButton("続行")
        self.accept_button.clicked.connect(self.on_click_accept_button)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.accept_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_click_accept_button(self):
        try:
            self.edit_result.handle(
                EditResultCommand(
                    self.target.id,
                    self.first_or_second_group.value,
                    self.result_group.value,
                    self.deck_name_group.my_deck_name,
                    self.deck_name_group.opponent_deck_name,
                    self.note_group.value
                )
            )
        except ValueError as ve:
            QMessageBox.warning(self, "値が不正", str(ve))
            self.reject()
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "データベースエラー", str(ae))
            exit(1)

        QMessageBox.information(self,
            "編集完了", "指定された試合結果の編集が完了しました"
        )
        self.accept()
