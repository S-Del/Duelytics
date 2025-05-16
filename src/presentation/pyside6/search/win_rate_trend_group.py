from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtWidgets import QGroupBox, QVBoxLayout
from PySide6.QtGui import QPainter, Qt
from PySide6.QtCore import QMargins


class WinRateTrendGroup(QGroupBox):
    def __init__(self):
        super().__init__("試合ごとの勝率推移")

        self.chart = QChart()
        self.chart.setMargins(QMargins(0, 0, 0, 0))

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("試合数")
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setMin(1)
        self.axis_x.setTickInterval(1)
        self.axis_x.setMinorTickCount(0)
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.1f%%")
        self.axis_y.setTitleText("勝率 (%)")
        self.axis_y.setMin(0)
        self.axis_y.setMax(100)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        self.setLayout(layout)

    def update_chart(self, trend: list[float]):
        self.chart.removeAllSeries()
        if not trend:
            return

        series = QLineSeries()
        for game_count, win_rate in enumerate(trend, 1):
            series.append(game_count, win_rate)

        self.chart.addSeries(series)
        series.attachAxis(self.axis_x)
        series.attachAxis(self.axis_y)
        self.chart.legend().setVisible(False)

        max_game_count = len(trend)
        if max_game_count < 30:
            self.axis_x.setTickInterval(1)
        elif max_game_count < 100:
            self.axis_x.setTickInterval(10)
        elif max_game_count < 500:
            self.axis_x.setTickInterval(50)
        elif max_game_count < 1000:
            self.axis_x.setTickInterval(100)
        else:
            self.axis_x.setTickInterval(500)
