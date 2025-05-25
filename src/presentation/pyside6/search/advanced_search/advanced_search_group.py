from PySide6.QtWidgets import QGridLayout, QGroupBox

from . import KeywordInputGroup, LimitInputGroup


class AdvancedSearchGroup(QGroupBox):
    def __init__(self):
        super().__init__("詳細条件 指定")

        self._limit_input_group = LimitInputGroup()
        self._keyword_input_group = KeywordInputGroup()

        layout = QGridLayout()
        layout.addWidget(self._limit_input_group)
        layout.addWidget(self._keyword_input_group)

        self.setLayout(layout)

    @property
    def limit(self) -> int:
        return self._limit_input_group.value

    @property
    def keywords(self) -> tuple[str, ...]:
        return self._keyword_input_group.values

    def reset(self):
        self._limit_input_group.reset()
        self._keyword_input_group.reset()
