from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QSplitter, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

from application.result.fetch import EncounteredDeckData, RecordData
from . import (
    DeckDistributionGroup,
    DisplayRecordGroup,
    SearchResultTableModel,
    SearchResultTableGroup,
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
        self.table_group = SearchResultTableGroup()

        row1 = QWidget()
        row1_h_splitter = QSplitter(Qt.Orientation.Horizontal)
        row1_h_splitter.addWidget(self.record_group)
        row1_h_splitter.addWidget(self.win_rate_trend_group)
        row1_h_splitter.setStretchFactor(0, 1)
        row1_h_splitter.setStretchFactor(1, 10)
        layout_for_row1 = QHBoxLayout(row1)
        layout_for_row1.addWidget(row1_h_splitter)

        row2 = QWidget()
        row2_h_splitter = QSplitter(Qt.Orientation.Horizontal)
        row2_h_splitter.addWidget(self.table_group)
        row2_h_splitter.addWidget(self.deck_distribution_group)

        row2_h_splitter.setStretchFactor(0, 16)
        row2_h_splitter.setStretchFactor(1, 9)
#       本来ならば setStretchFactor() のみで比率を指定したいが、
#       上手く動作しないので setSizes() で 16:9 の比率の値を渡している。
#       setSizes() は本来、絶対値のピクセル数を指定し、
#       そのサイズ通りに表示されることを期待するメソッドだと思うが、
#       渡された値が、QSplitter が利用可能な長さと異なる場合は、
#       その値の比率をなるべく維持して表示しようとする模様。
        row2_h_splitter.setSizes([192, 108])

        layout_for_row2 = QHBoxLayout(row2)
        layout_for_row2.addWidget(row2_h_splitter)

        v_splitter = QSplitter(Qt.Orientation.Vertical)
        v_splitter.addWidget(row1)
        v_splitter.addWidget(row2)
        v_splitter.setStretchFactor(0, 1)
        v_splitter.setStretchFactor(1, 3)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(v_splitter)

    def update_record(self, data: RecordData):
        self.record_group.update_record(data)

    def update_distribution_charts(self,
        distribution_for_pie: list[EncounteredDeckData],
        distribution_for_h_bar: list[EncounteredDeckData]
    ):
        self.deck_distribution_group.update_pie_chart(distribution_for_pie)
        self.deck_distribution_group.update_h_bar_chart(distribution_for_h_bar)

    def update_win_rate_trend(self, trend: list[float]):
        self.win_rate_trend_group.update_chart(trend)

    def update_table(self, model: SearchResultTableModel):
        self.table_group.update_table(model)

    def closeEvent(self, event: QCloseEvent):
        parent = self.parent()
        # 循環インポートを避けるためにローカルインポートを行っている
        from . import Tab
        if isinstance(parent, Tab):
            parent.remove_search_result_window(self)
        event.accept()
