from injector import inject
from logging import getLogger

from application.exception import (
    ApplicationOperationWarning, DomainObjectCreationError
)
from application.services.file import IDeckNameFileInitializer
from domain.repository.deck import (
    DeckNameCommandRepository, DeckNameQueryRepository
)
from domain.shared.unit import NonEmptyStr
from infrastructure.file.deck.exceptions import (
    DeckNameFileCreationError,
    DeckNameFileNotFoundError,
    DeckNameFileReadError,
    DeckNameFileWriteError
)
from . import RegisterDeckCommand


class RegisterDeckIfNotExists:
    @inject
    def __init__(self,
        query_repository: DeckNameQueryRepository,
        command_repository: DeckNameCommandRepository,
        deck_file_initializer: IDeckNameFileInitializer
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository
        self._deck_file_initializer = deck_file_initializer
        self._logger = getLogger()

    def handle(self, command: RegisterDeckCommand):
        self._logger.info(f"デッキ名の登録開始: {command.name}")
        try:
            if self.query_repository.exists(NonEmptyStr(command.name)):
                self._logger.info(f"登録済みデッキ名のためスキップ")
                return

            self.command_repository.add(NonEmptyStr(command.name))
        except ValueError as ve:
            # RegisterDeckCommand が生成された時点で、
            # name の値はバリデーションされているが念のため。
            msg = f"値オブジェクトの作成に失敗: {ve}"
            self._logger.error(msg, exc_info=True)
            raise DomainObjectCreationError(msg) from ve
        except DeckNameFileNotFoundError as fnfe:
            self._logger.error(f"デッキ名ファイルが存在しない: {fnfe}")
            try:
                self._deck_file_initializer.execute()
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
        except (DeckNameFileReadError, DeckNameFileWriteError) as rwe:
            msg = "デッキ名ファイルの読み書きエラー"
            self._logger.error(f"{msg}: {rwe}")
            raise ApplicationOperationWarning(
                msg,
                "デッキ名ファイルの読み込み、または書き込みが行えません。\n"
                "ファイル権限の確認をお勧めします。"
            ) from rwe
        self._logger.info("デッキ名の登録完了")
