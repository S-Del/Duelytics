from pathlib import Path
from unittest.mock import MagicMock, patch

from pytest import raises

from infrastructure.file.deck import DeckNameFilePath, DeckNameFileInitializer
from infrastructure.file.deck.exceptions import DeckNameFileCreationError


EXPECTED_INITIAL_CONTENT = DeckNameFileInitializer.INITIAL_CONTENT


def test_execute_success(temp_deck_file_path: Path):
    path = DeckNameFilePath(temp_deck_file_path)
    assert not path.exists()

    initializer = DeckNameFileInitializer(path)
    initializer.execute()

    assert path.exists() == True
    assert path.read_text(encoding="utf-8") == EXPECTED_INITIAL_CONTENT


def test_execute_if_file_exists(temp_deck_file_path: Path):
    path = DeckNameFilePath(temp_deck_file_path)
    existing_file_content = "先に存在するファイルの内容"
    path.write_text(existing_file_content, encoding="utf-8")

    initializer = DeckNameFileInitializer(path)
    initializer.execute()

    assert path.read_text(encoding="utf-8") == existing_file_content


@patch("builtins.open")
def test_execute_on_os_error(mock_open: MagicMock, temp_deck_file_path: Path):
    mock_open.side_effect = OSError("ファイルがいっぱいですテスト")
    initializer = DeckNameFileInitializer(
        DeckNameFilePath(temp_deck_file_path)
    )

    with raises(DeckNameFileCreationError) as exc_info:
        initializer.execute()
    mock_open.assert_called_once()
    assert "ファイルがいっぱいですテスト" in str(exc_info.value.__cause__)
