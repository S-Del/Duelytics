from collections import Counter
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtWidgets import QGroupBox, QVBoxLayout
from PySide6.QtGui import QPainter
from PySide6.QtCore import QMargins


class DeckDistributionGroup(QGroupBox):
    def __init__(self):
        super().__init__("相手のデッキ分布")

        self.chart = QChart()
        self.chart.setMargins(QMargins(0, 0, 0, 0))

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        self.setLayout(layout)

    def update_chart(self, distribution: Counter[str]):
        self.chart.removeAllSeries()
        series = QPieSeries()
        for name, count in distribution.items():
            slice = QPieSlice(name, count)
            slice.setLabelVisible(False)
            slice.setLabel(f"{name}: {count}")
            series.append(slice)
        self.chart.addSeries(series)
        series.hovered.connect(self.hovered_series)
        self.chart.legend().setVisible(False)

    def hovered_series(self, slice: QPieSlice, state: bool):
        slice.setExploded(state)
        slice.setLabelVisible(state)
