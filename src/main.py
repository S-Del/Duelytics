from PySide6.QtWidgets import QApplication
from injector import Injector

from infrastructure.logger.setup import init_logger
from infrastructure.sqlite.setup import init_sqlite
from injector_config import InjectorConfig
from presentation.pyside6 import Controller


def main():
    init_logger()
    init_sqlite()

    app = QApplication([])
    controller = Injector([InjectorConfig()]).get(Controller)
    controller.show()
    app.exec()


if __name__ == "__main__":
    main()
