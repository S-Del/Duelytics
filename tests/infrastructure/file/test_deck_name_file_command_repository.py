from pathlib import Path

from pytest import raises

from domain.shared.unit import NonEmptyStr
from infrastructure.file.deck import (
    DeckNameFilePath,
    DeckNameFileCommandRepository
)
from infrastructure.file.deck.exceptions import DeckNameFileNotFoundError


def test_add_to_empty_file(temp_deck_file_path: Path):
    initial_content = ""
    temp_deck_file_path.write_text(initial_content, encoding="utf-8")
    repository = DeckNameFileCommandRepository(
        DeckNameFilePath(temp_deck_file_path)
    )
    repository.add(NonEmptyStr('A'))

    after_add_content = temp_deck_file_path.read_text(encoding="utf-8")
    expected_content = initial_content + "A\n"
    assert after_add_content == expected_content


def test_add_to_existing_file(temp_deck_file_path: Path):
    initial_content = '\n'.join(['A', "BB", "CCC\n"])
    temp_deck_file_path.write_text(initial_content, encoding="utf-8")
    repository = DeckNameFileCommandRepository(
        DeckNameFilePath(temp_deck_file_path)
    )
    repository.add(NonEmptyStr("DDDD"))

    after_add_content = temp_deck_file_path.read_text(encoding="utf-8")
    expected_content = initial_content + "DDDD\n"
    assert after_add_content == expected_content


def test_non_existent_file(temp_deck_file_path: Path):
    path = DeckNameFilePath(temp_deck_file_path)
    assert not path.exists()

    repository = DeckNameFileCommandRepository(path)

    with raises(DeckNameFileNotFoundError) as exc_info:
        repository.add(NonEmptyStr("non existent file"))
    assert "デッキ名ファイルが見つからなかった" in str(exc_info.value)
