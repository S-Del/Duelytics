from injector import Injector, singleton
from PySide6.QtWidgets import QApplication, QMessageBox
from sqlite3 import Error
from sys import exit

from application.services.startup import StartupMessageService
from infrastructure.file.deck import DeckNameFileInitializer
from infrastructure.file.deck.exceptions import DeckNameFileCreationError
from infrastructure.logger.setup import init_logger
from infrastructure.sqlite import ReferenceData
from infrastructure.sqlite.config import DatabaseFilePath
from infrastructure.sqlite.setup import apply_migrations, create_reference_data
from injector_config import InjectorConfig
from presentation.pyside6 import Controller


def main():
    injector = Injector([InjectorConfig()])
    init_logger()
    app = QApplication([])

    try:
        db_path = injector.get(DatabaseFilePath)
        apply_migrations(db_path)
        injector.binder.bind(
            ReferenceData,
            to=create_reference_data(db_path),
            scope=singleton
        )
    except (AttributeError, Error):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("データベース初期化エラー")
        msg_box.setText(
            "データベースのマイグレーションに失敗しました。\n"
            "詳細はログファイルを確認してください。"
        )
        msg_box.exec()
        exit(1)

    try:
        injector.get(DeckNameFileInitializer).execute()
    except DeckNameFileCreationError as dnfce:
        message_service = injector.get(StartupMessageService)
        message_service.add_warning(
            "デッキ名ファイルの作成に失敗",
            "アプリは続行できますが、入力補完機能は無効になります。\n"
            "権限やディスク容量を確認をおすすめします。"
        )

    controller = injector.get(Controller)
    controller.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
