from injector import inject
from logging import getLogger

from domain.repository import UnitOfWork
from domain.repository.deck import DeckCommandRepository
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config.table import DeckTableConfig


class SQLiteDeckCommandRepository(DeckCommandRepository):
    @inject
    def __init__(self, uow: UnitOfWork):
        if not isinstance(uow, SQLiteUnitOfWork):
            raise TypeError(f"UnitOfWork の型が不正 {uow}")
        self._uow = uow
        self._logger = getLogger()

    @property
    def uow(self) -> SQLiteUnitOfWork:
        return self._uow

    def register_all(self, *names: str):
        if not names:
            self._logger.warning("デッキ名のリストが空")
            return
        sql = f"INSERT INTO {DeckTableConfig.TABLE_NAME} VALUES (?)"
        params = [(name,) for name in names]
        self._logger.debug("\n".join([
            "register_all()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.executemany(sql, params)

    def register(self, name: str):
        sql = f"INSERT INTO {DeckTableConfig.TABLE_NAME} VALUES (?)"
        param = (name,)
        self._logger.debug("\n".join([
            "register()",
            f"\tsql: {sql}",
            f"\tparam: {param}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, param)
