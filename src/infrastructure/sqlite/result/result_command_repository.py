from logging import getLogger
from uuid import UUID

from injector import inject

from application.services import UnitOfWork
from domain.model.result import DuelResult
from domain.repository.result import ResultCommandRepository
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import ResultSchema, MemoSchema


class SQLiteResultCommandRepository(ResultCommandRepository):
    @inject
    def __init__(self, uow: UnitOfWork):
        if not isinstance(uow, SQLiteUnitOfWork):
            raise TypeError(f"UnitOfWork の型が不正: {uow}")
        self._uow = uow
        self._logger = getLogger(__name__)

    def register(self, result: DuelResult):
        connection = self._uow.get_sqlite_connection()
        result_id_str = str(result.id)
        results_sql = " ".join([
            f"INSERT INTO {ResultSchema.TABLE_NAME} (",
            ", ".join([
                ResultSchema.Columns.ID,
                ResultSchema.Columns.REGISTERED_AT,
                ResultSchema.Columns.FIRST_OR_SECOND,
                ResultSchema.Columns.RESULT,
                ResultSchema.Columns.MY_DECK_NAME,
                ResultSchema.Columns.OPPONENT_DECK_NAME,
            ]),
            ") VALUES (?, ?, ?, ?, ?, ?);"
        ])
        results_params = (
            result_id_str,
            result.registered_at.isoformat(timespec="seconds"),
            result.first_or_second.value,
            result.result.value,
            result.my_deck_name.value,
            result.opponent_deck_name.value
        )
        self._logger.debug("\n".join([
            "register()",
            f"\tSQL: {results_sql}",
            f"\tParams: {results_params}"
        ]))
        connection.execute(results_sql, results_params)

        if not result.memo:
            return
        memos_sql = " ".join([
            f"INSERT INTO {MemoSchema.TABLE_NAME} (",
            ",".join([
                MemoSchema.Columns.RESULT_ID,
                MemoSchema.Columns.CONTENT
            ]),
            ") VALUES (?, ?);"
        ])
        memos_params = (result_id_str, result.memo.value)
        self._logger.debug("\n".join(["",
            f"\tSQL: {memos_sql}",
            f"\tParams: {memos_params}"
        ]))
        connection.execute(memos_sql, memos_params)

    def update(self, result: DuelResult):
        connection = self._uow.get_sqlite_connection()
        result_id_str = str(result.id)
        results_sql = " ".join([
            f"UPDATE {ResultSchema.TABLE_NAME} SET",
            ", ".join([
                f"{ResultSchema.Columns.FIRST_OR_SECOND} = ?",
                f"{ResultSchema.Columns.RESULT} = ?",
                f"{ResultSchema.Columns.MY_DECK_NAME} = ?",
                f"{ResultSchema.Columns.OPPONENT_DECK_NAME} = ?"
            ]),
            f"WHERE {ResultSchema.Columns.ID} = ?;"
        ])
        results_params = (
            result.first_or_second.value,
            result.result.value,
            result.my_deck_name.value,
            result.opponent_deck_name.value,
            result_id_str
        )
        self._logger.debug("\n".join([
            "update()",
            f"\tSQL: {results_sql}",
            f"\tParams: {results_params}"
        ]))
        connection.execute(results_sql, results_params)

        # 渡された result にメモが無かった場合は削除
        if not result.memo:
            memos_delete_sql = " ".join([
                f"DELETE FROM {MemoSchema.TABLE_NAME}",
                f"WHERE {MemoSchema.Columns.RESULT_ID} = ?;"
            ])
            memos_params = (result_id_str,)
            self._logger.debug("\n"
                f"\tSQL: {memos_delete_sql}\n"
                f"\tParams: {memos_params}"
            )
            connection.execute(memos_delete_sql, memos_params)
            return

        # 渡された result にメモが存在している場合は UPSERT
        memos_upsert_sql = " ".join([
            f"INSERT INTO {MemoSchema.TABLE_NAME} (",
            ",".join([
                MemoSchema.Columns.RESULT_ID,
                MemoSchema.Columns.CONTENT
            ]),
            ") VALUES (?, ?)",
            f"ON CONFLICT({MemoSchema.Columns.RESULT_ID})",
            f"DO UPDATE SET {MemoSchema.Columns.CONTENT}",
            f"= excluded.{MemoSchema.Columns.CONTENT};"
        ])
        memos_params = (result_id_str, result.memo.value)
        self._logger.debug("\n"
            f"\tSQL: {memos_upsert_sql}\n"
            f"\tParams: {memos_params}"
        )
        connection.execute(memos_upsert_sql, memos_params)

    def delete_by_id(self, id: UUID):
        sql = " ".join([
            f"DELETE FROM {ResultSchema.TABLE_NAME}",
            f"WHERE {ResultSchema.Columns.ID} = ?"
        ])
        param = (str(id),)
        self._logger.debug("\n".join([
            "delete_by_id()",
            f"\tSQL: {sql}",
            f"\tParam: {param}"
        ]))
        connection = self._uow.get_sqlite_connection()
        connection.execute(sql, param)
