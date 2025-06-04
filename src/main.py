from PySide6.QtWidgets import QApplication
from injector import Injector

from application.services.startup import StartupMessageService
from infrastructure.file.deck import DeckNameFileInitializer
from infrastructure.file.deck.exceptions import DeckNameFileCreationError
from infrastructure.logger.setup import init_logger
from infrastructure.sqlite.config import DatabaseFilePath
from infrastructure.sqlite.setup import init_sqlite
from injector_config import InjectorConfig
from presentation.pyside6 import Controller


def main():
    injector = Injector([InjectorConfig()])
    init_logger()
    init_sqlite(injector.get(DatabaseFilePath))

    try:
        injector.get(DeckNameFileInitializer).execute()
    except DeckNameFileCreationError as dnfce:
        message_service = injector.get(StartupMessageService)
        message_service.add_warning(
            "デッキ名ファイルの作成に失敗",
            "アプリは続行できますが、入力補完機能は無効になります。\n"
            "権限やディスク容量を確認をおすすめします。"
        )

    app = QApplication([])
    controller = injector.get(Controller)
    controller.show()
    app.exec()


if __name__ == "__main__":
    main()
