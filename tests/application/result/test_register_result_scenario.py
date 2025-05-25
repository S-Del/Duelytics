from datetime import datetime
from sqlite3 import Error as SQLiteError
from typing import cast
from unittest.mock import MagicMock
from uuid import UUID

from pytest import raises

from application.deck.register.use_case import RegisterDeckIfNotExists
from application.exception.application_critical_error import ApplicationCriticalError
from application.result.register import (
    RegisterResultCommand, RegisterResultScenario
)
from application.services import UnitOfWork
from domain.model.note import Note
from domain.model.result import DuelResult
from domain.repository.note import NoteCommandRepository
from domain.repository.result import ResultCommandRepository


def test_register_result_scenario_success(
    register_result_scenario: RegisterResultScenario,
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
    note_command_repository_mock: NoteCommandRepository,
    register_deck_if_not_exists_mock: RegisterDeckIfNotExists
):
    command = RegisterResultCommand(
        first_or_second='F',
        result='W',
        my_deck_name="自分のデッキ",
        opponent_deck_name="相手のデッキ"
    )
    register_result_scenario.execute(command)

    cast(MagicMock, uow_mock.__enter__).assert_called_once()
    cast(
        MagicMock, uow_mock.__exit__
    ).assert_called_once_with(None, None, None)
    cast(
        MagicMock, result_command_repository_mock.register
    ).assert_called_once()
    called_duel_result = cast(
        MagicMock, result_command_repository_mock.register
    ).call_args[0][0] # 位置引数の 0 番目の引数を取得
    assert isinstance(called_duel_result, DuelResult)
    assert isinstance(called_duel_result.id_raw, UUID)
    assert isinstance(called_duel_result.registered_at, datetime)
    assert called_duel_result.first_or_second.value == 'F'
    assert called_duel_result.result.value == 'W'
    assert called_duel_result.my_deck_name.value == "自分のデッキ"
    assert called_duel_result.opponent_deck_name.value == "相手のデッキ"

    # メモは登録していないので呼ばれない
    cast(
        MagicMock, note_command_repository_mock.register
    ).assert_not_called()

    deck_calls = cast(
        MagicMock, register_deck_if_not_exists_mock.handle
    ).call_args_list
    assert len(deck_calls) == 2 # 自分のデッキ名と相手デッキ名で 2 回
    called_deck_names = { call[0][0].name for call in deck_calls }
    assert called_deck_names == { "自分のデッキ", "相手のデッキ"}


def test_register_result_scenario_success_with_note(
    register_result_scenario: RegisterResultScenario,
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
    note_command_repository_mock: NoteCommandRepository,
    register_deck_if_not_exists_mock: RegisterDeckIfNotExists
):
    command = RegisterResultCommand(
        first_or_second='F',
        result='W',
        my_deck_name="自分のデッキ",
        opponent_deck_name="相手のデッキ",
        note="メモ"
    )
    register_result_scenario.execute(command)

    cast(MagicMock, uow_mock.__enter__).assert_called_once()
    cast(
        MagicMock, uow_mock.__exit__
    ).assert_called_once_with(None, None, None)
    cast(
        MagicMock, result_command_repository_mock.register
    ).assert_called_once()
    called_duel_result = cast(
        MagicMock, result_command_repository_mock.register
    ).call_args[0][0]
    assert isinstance(called_duel_result, DuelResult)
    assert isinstance(called_duel_result.id_raw, UUID)
    assert isinstance(called_duel_result.registered_at, datetime)
    assert called_duel_result.first_or_second.value == 'F'
    assert called_duel_result.result.value == 'W'
    assert called_duel_result.my_deck_name.value == "自分のデッキ"
    assert called_duel_result.opponent_deck_name.value == "相手のデッキ"

    cast(MagicMock, note_command_repository_mock.register).assert_called_once()
    called_note = cast(
        MagicMock, note_command_repository_mock.register
    ).call_args[0][0]
    assert isinstance(called_note, Note)
    assert called_note.content == "メモ"

    deck_calls = cast(
        MagicMock, register_deck_if_not_exists_mock.handle
    ).call_args_list
    assert len(deck_calls) == 2
    called_deck_names = { call[0][0].name for call in deck_calls }
    assert called_deck_names == { "自分のデッキ", "相手のデッキ"}


def test_register_result_scenario_on_sqlite_error(
    register_result_scenario: RegisterResultScenario,
    uow_mock: UnitOfWork,
    result_command_repository_mock: ResultCommandRepository,
    note_command_repository_mock: NoteCommandRepository,
    register_deck_if_not_exists_mock: RegisterDeckIfNotExists
):
    command = RegisterResultCommand(
        first_or_second='F',
        result='W',
        my_deck_name="自分のデッキ",
        opponent_deck_name="相手のデッキ",
        note="メモ"
    )
    cast(
        MagicMock, result_command_repository_mock.register
    ).side_effect = SQLiteError("DB エラーテスト")

    with raises(ApplicationCriticalError):
        register_result_scenario.execute(command)
    exit_args = cast(
        MagicMock, uow_mock.__exit__
    ).call_args[0]
    assert exit_args[0] is not None
    assert issubclass(exit_args[0], SQLiteError)
    cast(MagicMock, note_command_repository_mock.register).assert_not_called()
    cast(
        MagicMock, register_deck_if_not_exists_mock.handle
    ).assert_not_called()
