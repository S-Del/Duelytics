from PySide6.QtWidgets import QGroupBox, QFormLayout, QFrame, QLabel

from application.result.fetch import RecordData


class DisplayRecordGroup(QGroupBox):
    def __init__(self):
        super().__init__("戦績")

        self.game_count = QLabel()
        self.win_count = QLabel()
        self.loss_count = QLabel()
        self.draw_count = QLabel()
        self.first_count = QLabel()
        self.first_rate = QLabel()
        self.second_count = QLabel()
        self.second_rate = QLabel()
        self.win_rate = QLabel()
        self.first_win_rate = QLabel()
        self.second_win_rate = QLabel()

        layout = QFormLayout()
        layout.addRow(QLabel("試合数:"), self.game_count)
        layout.addRow(QLabel("勝利数:"), self.win_count)
        layout.addRow(QLabel("敗北数:"), self.loss_count)
        layout.addRow(QLabel("引分数:"), self.draw_count)
        layout.addRow(QFrame(frameShape=QFrame.Shape.HLine))
        layout.addRow(QLabel("先攻数:"), self.first_count)
        layout.addRow(QLabel("先攻率:"), self.first_rate)
        layout.addRow(QLabel("後攻数:"), self.second_count)
        layout.addRow(QLabel("後攻率:"), self.second_rate)
        layout.addRow(QFrame(frameShape=QFrame.Shape.HLine))
        layout.addRow(QLabel("勝率:"), self.win_rate)
        layout.addRow(QLabel("先攻勝率:"), self.first_win_rate)
        layout.addRow(QLabel("後攻勝率"), self.second_win_rate)
        self.setLayout(layout)

    def update_record(self, data: RecordData):
        self.game_count.setText(data.game_count_str)
        self.win_count.setText(data.win_count_str)
        self.loss_count.setText(data.loss_count_str)
        self.draw_count.setText(data.draw_count_str)
        self.first_count.setText(data.first_count_str)
        self.first_rate.setText(data.first_rate_percentage_str)
        self.second_count.setText(data.second_count_str)
        self.second_rate.setText(data.second_rate_percentage_str)
        self.win_rate.setText(data.win_rate_percentage_str)
        self.first_win_rate.setText(data.first_win_rate_percentage_str)
        self.second_win_rate.setText(data.second_win_rate_percentage_str)
