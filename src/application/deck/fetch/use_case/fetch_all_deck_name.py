from logging import getLogger
from injector import inject

from application.exception import ApplicationOperationWarning
from domain.repository.deck import DeckNameQueryRepository
from infrastructure.file.deck import DeckNameFileInitializer
from infrastructure.file.deck.exceptions import (
    DeckNameFileCreationError, DeckNameFileNotFoundError, DeckNameFileReadError
)


class FetchAllDeckName:
    @inject
    def __init__(self,
        repository: DeckNameQueryRepository,
        initializer: DeckNameFileInitializer
    ):
        self.repository = repository
        self._initializer = initializer
        self._logger = getLogger(__name__)

    def handle(self) -> frozenset[str]:
        self._logger.info("登録済みの全てのデッキ名の取得開始")

        try:
            deck_names = frozenset(
                deck.value for deck in self.repository.read_all()
            )
        except DeckNameFileNotFoundError as fnfe:
            self._logger.error(f"デッキ名ファイルが存在しない: {fnfe}")
            try:
                self._initializer.execute()
            except DeckNameFileCreationError as dnfce:
                msg = "デッキ名ファイルの作成に失敗"
                self._logger.error(f"{msg}: {dnfce}")
                raise ApplicationOperationWarning(
                    msg,
                    "アプリは続行できますが、入力補完機能は無効になります。\n"
                    "権限やディスク容量を確認をおすすめします。"
                ) from dnfce
            raise ApplicationOperationWarning(
                "デッキ名ファイルが再作成されました。",
                "デッキ名ファイルが存在しなかった為、再作成されました。\n"
                "再作成されたファイル内容は空のため、"
                "必要に応じてファイルを編集してください。"
            ) from fnfe
        except DeckNameFileReadError as re:
            msg = "デッキ名ファイルの読み取りエラー"
            self._logger.error(f"{msg}: {re}")
            raise ApplicationOperationWarning(
                msg,
                "デッキ名ファイルの読み取りが行えません。\n"
                "ファイル権限の確認をお勧めします。"
            ) from re

        self._logger.info(f"全てのデッキ名の取得完了: {len(deck_names)} 件")

        return deck_names
