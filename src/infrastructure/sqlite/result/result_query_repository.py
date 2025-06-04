from datetime import datetime
from injector import inject
from logging import getLogger
from sqlite3 import connect, Row
from typing import cast
from uuid import UUID

from domain.model.result import DuelResult, FirstOrSecond, ResultChar
from domain.repository.result.exception import RepositoryDataError
from domain.repository.result import (
    SearchResultsQuery,
    ResultQueryRepository
)
from domain.shared.unit import NonEmptyStr
from infrastructure.sqlite.config import (
    DatabaseFilePath, ResultSchema, MemoSchema
)
from . import SearchConditionBuilder


class SQLiteResultQueryRepository(ResultQueryRepository):
    @inject
    def __init__(self,
        db_path: DatabaseFilePath,
        builder: SearchConditionBuilder
    ):
        self._db_path = db_path
        self._builder = builder
        self._logger = getLogger(__name__)

    def _row_to_result(self, row: Row) -> DuelResult:
        try:
            memo_content_raw = row[MemoSchema.Columns.CONTENT]
            memo_content: NonEmptyStr | None = None
            if memo_content_raw:
                memo_content = NonEmptyStr(memo_content_raw)

            return DuelResult(
                id=UUID(row[ResultSchema.Columns.ID]),
                registered_at=datetime.fromisoformat(row[
                    ResultSchema.Columns.REGISTERED_AT
                ]),
                first_or_second=FirstOrSecond(
                    row[ResultSchema.Columns.FIRST_OR_SECOND]
                ),
                result=ResultChar(row[ResultSchema.Columns.RESULT]),
                my_deck_name=NonEmptyStr(
                    row[ResultSchema.Columns.MY_DECK_NAME]
                ),
                opponent_deck_name=NonEmptyStr(
                    row[ResultSchema.Columns.OPPONENT_DECK_NAME]
                ),
                memo=memo_content
            )
        except (KeyError, TypeError, ValueError) as e:
            msg = f"データベースからのマッピング中にエラー: {e} > {dict(row)}"
            self._logger.critical(msg, exc_info=True)
            raise RepositoryDataError(msg) from e

    def search_by_id(self, id: UUID) -> DuelResult | None:
        id_str = str(id)
        sql = " ".join([
            "SELECT r.*,",
            f"m.{MemoSchema.Columns.CONTENT} AS {MemoSchema.Columns.CONTENT}",
            f"FROM {ResultSchema.TABLE_NAME} AS r",
            f"LEFT JOIN {MemoSchema.TABLE_NAME} AS m",
            f"ON r.{ResultSchema.Columns.ID}",
            f"= m.{MemoSchema.Columns.RESULT_ID}",
            f"WHERE r.{ResultSchema.Columns.ID} = ?"
        ])
        param = (id_str,)
        self._logger.debug("\n".join([
            f"search_by_id()",
            f"\tSQL: {sql}",
            f"\tParam: {id_str}"
        ]))

        with connect(self._db_path) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(sql, param)
            data = cursor.fetchone()

        if data is None:
            return

        return self._row_to_result(cast(Row, data))

    def search(self, query: SearchResultsQuery) -> tuple[DuelResult, ...]:
        where_clause, params = self._builder.build(query)
        sql_parts = [
            "SELECT r.*,",
            f"m.{MemoSchema.Columns.CONTENT} AS {MemoSchema.Columns.CONTENT}",
            f"FROM {ResultSchema.TABLE_NAME} AS r",
            f"LEFT JOIN {MemoSchema.TABLE_NAME} AS m",
            f"ON r.{ResultSchema.Columns.ID}",
            f"= m.{MemoSchema.Columns.RESULT_ID}",
            where_clause,
            f"ORDER BY r.{ResultSchema.Columns.REGISTERED_AT}",
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

        with connect(self._db_path) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cast(list[Row], cursor.fetchall())

        duel_result_list = []
        for row in rows:
            duel_result_list.append(self._row_to_result(row))

        return tuple(duel_result_list)
