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
from application.result.fetch.use_case import (
    FetchResultsRequest, FetchResultsByQuery
)
from presentation.pyside6.event import StatusBarMessageEvent
from presentation.pyside6.search.advanced_search import AdvancedSearchGroup
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
        fetch_result_with_record: FetchResultsByQuery,
        fetch_all_deck_name: FetchAllDeckName
    ):
        super().__init__()
        self._event_aggregator = event_aggregator
        self._fetch_result_with_record = fetch_result_with_record
        self._fetch_all_deck_name = fetch_all_deck_name
        self._id_input_group = IdInputGroup()
        self._first_or_second_checkbox_group = FirstOrSecondCheckboxGroup()
        self._result_checkbox_group = ResultCheckboxGroup()
        self._deck_name_input_group = DeckNameInputGroup()
        self._deck_name_input_group.deck_input_focused.connect(
            self.update_completer_deck_list
        )
        self._date_range_input_group = DateRangeInputGroup()
        self._advanced_search_group = AdvancedSearchGroup()
        search_shortcut = QShortcut(
            QKeySequence("Ctrl+Return"),
            self
        )
        search_shortcut.activated.connect(self.on_click_search_button)
        self._search_result_windows: list[SearchResultWindow] = []

        form_layout = QGridLayout()
        form_layout.addWidget(self._id_input_group, 0, 0, 1, 2)
        form_layout.addWidget(self._date_range_input_group, 0, 2)
        form_layout.addWidget(self._first_or_second_checkbox_group, 1, 0)
        form_layout.addWidget(self._result_checkbox_group, 1, 1)
        form_layout.addWidget(self._deck_name_input_group, 1, 2)
        form_layout.addWidget(self._advanced_search_group, 2, 0, 1, 3)

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
            deck_names = self._fetch_all_deck_name.handle()
        except ApplicationOperationWarning as aow:
            self._event_aggregator.publish(
                StatusBarMessageEvent(aow.msg, aow.details)
            )
            return
        self._deck_name_input_group.update_completer_deck_list(
            tuple(deck_names)
        )

    def remove_search_result_window(self, window: SearchResultWindow):
        if window in self._search_result_windows:
            self._search_result_windows.remove(window)

    def on_click_clear_button(self):
        self._id_input_group.reset()
        self._first_or_second_checkbox_group.reset()
        self._result_checkbox_group.reset()
        self._deck_name_input_group.reset()
        self._date_range_input_group.reset()
        self._advanced_search_group.reset()

    def on_click_search_button(self):
        request: FetchResultsRequest = {}
        if self._id_input_group.id:
            request["id"] = self._id_input_group.id
        request["first_or_second"] = self._first_or_second_checkbox_group.values
        request["result"] = self._result_checkbox_group.values
        if self._deck_name_input_group.my_deck_name:
            request["my_deck_name"] = self._deck_name_input_group.my_deck_name
        request["my_deck_name_search_type"] = (
            self._deck_name_input_group.my_deck_search_type
        )
        if self._deck_name_input_group.opponent_deck_name:
            request["opponent_deck_name"] = (
                self._deck_name_input_group.opponent_deck_name
            )
        request["opponent_deck_name_search_type"] = (
            self._deck_name_input_group.opponent_deck_search_type
        )
        if self._date_range_input_group.since:
            request["since"] = self._date_range_input_group.since
        if self._date_range_input_group.until:
            request["until"] = self._date_range_input_group.until
        request["order"] = self._date_range_input_group.order_by
        request["limit"] = self._advanced_search_group.limit

        try:
            fetch_result = self._fetch_result_with_record.handle(request)
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
            SearchResultTableModel(fetch_result.result_data_list)
        )
        search_result_window.resize(1280, 720)
        search_result_window.show()
        self._search_result_windows.append(search_result_window)
