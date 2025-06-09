from pathlib import Path
from pytest import fixture

from infrastructure.file.deck import DeckNameFileParser
from infrastructure.sqlite import SQLiteUnitOfWork, ReferenceData
from infrastructure.sqlite.config import DatabaseFilePath
from infrastructure.sqlite.result import (
    SearchConditionBuilder,
    SQLiteResultCommandRepository,
    SQLiteResultQueryRepository
)
from infrastructure.sqlite.setup import apply_migrations, create_reference_data


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
    apply_migrations(temp_database_file_path)
    initialized_db_path = temp_database_file_path
    return initialized_db_path


@fixture(scope="function")
def reference_data(db_with_schema: DatabaseFilePath) -> ReferenceData:
    return create_reference_data(db_with_schema)


@fixture
def uow(db_with_schema) -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork(db_with_schema)


@fixture
def builder(reference_data: ReferenceData):
    return SearchConditionBuilder(reference_data)


@fixture
def command_repository(uow: SQLiteUnitOfWork, reference_data: ReferenceData):
    return SQLiteResultCommandRepository(uow, reference_data)


@fixture
def query_repository(
    db_with_schema: DatabaseFilePath,
    reference_data: ReferenceData,
    builder: SearchConditionBuilder
) -> SQLiteResultQueryRepository:
    return SQLiteResultQueryRepository(db_with_schema, reference_data, builder)
