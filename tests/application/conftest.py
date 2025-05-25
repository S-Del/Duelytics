from pytest import fixture
from unittest.mock import MagicMock

from application.deck.register.use_case import RegisterDeckIfNotExists
from application.result.delete.use_case import DeleteResultById
from application.result.edit import EditResultScenario
from application.result.fetch import FetchResultWithRecord
from application.result.fetch.use_case import FetchResultById
from application.result.register import RegisterResultScenario
from application.services import UnitOfWork
from application.services.file import IDeckNameFileInitializer
from domain.repository.deck import (
    DeckNameQueryRepository, DeckNameCommandRepository
)
from domain.repository.note import NoteCommandRepository, NoteQueryRepository
from domain.repository.result import (
    ResultCommandRepository, ResultQueryRepository
)

##### モック達 #####
@fixture
def deck_name_query_repository_mock() -> MagicMock:
    return MagicMock(spec=DeckNameQueryRepository)


@fixture
def deck_name_command_repository_mock() -> MagicMock:
    return MagicMock(spec=DeckNameCommandRepository)


@fixture
def deck_file_initializer_mock() -> MagicMock:
    return MagicMock(spec=IDeckNameFileInitializer)


@fixture
def note_command_repository_mock() -> MagicMock:
    return MagicMock(spec=NoteCommandRepository)


@fixture
def note_query_repository_mock() -> MagicMock:
    return MagicMock(spec=NoteQueryRepository)


@fixture
def result_command_repository_mock() -> MagicMock:
    return MagicMock(spec=ResultCommandRepository)


@fixture
def result_query_repository_mock() -> MagicMock:
    return MagicMock(spec=ResultQueryRepository)


@fixture
def uow_mock() -> MagicMock:
    return MagicMock(spec=UnitOfWork)


##### ユースケース達 #####
@fixture
def register_deck_if_not_exists(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_name_command_repository_mock: DeckNameCommandRepository,
    deck_file_initializer_mock: IDeckNameFileInitializer
) -> RegisterDeckIfNotExists:
    return RegisterDeckIfNotExists(
        deck_name_query_repository_mock,
        deck_name_command_repository_mock,
        deck_file_initializer_mock
    )


@fixture
def register_deck_if_not_exists_mock() -> MagicMock:
    return MagicMock(spec=RegisterDeckIfNotExists)


@fixture
def fetch_result_by_id(
    result_query_repository_mock: ResultQueryRepository
) -> FetchResultById:
    return FetchResultById(result_query_repository_mock)


@fixture
def fetch_result_by_id_mock() -> MagicMock:
    return MagicMock(spec=FetchResultById)


@fixture
def delete_result_by_id(
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
) -> DeleteResultById:
    return DeleteResultById(uow_mock, result_command_repository_mock)


@fixture
def delete_result_by_id_mock() -> MagicMock:
    return MagicMock(spec=DeleteResultById)


##### シナリオ達 #####
@fixture
def fetch_result_with_record(
    result_query_repository_mock: ResultQueryRepository
) -> FetchResultWithRecord:
    return FetchResultWithRecord(result_query_repository_mock)


@fixture
def register_result_scenario(
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
    note_command_repository_mock: NoteCommandRepository,
    register_deck_if_not_exists_mock: RegisterDeckIfNotExists
) -> RegisterResultScenario:
    return RegisterResultScenario(
        uow_mock,
        result_command_repository_mock,
        note_command_repository_mock,
        register_deck_if_not_exists_mock
    )


@fixture
def edit_result_scenario(
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
    note_command_repository_mock: NoteCommandRepository,
    note_query_repository_mock: NoteQueryRepository,
    register_deck_if_not_exists: RegisterDeckIfNotExists
) -> EditResultScenario:
    return EditResultScenario(
        uow_mock,
        result_command_repository_mock,
        note_command_repository_mock,
        note_query_repository_mock,
        register_deck_if_not_exists
    )
