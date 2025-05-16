from injector import inject
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from presentation.pyside6.register import Tab as RegisterTab
from presentation.pyside6.search import Tab as SearchTab
from presentation.pyside6.edit_and_delete import Tab as EditAndDeleteTab


class Controller(QMainWindow):
    @inject
    def __init__(self,
        register_tab: RegisterTab,
        search_tab: SearchTab,
        edit_and_delete_tab: EditAndDeleteTab
    ):
        super().__init__()

        central_widget = QWidget(self)
        self.setWindowTitle("Duelytics")
        self.setCentralWidget(central_widget)

        tab_control = QTabWidget()
        tab_control.addTab(register_tab, RegisterTab.TITLE)
        tab_control.addTab(search_tab, SearchTab.TITLE)
        tab_control.addTab(edit_and_delete_tab, EditAndDeleteTab.TITLE)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(tab_control)
