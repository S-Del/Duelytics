from injector import inject
from logging import getLogger
from sqlite3 import IntegrityError

from domain.repository import UnitOfWork
from domain.repository.deck import DeckCommandRepository, DeckQueryRepository
from . import RegisterDeckCommand


class RegisterDeckIfNotExists:
    @inject
    def __init__(self,
        uow: UnitOfWork,
        query_repository: DeckQueryRepository,
        command_repository: DeckCommandRepository
    ):
        self.uow = uow
        self.query_repository = query_repository
        self.command_repository = command_repository
        self._logger = getLogger()

    def handle(self, command: RegisterDeckCommand):
        try:
            if self.query_repository.exists(command.name):
                self._logger.info(
                    f"登録済みデッキ名のためスキップ: {command.name}"
                )
                return

            with self.uow:
                self.command_repository.register(command.name)
        except IntegrityError as ie:
            message = str(ie).lower()
            # 重複チェック後の重複エラーは「明らかに異常」なので、
            # 「基本的には起こらない」事を期待している。
            # 万が一起きた時の為に「特別」にログを取るため、
            # 醜悪ではあるがエラーメッセージ内の文字列で判定している。
            if "unique constraint failed" in message:
                self._logger.critical(
                    f"重複チェック後に発生した重複エラー: {ie}",
                    exc_info=True
                )
            # 最終的にどの IntegrityError も再送出する
            raise
