from logging import getLogger
from sqlite3 import connect, Connection, Error, OperationalError

from infrastructure.sqlite import ReferenceData
from infrastructure.sqlite.config import (
    DatabaseFilePath, FirstOrSecondTypesSchema, ResultTypesSchema
)
from infrastructure.sqlite.migrations.registry import MIGRATIONS


logger = getLogger(__name__)


def _get_current_version(conn: Connection) -> int:
    """現在のデータベースのバージョンを取得する。

    バージョン管理テーブルがなければ作成する。
    """
    try:
        cursor = conn.execute("SELECT version FROM _schema_version LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else 0
    except OperationalError:
        logger.info(
            "バージョン管理テーブル (_schema_version) が見つからないため、"
            "新規作成します。"
        )
        # バージョン管理テーブルを作成し、初期バージョン0を登録
        conn.execute("CREATE TABLE _schema_version (version INTEGER NOT NULL)")
        conn.execute("INSERT INTO _schema_version (version) VALUES (0)")
        return 0


def _set_current_version(conn: Connection, version: int):
    """データベースのバージョンを設定する"""
    conn.execute("UPDATE _schema_version SET version = ?", (version,))


def apply_migrations(db_path: DatabaseFilePath):
    """自作のマイグレーションシステムを適用する"""
    logger.info("データベースマイグレーションの確認と適用を開始します。")
    logger.info(f"対象データベース: {db_path}")

    try:
        with connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            current_version = _get_current_version(conn)
            logger.info(f"現在のデータベースバージョン: {current_version}")

            # 適用すべきマイグレーションを特定
            # MIGRATIONSリストの、current_version番目以降のスライスを取得
            migrations_to_apply = MIGRATIONS[current_version:]

            if not migrations_to_apply:
                logger.info("適用する新しいマイグレーションはありません。")
                return

            new_version_start = current_version + 1
            target_version_list = list(
                range(
                    new_version_start,
                    new_version_start + len(migrations_to_apply)
                )
            )
            logger.info(f"適用対象のバージョン: {target_version_list}")

            # enumerateを使って、新しいバージョン番号とマイグレーションモジュールを取得
            for version, migration in enumerate(
                migrations_to_apply,
                start=new_version_start
            ):
                logger.info(
                    f"バージョン {version} のマイグレーションを適用します..."
                )
                conn.executescript(migration.SQL)
                _set_current_version(conn, version)
                logger.info(f"バージョン {version} を適用しました。")

            logger.info("データベースマイグレーションが正常に完了しました。")
    except Error as e:
        logger.critical(
            f"データベースマイグレーション中にエラーが発生しました: {e}",
            exc_info=True
        )
        raise


def create_reference_data(db_path: DatabaseFilePath) -> ReferenceData:
    """参照テーブルからマッピングデータを読み込み、ReferenceDataを生成する。"""
    logger.info("参照データの読み込みを開始します。")
    try:
        # withステートメントで接続を管理し、処理が終わると自動で閉じる
        with connect(db_path) as conn:
            cursor = conn.cursor()

            # FirstOrSecond のマッピングを作成
            cursor.execute(
                f"SELECT id, code FROM {FirstOrSecondTypesSchema.TABLE_NAME}"
            )
            first_or_second_rows = cursor.fetchall()
            first_or_second_code_to_id = {
                row[1]: row[0] for row in first_or_second_rows
            }
            first_or_second_id_to_code = {
                row[0]: row[1] for row in first_or_second_rows
            }
            logger.debug(
                "FirstOrSecond マッピング完了\n"
                f"\tcode to id: {first_or_second_code_to_id}\n"
                f"\tid to code: {first_or_second_id_to_code}"
            )

            # ResultChar のマッピングを作成
            cursor.execute(
                f"SELECT id, code FROM {ResultTypesSchema.TABLE_NAME}"
            )
            result_rows = cursor.fetchall()
            result_char_code_to_id = {row[1]: row[0] for row in result_rows}
            result_char_id_to_code = {row[0]: row[1] for row in result_rows}
            logger.debug(
                "ResultChar マッピング完了\n"
                f"\tcode to id: {result_char_code_to_id}\n"
                f"\tid to code: {result_char_id_to_code}"
            )

            reference_data = ReferenceData(
                first_or_second_code_to_id=first_or_second_code_to_id,
                first_or_second_id_to_code=first_or_second_id_to_code,
                result_char_code_to_id=result_char_code_to_id,
                result_char_id_to_code=result_char_id_to_code
            )
            logger.info("参照データの読み込みが完了しました。")
            return reference_data
    except Error as e:
        logger.critical(
            f"参照データの読み込み中にエラーが発生しました: {e}",
            exc_info=True
        )
        raise
