from logging import getLogger
from uuid import UUID

from injector import inject

from domain.model.result import DuelResult
from domain.repository.result import (
    ResultCommandRepository, UpdateResultCommand
)
from domain.repository import UnitOfWork
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config.table import ResultTableConfig


class SQLiteResultCommandRepository(ResultCommandRepository):
    @inject
    def __init__(self, uow: UnitOfWork):
        if not isinstance(uow, SQLiteUnitOfWork):
            raise TypeError(f"UnitOfWork の型が不正: {uow}")
        self._uow = uow
        self._logger = getLogger()

    @property
    def uow(self) -> SQLiteUnitOfWork:
        return self._uow

    def register(self, result: DuelResult):
        sql = " ".join([
            f"INSERT INTO {ResultTableConfig.TABLE_NAME}",
            "VALUES (?, ?, ?, ?, ?, ?)"
        ])
        params = (
            result.id,
            result.registered_at_isoformat,
            result.first_or_second_raw.value,
            result.result_raw.value,
            result.my_deck_name,
            result.opponent_deck_name
        )
        self._logger.debug("\n".join([
            "register()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, params)

    def update(self, command: UpdateResultCommand):
        sql = " ".join([
            f"UPDATE {ResultTableConfig.TABLE_NAME} SET",
            ", ".join([
                f"{ResultTableConfig.COLUMN_NAMES.FIRST_OR_SECOND} = ?",
                f"{ResultTableConfig.COLUMN_NAMES.RESULT} = ?",
                f"{ResultTableConfig.COLUMN_NAMES.MY_DECK_NAME} = ?",
                f"{ResultTableConfig.COLUMN_NAMES.OPPONENT_DECK_NAME} = ?",
            ]),
            f"WHERE {ResultTableConfig.COLUMN_NAMES.ID} = ?"
        ])
        params = (
            command.first_or_second.value,
            command.result.value,
            command.my_deck_name,
            command.opponent_deck_name,
            str(command.id)
        )
        self._logger.debug("\n".join([
            "update()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))
        connection = self.uow.get_sqlite_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)

    def delete_by_id(self, id: UUID):
        sql = " ".join([
            f"DELETE FROM {ResultTableConfig.TABLE_NAME}",
            f"WHERE {ResultTableConfig.COLUMN_NAMES.ID} = ?"
        ])
        param = (str(id),)
        self._logger.debug("\n".join([
            "delete_by_id()",
            f"\tsql: {sql}",
            f"\tparam: {param}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, param)
