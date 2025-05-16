from sqlite3 import connect
from pytest import fixture

from application.deck.register.use_case import RegisterDeckIfNotExists
from application.result import IdForResult
from application.result.fetch import FetchResultWithRecord
from application.result.fetch.use_case import FetchResultById
from application.result.register import (
    RegisterResultCommand, RegisterResultScenario
)
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import ResultTableConfig
from infrastructure.sqlite.deck import (
    SQLiteDeckCommandRepository, SQLiteDeckQueryRepository
)
from infrastructure.sqlite.note import (
    SQLiteNoteCommandRepository, SQLiteNoteQueryRepository
)
from infrastructure.sqlite.result import (
    SearchConditionBuilder,
    SQLiteResultCommandRepository,
    SQLiteResultQueryRepository
)


# delete_all の様なユースケースやリポジトリのメソッドは存在しない為ここで定義。
@fixture
def delete_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(f"DELETE FROM {ResultTableConfig.TABLE_NAME}")
        conn.commit()


@fixture
def uow() -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork()


@fixture
def result_command_repository(
    uow: SQLiteUnitOfWork
) -> SQLiteResultCommandRepository:
    return SQLiteResultCommandRepository(uow)


@fixture
def note_command_repository(
    uow: SQLiteUnitOfWork
) -> SQLiteNoteCommandRepository:
    return SQLiteNoteCommandRepository(uow)


@fixture
def deck_command_repository(
    uow: SQLiteUnitOfWork
) -> SQLiteDeckCommandRepository:
    return SQLiteDeckCommandRepository(uow)


@fixture
def deck_query_repository() -> SQLiteDeckQueryRepository:
    return SQLiteDeckQueryRepository()


@fixture
def register_deck(
    uow: SQLiteUnitOfWork,
    deck_query_repository: SQLiteDeckQueryRepository,
    deck_command_repository: SQLiteDeckCommandRepository
) -> RegisterDeckIfNotExists:
    return RegisterDeckIfNotExists(
        uow, deck_query_repository, deck_command_repository
    )


@fixture
def register_result(
    uow: SQLiteUnitOfWork,
    result_command_repository: SQLiteResultCommandRepository,
    note_command_repository: SQLiteNoteCommandRepository,
    register_deck: RegisterDeckIfNotExists
):
    return RegisterResultScenario(
        uow,
        result_command_repository,
        note_command_repository,
        register_deck
    )


@fixture
def builder() -> SearchConditionBuilder:
    return SearchConditionBuilder()


@fixture
def result_query_repository(builder: SearchConditionBuilder) -> SQLiteResultQueryRepository:
    return SQLiteResultQueryRepository(builder)


@fixture
def fetch_result_with_record(
    result_query_repository: SQLiteResultQueryRepository
) -> FetchResultWithRecord:
    return FetchResultWithRecord(result_query_repository)


@fixture
def fetch_result_by_id(
    result_query_repository: SQLiteResultQueryRepository
) -> FetchResultById:
    return FetchResultById(result_query_repository)


def test_fetch_result_by_id(
    delete_all, # 全件削除
    fetch_result_with_record: FetchResultWithRecord,
    register_result: RegisterResultScenario,
    fetch_result_by_id: FetchResultById
):
    results = fetch_result_with_record.handle({})
    assert results is None

    register_result.execute(RegisterResultCommand('F', 'W', "TEST"))
    results = fetch_result_with_record.handle({})
    assert results is not None
    assert len(results.data_list) == 1

    src_result = results.data_list[0]
    tgt_result = fetch_result_by_id.handle(IdForResult(src_result.id))
    assert tgt_result is not None
    assert src_result.first_or_second == tgt_result.first_or_second
    assert src_result.result == tgt_result.result
    assert src_result.my_deck_name == tgt_result.my_deck_name
