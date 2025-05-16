from pytest import fixture
from sqlite3 import connect, IntegrityError

from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import DeckTableConfig
from infrastructure.sqlite.deck import (
    SQLiteDeckCommandRepository, SQLiteDeckQueryRepository
)
from tests.helpers import expect_uow_rollback_on_error


def delete_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(f"DELETE FROM {DeckTableConfig.TABLE_NAME}")
        conn.commit()


@fixture
def uow() -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork()


@fixture
def command_repository(uow) -> SQLiteDeckCommandRepository:
    return SQLiteDeckCommandRepository(uow)


@fixture
def query_repository() -> SQLiteDeckQueryRepository:
    return SQLiteDeckQueryRepository()


def test_deck_repository(
    uow: SQLiteUnitOfWork,
    command_repository: SQLiteDeckCommandRepository,
    query_repository: SQLiteDeckQueryRepository
):
    # 全件取得し、件数が 0 であるか検証。
    delete_all()
    results = query_repository.fetch_all()
    assert len(results) == 0

    # 空文字列の登録がエラーとなるか検証
    with expect_uow_rollback_on_error(uow, IntegrityError):
        command_repository.register("")
    results = query_repository.fetch_all()
    assert len(results) == 0

    # 重複した名前が単体登録できないか検証
    ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK = "メタビート"
    with uow:
        command_repository.register(ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK)
    # トランザクションを抜けてから再度単体登録し重複によるエラーとなるか検証
    with expect_uow_rollback_on_error(uow, IntegrityError):
        command_repository.register(ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK)
    results = query_repository.fetch_all()
    assert len(results) == 1

    # 登録されたデッキ名が存在するか検証
    assert query_repository.exists(ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK) == True
    # 登録されていないデッキ名の存在確認で False になるか検証
    assert query_repository.exists("隣の客はよく柿食うバスガス爆発だ") == False

    # 複数件登録し、全件登録されているか検証。
    delete_all()
    with uow:
        command_repository.register_all(
            ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK,
            "ラビュリンス",
            "原石青眼"
        )
    results = query_repository.fetch_all()
    assert len(list(results)) == 3
    assert set(results) == {
        ULTRA_SUPER_INCREDIBLY_UNBELIEVABLY_AMAZING_DECK,
        "ラビュリンス",
        "原石青眼"
    }

    # 同名のデッキが複数同時登録されても重複して登録されないか検証
    delete_all()
    with expect_uow_rollback_on_error(uow, IntegrityError):
        command_repository.register_all("A", "A", "B")
    results = query_repository.fetch_all()
    assert len(list(results)) == 0
