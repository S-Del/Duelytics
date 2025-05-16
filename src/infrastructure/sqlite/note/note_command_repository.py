from uuid import UUID
from injector import inject
from logging import getLogger

from domain.model.note import Note
from domain.repository import UnitOfWork
from domain.repository.note import NoteCommandRepository
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config.table import NoteTableConfig


class SQLiteNoteCommandRepository(NoteCommandRepository):
    @inject
    def __init__(self, uow: UnitOfWork):
        if not isinstance(uow, SQLiteUnitOfWork):
            raise TypeError(f"UnitOfWork の型が不正 {uow}")
        self._uow = uow
        self._logger = getLogger()

    @property
    def uow(self) -> SQLiteUnitOfWork:
        return self._uow

    def delete_by_id(self, id: UUID):
        sql = " ".join([
            f"DELETE FROM {NoteTableConfig.TABLE_NAME}",
            f"WHERE {NoteTableConfig.COLUMN_NAMES.ID} = ?"
        ])
        param = (str(id),)
        self._logger.debug("\n".join([
            "delete_by_id()",
            f"\tsql: {sql}",
            f"\tparam: {param}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, param)

    def register(self, note: Note):
        sql = f"INSERT INTO {NoteTableConfig.TABLE_NAME} VALUES (?, ?)"
        params = (str(note.id), note.content)
        self._logger.debug("\n".join([
            "register()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, params)

    def upsert(self, note: Note):
        sql = " ".join([
            f"INSERT INTO {NoteTableConfig.TABLE_NAME} VALUES (?, ?)",
            f"ON CONFLICT({NoteTableConfig.COLUMN_NAMES.ID})",
            f"DO UPDATE SET {NoteTableConfig.COLUMN_NAMES.NOTE}",
            f"= excluded.{NoteTableConfig.COLUMN_NAMES.NOTE}"
        ])
        params = (str(note.id), note.content)
        self._logger.debug("\n".join([
            "upsert()",
            f"\tsql: {sql}",
            f"\tparams: {params}"
        ]))
        connection = self.uow.get_sqlite_connection()
        connection.execute(sql, params)
