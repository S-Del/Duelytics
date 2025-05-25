from pytest import raises
from typing import cast
from unittest.mock import MagicMock

from application.deck.register.use_case import (
    RegisterDeckCommand, RegisterDeckIfNotExists
)
from application.exception import ApplicationOperationWarning
from application.services.file import IDeckNameFileInitializer
from domain.repository.deck import (
    DeckNameCommandRepository, DeckNameQueryRepository
)
from domain.shared.unit import NonEmptyStr
from infrastructure.file.deck.exceptions import (
    DeckNameFileCreationError,
    DeckNameFileNotFoundError,
    DeckNameFileReadError,
    DeckNameFileWriteError
)


def test_register_deck_if_not_exists_success(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_name_command_repository_mock: DeckNameCommandRepository,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    deck_name = "DECK_NAME"
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).return_value = False
    register_deck_if_not_exists.handle(RegisterDeckCommand(deck_name))

    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).assert_called_once_with(NonEmptyStr(deck_name))
    cast(
        MagicMock, deck_name_command_repository_mock.add
    ).assert_called_once_with(NonEmptyStr(deck_name))


def test_register_deck_if_exists_expected_none(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_name_command_repository_mock: DeckNameCommandRepository,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    deck_name = "DECK_NAME"
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).return_value = True
    ret = register_deck_if_not_exists.handle(RegisterDeckCommand(deck_name))

    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).assert_called_once_with(NonEmptyStr(deck_name))
    cast(
        MagicMock, deck_name_command_repository_mock.add
    ).assert_not_called()
    assert ret is None


def test_register_deck_with_deck_name_file_not_found(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_file_initializer_mock: IDeckNameFileInitializer,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).side_effect = DeckNameFileNotFoundError()

    with raises(ApplicationOperationWarning) as exc_info:
        register_deck_if_not_exists.handle(RegisterDeckCommand("TEST"))
    cast(
        MagicMock, deck_file_initializer_mock.execute
    ).assert_called_once()
    assert "デッキ名ファイルが再作成されました。" in str(exc_info.value)


def test_register_deck_with_file_not_found_and_creation_error(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_file_initializer_mock: IDeckNameFileInitializer,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).side_effect = DeckNameFileNotFoundError()
    cast(
        MagicMock, deck_file_initializer_mock.execute
    ).side_effect = DeckNameFileCreationError()

    with raises(ApplicationOperationWarning) as exc_info:
        register_deck_if_not_exists.handle(RegisterDeckCommand("TEST"))
    assert "デッキ名ファイルの作成に失敗" in str(exc_info.value)


def test_register_deck_with_deck_name_file_read_error(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_file_initializer_mock: IDeckNameFileInitializer,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).side_effect = DeckNameFileReadError()

    with raises(ApplicationOperationWarning) as exc_info:
        register_deck_if_not_exists.handle(RegisterDeckCommand("TEST"))
    cast(
        MagicMock, deck_file_initializer_mock.execute
    ).assert_not_called()
    assert "デッキ名ファイルの読み書きエラー" in str(exc_info.value)


def test_register_deck_with_deck_name_file_write_error(
    deck_name_query_repository_mock: DeckNameQueryRepository,
    deck_name_command_repository_mock: DeckNameCommandRepository,
    deck_file_initializer_mock: IDeckNameFileInitializer,
    register_deck_if_not_exists: RegisterDeckIfNotExists
):
    cast(
        MagicMock, deck_name_query_repository_mock.exists
    ).return_value = False
    cast(
        MagicMock, deck_name_command_repository_mock.add
    ).side_effect = DeckNameFileWriteError()

    with raises(ApplicationOperationWarning) as exc_info:
        register_deck_if_not_exists.handle(RegisterDeckCommand("TEST"))
    cast(
        MagicMock, deck_file_initializer_mock.execute
    ).assert_not_called()
    assert "デッキ名ファイルの読み書きエラー" in str(exc_info.value)
