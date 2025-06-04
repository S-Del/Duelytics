from logging import getLogger
from sqlite3 import connect, Error as SQLiteError

from infrastructure.sqlite.config import (
    DatabaseFilePath, ResultSchema, MemoSchema
)


logger = getLogger(__name__)


def create_database(path: DatabaseFilePath):
    logger.info(f"データベースが存在しないため作成を開始: {path}")
    try:
        with connect(path):
            pass
    except SQLiteError as e:
        logger.error(f"データベース作成エラー: {e}")
        raise
    logger.info("データベース作成完了")


def create_result_table(path: DatabaseFilePath):
    registered_at_format = '%Y-%m-%dT%H:%M:%S'
    sql = " ".join([
        f"CREATE TABLE IF NOT EXISTS {ResultSchema.TABLE_NAME} (",
        ResultSchema.Columns.ID,
        "TEXT UNIQUE NOT NULL PRIMARY KEY",
        f"CHECK ({ResultSchema.Columns.ID} <> ''),",
        ResultSchema.Columns.REGISTERED_AT,
        "TEXT NOT NULL",
        f"CHECK (strftime('{registered_at_format}',",
        f"{ResultSchema.Columns.REGISTERED_AT})",
        f"= {ResultSchema.Columns.REGISTERED_AT}),",
        ResultSchema.Columns.FIRST_OR_SECOND,
        "TEXT NOT NULL",
        f"CHECK ({ResultSchema.Columns.FIRST_OR_SECOND} <> ''),",
        ResultSchema.Columns.RESULT,
        "TEXT NOT NULL",
        f"CHECK ({ResultSchema.Columns.RESULT} <> ''),",
        ResultSchema.Columns.MY_DECK_NAME,
        "TEXT NOT NULL",
        f"CHECK ({ResultSchema.Columns.MY_DECK_NAME} <> ''),",
        ResultSchema.Columns.OPPONENT_DECK_NAME,
        "TEXT NOT NULL",
        f"CHECK ({ResultSchema.Columns.OPPONENT_DECK_NAME} <> ''))"
    ])
    logger.info(f"試合結果テーブル作成開始: {ResultSchema.TABLE_NAME}")
    logger.debug(f"\n\tsql: {sql}")
    with connect(path) as conn:
        try:
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"試合結果テーブル作成失敗: {e}")
            raise
        logger.info("試合結果テーブル作成完了")

        sql = " ".join([
            "CREATE INDEX IF NOT EXISTS",
            ResultSchema.Indexes.REGISTERED_AT,
            f"ON {ResultSchema.TABLE_NAME}",
            f"({ResultSchema.Columns.REGISTERED_AT} DESC)"
        ])
        logger.info(
            "登録日時カラムのインデックス作成開始: "
            f"{ResultSchema.Indexes.REGISTERED_AT}"
        )
        logger.debug(f"\n\tsql: {sql}")
        try:
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"インデックスの作成に失敗: {e}")
            raise
        logger.info("登録日時カラムのインデックス作成完了")


def create_memo_table(path: DatabaseFilePath):
    sql = " ".join([
        f"CREATE TABLE IF NOT EXISTS {MemoSchema.TABLE_NAME} (",
        MemoSchema.Columns.RESULT_ID,
        "TEXT UNIQUE NOT NULL PRIMARY KEY",
        f"CHECK ({MemoSchema.Columns.RESULT_ID} <> ''),",
        MemoSchema.Columns.CONTENT,
        "TEXT NOT NULL",
        f"CHECK ({MemoSchema.Columns.CONTENT} <> ''),",
        f"FOREIGN KEY ({MemoSchema.Columns.RESULT_ID})",
        f"REFERENCES {ResultSchema.TABLE_NAME}",
        f"({ResultSchema.Columns.ID}) ON DELETE CASCADE)"
    ])
    logger.info(f"メモテーブル作成開始: {MemoSchema.TABLE_NAME}")
    logger.debug(f"\n\tsql: {sql}")
    with connect(path) as conn:
        try:
            # results テーブルの ID に notes テーブルの ID が紐づく
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"メモテーブル作成失敗: {e}")
            raise
    logger.info("メモテーブル作成完了")


def init_sqlite(path: DatabaseFilePath):
    if path.exists():
        logger.info("データベースが存在するため作成をスキップ")
        return

    create_database(path)
    create_result_table(path)
    create_memo_table(path)
