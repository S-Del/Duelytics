from typing import ClassVar
from PySide6.QtCore import (
    QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
)
from PySide6.QtGui import QColor

from application.result.fetch.use_case import ResultData


class SearchResultTableModel(QAbstractTableModel):
    HEADERS: ClassVar[list[str]] = [
        "登録日時",
        "先/後",
        "試合結果",
        "自分のデッキ名",
        "相手のデッキ名",
        "メモ",
        "ID"
    ]

    def __init__(self, results: list[ResultData]):
        super().__init__()
        self._results = results

    def data(self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole
    ):
        if not index.isValid():
            return

        if role == Qt.ItemDataRole.DisplayRole:
            return self._results[index.row()][index.column()]

        blue = QColor(16, 96, 224)
        red = QColor(192, 16, 16)
        if role == Qt.ItemDataRole.ForegroundRole:
            if index.column() == SearchResultTableModel.HEADERS.index("先/後"):
                if self._results[index.row()].first_or_second_raw == 'F':
                    return blue
                else:
                    return red
            if index.column() == SearchResultTableModel.HEADERS.index(
                "試合結果"
            ):
                if self._results[index.row()].result_raw == 'W':
                    return blue
                if self._results[index.row()].result_raw == 'L':
                    return red

    def rowCount(self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._results)

    def columnCount(self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._results[0]) if self._results else 0

    def headerData(self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return SearchResultTableModel.HEADERS[section]
#           行番号を振る場合
#           else:
#               return str(section + 1)
        return None
