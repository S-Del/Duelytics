from sqlite3 import connect
from pytest import fixture

from application.deck.register.use_case import RegisterDeckIfNotExists
from application.result import IdForResult
from application.result.delete.use_case import DeleteResultById
from application.result.edit import EditResultCommand, EditResultScenario
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
def note_query_repository() -> SQLiteNoteQueryRepository:
    return SQLiteNoteQueryRepository()


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
def builder() -> SearchConditionBuilder:
    return SearchConditionBuilder()


@fixture
def result_query_repository(builder) -> SQLiteResultQueryRepository:
    return SQLiteResultQueryRepository(builder)


@fixture
def fetch_result(
    result_query_repository: SQLiteResultQueryRepository
) -> FetchResultWithRecord:
    return FetchResultWithRecord(result_query_repository)


@fixture
def fetch_result_by_id(
    result_query_repository: SQLiteResultQueryRepository
) -> FetchResultById:
    return FetchResultById(result_query_repository)


# 全件削除のユースケースやリポジトリのメソッドは存在しない為ここで定義。
@fixture
def delete_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(f"DELETE FROM {ResultTableConfig.TABLE_NAME}")
        conn.commit()


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


def test_register_result(
    delete_all, # 全件削除
    register_result: RegisterResultScenario,
    fetch_result: FetchResultWithRecord
):
    # 最初に全件検索して 0 件であることを検証
    response = fetch_result.handle({})
    assert response is None

    # 登録を検証
    register_result.execute(RegisterResultCommand('F', 'W', "TEST"))
    response = fetch_result.handle({})
    assert response
    assert len(response.data_list) == 1
    assert response.data_list[0].first_or_second_raw == 'F'
    assert response.data_list[0].result_raw == 'W'
    assert response.data_list[0].my_deck_name == "TEST"
    assert response.data_list[0].opponent_deck_name == "不明"
    assert response.data_list[0].note == ""


@fixture
def edit_result(
    uow: SQLiteUnitOfWork,
    result_command_repository: SQLiteResultCommandRepository,
    note_command_repository: SQLiteNoteCommandRepository,
    note_query_repository: SQLiteNoteQueryRepository,
    register_deck: RegisterDeckIfNotExists
) -> EditResultScenario:
    return EditResultScenario(
        uow,
        result_command_repository,
        note_command_repository,
        note_query_repository,
        register_deck
    )


@fixture
def delete_result_by_id(
    uow: SQLiteUnitOfWork,
    result_command_repository: SQLiteResultCommandRepository
) -> DeleteResultById:
    return DeleteResultById(uow, result_command_repository)


def test_edit_and_delete_result(
    delete_all, # 全件削除
    fetch_result: FetchResultWithRecord,
    register_result: RegisterResultScenario,
    edit_result: EditResultScenario,
    fetch_result_by_id: FetchResultById,
    delete_result_by_id: DeleteResultById
):
    # 全件検索して 0 件であることを検証
    response = fetch_result.handle({})
    assert response is None

    # テスト用データの登録と検索の検証
    register_result.execute(
        RegisterResultCommand(
            'F', 'W',
            "NAME FOR EDIT",
            note="NOTE FOR EDIT"
        )
    )
    response = fetch_result.handle({})
    assert response is not None
    assert len(response.data_list) == 1
    target = response.data_list[0]
    assert target.first_or_second_raw == 'F'
    assert target.result_raw == 'W'
    assert target.my_deck_name == "NAME FOR EDIT"
    assert target.opponent_deck_name == "不明"
    assert target.note == "NOTE FOR EDIT"

    # テスト用データの ID を指定し、試合結果を変更。
    edit_result.handle(
        EditResultCommand(
            target.id,
            'S',
            'L',
            "EDITED MY DECK NAME",
            "EDITED OPPONENT DECK NAME",
            "EDITED NOTE"
        )
    )
    id_for_result = IdForResult(target.id)
    edited = fetch_result_by_id.handle(id_for_result)
    assert edited is not None
    assert edited.first_or_second_raw == 'S'
    assert edited.result_raw == 'L'
    assert edited.my_deck_name == "EDITED MY DECK NAME"
    assert edited.opponent_deck_name == "EDITED OPPONENT DECK NAME"
    assert edited.note == "EDITED NOTE"

    delete_result_by_id.handle(id_for_result)
    deleted = fetch_result_by_id.handle(id_for_result)
    assert deleted is None
