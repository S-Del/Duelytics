from pathlib import Path

from pytest import raises

from domain.shared.unit.non_empty_str import NonEmptyStr
from infrastructure.file.deck import (
    DeckNameFilePath, DeckNameFileParser, DeckNameFileQueryRepository
)
from infrastructure.file.deck.exceptions.deck_name_file_not_found_error import DeckNameFileNotFoundError


def test_exists(
    temp_deck_file_path: Path,
    deck_name_file_parser: DeckNameFileParser
):
    temp_deck_file_path.write_text("\n".join(['A', "BB"]))
    repository = DeckNameFileQueryRepository(
        DeckNameFilePath(temp_deck_file_path), deck_name_file_parser
    )

    assert repository.exists(NonEmptyStr('A')) == True
    assert repository.exists(NonEmptyStr("BB")) == True
    assert repository.exists(NonEmptyStr('X')) == False


def test_find_all(
    temp_deck_file_path: Path,
    deck_name_file_parser: DeckNameFileParser
):
    temp_deck_file_path.write_text("\n".join(['A', 'B', 'C']))
    repository = DeckNameFileQueryRepository(
        DeckNameFilePath(temp_deck_file_path), deck_name_file_parser
    )

    expected_decks = { NonEmptyStr('A'), NonEmptyStr('B'), NonEmptyStr('C') }
    assert repository.read_all() == expected_decks


def test_non_existent_file(
    temp_deck_file_path: Path,
    deck_name_file_parser: DeckNameFileParser
):
    path = DeckNameFilePath(temp_deck_file_path)
    assert not path.exists()

    repository = DeckNameFileQueryRepository(path, deck_name_file_parser)

    with raises(DeckNameFileNotFoundError) as exc_info:
        repository.exists(NonEmptyStr('file not found'))
    assert "デッキ名ファイルが見つからなかった" in str(exc_info.value)
    with raises(DeckNameFileNotFoundError) as exc_info:
        repository.read_all()
    assert "デッキ名ファイルが見つからなかった" in str(exc_info.value)
