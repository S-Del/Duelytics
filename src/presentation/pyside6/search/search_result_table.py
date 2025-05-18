from PySide6.QtWidgets import QGroupBox, QTableView, QVBoxLayout

from . import SearchResultTableModel


class SearchResultTableGroup(QGroupBox):
    def __init__(self):
        super().__init__("検索結果一覧")

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def update_table(self, model: SearchResultTableModel):
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
