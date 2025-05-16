from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton


class ControlButtonGroup(QGroupBox):
    def __init__(self, slot_for_search: object, slot_for_clear: object):
        super().__init__("操作")

        search_button = QPushButton("検索")
        search_button.clicked.connect(slot_for_search)
        clear_button = QPushButton("クリア")
        clear_button.clicked.connect(slot_for_clear)

        layout = QHBoxLayout()
        layout.addWidget(search_button)
        layout.addWidget(clear_button)

        self.setLayout(layout)
