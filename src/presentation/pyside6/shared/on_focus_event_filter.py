from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, QObject
from typing import Callable


class OnFocusEventFilter(QObject):
    def __init__(self,
        on_focus: Callable[[], None],
        parent: QWidget | None = None
    ):
        super().__init__(parent)
        self.on_focus = on_focus

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.FocusIn:
            self.on_focus()

        return super().eventFilter(watched, event)
