from PySide6.QtWidgets import QGroupBox, QFormLayout, QFrame, QLabel

from application.result.fetch.use_case import RecordData


class DisplayRecordGroup(QGroupBox):
    def __init__(self):
        super().__init__("戦績")

        self._game_count = QLabel()
        self._win_count = QLabel()
        self._loss_count = QLabel()
        self._draw_count = QLabel()
        self._first_count = QLabel()
        self._first_rate = QLabel()
        self._second_count = QLabel()
        self._second_rate = QLabel()
        self._win_rate = QLabel()
        self._first_win_rate = QLabel()
        self._second_win_rate = QLabel()

        layout = QFormLayout()
        layout.addRow(QLabel("試合数:"), self._game_count)
        layout.addRow(QLabel("勝利数:"), self._win_count)
        layout.addRow(QLabel("敗北数:"), self._loss_count)
        layout.addRow(QLabel("引分数:"), self._draw_count)
        layout.addRow(QFrame(frameShape=QFrame.Shape.HLine))
        layout.addRow(QLabel("先攻数:"), self._first_count)
        layout.addRow(QLabel("先攻率:"), self._first_rate)
        layout.addRow(QLabel("後攻数:"), self._second_count)
        layout.addRow(QLabel("後攻率:"), self._second_rate)
        layout.addRow(QFrame(frameShape=QFrame.Shape.HLine))
        layout.addRow(QLabel("勝率:"), self._win_rate)
        layout.addRow(QLabel("先攻勝率:"), self._first_win_rate)
        layout.addRow(QLabel("後攻勝率"), self._second_win_rate)
        self.setLayout(layout)

    def update_record(self, data: RecordData):
        self._game_count.setText(data.game_count_str)
        self._win_count.setText(data.win_count_str)
        self._loss_count.setText(data.loss_count_str)
        self._draw_count.setText(data.draw_count_str)
        self._first_count.setText(data.first_count_str)
        self._first_rate.setText(data.first_rate_percentage_str)
        self._second_count.setText(data.second_count_str)
        self._second_rate.setText(data.second_rate_percentage_str)
        self._win_rate.setText(data.win_rate_percentage_str)
        self._first_win_rate.setText(data.first_win_rate_percentage_str)
        self._second_win_rate.setText(data.second_win_rate_percentage_str)
