from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QSpinBox


class LimitInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("最大取得件数 入力")

        group_label = QLabel("0 が入力された場合は無制限")

        self.limit_input = QSpinBox()
        self.limit_input.setMinimum(0)
        self.limit_input.setMaximum(0x7FFFFFFF) # == 32bit 符号付き整数の最大値
        self.limit_input.setValue(0)

        layout = QFormLayout()
        layout.addRow(group_label)
        layout.addRow(self.limit_input)

        self.setLayout(layout)

    @property
    def value(self) -> int:
        return self.limit_input.value()

    def reset(self):
        self.limit_input.setValue(0)
