from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLabel, QMessageBox, QPushButton, QWidget
)
from sys import exit

from application.exception import ApplicationCriticalError, InvalidCommandError
from application.result import IdForResult
from application.result.delete.use_case import DeleteResultById
from application.result.fetch.use_case import FetchResultData


class DeleteDialog(QDialog):
    def __init__(self,
        parent: QWidget | None,
        target: FetchResultData,
        delete_result_by_id: DeleteResultById
    ):
        super().__init__(parent)
        self.setWindowTitle("試合結果 削除")

        self.target = target
        self.delete_result_by_id = delete_result_by_id
        self.cancel_button = QPushButton("キャンセル")
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button = QPushButton("続行")
        self.accept_button.clicked.connect(self.on_click_accept_button)

        layout = QFormLayout()
        layout.addRow(QLabel("ID:"), QLabel(target.id))
        layout.addRow(QLabel("登録日時:"), QLabel(target.registered_at))
        layout.addRow(QLabel("先/後:"), QLabel(target.first_or_second))
        layout.addRow(QLabel("試合結果:"), QLabel(target.result))
        layout.addRow(QLabel("自分のデッキ名:"), QLabel(target.my_deck_name))
        layout.addRow(
            QLabel("相手のデッキ名:"), QLabel(target.opponent_deck_name)
        )
        layout.addRow(QLabel("メモ:"), QLabel(target.note or ""))
        layout.addRow(self.cancel_button, self.accept_button)
        self.setLayout(layout)

    def on_click_accept_button(self):
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
        self.accept()
