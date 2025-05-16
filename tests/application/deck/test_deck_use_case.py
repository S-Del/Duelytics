from sqlite3 import connect
from pytest import fixture, raises, mark

from application.deck.fetch.use_case import FetchAllDeckName
from application.deck.register.use_case import (
    RegisterDeckCommand, RegisterDeckIfNotExists
)
from application.exception import InvalidCommandError
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import DeckTableConfig
from infrastructure.sqlite.deck import (
    SQLiteDeckCommandRepository, SQLiteDeckQueryRepository
)


# use_case や command_repository に delete_all は存在しない為ここで定義
def delete_all():
    sql = f"DELETE FROM {DeckTableConfig.TABLE_NAME}"
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(sql)
        conn.commit()


@fixture
def uow() -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork()


@fixture
def query_repository() -> SQLiteDeckQueryRepository:
    return SQLiteDeckQueryRepository()


@fixture
def command_repository(uow: SQLiteUnitOfWork) -> SQLiteDeckCommandRepository:
    return SQLiteDeckCommandRepository(uow)


@fixture
def register_deck(
    uow: SQLiteUnitOfWork,
    query_repository: SQLiteDeckQueryRepository,
    command_repository: SQLiteDeckCommandRepository
) -> RegisterDeckIfNotExists:
    return RegisterDeckIfNotExists(uow, query_repository, command_repository)


@fixture
def fetch_all_deck(
    query_repository: SQLiteDeckQueryRepository
) -> FetchAllDeckName:
    return FetchAllDeckName(query_repository)


@mark.parametrize(
    "invalid_name",
    (
        "", " ", "\t", "\r", "\n", "\r\n"
    )
)
def test_register_invalid_names(invalid_name):
    with raises(InvalidCommandError):
        RegisterDeckCommand(invalid_name)


def test_register_and_fetch(
    register_deck: RegisterDeckIfNotExists,
    fetch_all_deck: FetchAllDeckName
):
    delete_all()
    zero = fetch_all_deck.handle()
    assert len(zero) == 0

    register_deck.handle(RegisterDeckCommand("メタビート"))
    one = fetch_all_deck.handle()
    assert len(one) == 1
    assert "メタビート" in one

    register_deck.handle(RegisterDeckCommand("メタビート"))
    one = fetch_all_deck.handle()
    assert len(one) == 1
