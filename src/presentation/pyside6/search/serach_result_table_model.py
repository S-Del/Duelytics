from PySide6.QtCore import (
    QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
)

from application.result.fetch.use_case import FetchResultData


class SearchResultTableModel(QAbstractTableModel):
    def __init__(self, results: list[FetchResultData]):
        super().__init__()
        self.results = results

    def data(self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.results[index.row()][index.column()]
        return None

    def rowCount(self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self.results)

    def columnCount(self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self.results[0]) if self.results else 0

    def headerData(self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole
    ):
        headers = [
            "登録日時",
            "先/後",
            "試合結果",
            "自分のデッキ名",
            "相手のデッキ名",
            "メモ",
            "ID"
        ]
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return headers[section]
#           行番号を振る場合
#           else:
#               return str(section + 1)
        return None
