from injector import inject
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QGridLayout, QMessageBox, QWidget
from sys import exit
from typing import ClassVar

from application.deck.fetch.use_case import FetchAllDeckName
from application.exception import ApplicationCriticalError
from application.result.fetch import FetchResultRequest, FetchResultWithRecord
from .advanced_search import AdvancedSearchGroup
from . import (
    IdInputGroup,
    FirstOrSecondCheckboxGroup,
    ResultCheckboxGroup,
    DeckNameInputGroup,
    DateRangeInputGroup,
    ControlButtonGroup,
    SearchResultTableModel,
    SearchResultWindow
)


class Tab(QWidget):
    TITLE: ClassVar[str] = "検索"

    @inject
    def __init__(self,
        fetch_result_with_record: FetchResultWithRecord,
        fetch_all_deck_name: FetchAllDeckName
    ):
        super().__init__()

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
        self.control_button_group = ControlButtonGroup(
            self.on_click_search_button,
            self.on_click_clear_button
        )
        search_shortcut = QShortcut(
            QKeySequence("Ctrl+Return"),
            self
        )
        search_shortcut.activated.connect(self.on_click_search_button)
        self.search_result_windows: list[SearchResultWindow] = []

        layout = QGridLayout()
        layout.addWidget(self.id_input_group, 0, 0, 1, 2)
        layout.addWidget(self.date_range_input_group, 0, 2)
        layout.addWidget(self.first_or_second_checkbox_group, 1, 0)
        layout.addWidget(self.result_checkbox_group, 1, 1)
        layout.addWidget(self.deck_name_input_group, 1, 2)
        layout.addWidget(self.advanced_search_group, 2, 0, 1, 3)
        layout.addWidget(self.control_button_group, 3, 0, 1, 3)
        self.setLayout(layout)

    def update_completer_deck_list(self):
        try:
            deck_names = self.fetch_all_deck_name.handle()
        except ApplicationCriticalError as ae:
            QMessageBox.critical(self, "アプリケーションエラー", str(ae))
            exit(1)
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
