from datetime import datetime
from injector import inject
from logging import getLogger
from sqlite3 import connect, Row
from typing import cast
from uuid import UUID

from domain.model.result import DuelResult, FirstOrSecond, ResultChar
from domain.repository.result.exception import RepositoryDataError
from domain.repository.result import (
    FetchResultQuery,
    ResultQueryRepository
)
from domain.shared.unit import NonEmptyStr
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import (
    ResultTableConfig,
    NoteTableConfig
)
from infrastructure.sqlite.utils import make_qualified_column
from . import SearchConditionBuilder


class SQLiteResultQueryRepository(ResultQueryRepository):
    @inject
    def __init__(self, builder: SearchConditionBuilder):
        self._logger = getLogger(__name__)
        self._builder = builder

    def _row_to_result(self, row: Row) -> DuelResult:
        try:
            return DuelResult(
                UUID(row[ResultTableConfig.COLUMN_NAMES.ID]),
                datetime.fromisoformat(row[
                    ResultTableConfig.COLUMN_NAMES.REGISTER_DATE
                ]),
                FirstOrSecond(row[
                    ResultTableConfig.COLUMN_NAMES.FIRST_OR_SECOND
                ]),
                ResultChar(row[ResultTableConfig.COLUMN_NAMES.RESULT]),
                NonEmptyStr(row[ResultTableConfig.COLUMN_NAMES.MY_DECK_NAME]),
                NonEmptyStr(
                    row[ResultTableConfig.COLUMN_NAMES.OPPONENT_DECK_NAME]
                ),
                row[NoteTableConfig.COLUMN_NAMES.NOTE]
            )
        except (KeyError, TypeError, ValueError) as e:
            self._logger.critical(
                f"リポジトリのデータ不整合: {e}",
                exc_info=True
            )
            raise RepositoryDataError from e

    def search_by_id(self, id: UUID) -> DuelResult | None:
        result_id_qualified = make_qualified_column(
            ResultTableConfig.TABLE_NAME,
            ResultTableConfig.COLUMN_NAMES.ID
        )
        note_id_qualified = make_qualified_column(
            NoteTableConfig.TABLE_NAME,
            NoteTableConfig.COLUMN_NAMES.ID
        )
        sql = " ".join([
            f"SELECT * FROM {ResultTableConfig.TABLE_NAME}",
            f"LEFT JOIN {NoteTableConfig.TABLE_NAME}",
            f"ON {result_id_qualified} = {note_id_qualified}",
            f"WHERE {result_id_qualified} = ?"
        ])
        self._logger.debug("\n".join([
            f"search_by_id()",
            f"\tsql: {sql}",
            f"\tparam: {id}"
        ]))

        with connect(DatabaseConfig.DATABASE_NAME) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(sql, (str(id),))
            data = cursor.fetchone()

        if data is None:
            return
        row = cast(Row, data)

        return self._row_to_result(row)

    def search(self, query: FetchResultQuery) -> tuple[DuelResult]:
        result_id_qualified = make_qualified_column(
            ResultTableConfig.TABLE_NAME,
            ResultTableConfig.COLUMN_NAMES.ID
        )
        note_id_qualified = make_qualified_column(
            NoteTableConfig.TABLE_NAME,
            NoteTableConfig.COLUMN_NAMES.ID
        )

        where_clause, params = self._builder.build(query)

        sql_parts = [
            f"SELECT * FROM {ResultTableConfig.TABLE_NAME}",
            f"LEFT JOIN {NoteTableConfig.TABLE_NAME}",
            f"ON {result_id_qualified} = {note_id_qualified}",
            where_clause,
            f"ORDER BY {ResultTableConfig.COLUMN_NAMES.REGISTER_DATE}",
            f"{query.get('order') or 'DESC'}"
        ]
        limit = query.get("limit")
        if limit:
            sql_parts.append(f"LIMIT ?")
            params.append(limit.value)

        sql = " ".join(sql_parts)

        self._logger.debug("\n".join([
            f"search()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))

        with connect(DatabaseConfig.DATABASE_NAME) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cast(list[Row], cursor.fetchall())

        duel_result_list = []
        for row in rows:
            duel_result_list.append(self._row_to_result(row))

        return tuple(duel_result_list)
