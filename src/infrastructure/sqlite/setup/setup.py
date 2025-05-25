from logging import getLogger
from os.path import exists
from sqlite3 import connect, Error as SQLiteError

from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import (
    ResultTableConfig,
    NoteTableConfig
)


logger = getLogger()


def create_database():
    logger.info("データベースが存在しない為作成します")
    try:
        with connect(DatabaseConfig.DATABASE_NAME):
            pass
    except SQLiteError as e:
        logger.error(f"データベース作成エラー: {e}")
        raise
    logger.info("データベース作成完了")


def create_result_table():
    sql = " ".join([
        f"CREATE TABLE IF NOT EXISTS {ResultTableConfig.TABLE_NAME} (",
        ResultTableConfig.COLUMN_NAMES.ID,
        "TEXT UNIQUE NOT NULL PRIMARY KEY",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.ID} <> ''),",
        ResultTableConfig.COLUMN_NAMES.REGISTER_DATE,
        "TEXT NOT NULL",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.REGISTER_DATE} <> ''),",
        ResultTableConfig.COLUMN_NAMES.FIRST_OR_SECOND,
        "TEXT NOT NULL",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.FIRST_OR_SECOND} <> ''),",
        ResultTableConfig.COLUMN_NAMES.RESULT,
        "TEXT NOT NULL",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.RESULT} <> ''),",
        ResultTableConfig.COLUMN_NAMES.MY_DECK_NAME,
        "TEXT NOT NULL",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.MY_DECK_NAME} <> ''),",
        ResultTableConfig.COLUMN_NAMES.OPPONENT_DECK_NAME,
        "TEXT NOT NULL",
        f"CHECK ({ResultTableConfig.COLUMN_NAMES.OPPONENT_DECK_NAME} <> ''))"
    ])
    logger.debug("\n".join([
        "create_result_table()",
        f"\tsql: {sql}"
    ]))
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        try:
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"試合結果テーブル作成失敗: {e}")
            raise
        logger.info("試合結果テーブル作成完了")

        sql = " ".join([
            "CREATE INDEX IF NOT EXISTS",
            ResultTableConfig.INDEX_NAMES.REGISTER_DATE,
            f"ON {ResultTableConfig.TABLE_NAME}",
            f"({ResultTableConfig.COLUMN_NAMES.REGISTER_DATE} DESC)"
        ])
        logger.debug("\n".join([
            "インデックスの作成開始"
            f"\tsql: {sql}"
        ]))
        try:
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"インデックスの作成に失敗: {e}")
            raise
        logger.info("登録日時カラムのインデックス作成完了")


def create_note_table():
    sql = " ".join([
        f"CREATE TABLE IF NOT EXISTS {NoteTableConfig.TABLE_NAME} (",
        NoteTableConfig.COLUMN_NAMES.ID,
        "TEXT UNIQUE NOT NULL PRIMARY KEY",
        f"CHECK ({NoteTableConfig.COLUMN_NAMES.ID} <> ''),",
        NoteTableConfig.COLUMN_NAMES.NOTE,
        "TEXT NOT NULL",
        f"CHECK ({NoteTableConfig.COLUMN_NAMES.NOTE} <> ''),",
        f"FOREIGN KEY ({NoteTableConfig.COLUMN_NAMES.ID})",
        f"REFERENCES {ResultTableConfig.TABLE_NAME}",
        f"({ResultTableConfig.COLUMN_NAMES.ID}) ON DELETE CASCADE)"
    ])
    logger.debug(f"sql: {sql}")
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        try:
            # results テーブルの ID に notes テーブルの ID が紐づく
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute(sql)
        except SQLiteError as e:
            logger.error(f"メモテーブル作成失敗: {e}")
            raise
    logger.info("メモテーブル作成完了")


def init_sqlite():
    if exists(DatabaseConfig.DATABASE_NAME):
        logger.info("既にデータベースが存在するため、作成はスキップします。")
        return

    create_database()
    create_result_table()
    create_note_table()
