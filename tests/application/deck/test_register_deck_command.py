from dataclasses import FrozenInstanceError
from pytest import fail, mark, raises

from application.deck.register.use_case import RegisterDeckCommand
from application.exception import InvalidCommandError


def test_register_deck_command_valid_name():
    deck_name = "メタビート"
    try:
        command = RegisterDeckCommand(deck_name)
        assert command.name == deck_name
    except InvalidCommandError:
        fail("有効なデッキ名での InvalidCommandError")
    except Exception as e:
        fail(f"予期せぬ例外: {e}")


@mark.parametrize(
    "invalid_name",
    ["", " ", "   ", "\r", "\n", "\t", "\t\t"]
)
def test_register_deck_command_invalid_names(invalid_name: str):
    with raises(InvalidCommandError) as exc_info:
        RegisterDeckCommand(invalid_name)
    assert "コマンドオブジェクトの作成に失敗" in str(exc_info.value)
    if exc_info.value.__cause__:
        assert "デッキ名が空か空白文字のみ" in str(exc_info.value.__cause__)


def test_register_deck_command_is_immutable():
    command = RegisterDeckCommand("test")
    with raises(FrozenInstanceError):
        command.name = "test" # type: ignore
