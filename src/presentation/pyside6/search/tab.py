from injector import inject
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QGridLayout, QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout, QWidget
)
from sys import exit
from typing import ClassVar

from application.deck.fetch.use_case import FetchAllDeckName
from application.events import EventAggregator
from application.exception import (
    ApplicationCriticalError, ApplicationOperationWarning
)
from application.result.fetch import FetchResultRequest, FetchResultWithRecord
from presentation.events.status_bar_message_event import StatusBarMessageEvent
from .advanced_search import AdvancedSearchGroup
from . import (
    IdInputGroup,
    FirstOrSecondCheckboxGroup,
    ResultCheckboxGroup,
    DeckNameInputGroup,
    DateRangeInputGroup,
    SearchResultTableModel,
    SearchResultWindow
)


class Tab(QWidget):
    TITLE: ClassVar[str] = "検索"

    @inject
    def __init__(self,
        event_aggregator: EventAggregator,
        fetch_result_with_record: FetchResultWithRecord,
        fetch_all_deck_name: FetchAllDeckName
    ):
        super().__init__()
        self._event_aggregator = event_aggregator
        self.fetch_result_with_record = fetch_result_with_record
        self.fetch_all_deck_name = fetch_all_deck_name
        self.id_input_group = IdInputGroup()
        self.first_or_second_checkbox_group = FirstOrSecondCheckboxGroup()
        self.result_checkbox_group = ResultCheckboxGroup()
        self.deck_name_input_group = DeckNameInputGroup()
        self.deck_name_input_group.deck_input_focused.connect(
            self.update_completer_deck_list
        )
        self.date_range_input_group = DateRangeInputGroup()
        self.advanced_search_group = AdvancedSearchGroup()
        search_shortcut = QShortcut(
            QKeySequence("Ctrl+Return"),
            self
        )
        search_shortcut.activated.connect(self.on_click_search_button)
        self.search_result_windows: list[SearchResultWindow] = []

        form_layout = QGridLayout()
        form_layout.addWidget(self.id_input_group, 0, 0, 1, 2)
        form_layout.addWidget(self.date_range_input_group, 0, 2)
        form_layout.addWidget(self.first_or_second_checkbox_group, 1, 0)
        form_layout.addWidget(self.result_checkbox_group, 1, 1)
        form_layout.addWidget(self.deck_name_input_group, 1, 2)
        form_layout.addWidget(self.advanced_search_group, 2, 0, 1, 3)

        search_button = QPushButton("検索")
        search_button.clicked.connect(self.on_click_search_button)
        clear_button = QPushButton("クリア")
        clear_button.clicked.connect(self.on_click_clear_button)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(search_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_completer_deck_list(self):
        try:
            deck_names = self.fetch_all_deck_name.handle()
        except ApplicationOperationWarning as aow:
            self._event_aggregator.publish(
                StatusBarMessageEvent(aow.msg, aow.details)
            )
            return
        self.deck_name_input_group.update_completer_deck_list(
            tuple(deck_names)
        )

    def remove_search_result_window(self, window: SearchResultWindow):
        if window in self.search_result_windows:
            self.search_result_windows.remove(window)

    def on_click_clear_button(self):
        self.id_input_group.reset()
        self.first_or_second_checkbox_group.reset()
        self.result_checkbox_group.reset()
        self.deck_name_input_group.reset()
        self.date_range_input_group.reset()
        self.advanced_search_group.reset()

    def on_click_search_button(self):
        request: FetchResultRequest = {}
        if self.id_input_group.id:
            request["id"] = self.id_input_group.id
        request["first_or_second"] = self.first_or_second_checkbox_group.values
        request["result"] = self.result_checkbox_group.values
        if self.deck_name_input_group.my_deck_name:
            request["my_deck_name"] = self.deck_name_input_group.my_deck_name
        request["my_deck_name_search_type"] = (
            self.deck_name_input_group.my_deck_search_type
        )
        if self.deck_name_input_group.opponent_deck_name:
            request["opponent_deck_name"] = (
                self.deck_name_input_group.opponent_deck_name
            )
        request["opponent_deck_name_search_type"] = (
            self.deck_name_input_group.opponent_deck_search_type
        )
        if self.date_range_input_group.since:
            request["since"] = self.date_range_input_group.since
        if self.date_range_input_group.until:
            request["until"] = self.date_range_input_group.until
        request["order"] = self.date_range_input_group.order_by
        request["limit"] = self.advanced_search_group.limit

        try:
            fetch_result = self.fetch_result_with_record.handle(request)
        except ValueError as ve:
            QMessageBox.warning(self, "不正な値", str(ve))
            return
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "アプリケーションエラー", str(ae))
            exit(1)

        if not fetch_result:
            QMessageBox.information(self,
                "検索終了", "検索結果がありませんでした。"
            )
            return

        search_result_window = SearchResultWindow(self)
        search_result_window.update_record(fetch_result.record)
        search_result_window.update_distribution_charts(
            fetch_result.distribution_for_pie,
            fetch_result.distribution_for_h_bar
        )
        search_result_window.update_win_rate_trend(
            fetch_result.win_rate_trend_data
        )
        search_result_window.update_table(
            SearchResultTableModel(fetch_result.data_list)
        )
        search_result_window.resize(1280, 720)
        search_result_window.show()
        self.search_result_windows.append(search_result_window)
