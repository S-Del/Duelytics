from PySide6.QtWidgets import QGroupBox, QTableView, QVBoxLayout

from . import SearchResultTableModel


class SearchResultTableGroup(QGroupBox):
    def __init__(self):
        super().__init__("検索結果一覧")

        self._table_view = QTableView()
        self._table_view.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self._table_view)

        self.setLayout(layout)

    def update_table(self, model: SearchResultTableModel):
        self._table_view.setModel(model)
        self._table_view.resizeColumnsToContents()
        self._table_view.resizeRowsToContents()
