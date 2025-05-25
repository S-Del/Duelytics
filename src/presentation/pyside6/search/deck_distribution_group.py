from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSet,
    QChart,
    QChartView,
    QHorizontalBarSeries,
    QPieSeries,
    QPieSlice,
    QValueAxis
)
from PySide6.QtWidgets import QGroupBox, QSplitter, QVBoxLayout
from PySide6.QtGui import QFont, QPainter
from PySide6.QtCore import QMargins, Qt

from application.result.fetch import EncounteredDeckData


class DeckDistributionGroup(QGroupBox):
    def __init__(self):
        super().__init__("相手のデッキ分布")

        v_splitter = QSplitter(Qt.Orientation.Vertical)

        self._pie_chart = QChart()
        self._pie_chart.setTitle("遭遇率 Top5 (+その他)")
        self._pie_chart.setMargins(QMargins(0, 0, 0, 0))
        pie_title_font = QFont()
        pie_title_font.setBold(True)
        self._pie_chart.setTitleFont(pie_title_font)
        pie_chart_view = QChartView(self._pie_chart)
        pie_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        v_splitter.addWidget(pie_chart_view)

        self._h_bar_chart = QChart()
        self._h_bar_chart.setTitle("対戦回数 Top10 (+その他)")
        self._h_bar_chart.setMargins(QMargins(0, 0, 0, 0))
        self._h_bar_chart.legend().setVisible(False)
        h_bar_title_font = QFont()
        h_bar_title_font.setBold(True)
        h_bar_chart_view = QChartView(self._h_bar_chart)
        self._h_bar_chart.setTitleFont(h_bar_title_font)
        h_bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        v_splitter.addWidget(h_bar_chart_view)

        layout = QVBoxLayout()
        layout.addWidget(v_splitter)
        self.setLayout(layout)

    def update_pie_chart(self, distribution: list[EncounteredDeckData]):
        self._pie_chart.removeAllSeries()
        if not distribution:
            return

        series = QPieSeries()
        for data in distribution:
            slice = QPieSlice(
                f"{data.name} ({data.encounter_rate})", data.count
            )
            series.append(slice)
        self._pie_chart.addSeries(series)
        series.hovered.connect(self.hovered_slice)

    def hovered_slice(self, slice: QPieSlice, state: bool):
        slice.setExploded(state)
        slice.setLabelVisible(state)

    def update_h_bar_chart(self, distribution: list[EncounteredDeckData]):
        self._h_bar_chart.removeAllSeries()
        if not distribution:
            return

        bar_set = QBarSet("対戦回数")
        names = []
        for data in reversed(distribution):
            bar_set.append(data.count)
            names.append(data.name)

        axis_x = QValueAxis()
        axis_x.setTitleText("対戦回数")
        axis_x.setMin(1)
        axis_x.setLabelFormat("%d")
        self._h_bar_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QBarCategoryAxis()
        axis_y.append(names)
        self._h_bar_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series = QHorizontalBarSeries()
        series.append(bar_set)
        series.setLabelsVisible(True)

        self._h_bar_chart.addSeries(series)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
