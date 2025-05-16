from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton


class ControlButtonGroup(QGroupBox):
    def __init__(self, slot_for_register: object, slot_for_clear: object):
        super().__init__("操作")

        register_button = QPushButton("登録")
        register_button.clicked.connect(slot_for_register)
        clear_button = QPushButton("クリア")
        clear_button.clicked.connect(slot_for_clear)

        layout = QHBoxLayout()
        layout.addWidget(register_button)
        layout.addWidget(clear_button)

        self.setLayout(layout)
