from logging import getLogger
from sqlite3 import connect, Connection
from types import TracebackType

from domain.repository.unit_of_work import UnitOfWork
from infrastructure.sqlite.config import DatabaseConfig


class SQLiteUnitOfWork(UnitOfWork):
    def __init__(self):
        self._db_path = DatabaseConfig.DATABASE_NAME
        self._conn: Connection | None = None
        self._transaction_depth = 0
        self._logger = getLogger(__name__)

    def __enter__(self) -> "SQLiteUnitOfWork":
        if self._transaction_depth == 0:
            self._logger.debug("新しいコネクションを作成")
            self._conn = connect(self._db_path)
            command = "PRAGMA foreign_keys = ON"
            self._logger.debug(f'外部キー制約を有効化: "{command}"')
            self._conn.execute(command)
        self._transaction_depth += 1
        self._logger.debug(f"transaction depth: {self._transaction_depth}")

        return self

    def __exit__(self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        _: TracebackType | None
    ) -> bool | None:
        self._transaction_depth -= 1
        self._logger.debug(f"transaction depth: {self._transaction_depth}")

        if self._transaction_depth == 0 and self._conn:
            try:
                if exc_type:
                    self._logger.warning(
                        f"エラー発生、ロールバックを実行。: {exc_value}",
                        exc_info=True
                    )
                    self._conn.rollback()
                else:
                    self._logger.debug("コネクションでコミットを実行")
                    self._conn.commit()
            finally:
                self._logger.debug("コネクションをクローズ")
                self._conn.close()
                self._conn = None

        return False # 例外を抑制せず、呼び出し元に再送出する。

    def get_sqlite_connection(self) -> Connection:
        if not self._conn or self._transaction_depth == 0:
            self._logger.error("トランザクション外でのコネクションの取得")
            raise RuntimeError(
                "アクティブなコネクションかトランザクションが存在しません。\n"
                "`with UnitOfWork:` ブロック内、もしくは、"
                "`UnitOfWork.__enter__()` メソッドの完了後、"
                "このメソッド実行されているか確認してください。"
            )
        return self._conn
