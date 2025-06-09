from collections import deque
from injector import inject
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QLabel, QMainWindow, QStatusBar, QTabWidget, QVBoxLayout, QWidget
)

from application.events import EventAggregator
from application.services.startup import StartupMessageService
from presentation.pyside6.event import StatusBarMessageEvent
from presentation.pyside6.register import Tab as RegisterTab
from presentation.pyside6.search import Tab as SearchTab
from presentation.pyside6.edit_and_delete import Tab as EditAndDeleteTab


class Controller(QMainWindow):
    @inject
    def __init__(self,
        message_service: StartupMessageService,
        event_aggregator: EventAggregator,
        register_tab: RegisterTab,
        search_tab: SearchTab,
        edit_and_delete_tab: EditAndDeleteTab
    ):
        super().__init__()
        self._event_aggregator = event_aggregator
        self._event_aggregator.subscribe(
            StatusBarMessageEvent, self._on_status_bar_message_event
        )
        central_widget = QWidget(self)
        self.setWindowTitle("Duelytics (v1.0)")
        self.setCentralWidget(central_widget)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(QLabel())

        tab_control = QTabWidget()
        tab_control.addTab(register_tab, RegisterTab.TITLE)
        tab_control.addTab(search_tab, SearchTab.TITLE)
        tab_control.addTab(edit_and_delete_tab, EditAndDeleteTab.TITLE)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(tab_control)

        if message_service.has_pending_messages():
            msg_queue = deque(message_service.get_pending_warnings())
            self._display_status_with_tips_from_queue(msg_queue)

    def _display_status_with_tips_from_queue(self,
        msg_queue: deque[tuple[str, str | None]],
        timeout_ms: int = 7000
    ):
        if not msg_queue:
            return
        sbar = self.statusBar()
        msg, tooltip = msg_queue.popleft()
        sbar.showMessage(msg, timeout_ms)
        if not tooltip:
            sbar.setToolTip("")
        else:
            sbar.setToolTip(tooltip)

        if msg_queue:
            QTimer.singleShot(
                timeout_ms,
                lambda: self._display_status_with_tips_from_queue(
                    msg_queue, timeout_ms
                )
            )
        else:
            QTimer.singleShot(timeout_ms, lambda: sbar.setToolTip(""))

    def _clear_tooltip_if_match(self, tooltip: str):
        """ツールチップクリア用メソッド

        現在表示されているメッセージを、
        別のメッセージでで上書きしないかチェックしてからクリアする。
        """
        sbar = self.statusBar()
        if sbar.toolTip() == tooltip:
            sbar.setToolTip("")

    def display_status_message_with_tips(self,
        msg: str,
        tooltip: str | None = None,
        timeout_ms: int = 7000
    ):
        sbar = self.statusBar()
        sbar.showMessage(msg, timeout_ms)

        if not tooltip:
            sbar.setToolTip("")
            return

        sbar.setToolTip(tooltip)
        if timeout_ms > 0:
            QTimer.singleShot(
                timeout_ms,
                lambda: self._clear_tooltip_if_match(tooltip)
            )

    def _on_status_bar_message_event(self, event: StatusBarMessageEvent):
        self.display_status_message_with_tips(event.msg, event.tooltip)
