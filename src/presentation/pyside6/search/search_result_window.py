from collections import Counter
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QSplitter, QTableView, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

from application.result.fetch import RecordData
from . import (
    DeckDistributionGroup,
    DisplayRecordGroup,
    SearchResultTableModel,
    WinRateTrendGroup
)


class SearchResultWindow(QMainWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setWindowTitle("検索結果")
        self.setMinimumSize(768, 768)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.record_group = DisplayRecordGroup()
        self.deck_distribution_group = DeckDistributionGroup()
        self.win_rate_trend_group = WinRateTrendGroup()
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        row_height = self.table_view.verticalHeader().defaultSectionSize()
        self.table_view.setMinimumHeight(row_height * 5)

        row1 = QWidget()
        row1_h_splitter = QSplitter(Qt.Orientation.Horizontal)
        row1_h_splitter.addWidget(self.record_group)
        row1_h_splitter.addWidget(self.win_rate_trend_group)
        row1_h_splitter.setStretchFactor(0, 1)
        row1_h_splitter.setStretchFactor(1, 5)
        layout_for_row1 = QHBoxLayout(row1)
        layout_for_row1.addWidget(row1_h_splitter)

        row2 = QWidget()
        row2_h_splitter = QSplitter(Qt.Orientation.Horizontal)
        row2_h_splitter.addWidget(self.table_view)
        row2_h_splitter.addWidget(self.deck_distribution_group)
        row2_h_splitter.setStretchFactor(0, 2)
        row2_h_splitter.setStretchFactor(1, 1)
        layout_for_row2 = QHBoxLayout(row2)
        layout_for_row2.addWidget(row2_h_splitter)

        v_splitter = QSplitter(Qt.Orientation.Vertical)
        v_splitter.addWidget(row1)
        v_splitter.addWidget(row2)
        v_splitter.setStretchFactor(0, 1)
        v_splitter.setStretchFactor(1, 2)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(v_splitter)

    def update_record(self, data: RecordData):
        self.record_group.update_record(data)

    def update_distribution(self, distribution: Counter[str]):
        self.deck_distribution_group.update_chart(distribution)

    def update_win_rate_trend(self, trend: list[float]):
        self.win_rate_trend_group.update_chart(trend)

    def update_table(self, model: SearchResultTableModel):
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

    def closeEvent(self, event: QCloseEvent):
        parent = self.parent()
        # 循環インポートを避けるためにローカルインポートを行っている
        from . import Tab
        if isinstance(parent, Tab):
            parent.remove_search_result_window(self)
        event.accept()
