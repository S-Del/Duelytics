from logging import getLogger
from sqlite3 import connect, Error as SQLiteError

from domain.repository.deck import DeckQueryRepository
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import DeckTableConfig


class SQLiteDeckQueryRepository(DeckQueryRepository):
    def __init__(self):
        self._logger = getLogger()

    def fetch_all(self) -> frozenset[str]:
        sql = f"SELECT * FROM {DeckTableConfig.TABLE_NAME}"
        self._logger.debug("\n".join(["fetch_all()", f"\tsql: {sql}"]))

        with connect(DatabaseConfig.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

        return frozenset(item[0] for item in cursor.fetchall())

    def exists(self, deck_name: str) -> bool:
        # SELECT EXISTS (SELECT 1 FROM table WHERE ...) とすることで、
        # 1 行でもマッチしたらその時点で即座に 1 を返す。
        sql = " ".join([
            "SELECT EXISTS (",
            f"SELECT 1 FROM {DeckTableConfig.TABLE_NAME}",
            f"WHERE {DeckTableConfig.COLUMN_NAMES.NAME} = ?"
            ")"
        ])
        param = (deck_name,)
        self._logger.debug("\n".join([
            "exists()",
            f"\tsql: {sql}",
            f"\tparam: {param}"
        ]))
        with connect(DatabaseConfig.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, param)
            data: tuple[int] = cursor.fetchone()

        # DB-API 2.0 仕様では fetchone が None を返す可能性があるが、
        # SELECT EXISTS (...) のクエリでは起こり得ない為、
        # if not data: のようなチェックはここでは行わない。

        return bool(data[0])
