from logging import getLogger
from sqlite3 import connect, Row
from uuid import UUID

from domain.model.note import Note
from domain.repository.note import NoteQueryRepository
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import NoteTableConfig


class SQLiteNoteQueryRepository(NoteQueryRepository):
    def __init__(self):
        self._logger = getLogger(__name__)

    def search_by_id(self, id: UUID) -> Note | None:
        sql = " ".join([
            f"SELECT * FROM {NoteTableConfig.TABLE_NAME}",
            f"WHERE {NoteTableConfig.COLUMN_NAMES.ID} = ?"
        ])
        param = (str(id),)
        self._logger.debug("\n".join([
            f"search_by_id()",
            f"\tsql: {sql}",
            f"\tparam: {param}"
        ]))

        with connect(DatabaseConfig.DATABASE_NAME) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            cursor.execute(sql, param)
            data = cursor.fetchone()

        if not data:
            return

        return Note(
            UUID(data[NoteTableConfig.COLUMN_NAMES.ID]),
            data[NoteTableConfig.COLUMN_NAMES.NOTE]
        )
