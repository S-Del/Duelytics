from pathlib import Path
from pytest import fixture

from infrastructure.file.deck import DeckNameFileParser


@fixture
def temp_deck_file_path(tmp_path: Path) -> Path:
    test_deck_file_path = tmp_path / "TEST-decks.dnl"
    return test_deck_file_path


@fixture
def deck_name_file_parser() -> DeckNameFileParser:
    return DeckNameFileParser()
