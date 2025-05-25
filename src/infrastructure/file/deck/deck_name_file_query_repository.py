from logging import getLogger
from injector import inject

from domain.repository.deck import DeckNameQueryRepository
from domain.shared.unit import NonEmptyStr
from infrastructure.file.deck.exceptions import (
    DeckNameFileNotFoundError, DeckNameFileReadError
)
from . import DeckNameFilePath, DeckNameFileParser


class DeckNameFileQueryRepository(DeckNameQueryRepository):
    @inject
    def __init__(self, path: DeckNameFilePath, parser: DeckNameFileParser):
        self._path = path
        self._parser = parser
        self._logger = getLogger(__name__)

    def _try_get_decks(self) -> set[NonEmptyStr]:
        try:
            with open(self._path, 'r', encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError as fne:
            msg = f"デッキ名ファイルが見つからなかった: {fne}"
            self._logger.error(msg, exc_info=True)
            raise DeckNameFileNotFoundError(msg) from fne
        except OSError as ose:
            msg = f"デッキ名ファイルの読み取りに失敗: {ose}"
            self._logger.error(msg, exc_info=True)
            raise DeckNameFileReadError(msg) from ose
        return self._parser.parse_lines(lines)

    def exists(self, name: NonEmptyStr) -> bool:
        decks = self._try_get_decks()
        return name in decks

    def read_all(self) -> set[NonEmptyStr]:
        return self._try_get_decks()
