from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtWidgets import QGroupBox, QVBoxLayout
from PySide6.QtGui import QPainter, Qt
from PySide6.QtCore import QMargins


class WinRateTrendGroup(QGroupBox):
    def __init__(self):
        super().__init__("試合ごとの勝率推移")

        self._chart = QChart()
        self._chart.setMargins(QMargins(0, 0, 0, 0))

        chart_view = QChartView(self._chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._axis_x = QValueAxis()
        self._axis_x.setTitleText("試合数")
        self._axis_x.setLabelFormat("%d")
        self._axis_x.setMin(1)
        self._axis_x.setTickInterval(1)
        self._axis_x.setMinorTickCount(0)
        self._chart.addAxis(self._axis_x, Qt.AlignmentFlag.AlignBottom)

        self._axis_y = QValueAxis()
        self._axis_y.setLabelFormat("%.1f%%")
        self._axis_y.setTitleText("勝率 (%)")
        self._axis_y.setMin(0)
        self._axis_y.setMax(100)
        self._chart.addAxis(self._axis_y, Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        self.setLayout(layout)

    def update_chart(self, trend: list[float]):
        self._chart.removeAllSeries()
        if not trend:
            return

        series = QLineSeries()
        for game_count, win_rate in enumerate(trend, 1):
            series.append(game_count, win_rate)

        self._chart.addSeries(series)
        series.attachAxis(self._axis_x)
        series.attachAxis(self._axis_y)
        self._chart.legend().setVisible(False)

        max_game_count = len(trend)
        if max_game_count < 30:
            self._axis_x.setTickInterval(1)
        elif max_game_count < 100:
            self._axis_x.setTickInterval(10)
        elif max_game_count < 500:
            self._axis_x.setTickInterval(50)
        elif max_game_count < 1000:
            self._axis_x.setTickInterval(100)
        else:
            self._axis_x.setTickInterval(500)
