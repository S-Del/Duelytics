from dataclasses import dataclass

from application.exception.invalid_command_error import InvalidCommandError


@dataclass(frozen=True)
class RegisterDeckCommand:
    name: str

    def __post_init__(self):
        try:
            self._validate_name()
        except ValueError as ve:
            raise InvalidCommandError(
                f"コマンドオブジェクトの作成に失敗"
            ) from ve

    def _validate_name(self):
        if not self.name.strip():
            raise ValueError(f"デッキ名が空か空白文字のみ: {self.name}")
