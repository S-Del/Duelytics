from injector import inject
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from sys import exit
from typing import ClassVar

from application.events import EventAggregator
from application.exception import ApplicationCriticalError, InvalidCommandError
from application.result import IdForResult
from application.result.delete.use_case import DeleteResultById
from application.result.edit import EditResultScenario
from application.result.fetch.use_case import FetchResultData, FetchResultById
from . import EditDialog


class Tab(QWidget):
    TITLE: ClassVar[str] = "編集・削除"

    @inject
    def __init__(self,
        event_aggregator: EventAggregator,
        fetch_result_by_id: FetchResultById,
        delete_result_by_id: DeleteResultById,
        edit_result: EditResultScenario,
    ):
        super().__init__()
        self._event_aggregator = event_aggregator
        self.fetch_result_by_id = fetch_result_by_id
        self.delete_result_by_id = delete_result_by_id
        self.edit_result = edit_result
        self.target: FetchResultData | None = None

        label = QLabel("ID (必須)")
        self.input = QLineEdit()
        self.input.setPlaceholderText("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
        search_button = QPushButton("対象指定")
        search_button.clicked.connect(self.on_click_search_button)
        form_layout = QHBoxLayout()
        form_layout.addWidget(label)
        form_layout.addWidget(self.input, 1)
        form_layout.addWidget(search_button)

        control_button_group = QGroupBox("操作")
        self.delete_button = QPushButton("削除💀")
        self.delete_button.clicked.connect(self.on_click_delete_button)
        self.delete_button.setEnabled(False)
        self.edit_button = QPushButton("編集")
        self.edit_button.clicked.connect(self.on_click_edit_button)
        self.edit_button.setEnabled(False)

        button_group_layout = QHBoxLayout()
        button_group_layout.addStretch(1)
        button_group_layout.addWidget(self.delete_button)
        button_group_layout.addStretch(1)
        button_group_layout.addWidget(self.edit_button)
        button_group_layout.addStretch(1)
        control_button_group.setLayout(button_group_layout)

        self.search_result_group = QGroupBox()
        self.search_result_group.setVisible(False)
        self.target_id = QLabel()
        self.target_registered_at = QLabel()
        self.target_first_or_second = QLabel()
        self.target_result = QLabel()
        self.target_my_deck_name = QLabel()
        self.target_opponent_deck_name = QLabel()
        self.target_note = QLabel()
        search_result_layout = QFormLayout()
        search_result_layout.addRow(QLabel("ID:"), self.target_id)
        search_result_layout.addRow(
            QLabel("登録日時:"), self.target_registered_at
        )
        search_result_layout.addRow(
            QLabel("先/後:"), self.target_first_or_second
        )
        search_result_layout.addRow(QLabel("試合結果:"), self.target_result)
        search_result_layout.addRow(
            QLabel("自分のデッキ名"), self.target_my_deck_name
        )
        search_result_layout.addRow(
            QLabel("相手のデッキ名"), self.target_opponent_deck_name
        )
        search_result_layout.addRow(QLabel("メモ:"), self.target_note)
        self.search_result_group.setLayout(search_result_layout)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.search_result_group)
        layout.addWidget(control_button_group)
        layout.addStretch(1)

        self.setLayout(layout)

    def reset(self):
        self.target = None
        self.input.setText("")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.search_result_group.setVisible(False)

    def on_click_search_button(self):
        """編集、削除の両方で使用する、ID による試合結果検索用メソッド。

        検索結果は self.target に格納され、編集や削除に利用される。
        """
        inputed_id = self.input.text().strip()
        if not inputed_id:
            QMessageBox.warning(self, "未入力項目", "ID を入力してください")
            return

        try:
            id_for_result = IdForResult(inputed_id)
            target = self.fetch_result_by_id.handle(id_for_result)
        except InvalidCommandError as ice:
            QMessageBox.warning(self, "コマンド実行エラー", str(ice))
            return
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "データベースエラー", str(ae))
            exit(1)

        if not target:
            QMessageBox.warning(self,
                "対象無し",
                "指定された ID の試合結果が存在しませんでした"
            )
            self.reset()
            return

        self.target = target
        self.target_id.setText(target.id)
        self.target_registered_at.setText(target.registered_at)
        self.target_first_or_second.setText(target.first_or_second)
        self.target_result.setText(target.result)
        self.target_my_deck_name.setText(target.my_deck_name)
        self.target_opponent_deck_name.setText(target.opponent_deck_name)
        self.target_note.setText(target.note or "")

        self.search_result_group.setVisible(True)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def on_click_edit_button(self):
        if not self.target:
            QMessageBox.warning(self,
                "対象無し",
                "編集対象が指定されていません"
            )
            self.reset()
            return
        dialog = EditDialog(
            self, self.target, self.edit_result, self._event_aggregator
        )
        dialog.exec()
        self.reset()

    def on_click_delete_button(self):
        if not self.target:
            QMessageBox.warning(self,
                "対象無し",
                "削除対象が指定されていません"
            )
            self.reset()
            return

        reply = QMessageBox.warning(self,
            "注意",
            "この試合結果を削除しますか？\nこの操作は取り消せません。",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Cancel
        )
        if reply != QMessageBox.StandardButton.Ok:
            QMessageBox.information(self, "削除中止", "削除を中止しました")
            self.reset()
            return

        try:
            id_for_result = IdForResult(self.target.id)
            self.delete_result_by_id.handle(id_for_result)
        except InvalidCommandError as ice:
            QMessageBox.warning(self, "コマンド実行エラー", str(ice))
            return
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "データベースエラー", str(ae))
            exit(1)

        QMessageBox.information(self, "削除完了", "試合結果を削除しました")
        self.reset()
