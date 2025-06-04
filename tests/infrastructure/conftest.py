from pathlib import Path
from pytest import fixture

from infrastructure.file.deck import DeckNameFileParser
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseFilePath
from infrastructure.sqlite.result import (
    SearchConditionBuilder,
    SQLiteResultCommandRepository,
    SQLiteResultQueryRepository
)
from infrastructure.sqlite.setup import init_sqlite


@fixture
def temp_deck_file_path(tmp_path: Path) -> Path:
    test_deck_file_path = tmp_path / "TEST-decks.dnl"
    return test_deck_file_path


@fixture
def deck_name_file_parser() -> DeckNameFileParser:
    return DeckNameFileParser()


@fixture
def temp_database_file_path(tmp_path: Path) -> DatabaseFilePath:
    return DatabaseFilePath(tmp_path / "TEST-duelstats.db")


@fixture(scope="function")
def db_with_schema(
    temp_database_file_path: DatabaseFilePath
) -> DatabaseFilePath:
    init_sqlite(temp_database_file_path)
    initialized_db_path = temp_database_file_path
    return initialized_db_path


@fixture
def uow(db_with_schema) -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork(db_with_schema)


@fixture
def builder():
    return SearchConditionBuilder()


@fixture
def command_repository(uow):
    return SQLiteResultCommandRepository(uow)


@fixture
def query_repository(
    db_with_schema: DatabaseFilePath,
    builder: SearchConditionBuilder
) -> SQLiteResultQueryRepository:
    return SQLiteResultQueryRepository(db_with_schema, builder)
