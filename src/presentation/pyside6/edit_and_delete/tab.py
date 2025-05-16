from injector import inject
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget
)
from sys import exit
from typing import ClassVar

from application.exception import ApplicationCriticalError, InvalidCommandError
from application.result import IdForResult
from application.result.delete.use_case import DeleteResultById
from application.result.edit import EditResultScenario
from application.result.fetch.use_case import FetchResultData, FetchResultById
from presentation.pyside6.edit_and_delete import DeleteDialog, EditDialog


class Tab(QWidget):
    TITLE: ClassVar[str] = "編集・削除"

    @inject
    def __init__(self,
        fetch_result_by_id: FetchResultById,
        delete_result_by_id: DeleteResultById,
        edit_result: EditResultScenario,
    ):
        super().__init__()

        self.fetch_result_by_id = fetch_result_by_id
        self.delete_result_by_id = delete_result_by_id
        self.edit_result = edit_result

        label = QLabel("ID (必須)")
        self.input = QLineEdit()
        self.input.setPlaceholderText("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")

        control_button_group = QGroupBox("操作")

        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self.on_click_edit_button)

        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self.on_click_delete_button)

        control_button_group_layout = QHBoxLayout()
        control_button_group_layout.addWidget(edit_button)
        control_button_group_layout.addWidget(delete_button)
        control_button_group.setLayout(control_button_group_layout)

        layout = QFormLayout()
        layout.addRow(label, self.input)
        layout.addRow(control_button_group)
        self.setLayout(layout)

    def _fetch_result_by_id_input(self) -> FetchResultData | None:
        """編集、削除の両方で使用する、ID による試合結果検索用内部メソッド。"""
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
            return
        return target

    def on_click_edit_button(self):
        target = self._fetch_result_by_id_input()
        if not target:
            return
        dialog = EditDialog(self, target, self.edit_result)
        dialog.exec()
        self.input.setText("")

    def on_click_delete_button(self):
        target = self._fetch_result_by_id_input()
        if not target:
            return
        dialog = DeleteDialog(self, target, self.delete_result_by_id)
        dialog.exec()
        self.input.setText("")
