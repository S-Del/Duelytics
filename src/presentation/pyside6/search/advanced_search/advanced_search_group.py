from PySide6.QtWidgets import QGridLayout, QGroupBox

from . import KeywordInputGroup, LimitInputGroup


class AdvancedSearchGroup(QGroupBox):
    def __init__(self):
        super().__init__("詳細条件 指定")

        self.limit_input_group = LimitInputGroup()
        self.keyword_input_group = KeywordInputGroup()

        layout = QGridLayout()
        layout.addWidget(self.limit_input_group)
        layout.addWidget(self.keyword_input_group)

        self.setLayout(layout)

    @property
    def limit(self) -> int:
        return self.limit_input_group.value

    @property
    def keywords(self) -> tuple[str, ...]:
        return self.keyword_input_group.values

    def reset(self):
        self.limit_input_group.reset()
        self.keyword_input_group.reset()
