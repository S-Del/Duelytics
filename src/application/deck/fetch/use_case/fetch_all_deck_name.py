from logging import getLogger
from injector import inject
from sqlite3 import Error as SQLiteError

from application.exception import ApplicationCriticalError
from domain.repository.deck import DeckQueryRepository


class FetchAllDeckName:
    @inject
    def __init__(self, repository: DeckQueryRepository):
        self.repository = repository
        self._logger = getLogger()

    def handle(self) -> frozenset[str]:
        self._logger.info("登録済みの全てのデッキ名の取得開始")

        try:
            deck_names = self.repository.fetch_all()
        except SQLiteError as e:
            self._logger.critical(f"デッキ名の取得に失敗: {e}")
            raise ApplicationCriticalError from e

        self._logger.info(f"全てのデッキ名の取得完了: {len(deck_names)} 件")

        return deck_names
